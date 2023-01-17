import pdb

import bs4
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


import pandas as pd
import requests
import sys
from datetime import datetime

from core.models import Otodom,OtodomLogs





class OtodomScrapper():
    def __init__(self):
        self.name = 'GoodRobot'
        self.link = ''


    def init_driver(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--incognito')
        firefox_options.add_argument('--window-size=1600,900')
        firefox_options.add_argument('--no-sandbox')
        self.driver = webdriver.Firefox(options=firefox_options)

    def run(self):
        print('Robot zaczyna prace')
        self.init_driver()
        self.real_estate_data('Mieszkania')

        print('done')
        time.sleep(5)
    def test(self):
        teraz = datetime.now()
        self.init_driver()
        self.driver.get('https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?market=ALL&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie&page=1&limit=72')
        #self.accept_cookies()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        titles = soup.find_all('h3', {'class' : 'css-1rhznz4 es62z2j12'})
        links = soup.find_all('a', {'class' : 'css-13ki2r1 es62z2j16'})
        params = soup.find_all('span',{'class' : 'css-s8wpzb e1brl80i1'})
        addresses = soup.find_all('h3', {'class' : 'css-1rhznz4 es62z2j12'})
        sellers = soup.find_all('span', {'class' : ['css-4pyl2y e1dxhs6v3','css-16zp76g e1dxhs6v2']})
        print(len(titles),len(links),len(params),len(addresses),len(sellers))
        self.driver.close()
        self.driver.quit()
        teraz1 = datetime.now()
        print(teraz1-teraz)


    def open_website(self,website):
        self.driver.get(website)
        time.sleep(5)

    def accept_cookies(self):
        try:
            self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/button[1]').click()
        except:
            print('No cookies')

        time.sleep(5)

    def find_error_letter(self,my_str):
        x = ''
        for x in my_str:
            try:
                int(x)
            except:
                break
        return x

    def real_estate_data(self,type):
        print(datetime.now)
        correct_params = False
        if type == 'Mieszkania':
            limit = 72
            number_of_offers = 75
            number_of_params = number_of_offers*4

            self.open_website(f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?market=ALL&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie&page=1&limit={limit}')
            self.accept_cookies()
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            number_of_pages = int(self.driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div[2]/main/div/div[2]/div[1]/div[4]/div/nav/button[5]').get_attribute('aria-label').split(' ')[-1])
            print(f'Number of pages {number_of_pages}')
            self.driver.close()
            self.driver.quit()

            for i in range(1,number_of_pages+1):
                try:




                    self.init_driver()
                    print('Driver inited')
                    otomoto_link = f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?market=ALL&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie&page={i}&limit={limit}'
                    print(otomoto_link)
                    self.open_website(otomoto_link)
                    print('Website opened')
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print('Website scrolled down')
                    time.sleep(5)

                    html = self.driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    offers = soup.find_all('li', {'class' : 'css-p74l73 es62z2j20'})

                    print('Number of offers in soup ' , len(offers))
                    if len(offers) == number_of_offers:

                        for j,offer in enumerate(offers):
                            self.link ='otodom.pl' + offer.find('a', {'class' : 'css-13ki2r1 es62z2j16'})['href']
                            try:
                                title = offer.find('h3', {'class' : 'css-1rhznz4 es62z2j12'}).text
                            except:
                                title= None
                            try:
                                address = offer.find('span', {'class' : 'css-17o293g es62z2j10'}).text
                            except:
                                address = None

                            param = offer.find_all('span', {'class' : 'css-s8wpzb e1brl80i1'})

                            bad_character = self.find_error_letter(param[0].text[:-2])
                            try:
                                price = float(param[0].text.replace(bad_character,"")[:-2])
                            except:
                                price = None
                            try:
                                price_per_m = int(param[1].text[:-5].replace(bad_character,''))
                            except:
                                price_per_m = None
                            try:
                                rooms = int(param[2].text.split(' ')[0])
                            except:
                                rooms = None
                            try:
                                size = float(param[3].text.split(' ')[0])
                            except:
                                size = None



                            try:
                                seller = offer.find('span', {'class' : ['css-16zp76g e1dxhs6v2','css-4pyl2y e1dxhs6v3']}).text
                            except:
                                seller = None

                            Otodom.objects.create(
                                link=self.link,
                                title=title,
                                address=address,
                                price=price,
                                price_per_m=price_per_m,
                                rooms=rooms,
                                size=size,
                                type='flat',
                                seller = seller,
                                filled = 0
                            )
                        self.driver.close()
                        self.driver.quit()

                        print(f'{offer.link : 'completed'}')

                except Exception as e:
                    OtodomLogs.objects.create(link=self.link,
                                              type = type,
                                              error = str(e),
                                          robot='OtodomScrapper')
                    self.driver.close()
                    self.driver.quit()










