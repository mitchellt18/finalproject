#import required modules
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import re
import bcrypt

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
        verifyPass.geometry("428x110")
        verifyPass.configure(bg="#C0392B")

        #verify title
        verifyTitle = Label(verifyPass, text="Please Re-enter Password", bg="#C0392B", wraplengt=400)
        verifyTitle.config(font=('Courier',25))
        verifyTitle.pack(side=TOP, anchor=NW)

        #password
        password = StringVar()
        Entry(verifyPass, textvariable = password, width = 30, show="*", bg='white', fg='black').pack()

        #verify button
        verifyImg = Image.open("./Buttons/Settings/button_verify.png")
        outputVerify = ImageTk.PhotoImage(verifyImg)
        
        verifyButton = Button(verifyPass, image = outputVerify,
                                command=lambda: checkDetails(verifyPass, username, password, offlineMode))

        verifyButton.image = outputVerify
        verifyButton.pack()
        

#Main Menu
def mainMenu(screen, offlineMode, username):
    from PIL import ImageTk, Image #import is here as is required when running function
    global mainMenuGUI

    screen.withdraw() #close previous window no longer required

    mainMenuGUI = Toplevel(screen)
    mainMenuGUI.title("Main Menu")
    mainMenuGUI.geometry("428x550")
    mainMenuGUI.configure(bg="#C0392B")

    #Main Menu Title
    mainmenuTitle = Label(mainMenuGUI, text="Main Menu", bg="#C0392B", wraplengt=400)
    mainmenuTitle.config(font=('Courier',25))
    mainmenuTitle.pack(side=TOP, anchor=NW)

    #settings button
    settingsImg = Image.open("./Buttons/mainMenu/button_settings.png").resize((90,22))
    outputSettings = ImageTk.PhotoImage(settingsImg)
    
    settingsButton = Button(mainMenuGUI, image = outputSettings, 
                    command=lambda: verify(mainMenuGUI, offlineMode, username))

    settingsButton.image = outputSettings
    settingsButton.pack(side=TOP, anchor=NE)

    #Option Label
    mainmenuLabel = Label(mainMenuGUI, text="Please choose an option below", bg="#C0392B")
    mainmenuLabel.pack()

    #monthly bill tracker button
    opt1Img = Image.open("./Buttons/mainMenu/button_monthly-bills-tracker.png")
    outputOpt1 = ImageTk.PhotoImage(opt1Img)
    
    opt1Button = Button(mainMenuGUI, image = outputOpt1, 
                    command=lambda: monthlyBills(mainMenuGUI, offlineMode, username))

    opt1Button.image = outputOpt1
    opt1Button.pack()

    #disposable tracker button
    opt2Img = Image.open("./Buttons/mainMenu/button_disposable-income-tracker.png")
    outputOpt2 = ImageTk.PhotoImage(opt2Img)
    
    opt2Button = Button(mainMenuGUI, image = outputOpt2, 
                    command = lambda: disposibleIncome(mainMenuGUI, offlineMode, username))

    opt2Button.image = outputOpt2
    opt2Button.pack()

    #financial recommendations button
    opt3Img = Image.open("./Buttons/mainMenu/button_financial-recommendations.png")
    outputOpt3 = ImageTk.PhotoImage(opt3Img)
    
    opt3Button = Button(mainMenuGUI, image = outputOpt3) 
                    #command=lambda: monthlyBills(mainMenuGUI, offlineMode, username))

    opt3Button.image = outputOpt3
    opt3Button.pack()

    #payment reminder button
    opt4Img = Image.open("./Buttons/mainMenu/button_payment-reminders.png")
    outputOpt4 = ImageTk.PhotoImage(opt4Img)
    
    opt4Button = Button(mainMenuGUI, image = outputOpt4, 
                    command = lambda: paymentReminders(mainMenuGUI, offlineMode, username))

    opt4Button.image = outputOpt4
    opt4Button.pack()

    if (offlineMode):        
        userLabel = Label(mainMenuGUI, text="Offline Mode. Using Local Database.", bg="#C0392B").pack()
    else:
        userLabel = Label(mainMenuGUI, text="Currently Logged In: " + username.get(), bg="#C0392B").pack()
