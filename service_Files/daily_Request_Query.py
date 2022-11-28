import sqlite3
from datetime import date, datetime

def startup_Request_Due_Date_Alert():
    todays_date = date.today()
    todays_year = str(todays_date.year)
    todays_year = todays_year[2:4]
    todays_month = todays_date.month
    todays_day = str(todays_date.day)
    todays_day2 = int(todays_date.day) + 2
    todays_date = f'{todays_month}/{str(todays_day2)}/{todays_year}'
    conn = sqlite3.connect('request.db')
    c = conn.cursor()
    c.execute(f'''SELECT * FROM request_entry 
                    WHERE state <> 'Resolved'
                    AND SUBSTR(completed_date,1,2) = '{str(todays_month)}' 
                    AND SUBSTR(completed_date,7,2) = '{str(todays_year)}' 
                    AND SUBSTR(completed_date,4,2) <= '{str(todays_day2)}'
                    AND SUBSTR(completed_date,4,2) >= '{todays_day}'
                    ORDER BY SUBSTR(completed_date,4,2);''')
    my_entries = c.fetchall()
    conn.commit()
    conn.close()
    for f in my_entries:
        print(f)

if __name__ == '__main__':
    startup_Request_Due_Date_Alert()