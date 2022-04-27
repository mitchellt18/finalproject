#import py files
from mainMenu import *
from registerPage import *
from forgottenPage import *

#import required modules
from tkinter import *
from PIL import ImageTk, Image
import os
from pymongo import MongoClient
import bcrypt
import re
import urllib.request

global loginGUI
global username
global password
global loginCounter
loginCounter = 5

#check internet connection
def connect():
    try:
        urllib.request.urlopen('http://google.com') #attempt connection to google
        return True
    except:
        return False

#function check to ensure login details are correct
def checkDetails(loginGUI, username, password):
    global loginCounter
    #establish connection with the database
    client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('user_db')
    records = db.user_details

    checkPassword = password.get().encode('utf-8') #encode inputted password as utf-8
    #userObject = records.find_one({'username': username.get()})

    userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})

    if(username.get() == ""):
        messagebox.showwarning("Error", "Please Enter Username!")#if username left blank
        
    elif (password.get() == ""):
        messagebox.showwarning("Error", "Please Enter Password!") #if password left blank
    
    elif (not records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})):
        messagebox.showwarning("Error", "User not found") #if username not found in db

    #check if account is blocked
    elif (userObject['lock'] == True):
        messagebox.showwarning("Error", "Your account is blocked. To re-gain access, please reset the password") #message for blocked account
    
    #check inputted password is correct
    elif (not bcrypt.checkpw(checkPassword, userObject['password'])):
        if (loginCounter <= 1):
            records.find_one_and_update({'username': userObject['username']},
                                    {'$set':{'lock': True}},
                                    return_document = ReturnDocument.AFTER)
            
            messagebox.showwarning("Error", "Your Account, " + username.get() + ", has been blocked, please reset the password.") #acc blocked
            
        else:
            loginCounter = loginCounter - 1
            messagebox.showwarning("Error", "Please ensure password is correct, you have " + str(loginCounter) + " attempts remaining") #if password doesn't match in db

    else:
        mainMenu(loginGUI, False, username) #all details are correct and found, login successful
    
#first gui presented to the user when opening application
def mainScreen():
    loginGUI = Tk() #create gui
    if (connect()):
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
        
        #buttons
        
        #login
        loginImg = Image.open("./Buttons/Login/button_login.png").resize((100, 22))
        outputLogin = ImageTk.PhotoImage(loginImg)
        
        loginButton = Button(loginGUI, image = outputLogin, 
                             command=lambda: checkDetails(loginGUI, username, password))
        loginButton.image = outputLogin
        loginButton.pack()

        #forgotten
        forgottenImg = Image.open("./Buttons/Login/button_forgotten.png").resize((100, 22))
        outputForgotten = ImageTk.PhotoImage(forgottenImg)
        
        forgottenButton = Button(loginGUI, image = outputForgotten,
                                 command=lambda: forgottenPage(loginGUI, mainMenu))
        forgottenButton.image = outputForgotten
        forgottenButton.pack()

        #register
        registerImg = Image.open("./Buttons/Login/button_register.png").resize((100, 22))
        outputRegister = ImageTk.PhotoImage(registerImg)
        
        registerButton = Button(loginGUI, image = outputRegister,
                                command=lambda: registerPage(loginGUI, mainMenu))

        registerButton.image = outputRegister
        registerButton.pack()

        #offline
        offlineImg = Image.open("./Buttons/Login/button_offline-mode.png").resize((100, 22))
        outputOffline = ImageTk.PhotoImage(offlineImg)
        
        offlineButton = Button(loginGUI, image = outputOffline,
                               command=lambda: mainMenu(loginGUI, True, 'offline'))

        offlineButton.image = outputOffline
        offlineButton.pack()
        
        loginGUI.mainloop()
    else:
        messagebox.showwarning("Warning", "Your Computer Is Not Connected to the Internet. You will automatically be placed into Offline Mode")
        mainMenu(loginGUI, True, 'offline')
mainScreen()
