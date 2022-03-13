#import required modules
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
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
def plot(selection, screen, disposibleTracker_df, categories, offlineMode):
    if (selection.get() == ""):
        messagebox.showwarning("Error", "Please Select a Month") #expenditure name missing
    else:
        global plotGUI
        plotGUI = Toplevel(screen)
        plotGUI.title(selection.get() + " Plot")
        plotGUI.geometry("428x526")
        plotGUI.configure(bg="#C0392B")

        disposibleTracker_df = disposibleTracker_df.fillna(0) #replace nan with 0

        #figure containing plot
        fig = Figure(figsize=(7,7))

        #adding to subplot
        plotGraph = fig.add_subplot(111)

        if (selection.get() == "Overview"):
            #plotting graph
            plotGraph.plot(disposibleTracker_df.sum())
            
        else:
            #loop for accessing all finances and converting into percentages
            y=0
            percentages = []
            for x in disposibleTracker_df[selection.get()]:
                sum = disposibleTracker_df[selection.get()][y]
                sum = (sum/disposibleTracker_df[selection.get()].sum())*100
                percentages.append(sum)
                y=y+1

        
            #plotting graph
            plotGraph.pie(percentages, labels=categories, autopct='%1.0f%%', shadow=True, startangle=70,)
        
        #creating tkinter canvas to display within gui
        canvas = FigureCanvasTkAgg(fig, master = plotGUI)
        canvas.draw()
        canvas.get_tk_widget().pack()

        
        if (selection.get() == "Overview"):
            totalMonthly = disposibleTracker_df.sum()
            average = totalMonthly.sum()/len(totalMonthly)
            
            Label(plotGUI, text="On Average, your total spendings per month is: £" + str(average), bg="#C0392B").pack()
        else:
            total = disposibleTracker_df[selection.get()].sum()
            Label(plotGUI, text="In " + selection.get() + " your total spendings was: £" + str(total), bg="#C0392B").pack()

        #more details button
        moreDetailsButton = Button(plotGUI, text="More Details", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                command=lambda: moreDetails(plotGUI, offlineMode, disposibleTracker_df, selection)).pack()

def disposibleIncome(screen, offlineMode, username):
    #if user is in offline mode, open/create local dataset
    if (offlineMode):
        exists = os.path.isfile('expenditures.xlsx') #checks if required dataset exists
        
        #if dataset doesn't exist, it creates one
        if (not exists):
            df = pd.DataFrame({'Bill': [], date.today().strftime('01/%m/%Y'): []}) #sets titles in xlsx file
            writer = pd.ExcelWriter('expenditures.xlsx', engine='xlsxwriter') #creates expenditures dataset
            df.to_excel(writer, sheet_name='monthlyBill', index=False) #sheet for monthly bills
            df.to_excel(writer, sheet_name='disposibleIncome', index=False) #sheet for disposible income
            writer.save()

########################################################################################################################################################################################
            #ONLINE MODE IN HASHES
    #if user is not in offline mode, retrieve dataset from online db
    else:
        print("not offline")
        #establish connection with the database to retrieve xls file and store it locally, every adjustment to xls, update db
########################################################################################################################################################################################

    global disposibleGUI
    disposibleGUI = Toplevel(screen)
    disposibleGUI.title("Disposible Income Tracker")
    disposibleGUI.geometry("420x175")
    disposibleGUI.configure(bg="#C0392B")

    #dictionary for dates
    monthDictionary = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    #array for storing dates from dataset
    dates = []
    pos = len(dates)

    #get data visualisations sorted for offline mode local files
    if (offlineMode):
        disposibleTracker_df = pd.read_excel(
            './expenditures.xlsx',
            sheet_name='disposibleIncome',
            index_col=0,
            )

########################################################################################################################################################################################
    else:
        print("Online Mode")
        disposibleTracker_df = False
########################################################################################################################################################################################
    #if dataset is empty, alerts user to add data
    if (disposibleTracker_df.empty):
        disposibleTitle = Label(disposibleGUI, text="Disposible Income Tracker", bg="#C0392B", wraplengt=400)
        disposibleTitle.config(font=('Courier',25))
        disposibleTitle.pack()
        Label(disposibleGUI, text="Your Dataset Is Empty, Please Add Expenditures", bg='#C0392B').pack()
        
    else:
        #retrieves all data in dataset
        for fullDate in disposibleTracker_df.columns:
            month = monthDictionary[str(fullDate.month)] #gets month
            year = str(fullDate.year) #gets year
            dateAdjusted = month + " " + year
            dates.insert(pos, dateAdjusted)
            pos = pos + 1

        #rename columns to relevant names
        disposibleTracker_df.columns= dates

        #loop for accessing indexes and inputting into array for future uses
        categories=[]
        y=0
        for x in disposibleTracker_df.index:
            categories.append(disposibleTracker_df.index[y])
            y = y+1

        #gui

        #Title
        disposibleTitle = Label(disposibleGUI, text="Disposible Income Tracker", bg="#C0392B", wraplengt=400)
        disposibleTitle.config(font=('Courier',25))
        disposibleTitle.pack()

        Label(disposibleGUI, text="Date:", bg='#C0392B').pack()
        if (len(dates) > 0):
            dates.insert(len(dates), "Overview")
        #show dates in dropdown box
        selection = StringVar()
        w = OptionMenu(disposibleGUI, selection, *dates).pack()

        selectButton = Button(disposibleGUI, text='Select Date', width = 15, height = 3, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                command=lambda: plot(selection, disposibleGUI, disposibleTracker_df, categories, offlineMode)).pack(side=LEFT, anchor=W, expand=True)
        
    #addExpenditure Button
    addExpenditureButton = Button(disposibleGUI, text="Add New Expenditure", width = 15, height = 3, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                  command=lambda: addExpenditure(disposibleGUI, offlineMode, username, expenditureType='d')).pack(side=RIGHT, anchor=E, expand=True)
