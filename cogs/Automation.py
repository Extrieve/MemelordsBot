# -*- coding: utf-8 -*-

from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import discord

class Automation(commands.Cog):
    """Cog for automation purposes with Selenium and Beautiful Soup."""

    service = Service(r'C:\Selenium\chromedriver_win32\chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    def __init__(self, bot):
        self.bot = bot


    # twitter video downloader
    @commands.command(name='twitter-video', aliases=['twitter-vid'])
    async def twitter_video(self, ctx, url):
        """Download a Twitter video"""
        if not url:
            return await ctx.send('Please provide a URL')

        await ctx.send('Loading your video...')

        site = 'https://www.savetweetvid.com/'
        self.driver.get(site)
        element = self.driver.find_element(By.NAME, 'url')
        element.send_keys(url)
        element.submit()

        # wait until class 'card-text' is loaded
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'card-text'))
        )

        # store table tag
        table = self.driver.find_element(By.TAG_NAME, 'table')

        links = []
        # append the links inside the table to the list
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            for link in row.find_elements(By.TAG_NAME, 'a'):
                links.append(link.get_attribute('href'))

        self.driver.close()
        self.driver.quit()

        return await ctx.send(links[0])


def setup(bot):
    bot.add_cog(Automation(bot))
