from datetime import datetime, date
import sqlite3
from tkinter import *
from tkinter import messagebox
import os
from numpy import record
import pandas as pd
from setuptools import Command

root = Tk()
root.title('Request Manager')
w = 520
h = 570
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.columnconfigure(0,weight=1) # column weight 100% 
# root.rowconfigure(0, weight=1) 
# root.rowconfigure(1, weight=1) # change weight to 4
# root.rowconfigure(2, weight=1)
# root.rowconfigure(3, weight=1)
app_menubar = Menu(root)
root.config(menu=app_menubar)

current_time = datetime.now()
formatted_date = current_time.strftime("%d-%m-%Y")
formatted_DateTime = current_time.strftime("%d-%m-%Y %H.%M")

def restart_command():
    root.destroy()
    os.startfile('inquiry_productivity2.pyw')

def search_records():
    newWindow = Toplevel(root)
    newWindow.title('Search Records')
    w = 1000
    h = 500
    ws = newWindow.winfo_screenwidth()
    hs = newWindow.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    newWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
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
        for record in r_set:
            for j in range(len(record)):
                results_area.grid(row=i)
                if not i % 10:
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

def open_manage_requests():
    initialize_mr_app()
    
def update_screen(old_window, rcd_id):
    old_window.destroy()
    print(rcd_id)
    updateWindow = Toplevel(root)
    updateWindow.title('Update Record')
    w = 520
    h = 570
    ws = updateWindow.winfo_screenwidth()
    hs = updateWindow.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    updateWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
    updateWindow.columnconfigure(0, weight=1)
    #Frames
    frame_top = Frame(updateWindow,)
    frame_mid_one = Frame(updateWindow,)
    frame_mid_two = Frame(updateWindow,)
    frame_mid_three = Frame(updateWindow,)
    frame_bottom = Frame(updateWindow,)
    frame_bottom_one = Frame(updateWindow,)
    frame_bottom_two = Frame(updateWindow,)
    frame_bottom_three = Frame(updateWindow,)
    #Frame Grid
    frame_top.grid(row=0, column=0, sticky='WENS')
    frame_mid_one.grid(row=1, column=0, sticky='WENS')
    frame_mid_two.grid(row=2, column=0, sticky='WENS')
    frame_mid_three.grid(row=3, column=0, sticky='WENS')
    frame_bottom.grid(row=4, column=0, sticky='WENS')
    frame_bottom_one.grid(row=5, column=0, sticky='WENS')
    frame_bottom_two.grid(row=6, column=0, sticky='WENS')
    frame_bottom_three.grid(row=7, column=0, sticky='WENS')
    #Frame Top 
    frame_top.columnconfigure(0, weight=1)
    frame_top.columnconfigure(1, weight=1)
    frame_top.columnconfigure(2, weight=1)
    frame_top.columnconfigure(3, weight=1)
    #Service
    Service_L = Label(frame_top, text='Service:')
    Service_L.grid(row=0, column=0,pady=10, sticky='E')
    options = [
        ' Police',
        ' Fire',
        ' Administration',
        ' Finance',
        ' City Water',
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
        pady=10,
        padx=15,
        sticky='W'
        )
    #Task
    Urgency_L = Label(frame_top,text="Urgency:")
    Urgency_L.grid(row=0,column=2, sticky='E')
    urgency_options = [
        ' Low',
        ' Medium',
        ' High',
        ' Emergency',
    ]
    clicked = StringVar()
    clicked.set(urgency_options[0])
    Urgency_OM = OptionMenu(frame_top, clicked, *urgency_options)
    Urgency_OM.grid( 
        row=0,
        column=3,
        pady=10,
        sticky='W'
        )
    #Frame Mid One----------------------------------------------------
    frame_mid_one.columnconfigure(0,weight=1)
    frame_mid_one.columnconfigure(1,weight=3)
    frame_mid_one.columnconfigure(2,weight=3)
    frame_mid_one.columnconfigure(3,weight=1)
    #State/Priority
    State_L = Label(frame_mid_one,text="State:")
    State_L.grid(row=1,column=0, sticky='E')
    state_options = [
        ' New',
        ' In-Progress',
        ' Resolved',
    ]
    clicked = StringVar()
    clicked.set(state_options[0])
    State_OM = OptionMenu(frame_mid_one, clicked, *state_options)
    State_OM.grid( 
        row=1,
        column=1,
        pady=10,
        sticky='WE'
        )
    #Caller
    Caller_L = Label(frame_mid_one,text='Name:')
    Caller_L.grid(row=1,column=2, sticky="WE")
    Caller_T = Entry(frame_mid_one, width=25)
    Caller_T.grid(row=1,column=3, sticky="W")
    #Frame Mid Two----------------------------------------------------
    frame_mid_two.columnconfigure(0,weight=1)
    frame_mid_two.columnconfigure(1,weight=1)
    frame_mid_two.columnconfigure(2,weight=1)
    frame_mid_two.columnconfigure(3,weight=1)
    #Email
    Email_L = Label(frame_mid_two,text='Email:')
    Email_L.grid(row=2,column=0, sticky="E")
    Email_T = Entry(frame_mid_two, width=25)
    Email_T.grid(row=2,column=1, sticky="W")
    #Frame Mid Three -------------------------------------------------
    frame_mid_three.columnconfigure(0,weight=1)
    frame_mid_three.columnconfigure(1,weight=1)
    frame_mid_three.columnconfigure(2,weight=1)
    frame_mid_three.columnconfigure(3,weight=1)
    #Phone Number
    Phone_L = Label(frame_mid_two,text='Phone:')
    Phone_L.grid(row=2,column=2, pady=10, sticky="W")
    Phone_T = Entry(frame_mid_two, width=25)
    Phone_T.grid(row=2,column=3, pady=10, sticky='W')
    #Frame Bottom -------------------------------------------------
    frame_bottom.columnconfigure(0,weight=1)
    frame_bottom.columnconfigure(1,weight=1)
    frame_bottom.columnconfigure(2,weight=1)
    frame_bottom.columnconfigure(3,weight=1)
    #Completion Date Label ---------------------------------------
    completed_Date_L = Label(frame_bottom, text='Completion Date:', padx=15)
    completed_Date_L.grid(row=4, column=1, pady=10)
    #Completed Date ----------------------------------------------
    completed_Date_input = Entry(frame_bottom, width=25)
    completed_Date_input.grid(row=4, column=2)
    #Frame Bottom One -------------------------------------------------
    frame_bottom_one.columnconfigure(0,weight=1)
    frame_bottom_one.columnconfigure(1,weight=1)
    frame_bottom_one.columnconfigure(2,weight=1)
    frame_bottom_one.columnconfigure(3,weight=1)
    #Description Label
    Description_L = Label(frame_bottom_one,text='Request Description:', padx=15)
    Description_L.grid(row=5,column=0, columnspan=0+4, pady=10)
    #Frame Bottom Two -------------------------------------------------
    frame_bottom_two.columnconfigure(0,weight=1)
    frame_bottom_two.columnconfigure(1,weight=1)
    frame_bottom_two.columnconfigure(2,weight=1)
    frame_bottom_two.columnconfigure(3,weight=1)
    #Description
    Description_T = Text(frame_bottom_two, wrap=WORD, height=16)
    Description_T.grid(row=6,column=0, pady=10, padx=20)
    #Frame Bottom Threhree-------------------------------------------------
    frame_bottom_three.columnconfigure(0,weight=1)
    frame_bottom_three.columnconfigure(1,weight=1)
    frame_bottom_three.columnconfigure(2,weight=1)
    frame_bottom_three.columnconfigure(3,weight=1)
    #Action Button
    Action_button_L = Button(frame_bottom_three,text='Confirm Update', command=update_record, padx=15)
    Action_button_L.grid(row=7,column=0, columnspan=0+4, pady=10)

def create_csvfile():
    #Connect to DB
    conn = sqlite3.connect('request.db')
    #Pandas to create CSV file
    df = pd.read_sql_query('Select * from request_entry', conn)
    #Handle Reports Folder and file name
    csv_filename = f'{formatted_DateTime}.csv'
    report_dir = './Reports'
    if not os.path.exists(report_dir):
        os.mkdir(report_dir)
    fullname = os.path.join(report_dir, csv_filename)
    #Create CSV
    df.to_csv(fullname)
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
#Actions
actions_menu = Menu(app_menubar, tearoff='off')
app_menubar.add_cascade(label='Actions', menu=actions_menu)
actions_menu.add_command(label='Manage Requests', command=open_manage_requests)
#Frames
frame_top = Frame(root,)
frame_mid_one = Frame(root,)
frame_mid_two = Frame(root,)
frame_mid_three = Frame(root,)
frame_bottom = Frame(root,)
frame_bottom_one = Frame(root,)
frame_bottom_two = Frame(root,)
frame_bottom_three = Frame(root,)
#Frame Grid
frame_top.grid(row=0, column=0, sticky='WENS')
frame_mid_one.grid(row=1, column=0, sticky='WENS')
frame_mid_two.grid(row=2, column=0, sticky='WENS')
frame_mid_three.grid(row=3, column=0, sticky='WENS')
frame_bottom.grid(row=4, column=0, sticky='WENS')
frame_bottom_one.grid(row=5, column=0, sticky='WENS')
frame_bottom_two.grid(row=6, column=0, sticky='WENS')
frame_bottom_three.grid(row=7, column=0, sticky='WENS')





def select_statement():
    #Select Statement to fill Listbox
    #Create connection to DB
    conn = sqlite3.connect('request.db')
    #Create Cursor
    c = conn.cursor()
    #Statement to execute
    c.execute(''' Select * from request_entry order by id; ''')
    for i in c:
        print(i)
    conn.commit()
    #Close connection to DB
    conn.close()

def initialize_mr_app():
    window = Toplevel(root)
    window.title('Manage Requests')

    #Service select
    manage_request_ServiceL = Label(window, text='Service:')
    manage_request_ServiceL.grid(row=0, column=0, pady=(10, 0), padx=(10, 0))
    options = [
        ' EMS',
        ' Fire',
        ' Administration',
        ' Finance',
        ' City Water',
        ' Sewer',
        ' Trash',
        ' Citizen Inquiry',
    ]
    clicked_Service = StringVar()
    clicked_Service.set(' EMS')
    manage_request_Service = OptionMenu(window, clicked_Service, *options)
    manage_request_Service.grid(
        row=0, 
        column=1,
        pady=(10, 0),
        sticky='W'
        )
    #Urgency Select
    manage_request_UrgencyL = Label(window, text='Urgency:')
    manage_request_UrgencyL.grid(row=0, column=2, pady=(10, 0), sticky='EW')

    urgency_options = [
        ' Low',
        ' Medium',
        ' High',
        ' Emergency',
    ]
    clicked = StringVar()
    clicked.set(' Low')
    Urgency_OM = OptionMenu(window, clicked, *urgency_options)
    Urgency_OM.grid( 
        row=0,
        column=3,
        sticky='EW',
        pady=(10, 0)
        )
    #Request State
    manage_request_StateL = Label(window, text='State:')
    manage_request_StateL.grid(row=1, column=0, padx=(10, 0))

    state_options = [
        ' New',
        ' In-Progress',
        ' Resolved',
    ]
    clicked = StringVar()
    clicked.set(' New')
    manage_request_State = OptionMenu(window, clicked, *state_options)
    manage_request_State.grid( 
        row=1,
        column=1,
        sticky='W'
        )
    #Name
    manage_request_NameL = Label(window, text='Name:')
    manage_request_NameL.grid(row=1, column=2, sticky='EW')

    mr_name = StringVar()
    manage_request_Name = Entry(window, textvariable=mr_name)
    manage_request_Name.grid(row=1, column=3,sticky='W')
    #Email
    manage_request_EmailL = Label(window, text='Email:')
    manage_request_EmailL.grid(row=2, column=0, padx=(10, 0))

    mr_email = StringVar()
    manage_request_Email = Entry(window, textvariable=mr_email)
    manage_request_Email.grid(row=2, column=1,sticky='W')
    #Phone
    manage_request_PhoneL = Label(window, text='Phone:')
    manage_request_PhoneL.grid(row=2, column=2,sticky='EW')

    mr_phone = StringVar()
    manage_request_Phone = Entry(window, textvariable=mr_phone)
    manage_request_Phone.grid(row=2, column=3,sticky='W')
    #Completion Date
    manage_request_CompletionL = Label(window, text='Completion Date:')
    manage_request_CompletionL.grid(row=3, column=1)

    mr_CompletionDate = StringVar()
    manage_request_Completion = Entry(window, textvariable=mr_CompletionDate)
    manage_request_Completion.grid(row=3, column=2)
    #Request Description
    request_descriptionL = Label(window, text='Request Description:')
    request_descriptionL.grid(row=4, column=1, columnspan=3)

    name_text7 = StringVar()
    request_description = Text(window, wrap=WORD, height=10, width=50)
    request_description.grid(row=5, column=1, columnspan=3)

    #Show records Widget
    listbox_ = Listbox(window, height=20, width=59)
    listbox_.grid(row=0, column=6, rowspan=6, columnspan=2, padx=(0,10), pady=(10,0))
    #Scrollbar
    scrl = Scrollbar(window,)
    scrl.grid(row=0, column=5, sticky='ns', rowspan=6, padx=(10, 0), pady=(10,0))
    #Attachment
    listbox_.configure(yscrollcommand=scrl.set)
    scrl.configure(command=listbox_.yview)
    
    def view_command():
        rows_returned = manage_requests_view()
        listbox_.delete(0,END)
        for row in rows_returned:
            listbox_.insert(END, row)
    #Buttons
    #Update
    b1 = Button(window, text='Update', width=12)
    b1.grid(row=7, column=1, pady=(0,10))
    #Delete
    b2 = Button(window, text='Delete', width=12)
    b2.grid(row=7, column=3, pady=(0,10))
    #View Records
    b3 = Button(window, text='View Records', command=view_command)
    b3.grid(row=7, column=6, columnspan=2)


    def manage_requests_view():
        conn = sqlite3.connect('request.db')
        cur=conn.cursor()
        cur.execute('Select * from request_entry')
        rows = cur.fetchall()
        conn.close()
        return rows

    # window.mainloop()

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
            completed_date text,
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
    if Caller_T.get() == '' or Email_T.get() == '' or Phone_T.get() == '' or Description_T.get('1.0', END) == '':
        messagebox.showinfo('Message', 'You have not filled in all fields.')
    else:
        # current_time = datetime.now()
        # formatted_DateTime = current_time.strftime("%d/%m/%Y %H:%M:%S")
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
                    completed_date,
                    description,
                    entered_timestamp)
                VALUES (:Service_OM, :Urgency_OM, :State_OM,
                        :Caller_T, :Email_T, :Phone_T, :Completed_Date,
                        :Description_T, :current_time) """,
                        {
                            'Service_OM': Service_OM['text'],
                            'Urgency_OM': Urgency_OM['text'],
                            'State_OM': State_OM['text'],
                            'Caller_T': Caller_T.get(),
                            'Email_T': Email_T.get(),
                            'Phone_T': Phone_T.get(),
                            'Completed_Date': completed_Date_input.get(),
                            'Description_T':Description_T.get('1.0', END),
                            'current_time': formatted_DateTime
                        })
        #Commit Changes
        conn.commit()
        #Close connection
        conn.close()
        report_dir = './Request_Documentation'
        if not os.path.exists(report_dir):
            os.mkdir(report_dir)
            caller_name = Caller_T.get().replace(' ', '-')
            request_foldername = caller_name + ' ' + formatted_date
            parent_sub = os.path.join(report_dir, request_foldername)
            os.mkdir(parent_sub)
        else:
            caller_name = Caller_T.get().replace('#%&}{/\?<>*!@$":+`|=', '-')
            request_foldername = caller_name + ' ' + formatted_date
            parent_sub = os.path.join(report_dir, request_foldername)
            os.mkdir(parent_sub)
        messagebox.showinfo('Message', "Entry was successful, fields will be cleared.")
        #Clear fields
        Caller_T.delete(0, END)
        Email_T.delete(0, END)
        Phone_T.delete(0, END)
        completed_Date_input.delete(0, END)
        Description_T.delete('1.0', END)

def update_record(request_list):
    conn = sqlite3.connect('request.db')
    c = conn.cursor()
    update_stmnt = c.execute('UPDATE request_entry')
    



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
Service_L = Label(frame_top, text='Service:')
Service_L.grid(row=0, column=0,pady=10, sticky='E')
options = [
    ' EMS',
    ' Fire',
    ' Administration',
    ' Finance',
    ' City Water',
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
    pady=10,
    padx=15,
    sticky='W'
    )
#Task
Urgency_L = Label(frame_top,text="Urgency:")
Urgency_L.grid(row=0,column=2, sticky='E')
urgency_options = [
    ' Low',
    ' Medium',
    ' High',
    ' Emergency',
]
clicked = StringVar()
clicked.set(urgency_options[0])
Urgency_OM = OptionMenu(frame_top, clicked, *urgency_options)
Urgency_OM.grid( 
    row=0,
    column=3,
    pady=10,
    sticky='W'
    )
#Frame Mid One----------------------------------------------------
frame_mid_one.columnconfigure(0,weight=1)
frame_mid_one.columnconfigure(1,weight=3)
frame_mid_one.columnconfigure(2,weight=3)
frame_mid_one.columnconfigure(3,weight=1)
#State/Priority
State_L = Label(frame_mid_one,text="State:")
State_L.grid(row=1,column=0, sticky='E')
state_options = [
    ' New',
    ' In-Progress',
    ' Resolved',
]
clicked = StringVar()
clicked.set(state_options[0])
State_OM = OptionMenu(frame_mid_one, clicked, *state_options)
State_OM.grid( 
    row=1,
    column=1,
    pady=10,
    sticky='WE'
    )
#Caller
Caller_L = Label(frame_mid_one,text='Caller:')
Caller_L.grid(row=1,column=2, sticky="WE")
Caller_T = Entry(frame_mid_one, width=25)
Caller_T.grid(row=1,column=3, sticky="W")
#Frame Mid Two----------------------------------------------------
frame_mid_two.columnconfigure(0,weight=1)
frame_mid_two.columnconfigure(1,weight=1)
frame_mid_two.columnconfigure(2,weight=1)
frame_mid_two.columnconfigure(3,weight=1)
#Email
Email_L = Label(frame_mid_two,text='Email:')
Email_L.grid(row=2,column=0, sticky="E")
Email_T = Entry(frame_mid_two, width=25)
Email_T.grid(row=2,column=1, sticky="W")
#Frame Mid Three -------------------------------------------------
frame_mid_three.columnconfigure(0,weight=1)
frame_mid_three.columnconfigure(1,weight=1)
frame_mid_three.columnconfigure(2,weight=1)
frame_mid_three.columnconfigure(3,weight=1)
#Phone Number
Phone_L = Label(frame_mid_two,text='Phone:')
Phone_L.grid(row=2,column=2, pady=10, sticky="W")
Phone_T = Entry(frame_mid_two, width=25)
Phone_T.grid(row=2,column=3, pady=10, sticky='W')
#Frame Bottom -------------------------------------------------
frame_bottom.columnconfigure(0,weight=1)
frame_bottom.columnconfigure(1,weight=1)
frame_bottom.columnconfigure(2,weight=1)
frame_bottom.columnconfigure(3,weight=1)
#Completion Date Label ---------------------------------------
completed_Date_L = Label(frame_bottom, text='Completion Date:', padx=15)
completed_Date_L.grid(row=4, column=1, pady=10, sticky='E')
#Completed Date ----------------------------------------------
completed_Date_input = Entry(frame_bottom, width=25)
completed_Date_input.grid(row=4, column=2, sticky='W')
#Frame Bottom One -------------------------------------------------
frame_bottom_one.columnconfigure(0,weight=1)
frame_bottom_one.columnconfigure(1,weight=1)
frame_bottom_one.columnconfigure(2,weight=1)
frame_bottom_one.columnconfigure(3,weight=1)
#Description Label
Description_L = Label(frame_bottom_one,text='Request Description:', padx=15)
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