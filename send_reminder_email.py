from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import smtplib
import ssl
from service_Files.secure import important_dictionary


def send_email(dict):
  request_entry = {}
  request_entry = dict
  sender_email = important_dictionary['sender_email']
  receiver_email = important_dictionary['receiver_email']
  password = important_dictionary['password']
  smtp_server = important_dictionary['smtp_server']
  port = important_dictionary['port']
  today_date = date.today()

  if request_entry['Update'] == False:
    # initialise message instance
    msg = MIMEMultipart()
    msg["Subject"] = f"New Request Reminder - {today_date}"
    msg["From"] = sender_email
    msg['To'] = receiver_email
    html = f"""<html>
                  <body>
                    <h1>New Request Reminder</h1>
                    <br>
                    <br>
                    <p>
                      You have Created a Request for <b>{request_entry['Name'].strip()}<b>.
                    </p>
                    <br>
                    <p>
                    Additional Details:<br>
                    Service: {request_entry['Service']}<br>
                    Priority: {request_entry['Urgency']}<br>
                    Request State: {request_entry['Request State']}<br>
                    Name: {request_entry['Name']}<br>
                    Email: {request_entry['Email']}<br>
                    Phone: {request_entry['Phone']}<br>
                    Completed by Date: {request_entry['Completed by Date']}<br>
                    Request Description: {request_entry['Request Description']}<br>
                    </p>
                  </body>
                </html>
            """
  else:
    # initialise message instance
    msg = MIMEMultipart()
    msg["Subject"] = f"Updated Request Reminder - {today_date}"
    msg["From"] = sender_email
    msg['To'] = receiver_email
    html = f"""<html>
                  <body>
                    <h1>Update Request Reminder</h1>
                    <br>
                    <br>
                    <p>
                      You have Updated a Request for <b>{request_entry['Name'].strip()}<b>.
                    </p>
                    <br>
                    <p>
                    Additional Details:<br>
                    Service: {request_entry['Service']}<br>
                    Priority: {request_entry['Urgency']}<br>
                    Request State: {request_entry['Request State']}<br>
                    Name: {request_entry['Name']}<br>
                    Email: {request_entry['Email']}<br>
                    Phone: {request_entry['Phone']}<br>
                    Completed by Date: {request_entry['Completed by Date']}<br>
                    Request Description: {request_entry['Request Description']}<br>
                    </p>
                    <br>
                    <br>
                    <p> Do NOT reply to this email.</p>
                  </body>
                </html>
            """  

  body_html = MIMEText(html, 'html')  # parse values into html text
  msg.attach(body_html)  # attaching the text body into msg

  context = ssl.create_default_context()
  # Try to log in to server and send email
  try:
      server = smtplib.SMTP(smtp_server, port)
      server.ehlo()  # check connection
      server.starttls(context=context)  # Secure the connection
      server.ehlo()  # check connection
      server.login(sender_email, password)

      # Send email here
      server.sendmail(sender_email, receiver_email, msg.as_string())
    
      return True

  except Exception as e:
      # Print any error messages to stdout
      print(e)
  finally:
      server.quit()
      
def daily_request_check(list):
  sender_email = important_dictionary['sender_email']
  receiver_email = important_dictionary['receiver_email']
  password = important_dictionary['password']
  smtp_server = important_dictionary['smtp_server']
  port = important_dictionary['port']
  today_date = date.today()
  my_record_list = list
  
    
  msg = MIMEMultipart()
  msg["Subject"] = f"Requests Nearing Completion - {today_date}"
  msg["From"] = sender_email
  msg['To'] = receiver_email
  html_object = []
  html_object.append("""<html>
                      <body>
                          <h1>Unresolved Requests Nearing Completion.</h1>
                          <br>
                          <br>
                          <br>
                          <p>""")
  for record in my_record_list:
      html_object.append(f"""
                          <br>
                          Additional Details:<br>
                          Service: {record[1]}<br>
                          Priority: {record[2]}<br>
                          Request State: {record[3]}<br>
                          Name: {record[4]}<br>
                          Email: {record[5]}<br>
                          Phone: {record[6]}<br>
                          Completed by Date: {record[7]}<br>
                          Request Description: {record[8]}
                          <br>""")
  html_object.append(f"""
                    Do NOT reply to this email.
                      </p>
                  </body>
              </html>
      """)
  full_html_string = "".join(html_object)
  body_html = MIMEText(full_html_string, 'html')  # parse values into html text
  msg.attach(body_html)  # attaching the text body into msg

  context = ssl.create_default_context()
  # Try to log in to server and send email
  try:
      server = smtplib.SMTP(smtp_server, port)
      server.ehlo()  # check connection
      server.starttls(context=context)  # Secure the connection
      server.ehlo()  # check connection
      server.login(sender_email, password)

      # Send email here
      server.sendmail(sender_email, receiver_email, msg.as_string())
    
      return True

  except Exception as e:
      # Print any error messages to stdout
      print(e)
  finally:
      server.quit()