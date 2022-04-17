# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import requests
import os, sys
import datetime

class Programming(commands.Cog):
    """The description for Programming goes here."""

    contest_url = 'https://kontests.net'

    cwd = os.getcwd()
    sys.path.append(f'{cwd}..')
    from config import available_contests

    def __init__(self, bot):
        self.bot = bot

    # contest information
    @commands.command(name='contest', aliases=['contestinfo'])
    async def contest(self, ctx, *, site=''):
        """
        Get information about the current contest.
        """
        if not site:
            endpoint = '/api/v1/all'
            r = requests.get(self.contest_url + endpoint)
            if r.status_code != (200 or 204):
                return await ctx.send(f'Error: {r.status_code}')

            data = r.json()
            # TODO: Complete the for contests of all sites
            pass
        
        site = site.replace(' ', '_')
        print(site)
        if site not in self.available_contests:
            return await ctx.send(f'Error: {site} is not a valid contest site.')

        # replace spaces with _
        endpoint = f'/api/v1/{site}'
        r = requests.get(self.contest_url + endpoint)

        if r.status_code != (200 or 204):
            return await ctx.send(f'Error: {r.status_code}')

        data = r.json()
        contests = []
        for entry in data:
            start_time = entry['start_time']
            end_time = entry['end_time']

            # TODO: Change time format

            contests.append(f'{entry["name"]} - {start_time} - {end_time} - {entry["url"]}')

        # embed the contest data
        embed = discord.Embed(title=f'{site.capitalize()}', description='\n'.join(contests), color=0x00ff00)
        image = self.available_contests[site]
        embed.set_thumbnail(url=image)
        await ctx.send(embed=embed)

        


def setup(bot):
    bot.add_cog(Programming(bot))
