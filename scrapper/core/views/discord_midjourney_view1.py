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

import discord
from discord.ext import commands





class Midjourney():

    def handle_response(self,message):
        if message == 'hello':
            return 'Hi there!'

    async def send_message(self,message,user_message):
        try:
            response = self.handle_response(user_message)
            await message.channel.send(response)
        except Exception as e:
            print(e)

    def run(self):

        subfolder_name = 'exotic_animals'
        intents = discord.Intents.default()
        intents.message_content = True

        # Tworzenie klienta bota
        bot = commands.Bot(command_prefix='!', intents=intents)

        # Event wywoływany przy uruchamianiu bota
        @bot.event
        async def on_ready():
            print(f'Zalogowano jako {bot.user.name}')

        # Event wywoływany przy otrzymaniu nowej wiadomości na kanale
        @bot.event
        async def on_message(message):
            if message.author == bot.user:  # Bot nie będzie reagował na swoje wiadomości
                return

            if str(message.author) == 'Midjourney Bot#9282' and 'Image #' in str(message.content):
                print('Midjourney bot try save')
                if message.attachments:
                    for attachment in message.attachments:
                        await attachment.save(f"C:\\Users\\sebas\\OneDrive\\Obrazy\\midjourney\\{subfolder_name}\\{attachment.filename}")
                        print(f'Pobrano załącznik: {attachment.filename}')

            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)


            print(username)
            print(user_message)
            print(channel)



            await self.send_message(message,user_message)

        @bot.command()
        async def load_history(ctx):
            message_history = []
            async for message in ctx.channel.history(limit=None, oldest_first=True):
                message_history.append(message.content)
                print(message_history)

        @bot.event
        async def on_button_click(interaction):
            for component in interaction.message.components:
                print(component)
                if isinstance(component, discord.ui.Button) and component.custom_id == interaction.custom_id:
                    await interaction.response.send_message(f'Kliknięto przycisk o custom_id: {interaction.custom_id}',
                                                            ephemeral=True)
                    break


        # Token bota - wymaga zastąpienia własnym tokenem
        bot_token = 'MTEzNTU3ODMzNDQwNzk1MDM4Ng.G8OMM0.U_4i6qpko_fV-xhw1Q6HmvL-3w-_hvxzv2qqho'
        bot.run(bot_token)







