# -*- coding: utf-8 -*-

from discord.ext import commands
from google.cloud import vision
import discord
import os

class Machinelearning(commands.Cog):
    """The description for Machinelearning goes here."""

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'db/google_vision.json'

    def __init__(self, bot):
        self.bot = bot

    def detect_labels_uri(self, uri):
        """Detects labels in the file located in Google Cloud Storage or on the
        Web."""
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = uri

        response = client.label_detection(image=image)
        labels = response.label_annotations
        output = []
        for label in labels:
            output.append(f'{label.description} {label.score:.2f}')

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

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
