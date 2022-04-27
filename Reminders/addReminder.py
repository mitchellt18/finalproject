#import required modules
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from tkcalendar import DateEntry
from PIL import ImageTk, Image #required for images
import re
import os
from datetime import date, datetime
import random
import numpy as np
import pandas as pd

#adds reminder to db
def addToDB(addGUI, offlineMode, username, billInput, dateEntry, reminderID):
    
    #offline mode
    if (offlineMode):
        #directory of local dataset
        excelFileName = './Reminders/reminders.xlsx'
        #read dataset into df
        df = pd.read_excel(excelFileName, sheet_name = 'reminders')

        #check if reminderID exists or not
        df2 = df.copy()
        df2.set_index('reminderID', inplace=True, drop=True)

        #while loop to get reminderID that is NOT in dataframe
        while (reminderID in df2.values):
            reminderID = random.randint(1000,9999) #gen new randomID

        #add reminder to df
        newReminderInput = {'reminderID': reminderID, 'Bill': billInput.get(), 'Date': dateEntry.get_date()}
        df = df.append(newReminderInput, ignore_index=True)

        #write df to xlsx file
        writer = pd.ExcelWriter(excelFileName, if_sheet_exists='overlay', engine='openpyxl', mode='a')
        df.to_excel(writer,
                    sheet_name = 'reminders',
                    index=False)
        writer.save()

        #success message
        messagebox.showinfo("Success", "Successfully Added Reminder!")

    #online mode
    else:
        #db code
        global client
        global db
        global records
        client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database('user_db')

        #user details collection
        records = db.user_details

        #reminders collection
        addReminderToDB = db.reminders

        #retireve user
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})

        #retrieve object ids
        objectID = userObject['objectIDReminders']

        #check if exists in db collection - if true, import into df
        if (objectID != "" and addReminderToDB.find_one({'_id': objectID[0]})):
            #retrieve objectID
            addReminderObject = addReminderToDB.find_one({'_id': objectID[0]},{'_id':0})
            #import from db to df
            df = pd.DataFrame([addReminderObject])
            #remove first element in objectID list since added to df
            objectID.pop(0) 

            #if remaining objectIDs present
            if (len(objectID)>0):
                for n in objectID:
                    addReminderObject = addReminderToDB.find_one({'_id': n},{'_id':0}) #retrieve next objectID
                    newDf = pd.DataFrame([addReminderObject]) #import from db to df
                    df = pd.concat([df, newDf]) #concat dfs

            #check if reminderID exists or not
            df2 = df.copy()
            df2.set_index('reminderID', inplace=True, drop=True)

            #while loop to get reminderID that is NOT in dataframe
            while (reminderID in df2.values):
                reminderID = random.randint(1000,9999) #gen new randomID

            #add new reminder input to df
            newReminderInput = {'reminderID': [reminderID], 'Bill': [billInput.get()], 'Date': [str(dateEntry.get_date())]}

            #create new df for new input
            newDf = pd.DataFrame(newReminderInput)

            #concat newdf and df
            df = pd.concat([df, newDf])

        #if no reminders, create new df and add new reminder
        else:
            #create new df
            newReminderInput = {'reminderID': [reminderID], 'Bill': [billInput.get()], 'Date': [str(dateEntry.get_date())]}
            #put new data in new df
            df = pd.DataFrame(newReminderInput)

        #add to db
        data = df.to_dict(orient='records') #convert dataframe to dictionary

        idObjectInsert = addReminderToDB.insert_many(data).inserted_ids #insert into db whilst retaining object id

        #insert objectid into user db
        records.find_one_and_update({'username': userObject['username']},
                                    {'$set':{'objectIDReminders': idObjectInsert} },
                                    return_document = ReturnDocument.AFTER)

        messagebox.showinfo("Success", "Successfully Added Reminder!") #tells user successfully added reminder
        
#check new reminder
def checkReminder(addGUI, offlineMode, username, billInput, dateEntry):
    from PIL import ImageTk, Image #required for images
    
    #if bill name blank - error
    if (billInput.get() == ""):
        messagebox.showwarning("Error", "Please Enter Bill Name")
        
    #if date selected is today - error
    elif (dateEntry.get_date() == date.today()):
        messagebox.showwarning("Error", "Please Select A Date Starting Tomorrow Onwards")
        
    #add to db
    else:
        addToDB(addGUI, offlineMode, username, billInput, dateEntry, random.randint(1000,9999))

#add reminder gui
def addReminder(screen, offlineMode, username):
    #setup the GUI
    global deleteGUI
    addGUI = Toplevel(screen)
    addGUI.title("Add a Reminder")
    addGUI.geometry("428x175")
    addGUI.configure(bg="#C0392B")

    #title of page
    addTitle = Label(addGUI, text="Add a Payment Reminder", bg="#C0392B", wraplengt=400)
    addTitle.config(font=('Courier',25))
    addTitle.pack()

    Label(addGUI, text="Please input the Bill Name:", bg='#C0392B').pack()

    #bill input
    billInput = StringVar()
    Entry(addGUI, textvariable = billInput, width = 30, bg='white', fg='black').pack()

    Label(addGUI, text="Please select when you want the Bill paid by:", bg='#C0392B').pack()

    #show calendar but restrict to only future dates
    dateEntry = DateEntry(addGUI, mindate = date.today(), locale='en_GB', date_pattern='dd/MM/yyyy')
    dateEntry.config(background = "#C0392B")
    dateEntry.pack()

    #add reminder button
    addImg = Image.open("./Buttons/Reminders/button_add.png").resize((100, 30))
    outputAdd = ImageTk.PhotoImage(addImg)
    
    addButton = Button(addGUI, image = outputAdd,
                           command = lambda: checkReminder(addGUI, offlineMode, username, billInput, dateEntry))

    addButton.image = outputAdd
    addButton.pack()

    
