import subprocess
import sys
import pandas as pd
import smtplib,ssl
from email.message import EmailMessage

#password = 'ZdzislawOgurekMM1'

class MemoryCheck():

    def run(self):
        threshold = 10
        child = subprocess.Popen(['df', '.'], stdout=subprocess.PIPE)
        output = child.communicate()[0].strip().decode('UTF-8').split("\n")
        output = output[1].split()
        self.memory = int((int(output[1]) - int(output[2]))/ 1000000)

        if self.memory < 10:
            self.send_email()

    def send_email(self):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "datalakenotifications@gmail.com"  # Enter your address
        receiver_email = "sebastian.placzek.af@gmail.com"
        #receiver_email = "p.kidawa@onnetwork.pl"
        password = "hsbgdstlbpzwbxjs"

        msg = EmailMessage()
        msg.set_content(f"Pozostala pamięć {self.memory}")
        msg['Subject'] = "Kończy się pamięć na GCP"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
            print('Send')