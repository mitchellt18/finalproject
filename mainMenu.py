from tkinter import *

def mainMenu(screen, offlineMode, username):
    global mainMenuGUI

    screen.withdraw() #close previous window no longer required

    mainMenuGUI = Toplevel(screen)
    mainMenuGUI.title("Main Menu")
    mainMenuGUI.geometry("428x526")
    mainMenuGUI.configure(bg="#C0392B")

    #Main Menu Title
    mainmenuTitle = Label(mainMenuGUI, text="Main Menu", bg="#C0392B", wraplengt=400)
    mainmenuTitle.config(font=('Courier',25))
    mainmenuTitle.pack(side=TOP, anchor=NW)

    #settings button
    settingsButton = Button(mainMenuGUI, text="Settings", bg="#C0392B", highlightbackground="#C0392B", fg = "white")
    settingsButton.pack(side=TOP, anchor=NE)

    #Option Label
    mainmenuLabel = Label(mainMenuGUI, text="Please choose an option below", bg="#C0392B")
    mainmenuLabel.pack()

    #option1 button
    option1Button = Button(mainMenuGUI, text="Monthly Bills Tracker", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white")
    option1Button.pack()

    #option2 button
    option2Button = Button(mainMenuGUI, text="Disposable Income Tracker", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white")
    option2Button.pack()

    #option3 button
    option3Button = Button(mainMenuGUI, text="Financial Recommendations", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white")
    option3Button.pack()

    #option4 button
    option4Button = Button(mainMenuGUI, text="Payment Reminders", width = 20, height = 5, bg="#C0392B", highlightbackground="#C0392B", fg = "white")
    option4Button.pack()

    if offlineMode:
        userLabel = Label(mainMenuGUI, text="Offline Mode", bg="#C0392B").pack()
    else:
        userLabel = Label(mainMenuGUI, text="Currently Logged In: " + username.get(), bg="#C0392B").pack()
