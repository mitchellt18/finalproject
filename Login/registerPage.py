#import required modules
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os
from pymongo import MongoClient
import bcrypt
import re

#global variables required
global registerGUI
global username
global pass1
global pass2
global salary
global securityQuestion
global securityAnswer

#show password requirements
def passRequirements(screen):
    #gui settings
    passGUI = Toplevel(screen)
    passGUI.title("Password Requirements")
    passGUI.geometry('350x195')
    passGUI.configure(bg="#C0392B")

    #Title
    passTitle = Label(passGUI, text="Password Requirements", bg="#C0392B", wraplengt=400)
    passTitle.config(font=('Courier',25))
    passTitle.pack(side=TOP)

    Label(passGUI, text="Your Password MUST contain at least the following:", bg="#C0392B").pack()
    Label(passGUI, text="- 8 Characters", bg="#C0392B").pack()
    Label(passGUI, text="- 1 Uppercase", bg="#C0392B").pack()
    Label(passGUI, text="- 1 Lowercase", bg="#C0392B").pack()
    Label(passGUI, text="- 1 Number", bg="#C0392B").pack()
    Label(passGUI, text="- 1 Special Character", bg="#C0392B").pack()
    Label(passGUI, text="Special Characters are: !@#$%^&*()-+?_=,<>/", bg="#C0392B").pack()

#check inputted details    
def checkDetails(registerGUI, username, pass1, pass2, salary, securityQuestion, securityAnswer, secAns2, mainMenu):
    #checks if input is float
    def checkFloat(salary):
        try:
            float(salary)
            return True
        except ValueError:
            return False

    #var to store special characters for password
    special_characters = "!@#$%^&*()-+?_=,<>/"

    #establish connection with db
    global client
    global db
    global records
    client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('user_db')
    records = db.user_details
                 
    #if username blank - error
    if(username.get() == ""):
        messagebox.showwarning("Error", "Please Enter Username!")

    #if username exists - error
    elif (records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})):
        messagebox.showwarning("Error", "Username already exists")

    #if passwords do not match - error
    elif (pass1.get() != pass2.get()):
        messagebox.showwarning("Error", "Passwords Do Not Match!")

    #if passwords blank - error
    elif (pass1.get() == "" or pass2.get() == ""):
        messagebox.showwarning("Error", "Please Input Your Passwords!")

    #if password not strong (doesn't meet states requirements) - error
    elif ((not len(pass1.get()) >= 8) or (not any(p.isupper() for p in pass1.get())) or (not any(p.islower() for p in pass1.get())) or (not any(p.isdigit() for p in pass1.get())) or (not any(p in special_characters for p in pass1.get()))):
        messagebox.showwarning("Error", "Password Not Strong Enough!")

    #if salary blank - error
    elif (salary.get() == ""):
        messagebox.showwarning("Error", "Please Input Salary!")

    #if salary is not integer or float - error
    elif (checkFloat(salary.get()) == False):
        messagebox.showwarning("Error", "Ensure Salary ONLY Contains Integer or Float Values!")

    #if security details blank - error
    elif (securityQuestion.get() == "" or securityAnswer.get() == "" or secAns2.get() == ""):
        messagebox.showwarning("Error", "Please Ensure Security Details Are Filled!")

    #if secuerity answers do not match - error
    elif (securityAnswer.get() != secAns2.get()):
        messagebox.showwarning("Error", "Please Ensure Security Answers Match!")

    #else - register user
    else:

        #encrypt password
        encodedPassword = pass1.get().encode('utf-8')
        encPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt(10))

        #encrypt Security Answer
        encodedSecurityAnswer = securityAnswer.get().encode('utf-8')
        encSecurityAnswer = bcrypt.hashpw(encodedSecurityAnswer, bcrypt.gensalt(10))
        
        #create new user
        new_user = {
            'username' : username.get(),
            'password': encPassword,
            'salary': salary.get(),
            'securityQuestion': securityQuestion.get(),
            'securityAnswer': encSecurityAnswer,
            'lock': False,
            'objectIDMonthly': '',
            'objectIDDisposible': '',
            'objectIDReminders': ''
            }

        #insert new user into db
        records.insert_one(new_user)
        
        #success message and takes user to main menu
        messagebox.showinfo("Success", "Registered Successfully!")
        mainMenu(registerGUI, False, username)

#gui
def registerPage(screen, mainMenu):

    #remove previous window
    screen.withdraw()

    #gui settings
    registerGUI = Toplevel(screen)
    registerGUI.title("Register User")
    registerGUI.geometry("428x720")
    registerGUI.configure(bg="#C0392B")

    #register Title
    registerTitle = Label(registerGUI, text="Register User", bg="#C0392B", wraplengt=400)
    registerTitle.config(font=('Courier',25))
    registerTitle.pack(side=TOP)

    Label(registerGUI, text="Welcome!", bg="#C0392B").pack()
    Label(registerGUI, text="Please enter the following details below:", bg="#C0392B", wraplengt=400).pack()

    #username input
    username = StringVar()
    Label(registerGUI, text="Username", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = username, width = 30, bg='white', fg='black').pack()
    
    #password inputs
    pass1 = StringVar()
    Label(registerGUI, text="Password", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = pass1, width = 30, show="*", bg='white', fg='black').pack()
    pass2 = StringVar()
    Label(registerGUI, text="Please Repeat Password", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = pass2, width = 30, show="*", bg='white', fg='black').pack()

    #password requirement button
    reqImg = Image.open("./Buttons/Register/button_password-requirements.png")
    outputReq = ImageTk.PhotoImage(reqImg)
    
    reqButton = Button(registerGUI, image = outputReq, 
                        command=lambda: passRequirements(registerGUI))

    reqButton.image = outputReq
    reqButton.pack()


    #salary input
    salary = StringVar() 
    Label(registerGUI, text="Please enter your salary in GBP (£)", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = salary, width = 30, bg='white', fg='black').pack()

    #security question input
    securityQuestion = StringVar()
    Label(registerGUI, text="For security reasons, please input security details.", bg="#C0392B", wraplengt=400).pack()
    Label(registerGUI, text="Please input security question:", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = securityQuestion, width = 30, bg='white', fg='black').pack()

    #security answer inputs
    securityAnswer = StringVar()
    Label(registerGUI, text="Please input a security answer:", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = securityAnswer, width = 30, show='*', bg='white', fg='black').pack()
    securityAnswer2 = StringVar()
    Label(registerGUI, text="Please re-input security question:", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = securityAnswer2, width = 30, show='*', bg='white', fg='black').pack()

    #register button
    registerImg = Image.open("./Buttons/Register/button_register.png")
    outputRegister = ImageTk.PhotoImage(registerImg)
    
    registerButton = Button(registerGUI, image = outputRegister, 
                    command=lambda: checkDetails(registerGUI, username, pass1, pass2, salary, securityQuestion, securityAnswer, securityAnswer2, mainMenu))

    registerButton.image = outputRegister
    registerButton.pack()
