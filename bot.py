#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import config
import asyncio

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('$'), **kwargs)
        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print(f'Could not load extension {cog} due to {exc.__class__.__name__}: {1}')

    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')

    # async def on_message(self, message):
    #     if message.author.bot:
    #         return

    #     if message.author.id == self.user.id:
    #         return

    #     # check if user 'Buddha#5777' sends a message
    #     if message.author.name == 'Buddha' and 'cdn' in message.content.lower():
    #         emoji = '🐺'
    #         # reply with woof, and a dog emoji
    #         await message.channel.send(f'Woof! {emoji}')

    #     if 'emoji' in message.content.lower():
    #         emoji = '🐺'
    #         await message.channel.send(f'Emoji! {emoji}')

# write general commands here

async def main():
    bot = Bot()
    await bot.start(config.token)

if __name__ == '__main__':
    asyncio.run(main())