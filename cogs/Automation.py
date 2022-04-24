# -*- coding: utf-8 -*-

from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import discord
import asyncio

class Automation(commands.Cog):
    """Cog for automation purposes with Selenium and Beautiful Soup."""

    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    resolution = "--window-size=1920,1080"
    opt.add_argument(resolution)
    service = Service(r'C:\Selenium\chromedriver_win32\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=opt)

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
        embed = discord.Embed(title='OP.GG', description='Select a region', color=0x00ff00)
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
        region = [key for key, value in self.regions.items() if value[1] == str(reaction.emoji)][0]

        url = f'https://{region}.op.gg'
        await ctx.send(url)
        

    

def setup(bot):
    bot.add_cog(Automation(bot))
