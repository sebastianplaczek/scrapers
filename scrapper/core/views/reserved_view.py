from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import sys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from django.utils import timezone

from webdriver_manager.firefox import GeckoDriverManager


from core.models import LinksToScrap,DailyScraps,ServicesLogs,ServicesErrors




class ReservedScrapRobot():

    def init_driver_firefox(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--incognito')
        firefox_options.add_argument('--window-size=1600,900')
        firefox_options.add_argument('--no-sandbox')
        self.driver = webdriver.Firefox(options=firefox_options)

    def run(self,link):
        self.init_driver_firefox()
        self.link = link
        self.item_to_scrap = LinksToScrap.objects.get(active=True, link=self.link)

        print(self.link)

        self.open_website()
        self.check_price_by_css_selector()
        if self.item_to_scrap.active == True:
            self.save_to_db()
        self.driver.close()


        print('done')
        time.sleep(5)

    def open_website(self):
        self.driver.get(self.link)
        time.sleep(5)
        self.accept_cookies()
    def accept_cookies(self):
        try:
            self.driver.find_element(By.XPATH,'/html/body/div/div[3]/div/div/button[2]').click()
        except Exception as e:
            print('No cookies')
        time.sleep(5)

    def check_price_by_css_selector(self):
        try:
            self.item_name = self.driver.find_element(By.CSS_SELECTOR, 'h1.product-name').text

        except Exception as e:
            self.item_name = None
            print(e)

        print('Item name',self.item_name)

        try:
            element = self.driver.find_element(By.CSS_SELECTOR, 'div.basic-pricestyled__StyledBasicPrice-ptbrpf-0.dhHSLU.basic-price.promo-price')
            self.discount_price = element.text.replace(',','.').split(' ')[0]
            print('discount_price',self.discount_price)
            time.sleep(1)

            element = self.driver.find_element(By.CSS_SELECTOR,
                                               'div.basic-pricestyled__StyledBasicPrice-ptbrpf-0.dhHSLU.basic-price.old-price')
            self.price = element.text.replace(',', '.').split(' ')[0]
            print('price', self.price)
            time.sleep(1)


        except Exception as e:
            print(e)
            print('Nie znaleziono ceny promocyjnej')
            self.discount_price = None
            try:
                element = self.driver.find_element(By.CSS_SELECTOR,
                                                   'div.basic-pricestyled__StyledBasicPrice-ptbrpf-0.dhHSLU.basic-price')

                self.price = element.text.replace(',', '.').split(' ')[0]
                print('price', self.price)
                time.sleep(1)


            except Exception as e1:
                print(e1)
                self.price=None
                self.discount_price = None

                # jezeli nie znajdzie elementu to ma zapisac w logach i zmienic status
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR,'div.search-empty').text.split('.')[0]
                    if element=='Przepraszamy, ta strona nie istnieje':
                        print('Nieaktywny link')
                        ServicesLogs.objects.create(linktoscrap=self.item_to_scrap,error='Link nieaktywny')
                        # zmiana statusu na inactive
                        self.item_to_scrap.active = False
                        self.item_to_scrap.deactivate_date = datetime.now()
                        self.item_to_scrap.save()



                except Exception as e2:
                    print(e2)
                    ServicesLogs.objects.create(service='reserved',linktoscrap=self.item_to_scrap, error='Other error',content=e2)
                    #zapisac do bazy jako inny blad na stronie

    def inactive_site_error_check(self):
        self.init_driver_firefox()
        self.link = 'https://www.reserved.com/pl/pl/some-item'
        self.open_website()
        element = self.driver.find_element(By.CSS_SELECTOR,'div.search-empty').text
        #element = self.driver.find_element(By.XPATH,'/html/body/div[2]/section/div/div/h2').text


        if element.split('.')[0] != 'Przepraszamy, ta strona nie istnieje':
            ServicesErrors.objects.create(service_name='Reserved', error='Not found zmieniło swoje miejsce w strukturze')
            self.correct_structure= False
        else:
            self.correct_structure = True


    def save_to_db(self):
        DailyScraps.objects.create(discount_price=self.discount_price,price=self.price,linktoscrap=self.item_to_scrap)



