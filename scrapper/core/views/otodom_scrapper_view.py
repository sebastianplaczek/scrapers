import pdb

import bs4
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


import pandas as pd
import requests
import sys
import json
from datetime import datetime
import psutil

from core.models import Otodom,OtodomLogs,Workers






class OtodomScrapper():
    def __init__(self):
        self.name = 'GoodRobot'
        self.link = ''


    # def init_driver(self):
    #     firefox_options = Options()
    #     firefox_options.add_argument("--headless")
    #     firefox_options.add_argument('--disable-gpu')
    #     firefox_options.add_argument('--incognito')
    #     firefox_options.add_argument('--window-size=1600,900')
    #     firefox_options.add_argument('--no-sandbox')
    #     self.driver = webdriver.Firefox(options=firefox_options)
    #
    #     self.run_worker(type='enable')
    #     print('Driver inited')

    def init_driver(self):

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--window-size=1600,900')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)

        self.run_worker(type='enable')
        print('Driver inited')

    def kill_driver(self):
        # try:
        #     self.driver.close()
        # except Exception as e:
        #     print(e)
        # try:
        #     self.driver.quit()
        # except Exception as e:
        #     print(e)
        try:
            self.driver.service.process.terminate()
        except Exception as e:
            print(e)
        self.run_worker(type='disable')
        print('Driver killed')

    def run_worker(self,type):
        if type == 'enable':
            worker = Workers.objects.filter(active = 1,type='OtoFirefox').first()
            worker.number += 1
            print(f'Active workers {worker.number}')
            worker.save()
        elif type == 'disable':
            worker = Workers.objects.filter(active=1, type='OtoFirefox').first()
            worker.number -= 1
            print(f'Active workers {worker.number}')
            worker.save()
        else:
            print('workers error')
    def change_worker_activity(self,type,name):
        if type == 'enable':
            worker = Workers.objects.filter(active=0, type=name).first()
            worker.save()
        elif type == 'disable':
            worker = Workers.objects.filter(active=1, type=name).first()
            worker.save()
        else:
            print('workers error')

    def check_worker_activity(self,name):
        worker = Workers.objects.filter(type=name).first()
        print(worker.active)
        if worker.active == 1:
            return True
        elif worker.active == 0:
            return False
        else:
            print('Activity error')

    def check_memory(self):
        RAM_THRESHOLD = 14000
        if psutil.virtual_memory().used / (1024*1024) > RAM_THRESHOLD:
            print('Przekroczono próg zajętości pamięci')
            return False
        else:
            print('Pamieć wolna')
            return True




    def run(self):
        print('Robot zaczyna prace')
        self.real_estate_data('house pm')

        print('done')
        time.sleep(5)
    def test(self):

        # Iterate over all running process
        import psutil

        print('Start test')

        listOfProcessNames = list()
        # Iterate over all running processes
        for proc in psutil.process_iter():
            # Get process detail as dictionary
            if 'firefox' in proc.name() :
                time = datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S")
                print(proc.name(),proc.pid,time)



    def open_website(self,website):
        self.driver.get(website)
        time.sleep(5)
        print('Web opened')

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
        #self.change_worker_activity(type='enable',name='OtoScr')


        vivodeships = [
            'dolnoslaskie',
            'kujawsko--pomorskie',
            'lodzkie',
            'lubelskie',
            'lubuskie',
            'malopolskie',
            'mazowieckie',
            'opolskie',
            'podkarpackie',
            'podlaskie',
            'pomorskie',
            'slaskie',
            'swietokrzyskie',
            'warminsko--mazurskie',
            'wielkopolskie',
            'zachodniopomorskie',

        ]

        real_estate_links = {
            'house pm' : 'https://www.otodom.pl/pl/wyniki/sprzedaz/dom,rynek-pierwotny/$VIV$?distanceRadius=0&page=$PAGE_NR$&limit=72&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing',
            'flat pm' : 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie,rynek-pierwotny/$VIV$?distanceRadius=0&$PAGE_NR$&limit=72&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing'
        }


        for re_type in real_estate_links:
            print(re_type)
            for vivo in vivodeships:
                print(vivo)

                web = real_estate_links[re_type].replace('$VIV$',vivo)

                first_web = web.replace('$PAGE_NR$','1')
                print('Link created')
                print(first_web)
                print(datetime.now)
                correct_params = False

                number_of_offers = 75
                number_of_params = number_of_offers*4

                self.init_driver()
                self.open_website(first_web)
                self.accept_cookies()
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                try:

                    html = self.driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    buttons = soup.find_all('button', {'class': 'eo9qioj1 css-ehn1gc e1e6gtx31'})
                    number_of_pages = int(buttons[-2].text)
                    print(f'Number of pages {number_of_pages}')
                except Exception as e:
                    print(e)
                    number_of_pages = 3

                self.kill_driver()

                for i in range(1,number_of_pages+1):
                    print(f'{i}/{number_of_pages+1}')
                    try:

                        self.init_driver()
                        otomoto_link = web.replace('$PAGE_NR$',str(i))
                        print(otomoto_link)
                        self.open_website(otomoto_link)
                        print('Website opened')
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        print('Website scrolled down')
                        time.sleep(5)

                        html = self.driver.page_source
                        soup = BeautifulSoup(html, "html.parser")

                        offers = soup.find_all('li', {'class' : 'css-iq9jxc e1n6ljqa1'})
                        print('Number of offers in soup ' , len(offers))
                        if len(offers) == number_of_offers:
                            print('correct number of offers')
                            #import pdb;pdb.set_trace()
                            for j,offer in enumerate(offers):
                                #print('enumerating')
                                self.link ='otodom.pl' + offer.find('a', {'class' : 'css-1up0y1q e1n6ljqa3'})['href']
                                try:

                                    title = offer.find('h3', {'class' : 'css-qch36y e1ualqfi3'}).text
                                    #print('title')
                                except:
                                    title= None
                                try:
                                    address = offer.find('p', {'class' : 'css-14aokuk e1ualqfi4'}).text
                                    #print('address')
                                except:
                                    address = None
                                param = offer.find_all('span', {'class' : 'css-1on0450 ei6hyam2'})
                                #print('params')

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
                                    seller = offer.find('div', { 'class' : 'css-70qvj9 enzg89n0'}).text

                                except:
                                    try:
                                        seller = offer.find('span', {
                                            'class': ['css-1k08n8y enzg89n5']}).text
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
                                    type=re_type,
                                    seller = seller,
                                    filled = 0,
                                    page = i
                                )
                            self.kill_driver()



                    except Exception as e:
                        print(e)
                        OtodomLogs.objects.create(link=self.link,
                                                  type = type,
                                                  error = str(e),
                                              robot='OtodomScrapper')
                        self.kill_driver()

        #self.change_worker_activity(type='disable', name='OtoScr')

    def fill_params_from_link(self):

        if self.check_worker_activity(name='OtoScr') == False and self.check_memory():
            start_dt = datetime.now()
            ads = Otodom.objects.filter(filled=0)[:4]

            if len(ads)== 0:
                print('No offer')

            else:
                print('Filler zaczyna prace')
                for ad in ads:
                    ad.filled = 1
                    ad.save()

                for ad in ads:


                    self.init_driver()
                    print(ad.link)
                    #ad.link = 'otodom.pl/pl/oferta/mieszkanie-45-48-m2-kazimierz-ID4lK4P'

                    self.open_website('https://www.'+ ad.link)
                    print('Website opened')
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print('Website scrolled down')
                    time.sleep(5)

                    html = self.driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    inactive = soup.find_all('strong', {'class' : 'css-1flyc9m ercakuy1'})

                    if len(inactive) > 0:
                        ad.active = 0
                        ad.save()
                    else:
                        try:
                            bumped = soup.find_all('p', {'class':'css-1vd92mz ewcwyit0'})
                            if len(bumped)>0:
                                ad.bumped = 1
                        except Exception as e:
                            print(e,'bump error')




                        address_params = soup.find_all('a', {'class': 'css-1in5nid e19r3rnf1'})
                        address_params_dict = {}
                        for i,param in enumerate(address_params):
                            if i >0:
                                address_params_dict[i] = param.text
                        print(address_params_dict)

                        try:
                            city = address_params[2].text
                            vivodeship = address_params[1].text
                        except Exception as e:
                            city = ''
                            vivodeship = ''
                            print(e)


                        additional_params1 = soup.find_all('div', {'class': 'css-kkaknb enb64yk0'})
                        additional_params1_dict = {}
                        for param in additional_params1:
                            print('param1 iteration')
                            try:
                                title = param.find('div', {'class': 'css-rqy0wg enb64yk2'}).text

                            except Exception:
                                title = ''
                            try:
                                param_1 = param.find('div', {'class': 'css-1wi2w6s enb64yk4'}).text
                            except Exception:
                                param_1 = ''

                            additional_params1_dict[title] = param_1
                        print('param1')

                        additional_params2 = soup.find_all('div', {'class': 'css-1k2qr23 enb64yk0'})
                        additional_params2_dict = {}
                        for param in additional_params2:
                            print('param2 iteration')
                            try:
                                title = param.find('div', {'class': 'css-rqy0wg enb64yk2'}).text

                            except Exception:
                                title = ''
                            try:
                                param_1 = param.find('div', {'class': 'css-1wi2w6s enb64yk4'}).text
                            except Exception:
                                param_1 = ''

                            additional_params2_dict[title] = param_1
                        print('param2')


                        description = soup.find('div', {'class': 'css-1wekrze e1lbnp621'}).text

                        try:
                            prediction = soup.find('p', {'class' : 'css-aovmnt e1vfrca35'}).find_all('b')

                            additional_params2_dict['pred_val_min'] = prediction[0].text[:-3].replace("\xa0",'')
                            additional_params2_dict['pred_val_max'] = prediction[1].text[:-3].replace("\xa0", '')
                        except Exception as e:
                            print('No predictions')
                            print(e)

                        ad.additional_params_1 = json.dumps(additional_params1_dict)
                        ad.additional_params_2 = json.dumps(additional_params2_dict)
                        ad.address_params = json.dumps(address_params_dict)
                        ad.city = city
                        ad.vivodeship = vivodeship

                        ad.save()

                    self.kill_driver()
            end_dt = datetime.now()
            print(f'Time {(end_dt - start_dt).seconds}')














