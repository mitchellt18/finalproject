from tkinter import *
from pymongo import MongoClient
from tkinter import messagebox
from pymongo.collection import ReturnDocument
import re
import os
from PIL import ImageTk, Image #required for images

#changes salary
def checkSalary(salaryGUI, username, salary):
    #checks if input is a float
    def checkFloat(salary):
        try:
            float(salary)
            return True
        except ValueError:
            return False
        
    #if salary is blank - error
    if (salary.get() == ""):
        messagebox.showwarning("Error", "Please Input Salary!")

    #if salary is not float or int - error
    elif (checkFloat(salary.get()) == False):
        messagebox.showwarning("Error", "Ensure Salary ONLY Contains Integer or Float Values!")
    else:
        #db code
        global client
        global db
        global records
        client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database('user_db')
        records = db.user_details
        
        #change salary
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})
        records.find_one_and_update({'username': userObject['username']},
                                    {'$set':{'salary': salary.get()} },
                                    return_document = ReturnDocument.AFTER)
        
        messagebox.showinfo("Success", "Salary Updated Successfully! ") #tells user salary updated
        salaryGUI.withdraw()

#change salary gui
def changeSalary(screen, username):
    from PIL import ImageTk, Image #required for images

    #gui settings
    global salaryGUI
    salaryGUI = Toplevel(screen)
    salaryGUI.title("Change Salary - Settings")
    salaryGUI.geometry("428x125")
    salaryGUI.configure(bg="#C0392B")

    #Change Salary Title
    salaryTitle = Label(salaryGUI, text="Change Salary", bg="#C0392B", wraplengt=400)
    salaryTitle.config(font=('Courier',25))
    salaryTitle.pack(side=TOP, anchor=NW)

    #input
    salary = StringVar()
    Label(salaryGUI, text="Please enter your salary in GBP (??): ", bg="#C0392B", wraplengt=400).pack()
    Entry(salaryGUI, textvariable=salary, width = 30, bg='white', fg='black').pack()

    #proceed button
    proceedImg = Image.open("./Buttons/Settings/button_proceed.png").resize((100, 30))
    outputProceed = ImageTk.PhotoImage(proceedImg)
    
    proceedButton = Button(salaryGUI, image = outputProceed,
                           command=lambda: checkSalary(salaryGUI, username, salary))

    proceedButton.image = outputProceed
    proceedButton.pack()
