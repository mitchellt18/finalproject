#import required modules
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
import re
from datetime import date, datetime
#import datetime
import pandas as pd
from openpyxl import load_workbook
import math
import numpy as np

def checkDetails(screen, selected_option, expenditureName, expenditureCost, offlineMode, expenditureType, username):
    #function to check if number is float
    def checkFloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False        

    #check expenditure name
    if (expenditureName.get() == ""):
        messagebox.showwarning("Error", "Please Enter Expenditure Name") #expenditure name missing

    #check expenditure cost
    elif (expenditureCost.get() == ""):
        messagebox.showwarning("Error", "Please Enter Expenditure Cost") #expenditure cost missing
    elif (checkFloat(expenditureCost.get()) == False):
        messagebox.showwarning("Error", "Please Ensure Expenditure Cost is Integer or Float Values Only!") #expenditure cost incorrect

    #if correct, input all data
    else:
        #offline mode
        if (offlineMode):
            excelFileName = 'expenditures.xlsx'

            if (expenditureType == 'm'):
                df = pd.read_excel(excelFileName, sheet_name = 'monthlyBill') #read dataset into dataframe
            else:
                df = pd.read_excel(excelFileName, sheet_name = 'disposibleIncome') #read dataset into dataframe

            #check if current month exists or not
            try:
                df[datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)] #retrieves current month data
            except:
                df[datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)] = math.nan #add new month to dataframe if doesn't exist

            #check if current expenditure exists or not
            try:
                #create copy of existing dataframe, to check if existing expenditure exists w/o messing up original expenditure
                df2 = df.copy()
                df2.set_index('Bill', inplace=True, drop=True)
                df2.loc[[expenditureName.get()]] #if this doesn't work then it proceeds to except block
                
                #replace existing value
                df.loc[df.index[df['Bill']==expenditureName.get()].tolist(), datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)] = expenditureCost.get()
                
            except:
                df = df.append({'Bill': expenditureName.get(),
                                datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0): expenditureCost.get()},
                               ignore_index=True)

            #write to xlsx file
            writer = pd.ExcelWriter(excelFileName, if_sheet_exists='overlay', engine='openpyxl', mode='a')
            if (expenditureType == 'm'):
                df.to_excel(writer,
                            sheet_name = 'monthlyBill',
                            index=False)
                writer.save()
            else:
                df.to_excel(writer,
                            sheet_name = 'disposibleIncome',
                            index=False)
                writer.save()
            
            messagebox.showinfo("Success", "Successfully Added Expenditure!") #tells user successfully added

        #online mode
        else:
            global client
            global db
            global records
            client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = client.get_database('user_db')
            records = db.user_details
            userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)}) #user
            replace=False #replace existing document if exists already
            
            if (expenditureType == 'm'):
                addExpenditureDB = db.monthly_bills #read in correct database collection
                objectID = userObject['objectIDMonthly'] #retrieve correct object id 
            else:
                addExpenditureDB = db.disposible_bills #read in correct database collection
                objectID = userObject['objectIDDisposible'] #retrieve correct object id

            #check if the document exists in the collection
            #if it does exist, need to import dataframe
            if (objectID != "" and addExpenditureDB.find_one({'_id': objectID[0]})):
                replace = True #convert stored into dataframe, but do not import username or id

                addExpenditureObject = addExpenditureDB.find_one({'_id': objectID[0]},{'_id':0}) #import dataframe data from db
                df = pd.DataFrame([addExpenditureObject]) #put dataframe data into a new dataframe
                objectID.pop(0) #remove first element in objectID list since added to dataframe
                
                #if remaining objectIDs present
                if (len(objectID) > 0):
                    for n in objectID:
                        addExpenditureObject = addExpenditureDB.find_one({'_id': n},{'_id':0}) #import dataframe data from db
                        newDf = pd.DataFrame([addExpenditureObject]) #put dataframe data into a new dataframe
                        df = pd.concat([df, newDf])
                
                df = df.set_index('Bill') #set index
                df = df.astype(np.float64) #set dtype
                
            #if it doesn't exist, need to create new dataframe
            else:
                #create new dataframe
                newDfData = {'Bill': [expenditureName.get()],
                        str(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)): [expenditureCost.get()]}
                df = pd.DataFrame(newDfData) #put data in new dataframe

            #check if current month exists or not
            try:
                df[str(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0))] #retrieves current month data
            except:
                df[str(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0))] = math.nan #add new month to dataframe if doesn't exist

            #check if current expenditure exists or not
            try:
                #create copy of existing dataframe, to check if existing expenditure exists w/o messing up original expenditure
                df2 = df.copy()
                df2.set_index('Bill', inplace=True, drop=True)
                df2.loc[[expenditureName.get()]] #if this doesn't work then it proceeds to except block
                
                #replace existing value
                df.loc[df.index[df['Bill']==expenditureName.get()].tolist(), str(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0))] = expenditureCost.get()
            except:
                #create new dataframe, put new input into new dataframe and concat old and new together

                #new data
                newDfData = {'Bill': [expenditureName.get()],
                        str(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)): [expenditureCost.get()]}
                newDf = pd.DataFrame(newDfData) #new dataframe
                newDf = newDf.set_index('Bill') #set index
                newDf = newDf.astype(np.float64)

                #concat new and old df
                df = pd.concat([df, newDf])
                
            #put dataframe back into db

            #check if replacing prev document
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
############################# 

            messagebox.showinfo("Success", "Successfully Added Expenditure!") #tells user successfully added
  

def selectedOption(screen, offlineMode, username, selected_option, expenditureType):
    if (selected_option == 'V'):
        messagebox.showwarning("Error", "Feature Not Yet Implemented. You can only add fixed bills for now.") #feature not yet implemented as required ai model implementation
    elif (selected_option == ''):
        messagebox.showwarning("Error", "Please Select an Option")
    else:
        global addExpenditure2GUI
        addExpenditure2GUI = Toplevel(screen)
        addExpenditure2GUI.geometry("428x526")
        addExpenditure2GUI.configure(bg="#C0392B")

        if (expenditureType == 'm'):
            addExpenditure2GUI.title("Monthly Bills Tracker")
            #Title
            title = Label(addExpenditure2GUI, text="Monthly Bills Tracker", bg="#C0392B", wraplengt=400)
            title.config(font=('Courier',25))
            title.pack(side=TOP, anchor=NW)
        else:
            addExpenditure2GUI.title("Disposible Income Tracker")
            #Title
            title = Label(addExpenditure2GUI, text="Disposible Income Tracker", bg="#C0392B", wraplengt=400)
            title.config(font=('Courier',25))
            title.pack(side=TOP, anchor=NW)

        #Labels
        Label(addExpenditure2GUI, text="Add Expenditure", bg="#C0392B").pack()

        #expenditure name
        expenditureName = StringVar()
        Label(addExpenditure2GUI, text="Expenditure Name", bg="#C0392B", wraplengt=400).pack()
        Entry(addExpenditure2GUI, textvariable=expenditureName, width = 30, bg='white', fg='black').pack()
        
        #cost of bill
        expenditureCost = StringVar()
        Label(addExpenditure2GUI, text="Cost of Expenditure", bg="#C0392B", wraplengt=400).pack()
        Entry(addExpenditure2GUI, textvariable=expenditureCost, width = 30, bg='white', fg='black').pack()
    
        #addExpenditure Button
        addExpenditureButton = Button(addExpenditure2GUI, text="Add", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                      command=lambda: checkDetails(addExpenditure2GUI, selected_option, expenditureName, expenditureCost, offlineMode, expenditureType, username)).pack()

def addExpenditure(screen, offlineMode, username, expenditureType):
    global addExpenditureGUI
    addExpenditureGUI = Toplevel(screen)
    addExpenditureGUI.configure(bg="#C0392B")

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

        #addExpenditure Button
        addExpenditureButton = Button(addExpenditureGUI, text="Continue", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                      command=lambda: selectedOption(screen, offlineMode, username, selected_option.get(), expenditureType)).pack()
    
    else:
        addExpenditureGUI.title("Disposible Income Tracker")
        addExpenditureGUI.geometry("428x150")
        
        #Title
        title = Label(addExpenditureGUI, text="Disposible Income Tracker", bg="#C0392B", wraplengt=400)
        title.config(font=('Courier',25))
        title.pack(side=TOP, anchor=NW)

        #Labels
        Label(addExpenditureGUI, text="Add Expenditure", bg="#C0392B").pack()

        #addExpenditure Button
        addExpenditureButton = Button(addExpenditureGUI, text="Continue", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                      command=lambda: selectedOption(screen, offlineMode, username, 'F', expenditureType)).pack()

    
    

