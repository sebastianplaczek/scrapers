from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import sys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from django.utils import timezone

from core.models import MohitoToScrap,MohitoDailyScraps,MohitoLogs,ServicesErrors




class MohitoScrapRobot():

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
        self.endpoint = endpoint
        self.item_to_scrap = MohitoToScrap.objects.get(active=True, endpoint=self.endpoint)

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
        time.sleep(3)
    def accept_cookies(self):
        try:
            self.driver.find_element(By.XPATH,'/html/body/div/div/div/div/button[2]').click()
        except Exception as e:
            print('No cookies')
        time.sleep(5)
    def close_newsletter_banner(self):
        try:
            self.driver.find_element(By.XPATH,'html/body/div[5]/div/button').click()
        except Exception as e:
            print('No banner')
        time.sleep(5)

    def check_price_by_css_selector(self):
        try:

            element = self.driver.find_element(By.CSS_SELECTOR, 'div.basic-pricestyled__StyledBasicPrice-sc-6u579m-0.bWLuLL.basic-price.promo-price')
            self.discount_price = element.text.replace(',','.').split(' ')[0]
            print('discount_price',self.discount_price)
            time.sleep(1)

            element = self.driver.find_element(By.CSS_SELECTOR,
                                               'div.basic-pricestyled__StyledBasicPrice-sc-6u579m-0.bWLuLL.basic-price.old-price')
            self.price = element.text.replace(',', '.').split(' ')[0]
            print('price', self.price)
            time.sleep(1)


        except Exception as e:
            print('Nie znaleziono ceny promocyjnej')
            self.discount_price = None
            try:
                element = self.driver.find_element(By.CSS_SELECTOR,
                                                   'div.basic-pricestyled__StyledBasicPrice-sc-6u579m-0.bWLuLL.basic-price')

                self.price = element.text.replace(',', '.').split(' ')[0]
                print('price', self.price)
                time.sleep(1)


            except Exception as e:
                print(e1)
                self.price=None
                self.discount_price = None

                # jezeli nie znajdzie elementu to ma zapisac w logach i zmienic status
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR,'div.centered.error-page-404').text

                    if 'BŁĄD 404' in element:
                        print('Inactive endpoint')
                        MohitoLogs.objects.create(toscrap=self.item_to_scrap,error='Endpoint nieaktywny')
                        # zmiana statusu na inactive
                        self.item_to_scrap.active = False
                        self.item_to_scrap.deactivate_date = datetime.now()
                        self.item_to_scrap.save()



                except Exception as e2:
                    print(e2)
                    MohitoLogs.objects.create(toscrap=self.item_to_scrap, error='Other error',content=e2)
                    #zapisac do bazy jako inny blad na stronie

    def inactive_site_error_check(self):
        self.init_driver_firefox()
        self.endpoint = 'https://www.mohito.com/pl/pl/some-item'
        self.open_website()
        element = self.driver.find_element(By.CSS_SELECTOR,'div.centered.error-page-404').text



        if 'BŁĄD 404' not in element:
            ServicesErrors.objects.create(service_name='Mohito', error='Not found zmieniło swoje miejsce w strukturze')
            self.correct_structure= False
        else:
            self.correct_structure = True


    def save_to_db(self):
        MohitoDailyScraps.objects.create(discount_price=self.discount_price,price=self.price,toscrap=self.item_to_scrap)



