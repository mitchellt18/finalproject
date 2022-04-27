#import required modules
from tkinter import *
from PIL import ImageTk, Image
import os
from pymongo import MongoClient
import bcrypt
import re
import urllib.request

#import py files
from mainMenu.mainMenu import *
from Login.registerPage import *
from Login.forgottenPage import *

#global variables required
global loginGUI
global username
global password

#variable to count amount of attempted logins
global loginCounter
loginCounter = 5

#verify internet connection
def connect():
    try:
        urllib.request.urlopen('http://google.com') #attempt connection to google
        return True
    except:
        return False

#check login details
def checkDetails(loginGUI, username, password):
    global loginCounter
    
    #database code
    client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('user_db') #retrieve correct database
    records = db.user_details #retrieve correct collection

    #encode inputted password as utf-8
    checkPassword = password.get().encode('utf-8')

    #retrieve user from database
    userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})

    #if username left blank - error
    if(username.get() == ""):
        messagebox.showwarning("Error", "Please Enter Username!")

    #if password left blank - error
    elif (password.get() == ""):
        messagebox.showwarning("Error", "Please Enter Password!")

    #if username not found in db - error
    elif (not records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})):
        messagebox.showwarning("Error", "User not found")

    #if account blocked - error
    elif (userObject['lock'] == True):
        messagebox.showwarning("Error", "Your account is blocked. To re-gain access, please reset the password")
    
    #if password incorrect - error
    elif (not bcrypt.checkpw(checkPassword, userObject['password'])):
        #blocks account if loginCounter too low
        if (loginCounter <= 1):
            records.find_one_and_update({'username': userObject['username']},
                                    {'$set':{'lock': True}},
                                    return_document = ReturnDocument.AFTER)
            
            messagebox.showwarning("Error", "Your Account, " + username.get() + ", has been blocked, please reset the password.") #acc blocked
            
        else:
            #if password incorrect - reduce loginCounter by 1 and error
            loginCounter = loginCounter - 1
            messagebox.showwarning("Error", "Please ensure password is correct, you have " + str(loginCounter) + " attempts remaining")

    #login successful
    else:
        mainMenu(loginGUI, False, username) #mainMenu
    
#gui
def mainScreen():
    loginGUI = Tk() #create gui
    #if internet connection present
    if (connect()):
        #gui settings
        loginGUI.geometry("428x730") #size of window
        loginGUI.configure(bg="#C0392B") #window background colour
        loginGUI.title("Welcome to Personal Finance Management") #window title

        #titles & labels
        welcomeTitle = Label(loginGUI, text="Welcome to Personal Finance Management", bg="#C0392B", wraplengt=400)
        welcomeTitle.config(font=('Courier',25))
        welcomeTitle.pack()
        Label(loginGUI, text="Welcome Back!", bg="#C0392B").pack()
        Label(loginGUI, text="Please enter your Username and Password Below:", bg="#C0392B", wraplengt=400).pack()

        #pig image
        pigImg = Image.open("./pig.png")
        newPigImg = pigImg.resize((366, 399))
        outputPigImg = ImageTk.PhotoImage(newPigImg)
        Label(loginGUI, image = outputPigImg, bg="#C0392B").pack()

        #username
        username = StringVar()
        Label(loginGUI, text="Username", bg="#C0392B", wraplengt=400).pack()
        Entry(loginGUI, textvariable=username, width = 30, bg='white', fg='black').pack()

        #password
        password = StringVar()
        Label(loginGUI, text="Password", bg="#C0392B", wraplengt=400).pack()
        Entry(loginGUI, textvariable = password, width = 30, show="*", bg='white', fg='black').pack()
        
        #login button
        loginImg = Image.open("./Buttons/Login/button_login.png").resize((100, 22))
        outputLogin = ImageTk.PhotoImage(loginImg)
        
        loginButton = Button(loginGUI, image = outputLogin, 
                             command=lambda: checkDetails(loginGUI, username, password))
        loginButton.image = outputLogin
        loginButton.pack()

        #forgotten button
        forgottenImg = Image.open("./Buttons/Login/button_forgotten.png").resize((100, 22))
        outputForgotten = ImageTk.PhotoImage(forgottenImg)
        
        forgottenButton = Button(loginGUI, image = outputForgotten,
                                 command=lambda: forgottenPage(loginGUI, mainMenu))
        forgottenButton.image = outputForgotten
        forgottenButton.pack()

        #register button
        registerImg = Image.open("./Buttons/Login/button_register.png").resize((100, 22))
        outputRegister = ImageTk.PhotoImage(registerImg)
        
        registerButton = Button(loginGUI, image = outputRegister,
                                command=lambda: registerPage(loginGUI, mainMenu))

        registerButton.image = outputRegister
        registerButton.pack()

        #offline button
        offlineImg = Image.open("./Buttons/Login/button_offline-mode.png").resize((100, 22))
        outputOffline = ImageTk.PhotoImage(offlineImg)
        
        offlineButton = Button(loginGUI, image = outputOffline,
                               command=lambda: mainMenu(loginGUI, True, 'offline'))

        offlineButton.image = outputOffline
        offlineButton.pack()
        
        loginGUI.mainloop()
    #if no internet detected - message and offlineMode
    else:
        messagebox.showwarning("Warning", "Your Computer Is Not Connected to the Internet. You will automatically be placed into Offline Mode")
        mainMenu(loginGUI, True, 'offline')
mainScreen()
