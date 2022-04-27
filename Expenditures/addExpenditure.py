#import required modules
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from PIL import ImageTk, Image
import re
import os
from datetime import date, datetime
import pandas as pd
from openpyxl import load_workbook
import math
import numpy as np

#checks inputted expenditure details
def checkDetails(screen, selected_option, expenditureName, expenditureCost, offlineMode, expenditureType, username):
    
    #check if number is float
    def checkFloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False        

    #if expenditure name is blank - error
    if (expenditureName.get() == ""):
        messagebox.showwarning("Error", "Please Enter Expenditure Name")

    #if expenditure cost is blank - error
    elif (expenditureCost.get() == ""):
        messagebox.showwarning("Error", "Please Enter Expenditure Cost")

    #if expenditure cost is not interger or float - error
    elif (checkFloat(expenditureCost.get()) == False):
        messagebox.showwarning("Error", "Please Ensure Expenditure Cost is Integer or Float Values Only!")

    #if correct - input all data
    else:
        
        #offline mode
        if (offlineMode):

            #local dataset directory
            excelFileName = './Expenditures/expenditures.xlsx'

            #if expendituretype is monthly - retrieve monthly bill sheet
            if (expenditureType == 'm'):
                df = pd.read_excel(excelFileName, sheet_name = 'monthlyBill')

            #if expendituretype is disposable - retrieve disposable bill sheet
            else:
                df = pd.read_excel(excelFileName, sheet_name = 'disposibleIncome')
                
            #check if current month exists in dataset or not
            try:
                #try retrieving current month data
                df[datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)]
                
            except:
                #if unable to retrieve current month data - add new month to df
                df[datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)] = math.nan

            #check if current expenditure exists or not
            try:
                #create copy of existing df
                df2 = df.copy()
                df2.set_index('Bill', inplace=True, drop=True)

                #try retrieving current expenditure data
                df2.loc[[expenditureName.get()]]
                
                #replace existing value if current expenditure exists
                df.loc[df.index[df['Bill']==expenditureName.get()].tolist(), datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)] = expenditureCost.get()
                
            except:
                #if unable to retrieve current expenditure - add new expenditure to df
                df = df.append({'Bill': expenditureName.get(),
                                datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0): expenditureCost.get()},
                               ignore_index=True)

            #write df to xlsx file
            writer = pd.ExcelWriter(excelFileName, if_sheet_exists='overlay', engine='openpyxl', mode='a')

            #if monthly bill - write to monthly bill sheet
            if (expenditureType == 'm'):
                df.to_excel(writer,
                            sheet_name = 'monthlyBill',
                            index=False)
                writer.save()

            #if disposable bill - write to disposable bill sheet
            else:
                df.to_excel(writer,
                            sheet_name = 'disposibleIncome',
                            index=False)
                writer.save()

            #success message
            messagebox.showinfo("Success", "Successfully Added Expenditure!")

        #online mode
        else:
            #db code
            global client
            global db
            global records
            client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = client.get_database('user_db')
            records = db.user_details
            
            #find user
            userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})

            #check if replacing existing document is necessary (if it already exists)
            replace = False

            #if expenditure is monthly bill
            if (expenditureType == 'm'):
                #read in correct collection and object ids
                addExpenditureDB = db.monthly_bills
                objectID = userObject['objectIDMonthly']
                
            #if expenditure is disposable bill
            else:
                #read in correct collection and object ids
                addExpenditureDB = db.disposible_bills
                objectID = userObject['objectIDDisposible'] 

            #check if exists in db collection - if true, import into df
            if (objectID != "" and addExpenditureDB.find_one({'_id': objectID[0]})):
                replace = True #replaces old objectID in db
                addExpenditureObject = addExpenditureDB.find_one({'_id': objectID[0]},{'_id':0}) #retrieve objectID
                df = pd.DataFrame([addExpenditureObject]) #import from db to df
                objectID.pop(0) #remove first element in objectID list since added to dataframe
                
                #if remaining objectIDs present
                if (len(objectID) > 0):
                    for n in objectID:
                        addExpenditureObject = addExpenditureDB.find_one({'_id': n},{'_id':0}) #retrieve next objectID
                        newDf = pd.DataFrame([addExpenditureObject]) #import from db to df
                        df = pd.concat([df, newDf]) #concat dfs
                
                df = df.set_index('Bill') #set index
                df = df.astype(np.float64) #set dtype
                
            #else create blank df to add new expenditure to
            else:
                #create new df
                newDfData = {'Bill': [expenditureName.get()],
                        str(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)): [expenditureCost.get()]}
                #put new expenditure into df
                df = pd.DataFrame(newDfData)

            #check if current month exists
            try:
                #try retrieving current month data
                df[str(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0))]
            except:
                #if unable to retrieve current month data - add new month to df
                df[str(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0))] = math.nan

            #check if current expenditure exists
            try:
                #create copy of existing df
                df2 = df.copy()
                df2.set_index('Bill', inplace=True, drop=True)

                #try retrieving current expenditure data
                df2.loc[[expenditureName.get()]]
                
                #replace existing value if current expenditure exists
                df.loc[df.index[df['Bill']==expenditureName.get()].tolist(), str(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0))] = expenditureCost.get()
                
            except:
                #if unable to retrieve current expenditure - create new df, put new input into df and concat old and new together
                
                #new data
                newDfData = {'Bill': [expenditureName.get()],
                        str(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)): [expenditureCost.get()]}
                
                newDf = pd.DataFrame(newDfData) #input into new df
                newDf = newDf.set_index('Bill') #set index
                newDf = newDf.astype(np.float64)

                #concat new and old df
                df = pd.concat([df, newDf])
                
            #put df back into db

            #check if replacing old objectIDs
            if (replace==True):
                for object_ID in objectID:
                    addExpenditureDB.delete_one({'_id':object_ID})
                df = df.reset_index() #reset index

            data = df.to_dict(orient='records') #convert dataframe to dictionary
            
            idObjectInsert = addExpenditureDB.insert_many(data).inserted_ids #insert into db whilst retaining object id

            #insert objectid into user db
            if (expenditureType == 'm'):
                records.find_one_and_update({'username': userObject['username']},
                                            {'$set':{'objectIDMonthly': idObjectInsert} },
                                            return_document = ReturnDocument.AFTER)
            else:
                records.find_one_and_update({'username': userObject['username']},
                                            {'$set':{'objectIDDisposible': idObjectInsert} },
                                            return_document = ReturnDocument.AFTER)

            #success message to user
            messagebox.showinfo("Success", "Successfully Added Expenditure!")
  
#next gui
def selectedOption(screen, offlineMode, username, selected_option, expenditureType):
    from PIL import ImageTk, Image #required for images

    #if variable bill
    if (selected_option == 'V'):
        messagebox.showwarning("Error", "Feature Not Yet Implemented. You can only add fixed bills for now.") #feature not yet implemented as requires ai model implementation
    #if no option selected - error
    elif (selected_option == ''):
        messagebox.showwarning("Error", "Please Select an Option")
    #fixed bill
    else:
        #GUI settings
        global addExpenditure2GUI
        addExpenditure2GUI = Toplevel(screen)
        addExpenditure2GUI.geometry("428x250")
        addExpenditure2GUI.configure(bg="#C0392B")

        #if monthly bill - correct title 
        if (expenditureType == 'm'):
            addExpenditure2GUI.title("Monthly Bills Tracker")
            #Title
            title = Label(addExpenditure2GUI, text="Monthly Bills Tracker", bg="#C0392B", wraplengt=400)
            title.config(font=('Courier',25))
            title.pack(side=TOP, anchor=NW)

        #if disposable income - correct title
        else:
            addExpenditure2GUI.title("Disposable Income Tracker")
            #Title
            title = Label(addExpenditure2GUI, text="Disposable Income Tracker", bg="#C0392B", wraplengt=400)
            title.config(font=('Courier',25))
            title.pack(side=TOP, anchor=NW)

        #Labels
        Label(addExpenditure2GUI, text="Add Expenditure", bg="#C0392B").pack()

        #expenditure name input
        expenditureName = StringVar()
        Label(addExpenditure2GUI, text="Expenditure Name", bg="#C0392B", wraplengt=400).pack()
        Entry(addExpenditure2GUI, textvariable=expenditureName, width = 30, bg='white', fg='black').pack()
        
        #cost of bill input
        expenditureCost = StringVar()
        Label(addExpenditure2GUI, text="Cost of Expenditure", bg="#C0392B", wraplengt=400).pack()
        Entry(addExpenditure2GUI, textvariable=expenditureCost, width = 30, bg='white', fg='black').pack()
    
        #add Expenditure button
        addImg = Image.open("./Buttons/Expenditures/button_add.png")
        outputAdd = ImageTk.PhotoImage(addImg)
        
        addExpenditureButton = Button(addExpenditure2GUI, image = outputAdd,
                               command=lambda: checkDetails(addExpenditure2GUI, selected_option, expenditureName, expenditureCost, offlineMode, expenditureType, username))

        addExpenditureButton.image = outputAdd
        addExpenditureButton.pack()

#first screen for adding expenditure
def addExpenditure(screen, offlineMode, username, expenditureType):
    from PIL import ImageTk, Image #required for images

    #gui settings
    global addExpenditureGUI
    addExpenditureGUI = Toplevel(screen)
    addExpenditureGUI.configure(bg="#C0392B")

    #if monthly bill - correct title and radio buttons
    if (expenditureType == 'm'):
        addExpenditureGUI.title("Monthly Bills Tracker")
        addExpenditureGUI.geometry("428x250")
        
        #Title
        title = Label(addExpenditureGUI, text="Monthly Bills Tracker", bg="#C0392B", wraplengt=400)
        title.config(font=('Courier',25))
        title.pack(side=TOP, anchor=NW)

        #Labels
        Label(addExpenditureGUI, text="Add Expenditure", bg="#C0392B").pack()

        Label(addExpenditureGUI, text="Fixed or Variable Bill?", bg="#C0392B").pack()

        #radiobutton
        selected_option = StringVar()
        option_list = (('Fixed', 'F'),
                   ('Variable', 'V'))
        for o in option_list:
            option = Radiobutton(addExpenditureGUI, text=o[0], value = o[1], variable = selected_option, bg="#C0392B")
            option.pack()

        #add expenditure button
        addImg = Image.open("./Buttons/Expenditures/button_continue.png")
        outputAdd = ImageTk.PhotoImage(addImg)
        
        addExpenditureButton = Button(addExpenditureGUI, image = outputAdd,
                               command=lambda: selectedOption(screen, offlineMode, username, selected_option.get(), expenditureType))

        addExpenditureButton.image = outputAdd
        addExpenditureButton.pack()

    #if disposable income - no need for radio buttons so just continue button
    else:
        addExpenditureGUI.title("Disposable Income Tracker")
        addExpenditureGUI.geometry("428x150")
        
        #Title
        title = Label(addExpenditureGUI, text="Disposable Income Tracker", bg="#C0392B", wraplengt=400)
        title.config(font=('Courier',25))
        title.pack(side=TOP, anchor=NW)

        #Labels
        Label(addExpenditureGUI, text="Add Expenditure", bg="#C0392B").pack()

        #add expenditure button
        addImg = Image.open("./Buttons/Expenditures/button_continue.png")
        outputAdd = ImageTk.PhotoImage(addImg)
        
        addExpenditureButton = Button(addExpenditureGUI, image = outputAdd,
                               command=lambda: selectedOption(screen, offlineMode, username, 'F', expenditureType))

        addExpenditureButton.image = outputAdd
        addExpenditureButton.pack()

    
    

