# -*- coding: utf-8 -*-

from discord.ext import commands
from selenium import webdriver
from Screenshot import Screenshot_Clipping
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
import os
import discord
import asyncio

class Automation(commands.Cog):
    """Cog for automation purposes with Selenium and Beautiful Soup."""

    chrome_options = webdriver.ChromeOptions()

    resolution = "--window-size=1920,1080"
    chrome_options.add_argument(resolution)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    service = Service(os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, chrome_options=chrome_options)

    # op gg regions
    regions = {'na': ('North America', '🇺🇸'), 'euw': ('Europe West', '🇪🇺'), 'br': (
        'Brazil', '🇧🇷'), 'las': ('LAS', '🇵🇪'), 'lan': ('LAN', '🇲🇽')}

    flags = [item[1] for item in regions.values()]

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

    @commands.command(name='opgg')
    async def opgg(self, ctx, *, summoner):
        """Get your OP.GG stats"""
        if not summoner:
            return await ctx.send('Please provide a summoner name')

        # send embed with the regions and their respective flags next to it
        embed = discord.Embed(
            title='OP.GG', description='Select a region', color=0x00ff00)
        for region, values in self.regions.items():
            embed.add_field(name=region, value=values[1], inline=True)
        msg = await ctx.send(embed=embed)

        # add reactions to the message
        for region in self.regions:
            await msg.add_reaction(self.regions[region][1])

        # wait for a reaction
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in self.flags

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send('You took too long to react, cancelling...')

        # get the region from the reaction
        region = [key for key, value in self.regions.items() if value[1]
                  == str(reaction.emoji)][0]

        url = f'https://{region}.op.gg'
        self.driver.get(url)

        await ctx.send('Loading your stats...')

        search = self.driver.find_element(By.ID, 'searchSummoner')
        search.send_keys(summoner)
        search.submit()

        # wait until class name is loaded
        WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'profile'))
        )
        self.driver.get(self.driver.current_url + '/ingame')

        # # find div tag
        # divs = self.driver.find_element(By.TAG_NAME, 'div')

        # # for all divs find class name = 'css-1n276kj eafu1dm0'
        # div = divs.find_elements(By.CLASS_NAME, 'css-1n276kj eafu1dm0')

        WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'team-name'))
        )

        # take a full page screenshot
        # ob = Screenshot_Clipping.Screenshot()
        # ob.full_Screenshot(self.driver, save_path=r'..',
        #                    image_name='livegame.png')

        img = self.ob.get_screenshot(self.driver)

        # width, height
        w, h = img.size

        # cropping the image
        left = int(w * 0.24)
        right = int(w * 0.76)
        top = int(h * 0.47)
        bottom = int(h * 0.88)

        # save the cropped image
        img = img.crop((left, top, right, bottom)).save(r'../livegame_cropped.png')
        # close browser
        self.driver.close()
        self.driver.quit()

        # send the image variable
        await ctx.send(file=discord.File(r'../livegame_cropped.png'))


def setup(bot):
    bot.add_cog(Automation(bot))
