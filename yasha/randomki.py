import asyncio
import discord
import random
import requests
import json
from tools import getlang,getpref,highlight

TOKEN = 'secretcodeddededed'
client = discord.Client()

def flip():
    sides=['dotabase/emoticons/yasha.gif','dotabase/emoticons/sange.gif']
    return random.choice(sides)


async def randomtip(message,client):
    if message.content.startswith('randomtip',1):
        lang=getlang(message.guild.id)
        pref=getpref(message.guild.id)
        responses={'en':{'rndtip':'Random tip'},

                   'ru':{'rndtip':'Случайный совет'}}
        phr=responses[lang]

        
        if pref==message.content[0]:
            with open(f"dotabase/tips_{lang}.txt",'r') as f:
                tips = f.readlines()
            tip=random.choice(tips)
            embed = discord.Embed(colour=discord.Colour(0xd0021b))
            embed.set_thumbnail(url="https://gamepedia.cursecdn.com/dota2_gamepedia/f/fc/Tome_of_Knowledge_icon.png")
            embed.set_footer(text=f"{client.user.name} | {pref}randomtip", icon_url=client.user.avatar_url_as(format='png'))
            embed.add_field(name=phr['rndtip'],value=highlight(tip))
            await message.channel.send(embed=embed)


            
async def randomhero(message,client):
    if message.content.startswith('randomhero',1):
        lang=getlang(message.guild.id)
        pref=getpref(message.guild.id)
        
        if pref[0]==message.content[0]:
            start = {'ru':['Думаю, ','Стоит попробовать ','Возможно стоит взять ','Определённо ','Может быть '],'en':['Maybe ','You should try ','Pick ','Try ','Hmm, ', 'Obviously ']}
            with open('dotabase/heroes.txt', mode='r', encoding='utf-8-sig') as f:
                heroes=f.readlines()
            hero=dict(eval(random.choice(heroes)))
            embed = discord.Embed(title=random.choice(start[lang])+f'<{hero["emoji"]}>**{hero["name"]}**',colour=discord.Colour(0xd0021b))
            embed.set_image(url=f'http://cdn.dota2.com/apps/dota2/images/heroes/{hero["icon"]}')
            embed.set_footer(text=f"{client.user.name} | {pref}randomhero", icon_url=client.user.avatar_url_as(format='png'))
            await message.channel.send(embed=embed)
            
        
