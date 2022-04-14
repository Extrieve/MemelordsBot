# -*- coding: utf-8 -*-

from discord.ext import commands
from numpy import random
import discord
import json
import asyncio
import csv
import os
import requests
import sys
import urllib.parse


class Anime(commands.Cog):
    """The description for Anime goes here."""

    working_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(f'{working_dir}..')
    themes_data = json.load(open(f'{working_dir}/../db/themes1.json', encoding='utf8'))
    pic_url = 'https://api.waifu.pics/sfw/'

    with open(f'{working_dir}/../db/registered_ids.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        registered_ids = [int(row[0]) for row in list(reader)[1:]]

    from config import categories

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

    
    def anilist_query(self, anime_id):
        
        query = '''
        query ($id: Int) { # Define which variables will be used in the query (id)
        Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            id
            title {
            romaji
            english
            native
            }
        }
        }
        '''

        # Define our query variables and values that will be used in the query request
        variables = {
            'id': int(anime_id)
        }

        url = 'https://graphql.anilist.co'

        # Make the HTTP Api request
        response = requests.post(url, json={'query': query, 'variables': variables})

        if response.status_code != 200:
            raise Exception('Query failed to run by returning code of {}. {}'.format(response.status_code, response.text))

        data = response.json()
        output = {}
        output['title_rom'] = data['data']['Media']['title']['romaji']
        output['title_eng'] = data['data']['Media']['title']['english']

        return output


    @commands.command(name='ani-search', aliases=['anime-info', 'anime-search'])
    async def ani_search(self, ctx, *, anime_name):
        """
        Get information about an anime.
        """
        if not anime_name:
            return await ctx.send('Please enter an anime name.')
        
        if len(anime_name) < 4:
            return await ctx.send('The anime name must be at least 4 characters long.')

        url = 'https://api.jikan.moe/v4/anime'
        params = {'q' : anime_name}

        request = requests.get(url, params=params, verify=False)

        if request.status_code != 200:
            return await ctx.send('Anime not found.')
        
        data = request.json()
        results = []
        for i, entry in enumerate(data['data']):
            results.append(f'{i+1}. {entry["title"]}')

        embed = discord.Embed(title='Anime Search', description='\n'.join(results), color=0x00ff00)
        embed.set_footer(text='Type the number of the anime you want to get info on.')
        await ctx.send(embed=embed)

        # Get user selection
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            choice = await self.bot.wait_for('message', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            return await ctx.send('You took too long to respond.')
            
        try:
            choice = int(choice.content) - 1
        except ValueError:
            return await ctx.send('Please enter a valid number.')
        
        if choice < 0 or choice >= len(data['data']):
            return await ctx.send('Please enter a valid number.')
        
        response = []
        try:
            response.append(f'**{data["data"][choice]["title"]}**')
            response.append(f'**Score:** {data["data"][choice]["score"]}')
            response.append(f'**Rating:** {data["data"][choice]["rating"]}')
            response.append(f'**Episodes:** {data["data"][choice]["episodes"]}')
            response.append(f'**Popularity:** {data["data"][choice]["popularity"]}')
            response.append(f'**Studios:** {data["data"][choice]["studios"][0]["name"]}')
            response.append(f'**Synopsis:** {data["data"][choice]["synopsis"]}')
            response.append(f'**Posters:** {data["data"][choice]["images"]["jpg"]["large_image_url"]}')
        except (KeyError, IndexError, ValueError) as e:
            print(e)
            response = []
            response.append(f'**{data["data"][choice]["title"]}**')
            response.append(f'**Score:** {data["data"][choice]["score"]}')
            response.append(f'**Rating:** {data["data"][choice]["rating"]}')
            response.append(f'**Popularity:** {data["data"][choice]["popularity"]}')
            response.append(
                f'**Synopsis:** {data["data"][choice]["synopsis"]}')
            response.append(
                f'**Posters:** {data["data"][choice]["images"]["jpg"]["large_image_url"]}')

        
        embed = discord.Embed(title='Anime Info', description='\n'.join(response), color=0x00ff00)
        embed.set_thumbnail(url=data["data"][choice]["images"]["jpg"]["large_image_url"])
        # embed.set_footer(text='Type the number of the anime you want to get info on.')
        return await ctx.send(embed=embed)

    # manga search
    @commands.command(name='manga-search', aliases=['manga-info', 'man-search'])
    async def manga_search(self, ctx, *, manga_name):
        """
        Get information about a manga.
        """
        
        if not manga_name:
            return await ctx.send('Please enter a manga name.')
        
        if len(manga_name) < 4:
            return await ctx.send('The manga name must be at least 4 characters long.')

        url = 'https://api.jikan.moe/v4/manga/'
        params = {'q' : manga_name, 'page' : 1}

        request = requests.get(url, params=params, verify=False)

        if request.status_code != (200 or 204):
            return await ctx.send('Manga not found.')
        
        data = json.loads(request.text)
        results = []
        for i, entry in enumerate(data['data']):
            results.append(f'{i+1}. {entry["title"]}')

        embed = discord.Embed(title='Manga Search', description='\n'.join(results), color=0x00ff00)
        embed.set_footer(text='Type the number of the manga you want to get info on.')
        await ctx.send(embed=embed)

        # Get user selection
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            choice = await self.bot.wait_for('message', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            return await ctx.send('You took too long to respond.')
            
        try:
            choice = int(choice.content) - 1
        except ValueError:
            return await ctx.send('Please enter a valid number.')
        
        if choice < 0 or choice >= len(data['data']):
            return await ctx.send('Please enter a valid number.')
        
        response = []
        try:
            title = data['data'][choice]['title']
            image = data['data'][choice]['images']['jpg']['large_image_url']
            response.append(f'**Chapters**: {data["data"][choice]["chapters"]}')
            response.append(f'**Volumes**: {data["data"][choice]["volumes"]}')
            response.append(f'**Score**: {data["data"][choice]["score"]}')
            response.append(f'**Synopsis**: {data["data"][choice]["synopsis"]}')
        except (KeyError, IndexError, ValueError) as e:
            print(e)
            return await ctx.send('Manga not found.')

        embed = discord.Embed(title=title, description='\n'.join(response), color=0x00ff00)
        embed.set_thumbnail(url=image)
        return await ctx.send(embed=embed)


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
            await ctx.send(f'This title contains {len(ops)} opening(s). Enter the number of the video you want to watch.')

            try:
                choice = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
            except asyncio.TimeoutError:
                return await ctx.send('You took too long to respond.')
            
            choice = int(choice.content) - 1
            if choice < 0 or choice >= len(ops):
                return await ctx.send('Invalid choice.')
            
            return await ctx.send(f'Opening #{choice + 1}):\n{ops[choice]}')

        elif eds and not ops:
            await ctx.send(f'This title contains {len(eds)} ending(s). Enter the number of the video you want to watch.')

            try:
                choice = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
            except asyncio.TimeoutError:
                return await ctx.send('You took too long to respond.')
            
            choice = int(choice.content) - 1
            if choice < 0 or choice >= len(eds):
                return await ctx.send('Invalid choice.')
            
            return await ctx.send(f'Ending #{choice + 1}:\n{eds[choice]}')

        else:
            msg = await ctx.send(f'This title contains {len(ops)} opening(s) and {len(eds)} ending(s).\nDo you want to select an opening 😎 or an ending 🥰?')

            # add reactions to message
            await msg.add_reaction('😎')
            await msg.add_reaction('🥰')

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['🥰', '😎']
            try:
            
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
            except asyncio.TimeoutError:
                return await ctx.send('You took too long to respond.')
            
            if str(reaction.emoji) == '😎':
                await ctx.send(f'This title has {len(ops)} opening(s). Enter the number of the video you want to watch.')
                try:
                    choice = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
                except asyncio.TimeoutError:
                    return await ctx.send('You took too long to respond.')
                
                choice = int(choice.content) - 1
                if choice < 0 or choice >= len(ops):
                    return await ctx.send('Invalid choice.')
                
                return await ctx.send(f'Opening #{choice + 1}):\n{ops[choice]}')
            
            else:
                await ctx.send(f'This title has {len(eds)} ending(s). Enter the number of the video you want to watch.')

                try:
                    choice = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
                except asyncio.TimeoutError:
                    return await ctx.send('You took too long to respond.')
                
                choice = int(choice.content) - 1
                if choice < 0 or choice >= len(eds):
                    return await ctx.send('Invalid choice.')
                
                return await ctx.send(f'Ending #{choice+1}:\n{eds[choice]}')

    
    # anime pictures, make category an optional parameter
    @commands.command(name='anime-pic', aliases=['anime-pics', 'anime-pictures'])
    async def anime_pic(self, ctx, category: str = None):
        """
        Get a random anime picture from the specified category.
        """
        if not category:
            # Return a random picture
            category = random.choice(self.categories)
            await ctx.send(f"You didn't specify a category, so I'll pick one for you: {category}")

            # Api call
            response = requests.get(f'{self.pic_url}{category}').text
            picture = json.loads(response)['url']
            return await ctx.send(picture)


        if category.lower() not in self.categories:
            return await ctx.send('Invalid category.')

        response = requests.get(f'{self.pic_url}{category}').text
        picture = json.loads(response)['url']
        return await ctx.send(picture)

    
    # Recognize anime by scene
    @commands.command(name='ani-scene', aliases=['ani-scenes, anime-scene'])
    async def ani_scene(self, ctx, scene_url: str):
        """
        Recognize anime by scene.
        """
        
        # verify that the url contains an image
        if not scene_url.endswith('.jpg') and not scene_url.endswith('.png') and not scene_url.endswith('.jpeg'):
            return await ctx.send('Invalid url.')

        parse_url = urllib.parse.quote_plus(scene_url)
        response = requests.get(f"https://api.trace.moe/search?url={parse_url}").json()
        
        if response['error']:
            return await ctx.send('Could not find anime.')
        
        results = response['result']

        anime_id = results[0]['anilist']
        titles = self.anilist_query(anime_id)

        output = []
        title_rom = titles['title_rom']
        output.append(f"**English Title**: {titles['title_eng']}")
        output.append(f"**Filename**: {results[0]['filename']}")
        output.append(f"**Episode**: {results[0]['episode']}")
        output.append(f"Similarity: {round(results[0]['similarity'], 2)}")

        embed = discord.Embed(title=title_rom, description='\n'.join(output), color=0x00ff00)
        embed.set_image(url=scene_url)
        return await ctx.send(embed=embed)


    # on raw reaction
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if message.author.bot:
            return
        
        reaction = discord.utils.get(message.reactions, emoji='🤓')
        # print(reaction)
        if not reaction:
            return

        user = payload.member
        # print(user)

        print('HERE')
        # print(output)
        # await self.bot.get_channel(payload.channel_id).send(output)
        return await self.ani_scene(message.channel, message.content)
        

def setup(bot):
    bot.add_cog(Anime(bot))
