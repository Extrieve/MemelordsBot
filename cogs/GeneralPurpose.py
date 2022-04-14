# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import requests
import json

class Generalpurpose(commands.Cog):
    """The description for Generalpurpose goes here."""

    def __init__(self, bot):
        self.bot = bot

    # url shortener
    @commands.command(name='short', aliases=['shorten'])
    async def short(self, ctx, *, url):
        """Shorten a URL"""

        # check if url is valid
        if not url.startswith('http'):
            url = 'http://' + url

        # shorten url
        r = requests.get("https://api.1pt.co/addURL",
                            params={"long": url})
        
        if r.status_code != (200 or 201):
            return await ctx.send(f"Error: {r.status_code}")

        return await ctx.send(f'Here is your shortened URL: 1pt.co/{r.json()["short"]}')

    # yo momma jokes
    @commands.command(name='momma', aliases=['yo-momma'])
    async def momma(self, ctx):
        """Get a random yo momma joke"""

        # get joke
        yomomma = requests.get('https://yomomma-api.herokuapp.com/jokes')
        if yomomma:
            return await ctx.send(json.loads(yomomma.text)['joke'])
        else:
            return await ctx.send('Sorry, there was an error getting yo momma')

    @commands.command(name='8ball', aliases=['8b'])
    async def eightball(self, ctx, *, question):
        """Ask the magic 8ball a question"""

        # get answer
        eightball = requests.get('https://8ball.delegator.com/magic/JSON/')
        if eightball:
            return await ctx.send(json.loads(eightball.text)['magic']['answer'])
        else:
            return await ctx.send('Sorry, there was an error getting the magic 8ball')
    
    # duck pic
    @commands.command(name='duck', aliases=['duckpic'])
    async def duck(self, ctx):
        """Get a random duck pic"""

        # get pic
        duck = requests.get('https://random-d.uk/api/random')
        if duck:
            return await ctx.send(json.loads(duck.text)['url'])
        else:
            return await ctx.send('Sorry, there was an error getting the duck pic')

    
    # define a listener
    @commands.Cog.listener()
    async def on_message(self, message):
        # check if message author is 'Extrieve'
        if message.author.name == 'Renato Tizon':
            # fire emoji reaction
            await message.add_reaction('🔥')
            # red pepper emoji
            await message.add_reaction('🌶')

        if message.author.name == 'Buddha':
            if 'png' or 'jpg' in message.content:
                # add wolf emoji reaction
                await message.add_reaction('🐺')
            
        

def setup(bot):
    bot.add_cog(Generalpurpose(bot))
