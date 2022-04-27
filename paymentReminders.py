#import required modules
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pymongo import MongoClient
#local dataset modules
from PIL import ImageTk, Image
import os
import re
from datetime import date, datetime

import numpy as np
import pandas as pd

from deleteReminder import *
from addReminder import *

def paymentReminders(screen, offlineMode, username):
    from PIL import ImageTk, Image #required for images
    #setup the GUI
    global remindersGUI
    remindersGUI = Toplevel(screen)
    remindersGUI.title("Payment Reminders")
    remindersGUI.geometry("620x390")
    remindersGUI.configure(bg="#C0392B")

    #title of page
    remindersTitle = Label(remindersGUI, text="Bill Payment Reminders", bg="#C0392B", wraplengt=400)
    remindersTitle.config(font=('Courier',25))
    remindersTitle.pack()
    empty = False

    #firstly check if the dataset for reminders exists, in online or offline mode
    #if the user is in offline mode, open/create local dataset
    if (offlineMode):
        exists = os.path.isfile('reminders.xlsx') #checks if required dataset exists

        if (not exists):
            df = pd.DataFrame({'reminderID': [], 'Bill': [], 'Date': []}) #sets titles in xlsx file
            writer = pd.ExcelWriter('reminders.xlsx', engine='xlsxwriter') #creates expenditures dataset
            df.to_excel(writer, sheet_name='reminders', index=False) #sheet for reminders
            writer.save()

        #put into dataframe
        df = pd.read_excel(
            './reminders.xlsx',
            sheet_name = 'reminders',
            index_col = 0,
            )

        #if dataset is empty, alerts user to add data
        if (df.empty):
            empty = True
            
        df.reset_index(drop=False, inplace=True)


    #else if user is in online mode, retrieve from online db
    else:
        #establish a connection with db
        global client
        global db
        global records
        client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database('user_db') #get data from db
        records = db.user_details #get user details from user document
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)}) #retireve logged in user
        reminderRecords = db.reminders #get data from reminders document
        objectID = userObject['objectIDReminders'] #retrieve correct object ids

        #check if existing reminders in the collection, if so, need to import to df
        if (objectID != "" and reminderRecords.find_one({'_id': objectID[0]})):
            
            reminderObject = reminderRecords.find_one({'_id': objectID[0]},{'_id':0}) #import df data from db
            df = pd.DataFrame([reminderObject]) #put df data into a new df
            objectID.pop(0) #remove first element in objectID list since added to df

            #if remaining objectIDs present
            if (len(objectID)>0):
                for n in objectID:
                    reminderObject = reminderRecords.find_one({'_id': n},{'_id':0}) #import df data from db
                    newDf = pd.DataFrame([reminderObject]) #put df data into a new df
                    df = pd.concat([df, newDf])
                    
        else:
            empty = True #empty dataset for user

    if (empty):
        Label(remindersGUI, text="You Have No Reminders!", bg='#C0392B').pack()
    else:
        #put df into table to display to user
        Label(remindersGUI, text="Below are your Reminders:", bg='#C0392B').pack()
        
        #set date dtype to datetime object when imported from online db
        if (not offlineMode):
            df['Date'] = pd.to_datetime(df['Date']) #date needs to be datetime object

        df = df.sort_values(by='Date') #order df by date so important reminders appear first

        df_2days = df[df['Date'] < datetime.now() + pd.to_timedelta("2 days")]
        
        #create treeview frame
        outputFrame = ttk.Treeview(remindersGUI, columns=list(df[['reminderID', 'Bill', 'Date']]), show='headings')

        #insert column headers of dataframe into tree
        for col in list(df[['reminderID', 'Bill', 'Date']]):
            outputFrame.heading(col, text=col)
        outputFrame.pack()

        #insert contents of dataframe into tree
        for val in df[['reminderID', 'Bill', 'Date']].values.tolist():
            outputFrame.insert("", "end", values=val)

    #buttons for adding/deleting reminders

    #add reminder
    addImg = Image.open("./Buttons/Reminders/button_add-reminder.png")
    outputadd = ImageTk.PhotoImage(addImg)
    
    addButton = Button(remindersGUI, image = outputadd,
                            command = lambda: addReminder(remindersGUI, offlineMode, username))

    addButton.image = outputadd
    addButton.pack(side=LEFT, anchor=W, expand=True)

    #delete reminder
    delImg = Image.open("./Buttons/Reminders/button_delete-reminder.png")
    outputdel = ImageTk.PhotoImage(delImg)
    
    delButton = Button(remindersGUI, image = outputdel,
                            command=lambda: deleteReminder(remindersGUI, offlineMode, username, df))

    delButton.image = outputdel
    delButton.pack(side=RIGHT, anchor=E, expand=True)

    

    if (not df_2days.empty):
        urgentBills = df_2days['Bill'].values.tolist()

        messagebox.showwarning("ATTENTION", "You Have Bills Due in the Next 2 Days! Ensure To Pay For The Following Bills: " + ', '.join(urgentBills)) #alerts users of near bills
    
