# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import json
import asyncio
import csv
import os
import requests


class Anime(commands.Cog):
    """The description for Anime goes here."""

    working_dir = os.path.dirname(os.path.abspath(__file__))
    themes_data = json.load(open(f'{working_dir}/../db/themes1.json', encoding='utf8'))

    with open(f'{working_dir}/../db/registered_ids.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        registered_ids = [int(row[0]) for row in list(reader)[1:]]

    def __init__(self, bot):
        self.bot = bot

    ### Non-command functions ###
    def get_anime_data(self, anime_name):
        """
        Returns the data of the anime with the given name.
        """
        if len(anime_name) < 4:
            raise commands.BadArgument('The anime name must be at least 4 characters long.')

        url = 'https://api.jikan.moe/v4/anime'
        params = {'q' : anime_name}

        request = requests.get(url, params=params)
        if request.status_code != 200:
            raise commands.BadArgument('Anime not found.')
        
        data = request.json()
        names, anime_ids = [], []
        for anime in data['data']:
            names.append(anime['title'])
            anime_ids.append(anime['mal_id'])
        
        return list(zip(anime_ids, names))

    
    def get_anime_vid(self, anime_id):
        """
        Returns the video of the anime with the given id.
        """
        openings, endings = [], []

        for item in self.themes_data:
            if item['anime_id'] == anime_id:
                current = item['mirrors'][0]['mirror']
                openings.append(current) if 'OP' in current else endings.append(current)
        
        return openings, endings


    @commands.command(name='anime', aliases=['anime-info'])
    async def anime(self, ctx, *, anime_name):
        """
        Get information about an anime.
        """
        await ctx.send(f'{anime_name}')

    @commands.command(name='ani-vid', aliases=['anime-video', 'anime-vid'])
    async def ani_vid(self, ctx, *, anime_name):
        """
        Get the selected opening or ending for an anime search.
        """
        if len(anime_name) < 4:
            return await ctx.send('The anime name must be at least 4 characters long.')

        query = self.get_anime_data(anime_name)
        if not query:
            return await ctx.send('Anime not found.')
        
        available = []
        for anime in query:
            if anime[0] in self.registered_ids:
                available.append(anime)

        if not available:
            return await ctx.send('Anime not found.')

        await ctx.send('\n'.join([f'{i+1}) {item[1]}' for i, item in enumerate(available)]))

        try:
            choice = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
        except asyncio.TimeoutError:
            return await ctx.send('You took too long to respond.')
        
        choice = int(choice.content) - 1
        if choice < 0 or choice >= len(available):
            return await ctx.send('Invalid choice.')

        ops, eds = self.get_anime_vid(available[choice][0])

        if ops and not eds:
            await ctx.send(f'This title contains {len(ops)} opening(s).\nSelect one of them')

            try:
                choice = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
            except asyncio.TimeoutError:
                return await ctx.send('You took too long to respond.')
            
            choice = int(choice.content) - 1
            if choice < 0 or choice >= len(ops):
                return await ctx.send('Invalid choice.')
            
            return await ctx.send(f'Opening #{choice + 1}):\n{ops[choice]}')

        elif eds and not ops:
            await ctx.send(f'This title contains {len(eds)} ending(s).\nSelect one of them')

            try:
                choice = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
            except asyncio.TimeoutError:
                return await ctx.send('You took too long to respond.')
            
            choice = int(choice.content) - 1
            if choice < 0 or choice >= len(eds):
                return await ctx.send('Invalid choice.')
            
            return await ctx.send(f'Ending #{choice + 1}:\n{eds[choice]}')

        else:
            await ctx.send(f'This title contains {len(ops)} opening(s) and {len(eds)} ending(s).\nDo you want to select an opening or an ending?')

            try:
                choice = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['opening', 'ending'])
            except asyncio.TimeoutError:
                return await ctx.send('You took too long to respond.')
            
            choice = choice.content.lower()
            if choice == 'opening':
                await ctx.send(f'This title has {len(ops)} opening(s).\nSelect one of them')
                try:
                    choice = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
                except asyncio.TimeoutError:
                    return await ctx.send('You took too long to respond.')
                
                choice = int(choice.content) - 1
                if choice < 0 or choice >= len(ops):
                    return await ctx.send('Invalid choice.')
                
                return await ctx.send(f'Opening #{choice + 1}):\n{ops[choice]}')
            
            else:
                await ctx.send(f'This title has {len(eds)} ending(s).\nSelect one of them')

                try:
                    choice = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
                except asyncio.TimeoutError:
                    return await ctx.send('You took too long to respond.')
                
                choice = int(choice.content) - 1
                if choice < 0 or choice >= len(eds):
                    return await ctx.send('Invalid choice.')
                
                return await ctx.send(f'Ending #{choice+1}:\n{eds[choice]}')

    # define a listener function
    @commands.Cog.listener()
    async def on_message(self, message):
        pass


def setup(bot):
    bot.add_cog(Anime(bot))
