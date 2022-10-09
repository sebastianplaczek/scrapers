from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests as r
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService


from core.models import ZalandoToScrap,ZalandoDailyScraps




class ZalandoScrapRobot():


    def init_driver_firefox(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--incognito')
        firefox_options.add_argument('--window-size=1600,900')
        firefox_options.add_argument('--no-sandbox')
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)

    def run(self,endpoint):
        self.endpoint = endpoint
        print(self.endpoint)
        self.check_request()
        self.init_driver_firefox()
        self.open_website()
        #self.accept_cookies()
        self.check_price_by_path()
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
        except Exception as e:
            self.price=None
            print(e)

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
        item_to_scrap = ZalandoToScrap.objects.get(active=True,endpoint=self.endpoint)

        ZalandoDailyScraps.objects.create(price=self.price,zalandotoscrap=item_to_scrap)

    def check_request(self,endpoint):
        print(r.get(endpoint))


