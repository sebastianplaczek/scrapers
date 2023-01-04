from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import sys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from django.utils import timezone

from core.models import LinksToScrap,DailyScraps,ServicesLogs,ServicesErrors
#from core.models import ZalandoToScrap,ZalandoDailyScraps,ZalandoLogs,ServicesErrors




class ZalandoScrapRobot():

    def init_driver_firefox(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--incognito')
        firefox_options.add_argument('--window-size=1600,900')
        firefox_options.add_argument('-ox_options.add_argument('--no-sandbox')
        self.driver = webdriver.Firefox(options=firefox_options)

    def run(self,endpoint):
        self.init_driver_firefox()
        self.inactive_site_error_check()
        self.endpoint = endpoint
        self.item_to_scrap = ZalandoToScrap.objects.get(active=True, endpoint=self.endpoint)

        print(self.endpoint)

        self.open_website()
        #self.accept_cookies()
        self.check_price_by_path()
        if self.item_to_scrap.active == True:
            self.save_to_db()
        self.driver.close()


        print('done')
        time.sleep(5)

    def open_website(self):
        self.driver.get(self.endpoint)
        time.sleep(5)
    def accept_cookies(self):
        try:
            self.driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/button[1]').click()
        except Exception as e:
            print(e)
        time.sleep(5)

    def check_price_by_path(self):
        try:
            element = self.driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/x-wrapper-re-1-4/div[1]/div[2]/div[1]/div[1]/div[1]/p')
            element = element.text.replace(',','.')
            element_list = element.split(' ')
            self.find_price(element_list)
            time.sleep(1)
        except Exception as e1:
            self.price=None
            # jezeli nie znajdzie elementu to ma zapisac w logach i zmienic status
            try:
                element = self.driver.find_element(By.XPATH,
                                                   '/html/body/div/div[29]/section[9]/h1').text
                if element=='Wystąpił błąd':
                    print('Inactive endpoint')
                    ZalandoLogs.objects.create(zalandotoscrap=self.item_to_scrap,error='Endpoint nieaktywny')
                    # zmiana statusu na inactive
                    self.item_to_scrap.active = False
                    self.item_to_scrap.deactivate_date = datetime.now()
                    self.item_to_scrap.save()



            except Exception as e2:
                print(e2)
                ZalandoLogs.objects.create(zalandotoscrap=self.item_to_scrap, error='Other error',content=e2)
                #zapisac do bazy jako inny blad na stronie

    def inactive_site_error_check(self):
        self.endpoint = 'https://www.zalando.pl/some-product'
        self.open_website()
        element = self.driver.find_element(By.XPATH,'/html/body/div[2]/div[29]/section[9]/h1').text
        if element != 'Wystąpił błąd':
            ServicesErrors.objects.create(service_name='Zalando', error='Not found zmieniło swoje miejsce w strukturze')

    # def check_price_by_class(self):
    #     #not working on zalando
    #     try:
    #         #element = self.driver.find_element(By.XPATH,'_0Qm8W1uqkIZwdgII7d_88STHx')
    #         #element = self.driver.find_element(By.CSS_SELECTOR, "._0Qm8W1.uqkIZw.dgII7d._88STHx")
    #         # element = self.driver.find_element(By.CLASS_NAME,'_0Qm8W1uqkIZwdgII7d_88STHx')
    #
    #         print(f'Class search price : {element.text}')
    #         time.sleep(1)
    #     except Exception as e:
    #         print(e)

    def find_price(self,list):
        self.price_list = []
        for elem in list:
            try:
                self.price_list.append(float(elem))
            except Exception as e:
                pass
        if len(self.price_list)>0:
            self.price = self.price_list[0]
        else:
            self.price = None

    def save_to_db(self):
        ZalandoDailyScraps.objects.create(price=self.price,zalandotoscrap=self.item_to_scrap)



