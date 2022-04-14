# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import os, sys
import requests

class Machinelearning(commands.Cog):
    """The description for Machinelearning goes here."""

    cwd = os.getcwd()
    sys.path.append(f'{cwd}..')
    from config import google_key

    def __init__(self, bot):
        self.bot = bot

    def detect_labels_uri(self, uri):
        """Detects labels in the file located in Google Cloud Storage or on the
        Web."""
        api_root = 'https://vision.googleapis.com/v1/images:annotate?key='

        # Request parameters
        params = {
            'requests': [{
                'image': {
                    'source': {
                        'imageUri': uri
                    }
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10
                }]
            }]
        }

        # make the request
        r = requests.post(api_root + self.google_key, json=params)

        # print the response
        response = r.json()['responses'][0]['labelAnnotations']
        output = []
        for item in response:
            output.append(f"{item['description']}: {round(item['score'], 2)}")

        return output


    @commands.command(name='label', aliases=['labels'])
    async def label(self, ctx, *, image_url):
        """Detects labels in the file located in Google Cloud Storage or on the
        Web."""
        labels = self.detect_labels_uri(image_url)
        
        # Embed the labels
        embed = discord.Embed(title='Labels', description='\n'.join(labels))
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    
    
def setup(bot):
    bot.add_cog(Machinelearning(bot))
