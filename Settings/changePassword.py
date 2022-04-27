from tkinter import *
from pymongo import MongoClient
from tkinter import messagebox
from pymongo.collection import ReturnDocument
import bcrypt
import re
import os
from PIL import ImageTk, Image #required for images

#password requirements screen
def passRequirements(screen):
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

#change password functions
def checkPassword(passwordGUI, username, password, p2):
    
    #var to store special characters for password
    special_characters = "!@#$%^&*()-+?_=,<>/"
    
    #if passwords do not match - error
    if (password.get() != p2.get()):
        messagebox.showwarning("Error", "Passwords Do Not Match!")

    #if passwords blank - error
    elif (password.get() == "" or p2.get() == ""):
        messagebox.showwarning("Error", "Please Input Your Passwords!")

    #if passwords not strong enough - error
    elif ((not len(password.get()) >= 8) or (not any(p.isupper() for p in password.get())) or (not any(p.islower() for p in password.get())) or (not any(p.isdigit() for p in password.get())) or (not any(p in special_characters for p in password.get()))):
        messagebox.showwarning("Error", "Password Not Strong Enough!")

    #else - change password in db
    else:
        #db code
        global client
        global db
        global records
        client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database('user_db')
        records = db.user_details

        #encrypt password
        encodedPassword = password.get().encode('utf-8')
        encPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt(10))
        
        #change password
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})
        records.find_one_and_update({'username': userObject['username']},
                                    {'$set':{'password': encPassword} },
                                    return_document = ReturnDocument.AFTER)
        
        messagebox.showinfo("Success", "Password Updated Successfully! ") #tells user password updated
        passwordGUI.withdraw()

#change password gui
def changePassword(screen, username):
    from PIL import ImageTk, Image #required for images

    #gui settings
    global passwordGUI
    passwordGUI = Toplevel(screen)
    passwordGUI.title("Change Password - Settings")
    passwordGUI.geometry("428x230")
    passwordGUI.configure(bg="#C0392B")

    #Change Password Title
    passTitle = Label(passwordGUI, text="Change Password", bg="#C0392B", wraplengt=400)
    passTitle.config(font=('Courier',25))
    passTitle.pack(side=TOP, anchor=NW)

    #input
    pass1 = StringVar()
    Label(passwordGUI, text="Please enter your new password: ", bg="#C0392B", wraplengt=400).pack()
    Entry(passwordGUI, textvariable=pass1, width = 30, show='*', bg='white', fg='black').pack()

    #inpu2
    pass2 = StringVar()
    Label(passwordGUI, text="Please enter your new password again: ", bg="#C0392B", wraplengt=400).pack()
    Entry(passwordGUI, textvariable=pass2, width = 30, show='*', bg='white', fg='black').pack()

    #password requirements button
    reqImg = Image.open("./Buttons/Register/button_password-requirements.png")
    outputReq = ImageTk.PhotoImage(reqImg)
    
    reqButton = Button(passwordGUI, image = outputReq,
                           command=lambda: passRequirements(passwordGUI))

    reqButton.image = outputReq
    reqButton.pack()

    #proceed button
    proceedImg = Image.open("./Buttons/Settings/button_proceed.png").resize((100, 30))
    outputProceed = ImageTk.PhotoImage(proceedImg)
    
    proceedButton = Button(passwordGUI, image = outputProceed,
                           command=lambda: checkPassword(passwordGUI, username, pass1, pass2))

    proceedButton.image = outputProceed
    proceedButton.pack()
