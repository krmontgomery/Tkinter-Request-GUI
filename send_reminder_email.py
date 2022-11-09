from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import smtplib
import ssl
from secure import important_dictionary


def send_email(dict):
  request_entry = {}
  request_entry = dict
  sender_email = important_dictionary['sender_email']
  receiver_email = important_dictionary['receiver_email']
  password = important_dictionary['password']
  smtp_server = important_dictionary['smtp_server']
  port = important_dictionary['port']
  today_date = date.today()

  # initialise message instance
  msg = MIMEMultipart()
  msg["Subject"] = f"Request Reminder - {today_date}"
  msg["From"] = sender_email
  msg['To'] = receiver_email

  html = f"""<html>
                <body>
                  <h1>Request Reminder</h1>
                  <br>
                  <br>
                  <p>
                    You have created a request for <b>{request_entry['Name'].strip()}<b>.
                  </p>
                  <br>
                  <p>
                  Additional Details:<br>
                  Service: {request_entry['Service']}<br>
                  Urgency: {request_entry['Urgency']}<br>
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

  except Exception as e:
      # Print any error messages to stdout
      print(e)
  finally:
      server.quit()