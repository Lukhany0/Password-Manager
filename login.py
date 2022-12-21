from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as sql
from mysql.connector import Error

from createAccount import CreateAccount
from appscreen import MainScreen
class LoginScreen:

    def __init__(self, root):

        #First Screen: login screen
        self.root = root
        root.geometry("600x500")
        root.title("Login")
        root.resizable(width=False, height=False)
        mainFrame = Frame(root, width = 600, height = 500, bg = "#27dde3")
        mainFrame.pack()
        self.heading = Label(mainFrame, text="Login", font = ("Times New Roman", 35), bg = "#27dde3")
        self.heading.place(x = 200, y = 150)
        
        #logins label
        self.username_label = Label(root, text="username: ", font = ("Times New Roman", 16), bg = "#27dde3")
        self.username_label.place(x= 100, y= 280)
        self.password_label = Label(root, text="password: ", font = ("Times New Roman", 16), bg = "#27dde3")
        self.password_label.place(x = 100, y= 330)
        #logins entry
        self.username_entry = Entry(root, font = ("Times New Roman", 16))
        self.username_entry.place(x = 200, y= 280)
        self.password_entry = Entry(root, font = ("Times New Roman", 16), show = "*")
        self.password_entry.place(x= 200,y= 330)

        self.submit_button = Button(root, text="login", font = ("Times New Roman", 16), width = 21, command = self.login)
        self.submit_button.place(x=200, y=380)
        self.signup_button = Button(root, text="create accout", font = ("Times New Roman", 16), command = self.callCreate)
        self.signup_button.place(x= 334, y=430)

        self.resetLogin_button= Button(root, text="forgot logins", font = ("Times New Roman", 16))
        self.resetLogin_button.place(x=200, y=430)

    def callCreate(self):
        rt = Tk()
        cs = CreateAccount(rt)
        self.close()
    def callApp(self, usern):
        rt = Tk()
        c = MainScreen(rt, usern)
        self.close()
    def close(self):
        self.root.destroy()
    def login(self):
        if(self.username_entry.get() == "" or self.password_entry.get() == ""):
            messagebox.showerror("login", "enter your logins")
    
        else:
            mydb = None
            try:
                mydb = sql.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "passwords_manager")

                print("database connection successful")
                cursor = mydb.cursor()

                #query: retrive logins in database
                cursor.execute("SELECT username, password FROM users WHERE username = %s and password = %s",(self.username_entry.get(), self.password_entry.get()))
                results = cursor.fetchone() #logins
                print(results)
                if(results == None):
                    messagebox.showerror("login error", "logins not found")
                else:
                    print("log in successful")
                    #save primary key
                    login_username = self.username_entry.get()
                    #call appscreen(root, login_username)
                    self.callApp(login_username)

            except Error as err:
                print(f"Error: {err}")
root = Tk()   
ls = LoginScreen(root)
root.mainloop()
