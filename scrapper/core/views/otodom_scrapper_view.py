

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

from core.models import Otodom,OtodomLogs,Workers,Otodom_fills




class MyCustomError(Exception):
    pass

class OtodomScrapper():
    def __init__(self):
        self.name = 'GoodRobot'
        self.link = ''
        self.save = True


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

        self.chrome_options = Options()
        #self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--incognito')
        self.chrome_options.add_argument('--window-size=1600,900')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.page_load_strategy = 'normal'
        #self.driver = webdriver.Chrome(options=chrome_options)

        #self.run_worker(type='enable')
        print('Driver inited')

    def kill_driver(self):
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
            worker.active = 1
            worker.save()
            print('Worker enabled')
        elif type == 'disable':
            worker = Workers.objects.filter(active=1, type=name).first()
            worker.active = 0
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
        RAM_THRESHOLD = 8000
        if psutil.virtual_memory().used / (1024*1024) > RAM_THRESHOLD:
            print(f'Przekroczono próg zajętości pamięci, {psutil.virtual_memory().used}')
            return False
        else:
            print(f'Pamieć wolna, zajete {psutil.virtual_memory().used}')
            return True




    def run(self):
        print('Robot zaczyna prace')

        self.change_worker_activity(type='enable', name='OtoScr')
        import pdb;
        self.real_estate_data()

        print('done')
        self.change_worker_activity(type='disable', name='OtoScr')
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

    def real_estate_data(self):

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
            'flat pm' : 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie,rynek-pierwotny/$VIV$?distanceRadius=0&2=&limit=72&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing&page=$PAGE_NR$',
            'plot' : 'https://www.otodom.pl/pl/wyniki/sprzedaz/dzialka/$VIV$?distanceRadius=0&limit=72&by=DEFAULT&direction=DESC&viewType=listing&page=$PAGE_NR$',
            'flat sm' : 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie,rynek-wtorny/$VIV$?ownerTypeSingleSelect=ALL&distanceRadius=0&by=DEFAULT&direction=DESC&viewType=listing&limit=72&page=$PAGE_NR$',
            'house sm' : 'https://www.otodom.pl/pl/wyniki/sprzedaz/dom,rynek-wtorny/$VIV$?distanceRadius=0&limit=72&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing&page=$PAGE_NR$'

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


                with webdriver.Chrome(options=self.chrome_options) as self.driver:
                    self.open_website(first_web)
                    #self.accept_cookies()
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)
                    try:

                        html = self.driver.page_source
                        soup = BeautifulSoup(html, "html.parser")
                        buttons = soup.find_all('a', {'class': 'eo9qioj1 css-5tvc2l edo3iif1'})
                        number_of_pages = int(buttons[-1].text)
                        print(f'Number of pages {number_of_pages}')
                    except Exception as e:
                        print(e)
                        number_of_pages = 3

                self.links = []
                test_df = pd.DataFrame()
                for i in range(1,number_of_pages+1):
                    print('df shape',test_df.shape[0])
                    print((i-1)*number_of_offers,len(set(self.links)))
                    print(f'pages {i}/{number_of_pages+1}')
                    try:

                        self.init_driver()
                        for r in range(0,5):
                            print(f'Repeat loop {r}')
                            try:
                                with (webdriver.Chrome(options=self.chrome_options) as self.driver):

                                    otomoto_link = web.replace('$PAGE_NR$',str(i))
                                    print(otomoto_link)
                                    self.open_website(otomoto_link)
                                    print('Website opened')
                                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                    print('Website scrolled down')
                                    time.sleep(5)

                                    html = self.driver.page_source
                                    soup = BeautifulSoup(html, "html.parser")

                                    offers = soup.find_all('li', {'class' : ['css-o9b79t e1dfeild0',
                                                                                        'css-rpzu07 e1o4jl71']})
                                    awarded_offers = soup.find_all('a', {'class' : 'css-5xrhwq e1symgi0'})

                                    print('Number of offers in soup ' , len(offers),len(awarded_offers))

                                    if len(offers) >= 0:
                                    #or i==number_of_pages+1:
                                        print('correct number of offers')
                                        #import pdb;pdb.set_trace()


                                        for j,offer in enumerate(offers):
                                            #print('enumerating')
                                            try:
                                                self.link ='otodom.pl' + offer.find('a', {'class' : ['css-1tiwk2i e1dfeild2','css-dc6cnc e1o4jl75']})['href']


                                                try:

                                                    title = offer.find('div', {'class' : 'css-gg4vpm e1n06ry51'}).text
                                                    #print('title')
                                                except:
                                                    title= None
                                                    print(j,'no title')
                                                try:
                                                    address = offer.find('p', {'class' : 'css-19dkezj e1n06ry53'}).text
                                                    #print('address')
                                                except:
                                                    address = None
                                                    print(j, 'no address')

                                                param = offer.find_all('span', {'class' : 'css-1cyxwvy ei6hyam2'})
                                                #print('params')

                                                bad_character = self.find_error_letter(param[0].text[:-2])
                                                try:
                                                    price = float(param[0].text.replace(bad_character,"")[:-2])
                                                except:
                                                    price = None
                                                    print(j, 'no price')
                                                try:
                                                    price_per_m = int(param[1].text[:-5].replace(bad_character,''))
                                                except:
                                                    price_per_m = None
                                                    print(j, 'no price per m')
                                                try:
                                                    rooms = int(param[2].text.split(' ')[0])
                                                except:
                                                    rooms = None
                                                    print(j, 'no rooms')
                                                try:
                                                    size = float(param[3].text.split(' ')[0])
                                                except:
                                                    size = None
                                                    print(j, 'no size')



                                                try:
                                                    seller = offer.find('div', { 'class' : 'css-70qvj9 enzg89n0'}).text

                                                except:
                                                    try:
                                                        seller = offer.find('span', {
                                                            'class': ['css-6luqt7 enzg89n4']}).text
                                                    except:

                                                        seller = None


                                                print(f'before save duplikat : {self.link in self.links}')
                                                if self.save== True and self.link not in self.links:
                                                    object = Otodom.objects.create(
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
                                                        page = i,
                                                        vivodeship = vivo
                                                    )
                                                    self.links.append(object.link)
                                                    test_df.loc[test_df.shape[0]+1,['link','title','address','price','price_per_m','rooms','size',
                                                                                    'type','seller','filled','page']] = [self.link,title,address,price,
                                                                                                                         price_per_m,rooms,size,re_type,
                                                                                                                      seller,0,i]
                                                    print(f'save {j}')





                                            except Exception as e:
                                                print(e)
                                                print(j,'Error with link')
                                                #import pdb; pdb.set_trace()
                                    else:
                                        print('incorrect number of offers')
                                        raise MyCustomError("Błedna ilość ofert, powtarzam pętle")

                                break
                            except Exception as e:
                                print(e)
                                print('Session error,wait 30s')
                                #import pdb;pdb.set_trace()
                                time.sleep(30)
                        #import pdb;pdb.set_trace()

                    except Exception as e:
                        print(e)
                        OtodomLogs.objects.create(link=self.link,
                                                  type = type,
                                                  error = str(e),
                                              robot='OtodomScrapper')
                        self.change_worker_activity(type='disable', name='OtoScr')



    def fill_params_from_link(self):
        self.sample_size = 10
        if self.check_worker_activity(name='OtoScr') == False and self.check_memory():
            start_dt = datetime.now()
            ads = Otodom.objects.filter(filled=0)[:self.sample_size]

            if len(ads)== 0:
                print('No offer')

            else:
                print('Filler zaczyna prace')
                for ad in ads:
                    ad.filled = 1
                    ad.save()

                self.init_driver()
                for index,ad in enumerate(ads):

                    duplicate = Otodom_fills.objects.filter(link=ad.link)


                    print(f'Dup len {len(duplicate)}')
                    if len(duplicate) ==1:
                        print(duplicate[0].link)
                    if len(duplicate)==0:

                        print(f'{index}/{self.sample_size} New record {ad.id}')
                        #import pdb;pdb.set_trace()
                        with webdriver.Chrome(options=self.chrome_options) as self.driver:

                            print(ad.id,ad.link)
                            #ad.link = 'otodom.pl/pl/oferta/mieszkanie-45-48-m2-kazimierz-ID4lK4P'
                            if ad.link[:17] == 'otodom.plhttps://':
                                ad.link = ad.link[17:]
                                print(ad.id,'Link edited', ad.link)
                            self.open_website('https://www.'+ ad.link)
                            print('Website opened')
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            print('Website scrolled down')

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


                                #description = soup.find('div', {'class': 'css-1wekrze e1lbnp621'}).text

                                try:
                                    prediction = soup.find('p', {'class' : 'css-aovmnt e1vfrca35'}).find_all('b')

                                    additional_params2_dict['pred_val_min'] = prediction[0].text[:-3].replace("\xa0",'')
                                    additional_params2_dict['pred_val_max'] = prediction[1].text[:-3].replace("\xa0", '')
                                except Exception as e:
                                    print('No predictions')
                                    print(e)

                                print('Params added')



                                Otodom_fills.objects.create(
                                    link=ad.link,
                                    additional_params_1=json.dumps(additional_params1_dict),
                                    additional_params_2=json.dumps(additional_params2_dict),
                                    address_params=json.dumps(address_params_dict),
                                    city=city,
                                    vivodeship=vivodeship
                                )
                                print('Save params')
                            #self.kill_driver()
                    else:
                        print(f'{index}/{self.sample_size}  Duplicate {ad.id}')
            end_dt = datetime.now()
            print(f'Time {(end_dt - start_dt).seconds}')














