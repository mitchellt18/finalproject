#import required modules
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
import bcrypt
import re

global registerGUI
global username
global pass1
global pass2
global salary
global securityQuestion
global securityAnswer

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
    

def registerToDB():
    print("Register to DB Here")

def checkDetails(registerGUI, username, pass1, pass2, salary, securityQuestion, securityAnswer, secAns2, mainMenu):
    #continue checking by ensuring username doesn't exist (connection to db) and passwords are strong
    def checkFloat(salary):
        try:
            float(salary)
            return True
        except ValueError:
            return False

    #var to store special characters for password
    special_characters = "!@#$%^&*()-+?_=,<>/"
                 
    #check username
    if(username.get() == ""):
        messagebox.showwarning("Error", "Please Enter Username!") #check if username is blank

    elif (records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})):
        messagebox.showwarning("Error", "Username already exists") #if username exists in db

    #check password
    elif (pass1.get() != pass2.get()):
        messagebox.showwarning("Error", "Passwords Do Not Match!") #check if passwords do not match
    elif (pass1.get() == "" or pass2.get() == ""):
        messagebox.showwarning("Error", "Please Input Your Passwords!") #check if passwords is blank
    elif ((not len(pass1.get()) >= 8) or (not any(p.isupper() for p in pass1.get())) or (not any(p.islower() for p in pass1.get())) or (not any(p.isdigit() for p in pass1.get())) or (not any(p in special_characters for p in pass1.get()))):
        messagebox.showwarning("Error", "Password Not Strong Enough!") #check if passwords is strong enough

    #check salary
    elif (salary.get() == ""):
        messagebox.showwarning("Error", "Please Input Salary!") #check if salary is blank
    elif (checkFloat(salary.get()) == False):
        messagebox.showwarning("Error", "Ensure Salary ONLY Contains Integer or Float Values!") #check if salary is not float

    #check security questions
    elif (securityQuestion.get() == "" or securityAnswer.get() == "" or secAns2.get() == ""):
        messagebox.showwarning("Error", "Please Ensure Security Details Are Filled!") #check if security details is not filled
    elif (securityAnswer.get() != secAns2.get()):
        messagebox.showwarning("Error", "Please Ensure Security Answers Match!") #check if security details is not filled

    #Once all checked, input into database
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
            'lock': False
            }
        records.insert_one(new_user) #inputs new user into db
        messagebox.showinfo("Success", "Registered Successfully!") #tells user successfully registered
        mainMenu(registerGUI, False, username) #takes user to main menu logged in
        
def registerPage(screen, mainMenu):
    screen.withdraw() #close previous window no longer required

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

    #username
    username = StringVar()
    Label(registerGUI, text="Username", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = username, width = 30, bg='white', fg='black').pack()
    
    #password
    pass1 = StringVar()
    Label(registerGUI, text="Password", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = pass1, width = 30, show="*", bg='white', fg='black').pack()
    pass2 = StringVar()
    Label(registerGUI, text="Please Repeat Password", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = pass2, width = 30, show="*", bg='white', fg='black').pack()

    Button(registerGUI, text='Password Requirements', bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                            command=lambda: passRequirements(registerGUI)).pack()

    #salary
    salary = StringVar() 
    Label(registerGUI, text="Please enter your salary in GBP (£)", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = salary, width = 30, bg='white', fg='black').pack()

    #security questions
    securityQuestion = StringVar()
    Label(registerGUI, text="For security reasons, please input security details.", bg="#C0392B", wraplengt=400).pack()
    Label(registerGUI, text="Please input security question:", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = securityQuestion, width = 30, bg='white', fg='black').pack()

    #security answer
    securityAnswer = StringVar()
    Label(registerGUI, text="Please input a security answer:", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = securityAnswer, width = 30, show='*', bg='white', fg='black').pack()
    securityAnswer2 = StringVar()
    Label(registerGUI, text="Please re-input security question:", bg="#C0392B", wraplengt=400).pack()
    Entry(registerGUI, textvariable = securityAnswer2, width = 30, show='*', bg='white', fg='black').pack()

    registerButton = Button(registerGUI, text='Register', bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                            command=lambda: checkDetails(registerGUI, username, pass1, pass2, salary, securityQuestion, securityAnswer, securityAnswer2, mainMenu)).pack()

    #backButton = Button(registerGUI, text='Back to Login', bg="#C0392B", highlightbackground="#C0392B", fg = "white",
    #                        command=mainScreen()).pack()
