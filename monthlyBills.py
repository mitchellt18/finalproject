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
from addExpenditure import *
from moreDetails import *

#plot graph
def plot(selection, screen, monthlyTracker_df, categories, offlineMode):
    from PIL import ImageTk, Image #required for opening images
    if (selection.get() == ""):
        messagebox.showwarning("Error", "Please Select a Month") #expenditure name missing
    else:
        global plotGUI
        plotGUI = Toplevel(screen)
        plotGUI.title(selection.get() + " Plot")
        plotGUI.geometry("428x526")
        plotGUI.configure(bg="#C0392B")
        
        monthlyTracker_df = monthlyTracker_df.fillna(0) #replace nan with 0
        
        #figure containing plot
        fig = Figure(figsize=(7,7))

        #adding to subplot
        plotGraph = fig.add_subplot(111)

        if (selection.get() == "Overview"):
            #plotting graph
            plotGraph.plot(monthlyTracker_df.sum())
            
        else:
            
            #loop for accessing all finances and converting into percentages
            y=0
            percentages = []
            labelCategories = []
            for x in monthlyTracker_df[selection.get()]:
                sum = monthlyTracker_df[selection.get()][y]
                sum = (sum/monthlyTracker_df[selection.get()].sum())*100
                if (sum != 0):
                    #if the expenditure has a value it will be put into the visualisation
                    percentages.append(sum)
                    labelCategories.append(monthlyTracker_df[selection.get()].index[y])
                y=y+1

            #plotting graph
            plotGraph.pie(percentages, labels=labelCategories, autopct='%1.0f%%', shadow=True, startangle=70,)
            
        #creating tkinter canvas to display within gui
        canvas = FigureCanvasTkAgg(fig, master = plotGUI)
        canvas.draw()
        canvas.get_tk_widget().pack()

        if (selection.get() == "Overview"):
            totalMonthly = monthlyTracker_df.sum()
            average = totalMonthly.sum()/len(totalMonthly)
            
            Label(plotGUI, text="On Average, your total spendings per month is: £" + str(average), bg="#C0392B").pack()
        else:
            total = monthlyTracker_df[selection.get()].sum()
            Label(plotGUI, text="In " + selection.get() + " your total spendings was: £" + str(total), bg="#C0392B").pack()
        
        #more details button
        moreDetailsImg = Image.open("./Buttons/Expenditures/button_more-details.png")
        outputMoreDetails = ImageTk.PhotoImage(moreDetailsImg)
        
        moreDetailsButton = Button(plotGUI, image = outputMoreDetails,
                               command=lambda: moreDetails(plotGUI, offlineMode, monthlyTracker_df, selection))

        moreDetailsButton.image = outputMoreDetails
        moreDetailsButton.pack()

def monthlyBills(screen, offlineMode, username):
    from PIL import ImageTk, Image #required for opening images
    #set up gui
    global monthlyGUI
    monthlyGUI = Toplevel(screen)
    monthlyGUI.title("Monthly Bills Tracker")
    monthlyGUI.geometry("550x175")
    monthlyGUI.configure(bg="#C0392B")

    #Title
    monthlyTitle = Label(monthlyGUI, text="Monthly Bills Tracker", bg="#C0392B", wraplengt=400)
    monthlyTitle.config(font=('Courier',25))
    monthlyTitle.pack()

    #dictionary for dates
    monthDictionary = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    #array for storing dates from dataset
    dates = []
    pos = len(dates)
    empty=False #checks if dataset is empty

    #firstly check if correct dataset exists, in online or offline mode
    #if user is in offline mode, open/create local dataset
    if (offlineMode):
        exists = os.path.isfile('expenditures.xlsx') #checks if required dataset exists
        
        #if dataset doesn't exist, it creates one
        if (not exists):
            df = pd.DataFrame({'Bill': [], date.today().strftime('01/%m/%Y'): []}) #sets titles in xlsx file
            writer = pd.ExcelWriter('expenditures.xlsx', engine='xlsxwriter') #creates expenditures dataset
            df.to_excel(writer, sheet_name='monthlyBill', index=False) #sheet for monthly bills
            df.to_excel(writer, sheet_name='disposibleIncome', index=False) #sheet for disposable income
            writer.save()

        #put into dataframe for data visualisations
        monthlyTracker_df = pd.read_excel(
        './expenditures.xlsx',
        sheet_name='monthlyBill',
        index_col=0,
        )
        
        #if dataset is empty, alerts user to add data
        if (monthlyTracker_df.empty):
            empty = True
        
    #if user is in online mode, retrieve dataset from online db
    else:
        #establish connection with db
        global client
        global db
        global records
        client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database('user_db')
        records = db.user_details
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)}) #user
        monthlyBillRecords = db.monthly_bills
        objectID = userObject['objectIDMonthly'] #retrieve correct object id
        
        #checks if dataset exists in db
        if (objectID != "" and monthlyBillRecords.find_one({'_id': objectID[0]})):
            
            #import dataframe from db into new dataframe
            monthlyBillsObject = monthlyBillRecords.find_one({'_id': objectID[0]},{'_id':0}) #import dataframe data from db
            
            monthlyTracker_df = pd.DataFrame([monthlyBillsObject]) #put dataframe data into a new dataframe
            objectID.pop(0)

             #if remaining objectIDs present
            if (len(objectID) > 0):
                for n in objectID:
                    monthlyBillsObject = monthlyBillRecords.find_one({'_id': n},{'_id':0}) #import dataframe data from db
                    newmonthlyTracker_df = pd.DataFrame([monthlyBillsObject]) #put dataframe data into a new dataframe
                    monthlyTracker_df = pd.concat([monthlyTracker_df, newmonthlyTracker_df])
                    
            
            monthlyTracker_df = monthlyTracker_df.set_index('Bill') #set index
            monthlyTracker_df = monthlyTracker_df.astype(np.float64) #set dtype
 
        else:
            empty = True #empty dataset for user
            
    if (empty):
        Label(monthlyGUI, text="Your Dataset Is Empty, Please Add Expenditures", bg='#C0392B').pack()
    else:
        #retrieves all dates in dataset
            for fullDate in monthlyTracker_df.columns:
                #if string need to convert to datetime object
                if (isinstance(fullDate, str)):
                    #convert to datetime
                    fullDate = datetime.strptime(fullDate, '%Y-%m-%d %H:%M:%S') #input yyyy-mm-dd hh:mm:ss
                    
                month = monthDictionary[str(fullDate.month)] #gets month
                year = str(fullDate.year) #gets year
                dateAdjusted = month + " " + year
                dates.insert(pos, dateAdjusted) #adds dates into array for easier viewing for user
                pos = pos + 1

            monthlyTracker_df.columns= dates #rename columns to relevant names

            #loop for accessing indexes and inputting into array for future uses
            categories=[]
            y=0
            for x in monthlyTracker_df.index:
                categories.append(monthlyTracker_df.index[y])
                y = y+1

            #gui
            Label(monthlyGUI, text="Date:", bg='#C0392B').pack()
            if (len(dates) > 0):
                dates.insert(len(dates), "Overview")
            #show dates in dropdown box
            selection = StringVar()
            w = OptionMenu(monthlyGUI, selection, *dates).pack()

            #select button
            selectImg = Image.open("./Buttons/Expenditures/button_select-date.png")
            outputSelect = ImageTk.PhotoImage(selectImg)
            
            selectButton = Button(monthlyGUI, image = outputSelect,
                                   command=lambda: plot(selection, monthlyGUI, monthlyTracker_df, categories, offlineMode))

            selectButton.image = outputSelect
            selectButton.pack(side=LEFT, anchor=W, expand=True)


    #add expenditure button
    addImg = Image.open("./Buttons/Expenditures/button_add-new-expenditure.png")
    outputAdd = ImageTk.PhotoImage(addImg)
    
    addExpenditureButton = Button(monthlyGUI, image = outputAdd,
                           command=lambda: addExpenditure(monthlyGUI, offlineMode, username, expenditureType='m'))

    addExpenditureButton.image = outputAdd
    addExpenditureButton.pack(side=RIGHT, anchor=E, expand=True)
