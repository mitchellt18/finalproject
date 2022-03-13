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
def plot(selection, screen, monthlyTracker_df, categories, offlineMode):
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
            for x in monthlyTracker_df[selection.get()]:
                sum = monthlyTracker_df[selection.get()][y]
                sum = (sum/monthlyTracker_df[selection.get()].sum())*100
                percentages.append(sum)
                y=y+1

            #plotting graph
            plotGraph.pie(percentages, labels=categories, autopct='%1.0f%%', shadow=True, startangle=70,)
            
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
        moreDetailsButton = Button(plotGUI, text="More Details", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                command=lambda: moreDetails(plotGUI, offlineMode, monthlyTracker_df, selection)).pack()

def monthlyBills(screen, offlineMode, username):
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

    global monthlyGUI
    monthlyGUI = Toplevel(screen)
    monthlyGUI.title("Monthly Bills Tracker")
    monthlyGUI.geometry("350x175")
    monthlyGUI.configure(bg="#C0392B")

    #dictionary for dates
    monthDictionary = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    #array for storing dates from dataset
    dates = []
    pos = len(dates)

    #get data visualisations sorted for offline mode local files
    if (offlineMode):
        monthlyTracker_df = pd.read_excel(
            './expenditures.xlsx',
            sheet_name='monthlyBill',
            index_col=0,
            )

########################################################################################################################################################################################
    else:
        print("Online Mode")
        monthlyTracker_df = False
########################################################################################################################################################################################
    #if dataset is empty, alerts user to add data
    if (monthlyTracker_df.empty):
        monthlyTitle = Label(monthlyGUI, text="Monthly Bills Tracker", bg="#C0392B", wraplengt=400)
        monthlyTitle.config(font=('Courier',25))
        monthlyTitle.pack()
        Label(monthlyGUI, text="Your Dataset Is Empty, Please Add Expenditures", bg='#C0392B').pack()
        
    else:
        #retrieves all dates in dataset
        for fullDate in monthlyTracker_df.columns:
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

        #Title
        monthlyTitle = Label(monthlyGUI, text="Monthly Bills Tracker", bg="#C0392B", wraplengt=400)
        monthlyTitle.config(font=('Courier',25))
        monthlyTitle.pack()

        Label(monthlyGUI, text="Date:", bg='#C0392B').pack()
        if (len(dates) > 0):
            dates.insert(len(dates), "Overview")
        #show dates in dropdown box
        selection = StringVar()
        w = OptionMenu(monthlyGUI, selection, *dates).pack()

        selectButton = Button(monthlyGUI, text='Select Date', width = 15, height = 3, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                command=lambda: plot(selection, monthlyGUI, monthlyTracker_df, categories, offlineMode)).pack(side=LEFT, anchor=W, expand=True)
        
    #addExpenditure Button
    addExpenditureButton = Button(monthlyGUI, text="Add New Expenditure", width = 15, height = 3, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                  command=lambda: addExpenditure(monthlyGUI, offlineMode, username, expenditureType='m')).pack(side=RIGHT, anchor=E, expand=True)