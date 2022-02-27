from tkinter import *
from pymongo import MongoClient
from tkinter import messagebox
from pymongo.collection import ReturnDocument
import re

#establish connection with db
global client
global db
global records
client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('user_db')
records = db.user_details

#change security question functions

def checkQuestion(securityGUI, username, securityQuestion):
    #check security questions
    if (securityQuestion.get() == ""):
        messagebox.showwarning("Error", "Please Ensure Security Details Are Filled!") #check if security details is not filled
        
    else:
        #change security question
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})
        records.find_one_and_update({'username': userObject['username']},
                                    {'$set':{'securityQuestion': securityQuestion.get()} },
                                    return_document = ReturnDocument.AFTER)
        messagebox.showinfo("Success", "Security Question Updated Successfully! ") #tells user question updated
        securityGUI.withdraw()

def changeQuestion(screen, username):
    global securityGUI
    securityGUI = Toplevel(screen)
    securityGUI.title("Change Security Question - Settings")
    securityGUI.geometry("428x125")
    securityGUI.configure(bg="#C0392B")

    #Change Question Title
    qTitle = Label(securityGUI, text="Change Security Question", bg="#C0392B", wraplengt=400)
    qTitle.config(font=('Courier',25))
    qTitle.pack(side=TOP, anchor=NW)

    #input
    question = StringVar()
    Label(securityGUI, text="Please enter your new Security Question: ", bg="#C0392B", wraplengt=400).pack()
    Entry(securityGUI, textvariable=question, width = 30, bg='white', fg='black').pack()

    #button
    proceed = Button(securityGUI, text="Proceed", bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                         command=lambda: checkQuestion(securityGUI, username, question)).pack()
