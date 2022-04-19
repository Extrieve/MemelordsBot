import os

categories = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile',
              'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe']
ame_endpoints = ['approved', 'beautiful', 'challenger', 'circle', 'crush', 'dungeon', 'dictator',
            'fire', 'jail', 'missionpassed', 'rip', 'utatoo', 'wated']

available_contests = {'codeforces': ('https://play-lh.googleusercontent.com/EkSlLWf2-04k5Y5F_MDLqoXPdo0TyZX3zKdCfsEUDqVB7INUypTOd6AVmkE_X7ej3JuR', '%Y-%m-%dT%H:%M:%S.%LZ'),
                      'top_coder': ('https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/tdenoarg7lu2emnoyu7c', '%Y-%m-%dT%H:%M:%S.%LZ'),
                      'at_coder': ('https://img.atcoder.jp/assets/atcoder.png', '%Y-%m-%dT%H:%M:%S.%LZ'),
                      'cs_academy': ('https://students.ieee.org/wp-content/uploads/2018/08/csacademy_sponsor.png', '%Y-%m-%dT%H:%M:%S.%LZ'),
                      'code_chef': ('https://pbs.twimg.com/profile_images/1477930785537605633/ROTVNVz7_400x400.jpg', '%Y-%m-%dT%H:%M:%S.%LZ'),
                      'hacker_rank': ('https://upload.wikimedia.org/wikipedia/commons/4/40/HackerRank_Icon-1000px.png', '%Y-%m-%dT%H:%M:%S.%LZ'),
                      'hacker_earth': ('https://upload.wikimedia.org/wikipedia/commons/e/e8/HackerEarth_logo.png', '%Y-%m-%dT%H:%M:%S.%LZ'),
                      'kick_start': ('https://bookassist.org/wp-content/uploads/2021/07/google-logo.jpg', '%Y-%m-%dT%H:%M:%S.%LZ'),
                      'leet_code': ('https://leetcode.com/static/images/LeetCode_logo_rvs.png', '%Y-%m-%dT%H:%M:%S.%LZ')}

# get working directory
cwd = os.getcwd()

# load all cog files
cogs = []
for file in os.listdir(cwd + "/cogs"):
    if file.endswith(".py") and '__' not in file:
        cogs.append(f'cogs.{file[:-3]}')
