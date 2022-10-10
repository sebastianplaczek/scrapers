from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import sys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from django.utils import timezone

from core.models import ReservedToScrap,ReservedDailyScraps,ReservedLogs,ServicesErrors




class ReservedScrapRobot():

    def init_driver_firefox(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--incognito')
        firefox_options.add_argument('--window-size=1600,900')
        firefox_options.add_argument('--no-sandbox')
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)

    def run(self,endpoint):
        self.init_driver_firefox()
        #self.inactive_site_error_check()
        self.endpoint = endpoint
        self.item_to_scrap = ReservedToScrap.objects.get(active=True, endpoint=self.endpoint)

        print(self.endpoint)

        self.open_website()
        self.check_price_by_css_selector()
        if self.item_to_scrap.active == True:
            self.save_to_db()
        self.driver.close()


        print('done')
        time.sleep(5)

    def open_website(self):
        self.driver.get(self.endpoint)
        time.sleep(5)
        self.accept_cookies()
    def accept_cookies(self):
        try:
            self.driver.find_element(By.XPATH,'/html/body/div/div[3]/div/div/button[2]').click()
        except Exception as e:
            print(e)
        time.sleep(5)

    def check_price_by_css_selector(self):
        try:
            #element = self.driver.find_element(By.XPATH,'/html/body/div[2]/section/div[2]/div/div/section/section[3]/div/div/div/div[1]')
            element = self.driver.find_element(By.CSS_SELECTOR, 'div.basic-pricestyled__StyledBasicPrice-ptbrpf-0.dhHSLU.basic-price.promo-price')

            self.price = element.text.replace(',','.').split(' ')[0]
            print(self.price)
            sys.exit()
            time.sleep(1)
        except Exception as e1:
            print(e1)
            sys.exit()
            self.price=None
            # jezeli nie znajdzie elementu to ma zapisac w logach i zmienic status
            try:
                element = self.driver.find_element(By.XPATH,
                                                   '/html/body/div/div[29]/section[9]/h1').text
                if element=='Wystąpił błąd':
                    print('Inactive endpoint')
                    ZalandoLogs.objects.create(toscrap=self.item_to_scrap,error='Endpoint nieaktywny')
                    # zmiana statusu na inactive
                    self.item_to_scrap.active = False
                    self.item_to_scrap.deactivate_date = datetime.now()
                    self.item_to_scrap.save()



            except Exception as e2:
                print(e2)
                ZalandoLogs.objects.create(toscrap=self.item_to_scrap, error='Other error',content=e2)
                #zapisac do bazy jako inny blad na stronie

    def inactive_site_error_check(self):
        self.endpoint = 'https://www.reserved.com/pl/pl/some-item'
        self.open_website()
        element = self.driver.find_element(By.XPATH,'/html/body/div[2]/section/div/div/h2').text
        if element != 'Przepraszamy, ta strona nie istnieje.':
            ServicesErrors.objects.create(service_name='Reserved', error='Not found zmieniło swoje miejsce w strukturze')
        else:
            print('Error correct')
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
        ReservedDailyScraps.objects.create(price=self.price,toscrap=self.item_to_scrap)



