#import required modules
from tkinter import *
from tkinter import messagebox
import bcrypt
import re

#import py files
from settings import *
from monthlyBills import *
from disposibleIncome import *

from paymentReminders import *

#Verify Password Function
def verify(screen, offlineMode, username):
    if (offlineMode):
        settings(screen, offlineMode, username)
    else:
        def checkDetails(screen, username, password, offlineMode):
            #establish connection with the database
            client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = client.get_database('user_db')
            records = db.user_details

            checkPassword = password.get().encode('utf-8') #encode inputted password as utf-8
            userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})

            if(password.get() == ""):
                messagebox.showwarning("Error", "Please Enter Password!")#if password left blank

            #check inputted password is correct
            elif (not bcrypt.checkpw(checkPassword, userObject['password'])):
                messagebox.showwarning("Error", "Please ensure password is correct") #if password doesn't match in db

            else:
                screen.withdraw()
                settings(screen, offlineMode, username)
                
        
        #ask for password re-entry
        global verifyPass
        verifyPass = Toplevel(screen)
        verifyPass.title("Verify Password")
        verifyPass.geometry("428x100")
        verifyPass.configure(bg="#C0392B")

        #verify title
        verifyTitle = Label(verifyPass, text="Please Re-enter Password", bg="#C0392B", wraplengt=400)
        verifyTitle.config(font=('Courier',25))
        verifyTitle.pack(side=TOP, anchor=NW)

        #password
        password = StringVar()
        Entry(verifyPass, textvariable = password, width = 30, show="*", bg='white', fg='black').pack()

        verifyButton = Button(verifyPass, text='Verify', bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                            command=lambda: checkDetails(verifyPass, username, password, offlineMode)).pack()
        

#Main Menu
def mainMenu(screen, offlineMode, username):
    global mainMenuGUI

    screen.withdraw() #close previous window no longer required

    mainMenuGUI = Toplevel(screen)
    mainMenuGUI.title("Main Menu")
    mainMenuGUI.geometry("428x526")
    mainMenuGUI.configure(bg="#C0392B")

    #Main Menu Title
    mainmenuTitle = Label(mainMenuGUI, text="Main Menu", bg="#C0392B", wraplengt=400)
    mainmenuTitle.config(font=('Courier',25))
    mainmenuTitle.pack(side=TOP, anchor=NW)

    #settings button
    settingsButton = Button(mainMenuGUI, text="Settings", bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                            command=lambda: verify(mainMenuGUI, offlineMode, username))
    settingsButton.pack(side=TOP, anchor=NE)

    #Option Label
    mainmenuLabel = Label(mainMenuGUI, text="Please choose an option below", bg="#C0392B")
    mainmenuLabel.pack()

    #option1 button
    option1Button = Button(mainMenuGUI, text="Monthly Bills Tracker", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                            command=lambda: monthlyBills(mainMenuGUI, offlineMode, username))
    option1Button.pack()

    #option2 button
    option2Button = Button(mainMenuGUI, text="Disposible Income Tracker", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                           command = lambda: disposibleIncome(mainMenuGUI, offlineMode, username))
    option2Button.pack()

    #option3 button
    option3Button = Button(mainMenuGUI, text="Financial Recommendations", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white")
    option3Button.pack()

    #option4 button
    option4Button = Button(mainMenuGUI, text="Payment Reminders", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                           command = lambda: paymentReminders(mainMenuGUI, offlineMode, username))
    option4Button.pack()

    if (offlineMode):        
        userLabel = Label(mainMenuGUI, text="Offline Mode. Using Local Database.", bg="#C0392B").pack()
    else:
        userLabel = Label(mainMenuGUI, text="Currently Logged In: " + username.get(), bg="#C0392B").pack()
