import asyncio
import discord
from random import choice,randint
import requests
import json
from tools import getlang,getpref,highlight

with open('token.txt','r') as f:
    TOKEN=f.read()
client = discord.Client()

def flip():
    sides=['dotabase/emoticons/yasha.gif','dotabase/emoticons/sange.gif']
    return choice(sides)

async def roll(message,client):
    if message.content.startswith('roll',1):
        lang=getlang(message.guild.id)
        pref=getpref(message.guild.id)
        responses={'en':{'rnd':' rolls'},
                   'ru':{'rnd':' получает случайное число'}}
        phr=responses[lang]
        if pref==message.content[0]:
            command=message.content.split()
            if len(command)==1:
                l,r=1,100
                await message.channel.send(f'**{message.author.name}**{phr["rnd"]}({l}-{r}): `{randint(l,r)}`')
                
            if len(command)==2:
                if command[1].isdigit():
                    l,r=1,int(command[1])
                    await message.channel.send(f'**{message.author.name}**{phr["rnd"]}({l}-{r}): `{randint(l,r)}`')
                else:
                    l,r=1,100
                    await message.channel.send(f'**{message.author.name}**{phr["rnd"]}({l}-{r}): `{randint(l,r)}`')
                    
            if len(command)==3:
                if command[1].isdigit() and command[2].isdigit():
                    l,r=int(command[1]),int(command[2])
                    await message.channel.send(f'**{message.author.name}**{phr["rnd"]}({l}-{r}): `{randint(l,r)}`')
                else:
                    l,r=1,100
                    await message.channel.send(f'**{message.author.name}**{phr["rnd"]}({l}-{r}): `{randint(l,r)}`')                   

async def randomstuff(message,client):
    if message.content.startswith('random',1):
        lang=getlang(message.guild.id)
        pref=getpref(message.guild.id)
        responses={'en':{'rndtip':'Random tip',
                         '404':'Invalid command',
                         'name':'<a:coinflip:594438507938709524>Random stuff<a:coinflip:594438507938709524>',
                         'value':f'`{pref}random <command>`  - returns a random value. Available commands:\n'+u"\u2022"+'**hero** - If you have a hard time picking a hero\n'+u"\u2022"+'**tip** - Random in-game pause tip\n'+u"\u2022"+f'**mode** - If you don\'t know which game mode to choose\n\n`{pref}flip` - coinflip\n\n`{pref}roll <right border> / <left border> <right border>` - get a random number in the given range. If no numbers are given the range is 1-100'},

                   'ru':{'rndtip':'Случайный совет',
                         '404':'Некорректный запрос',
                         'name':'<a:coinflip:594438507938709524>Всякий рандом<a:coinflip:594438507938709524>',
                         'value':f'`{pref}random <command>`  - возвращает случайное значение. Допустимые команды:\n'+u"\u2022"+'**hero** - если сложно выбрать героя\n'+u"\u2022"+'**tip** - случайный совет с экрана паузы\n'+u"\u2022"+f'**mode** - если не получается выбрать режим игры\n\n`{pref}flip` - подбрасывание монетки\n\n`{pref}roll <правая граница> / <левая граница> <правая граница>` - возвращает случайное число в заданном диапазоне. Если числа не введены, то диапазон допустимых значений: 1-100'}}
        phr=responses[lang]
        if pref==message.content[0]:
            command=message.content.split()
            if len(command)==1:
                embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                embed.add_field(name=phr['name'],value=phr['value'],inline=True)
                await message.channel.send(embed=embed)
            else:
                if command[1]=='tip':
                    with open(f"dotabase/tips_{lang}.txt",'r') as f:
                        tips = f.readlines()
                    tip=choice(tips)
                    embed = discord.Embed(colour=discord.Colour(0xd0021b))
                    embed.set_thumbnail(url="https://gamepedia.cursecdn.com/dota2_gamepedia/f/fc/Tome_of_Knowledge_icon.png")
                    embed.set_footer(text=f"{client.user.name} | {pref}random", icon_url=client.user.avatar_url_as(format='png'))
                    embed.add_field(name=phr['rndtip'],value=highlight(tip))
                    await message.channel.send(embed=embed)
                elif command[1]=='mode':
                    lang=getlang(message.guild.id)
                    pref=getpref(message.guild.id)
                    if pref[0]==message.content[0]:
                        modes=["All Pick","Captains Mode","Random Draft","Single Draft","All Random","Mid Only","Least Played","Custom Mode","Captains Draft","Ability Draft","Event (if available)","All Random Deathmatch","1v1 Solo Mid","All Pick","Turbo"]
                        await message.channel.send(choice(modes))

                elif command[1]=='hero':
                    start = {'ru':['Думаю, ','Стоит попробовать ','Возможно, стоит взять ','Определённо ','Может быть '],'en':['Maybe ','You should try ','Pick ','Try ','Hmm, ', 'Obviously ']}
                    with open('dotabase/heroes.txt', mode='r', encoding='utf-8-sig') as f:
                        heroes=f.readlines()
                    hero=dict(eval(choice(heroes)))
                    embed = discord.Embed(title=choice(start[lang])+f'<{hero["emoji"]}>**{hero["name"]}**',colour=discord.Colour(0xd0021b))
                    embed.set_image(url=f'http://cdn.dota2.com/apps/dota2/images/heroes/{hero["icon"]}')
                    embed.set_footer(text=f"{client.user.name} | {pref}random", icon_url=client.user.avatar_url_as(format='png'))
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(phr['404'])
            
        
