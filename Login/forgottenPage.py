#import required modules
from tkinter import *
from PIL import ImageTk, Image
import os
import re
from tkinter import messagebox
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
import bcrypt

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

    #Labels with details
    Label(passGUI, text="Your Password MUST contain at least the following:", bg="#C0392B").pack()
    Label(passGUI, text="- 8 Characters", bg="#C0392B").pack()
    Label(passGUI, text="- 1 Uppercase", bg="#C0392B").pack()
    Label(passGUI, text="- 1 Lowercase", bg="#C0392B").pack()
    Label(passGUI, text="- 1 Number", bg="#C0392B").pack()
    Label(passGUI, text="- 1 Special Character", bg="#C0392B").pack()
    Label(passGUI, text="Special Characters are: !@#$%^&*()-+?_=,<>/", bg="#C0392B").pack()


#check password
def checkPass(resetPassGUI, pass1, pass2, userObject, username, mainMenu):
    #var to store special characters for password
    special_characters = "!@#$%^&*()-+?_=,<>/"

    #db code
    client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('user_db')
    records = db.user_details
    
    #check password
    
    #if passwords do not match - error
    if (pass1.get() != pass2.get()):
        messagebox.showwarning("Error", "Passwords Do Not Match!")
        
    #if passwords blank - error
    elif (pass1.get() == "" or pass2.get() == ""):
        messagebox.showwarning("Error", "Please Input Your Passwords!")

    #if password not strong (doesn't meet stated requirements) - error
    elif ((not len(pass1.get()) >= 8) or (not any(p.isupper() for p in pass1.get())) or (not any(p.islower() for p in pass1.get())) or (not any(p.isdigit() for p in pass1.get())) or (not any(p in special_characters for p in pass1.get()))):
        messagebox.showwarning("Error", "Password Not Strong Enough!")

    #password strong enough - continue
    else:
        #encrypt password
        encodedPassword = pass1.get().encode('utf-8')
        encPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt(10))

        #update password in db
        records.find_one_and_update({'username': userObject['username']},
                                    {'$set':{
                                        'password': encPassword,
                                        'lock': False
                                        }
                                     },
                                    return_document = ReturnDocument.AFTER)
        #success message and takes user to main menu
        messagebox.showinfo("Success", "Password Reset Successfully! Now Logging In...")
        mainMenu(resetPassGUI, False, username)
        

#gui to reset password
def resetPass(securityQuestionGUI, userObject, username, mainMenu):

    #remove old window
    securityQuestionGUI.withdraw()

    #gui settings
    resetPassGUI = Toplevel(securityQuestionGUI)
    resetPassGUI.title("Reset Password")
    resetPassGUI.geometry("428x220")
    resetPassGUI.configure(bg="#C0392B")

    #Title
    resetTitle = Label(resetPassGUI, text="Forgotten User", bg="#C0392B", wraplengt=400)
    resetTitle.config(font=('Courier',25))
    resetTitle.pack(side=TOP)

    Label(securityQuestionGUI, text="Please Enter your New Password", bg="#C0392B", wraplengt=400).pack()
    
    #password input 1
    pass1 = StringVar()
    Label(resetPassGUI, text="Password", bg="#C0392B", wraplengt=400).pack()
    Entry(resetPassGUI, textvariable = pass1, width = 30, show="*", bg='white', fg='black').pack()

    #password input 2
    pass2 = StringVar()
    Label(resetPassGUI, text="Please Repeat Password:", bg="#C0392B", wraplengt=400).pack()
    Entry(resetPassGUI, textvariable = pass2, width = 30, show="*", bg='white', fg='black').pack()

    #password requirement button
    reqImg = Image.open("./Buttons/forgottenPassword/button_password-requirements.png")
    outputReq = ImageTk.PhotoImage(reqImg)
    
    reqButton = Button(resetPassGUI, image = outputReq, 
                        command=lambda: passRequirements(resetPassGUI))

    reqButton.image = outputReq
    reqButton.pack()

    #password reset button
    resetImg = Image.open("./Buttons/forgottenPassword/button_reset-password.png")
    outputReset = ImageTk.PhotoImage(resetImg)
    
    resetButton = Button(resetPassGUI, image = outputReset, 
                        command=lambda: checkPass(resetPassGUI, pass1, pass2, userObject, username, mainMenu))

    resetButton.image = outputReset
    resetButton.pack()

#checks security answer
def checkAns(securityQuestionGUI, ans, userObject, username, mainMenu):
    checkSecurityAnswer = ans.get().encode('utf-8')

    #establish connection with db
    client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('user_db')
    records = db.user_details
    
    #if input blank - error
    if(ans.get() == ""):
        messagebox.showwarning("Error", "Please Enter Security Answer!")
        
    #if inputted answer do not match - error
    elif (not bcrypt.checkpw(checkSecurityAnswer, userObject['securityAnswer'])):
        messagebox.showwarning("Error", "Security Answer Not Correct, Try Again")

    #proceed to reset password  
    else:
        resetPass(securityQuestionGUI, userObject, username, mainMenu)

#outputs security question with input for security answer
def checkSecurityQuestion(forgottenGUI, userObject, username, mainMenu):

    #remove previous window
    forgottenGUI.withdraw()

    #gui settings
    securityQuestionGUI = Toplevel(forgottenGUI)
    securityQuestionGUI.title("Security Question")
    securityQuestionGUI.geometry("428x200")
    securityQuestionGUI.configure(bg="#C0392B")

    #establish connection with db
    client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('user_db')
    records = db.user_details
    
    #Title
    secTitle = Label(securityQuestionGUI, text="Forgotten User", bg="#C0392B", wraplengt=400)
    secTitle.config(font=('Courier',25))
    secTitle.pack(side=TOP)
    
    Label(securityQuestionGUI, text="Please Answer the Following Security Question:", bg="#C0392B", wraplengt=400).pack()

    #outputs security question
    Label(securityQuestionGUI, text=userObject['securityQuestion'] + "?", bg="#C0392B", wraplengt=400).pack()
    Label(securityQuestionGUI, text="Please Input the Answer Here:", bg="#C0392B", wraplengt=400).pack()

    #security answer input
    ans = StringVar()
    Entry(securityQuestionGUI, textvariable = ans, width = 30, show = '*', bg='white', fg='black').pack()
    
    Label(securityQuestionGUI, text="Please Note: Security Answers ARE Case Sensitive!", bg="#C0392B", wraplengt=400).pack()

    #proceed button
    forgottenImg = Image.open("./Buttons/forgottenPassword/button_continue.png")
    outputForgotten = ImageTk.PhotoImage(forgottenImg)
    
    forgottenButton = Button(securityQuestionGUI, image = outputForgotten, 
                        command=lambda: checkAns(securityQuestionGUI, ans, userObject, username, mainMenu))

    forgottenButton.image = outputForgotten
    forgottenButton.pack()
    
    
#checks if user exists
def checkDetails(forgottenGUI, username, mainMenu):
    
    #establish connection with db
    client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('user_db')
    records = db.user_details

    #if username left blank - error
    if(username.get() == ""):
        messagebox.showwarning("Error", "Please Enter Username!")

    #if username doesn't exist - error
    elif (not records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})):
        messagebox.showwarning("Error", "User not found") #if username not found in db

    #else retrieve user from db and proceed
    else:
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})
        checkSecurityQuestion(forgottenGUI, userObject, username, mainMenu)

#user enters username
def forgottenPage(screen, mainMenu):

    #remove previous window
    screen.withdraw()

    #gui settings
    global forgottenGUI
    forgottenGUI = Toplevel(screen)
    forgottenGUI.title("Forgotten User")
    forgottenGUI.geometry("428x150")
    forgottenGUI.configure(bg="#C0392B")

    #forgotten Title
    forgottenTitle = Label(forgottenGUI, text="Forgotten User", bg="#C0392B", wraplengt=400)
    forgottenTitle.config(font=('Courier',25))
    forgottenTitle.pack(side=TOP)

    #username input
    username = StringVar()
    Label(forgottenGUI, text="Username", bg="#C0392B", wraplengt=400).pack()
    Entry(forgottenGUI, textvariable = username, width = 30, bg='white', fg='black').pack()

    #proceed button
    forgottenImg = Image.open("./Buttons/forgottenPassword/button_get-security-question.png")
    outputForgotten = ImageTk.PhotoImage(forgottenImg)
    
    forgottenButton = Button(forgottenGUI, image = outputForgotten, 
                        command=lambda: checkDetails(forgottenGUI, username, mainMenu))

    forgottenButton.image = outputForgotten
    forgottenButton.pack()
    
