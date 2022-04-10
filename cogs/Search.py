# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import sys
import os
from serpapi import GoogleSearch

class Search(commands.Cog):
    """The description for Search goes here."""

    # Get current working directory and add it to the path
    cwd = os.getcwd()
    sys.path.append(f'{cwd}..')
    from config import serp_key

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='image', aliases=['img'])
    async def image_search(self, ctx, *, search):
        """
        Search for an image on Google Images.
        """
        
        if not search:
            return await ctx.send('Please enter a search term.')

        params = {
            'q': search,
            'tbm': 'isch',
            'ijn': '0',
            'api_key': self.serp_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Tell user we're loading the request
        await ctx.send(f'Loading...')

        if not results:
            return await ctx.send(f'No results found for {search}.')
    
        # await ctx.send(results['images_results'][0]['original'])

        # Display the first image but allow the user to traverse the rest
        embed = discord.Embed(title=f'{results["images_results"][0]["title"]}', url=results['images_results'][0]['original'], color=0x00ff00)
        embed.set_image(url=results['images_results'][0]['original'])
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Search(bot))
