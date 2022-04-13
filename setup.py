import os

categories = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile',
              'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe']


# get working directory
cwd = os.getcwd()

# load all cog files
cogs = []
for file in os.listdir(cwd + "/cogs"):
    if file.endswith(".py") and '__' not in file:
        cogs.append(f'cogs.{file[:-3]}')
