#import required modules
from tkinter import *
from tkinter import messagebox
import re
import os
from PIL import ImageTk, Image #required for images

#import py files
from changeSalary import *
from changePassword import *
from changeQuestion import *
from changeAnswer import *

#Delete User Function
def delUser(settingsGUI, username):
    MessageBox = messagebox.askquestion ('Delete User','Are you sure you want to delete your user account? All Data Will Be Deleted!!',icon = 'warning')
    if MessageBox == 'yes':
        MessageBox2 = messagebox.askquestion ('Delete User','Are you ABSOLUTELY sure? This action is irreversable!!!',icon = 'warning')
        if MessageBox2 == 'yes':
            
            #establish connection with the database
            client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = client.get_database('user_db')
            records = db.user_details

            #delete user from db
            records.delete_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})
            
            messagebox.showinfo('Deleted User','Your Account Details Have Now Been Deleted :( Feel free to sign back up later on!')
            quit()
        else:
            messagebox.showinfo('Not Deleted User','Your Account Details Have NOT Been Deleted. Proceeding back to Settings Menu')
    else:
        messagebox.showinfo('Not Deleted User','Your Account Details Have NOT Been Deleted. Proceeding back to Settings Menu')

#Settings
def settings(screen, offlineMode, username):
    from PIL import ImageTk, Image #required for images
    global settingsGUI
    settingsGUI = Toplevel(screen)
    settingsGUI.title("Settings")
    settingsGUI.geometry("428x526")
    settingsGUI.configure(bg="#C0392B")

    #Settings Title
    settingsTitle = Label(settingsGUI, text="Settings", bg="#C0392B", wraplengt=400)
    settingsTitle.config(font=('Courier',25))
    settingsTitle.pack(side=TOP, anchor=NW)

    if (offlineMode):
        Label(settingsGUI, text="You are in Offline Mode", bg="#C0392B").pack()
        Label(settingsGUI, text="Settings is only available to Registered Users", bg="#C0392B").pack()

    else:
    
        #Option Label
        mainmenuLabel = Label(settingsGUI, text="Please choose an option below", bg="#C0392B")
        mainmenuLabel.pack()

        #Option 1 Button
        option1Img = Image.open("./Buttons/Settings/button_change-salary.png")
        outputOption1 = ImageTk.PhotoImage(option1Img)
        
        option1Button = Button(settingsGUI, image = outputOption1,
                               command=lambda: changeSalary(settingsGUI, username))

        option1Button.image = outputOption1
        option1Button.pack()

        #Option 2 Button
        option2Img = Image.open("./Buttons/Settings/button_change-password.png")
        outputOption2 = ImageTk.PhotoImage(option2Img)
        
        option2Button = Button(settingsGUI, image = outputOption2,
                               command=lambda: changePassword(settingsGUI, username))

        option2Button.image = outputOption2
        option2Button.pack()

        #Option 3 Button
        option3Img = Image.open("./Buttons/Settings/button_security-question.png")
        outputOption3 = ImageTk.PhotoImage(option3Img)
        
        option3Button = Button(settingsGUI, image = outputOption3,
                               command=lambda: changeQuestion(settingsGUI, username))

        option3Button.image = outputOption3
        option3Button.pack()

        #Option 4 Button
        option4Img = Image.open("./Buttons/Settings/button_security-answer.png")
        outputOption4 = ImageTk.PhotoImage(option4Img)
        
        option4Button = Button(settingsGUI, image = outputOption4,
                               command=lambda: changeAnswer(settingsGUI, username))

        option4Button.image = outputOption4
        option4Button.pack()
        
        #Option 5 Button
        option5Img = Image.open("./Buttons/Settings/button_delete-user.png")
        outputOption5 = ImageTk.PhotoImage(option5Img)
        
        option5Button = Button(settingsGUI, image = outputOption5,
                               command=lambda: delUser(settingsGUI, username))

        option5Button.image = outputOption5
        option5Button.pack()
