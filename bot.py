#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import os
import asyncio
import setup
import discord

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('$'), **kwargs)
        for cog in setup.cogs:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print(f'Could not load extension {cog} due to {exc.__class__.__name__}: {1}')

    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')

# write general commands here

async def main():
    intents = discord.Intents.default()
    intents.members = True
    bot = Bot(intents=intents)
    await bot.start(os.environ['token'])

if __name__ == '__main__':
    asyncio.run(main())