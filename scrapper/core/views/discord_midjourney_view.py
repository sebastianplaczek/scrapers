import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import sys

import requests
import pyautogui

from datetime import datetime


PROMPT_PATH ='C:\\projects\\scrapers\\prompts\\'
PROMPT_FILENAME = 'prompts.xlsx'



class Midjourney():

    def __init__(self):
        self.topic = 'sea creatures'

    def init_driver(self):
        self.chrome_options = Options()
        #self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--incognito')
        self.chrome_options.add_argument('--window-size=1600,900')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.page_load_strategy = 'normal'

    def discord_run(self):
        self.init_driver()
        with webdriver.Chrome('C:\projects\chromedriver\chromedriver.exe',options=self.chrome_options) as self.driver:
            discord_link = 'https://discord.com/login'
            self.driver.get(discord_link)
            username = self.driver.find_element(By.CSS_SELECTOR,'input#uid_5.inputDefault-Ciwd-S.input-3O04eu.inputField-2RZxdl')
            username.send_keys('nikoletaisebastian@gmail.com')
            password = self.driver.find_element(By.CSS_SELECTOR,'input#uid_7.inputDefault-Ciwd-S.input-3O04eu')
            password .send_keys('FrancóskieOgurki1!')
            time.sleep(3)
            submit = self.driver.find_element(By.CSS_SELECTOR,'button.marginBottom8-emkd0_.button-1cRKG6.button-ejjZWC.lookFilled-1H2Jvj.colorBrand-2M3O3N.sizeLarge-2xP3-w.fullWidth-3M-YBR.grow-2T4nbg').click()
            time.sleep(5)
            self.driver.get('https://discord.com/channels/1136708220258361474/1136708220258361477')

            time.sleep(5)

            #read excel
            df = pd.read_excel(PROMPT_PATH + PROMPT_FILENAME)

            for i in range(0,df.shape[0]):
                if i ==0:
                    prompt = f'{datetime.now()}{self.topic}'

                    input = self.driver.find_element(By.CSS_SELECTOR,
                                                     'div.markup-eYLPri.editor-H2NA06.slateTextArea-27tjG0.fontSize16Padding-XoMpjI')
                    input.send_keys(f'{prompt}')
                    time.sleep(3)
                    pyautogui.press('enter')
                    time.sleep(5)
                size = ' --ar 17:22 --v 5'
                prompt = df.loc[i,'prompt'] + size

                input = self.driver.find_element(By.CSS_SELECTOR,
                                         'div.markup-eYLPri.editor-H2NA06.slateTextArea-27tjG0.fontSize16Padding-XoMpjI')
                input.send_keys(f'{prompt}')
                time.sleep(3)
                # Wprowadź treść wiadomości

                # Wciśnij klawisz Enter
                pyautogui.press('enter')
                print(i+1)
                time.sleep(5)




    def run(self):
        self.discord_run()



    def run_bot(self):
        url = 'https://discord.com/api/v9/channels/1008571069797507102/messages'
        auth = {
            'authorization' : 'MTEzNTI5ODE4Njc3MzI3NDc3Ng.G14wQQ.iOzB1fWpzcXsWzmZbzVtkMAi3YMq5yT55HPOJ4'
        }

        msg = {
            'content' : '/imagine prompt: coloring page for kids, submarine exploring the ocean depths , no shading,low detail – ar 9:11 –v 5'
        }
        requests.post(url,headers=auth,data=msg)






