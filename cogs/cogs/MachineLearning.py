# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Machinelearning(commands.Cog):
    """The description for Machinelearning goes here."""

    def __init__(self, bot):
        self.bot = bot

    

def setup(bot):
    bot.add_cog(Machinelearning(bot))
