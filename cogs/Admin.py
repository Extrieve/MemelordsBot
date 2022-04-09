# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Admin(commands.Cog):
    """The description for Admin goes here."""

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Admin(bot))
