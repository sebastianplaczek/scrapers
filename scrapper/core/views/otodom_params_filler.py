import pdb

import bs4
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

import json


import pandas as pd
import requests
import sys
from datetime import datetime

from core.models import Otodom,OtodomLogs





class OtodomFiller():
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

        self.real_estate_filler('Mieszkania')

        print('done')
        time.sleep(5)
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

    def real_estate_filler(self,type):
        print(datetime.now)
        correct_params = False
        if type == 'Mieszkania':
            working = True

            while working== True:
                try:
                    offer = Otodom.objects.filter(filled=0).first()
                    if offer == None :
                        working= False
                    else:

                        self.init_driver()
                        print(offer.link)

                        self.open_website(f'https://www.{offer.link}')
                        #self.accept_cookies()

                        time.sleep(3)

                        html = self.driver.page_source
                        soup_before = BeautifulSoup(html, "html.parser")

                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(5)

                        html = self.driver.page_source
                        soup = BeautifulSoup(html, "html.parser")

                        params1 =  soup.find_all('div', {'class' : 'css-1ccovha estckra9'})
                        params2 = soup.find_all('div', {'class' : 'css-f45csg estckra9'})
                        address = soup.find('a', {'class' : 'e1nbpvi60 css-171pgf6 e1enecw71'}).text

                        categories = soup_before.find_all('a', {'class' : 'css-1in5nid e1je57sb4'})
                        if len(categories) == 0:
                            soup.find_all('a', {'class': 'css-1in5nid e1je57sb4'})

                        try:
                            vivodeship = categories[1].text
                        except Exception as e:
                            print(e)
                            vivodeship = ''
                        try:
                            city = categories[2].text
                        except Exception as e:
                            print(e)
                            city = ''


                        params1_dict = {}
                        for param in params1:
                            try:
                                value = param.find('div', {'class': 'css-1wi2w6s estckra5'}).text
                                params1_dict[f"{param['aria-label']}"] = value
                            except Exception as e:
                                value = ''
                                params1_dict[f"{param['aria-label']}"] = value
                                print(param)


                        params2_dict = {}
                        for param in params2:
                            try:
                                value = param.find('div', {'class': 'css-1wi2w6s estckra5'}).text
                                params2_dict[f"{param['aria-label']}"] = value
                            except Exception as e:
                                value = ''
                                params2_dict[f"{param['aria-label']}"] = value
                                print(param)

                        params1 = json.dumps(params1_dict)
                        params2 = json.dumps(params2_dict)


                        offer.additional_params_1 = params1
                        offer.additional_params_2 = params2
                        offer.city = city
                        offer.vivodeship = vivodeship
                        offer.filled = 1

                        if offer.address == None:
                            offer.address = address

                        offer.save()

                        print(f"{offer.link} : 'completed' ")






                        self.driver.close()
                        self.driver.quit()
                except Exception as e:
                    offer.filled = 2
                    offer.save()
                    OtodomLogs.objects.create(link=offer.link,
                                              type = type,
                                              error = str(e),
                                              robot='OtodomFiller')
                    self.driver.close()
                    self.driver.quit()
                    time.sleep(5)










