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

def moreDetails(screen, offlineMode, df, date):

    global moreDetailsGUI
    moreDetailsGUI = Toplevel(screen)
    moreDetailsGUI.title("More Details: " + date.get())
    moreDetailsGUI.configure(bg="#C0392B")

    #Title
    moreDetailsTitle = Label(moreDetailsGUI, text="More Details for " + date.get(), bg="#C0392B", wraplengt=400)
    moreDetailsTitle.config(font=('Courier',25))
    moreDetailsTitle.pack()
    df = df.reset_index(drop=False)

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
