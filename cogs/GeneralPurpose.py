# -*- coding: utf-8 -*-

from discord.ext import commands
from numpy import random
import discord
import requests
import json
import sys, os

class Generalpurpose(commands.Cog):
    """The description for Generalpurpose goes here."""

    cwd = os.getcwd()
    sys.path.append(f'{cwd}..')
    from config import ame_token, ame_endpoints

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


    @commands.command(name='ame', aliases=['ame-api'])
    async def ame_api(self, ctx, tag, image_url=''):
        """
        Get an image embed from Ame, $ame <tag> <image_url>, 
        $ame tags for a list of tags
        """
        
        if not tag:
            # get random tag
            tag = self.random.choice(self.ame_endpoints)
            await ctx.send(f'No tag specified, using {tag}')

        if tag == ('tag' or 'tags' or 'help'):
            # list tags
            return await ctx.send(f'Available tags: {", ".join(self.ame_endpoints)}')

        if tag not in self.ame_endpoints:
            return await ctx.send(f'Invalid tag, available tags: {", ".join(self.ame_endpoints)}')

        if not image_url:
            return await ctx.send('Please provide an image url')

        # Base url
        base_url = "https://v1.api.amethyste.moe"
        headers = {'Authorization': f'Bearer {self.ame_token}'}
        data = {'url': image_url}

        r = requests.post(f'{base_url}/generate/{tag}', headers=headers, data=data)

        if r.status_code != (200 or 201):
            return await ctx.send(f"Error: {r.status_code}")
        
        # save request as a png
        with open(f'ame_{tag}.png', 'wb') as f:
            f.write(r.content)
        
        # send image
        await ctx.send(file=discord.File(f'ame_{tag}.png'))

        
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


    # grab the user's avatar
    @commands.command(name='avatar', aliases=['av'])
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Get a user's avatar"""

        # get user
        if not user:
            user = ctx.author

        # get avatar
        avatar = user.avatar_url
        if avatar:
            return await ctx.send(avatar)
        else:
            return await ctx.send('Sorry, there was an error getting the avatar')

    @commands.command(name='qr', aliases=['qrcode'])
    async def qr(self, ctx, qr_url):
        """
        Decode a QR code from a given URL.
        """
        if not qr_url:
            return await ctx.send('You did not specify a URL.')

        url = 'http://api.qrserver.com/v1/read-qr-code/?fileurl='

        r = requests.get(url + qr_url)
        await ctx.send('Loading...')
        if r.status_code != (200 or 204):
            return await ctx.send(f'Error: {r.status_code}')

        data = r.json()
        return await ctx.send(data[0]['symbol'][0]['data'])

    # on raw reaction

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if message.author.bot:
            return

        reaction = discord.utils.get(message.reactions, emoji='😎')
        if not reaction:
            return

        # user = payload.member
        return await self.qr(message.channel, message.content)

    
    # define a listener
    @commands.Cog.listener()
    async def on_message(self, message): pass
        # check if message author is 'Extrieve'
        # if message.author.name == 'Renato Tizon':
        #     # fire emoji reaction
        #     await message.add_reaction('🔥')
        #     # red pepper emoji
        #     await message.add_reaction('🌶')

        # if message.author.name == 'Buddha':
        #     if 'png' or 'jpg' in message.content:
        #         # add wolf emoji reaction
        #         await message.add_reaction('🐺')
            
        

def setup(bot):
    bot.add_cog(Generalpurpose(bot))
