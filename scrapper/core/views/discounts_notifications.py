import subprocess
import sys
import pandas as pd
import smtplib,ssl
from email.message import EmailMessage

from core.models import UsersLinks,DailyScraps,LinksToScrap

from django.contrib.auth.models import User
from datetime import datetime


#password = 'ZdzislawOgurekMM1'

class Notify():

    def __init__(self):
        self.today = datetime.today().strftime('%Y-%m-%d')

    def run(self):
        users = User.objects.all()
        for user in users:
            self.check_prices(user.id)

    def check_prices(self,user_id):
        user = User.objects.get(id=user_id)
        self.email_address = user.email
        user_links = UsersLinks.objects.filter(active=1,user=user)
        for user_link in user_links:
            print(user_link.conditional_price)
            daily = DailyScraps.objects.filter(linktoscrap=user_link.linktoscrap,create_date__gte=self.today).first()
            print(daily.discount_price,daily.price)
            print(user_link.conditional_price)

            if daily.discount_price:
                self.price = daily.discount_price
            else:
                self.price = daily.price
            if self.price <= user_link.conditional_price:
                self.send_email('Powiadomienie o zmianie ceny obserwowanego produktu',
                                f'Cena produktu {user_link.linktoscrap.item_name} to obecnie {self.price} . Sprawdz teraz {user_link.linktoscrap.link}')






    def send_email(self,email_subject,content):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = 'datalakenotifications@gmail.com'
        receiver_email = self.email_address
        password = "hsbgdstlbpzwbxjs"

        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = email_subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
            print('Send')