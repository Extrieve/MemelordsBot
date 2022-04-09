# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Music(commands.Cog):
    """The description for Music goes here."""

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Music(bot))
