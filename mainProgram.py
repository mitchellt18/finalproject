from mainMenu import *
from registerPage import *
from forgottenPage import *
from tkinter import *
from PIL import ImageTk, Image
import os
from pymongo import MongoClient

global loginGUI
global username
global password

#delete function below if not necessary
def login():
    print("Login Failed :(")

#function check to ensure login details are correct
def checkDetails(loginGUI, username, password):

    #establish connection with the database
    client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('user_db')
    records = db.user_details

    if(username.get() == ""):
        messagebox.showwarning("Error", "Please Enter Username!")#if username left blank
        
    elif (password.get() == ""):
        messagebox.showwarning("Error", "Please Enter Password!") #if password left blank
    
    elif (not records.find_one({'username':username.get()})):
        messagebox.showwarning("Error", "User not found") #if username not found in db
    
    elif (not records.find_one({'username':username.get(), 'password': password.get()})):
        messagebox.showwarning("Error", "Please ensure password is correct") #if password doesn't match in db
        
    else:
        mainMenu(loginGUI, False, username)#all details are correct and found, login successful
    
#first gui presented to the user when opening application
def mainScreen():
    loginGUI = Tk() #create gui
    loginGUI.geometry("428x720") #size of window
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
    loginButton = Button(loginGUI, text="Login", bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                         command=lambda: checkDetails(loginGUI, username, password)).pack()
    forgottenButton = Button(loginGUI, text="Forgotten?", bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                             command=lambda: forgottenPage(loginGUI, mainMenu)).pack()
    registerButton = Button(loginGUI, text='Register', bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                            command=lambda: registerPage(loginGUI, mainMenu)).pack()
    offlineButton = Button(loginGUI, text="Offline Mode", bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                           command=lambda: mainMenu(loginGUI, True, 'offline')).pack()
    loginGUI.mainloop()
mainScreen()
