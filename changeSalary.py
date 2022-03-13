from tkinter import *
from pymongo import MongoClient
from tkinter import messagebox
from pymongo.collection import ReturnDocument
import re

#change salary functions
def checkSalary(salaryGUI, username, salary):
    #checks if input is a float
    def checkFloat(salary):
        try:
            float(salary)
            return True
        except ValueError:
            return False
        
    #check salary
    if (salary.get() == ""):
        messagebox.showwarning("Error", "Please Input Salary!") #check if salary is blank
    elif (checkFloat(salary.get()) == False):
        messagebox.showwarning("Error", "Ensure Salary ONLY Contains Integer or Float Values!") #check if salary is not float
    else:
        #establish connection with db
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

def changeSalary(screen, username):
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
    Label(salaryGUI, text="Please enter your salary in GBP (£): ", bg="#C0392B", wraplengt=400).pack()
    Entry(salaryGUI, textvariable=salary, width = 30, bg='white', fg='black').pack()

    #button
    proceed = Button(salaryGUI, text="Proceed", bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                         command=lambda: checkSalary(salaryGUI, username, salary)).pack()
