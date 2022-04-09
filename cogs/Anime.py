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

def setup(bot):
    bot.add_cog(Anime(bot))
