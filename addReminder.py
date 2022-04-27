#import required modules
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from tkcalendar import DateEntry
#local dataset modules
from PIL import ImageTk, Image #required for images
import re
import os
from datetime import date, datetime
import random
import numpy as np
import pandas as pd


def addToDB(addGUI, offlineMode, username, billInput, dateEntry, reminderID):
    
    #if offline, input into excel file
    if (offlineMode):

        excelFileName = 'reminders.xlsx'
        df = pd.read_excel(excelFileName, sheet_name = 'reminders') #read dataset into dataframe

        #check if reminderID exists or not
        df2 = df.copy()
        df2.set_index('reminderID', inplace=True, drop=True)

        #while loop to get reminderID that is NOT in dataframe
        while (reminderID in df2.values):
            reminderID = random.randint(1000,9999) #gen new randomID

        #add reminderID, reminder and date to dataframe
        newReminderInput = {'reminderID': reminderID, 'Bill': billInput.get(), 'Date': dateEntry.get_date()}
        df = df.append(newReminderInput, ignore_index=True)

        #write df to xlsx file
        writer = pd.ExcelWriter(excelFileName, if_sheet_exists='overlay', engine='openpyxl', mode='a')
        df.to_excel(writer,
                    sheet_name = 'reminders',
                    index=False)
        writer.save()

        messagebox.showinfo("Success", "Successfully Added Reminder!") #tells user successfully added reminder

    #if online, input into online db
    else:
        global client
        global db
        global records
        client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database('user_db')
        records = db.user_details
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)}) #logged in user
        addReminderToDB = db.reminders

        objectID = userObject['objectIDReminders'] #retrieve correct object ids

        #check if existing reminders in the collection, if so, need to import to df
        if (objectID != "" and addReminderToDB.find_one({'_id': objectID[0]})):
            addReminderObject = addReminderToDB.find_one({'_id': objectID[0]},{'_id':0}) #import df data from db
            df = pd.DataFrame([addReminderObject]) #put df data into a new df
            objectID.pop(0) #remove first element in objectID list since added to df

            #if remaining objectIDs present
            if (len(objectID)>0):
                for n in objectID:
                    addReminderObject = addReminderToDB.find_one({'_id': n},{'_id':0}) #import df data from db
                    newDf = pd.DataFrame([addReminderObject]) #put df data into a new df
                    df = pd.concat([df, newDf])

            #df = df.set_index('reminderID')
            #df = df.astype(np.float64) #set dtype

            #check if reminderID exists or not
            df2 = df.copy()
            df2.set_index('reminderID', inplace=True, drop=True)

            #while loop to get reminderID that is NOT in dataframe
            while (reminderID in df2.values):
                reminderID = random.randint(1000,9999) #gen new randomID

            #add new reminder input to df
            newReminderInput = {'reminderID': [reminderID], 'Bill': [billInput.get()], 'Date': [str(dateEntry.get_date())]}

            #need to create new df for new input to concat with old df
            newDf = pd.DataFrame(newReminderInput)

            df = pd.concat([df, newDf])
            #print(newDf)
            #print(df)

        #if there are no reminders present, need to create new df to add
        else:
            #create new df with reminderID, reminder and date
            newReminderInput = {'reminderID': [reminderID], 'Bill': [billInput.get()], 'Date': [str(dateEntry.get_date())]}
            df = pd.DataFrame(newReminderInput) #put new data in new df
            #print("NO EXISTING REMINDERS")
            #print(df)

        #now add to db
        data = df.to_dict(orient='records') #convert dataframe to dictionary

        idObjectInsert = addReminderToDB.insert_many(data).inserted_ids #insert into db whilst retaining object id

        #insert objectid into user db
        records.find_one_and_update({'username': userObject['username']},
                                    {'$set':{'objectIDReminders': idObjectInsert} },
                                    return_document = ReturnDocument.AFTER)

        messagebox.showinfo("Success", "Successfully Added Reminder!") #tells user successfully added reminder

def checkReminder(addGUI, offlineMode, username, billInput, dateEntry):
    from PIL import ImageTk, Image #required for images
    #check if bill name is inputted
    if (billInput.get() == ""):
        messagebox.showwarning("Error", "Please Enter Bill Name")
    #check if date is inputted
    elif (dateEntry.get_date() == date.today()):
        messagebox.showwarning("Error", "Please Select A Date Starting Tomorrow Onwards")
        
    #if all passes then can add to db
    else:
        addToDB(addGUI, offlineMode, username, billInput, dateEntry, random.randint(1000,9999))

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
    
    billInput = StringVar()
    Entry(addGUI, textvariable = billInput, width = 30, bg='white', fg='black').pack()

    Label(addGUI, text="Please select when you want the Bill paid by:", bg='#C0392B').pack()

    #show calendar but restrict to only future dates
    dateEntry = DateEntry(addGUI, mindate = date.today(), locale='en_GB', date_pattern='dd/MM/yyyy')
    dateEntry.config(background = "#C0392B")
    dateEntry.pack()

    #add reminder
    addImg = Image.open("./Buttons/Reminders/button_add.png").resize((100, 30))
    outputAdd = ImageTk.PhotoImage(addImg)
    
    addButton = Button(addGUI, image = outputAdd,
                           command = lambda: checkReminder(addGUI, offlineMode, username, billInput, dateEntry))

    addButton.image = outputAdd
    addButton.pack()

    
