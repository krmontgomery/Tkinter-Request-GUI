from datetime import datetime, date
import sqlite3
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import os
import pandas as pd
from send_reminder_email import send_email
from run_daily_job import run_daily_job_main

root = Tk()
root.title('Request Manager')
w = 550
h = 600
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.columnconfigure(0,weight=1) # column weight 100% 
app_menubar = Menu(root)
root.config(menu=app_menubar)
root.configure(bg='#042440')

current_time = datetime.now()
formatted_date = current_time.strftime("%d-%m-%Y")
formatted_DateTime = current_time.strftime("%d-%m-%Y %H.%M")

# Run Daily Job
run_daily_job_main()

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
    newWindow.configure(bg='#042440')
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
    results_area = Text(newWindow, wrap=WORD, insertbackground="white")
    results_area.configure(fg='White', bg='#133e63')
    results_area.grid(row=i,sticky='WENS')
    search_table = Button(newWindow, text='Search', command=select_all_records)
    search_table.grid(row=0, pady=10)

def open_manage_requests():
    initialize_mr_app()

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
#Set application backgroun color
frame_top.configure(bg='#042440')
frame_mid_one.configure(bg='#042440')
frame_mid_two.configure(bg='#042440')
frame_mid_three.configure(bg='#042440')
frame_bottom.configure(bg='#042440')
frame_bottom_one.configure(bg='#042440')
frame_bottom_two.configure(bg='#042440')
frame_bottom_three.configure(bg='#042440')
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
    w = 900
    h = 400
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    window.columnconfigure(0, weight=1)
    window.configure(bg='#042440')

    #Service select
    manage_request_ServiceL = Label(window, text='Service:')
    manage_request_ServiceL.configure(fg='White', bg='#042440', font=11)
    manage_request_ServiceL.grid(row=0, column=0, pady=(10, 0), padx=(10, 0))
    options = [
        'Police',
        'Fire',
        'Administration',
        'Finance',
        'City Water',
        'Sewer',
        'Trash',
        'Citizen Inquiry',
    ]
    clicked_Service = StringVar()
    clicked_Service.set('Police')
    manage_request_Service = OptionMenu(window, clicked_Service, *options)
    manage_request_Service.configure(fg='White', bg='#105c9e', font=8, highlightthickness=0)
    manage_request_Service.grid(
        row=0, 
        column=1,
        pady=(10,5),
        sticky='W'
        )
    #Urgency Select
    manage_request_UrgencyL = Label(window, text='Priority:', font=8)
    manage_request_UrgencyL.configure(fg='White', bg='#042440')
    manage_request_UrgencyL.grid(row=0, column=2, pady=(10, 0), sticky='EW')

    urgency_options = [
        'Low',
        'Medium',
        'High',
        'Emergency',
    ]
    clicked_urgent = StringVar()
    clicked_urgent.set(' Low')
    Urgency_OM = OptionMenu(window, clicked_urgent, *urgency_options)
    Urgency_OM.configure(fg='White', bg='#105c9e', font=8, highlightthickness=0)
    Urgency_OM.grid( 
        row=0,
        column=3,
        sticky='EW',
        pady=(10,5)
        )
    #Request State
    manage_request_StateL = Label(window, text='State:')
    manage_request_StateL.configure(fg='White', bg='#042440', font=11)
    manage_request_StateL.grid(row=1, column=0, padx=(10, 0))

    state_options = [
        'New',
        'In-Progress',
        'Resolved',
    ]
    clicked_state = StringVar()
    clicked_state.set(' New')
    manage_request_State = OptionMenu(window, clicked_state, *state_options)
    manage_request_State.configure(fg='White', bg='#105c9e', font=11, highlightthickness=0)
    manage_request_State.grid( 
        row=1,
        column=1,
        sticky='W',
        pady=5
        )
    #Name
    manage_request_NameL = Label(window, text='Name:')
    manage_request_NameL.configure(fg='White', bg='#042440', font=11)
    manage_request_NameL.grid(row=1, column=2, sticky='EW')

    mr_name = StringVar()
    manage_request_Name = Entry(window, textvariable=mr_name, fg='white', bg='#133e63', insertbackground="white")
    manage_request_Name.grid(row=1, column=3,sticky='W')
    #Email
    manage_request_EmailL = Label(window, text='Email:')
    manage_request_EmailL.configure(fg='White', bg='#042440', font=11)
    manage_request_EmailL.grid(row=2, column=0, padx=(10, 0))

    mr_email = StringVar()
    manage_request_Email = Entry(window, textvariable=mr_email, fg='white', bg='#133e63', insertbackground="white")
    manage_request_Email.grid(row=2, column=1,sticky='W')
    #Phone
    manage_request_PhoneL = Label(window, text='Phone:')
    manage_request_PhoneL.configure(fg='White', bg='#042440', font=11)
    manage_request_PhoneL.grid(row=2, column=2,sticky='EW')

    mr_phone = StringVar()
    manage_request_Phone = Entry(window, textvariable=mr_phone, fg='white', bg='#133e63', insertbackground="white")
    manage_request_Phone.grid(row=2, column=3,sticky='W')
    #Completion Date
    manage_request_CompletionL = Label(window, text='Completion Date:')
    manage_request_CompletionL.configure(fg='White', bg='#042440', font=11)
    manage_request_CompletionL.grid(row=3, column=1, sticky='E')

    # mr_CompletionDate = StringVar()
    # manage_request_Completion = Entry(window, textvariable=mr_CompletionDate, fg='white', bg='#133e63', insertbackground="white")
    # manage_request_Completion.grid(row=3, column=2)
    manage_request_Completion = DateEntry(window, selectmode='day',background='#133e63', foreground='white')
    manage_request_Completion.grid(row=3, column=3, sticky='W')
    #Request Description
    request_descriptionL = Label(window, text='Request Description:')
    request_descriptionL.configure(fg='White', bg='#042440', font=11)
    request_descriptionL.grid(row=4, column=1, columnspan=3)

    request_description = Text(window, wrap=WORD, height=10, width=50, fg='white', bg='#133e63', insertbackground="white")
    request_description.grid(row=5, column=1, columnspan=3)

    #Show records Widget
    listbox_ = Listbox(window, height=20, width=59, exportselection=0, fg='white', bg='#133e63', highlightthickness=0)
    listbox_.grid(row=0, column=6, rowspan=6, columnspan=2, padx=(0,10), pady=(10,0))
    #Scrollbar
    scrl = Scrollbar(window,)
    scrl.grid(row=0, column=5, sticky='ns', rowspan=6, padx=(10, 0), pady=(10,0),)
    #Attachment
    listbox_.configure(yscrollcommand=scrl.set)
    scrl.configure(command=listbox_.yview)
    
    def view_command():
        rows_returned = manage_requests_view()
        listbox_.delete(0,END)
        for row in rows_returned:
            listbox_.insert(END, row)

    def get_selected_record(event):
        index = listbox_.curselection()[0]
        selected_record = listbox_.get(index)
        print(f'{str(selected_record[0])} / {selected_record[1]} / {selected_record[2]} / {selected_record[3]}')
        #Service Option menu
        service_options = [
        'Police',
        'Fire',
        'Administration',
        'Finance',
        'City Water',
        'Sewer',
        'Trash',
        'Citizen Inquiry',
        ]
        manage_request_Service.destroy()
        clicked_Service.set(selected_record[1])
        manage_Service = OptionMenu(window, clicked_Service, *service_options)
        manage_Service.configure(fg='White', bg='#105c9e', font=11, highlightthickness=0)
        manage_Service.grid(
            row=0, 
            column=1,
            pady=(10, 0),
            sticky='W'
            )
        #Urgency Option Menu
        urgency_options = [
            ' Low',
            ' Medium',
            ' High',
            ' Emergency',
        ]
        clicked_urgent.set(selected_record[2])
        manage_request_urgency = OptionMenu(window, clicked_urgent, *urgency_options)
        manage_request_urgency.configure(fg='White', bg='#105c9e', font=11, highlightthickness=0)
        manage_request_urgency.grid( 
            row=0,
            column=3,
            sticky='EW',
            pady=(10, 0)
            )
        #State Option Menu
        state_options = [
        ' New',
        ' In-Progress',
        ' Resolved'
        ]
        clicked_state.set(selected_record[3])
        manage_request_State2 = OptionMenu(window, clicked_state, *state_options)
        manage_request_State2.configure(fg='White', bg='#105c9e', font=11, highlightthickness=0)
        manage_request_State2.grid( 
            row=1,
            column=1,
            sticky='EW'
            )
        #Name
        manage_request_Name.delete(0, END)
        manage_request_Name.insert(END, selected_record[4])
        #Email
        manage_request_Email.delete(0, END)
        manage_request_Email.insert(END, selected_record[5])
        #Phone
        manage_request_Phone.delete(0, END)
        manage_request_Phone.insert(END, selected_record[6])
        #Completion Date
        manage_request_Completion.delete(0, END)
        manage_request_Completion.insert(END, selected_record[7])
        #Request Description
        request_description.delete('1.0', END)
        request_description.insert('1.0', selected_record[8])

    listbox_.bind('<<ListboxSelect>>', get_selected_record)

    def get_record_id():
        index = listbox_.curselection()[0]
        selected_record = listbox_.get(index)
        print(selected_record[0], 'get_record_id, selected_record[0]')
        #Connect to DB
        conn = sqlite3.connect('request.db')
        #Set Cursor
        c = conn.cursor()        
        c.execute(f'''SELECT id FROM request_entry where id = {selected_record[0]};''')       
        # #Retrieve ID
        record_id = c.fetchone()
        conn.commit()
        conn.close()  
        
        return record_id

    def delete_command():
        try:
            rcd_id = get_record_id()
            rcd_id = str(rcd_id).strip('(,)')
            does_user_consent = messagebox.askyesno(title='Delete Record', message='Are you sure you want to delete this record?', parent=window)
            print(does_user_consent)
            print(rcd_id)
            if does_user_consent == True:
                conn = sqlite3.connect('request.db')
                c = conn.cursor()
                c.execute(f'DELETE FROM request_entry WHERE id={rcd_id};')
                conn.commit()
                conn.close()
                #Service Option Reset
                clicked_Service.set(service_options[0])
                #Urgency options reset
                clicked_urgent.set(urgency_options[0])
                #State Options Reset
                clicked_state.set(state_options[0])
                #Name
                manage_request_Name.delete(0, END)
                #Email
                manage_request_Email.delete(0, END)
                #Phone
                manage_request_Phone.delete(0, END)
                #Completion Date
                manage_request_Completion.delete(0, END)
                #Request Description
                request_description.delete('1.0', END)
                # print(root.focus_get())
                # if str(root.focus_get()) != '.!toplevel.!listbox':
                #     print('poo')
                # else: 
                #     print('yay')  
            else:
                messagebox.showinfo(title='Delete Record', message='Record was NOT deleted.', parent=window)
        except IndexError:
            messagebox.showerror(title='Delete Error', message="You're trying to delete an unselected record!", parent=window)

    def update_command():
        if messagebox.askyesno(title='Update Record', message='Are you sure you want to update this record?', parent=window):
            try:
                index = listbox_.curselection()[0]
                selected_record = listbox_.get(index)
                conn = sqlite3.connect('request.db')
                c = conn.cursor()
                c.execute('''UPDATE request_entry SET city_service=?, urgency=?, state=?,
                            caller=?, email=?, phone=?, completed_date=?, description=? WHERE id=?''',
                        (clicked_Service.get().strip(),clicked_urgent.get().strip(),clicked_state.get().strip(),
                            manage_request_Name.get().strip(), manage_request_Email.get().strip(), manage_request_Phone.get().strip(), 
                            manage_request_Completion.get().strip(), request_description.get('1.0', END).strip(), selected_record[0]))
                conn.commit()
                conn.close()
                #Send Email - Dictionary import to function
                updateRequestEntryDict = {
                        'Service': clicked_Service.get(),
                        'Urgency': clicked_urgent.get(),
                        'Request State': clicked_state.get(),
                        'Name': manage_request_Name.get(),
                        'Email': manage_request_Email.get(),
                        'Phone': manage_request_Phone.get(),
                        'Completed by Date': manage_request_Completion.get(),
                        'Request Description': request_description.get('1.0', END),
                        'Update': True
                }
                if messagebox.askyesno('Send Email', 'Do you want to send an email for this Update Request Entry?', parent=window) == True:
                    if send_email(updateRequestEntryDict):
                        messagebox.showinfo('Send Email', 'Emailing Reminder for Updated Request Entry', parent=window)
                else:
                    messagebox.showinfo('Send Email', 'Update email was not sent!', parent=window)
                #Service Option Reset
                clicked_Service.set(service_options[0])
                #Urgency options reset
                clicked_urgent.set(urgency_options[0])
                #State Options Reset
                clicked_state.set(state_options[0])
                #Name
                manage_request_Name.delete(0, END)
                #Email
                manage_request_Email.delete(0, END)
                #Phone
                manage_request_Phone.delete(0, END)
                #Completion Date
                manage_request_Completion.delete(0, END)
                #Request Description
                request_description.delete('1.0', END)
                messagebox.showinfo(title='Update Record', message='Record was successfully updated!', parent=window)
            except IndexError:
                messagebox.showerror(title='Update Error', message="You don't have a record selected to update!", parent=window)
        else:
            messagebox.showinfo(title='Update Record', message='Record was not updated.', parent=window)

    #Buttons
    #Update
    b1 = Button(window, text='Update', width=12, command=update_command)
    b1.configure(bg='#00db84')
    b1.grid(row=7, column=1, pady=10)
    #Delete
    b2 = Button(window, text='Delete', width=12, command=delete_command)
    b2.configure(bg='#d65454')
    b2.grid(row=7, column=3, pady=10)
    #View Records
    b3 = Button(window, text='View Records/Refresh', command=view_command)
    b3.grid(row=7, column=6, columnspan=2, pady=10)


    def manage_requests_view():
        conn = sqlite3.connect('request.db')
        cur=conn.cursor()
        cur.execute('Select * from request_entry')
        rows = cur.fetchall()
        conn.close()
        return rows

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
                            'Service_OM': clicked_serv.get().lstrip(),
                            'Urgency_OM': clicked_urg.get().lstrip(),
                            'State_OM': clicked_stat.get().lstrip(),
                            'Caller_T': Caller_T.get().lstrip(),
                            'Email_T': Email_T.get().lstrip(),
                            'Phone_T': Phone_T.get().lstrip(),
                            'Completed_Date': completed_Date_input.get(),
                            'Description_T':Description_T.get('1.0', END).lstrip(),
                            'current_time': formatted_DateTime
                        })
        print(completed_Date_input.get_date())
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
        #Send Email - Dictionary import to function
        requestEntryDictionary = {
                'Service': clicked_serv.get(),
                'Urgency': clicked_urg.get(),
                'Request State': clicked_stat.get(),
                'Name': Caller_T.get(),
                'Email': Email_T.get(),
                'Phone': Phone_T.get(),
                'Completed by Date': completed_Date_input.get(),
                'Request Description':Description_T.get('1.0', END),
                'Update': False
        }
        if messagebox.askyesno('Send Email', 'Do you want to send an email for this Request Entry?') == True:
            if send_email(requestEntryDictionary):
                messagebox.showinfo('Send Email', 'Email reminder sent for Request Entry!')
        else:
            messagebox.showinfo('Send Email', 'Email was not sent!')
        #Clear fields
        #Service
        clicked_serv.set(service_options[0])
        #Task Urgency
        clicked_urg.set(urgency_options[0])
        #State/Priority
        clicked_stat.set(state_options[0])
        Caller_T.delete(0, END)
        Email_T.delete(0, END)
        Phone_T.delete(0, END)
        Description_T.delete('1.0', END)

#Frame Top 
frame_top.columnconfigure(0, weight=1)
frame_top.columnconfigure(1, weight=1)
frame_top.columnconfigure(2, weight=1)
frame_top.columnconfigure(3, weight=1)
#Service
Service_L = Label(frame_top, text='Service:',fg='White', bg='#042440', font=11)
Service_L.grid(row=0, column=0,pady=10, sticky='E')
service_options = [
    ' Police',
    ' Fire',
    ' Administration',
    ' Finance',
    ' City Water',
    ' Sewer',
    ' Trash',
    ' Citizen Inquiry',
]
clicked_serv = StringVar()
clicked_serv.set(service_options[0])
Service_OM = OptionMenu(frame_top, clicked_serv, *service_options)
Service_OM.configure(fg='White', bg='#105c9e', font=11, highlightthickness=0)
Service_OM.grid(
    row=0, 
    column=1,
    pady=10,
    padx=15,
    sticky='W'
    )
#Task
Urgency_L = Label(frame_top,text="Priority:",fg='White', bg='#042440', font=11)
Urgency_L.grid(row=0,column=2, sticky='E')
urgency_options = [
    ' Low',
    ' Medium',
    ' High',
    ' Emergency',
]
clicked_urg = StringVar()
clicked_urg.set(urgency_options[0])
Urgency_OM = OptionMenu(frame_top, clicked_urg, *urgency_options)
Urgency_OM.configure(fg='White', bg='#105c9e', font=11, highlightthickness=0)
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
State_L = Label(frame_mid_one,text="State:",fg='White', bg='#042440', font=11)
State_L.grid(row=1,column=0, sticky='E')
state_options = [
    ' New',
    ' In-Progress',
    ' Resolved',
]
clicked_stat = StringVar()
clicked_stat.set(state_options[0])
State_OM = OptionMenu(frame_mid_one, clicked_stat, *state_options)
State_OM.configure(fg='White', bg='#105c9e', font=11, highlightthickness=0)
State_OM.grid( 
    row=1,
    column=1,
    pady=10,
    sticky='W'
    )
#Caller
Caller_L = Label(frame_mid_one,text='Name:',fg='White', bg='#042440', font=11)
Caller_L.grid(row=1,column=2, sticky="WE")
Caller_T = Entry(frame_mid_one, width=25, insertbackground="white")
Caller_T.configure(fg='White', bg='#133e63')
Caller_T.grid(row=1,column=3, sticky="W")
#Frame Mid Two----------------------------------------------------
frame_mid_two.columnconfigure(0,weight=1)
frame_mid_two.columnconfigure(1,weight=1)
frame_mid_two.columnconfigure(2,weight=1)
frame_mid_two.columnconfigure(3,weight=1)
#Email
Email_L = Label(frame_mid_two,text='Email:',fg='White', bg='#042440', font=11)
Email_L.grid(row=2,column=0, sticky="E")
Email_T = Entry(frame_mid_two, width=25, insertbackground="white")
Email_T.configure(fg='White', bg='#133e63')
Email_T.grid(row=2,column=1, sticky="W")
#Frame Mid Three -------------------------------------------------
frame_mid_three.columnconfigure(0,weight=1)
frame_mid_three.columnconfigure(1,weight=1)
frame_mid_three.columnconfigure(2,weight=1)
frame_mid_three.columnconfigure(3,weight=1)
#Phone Number
Phone_L = Label(frame_mid_two,text='Phone:',fg='White', bg='#042440', font=11)
Phone_L.grid(row=2,column=2, pady=10, sticky="W")
Phone_T = Entry(frame_mid_two, width=25, insertbackground="white")
Phone_T.configure(fg='White', bg='#133e63')
Phone_T.grid(row=2,column=3, pady=10, sticky='W')
#Frame Bottom -------------------------------------------------
frame_bottom.columnconfigure(0,weight=1)
frame_bottom.columnconfigure(1,weight=1)
frame_bottom.columnconfigure(2,weight=1)
frame_bottom.columnconfigure(3,weight=1)
#Completion Date Label ---------------------------------------
completed_Date_L = Label(frame_bottom, text='Completion Date:', padx=15,fg='White', bg='#042440', font=11)
completed_Date_L.grid(row=4, column=1, pady=10,)
#Completed Date ----------------------------------------------
completed_Date_input = DateEntry(frame_bottom, selectmode='day',background='#133e63', foreground='white')
completed_Date_input.grid(row=4, column=2, sticky='W')
#Frame Bottom One -------------------------------------------------
frame_bottom_one.columnconfigure(0,weight=1)
frame_bottom_one.columnconfigure(1,weight=1)
frame_bottom_one.columnconfigure(2,weight=1)
frame_bottom_one.columnconfigure(3,weight=1)
#Description Label
Description_L = Label(frame_bottom_one,text='Request Description:', padx=15,fg='White', bg='#042440', font=11)
Description_L.grid(row=4,column=0, columnspan=0+4, pady=10)
#Frame Bottom Two -------------------------------------------------
frame_bottom_two.columnconfigure(0,weight=1)
frame_bottom_two.columnconfigure(1,weight=1)
frame_bottom_two.columnconfigure(2,weight=1)
frame_bottom_two.columnconfigure(3,weight=1)
#Description
Description_T = Text(frame_bottom_two, wrap=WORD, height=16, insertbackground="white")
Description_T.configure(fg='White', bg='#133e63')
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
    else:
        messagebox.showinfo("Message", "Table didn't exist. Has been created.")
#Action Button
Action_button_L = Button(frame_bottom_three,text='Confirm Entry', command=button_func, padx=15, bg='#00db84')
Action_button_L.grid(row=5,column=0, columnspan=0+4, pady=10)

root.mainloop()