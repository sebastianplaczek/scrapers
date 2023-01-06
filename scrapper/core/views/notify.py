import subprocess
import sys
import pandas as pd
import smtplib,ssl
from email.message import EmailMessage

#password = 'ZdzislawOgurekMM1'

class Notify():

    def run(self):
        self.send_email()

    def send_email(self):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "datalakenotifications@gmail.com"  # Enter your address
        receiver_email = "sebastian.placzek.af@gmail.com"
        receiver_email = "p.kidawa@onnetwork.pl"
        password = "hsbgdstlbpzwbxjs"

        msg = EmailMessage()
        msg.set_content("Notification")
        msg['Subject'] = "Testowy mail dla pientaszka"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
            print('Send')