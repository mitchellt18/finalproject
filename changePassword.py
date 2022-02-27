from tkinter import *
from pymongo import MongoClient
from tkinter import messagebox
from pymongo.collection import ReturnDocument
import bcrypt
import re

#establish connection with db
global client
global db
global records
client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('user_db')
records = db.user_details

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
    
    #check password
    if (password.get() != p2.get()):
        messagebox.showwarning("Error", "Passwords Do Not Match!") #check if passwords do not match
    elif (password.get() == "" or p2.get() == ""):
        messagebox.showwarning("Error", "Please Input Your Passwords!") #check if passwords is blank
    elif ((not len(password.get()) >= 8) or (not any(p.isupper() for p in password.get())) or (not any(p.islower() for p in password.get())) or (not any(p.isdigit() for p in password.get())) or (not any(p in special_characters for p in password.get()))):
        messagebox.showwarning("Error", "Password Not Strong Enough!") #check if passwords is strong enough
    else:

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

def changePassword(screen, username):
    global passwordGUI
    passwordGUI = Toplevel(screen)
    passwordGUI.title("Change Password - Settings")
    passwordGUI.geometry("428x200")
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

    Button(passwordGUI, text='Password Requirements', bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                        command=lambda: passRequirements(passwordGUI)).pack()

    #button
    proceed = Button(passwordGUI, text="Proceed", bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                         command=lambda: checkPassword(passwordGUI, username, pass1, pass2)).pack()
