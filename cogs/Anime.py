# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Anime(commands.Cog):
    """The description for Anime goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime', aliases=['anime-info'])
    async def anime(self, ctx, *, anime_name):
        """
        Get information about an anime.
        """
        await ctx.send(f'{anime_name}')

    @commands.command(name='search-anime', aliases=['search-ani'])
    async def search_anime(self, ctx, *, anime_name):
        """
        Search for an anime.
        """
        if anime_name == 'help':
            await ctx.send('You can search for an anime by typing `!search-anime <anime name>`')
        if len(anime_name) <= 3:
            await ctx.send('Please enter a longer anime name.')
            
        url = 'https://api.jikan.moe/v4/anime'


def setup(bot):
    bot.add_cog(Anime(bot))
