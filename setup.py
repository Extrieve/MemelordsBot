import os

categories = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile',
              'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe']
ame_endpoints = ['approved', 'beautiful', 'challenger', 'circle', 'crush', 'dungeon', 'dictator',
            'fire', 'jail', 'missionpassed', 'rip', 'utatoo', 'wated']

available_contests = {'codeforces': 'https://play-lh.googleusercontent.com/EkSlLWf2-04k5Y5F_MDLqoXPdo0TyZX3zKdCfsEUDqVB7INUypTOd6AVmkE_X7ej3JuR',
                      'top_coder': 'https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/tdenoarg7lu2emnoyu7c',
                      'at_coder': 'https://img.atcoder.jp/assets/atcoder.png',
                      'cs_academy': 'https://students.ieee.org/wp-content/uploads/2018/08/csacademy_sponsor.png',
                      'code_chef': 'https://pbs.twimg.com/profile_images/1477930785537605633/ROTVNVz7_400x400.jpg',
                      'hacker_rank': 'https://upload.wikimedia.org/wikipedia/commons/4/40/HackerRank_Icon-1000px.png',
                      'hacker_earth': 'https://upload.wikimedia.org/wikipedia/commons/e/e8/HackerEarth_logo.png',
                      'kick_start': 'https://bookassist.org/wp-content/uploads/2021/07/google-logo.jpg',
                      'leet_code': 'https://leetcode.com/static/images/LeetCode_logo_rvs.png',
                      'toph': 'https://help.toph.co/emblems/platform.2246769acdc0086a24ee5a72689be221a0d7e8bab8897faac42ff0664be37a8e.png'}

# get working directory
cwd = os.getcwd()

# load all cog files
cogs = []
for file in os.listdir(cwd + "/cogs"):
    if file.endswith(".py") and '__' not in file:
        cogs.append(f'cogs.{file[:-3]}')
