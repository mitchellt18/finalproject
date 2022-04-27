#import required modules
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
from PIL import ImageTk, Image
import re
import os
from datetime import date, datetime
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#import py files
from Expenditures.addExpenditure import *
from Expenditures.moreDetails import *

#gui
def mainExpenditurePage(screen, offlineMode, username, expenditureType):
    from PIL import ImageTk, Image #required for images
    #gui
    global expenditureGUI
    expenditureGUI = Toplevel(screen)
    expenditureGUI.geometry("550x175")
    expenditureGUI.configure(bg="#C0392B")

    #Display correct expenditure type and correct dataset based on previous user input
    if (expenditureType == 'D'):
        sheetName = 'disposibleIncome'
        expenditureTypeAdd = 'd'
        expenditureGUI.title("Disposable Income Tracker")
        expenditureTitle = Label(expenditureGUI, text="Disposable Income Tracker", bg="#C0392B", wraplengt=400)
        
    else:
        sheetName = 'monthlyBill'
        expenditureTypeAdd = 'm'
        expenditureGUI.title("Monthly Bills Tracker")
        expenditureTitle = Label(expenditureGUI, text="Monthly Bills Tracker", bg="#C0392B", wraplengt=400)

    expenditureTitle.config(font=('Courier',25))
    expenditureTitle.pack()

    #dictionary for dates
    monthDictionary = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}

    #array for storing dates from dataset
    dates = []
    pos = len(dates)

    #variable to check if dataset is empty
    empty = False

    #check if dataset exists
    
    #offline mode
    if (offlineMode):
        #checks if local dataset exists
        exists = os.path.isfile('./Expenditures/expenditures.xlsx')
        
        #if no dataset - creates one
        if (not exists):
            #title of xlsx file
            df = pd.DataFrame({'Bill': [], date.today().strftime('01/%m/%Y'): []})
            #creates xlsx file
            writer = pd.ExcelWriter('./Expenditures/expenditures.xlsx', engine='xlsxwriter')
            #sheet for monthlyBills
            df.to_excel(writer, sheet_name='monthlyBill', index=False)
            #sheet for disposable income
            df.to_excel(writer, sheet_name='disposibleIncome', index=False)
            writer.save()

        #put dataset into dataframe for data visualisations
        expenditureTracker_df = pd.read_excel(
            './Expenditures/expenditures.xlsx',
            sheet_name=sheetName,
            index_col=0,
            )

        #if dataframe is empty, displays empty message later on
        if (expenditureTracker_df.empty):
            empty=True

    #online mode
    else:
        #db code
        global client
        global db
        global records
        client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database('user_db')
        records = db.user_details
        #retrieves user from db
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)}) #user

        #if expenditure type is disposable income, retrieves correct collection and object ids
        if (expenditureType == 'D'):
            expenditureRecords = db.disposible_bills
            objectID = userObject['objectIDDisposible']

        #if expenditure type is monthly bills, retrieves correct collection and object ids
        else:
            expenditureRecords = db.monthly_bills
            objectID = userObject['objectIDMonthly'] #retrieve correct object id


        #checks if dataset exists in db
        if (objectID != "" and expenditureRecords.find_one({'_id': objectID[0]})):
            
            #import dataset into dataframe
            expenditureBillsObject = expenditureRecords.find_one({'_id': objectID[0]},{'_id':0}) #import df data
            #put data into df 
            expenditureTracker_df = pd.DataFrame([expenditureBillsObject])
            #remove data from array as been retrieved
            objectID.pop(0)

            #if remaining objectIDs exist
            if (len(objectID) > 0):
                #for loop over objectID array
                for n in objectID:
                    #import df date
                    expenditureBillsObject = expenditureRecords.find_one({'_id': n},{'_id':0})
                    #put data into df
                    newexpenditureTracker_df = pd.DataFrame([expenditureBillsObject])
                    #concat both dfs
                    expenditureTracker_df = pd.concat([expenditureTracker_df, newexpenditureTracker_df])
                    
            
            expenditureTracker_df = expenditureTracker_df.set_index('Bill') #set index
            expenditureTracker_df = expenditureTracker_df.astype(np.float64) #set dtype

        #if dataframe is empty, displays empty message later on
        else:
            empty = True #empty dataset for user

    #if dataframe empty, display empty message
    if (empty):
        Label(expenditureGUI, text="Your Dataset Is Empty, Please Add Expenditures", bg='#C0392B').pack()

    #else dataframe is not empty, so retrieve data
    else:
        #retrieves all data in dataset using for loop
        for fullDate in expenditureTracker_df.columns:
            
            #if string needs to convert to datetime object
            if (isinstance(fullDate, str)):
                #convert to datetime
                fullDate = datetime.strptime(fullDate, '%Y-%m-%d %H:%M:%S') #input yyyy-mm-dd hh:mm:ss
                
            month = monthDictionary[str(fullDate.month)] #gets word month
            year = str(fullDate.year) #gets year
            dateAdjusted = month + " " + year #adds both together (eg March + 2022 = March 2022)
            dates.insert(pos, dateAdjusted) #insert date into array
            pos = pos + 1 #increase position by 1
            
        #rename columns to relevant names
        expenditureTracker_df.columns = dates

        #loop for accessing indexes and inputting into array for future uses
        categories=[]
        y=0
        for x in expenditureTracker_df.index:
            categories.append(expenditureTracker_df.index[y])
            y = y+1

        #gui
        Label(expenditureGUI, text="Date:", bg='#C0392B').pack()
        #Inserts Overview if multiple dates
        if (len(dates) > 0):
            dates.insert(len(dates), "Overview")
        #show dates in dropdown box
        selection = StringVar()
        w = OptionMenu(expenditureGUI, selection, *dates)
        w.config(bg='#C0392B')
        w["menu"].config(bg='#C0392B')
        w.pack()

        #select button
        selectImg = Image.open("./Buttons/Expenditures/button_select-date.png")
        outputSelect = ImageTk.PhotoImage(selectImg)
        
        selectButton = Button(expenditureGUI, image = outputSelect,
                               command=lambda: plot(selection, expenditureGUI, expenditureTracker_df, categories, offlineMode))

        selectButton.image = outputSelect
        selectButton.pack(side=LEFT, anchor=W, expand=True)


    #add expenditure button
    addImg = Image.open("./Buttons/Expenditures/button_add-new-expenditure.png")
    outputAdd = ImageTk.PhotoImage(addImg)
    
    addExpenditureButton = Button(expenditureGUI, image = outputAdd,
                           command=lambda: addExpenditure(expenditureGUI, offlineMode, username, expenditureType=expenditureTypeAdd))

    addExpenditureButton.image = outputAdd
    addExpenditureButton.pack(side=RIGHT, anchor=E, expand=True)
