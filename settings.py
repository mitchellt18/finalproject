#import required modules
from tkinter import *
from tkinter import messagebox
import re

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

        #option1 button
        option1Button = Button(settingsGUI, text="Change Salary", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                               command=lambda: changeSalary(settingsGUI, username))
        option1Button.pack()

        #option2 button
        option2Button = Button(settingsGUI, text="Change Password", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                               command=lambda: changePassword(settingsGUI, username))
        option2Button.pack()

        #option3 button
        option3Button = Button(settingsGUI, text="Change Security Question", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                               command=lambda: changeQuestion(settingsGUI, username))
        option3Button.pack()

        #option4 button
        option4Button = Button(settingsGUI, text="Change Security Answer", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                               command=lambda: changeAnswer(settingsGUI, username))
        option4Button.pack()

        #option5 button
        option5Button = Button(settingsGUI, text="Delete User", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                               command=lambda: delUser(settingsGUI, username))
        option5Button.pack()
