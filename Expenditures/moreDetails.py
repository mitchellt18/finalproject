#import required modules
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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

#show more details of finances
def moreDetails(screen, offlineMode, df, date):

    #gui settings
    global moreDetailsGUI
    moreDetailsGUI = Toplevel(screen)
    moreDetailsGUI.title("More Details: " + date.get())
    moreDetailsGUI.configure(bg="#C0392B")

    #Title
    moreDetailsTitle = Label(moreDetailsGUI, text="More Details for " + date.get(), bg="#C0392B", wraplengt=400)
    moreDetailsTitle.config(font=('Courier',25))
    moreDetailsTitle.pack()
    df = df.reset_index(drop=False)

    #if overview of all months - wider screen and shows all dataframe
    if (date.get() == "Overview"):        
        moreDetailsGUI.geometry("1400x526")

        #create treeview frame
        outputFrame = ttk.Treeview (moreDetailsGUI, columns = list(df), show='headings')

        #insert column headers of dataframe into tree
        for col in list(df):
            outputFrame.heading(col, text=col)
        outputFrame.pack()
        
        #insert contents of dataframe into tree
        for val in df.values.tolist():
            outputFrame.insert("", "end", values=val)

    #if not overview, outputs correct month from df  
    else:
        moreDetailsGUI.geometry("428x526")

        #create treeview frame
        outputFrame = ttk.Treeview (moreDetailsGUI, columns = list(df[['Bill',date.get()]]), show='headings')

        #insert column headers of dataframe into tree
        for col in list(df[['Bill',date.get()]]):
            outputFrame.heading(col, text=col)
        outputFrame.pack()
        
        #insert contents of dataframe into tree
        for val in df[['Bill',date.get()]].values.tolist():
            outputFrame.insert("", "end", values=val)

            
#plot graph
def plot(selection, screen, df, categories, offlineMode):
    from PIL import ImageTk, Image #required for images

    #if month not selected - error
    if (selection.get() == ""):
        messagebox.showwarning("Error", "Please Select a Month")
    else:

        #gui settings
        global plotGUI
        plotGUI = Toplevel(screen)
        plotGUI.title(selection.get() + " Plot")
        plotGUI.geometry("428x526")
        plotGUI.configure(bg="#C0392B")

        df = df.fillna(0) #replace nan with 0

        #figure containing plot
        fig = Figure(figsize=(7,7))

        #adding to subplot
        plotGraph = fig.add_subplot(111)

        #if overview selected - line graph of total finances
        if (selection.get() == "Overview"):
            plotGraph.plot(df.sum())

        #else if month selected - pie chart shown
        else:
            #loop for accessing all finances and converting into percentages
            y=0
            percentages = []
            labelCategories = []
            for x in df[selection.get()]:
                sum = df[selection.get()][y]
                sum = (sum/df[selection.get()].sum())*100
                if (sum != 0):
                    #if the expenditure has a value it will be put into the visualisation
                    percentages.append(sum)
                    labelCategories.append(df[selection.get()].index[y])
                y=y+1

            #plotting graph
            plotGraph.pie(percentages, labels=labelCategories, autopct='%1.0f%%', shadow=True, startangle=70,)
        
        #creating tkinter canvas to display within gui
        canvas = FigureCanvasTkAgg(fig, master = plotGUI)
        canvas.draw()
        canvas.get_tk_widget().pack()

        #if overview option, shows average spending per month
        if (selection.get() == "Overview"):
            totalMonthly = df.sum()
            average = totalMonthly.sum()/len(totalMonthly)
            
            Label(plotGUI, text="On average, your total spendings per month is: £" + str(average), bg="#C0392B").pack()

        #else shows total spending for selected month
        else:
            total = df[selection.get()].sum()
            Label(plotGUI, text="In " + selection.get() + " your total spendings was: £" + str(total), bg="#C0392B").pack()

        #more details button
        moreDetailsImg = Image.open("./Buttons/Expenditures/button_more-details.png")
        outputMoreDetails = ImageTk.PhotoImage(moreDetailsImg)
        
        moreDetailsButton = Button(plotGUI, image = outputMoreDetails,
                               command=lambda: moreDetails(plotGUI, offlineMode, df, selection))

        moreDetailsButton.image = outputMoreDetails
        moreDetailsButton.pack()
