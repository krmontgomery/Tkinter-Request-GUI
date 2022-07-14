from datetime import datetime
import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import date
import os
import pandas as pd

root = Tk()
root.title('Request Manager')
root.geometry('500x550')
root.columnconfigure(0,weight=1) # column weight 100% 
# root.rowconfigure(0, weight=1) 
# root.rowconfigure(1, weight=1) # change weight to 4
# root.rowconfigure(2, weight=1)
# root.rowconfigure(3, weight=1)
app_menubar = Menu(root)
root.config(menu=app_menubar)

def restart_command():
    root.destroy()
    os.startfile('inquiry_productivity2.pyw')

def search_records():
    newWindow = Toplevel(root)
    newWindow.title('Search Records')
    newWindow.geometry('1000x500')
    newWindow.columnconfigure(0, weight=1)
    i=1
    def select_all_records():
        results_area.delete('1.0',END)
        #Create DB/Connect to DB
        conn = sqlite3.connect('request.db')
        #Create Cursor
        c = conn.cursor()
        r_set = c.execute('Select * from request_entry')
        i=0
        i_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
        for record in r_set:
            for j in range(len(record)):
                results_area.grid(row=i)
                if i in i_list:
                    results_area.insert(END, '\n\n')
                else:
                    pass
                results_area.insert(END, str(record[j]).strip('\n').strip(' '))
                results_area.insert(END, ',')
                i=i+1
        #Commit Changes
        conn.commit()
        #Close connection
        conn.close()
    results_area = Text(newWindow, wrap=WORD)
    results_area.grid(row=i,sticky='WENS')
    search_table = Button(newWindow, text='Search', command=select_all_records)
    search_table.grid(row=0, pady=10)

def create_csvfile():
    conn = sqlite3.connect('request.db')
    #Create Cursor
    today = date.today()
    todays_date = today.strftime("%b-%d-%Y")
    #Pandas to create CSV file
    df = pd.read_sql_query('Select * from request_entry', conn)
    df.to_csv(f'./Reports/{todays_date}.csv')
    #Commit Changes
    conn.commit()
    #Close connection
    conn.close()

#Create Menu Items -------------------------------------------------------------
#File
file_menu = Menu(app_menubar, tearoff="off")
app_menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label='Restart', command=restart_command)
file_menu.add_command(label='Exit', command=root.quit)
#Utilities
utilities_menu = Menu(app_menubar, tearoff="off")
app_menubar.add_cascade(label='Utilities', menu=utilities_menu)
utilities_menu.add_command(label='Show All Records', command=search_records)
utilities_menu.add_command(label='Create Report', command=create_csvfile)

#Frames
frame_top = Frame(root,)
frame_mid_one = Frame(root,)
frame_mid_two = Frame(root,)
frame_mid_three = Frame(root,)
frame_bottom = Frame(root,)
frame_bottom_two = Frame(root,)
frame_bottom_three = Frame(root,)
#Frame Grid
frame_top.grid(row=0, column=0, sticky='WENS')
frame_mid_one.grid(row=1, column=0, sticky='WENS')
frame_mid_two.grid(row=2, column=0, sticky='WENS')
frame_mid_three.grid(row=3, column=0, sticky='WENS')
frame_bottom.grid(row=4, column=0, sticky='WENS')
frame_bottom_two.grid(row=5, column=0, sticky='WENS')
frame_bottom_three.grid(row=6, column=0, sticky='WENS')

Service_OM = StringVar()

# #Create DB/Connect to DB
# conn = sqlite3.connect('request.db')
# #Create Cursor
# c = conn.cursor()

# c.execute('''Drop table if exists request_entry ''')

# #Commit Changes
# conn.commit()
# #Close connection
# conn.close()

def doesTableExist():
    #Create DB/Connect to DB
    conn = sqlite3.connect('request.db')
    #Create Cursor
    c = conn.cursor()

    tableIndicator = c.execute(''' Select name from sqlite_master where type='table' and name='request_entry'; ''').fetchall()

    if tableIndicator == []:  
        #Create Table
        c.execute("""CREATE TABLE request_entry(
            id integer primary key,
            city_service text,
            urgency text,
            state text,
            caller text,
            email text,
            phone integer,
            filename text,
            description text,
            entered_timestamp text
            );""")
        #Commit Changes
        conn.commit()
        #Close connection
        conn.close()
        print('DB Table has been created.')
        return False
    else:
        return True

def insertIntoTable():

    if Caller_T.get() == '' or Email_T.get() == '' or Phone_T.get() == '' or Filename_T.get() == '' or Description_T.get('1.0', END) == '':
        messagebox.showinfo('Message', 'You have not filled in all fields.')
    else:
        current_time = datetime.datetime.now()
        #Create DB/Connect to DB
        conn = sqlite3.connect('request.db')
        #Create Cursor
        c = conn.cursor()
        #Insert
        c.execute("""INSERT INTO request_entry (
                    city_service,
                    urgency,
                    state,
                    caller,
                    email,
                    phone,
                    filename,
                    description,
                    entered_timestamp)
                VALUES (:Service_OM, :Urgency_OM, :State_OM,
                        :Caller_T, :Email_T, :Phone_T, :Filename_T,
                        :Description_T, :current_time) """,
                        {
                            'Service_OM': Service_OM['text'],
                            'Urgency_OM': Urgency_OM['text'],
                            'State_OM': State_OM['text'],
                            'Caller_T': Caller_T.get(),
                            'Email_T': Email_T.get(),
                            'Phone_T': Phone_T.get(),
                            'Filename_T': Filename_T.get(),
                            'Description_T':Description_T.get('1.0', END),
                            'current_time': current_time
                        })
        #Commit Changes
        conn.commit()
        #Close connection
        conn.close()

        messagebox.showinfo('Message', "Entry was successful, fields have been cleared.")
        #Clear fields
        Caller_T.delete(0, END)
        Email_T.delete(0, END)
        Phone_T.delete(0, END)
        Filename_T.delete(0, END)
        Description_T.delete(0, END)

def select_all_records():
    #Create DB/Connect to DB
    conn = sqlite3.connect('request.db')
    #Create Cursor
    c = conn.cursor()
    r_set = c.execute('Select * from request_entry')
    #Commit Changes
    conn.commit()
    #Close connection
    conn.close()



#Frame Top 
frame_top.columnconfigure(0, weight=1)
frame_top.columnconfigure(1, weight=1)
frame_top.columnconfigure(2, weight=1)
frame_top.columnconfigure(3, weight=1)
#Service
Service_L = Label(frame_top, text='City Service:')
Service_L.grid(row=0, column=1,pady=10)
options = [
    ' Water',
    ' Sewer',
    ' Trash',
    ' Citizen Inquiry',
]
clicked = StringVar()
clicked.set(options[0])
Service_OM = OptionMenu(frame_top, clicked, *options)
Service_OM.grid(
    row=0, 
    column=1,
    columnspan=1+2,
    pady=10
    )
#Frame Mid----------------------------------------------------
frame_mid_one.columnconfigure(0,weight=1)
frame_mid_one.columnconfigure(1,weight=1)
frame_mid_one.columnconfigure(2,weight=1)
frame_mid_one.columnconfigure(3,weight=1)
#Task
Urgency_L = Label(frame_mid_one,text="Urgency:", padx=15)
Urgency_L.grid(row=1,column=0)
urgency_options = [
    ' Low',
    ' Medium',
    ' High',
    ' Emergency',
]
clicked = StringVar()
clicked.set(urgency_options[0])
Urgency_OM = OptionMenu(frame_mid_one, clicked, *urgency_options)
Urgency_OM.grid( 
    row=1,
    column=1,
    pady=10
    )
#State/Priority
State_L = Label(frame_mid_one,text="State:", padx=15)
State_L.grid(row=1,column=2)
state_options = [
    ' New',
    ' In-Progress',
    ' Resolved',
    ' Cancelled',
]
clicked = StringVar()
clicked.set(state_options[0])
State_OM = OptionMenu(frame_mid_one, clicked, *state_options)
State_OM.grid( 
    row=1,
    column=3,
    pady=10
    )
#Frame Mid Two----------------------------------------------------
frame_mid_two.columnconfigure(0,weight=1)
frame_mid_two.columnconfigure(1,weight=1)
frame_mid_two.columnconfigure(2,weight=1)
frame_mid_two.columnconfigure(3,weight=1)
#Caller
Caller_L = Label(frame_mid_two,text='Caller:', padx=15)
Caller_L.grid(row=2,column=0)
Caller_T = Entry(frame_mid_two, width=25)
Caller_T.grid(row=2,column=1)
#Email
Email_L = Label(frame_mid_two,text='Email:', padx=15)
Email_L.grid(row=2,column=2)
Email_T = Entry(frame_mid_two, width=25)
Email_T.grid(row=2,column=3)
#Frame Mid Three -------------------------------------------------
frame_mid_three.columnconfigure(0,weight=1)
frame_mid_three.columnconfigure(1,weight=1)
frame_mid_three.columnconfigure(2,weight=1)
frame_mid_three.columnconfigure(3,weight=1)
#Phone Number
Phone_L = Label(frame_mid_three,text='Phone:', padx=15)
Phone_L.grid(row=3,column=0, pady=10)
Phone_T = Entry(frame_mid_three, width=25)
Phone_T.grid(row=3,column=1, pady=10)
#Short Filename
Filename_L = Label(frame_mid_three,text='Filename:', padx=15)
Filename_L.grid(row=3,column=2, pady=10)
Filename_T = Entry(frame_mid_three, width=25)
Filename_T.grid(row=3,column=3, pady=10)
#Frame Bottom -------------------------------------------------
frame_bottom.columnconfigure(0,weight=1)
frame_bottom.columnconfigure(1,weight=1)
frame_bottom.columnconfigure(2,weight=1)
frame_bottom.columnconfigure(3,weight=1)
#Description Label
Description_L = Label(frame_bottom,text='Request Description:', padx=15)
Description_L.grid(row=4,column=0, columnspan=0+4, pady=10)
#Frame Bottom Two -------------------------------------------------
frame_bottom_two.columnconfigure(0,weight=1)
frame_bottom_two.columnconfigure(1,weight=1)
frame_bottom_two.columnconfigure(2,weight=1)
frame_bottom_two.columnconfigure(3,weight=1)
#Description
Description_T = Text(frame_bottom_two, wrap=WORD, height=16)
Description_T.grid(row=4,column=0, pady=10, padx=20)
#Frame Bottom Threhree-------------------------------------------------
frame_bottom_three.columnconfigure(0,weight=1)
frame_bottom_three.columnconfigure(1,weight=1)
frame_bottom_three.columnconfigure(2,weight=1)
frame_bottom_three.columnconfigure(3,weight=1)
#Functions
def button_func():
    tblExistsIndicator = doesTableExist()
    if tblExistsIndicator == True:
        insertIntoTable()
        # messagebox.showinfo("Message", "Table Exists!")
    else:
        messagebox.showinfo("Message", "Table didn't exist. Has been created.")
#Action Button
Action_button_L = Button(frame_bottom_three,text='Confirm Entry', command=button_func, padx=15)
Action_button_L.grid(row=5,column=0, columnspan=0+4, pady=10)

root.mainloop()