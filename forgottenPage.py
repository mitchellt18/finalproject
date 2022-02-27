from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
import bcrypt

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


def checkPass(resetPassGUI, pass1, pass2, userObject, username, mainMenu):
    #var to store special characters for password
    special_characters = "!@#$%^&*()-+?_=,<>/"
    
    #check password
    if (pass1.get() != pass2.get()):
        messagebox.showwarning("Error", "Passwords Do Not Match!") #check if passwords do not match
    elif (pass1.get() == "" or pass2.get() == ""):
        messagebox.showwarning("Error", "Please Input Your Passwords!") #check if passwords is blank
    elif ((not len(pass1.get()) >= 8) or (not any(p.isupper() for p in pass1.get())) or (not any(p.islower() for p in pass1.get())) or (not any(p.isdigit() for p in pass1.get())) or (not any(p in special_characters for p in pass1.get()))):
        messagebox.showwarning("Error", "Password Not Strong Enough!") #check if passwords is strong enough
    else:

        #encrypt password
        encodedPassword = pass1.get().encode('utf-8')
        encPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt(10))
        
        records.find_one_and_update({'username': userObject['username']},
                                    {'$set':{'password': encPassword} },
                                    return_document = ReturnDocument.AFTER)
        messagebox.showinfo("Success", "Password Reset Successfully! Now Logging In...") #tells user successfully registered
        mainMenu(resetPassGUI, False, username) #takes user to main menu logged in
        


def resetPass(securityQuestionGUI, userObject, username, mainMenu):
    securityQuestionGUI.withdraw()
    resetPassGUI = Toplevel(securityQuestionGUI)
    resetPassGUI.title("Reset Password")
    resetPassGUI.geometry("428x720")
    resetPassGUI.configure(bg="#C0392B")

    #Title
    resetTitle = Label(resetPassGUI, text="Forgotten User", bg="#C0392B", wraplengt=400)
    resetTitle.config(font=('Courier',25))
    resetTitle.pack(side=TOP)

    Label(securityQuestionGUI, text="Please Enter your New Password", bg="#C0392B", wraplengt=400).pack()
    
    #reset password
    pass1 = StringVar()
    Label(resetPassGUI, text="Password", bg="#C0392B", wraplengt=400).pack()
    Entry(resetPassGUI, textvariable = pass1, width = 30, show="*", bg='white', fg='black').pack()
    
    pass2 = StringVar()
    Label(resetPassGUI, text="Please Repeat Password:", bg="#C0392B", wraplengt=400).pack()
    Entry(resetPassGUI, textvariable = pass2, width = 30, show="*", bg='white', fg='black').pack()

    Button(resetPassGUI, text='Password Requirements', bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                            command=lambda: passRequirements(resetPassGUI)).pack()

    Button(resetPassGUI, text='Reset Password', bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                            command=lambda: checkPass(resetPassGUI, pass1, pass2, userObject, username, mainMenu)).pack()


def checkAns(securityQuestionGUI, ans, userObject, username, mainMenu):
    checkSecurityAnswer = ans.get().encode('utf-8')
    
    #check input is blank
    if(ans.get() == ""):
        messagebox.showwarning("Error", "Please Enter Security Answer!")
        
    #check if inputted answer matches
    elif (not bcrypt.checkpw(checkSecurityAnswer, userObject['securityAnswer'])):
        messagebox.showwarning("Error", "Security Answer Not Correct, Try Again") #if answer doesn't match
        
    else:
        resetPass(securityQuestionGUI, userObject, username, mainMenu) #proceed to reset pass

#outputs security question with input for security answer
def checkSecurityQuestion(forgottenGUI, userObject, username, mainMenu):
    forgottenGUI.withdraw()
    securityQuestionGUI = Toplevel(forgottenGUI)
    securityQuestionGUI.title("Security Question")
    securityQuestionGUI.geometry("428x720")
    securityQuestionGUI.configure(bg="#C0392B")
    
    #Title
    secTitle = Label(securityQuestionGUI, text="Forgotten User", bg="#C0392B", wraplengt=400)
    secTitle.config(font=('Courier',25))
    secTitle.pack(side=TOP)
    
    #username
    secAnswer = StringVar()
    Label(securityQuestionGUI, text="Please Answer the Following Security Question:", bg="#C0392B", wraplengt=400).pack()
    #outputs security question
    Label(securityQuestionGUI, text=userObject['securityQuestion'] + "?", bg="#C0392B", wraplengt=400).pack()
    Label(securityQuestionGUI, text="Please Input the Answer Here:", bg="#C0392B", wraplengt=400).pack()

    #security question answer input
    ans = StringVar()
    Entry(securityQuestionGUI, textvariable = ans, width = 30, bg='white', fg='black').pack()
    Label(securityQuestionGUI, text="Please Note: Security Answers ARE Case Sensitive!", bg="#C0392B", wraplengt=400).pack()

    #proceed button
    forgottenButton = Button(securityQuestionGUI, text='Continue', bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                            command=lambda: checkAns(securityQuestionGUI, ans, userObject, username, mainMenu)).pack()
    
    
#checks if user exists
def checkDetails(forgottenGUI, username, mainMenu):
    #check username actually exists in db
    if(username.get() == ""):
        messagebox.showwarning("Error", "Please Enter Username!")
    elif (not records.find_one({'username':username.get()})):
        messagebox.showwarning("Error", "User not found") #if username not found in db
    else:
        #retrieve user from db as an object
        userObject = records.find_one({'username': username.get()})
        checkSecurityQuestion(forgottenGUI, userObject, username, mainMenu)

#window where user enters username
def forgottenPage(screen, mainMenu):
    global forgottenGUI

    screen.withdraw() #close previous window no longer required

    forgottenGUI = Toplevel(screen)
    forgottenGUI.title("Forgotten User")
    forgottenGUI.geometry("428x720")
    forgottenGUI.configure(bg="#C0392B")

    #forgotten Title
    forgottenTitle = Label(forgottenGUI, text="Forgotten User", bg="#C0392B", wraplengt=400)
    forgottenTitle.config(font=('Courier',25))
    forgottenTitle.pack(side=TOP)

    #username
    username = StringVar()
    Label(forgottenGUI, text="Username", bg="#C0392B", wraplengt=400).pack()
    Entry(forgottenGUI, textvariable = username, width = 30, bg='white', fg='black').pack()

    forgottenButton = Button(forgottenGUI, text='Get Security Question', bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                            command=lambda: checkDetails(forgottenGUI, username, mainMenu)).pack()
    
