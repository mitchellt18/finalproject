#import required modules
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
import os
import pandas as pd
import numpy as np
import re

def advice(screen, offlineMode, username):
    #gui settings
    global adviceGUI
    adviceGUI = Toplevel(screen)
    adviceGUI.title("Financial Recommendations")
    adviceGUI.geometry("428x630")
    adviceGUI.configure(bg="#C0392B")

    #Title
    adviceTitle = Label(adviceGUI, text="Financial Recommendations", bg="#C0392B", wraplengt=400)
    adviceTitle.config(font=('Courier',25))
    adviceTitle.pack(side=TOP, anchor=NW)

    Label(adviceGUI, text="Here you will see some financial recommendations based on the following:", bg="#C0392B", wraplengt=400).pack()
    Label(adviceGUI, text="-Your average monthly bills spending", bg="#C0392B", wraplengt=400).pack()
    Label(adviceGUI, text="-Your average disposable spending", bg="#C0392B", wraplengt=400).pack()
    Label(adviceGUI, text="-Your average total spending", bg="#C0392B", wraplengt=400).pack()

    if (not offlineMode):
        Label(adviceGUI, text="-Your salary compared to total spending", bg="#C0392B", wraplengt=400).pack()

    empty = False #check if dfs are empty

    if (offlineMode):
        exists = os.path.isfile('./Expenditures/expenditures.xlsx') #checks if dataset exists

        if (not exists):
            empty = True #if it doesn't, empty df
        else:
            #import monthly and disposable into df
            monthlyTracker_df = pd.read_excel(
            './Expenditures/expenditures.xlsx',
            sheet_name='monthlyBill',
            index_col=0,
            )

            disposableTracker_df = pd.read_excel(
            './Expenditures/expenditures.xlsx',
            sheet_name='disposibleIncome',
            index_col=0,
            )

            #checks if either one is empty
            if (monthlyTracker_df.empty or disposableTracker_df.empty):
                empty=True

    else:
        #db code
        global client
        global db
        global records
        client = MongoClient("mongodb+srv://mitchellt22:aVJ3L0ilDrgKswZs@cluster0.n9xwq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database('user_db')
        records = db.user_details
        #retrieves user from db
        userObject = records.find_one({'username': re.compile('^' + re.escape(username.get()) + '$', re.IGNORECASE)})
        monthlyRecords = db.monthly_bills
        disposableRecords = db.disposible_bills

        #objectIDs from both
        objectID_Monthly = userObject['objectIDMonthly']
        objectID_Disposable = userObject['objectIDDisposible']

        if (objectID_Monthly != "" and objectID_Disposable != "" and monthlyRecords.find_one({'_id': objectID_Monthly[0]}) and disposableRecords.find_one({'_id': objectID_Disposable[0]})):

            #import dataset into df
            monthlyBillsObject = monthlyRecords.find_one({'_id': objectID_Monthly[0]},{'_id':0}) #monthly
            disposableBillsObject = disposableRecords.find_one({'_id': objectID_Disposable[0]},{'_id':0}) #disposable

            #put data into df
            monthlyTracker_df = pd.DataFrame([monthlyBillsObject])
            disposableTracker_df =pd.DataFrame([disposableBillsObject])

            #remove data from array as been retrieved
            objectID_Monthly.pop(0)
            objectID_Disposable.pop(0)

            #if remaining objectIDs exist
            #monthly
            if (len(objectID_Monthly) > 0):
                #for loop over objectID array
                for n in objectID_Monthly:
                    #import df date
                    monthlyBillsObject = monthlyRecords.find_one({'_id': n},{'_id':0})
                    #put data into df
                    newmonthlyTracker_df = pd.DataFrame([monthlyBillsObject])
                    #concat both dfs
                    monthlyTracker_df = pd.concat([monthlyTracker_df, newmonthlyTracker_df])

            monthlyTracker_df = monthlyTracker_df.set_index('Bill') #set index
            monthlyTracker_df = monthlyTracker_df.astype(np.float64) #set dtype

            #disposable
            if (len(objectID_Disposable) > 0):
                #for loop over objectID array
                for n in objectID_Disposable:
                    #import df date
                    disposableBillsObject = disposableRecords.find_one({'_id': n},{'_id':0})
                    #put data into df
                    newdisposableTracker_df = pd.DataFrame([disposableBillsObject])
                    #concat both dfs
                    disposableTracker_df = pd.concat([disposableTracker_df, newdisposableTracker_df])
                    
            disposableTracker_df = disposableTracker_df.set_index('Bill') #set index
            disposableTracker_df = disposableTracker_df.astype(np.float64) #set dtype

        #df is empty
        else:
            empty = True

    if (empty):
        #Title
        adviceTitle = Label(adviceGUI, text="PLEASE NOTE", bg="#C0392B", wraplengt=400)
        adviceTitle.config(font=('Courier',25))
        adviceTitle.pack()
        Label(adviceGUI, text="YOU DO NOT HAVE BOTH MONTHLY BILLS AND DISPOSABLE INCOME SECTIONS FILLED OUT, THEREFORE ADVICE IS UNAVAILABLE", bg="#C0392B", wraplengt=400).pack()

    else:
        #Title
        adviceTitle = Label(adviceGUI, text="Here Are Your Financial Recommendations:", bg="#C0392B", wraplengt=400)
        adviceTitle.config(font=('Courier',25))
        adviceTitle.pack()

        #average for monthly bills
        totalMonthly = monthlyTracker_df.sum()
        monthlyAverage = totalMonthly.sum()/len(totalMonthly)
        Label(adviceGUI, text="Your average for monthly bills spending per month is: £" + str(monthlyAverage), bg="#C0392B", wraplengt=400).pack()
        
        #average for monthly disposable spending
        totalDisposable = disposableTracker_df.sum()
        disposableAverage = totalDisposable.sum()/len(totalDisposable)
        Label(adviceGUI, text="Your average for disposable spending per month is: £" + str(disposableAverage), bg="#C0392B", wraplengt=400).pack()

        #average for total monthly costs
        totalAverage = monthlyAverage + disposableAverage
        totalAverage = round(totalAverage, 2)
        Label(adviceGUI, text="Your average total monthly spending: £" + str(totalAverage), bg="#C0392B", wraplengt=400).pack()

        #check if percentage of monthly disposable is 30% or more of total costs
        disposablePercentage = (disposableAverage / totalAverage) * 100
        Label(adviceGUI, text="Your disposable costs are " + str(round(disposablePercentage, 2)) + "% of total spending", bg="#C0392B", wraplengt=400).pack()

        if (disposablePercentage > 29.9):
            Label(adviceGUI, text="Since your average disposable spending is a high portion of your spending, consider reducing spending on non-essential items or activities.", bg="#C0392B", wraplengt=400).pack()

        #check if percentage of monthly bills is 85% or more of total costs
        monthlyPercentage = (monthlyAverage / totalAverage) * 100
        Label(adviceGUI, text="Your monthly bills costs are " + str(round(monthlyPercentage, 2)) + "% of total spending", bg="#C0392B", wraplengt=400).pack()

        if (monthlyPercentage > 84.9):
            Label(adviceGUI, text="Since your average monthly spending is a high portion of your spending, consider reducing bills by shopping around eg insurance, gas/electricity.", bg="#C0392B", wraplengt=400).pack()

        #if offline mode, that is it for the advice section
        if (offlineMode):
            Label(adviceGUI, text="Since you are using Offline Mode, that is it for the advice! If you utilise an online account with built in salary checker, you will be able to compare these costs against your salary!", bg="#C0392B", wraplengt=400).pack()
        else:
            #online mode can use salary
            salary = userObject['salary']
            monthlySalary = float(salary) / 12

            #shows users salary
            Label(adviceGUI, text="Your salary is: £" + str(salary) + " which means on average per month you earn: £" + str(round(monthlySalary, 2)), bg="#C0392B", wraplengt=400).pack()

            #shows users average remaining money per month
            Label(adviceGUI, text="Based on this information, you have on average £" + str(round((monthlySalary - totalAverage), 2)) + " money left over per month.", bg="#C0392B", wraplengt=400).pack()

            #if average spending is higher than average monthly salary
            if (totalAverage > monthlySalary):
                Label(adviceGUI, text="As you can see, you are spending more per month then you are earning. It is vital you look at methods to reduce monthly costs, potentially using the methods presented.", bg="#C0392B", wraplengt=400).pack()

            #if average spending is lower than average monthly spending
            else:
                percentageIncomeLeftOver = (totalAverage/monthlySalary) * 100 #percentage of income remaining out of average monthly income

                #if small amount left over per month (less than 10%)
                if (percentageIncomeLeftOver < 10):
                    Label(adviceGUI, text="Even though you are not spending more than you are receiving, you only have " + str(round(percentageIncomeLeftOver, 2)) + "% of your income remaining per month. If you would like to save money, it would be a good idea to look at reducing costs and putting the remaining money into a savings account or an emergency money account.", bg="#C0392B", wraplengt=400).pack()

                #if larger amount left over per month (10% or more)
                else:
                    Label(adviceGUI, text="You have a significant portion of " + str(round(percentageIncomeLeftOver, 2)) + "% of your income remaining per month. It is a good idea, if you are not already, to look into potentially saving this money, by means of investing into a savings account, an emergency savings account, or by other means. Or even (very risky) method of investing a small amount into stocks/cryptocurrencies.", bg="#C0392B", wraplengt=400).pack()
  
        #disclaimer
        Label(adviceGUI, text="DISCLAIMER: Any advice on here should NOT be fully relied on, it is fairly generic. It's purpose is to give you an idea on where your spending habits weigh heavily on and how much free cash you have/overspending you engage in, and any financial decision taken is solely your decision and responsibility.", bg="#C0392B", wraplengt=400).pack()

    
    
