import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service as ChromeService





class OtodomScrapper():
    def __init__(self):
        self.name = 'GoodRobot'

    def init_driver(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--window-size=1600,900')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)

    def run(self):
        print('Robot zaczyna prace')
        self.init_driver()
        self.open_website('https://www.otodom.pl/')
        self.accept_cookies()
        self.chose_purpose()




        print('done')
        time.sleep(5)

    def open_website(self,website):
        self.driver.get(website)
        time.sleep(5)

    def accept_cookies(self):
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/button[1]').click()
        time.sleep(3)

    def chose_purpose(self,purpose='sell'):
        if purpose == 'rent':
            self.driver.find_element(By.XPATH,'/html/body/div/main/section/div/form/div/div/div[2]/div/div/div/div/div[2]').click()
            time.sleep(3)
            self.driver.find_element(By.XPATH,'html/body/div/main/section/div/form/div/div/div[2]/div/div/div/div[2]/div').click()
        # elif purpose == 'sell':
        #     self.driver.find_element(By.XPATH,'html/body/div/main/section/div/form/div/div/div[2]/div/div/div/div[2]/div/div').click()

        time.sleep(3)





