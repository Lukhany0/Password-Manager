from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as sql
from mysql.connector import Error

from insertData import InsertData
class MainScreen:

    def __init__(self, root, login_username):

        self.login_username = login_username
        self.root = root
        root.geometry("1200x700")
        root.title("Passwords Manager")
        root.resizable(width=False, height=False)
    #=================
        self.row = [] #array to store values of selected row in treeview
    #====================================================FRAMES=========================================
        self.mainFrame = Frame(root, width = 1200, height = 700, bg = "#27dde3", bd = 5,relief="ridge",highlightbackground="#cfe6e4", highlightthickness=1)
        self.mainFrame.place(x=0, y=0)
        self.titleFrame = Frame(self.mainFrame, width = 1190, height = 100, bg = "#27dde3", relief="flat",highlightbackground="#cfe6e4", highlightthickness=1)
        self.titleFrame.place(x=0, y=0)
        self.heading = Label(self.titleFrame, text = "PASSWORDS MANAGER", font = ("Times New Roman", 35), bg = "#27dde3")
        self.heading.place(x=250, y=5)
        self.userLabel = Label(self.titleFrame, text = "username: " + self.login_username, font = ("Times New Roman", 15), bg = "#27dde3")
        self.userLabel.place(x = 400, y=50)
        self.searchFrame = Frame(self.mainFrame, width=390, height = 150, bg ="#27dde3", relief="flat",highlightbackground="#cfe6e4", highlightthickness=1)
        self.searchFrame.place(x=800, y=100)

        self.filterFrame = Frame(self.mainFrame, width=800, height = 50, bg ="#27dde3", relief="flat",highlightbackground="#cfe6e4", highlightthickness=1)
        self.filterFrame.place(x=0, y=100)

        self.sortbutton = Menubutton(self.filterFrame, text = "Sort", font = ("Times New Roman",15), relief="raised", width = 5,bd = 2)
        self.sortbutton.place(x = 0, y = 10)
        self.sortbutton.menu = Menu(self.sortbutton, tearoff = 0)
        self.sortbutton["menu"] = self.sortbutton.menu
        self.sortbutton.menu.add_command(label = "Ascending", command = lambda: self.displayData("site asc"))
        self.sortbutton.menu.add_command(label = "Descending", command = lambda: self.displayData("site desc"))
        self.sortbutton.menu.add_command(label = "First added", command = lambda: self.displayData("id asc"))

        self.tableFrame = Frame(self.mainFrame, width=800, height = 100, bg ="#27dde3", relief="flat",highlightbackground="#cfe6e4", highlightthickness=1)
        self.tableFrame.place(x=0, y=150)
        self.displayButton = Button(self.tableFrame, text = "show", relief = "raised",
                                    font = ("Times New Roman", 15),
                                    command = self.displayData)
        self.displayButton.place(x=0, y=50)
        self.dataFrame = Frame(self.mainFrame, width=1190, height = 350, bg ="#27dde3", bd = 5, relief="flat")
        self.dataFrame.pack_propagate(0)
        self.dataFrame.place(x=0, y=250)

        self.optionsFrame = Frame(self.mainFrame, width = 1190, height = 100, bg = "#27dde3", relief="flat")
        self.optionsFrame.place(x=300, y=600)

        self.scrollerY = Scrollbar(self.dataFrame, orient = VERTICAL)
        self.passwordRecords = ttk.Treeview(self.dataFrame, columns =("site","url","acc_username","acc_password"), height=15, yscrollcommand = self.scrollerY.set)
        self.scrollerY.pack(side = RIGHT, fill = Y)

        
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("None", 15))
        self.style.configure("Treeview.Column", font=("None", 15))

        self.passwordRecords.heading("site", text = "site")
        self.passwordRecords.heading("url", text = "url")
        self.passwordRecords.heading("acc_username", text = "username")
        self.passwordRecords.heading("acc_password", text = "password")
        self.passwordRecords['show'] = 'headings'

        self.passwordRecords.column("site", width=100)
        self.passwordRecords.column("url", width=100)
        self.passwordRecords.column("acc_username", width=100)
        self.passwordRecords.column("acc_password", width=100)

        #selectdata = self.selectData()#selectData method variable
        self.passwordRecords.pack(fill = BOTH, expand = 1)
        self.passwordRecords.bind("<ButtonRelease-1>", self.selectData)
        self.scrollerY.config(command=self.passwordRecords.yview)
        self.displayData()

        self.addButton = Button(self.optionsFrame, text = "Add new",
                                    font = ("Times New Roman", 20), command = lambda: self.clicked("addnew"))
        self.addButton.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.deleteButton = Button(self.optionsFrame, text = "Delete",
                                    font = ("Times New Roman", 20), command = self.deleteRecord)
        self.deleteButton.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.updateButton = Button(self.optionsFrame, text = "Update",
                                    font = ("Times New Roman", 20), command = lambda: self.clicked("update", self.row))
        self.updateButton.grid(row = 1, column = 2, padx = 10, pady = 10)

        #search record
        self.searchLabel = Label(self.searchFrame, text = "search:",font = ("Times New Roman", 15), bg = "#27dde3")
        self.searchLabel.place(x=20, y=10)
        self.searchEntry = Entry(self.searchFrame, font = ("Times New Roman", 15))
        self.searchEntry.place(x=100,y=10)
    
        self.opt = StringVar(value=" ") #make the radio button not select all options when app opens
        self.opt.set("site") #initial choice
        self.usernameRadio =  Radiobutton(self.searchFrame, text = "username", variable = self.opt , value = "acc_username", font = ("Times New Roman", 15), bg = "#27dde3", activebackground = "#27dde3")
        self.usernameRadio.place(x=20, y=60)
        self.usernameRadio =  Radiobutton(self.searchFrame, text = "password", variable = self.opt , value = "acc_password", font = ("Times New Roman", 15), bg = "#27dde3", activebackground = "#27dde3")
        self.usernameRadio.place(x=130, y=60)
        self.usernameRadio =  Radiobutton(self.searchFrame, text = "site", variable = self.opt , value = "site", font = ("Times New Roman", 15), bg = "#27dde3", activebackground = "#27dde3")
        self.usernameRadio.place(x=240, y=60)

        self.searchButton = Button(self.searchFrame, text = "search",
                                    font = ("Times New Roman", 15),
                                    command = self.searchRecord)
        self.searchButton.place(x=130, y=100)

    def clicked(self, option, row = None):

            if((option == "update" and len(row) != 0) or option == "addnew"):
              
                screen = Toplevel(self.root)
                screen.grab_set() #prevent parent window from working while this window is not closed
                insert_class = InsertData(screen, self.login_username, option, row, self.displayData)
                if(option == "update"):
                    insert_class.siteEntry.insert(0, row[0])
                    insert_class.urlEntry.insert(0, row[1])
                    insert_class.usernameEntry.insert(0, row[2])
                    insert_class.passwordEntry.insert(0, row[3])
                #screen.mainloop()
                self.row = None

    #select row data 
    def selectData(self, ev):
        try:
            viewInfo = self.passwordRecords.focus()
            passwordData = self.passwordRecords.item(viewInfo)
            self.row = passwordData['values']
        except:
            print("data selection error")
    #delete data record
    def deleteRecord(self):
        if(len(self.row) !=0):
            mydb = None
            try:
                s = self.row[0]  #site 
                u = self.row[1]  #url
                usr = self.row[2]  #username
                p = self.row[3]  #password
                mydb = sql.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "passwords_manager")
                print("database connection successful")
                cursor = mydb.cursor()
                cursor.execute("DELETE FROM accounts WHERE username = %s AND url=%s AND acc_username=%s AND acc_password=%s AND site=%s", (self.login_username,u,usr,p,s))
                mydb.commit()
                mydb.close()
                self.displayData()
            except Error as err:
                print(f"Error: {err}")
            finally:
                mydb.close()
                self.row = None
    #display data
    def displayData(self, order=None):
        try:
            mydb = sql.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "passwords_manager")
            print("database connection successful")
            cursor = mydb.cursor()

            #query: retrive records
            
            if order:
                cursor.execute("SELECT site,url,acc_username,acc_password FROM accounts WHERE username = %s ORDER BY " + order, (self.login_username,))
            else:
                cursor.execute("SELECT site,url,acc_username,acc_password FROM accounts WHERE username = %s", (self.login_username,))
            results = cursor.fetchall() #store records
            if(len(results) != 0):
                self.passwordRecords.delete(*self.passwordRecords.get_children())
                for row in results:
                    self.passwordRecords.insert('', END, values = row)
                    mydb.commit()
        except Error as err:
            print(f"Error: {err}")
        finally:
            mydb.close()
    #search value
    def searchRecord(self):
        value = self.searchEntry.get()
        if(len(value)>=1):
            try:
                mydb = sql.connect(host = "localhost",
                            user = "root",
                            password = "",
                            database = "passwords_manager")
                cursor = mydb.cursor()

                #query: retrive records
                item = self.opt.get() #get radion button option user uses to search
                cursor.execute("SELECT site,url,acc_username,acc_password FROM accounts WHERE username = %s AND " + item + " LIKE %s", (self.login_username, value + "%",))
                results = cursor.fetchall() #search results
                if(not results):
                    messagebox.showerror("Error", value + " not found")
                else:
                    self.passwordRecords.selection()
                    fetchdata = self.passwordRecords.get_children()
                    for f in fetchdata:
                        self.passwordRecords.delete(f)
                    for res in results:
                        self.passwordRecords.insert("", END, values=res)
            except Error as err:
                print(f"Error: {err}")
            finally:
                mydb.close()
"""rt = Tk()
c = MainScreen(rt, 'lukhanyo')
rt.mainloop()
"""