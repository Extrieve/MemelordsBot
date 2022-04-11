# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import sys
import os
import requests
import json
import asyncio
from serpapi import GoogleSearch

class Search(commands.Cog):
    """The description for Search goes here."""

    # Get current working directory and add it to the path
    cwd = os.getcwd()
    sys.path.append(f'{cwd}..')
    from config import serp_key

    def __init__(self, bot):
        self.bot = bot

    def getDefinition(self, word):
        response = requests.get(
            f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        processedResponse = json.loads(response.text)
        # return f"Definition: {processedResponse[0]['meanings'][0]['definitions'][0]['definition']}"
        return processedResponse[0]['meanings'][0]['definitions']

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

    # Dictionary definitions
    @commands.command(name='define', aliases=['d'])
    async def define(self, ctx, *, search):
        """
        Search for a word or phrase on Google Dictionary.
        """

        if not search:
            return await ctx.send('Please enter a search term.')

        try:
            definition = self.getDefinition(search)
        except KeyError:
            return await ctx.send(f'No results found for {search}.')

        # Embed the definition
        index = 0
        embed = discord.Embed(title=f'{search.capitalize()}', color=0x00ff00)
        embed.add_field(name='Definition', value=definition[index]['definition'])
        embed.set_footer(text=f'Definition {index + 1} of {len(definition)}')
        message = await ctx.send(embed=embed)

        # Add reactions to the message
        await message.add_reaction('◀️')
        await message.add_reaction('▶️')

        # Wait for a reaction
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['◀️', '▶️'] and reaction.message.id == message.id
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send('Timed out.')

            if str(reaction.emoji) == '◀️':
                index -= 1
                if index < 0:
                    index = len(definition) - 1
            elif str(reaction.emoji) == '▶️':
                index += 1
                if index >= len(definition):
                    index = 0

            embed.clear_fields()
            embed.add_field(name='Definition', value=definition[index]['definition'])
            embed.set_footer(text=f'Definition {index + 1} of {len(definition)}')
            await message.edit(embed=embed)

            await message.remove_reaction(reaction.emoji, user)

        
def setup(bot):
    bot.add_cog(Search(bot))
