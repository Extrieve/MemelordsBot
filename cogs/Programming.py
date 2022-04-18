# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import requests
import os
import sys
from datetime import datetime
import pytz


class Programming(commands.Cog):
    """The description for Programming goes here."""

    contest_url = 'https://kontests.net'

    cwd = os.getcwd()
    sys.path.append(f'{cwd}..')
    from setup import available_contests

    def __init__(self, bot):
        self.bot = bot


    def time_convert(self, convert):
        est = pytz.timezone('US/Eastern')
        utc = pytz.utc
        # 2022-05-08T12:00:00.000Z format
        fmt = '%Y-%m-%dT%H:%M:%S.000Z'

        winter = datetime(2022, 1, 24, 18, 0, 0, tzinfo=utc)
        summer = datetime(2022, 7, 24, 18, 0, 0, tzinfo=utc)

        start_time = datetime.strptime(convert, fmt)
        start_time = start_time.astimezone(est)

        date, time = start_time.strftime(
            '%Y-%m-%d'), str(start_time).split(' ')[1]
        difference = time.split('-')[-1]
        difference = int(difference.split(':')[0])

        new_hour = int(time.split(':')[0]) - difference

        time = time.split(':')
        time[0] = str(new_hour)
        time = ':'.join(time)

        index = time.index('-') if '-' in time else time.index('+')
        time = time[:index]

        return date, time


    # contest information
    @commands.command(name='contest', aliases=['contestinfo'])
    async def contest(self, ctx, *, site=''):
        """
        Get information about the current contest.
        """
        if not site:
            # return all the possible endpoints
            await ctx.send('You did not specifcy a contest site.\nHere are the available sites:')
            embed = discord.Embed(title='Contest Information', description='\n'.join(
                self.available_contests), color=0x00ff00)
            return await ctx.send(embed=embed)

        site = site.replace(' ', '_')
        # print(site)
        if site not in self.available_contests:
            await ctx.send(f'Error: {site} is not a valid contest site.\nThe available sites are:')
            embed = discord.Embed(title='Contest Information', description='\n'.join(
                self.available_contests), color=0x00ff00)
            return await ctx.send(embed=embed)

        # replace spaces with _
        endpoint = f'/api/v1/{site}'
        r = requests.get(self.contest_url + endpoint)

        if r.status_code != (200 or 204):
            return await ctx.send(f'Error: {r.status_code}')

        data = r.json()
        contests = []
        for entry in data:
            start_d, start_t = self.time_convert(entry['start_time'])
            end_d, end_t = self.time_convert(entry['end_time'])
            contests.append(
                f'{entry["name"]} - Day: {start_d} - Start: {start_t} - End: {end_t} - {entry["url"]}')

        # embed the contest data
        embed = discord.Embed(title=f'{" ".join([item.capitalize() for item in site.split("_")])}', description='\n'.join(
            contests), color=0x00ff00)
        image = self.available_contests[site]
        embed.set_thumbnail(url=image)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Programming(bot))
