import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
from datetime import datetime

# URL for the GET request to fetch the HTML content

def send_email(quota):
    # Email credentials and settings
    sender_email = "sender-email-address"
    sender_password = "pw"
    receiver_email = "receiver-email-address"
    smtp_server = ""  # SMTP server for your email provider
    smtp_port = 587  # SMTP port for your email provider

    message = MIMEMultipart("alternative")
    message["Subject"] = "Quota Alert for CS 421-1"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = f"The quota for CS 421-1 is now {quota}. Act quickly to secure a spot."
    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully!")


def check_quota():
    url = "https://stars.bilkent.edu.tr/homepage/ajax/plainOfferings.php?COURSE_CODE=CS&SEMESTER=20232&submit=List%20Selected%20Offerings&rndval=1706614822162"

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        row = soup.find('td', text='CS 421-1').parent if soup.find('td', text='CS 421-1') else None

        while True:
            response = requests.get(url)
            print(response.status_code)
            soup = BeautifulSoup(response.content, 'html.parser')
            row = soup.find('td', text='CS 421-1').parent if soup.find('td', text='CS 421-1') else None



            if row:
                ##columns = row.find_all('td')
                ##quota_text = columns[9].get_text() if len(columns) > 9 else "Quota not found"
                quota_text = row.find_all('td')[-3].get_text()



                try:
                    quota = int(quota_text.strip())
                    if quota > 0:
                        print(f"Quota is more than 0, it's currently {quota}.")
                        send_email(quota)
                        os.system('afplay /System/Library/Sounds/Purr.aiff')

                        break
                    else:
                        print(f"Quota is not more than 0, it's currently {quota}.")
                        current_time = datetime.now()

                        # Print it in a specific format, for example: "Hour:Minute:Second"
                        print(current_time.strftime("%H:%M:%S"))
                except ValueError:
                    print(f"Quota value is not an integer: {quota_text}")
            else:
                print("CS 421-1 is not found in the table.")
            time.sleep(10)  # Wait for 1 second before making the next request


check_quota()
