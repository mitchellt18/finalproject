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

#import py files
from Reminders.deleteReminder import *
from Reminders.addReminder import *

#gui
def paymentReminders(screen, offlineMode, username):
    from PIL import ImageTk, Image #required for images
    
    #setup the GUI
    global remindersGUI
    remindersGUI = Toplevel(screen)
    remindersGUI.title("Payment Reminders")
    remindersGUI.geometry("620x390")
    remindersGUI.configure(bg="#C0392B")

    #title
    remindersTitle = Label(remindersGUI, text="Bill Payment Reminders", bg="#C0392B", wraplengt=400)
    remindersTitle.config(font=('Courier',25))
    remindersTitle.pack()

    #var to check if reminders empty or not
    empty = False

    #check if dataset is empty or not
    
    #offline mode
    if (offlineMode):
        #checks if dataset exists
        exists = os.path.isfile('./Reminders/reminders.xlsx')

        #if it doesn't exist - creates local dataset
        if (not exists):
            #create df with titles
            df = pd.DataFrame({'reminderID': [], 'Bill': [], 'Date': []})
            #creates reminder xlsx file
            writer = pd.ExcelWriter('./Reminders/reminders.xlsx', engine='xlsxwriter')
            #sheet for reminder in xlsx file
            df.to_excel(writer, sheet_name='reminders', index=False)
            writer.save()

        #put into df
        df = pd.read_excel(
            './Reminders/reminders.xlsx',
            sheet_name = 'reminders',
            index_col = 0,
            )

        #if df is empty, alerts user to add data
        if (df.empty):
            empty = True
            
        df.reset_index(drop=False, inplace=True)


    #online mode
    else:
        #db code
        global client
        global db
        global records
        client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database('user_db') #get data from correct db

        #user details collection
        records = db.user_details

        #reminders collection
        reminderRecords = db.reminders
        
        #retrieves user from db
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})
        
        objectID = userObject['objectIDReminders'] #retrieve correct object ids

        #if reminders exist - import to df
        if (objectID != "" and reminderRecords.find_one({'_id': objectID[0]})):

            #import data into df
            reminderObject = reminderRecords.find_one({'_id': objectID[0]},{'_id':0})

            #put data into df
            df = pd.DataFrame([reminderObject])

            #remove data from array as now retrieved
            objectID.pop(0)

            #if remaining objectIDs present
            if (len(objectID)>0):
                #loop over objectID array
                for n in objectID:
                    #import df date
                    reminderObject = reminderRecords.find_one({'_id': n},{'_id':0})
                    #put data into df
                    newDf = pd.DataFrame([reminderObject])
                    #concat both dfs
                    df = pd.concat([df, newDf])
                    
        #otherwise df is empty       
        else:
            empty = True

    #if df empty, display empty message
    if (empty):
        Label(remindersGUI, text="You Have No Reminders!", bg='#C0392B').pack()

    #else df is not empty, so retrieve reminders and output
    else:
        Label(remindersGUI, text="Below are your Reminders:", bg='#C0392B').pack()
        
        #set date dtype to datetime object when imported from online db
        if (not offlineMode):
            df['Date'] = pd.to_datetime(df['Date'])

        #import df by date so important reminders appear first
        df = df.sort_values(by='Date')

        #all reminders due within 2 days are stored in this df
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

    #if user has reminders in next 2 days, the bill names are outputted as an alert
    if (not empty):
        if (not df_2days.empty):
            urgentBills = df_2days['Bill'].values.tolist()

            messagebox.showwarning("ATTENTION", "You Have Bills Due in the Next 2 Days! Ensure To Pay For The Following Bills: " + ', '.join(urgentBills)) #alerts users of near bills
    
