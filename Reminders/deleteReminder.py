#import required modules
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
from PIL import ImageTk, Image #required for images
import re
import os
from datetime import date, datetime
from bson.objectid import ObjectId
import pandas as pd

#delete reminder from db
def deleteFromDB(deleteGUI, offlineMode, username, delInt, df):

    #if reminder id blank - error
    if (delInt.get() == ""):
        messagebox.showwarning("Error", "Please Input Reminder ID")

    #if reminder id is not 4 digits - error
    elif (len(delInt.get()) != 4):
        messagebox.showwarning("Error", "Reminder IDs are only 4 in length")

    else:
        #try to find reminder
        try:
            delInt = int(delInt.get()) #convert input to integer
            
            #check if reminderID exists or not
            df2 = df.copy()

            #if reminder found - delete reminder
            if (delInt in df2.values):
                #delete reminder from df
                df2.set_index('reminderID', inplace=True, drop=True)
                df2 = df2.drop([delInt])
                
                #offline mode
                if (offlineMode):
                    #re-write df into dataset
                    excelFileName = './Reminders/reminders.xlsx'
                    df2.reset_index(drop=False, inplace=True)
                    #write df to xlsx file
                    writer = pd.ExcelWriter(excelFileName, engine='openpyxl', mode='w')
                    df2.to_excel(writer,
                                sheet_name = 'reminders',
                                index=False)
                    writer.save()

                #online mode
                else:
                    #db code
                    global client
                    global db
                    global records
                    client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                    db = client.get_database('user_db')
                    records = db.user_details
                    userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)}) #logged in user
                    removeReminderFromDB = db.reminders

                    #re-write df into db
                    objectID = userObject['objectIDReminders'] #retrieve correct object ids

                    #loop through objectIDs, if reminderID matches, delete from objectID array
                    for n in objectID:
                        reminderObject = removeReminderFromDB.find_one({'_id': n},{'_id':0})
                        if (reminderObject['reminderID'] == delInt):
                            
                            #remove reminderObject from removeReminderFromDB and userObject

                            #remove from reminders db collection
                            removeReminderFromDB.delete_one({'_id': ObjectId(n)})

                            #remove objectID from correct user document in user collection
                            records.find_one_and_update({'_id': userObject.get('_id')}, {'$pull': {'objectIDReminders': n}})

                #success message
                messagebox.showinfo("Success!", "Reminder Removed")
                
            #if error - reminder not found
            else:
                messagebox.showwarning("Error", "Reminder Not Found")
                
        #if non integer values inputted - error
        except:
            messagebox.showwarning("Error", "Please Ensure to Input Integer Values ONLY")

#delete reminder gui
def deleteReminder(screen, offlineMode, username, df):
    from PIL import ImageTk, Image #required for images
    
    #setup the GUI
    global deleteGUI
    deleteGUI = Toplevel(screen)
    deleteGUI.title("Delete a Reminder")
    deleteGUI.geometry("428x150")
    deleteGUI.configure(bg="#C0392B")

    #title of page
    delTitle = Label(deleteGUI, text="Delete a Payment Reminder", bg="#C0392B", wraplengt=400)
    delTitle.config(font=('Courier',25))
    delTitle.pack()

    Label(deleteGUI, text="Please input the Reminder ID you wish to delete:", bg='#C0392B').pack()
    
    delInt = StringVar()
    Entry(deleteGUI, textvariable = delInt, width = 10, bg='white', fg='black').pack()

    #add reminder button
    delImg = Image.open("./Buttons/Reminders/button_delete.png").resize((100, 30))
    outputDel = ImageTk.PhotoImage(delImg)
    
    delButton = Button(deleteGUI, image = outputDel,
                           command = lambda: deleteFromDB(deleteGUI, offlineMode, username, delInt, df))

    delButton.image = outputDel
    delButton.pack()

    
