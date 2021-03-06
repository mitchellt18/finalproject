from tkinter import *
from pymongo import MongoClient
from tkinter import messagebox
from pymongo.collection import ReturnDocument
import bcrypt
import re
import os
from PIL import ImageTk, Image #required for images

#change password functions
def checkAnswer(securityGUI, username, answer, a2):
    
    #if answers do not match - error
    if (answer.get() != a2.get()):
        messagebox.showwarning("Error", "Answers Do Not Match!")

    #if answers blank - error
    elif (answer.get() == "" or a2.get() == ""):
        messagebox.showwarning("Error", "Please Input Your Answers!")
        
    #else change answer
    else:
        #db code
        global client
        global db
        global records
        client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database('user_db')
        records = db.user_details

        #encrypt Security Answer
        encodedSecurityAnswer = answer.get().encode('utf-8')
        encSecurityAnswer = bcrypt.hashpw(encodedSecurityAnswer, bcrypt.gensalt(10))
        
        #change password
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})
        records.find_one_and_update({'username': userObject['username']},
                                    {'$set':{'securityAnswer': encSecurityAnswer} },
                                    return_document = ReturnDocument.AFTER)
        
        messagebox.showinfo("Success", "Security Answer Updated Successfully! ") #tells user password updated
        securityGUI.withdraw()

#change answer gui
def changeAnswer(screen, username):
    from PIL import ImageTk, Image #required for images

    #gui settings
    global securityGUI
    securityGUI = Toplevel(screen)
    securityGUI.title("Change Security Answer - Settings")
    securityGUI.geometry("428x200")
    securityGUI.configure(bg="#C0392B")

    #Change Answer Title
    aTitle = Label(securityGUI, text="Change Answer Question", bg="#C0392B", wraplengt=400)
    aTitle.config(font=('Courier',25))
    aTitle.pack(side=TOP, anchor=NW)

    #input
    answer = StringVar()
    Label(securityGUI, text="Please enter your new Security Answer: ", bg="#C0392B", wraplengt=400).pack()
    Entry(securityGUI, textvariable=answer, width = 30, bg='white', show = '*', fg='black').pack()

    #input
    answer2 = StringVar()
    Label(securityGUI, text="Please re-enter your new Security Answer: ", bg="#C0392B", wraplengt=400).pack()
    Entry(securityGUI, textvariable=answer2, width = 30, bg='white', show = '*', fg='black').pack()

    #proceed button
    proceedImg = Image.open("./Buttons/Settings/button_proceed.png").resize((100, 30))
    outputProceed = ImageTk.PhotoImage(proceedImg)
    
    proceedButton = Button(securityGUI, image = outputProceed,
                           command=lambda: checkAnswer(securityGUI, username, answer, answer2))

    proceedButton.image = outputProceed
    proceedButton.pack()
