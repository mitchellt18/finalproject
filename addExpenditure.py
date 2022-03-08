#import required modules
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
from pymongo import MongoClient
import re
import datetime
import pandas as pd
from openpyxl import load_workbook

def checkDetails(screen, selected_option, expenditureName, expenditureCost, expenditureDate, offlineMode):
    #check if var is float or not
    def checkFloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def validateDate(date):
        try:
            datetime.datetime.strptime(date, '%m/%d/%y')
            return True
        except ValueError:
            return False

    def validateDateExists(exists, formatDate):
        try:
            print(df[str(formatDate.strftime('01/%m/%Y'))])
            exists = True
            return exists
        except:
            return exists
        

    #check expenditure name
    if (expenditureName.get() == ""):
        messagebox.showwarning("Error", "Please Enter Expenditure Name") #expenditure name missing

    #check expenditure cost
    elif (expenditureCost.get() == ""):
        messagebox.showwarning("Error", "Please Enter Expenditure Cost") #expenditure cost missing
    elif (checkFloat(expenditureCost.get()) == False):
        messagebox.showwarning("Error", "Please Ensure Expenditure Cost is Integer or Float Values Only!") #expenditure cost incorrect

    #check expenditure date
    elif (validateDate(expenditureDate.get()) == False):
         messagebox.showwarning("Error", "Please Ensure Expenditure Date is Filled Out Correctly!") #expenditure date incorrect

    #if correct, input all data
    else:
        if (offlineMode):
            excelFileName = 'expenditures.xlsx'

            
            print("All Variables Correctly Inputted :) Now need to input into xls file")
            formatDate = datetime.datetime.strptime(expenditureDate.get(), '%m/%d/%y') #format date from string to date object
            
            df = pd.read_excel(excelFileName) #read dataset into dataframe
            print(df)
            print("***********************************************************************************************************")

            #try accessing selected date in dataframe
            
            dateExists = validateDateExists(False, formatDate)

            #if date doesn't exist, will add new date, else will add to existing column
            if (dateExists == False):
                df[str(formatDate.strftime('01/%m/%Y'))] = None #add new date with new expenditure cost to dataframe
                print(df)
                df.to_excel(excelFileName, sheet_name = 'monthlyBill', index=False, header=False)

            #else:
                #print (True)
                #tempDf = pd.DataFrame(columns = df.columns)
                #tempDf[str(formatDate.strftime('01/%m/%Y'))] = [str(expenditureCost.get())]
                #df = pd.concat([df, tempDf], ignore_index = True)
                
            
            newData = pd.DataFrame({'Bill': [str(expenditureName.get())], str(formatDate.strftime('01/%m/%Y')): [str(expenditureCost.get())]}) #create dataframe for inputted data
            workbook = load_workbook(excelFileName)
            with pd.ExcelWriter(excelFileName, if_sheet_exists='overlay', engine='openpyxl', mode='a') as writer:
                newData.to_excel(writer,
                            sheet_name = 'monthlyBill',
                            startrow=workbook['monthlyBill'].max_row,
                            header=False,
                            index=False)
                
                print("ADDED")
        else:
            print("online mode not implemented yet")

        #message added to dataset
    

def selectedOption(screen, offlineMode, username, selected_option):
    
    if (selected_option.get() == 'V'):
        messagebox.showwarning("Error", "Feature Not Yet Implemented. You can only add fixed bills for now.") #feature not yet implemented
    elif (selected_option.get() == ''):
        messagebox.showwarning("Error", "Please Select an Option")
    else:
        global addExpenditure2GUI
        addExpenditure2GUI = Toplevel(screen)
        addExpenditure2GUI.title("Monthly Bills Tracker")
        addExpenditure2GUI.geometry("428x526")
        addExpenditure2GUI.configure(bg="#C0392B")


        #Title
        title = Label(addExpenditure2GUI, text="Monthly Bills Tracker", bg="#C0392B", wraplengt=400)
        title.config(font=('Courier',25))
        title.pack(side=TOP, anchor=NW)

        #Labels
        Label(addExpenditure2GUI, text="Add Expenditure", bg="#C0392B").pack()


    #if (selected_option.get() == 'V'):
        
    #else:
        #expenditure name
        expenditureName = StringVar()
        Label(addExpenditure2GUI, text="Expenditure Name", bg="#C0392B", wraplengt=400).pack()
        Entry(addExpenditure2GUI, textvariable=expenditureName, width = 30, bg='white', fg='black').pack()
        
        #cost of bill
        expenditureCost = StringVar()
        Label(addExpenditure2GUI, text="Cost of Expenditure", bg="#C0392B", wraplengt=400).pack()
        Entry(addExpenditure2GUI, textvariable=expenditureCost, width = 30, bg='white', fg='black').pack()
        
        #when was bill
        expenditureDate = StringVar()
        Label(addExpenditure2GUI, text="Expenditure Date", bg="#C0392B", wraplengt=400).pack()
        #Entry(addExpenditure2GUI, textvariable=expenditureDate, width = 30, bg='white', fg='black').pack()
        date=DateEntry(addExpenditure2GUI, selectmode='day', textvariable=expenditureDate).pack()
    
        #addExpenditure Button
        addExpenditureButton = Button(addExpenditure2GUI, text="Add", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                      command=lambda: checkDetails(addExpenditure2GUI, selected_option, expenditureName, expenditureCost, expenditureDate, offlineMode)).pack()

def addExpenditure(screen, offlineMode, username):

    #once added to excel offline and online, dismiss this screen

    global addExpenditureGUI
    addExpenditureGUI = Toplevel(screen)
    addExpenditureGUI.title("Monthly Bills Tracker")
    addExpenditureGUI.geometry("428x526")
    addExpenditureGUI.configure(bg="#C0392B")


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
        option = Radiobutton(addExpenditureGUI, text=o[0], value = o[1], variable = selected_option)
        option.pack()

    #addExpenditure Button
    addExpenditureButton = Button(addExpenditureGUI, text="Continue", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white",
                                  command=lambda: selectedOption(screen, offlineMode, username, selected_option)).pack()

    
    

