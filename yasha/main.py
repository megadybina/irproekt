import asyncio
import discord
import aiohttp
import random
from os import remove
import requests
import json
from picmaker import *
from randomki import *
from tools import *
from bothelp import *
import dotainfo
from discord.ext import tasks, commands
import time
import datetime
from time import time as currenttime
from time import ctime,gmtime,strftime
import shutil
import logging
from pprint import pprint as pp

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
with open('token.txt','r') as f:
    TOKEN=f.read()
client = discord.Client()


#подключение к серверу
@client.event
async def on_guild_join(guild):
            embed = discord.Embed(title="Setup", colour=discord.Colour(0xd0021b), url="https://discordapp.com")
            embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url_as(format='png'))
            embed.add_field(name="Hello!", value="First pick a language by choosing a flag below\n (Note: only admins can use this menu)")
            for channel in guild.channels:
                if channel.permissions_for(guild.me).send_messages:
                    try:
                       msg = await channel.send(embed=embed)
                       setupchannel=channel
                       break
                    except:
                       pass
            await msg.add_reaction(":ru:553975997389864978")
            await msg.add_reaction(":en:553975997515694141")
    
            def check(reaction,user):
                perm=dict(user.guild_permissions)
                return perm["administrator"] and user.id!=537272694018932754 and reaction.message.channel==setupchannel
    

            lang = await client.wait_for('reaction_add',check=check)
            if str(lang[0])=="<:ru:553975997389864978>":
                langset="ru"
                embed = discord.Embed(title="Настройка", colour=discord.Colour(0xd0021b), url="https://discordapp.com")
                embed.set_footer(text=f"{client.user.name} | Настройка", icon_url=client.user.avatar_url_as(format='png'))
                embed.add_field(name="Установлен русский язык", value="Теперь отправьте в чат сообщение, содержащее префикс для команд (Пример: ! или +)\nПрефикс должен состоять из одного символа \nЕсли на сервере есть другие боты, то убедитесь, что выбранный префикс не используется другими ботами")            
            elif str(lang[0])=="<:en:553975997515694141>":
                langset="en"
                embed = discord.Embed(title="Setup", colour=discord.Colour(0xd0021b), url="https://discordapp.com")
                embed.set_footer(text=f"{client.user.name} | Setup", icon_url=client.user.avatar_url_as(format='png'))
                embed.add_field(name="English language set", value="Now write a message with a prefix that will be used for commands(e.g. ! or +) \nYou must use one symbol only as a prefix \nIf there are other bots on the server make sure that the chosen prefix is not used by other bots")

            def check(msg):
                perm=dict(msg.author.guild_permissions)
                return perm["administrator"] and msg.author.id!=537272694018932754 and msg.channel==setupchannel and len(msg.content)==1

            await msg.clear_reactions()
            await msg.edit(embed=embed)
            prefixmsg = await client.wait_for('message',check=check)

                
            f=open('dotabase/serversettings.txt', 'r')
            lines = f.readlines()
            exists=False
            serversettings={"server_id":msg.guild.id,"lang":langset,"prefix":prefixmsg.content}
            for line in lines:
                t=dict(eval(line))
                if msg.guild.id==t["server_id"]:
                    f = open("dotabase/serversettings.txt","w")
                    for line in lines:
                        t1=dict(eval(line))
                        if msg.guild.id!=t1["server_id"]:
                            f.write(line)
                        if msg.guild.id==t1["server_id"]:
                            f.write("{0}\n".format(serversettings))
                    f.close()
                    exists=True
                    break
                    
            if exists==False:
                f=open('dotabase/serversettings.txt', 'a')
                f.write("{0}\n".format(serversettings))
                f.close()

            if langset=="ru":
                embedfin = discord.Embed(title="Настройка завершена", colour=discord.Colour(0xd0021b), url="https://discordapp.com")
                embedfin.set_footer(text=f"{client.user.name} | Настройка ", icon_url=client.user.avatar_url_as(format='png'))
                embedfin.add_field(name="Готово!", value="Чтобы получить краткое описание меня и список доступных команд введите {}help".format(prefixmsg.content))            
            elif langset=="en":
                embedfin = discord.Embed(title="Setup complete", colour=discord.Colour(0xd0021b), url="https://discordapp.com")
                embedfin.set_footer(text=f"{client.user.name} | Setup", icon_url=client.user.avatar_url_as(format='png'))
                embedfin.add_field(name="All done!", value="To get a short description of me and all the list of available commands use {}help".format(prefixmsg.content))
            await msg.edit(embed=embedfin)
            await msg.add_reaction("✅")


####################      


@client.event
async def on_message(message):
    message.content=message.content.lower()
        
#####Меню настроек   
    if message.content.startswith('settings',1):

        responses={"en":{"title":"Bot settings",
                         "cur_lang":"Current language",
                         "cur_lang_value":"English <:en:553975997515694141>",
                         "cur_pref":"Current prefix",
                         "edit":"Editing",
                         "edit_guide":"To change language to russian press {0}\nTo change the sevrer prefix press {1} and then send a message with a new prefix\n To cancel press {2} \n(Note: only admins can use this menu)".format("<:ru:553975997389864978>",u"\U0001F523","❌"),
                         "pref_change":"Changing prefix",
                         "pref_change_value":"Send a message with a new prefix \nYou must use one symbol only as a prefix",
                         },
                         
                   "ru":{"title":"Настройки бота",
                         "cur_lang":"Установленный язык",
                         "cur_lang_value":"Русский <:ru:553975997389864978>",
                         "cur_pref":"Установленный",
                         "edit":"Внесение изменений",
                         "edit_guide":"Для смены языка на английский нажмите {0}\nДля смены префикса команд нажмите {1} и потом отправьте в чат сообщение с новым префиксом\nДля отмены {2} \n(Примечание: Только админы могут вносить изменения в настройки бота)".format("<:uk:553975997515694141>",u"\U0001F523","❌"),
                         "pref_change":"Смена префикса",
                         "pref_change_value":"Отправьте сообщение с новым префиксом \nПрефикс должен состоять из одного символа",
                         }}
        lang=getlang(message.guild.id)
        pref=getpref(message.guild.id)
        if pref==message.content[0]:
            embed = discord.Embed(title=f"{responses[f'{lang}']['title']}", colour=discord.Colour(0xd0021b), url="https://discordapp.com")
            embed.set_footer(text=f"{client.user.name} | {pref}settings", icon_url=client.user.avatar_url_as(format='png'))
            embed.add_field(name=f"{responses[f'{lang}']['cur_lang']}", value=f"{responses[f'{lang}']['cur_lang_value']}")
            embed.add_field(name=f"{responses[f'{lang}']['cur_pref']}", value=f"{pref}")
            embedinfo=embed
            embed.add_field(name=f"{responses[f'{lang}']['edit']}", value=f"{responses[f'{lang}']['edit_guide']}")
            msg = await message.channel.send(embed=embed)
            
            if lang=="en":
                await msg.add_reaction(":ru:553975997389864978")
            else:
                await msg.add_reaction(":en:553975997515694141")
            await msg.add_reaction(u"\U0001F523")
            await msg.add_reaction("❌")
            
        
        def check(reaction,user): #admin check
            perm=dict(user.guild_permissions)
            return perm["administrator"] and user.id!=537272694018932754 and msg.id==reaction.message.id
        
        react = await client.wait_for("reaction_add",check=check)

        #Отмена        
        if str(react[0])=="❌":
            await msg.clear_reactions()
            await msg.edit(embed=embedinfo)
            
        #смена префикса    
        if str(react[0])==u"\U0001F523":
            def check(msg):#admin check
                perm=dict(msg.author.guild_permissions)
                return perm["administrator"] and msg.author.id!=537272694018932754 and len(msg.content)==1 and msg.content!=' '

            await msg.clear_reactions()
            embed = discord.Embed(title=f"{responses[f'{lang}']['title']}", colour=discord.Colour(0xd0021b), url="https://discordapp.com")
            embed.set_footer(text=f"{client.user.name} | {pref}settings", icon_url=client.user.avatar_url_as(format='png'))
            embed.add_field(name=f"{responses[f'{lang}']['pref_change']}", value=f"{responses[f'{lang}']['pref_change_value']}")
            await msg.edit(embed=embed)
            
            prefixmsg = await client.wait_for('message',check=check)
            serversettings={"server_id":msg.guild.id,"lang":lang,"prefix":prefixmsg.content}

            f=open('dotabase/serversettings.txt', 'r')
            lines = f.readlines()
            for line in lines:
                t=dict(eval(line))
                if msg.guild.id==t["server_id"]:
                    f = open("dotabase/serversettings.txt","w")
                    for line in lines:
                        t1=dict(eval(line))
                        if msg.guild.id!=t1["server_id"]:
                            f.write(line)
                        if msg.guild.id==t1["server_id"]:
                            f.write("{0}\n".format(serversettings))
                    f.close()
                    break
            await prefixmsg.add_reaction("✅")
            pref=prefixmsg.content
            embedinfo.remove_field(1)
            embedinfo.insert_field_at(1,name=f"{responses[f'{lang}']['cur_pref']}", value=f"{prefixmsg.content}",inline=True)
            await msg.edit(embed=embedinfo)
            
            
         #смена языка  
        if str(react[0])=="<:ru:553975997389864978>" or str(react[0])=="<:en:553975997515694141>":
            lang=str(react[0])
            lang=lang[2:4]
            serversettings={"server_id":msg.guild.id,"lang":lang,"prefix":pref}
            f=open('dotabase/serversettings.txt', 'r')
            lines = f.readlines()
            for line in lines:
                t=dict(eval(line))
                if msg.guild.id==t["server_id"]:
                    f.close()
                    f = open("dotabase/serversettings.txt","w")
                    for line in lines:
                        t1=dict(eval(line))
                        if msg.guild.id!=t1["server_id"]:
                            f.write(line)
                        if msg.guild.id==t1["server_id"]:
                            f.write("{0}\n".format(serversettings))
                    f.close()
                    break
            await msg.clear_reactions()
            embed = discord.Embed(title=f"{responses[f'{lang}']['title']}", colour=discord.Colour(0xd0021b), url="https://discordapp.com")
            embed.set_footer(text=f"{client.user.name} | {pref}settings", icon_url=client.user.avatar_url_as(format='png'))
            embed.add_field(name=f"{responses[f'{lang}']['cur_lang']}", value=f"{responses[f'{lang}']['cur_lang_value']}")
            embed.add_field(name=f"{responses[f'{lang}']['cur_pref']}", value=f"{pref}")
            await msg.edit(embed=embed)            
            await msg.add_reaction("✅")

        

#профиль пользователя#                                     
    if message.content.startswith('profile',1):
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'

        responses={"en":{"bad_steamid":"User with this ID was not found",
                         "invalid_id":"Invalid ID",
                         "error":"An error occured",
                         "recent_unav":"Recent matches unavailable. Maybe [OpenDota](https://www.opendota.com) is down?",
                         "later":"Make sure this profile is public and try again in a bit",
                         "private":"This profile is private",
                         "no_steamid":f'Your SteamID is not in the database. Send a message with your ID after {pref[0]}steamid',
                         "dotaprof":"DOTA 2 profile",
                         "rpgprof":"RPG profile",
                         "lvl":"Level",
                         "rpgitems":"Items",
                         "matchcount":"Total matches",
                         "winlose":"Won / lost",
                         "BCpart":"Battle Cup participations",
                         "BCwins":"Battle Cup victories",
                         "top_heroes":"Top heroes",
                         "mostmatchesheroes":"Most picked heroes",
                         "topwinrateheroes":"Highest winrate",
                         'recent':'Recent matches',
                         'date':'Date',
                         'id':'Match ID',
                         'hero':'Hero',
                         'gm':'Game mode'},
                         
                   "ru":{"bad_steamid":"Пользователь с таким ID не найден",
                         "invalid_id":"Недопустимый ID",
                         "error":"Возникла ошибка",
                         "recent_unav":"Недавние матчи недоступны. Может [OpenDota](https://www.opendota.com) не работает?",
                         "later":"Убедитесь, что этот профиль публичный и попробуйте через пару минут",
                         "private":"История матчей этого профиля приватна",
                         "no_steamid":f'Вашего SteamID нет в базе данных. Введите ваш ID после команды {pref[0]}steamid',
                         "dotaprof":"Профиль DOTA 2",
                         "rpgprof":"RPG Профиль",
                         "lvl":"Уровень",
                         "rpgitems":"Предметы",
                         "matchcount":"Всего матчей",
                         "winlose":"Побед / поражений",
                         "BCpart":"Участий в Боевом Кубке",
                         "BCwins":"Побед в Боевом Кубке",
                         "top_heroes":"Лучшие герои",
                         "mostmatchesheroes":"Наибольшее число матчей",
                         "topwinrateheroes":"Наибольшая доля побед",
                         'recent':'Недавние матчи',
                         'date':'Дата',
                         'id':'ID матча',
                         'hero':'Герой',
                         'gm':'Режим игры'}}

        phr=responses[lang]
        if pref==message.content[0]:
            await message.add_reaction("⏳")
            
            playerid,adres=None,None
            command=message.content.split()
            if len(command)==2:                 ##разбор запроса пользователя
                if command[1].isdigit():
                    playerid=command[1]
                    adres=message.channel
                elif command[1].lower()=='private':
                    user=get_user(message.author.id)
                    if user!=None:
                        playerid=user['steam_id']
                    else:
                        await message.channel.send(phr['no_steamid'])
                        return
                    adres=message.author
                else:
                    await message.channel.send(phr["error"])
                    return
                
            elif len(command)==3:
                if command[2].lower()=='private':
                    adres=message.author
                    if command[1].isdigit():
                        playerid=command[1]
                    else:
                        await message.channel.send(phr["invalid_id"])
                        return                               
                elif command[1].lower()=='private':
                    adres=message.author
                    if command[2].isdigit():
                        playerid=command[2]
                    else:
                        await message.channel.send(phr["invalid_id"])
                        return  
                else:
                    await message.channel.send(phr["error"])
                    return                    
            else:
                user=get_user(message.author.id)
                if user!=None:
                    playerid=user['steam_id']
                else:
                    await message.channel.send(phr['no_steamid'])
                    return
                adres=message.channel

                
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.stratz.com/api/v1/Player/{playerid}") as r:
                        user=json.loads(await r.text())
            except:
                if int(r.status)==403:       ##403 - доступ запрещен --> профиль приватный
                    await message.channel.send(f'{phr["error"]}: {phr["private"]}')
                else:
                    await message.channel.send(f'{phr["error"]}: {r.status}. {phr["later"]}')
                return
            
            bk_profile=''
            try:                    #запрос инфы о боевом кубке
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.stratz.com/api/v1/Player/{playerid}/matches?lobbyType=9&take=250") as r:
                        bkinfo=json.loads(await r.text())
                trophy=''
                countbk,countt,countparts=0,0,0
                for el in reversed(bkinfo):
                    if el['didRadiantWin'] == el['players'][0]['isRadiant']:
                        countt+=1
                        if countt==3:
                            countbk+=1
                            countparts+=1
                            countt=0
                    else:
                        countt=0
                        countparts+=1
                if countbk>0:
                    trophy=u"\U0001F3C6"
                bk_profile=phr['BCpart']+': **'+str(countparts)+'**\n'+phr['BCwins']+f': {trophy}**'+str(countbk)+'**'
            except:
                pass
            plus=''
            if user['steamAccount'].get('isDotaPlusSubscriber',False):
                plus+='<:dotaplus:591631737172393997>'

            steam_url=user["steamAccount"].get("profileUri","https://discordapp.com")               
            embed = discord.Embed(title=f'**{user["steamAccount"]["name"]}**'+plus,colour=discord.Colour(0xccc21f),url=steam_url)

            matches=user.get('matchCount',0)
            wins=user.get('winCount',0)
            dota_profile=phr['matchcount']+': **'+str(matches)+'**\n'+phr['winlose']+": **"+str(wins)+'** / **'+str(matches-wins)+'**'

            rank=user['steamAccount'].get('seasonRank',"00")            
            makerang(rank)
            frank=discord.File(fp=f"{rank}.png")
            embed.set_thumbnail(url=f"attachment://{rank}.png") 
           
            embed.add_field(name='**'+phr['dotaprof']+'**',value=dota_profile+'\n'+bk_profile,inline=False)

            most_heroes=''
            best_heroes=''
            try:           #запрос инфы о топ героях юзера
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.stratz.com/api/v1/Player/{playerid}/heroPerformance") as r:
                        bestheroes=json.loads(await r.text())
                        mostheroes=json.loads(await r.text())
            except:
                if int(r.status)==403:
                    await message.channel.send(f'{phr["error"]}: {phr["private"]}')
                else:
                    await message.channel.send(f'{phr["error"]}: {r.status}. {phr["later"]}')
                return
            most_h_list=[]
            best_h_list=[]
            def getwinrate(hero):
                if hero['matchCount']>20:
                    return hero['winCount']/hero['matchCount']
                else:
                    return 0
            most_h_list = sorted(mostheroes, key=lambda k: k['matchCount'],reverse=True)
            best_h_list = sorted(bestheroes, key=lambda k: getwinrate(k),reverse=True)

            with open('dotabase/heroes.txt','r', encoding='utf-8-sig') as f:
                lines=f.readlines()
            for el in most_h_list[:3]:    
                for line in lines:
                    hero=dict(eval(line))
                    if hero['id']==el['heroId']:
                        tot=str(el['matchCount'])
                        if len(tot)>3:
                            tot=tot[:-3]+','+tot[-3:]
                        most_heroes+='<'+hero['emoji']+'>'+u"\u2800"+'**'+tot+'**\n'
            for el in best_h_list[:3]:
                for line in lines:
                    hero=dict(eval(line))
                    if hero['id']==el['heroId']:
                        wr=str(int(el['winCount']/el['matchCount']*100))+'%'
                        best_heroes+='<'+hero['emoji']+'>'+u"\u2800"+'**'+wr+f'** ({el["winCount"]} / {el["matchCount"]-el["winCount"]})'+'\n'
            embed.add_field(name='__'+phr['mostmatchesheroes']+'__',value=most_heroes,inline=True)
            embed.add_field(name='__'+phr['topwinrateheroes']+'__',value=best_heroes,inline=True)
            try:
                lobby={-1:'Invalid',0:'Unranked',1:'Practice',2:'Tournament',3:'Tutorial',4:'Coop vs Bots',5:'Team Match',6:'Solo Queue',7:'Ranked',8:'Solo Mid',9:'Battle Cup'}
                gamemodes={1:"All Pick",2:"Captains Mode",3:"Random Draft",4:"Single Draft",5:"All Random",11:"Mid Only",12:"Least Played",15:"Custom Mode",16:"Captains Draft",18:"Ability Draft",19:"Event",20:"All Random Deathmatch",21:"1v1 Solo Mid",22:"All Pick",23:"Turbo"}
                recent_matches=''
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.opendota.com/api/players/{playerid}/recentMatches") as r:
                        recent = json.loads(await r.text())
                        if len(recent)>10:
                            recent=recent[:10]
                        for match in recent:
                            for line in lines:
                                hero=dict(eval(line))
                                if hero['id']==match['hero_id']:
                                    win='**Lose**'
                                    if match['radiant_win'] and match['player_slot']<=127:
                                        win='**Win**'
                                    if not match['radiant_win'] and match['player_slot']>127:
                                        win='**Win**'
                                    if lobby.get(match['lobby_type'],'')=='Ranked':
                                        recent_matches+='<'+hero['emoji']+'>'+u"\u2800"*2+strftime('%H:%M %d/%m/%y',gmtime(match['start_time']))+u"\u2800"*2+str(match['match_id'])+u"\u2800"*2+lobby.get(match['lobby_type'],'')+' '+gamemodes.get(match['game_mode'],'')+'\n'
                                    else:
                                        recent_matches+='<'+hero['emoji']+'>'+u"\u2800"*2+strftime('%H:%M %d/%m/%y',gmtime(match['start_time']))+u"\u2800"*2+str(match['match_id'])+u"\u2800"*2+gamemodes.get(match['game_mode'],'')+'\n'
                        embed.add_field(name='__'+phr['recent']+'__\n'+phr['hero']+u"\u2800"*2+phr['date']+u"\u2800"*8+phr['id']+u"\u2800"*5+phr['gm'],value=recent_matches)
                        len(recent_matches)
                                        
            except:
                embed.add_field(name='__'+phr['recent']+'__\n'+phr['hero']+u"\u2800"*2+phr['date']+u"\u2800"*8+phr['id']+u"\u2800"*5+phr['gm'],value=phr['recent_unav'])
            await adres.send(embed=embed,file=frank)
            await message.clear_reactions()
            remove(f'{rank}.png') 
             
###history
    if message.content.startswith('matches',1):
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'

        responses={"en":{"bad_steamid":"User with this ID was not found",
                         "error":"An error occured",
                         "later":"Make sure this profile is public and try again in a bit",
                         "private":"This profile is private",
                         "no_steamid":f'Your SteamID is not in the database. Send a message with your ID after {pref[0]}steamid',
                         "dotaprof":"DOTA 2 profile",
                         "rpgprof":"RPG profile",
                         "lvl":"Level",
                         "rpgitems":"Items",
                         "matchcount":"Total matches",
                         'history':'Match history',
                         'date':'Date',
                         'id':'Match ID',
                         'hero':'Hero',
                         'gm':'Game mode',
                         'matches':'Matches of player ',
                         'all':'All ',
                         'won':'Matches won by player ',
                         'lost':'Matches lost by player ',
                         'as':' as ',
                         'with':' with ',
                         'and':' and ',
                         'against':' against ',
                         'patch':' during patch ',
                         '404':'Nothing here('},
                         
                   "ru":{"bad_steamid":"Пользователь с таким ID не найден",
                         "error":"Возникла ошибка",
                         "later":"Убедитесь, что этот профиль публичный и попробуйте через пару минут",
                         "private":"История матчей этого профиля приватна",
                         "no_steamid":f'Вашего SteamID нет в базе данных. Введите ваш ID после команды {pref[0]}steamid',
                         "rpgitems":"Предметы",
                         "matchcount":"Всего матчей",
                         'history':'Match history',
                         'date':'Дата',
                         'id':'ID матча',
                         'hero':'Герой',
                         'gm':'Режим игры',
                         'matches':'Матчи игрока ',
                         'all':'Все ',
                         'won':'Выигранные матчи игрока ',
                         'lost':'Проигранные матчи игрока ',
                         'as':' за ',
                         'with':' с ',
                         'and':' и ',
                         'against':' против ',
                         'patch':' в патче ',
                         '404':'Пусто('}}
                
        phr=responses[lang]
        command=message.content+' '
        if pref==message.content[0]:
            user=get_user(message.author.id)
            if user!=None:
                playerid=user['steam_id']
            else:
                await message.channel.send(phr['no_steamid'])
                return
            await message.add_reaction("⏳")
            '''
            version = None       #версия игры
            with open('dotabase/version.txt','r') as f:
                versions=dict(eval(f.read()))
                for ver in versions.keys():
                    if ver in command:
                        version = versions[ver]
                        break
            ''' 
            win = None        #победа / поражение
            if 'win' in command or 'won' in command or 'victory' in command:
                win=1
            if 'lose' in command or 'lost' in command:
                win=0
            sign = 1
            if ' all ' in command:
                sign=0
            
            hero = None   #Герой пользователя и герои в команде союзников / врагов
            allies,enemies=[],[]
            searchcom=command.replace('-','')
            searchcom=searchcom.replace('+','')
            with open('dotabase/heroes.txt','r', encoding='utf-8-sig') as f:
                heroes=f.readlines()
                for fhero in heroes:
                    h=dict(eval(fhero))
                    if any(al in searchcom.split() for al in h['aliases']):
                        for al in h['aliases']:
                            alindex=command.find(al)
                            if alindex!=-1:
                                if command[alindex-1]==' ':
                                    hero={'name':h['name'],'id':h['id'],'emoji':h['emoji']}
                                elif command[alindex-1]=='-':
                                    enemies.append({'name':h['name'],'id':h['id'],'emoji':h['emoji']})
                                elif command[alindex-1]=='+':
                                    allies.append({'name':h['name'],'id':h['id'],'emoji':h['emoji']})
                
                    elif command.find(h['name'].lower())!=-1:
                        index=command.find(h['name'].lower())
                        if index!=-1:
                            if command[index-1]==' ':
                                hero={'name':h['name'],'id':h['id'],'emoji':h['emoji']}
                            elif command[index-1]=='-':
                                enemies.append({'name':h['name'],'id':h['id'],'emoji':h['emoji']})
                            elif command[index-1]=='+':
                                allies.append({'name':h['name'],'id':h['id'],'emoji':h['emoji']})
                    elif command.find((h['name'].replace("'","")).lower())!=-1:
                        index=command.find((h['name'].replace("'","")).lower())
                        if index!=-1:
                            if command[index-1]==' ':
                                hero={'name':h['name'],'id':h['id'],'emoji':h['emoji']}
                            elif command[index-1]=='-':
                                enemies.append({'name':h['name'],'id':h['id'],'emoji':h['emoji']})
                            elif command[index-1]=='+':
                                allies.append({'name':h['name'],'id':h['id'],'emoji':h['emoji']})
                                
            # passing an array --> https://api.opendota.com/api/players/130403136/matches?with_hero_id[]=31&with_hero_id[]=102
            query=f'https://api.opendota.com/api/players/{playerid}/matches?limit=100&'
            params,desc=[],''
            
            if sign==0:
                params.append(f"significant=0")
                desc+=phr['all']
                
            if win!=None:
                params.append(f"win={win}")
                if sign==0:
                    if win==1:
                        desc+=phr['won'].lower()+str(playerid)
                    else:
                        desc+=phr['lost'].lower()+str(playerid)
                else:
                    if win==1:
                        desc+=phr['won']+str(playerid)
                    else:
                        desc+=phr['lost']+str(playerid)
            else:
                if sign==0:
                    desc+=phr['matches'].lower()+str(playerid)
                else:
                    desc+=phr['matches']+str(playerid)
                
            if hero!=None:
                params.append(f"hero_id={hero['id']}")
                desc+=phr['as']+f'<{hero["emoji"]}>**{hero["name"]}**'
                
                
            if allies!=[]:
                if len(allies)>1:
                    al=[]
                    for ally in allies:
                        params.append(f"with_hero_id[]={ally['id']}")
                        al.append(f'<{ally["emoji"]}>**{ally["name"]}**')
                    desc+=phr['with']+phr['and'].join(al)
                else:
                    params.append(f"with_hero_id={allies[0]['id']}")
                    desc+=phr['with']+f'<{allies[0]["emoji"]}>**{allies[0]["name"]}**'
            if enemies!=[]:
                if len(enemies)>1:
                    en=[]
                    for enemy in enemies:
                        params.append(f"against_hero_id[]={enemy['id']}")
                        en.append(f'<{enemy["emoji"]}>**{enemy["name"]}**')
                    desc+=phr['against']+phr['and'].join(en)
                else:
                    params.append(f"against_hero_id={enemies[0]['id']}")
                    desc+=phr['against']+f'<{enemies[0]["emoji"]}>**{enemies[0]["name"]}**'               
            '''
            if version!=None:
                params.append(f"patch={version}")
                desc+=phr['patch']+ver
            '''
            query=query+"&".join(params)
            try:           
                async with aiohttp.ClientSession() as session:
                    async with session.get(query) as r:
                        matches=json.loads(await r.text())
            except:
                await message.channel.send(f'{phr["error"]}: {r.status}')
                return

            page_emojis=['<:page_1:599965301496348722>','<:page_2:599965301466988545>','<:page_3:599965301504999444>','<:page_4:599965301496348711>','<:page_5:599965301500542995>','<:page_6:599965301295153153>','<:page_7:599965301366456342>','<:page_8:599965301513125898>','<:page_9:599965301500542987>','<:page_10:599965301525839897>']    
            lobby={-1:'Invalid',0:'Unranked',1:'Practice',2:'Tournament',3:'Tutorial',4:'Coop vs Bots',5:'Team Match',6:'Solo Queue',7:'Ranked',8:'Solo Mid',9:'Battle Cup'}
            gamemodes={1:"All Pick",2:"Captains Mode",3:"Random Draft",4:"Single Draft",5:"All Random",11:"Mid Only",12:"Least Played",15:"Custom Mode",16:"Captains Draft",18:"Ability Draft",19:"Event",20:"All Random Deathmatch",21:"1v1 Solo Mid",22:"All Pick",23:"Turbo"}
            with open('dotabase/gamemodes.txt','r') as f:
                gamemodes=dict(eval(f.read()))
            with open('dotabase/lobby.txt','r') as f:
                lobby=dict(eval(f.read()))
            ##создание сообщения со списком игр
            n=len(matches)
            embed = discord.Embed(title=f'{phr["history"]}',colour=discord.Colour(0x22bf5a),url='https://www.opendota.com')
            embed.set_footer(text=f"{client.user.name} | {pref}matches | {phr['matchcount']}: {n}", icon_url=client.user.avatar_url_as(format='png'))
            embed.description=desc
            countm,countp,pages=0,0,{}
            page=''
            for match in matches:
                if hero!=None:
                    if lobby.get(match['lobby_type'],'')=='Ranked':
                        page+='<'+hero['emoji']+'>'+u"\u2800"*2+strftime('%H:%M %d/%m/%y',gmtime(match['start_time']))+u"\u2800"*2+str(match['match_id'])+u"\u2800"*2+lobby.get(match['lobby_type'],'')+' '+gamemodes.get(match['game_mode'],'')+'\n'
                    else:
                        page+='<'+hero['emoji']+'>'+u"\u2800"*2+strftime('%H:%M %d/%m/%y',gmtime(match['start_time']))+u"\u2800"*2+str(match['match_id'])+u"\u2800"*2+gamemodes.get(match['game_mode'],'')+'\n'
                else:
                    for fhero in heroes:
                        h=dict(eval(fhero))
                        if h['id']==match['hero_id']:
                            if lobby.get(match['lobby_type'],'')=='Ranked':
                                page+='<'+h['emoji']+'>'+u"\u2800"*2+strftime('%H:%M %d/%m/%y',gmtime(match['start_time']))+u"\u2800"*2+str(match['match_id'])+u"\u2800"*2+lobby.get(match['lobby_type'],'')+' '+gamemodes.get(match['game_mode'],'')+'\n'
                            else:
                                page+='<'+h['emoji']+'>'+u"\u2800"*2+strftime('%H:%M %d/%m/%y',gmtime(match['start_time']))+u"\u2800"*2+str(match['match_id'])+u"\u2800"*2+gamemodes.get(match['game_mode'],'')+'\n'
                            break
                countm+=1
                if countm==10:
                    if len(matches)==10:
                        embed.add_field(name=phr['hero']+u"\u2800"*2+phr['date']+u"\u2800"*8+phr['id']+u"\u2800"*5+phr['gm'],value=page)
                        hist = await message.channel.send(embed=embed)
                        return
                    pages[page_emojis[countp]]=page
                    countp+=1
                    countm=0
                    page=''
                if n==countm+countp*10 and n%10!=0:
                    pages[page_emojis[countp]]=page

                    
            if countp==0 and countm==0:
                embed.clear_fields()
                embed.add_field(name=phr['hero']+u"\u2800"*2+phr['date']+u"\u2800"*8+phr['id']+u"\u2800"*5+phr['gm'],value=phr['404'])
                hist = await message.channel.send(embed=embed)
                return
            if countm<10 and countp==0:
                embed.add_field(name=phr['hero']+u"\u2800"*2+phr['date']+u"\u2800"*8+phr['id']+u"\u2800"*5+phr['gm'],value=page)
                hist = await message.channel.send(embed=embed)
            else:
                embed.add_field(name=phr['hero']+u"\u2800"*2+phr['date']+u"\u2800"*8+phr['id']+u"\u2800"*5+phr['gm'],value=pages['<:page_1:599965301496348722>'])
                hist = await message.channel.send(embed=embed)
                for pagenumber in pages.keys():
                    await hist.add_reaction(pagenumber)
                await hist.add_reaction('❌')
            
                def check(reaction,user):
                    return user.id==message.author.id and reaction.message.id==hist.id
            
                react = await client.wait_for("reaction_add",check=check)
            
                while str(react[0])!="❌":
                    if str(react[0]) in pages.keys():
                        embed.clear_fields()
                        embed.add_field(name=phr['hero']+u"\u2800"*2+phr['date']+u"\u2800"*8+phr['id']+u"\u2800"*5+phr['gm'],value=pages[str(react[0])])
                        await hist.edit(embed=embed)
                    react = await client.wait_for("reaction_add",check=check)
                await hist.clear_reactions()


            
#HELPHELPHELP

    if message.content.startswith('help',1):
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'

        command=message.content.split()
        if pref==message.content[0]:
            if len(command)>=2:
                await helpcom(message,client,command[1],lang,pref)
            else:
                reacts=['<a:matchinfo:595952615599374337>','<:exp:593470312088338441>','<a:coinflip:594438507938709524>',u"\U0001F916"]
                mainhelp = helpmain(message,client,lang,pref)
                helpmsg = await message.channel.send(embed=mainhelp)
                for react in reacts:
                    await helpmsg.add_reaction(react)
                await helpmsg.add_reaction('❌')

                def check(reaction,user):
                    return user.id==message.author.id
                react = await client.wait_for("reaction_add",check=check)
                
                while str(react[0])!="❌":
                    if str(react[0]) in reacts:
                        infoemb = await helpcom(message,client,str(react[0]),lang,pref)
                        await helpmsg.clear_reactions()
                        await helpmsg.edit(embed=infoemb)
                        await helpmsg.add_reaction('↩')
                    if str(react[0]) == '↩':
                        await helpmsg.clear_reactions()
                        await helpmsg.edit(embed=mainhelp)
                        for react in reacts:
                            await helpmsg.add_reaction(react)
                        await helpmsg.add_reaction('❌')
                    react = await client.wait_for("reaction_add",check=check)
                await helpmsg.clear_reactions()


#рандомки#         

    await randomstuff(message,client)

    await roll(message,client)


### информация

    await dotainfo.patch(message,client)

    await dotainfo.hero(message,client)

    await dotainfo.abs(message,client)

    await dotainfo.item(message,client)

    await dotainfo.ability(message,client)

    if (message.content.startswith('info',1) and message.content.endswith('info')) or (message.content.startswith('tome',1) and message.content.endswith('tome')):
        mainembed = dotainfo.info(message,client,'main')
        page_emojis=['<:page_0:599965301676965890>','<:page_1:599965301496348722>','<:page_2:599965301466988545>','<:page_3:599965301504999444>','<:page_4:599965301496348711>','<:page_5:599965301500542995>','<:page_6:599965301295153153>','<:page_7:599965301366456342>','<:page_8:599965301513125898>','<:page_9:599965301500542987>','<:page_10:599965301525839897>']
        info = await message.channel.send(embed=mainembed['msg'])
        cats = mainembed['emojis']
        for emoji in cats:
            await info.add_reaction(emoji)
        await info.add_reaction('❌')
        in_main=True
        in_cat=False
        
        def check(reaction,user):
            return user.id==message.author.id and reaction.message.id==info.id
        react = await client.wait_for("reaction_add",check=check)
        while str(react[0])!="❌":
            if str(react[0]) in cats.keys() and in_main==True:
                mecembed = dotainfo.info(message,client,cats[str(react[0])])
                await info.clear_reactions()
                await info.edit(embed=mecembed['msg'])
                mecs = mecembed['emojis']
                for emoji in mecs:
                    await info.add_reaction(emoji)
                await info.add_reaction('↩')
                in_main=False
                in_cat=True
            else:
                if str(react[0]) in mecs.keys() and in_main==False:
                        mechanic = dotainfo.info(message,client,mecs[str(react[0])])
                        await info.edit(embed=mechanic)
                        await info.add_reaction('↩')
                        await info.add_reaction('⏪')
                        in_cat=False

            
                  
            if str(react[0]) == '↩':
                try:
                    if in_cat==True:
                        await info.clear_reactions()
                        await info.edit(embed=mainembed['msg'])
                        for emoji in cats:
                            await info.add_reaction(emoji)
                        await info.add_reaction('❌')
                        in_main=True
                    else:
                        await info.clear_reactions()
                        await info.edit(embed=mecembed['msg'])
                        for emoji in mecs:
                            await info.add_reaction(emoji)
                        await info.add_reaction('↩')
                        in_cat=True
                except:
                    pass

            if str(react[0]) == '⏪':
                try:
                    await info.clear_reactions()
                    await info.edit(embed=mainembed['msg'])
                    for emoji in cats:
                        await info.add_reaction(emoji)
                    await info.add_reaction('❌')
                    in_main=True
                    in_cat=False
                except:
                    pass

                
            react = await client.wait_for("reaction_add",check=check)
        await info.clear_reactions()

######                                                                  
    if message.content.startswith('matchinfo',1) or message.content.startswith('lastmatchinfo',1):
        startt=currenttime()
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'
        responses={"en":{"bad_matchid":"Invalid match ID",
                         "error":"An error occured",
                         "oddown":"Can't connect to OpenDota. Trying to connect to STRATZ",
                         "stratzdead":"Can't connect to STRATZ",
                         "later":"Make sure your profile is public and try again later",
                         "no_steamid":f'Your SteamID is not in the database. Send a message with your ID after {pref}steamid',
                         "match":"Match",
                         "gamemode":"Game mode",
                         "map":"Buildings map",
                         "draft":"Draft",
                         "picks":"Picks",
                         "bans":"Bans",
                         "runes":"Rune pickups",
                         "league":"League",
                         "radiant_team":"Radiant team",
                         "dire_team":"Dire team",
                         "summary":"Summary",
                         "rad_score":"Radiant score",
                         "dire_score":"Dire score",
                         "exp":"Experience",
                         "nw":"Net Worth",
                         "player_stats":"Player stats",
                         "stats":"Stats",
                         "hero":"Hero",
                         "kda":"Kills/Deaths/Assists",
                         "kda_short":"K/D/A",
                         "lh_den":"Last hits/Denies",
                         "lh_den_short":"LH/D",
                         "gpm_expm":"Gold/Exp per min",
                         "totalgold_exp":"Total gold/exp",
                         "totalgold":"NW",
                         "obs_sen":"Wards placed",
                         "towerdmg_herodmg":"Hero/Building damage",
                         "permbuffs":"Permanent buffs",
                         "adv_graph":"Teams' total gold and experience advantage graph",
                         'killed':'Killed heroes',
                         'killed_by':'Killed by heroes'},
                         
                   "ru":{"bad_matchid":"Некорректный ID матча",
                         "error":"Возникла ошибка",
                         "oddown":"Не удается соединиться с OpenDota. Попытка подключения в к STRATZ",
                         "stratzdead":"Не удается соединиться с STRATZ",
                         "later":"Убедитесь, что ваш профиль публичный и попробуйте позже",
                         "no_steamid":f'Вашего SteamID нет в базе данных. Введите ваш ID после команды {pref}steamid',
                         "match":"Матч",
                         "gamemode":"Режим игры",
                         "map":"Карта построек",
                         "draft":"Драфт",
                         "picks":"Пики",
                         "bans":"Баны",
                         "runes":"Подобранные руны",
                         "league":"Событие",
                         "radiant_team":"Команда сил Света",
                         "dire_team":"Команда сил Тьмы",
                         "summary":"Общая статистика",
                         "rad_score":"Счет сил Света",
                         "dire_score":"Счет сил Тьмы",
                         "exp":"Опыт",
                         "nw":"Общая ценность",
                         "player_stats":"Статистика игрока",
                         "stats":"Статистика",
                         "hero":"Герой",
                         "kda":"Убийств/Смертей/Помощи",
                         "kda_short":"K/D/A",
                         "lh_den_short":"LH/D",
                         "lh_den":"Ласт хитов/Денаев",
                         "gpm_expm":"Золота/Опыта в минуту",
                         "totalgold_exp":"Всего золота/опыта",
                         "totalgold":"NW",
                         "obs_sen":"Установлено вардов",
                         "towerdmg_herodmg":"Урона героям/постройкам",
                         "permbuffs":"Постоянные усиления",
                         "adv_graph":"График преимущества сторон по общему количеству золота и опыта",
                         'killed':'Убийства героев',
                         'killed_by':'Убит героями'}}

        variables={'od':{'radiant_win':'radiant_win',
                         "league_name":"name",
                         "lobby_type":"lobby_type",
                         "game_mode":"game_mode",
                         'radiant_team':'radiant_team',
                         'dire_team':'dire_team',
                         "logo_url":"logo_url",
                         "hero_id":"hero_id",
                         "kills":"kills",
                         "deaths":"deaths",
                         "assists":"assists",
                         "last_hits":"last_hits",
                         "denies":"denies",
                         "picks_bans":"picks_bans",
                         "duration":"duration",
                         "radiant_gold_adv":"radiant_gold_adv",
                         "radiant_xp_adv":"radiant_xp_adv",
                         "rank_tier":"rank_tier",
                         'gold_per_min':'gold_per_min',
                         'xp_per_min':'xp_per_min',
                         'hero_damage':'hero_damage',
                         'tower_damage':'tower_damage',
                         'runetype':'key',
                         "player_slot":"player_slot"},

                   'stratz':{'radiant_win':"didRadiantWin",
                             "league_name":"displayName",
                             "lobby_type":"lobbyType",
                             "game_mode":"gameMode",
                             'radiant_team':'radiantTeam',
                             'dire_team':'direTeam',
                             "logo_url":"logo",
                             "hero_id":"heroId",
                             "kills":"numKills",
                             "deaths":"numDeaths",
                             "assists":"numAssists",
                             "last_hits":"numLastHits",
                             "denies":"numDenies",
                             "picks_bans":"picksBans",
                             "duration":"durationSeconds",
                             "radiant_gold_adv":'radiantNetworthLead',
                             "radiant_xp_adv":'radiantExperienceLead',
                             "rank_tier":"seasonRank",
                             'gold_per_min':'goldPerMinute',
                             'xp_per_min':'experiencePerMinute',
                             'hero_damage':'heroDamage',
                             'tower_damage':'towerDamage',
                             'runetype':'type',
                             "player_slot":"playerSlot"}}



                             
        phr=responses[lang]
        command=message.content.split()
        user_msg=message
        user=get_user(message.author.id)

        if pref==message.content[0]:
                await message.add_reaction("⏳")
                stratz=False
                if command[0]==f'{pref}matchinfo':
                    if len(command)>1:
                        matchid=command[1]
                        if matchid.isalnum()==False:
                            await message.channel.send(phr["bad_matchid"])
                            await message.clear_reactions()
                            return
                    else:
                        await message.channel.send(phr["bad_matchid"])
                        await message.clear_reactions()
                        return
                
                elif command[0]==f'{pref}lastmatchinfo':
                    if user!=None:
                        steamid=user['steam_id']
                        matchid=await get_lm_od(steamid)
                        if type(matchid)!=int:
                            await message.channel.send(f'{phr["error"]}. {phr["oddown"]}')
                            try:
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(f"https://api.stratz.com/api/v1/Player/{steamid}/matches?take=1") as r:
                                        lastmatch = json.loads(await r.text())
                                        matchid=lastmatch[0]['id']
                                        stratz=True
                            except Exception as e:
                                await message.channel.send(f'{phr["error"]}:{phr["stratzdead"]}. {phr["later"]}')
                                await message.clear_reactions()
                                return
                    else:
                        await message.channel.send(phr['no_steamid'])
                        await message.clear_reactions()
                        return
                

                try:                    #запрос инфы о матче
                    if not stratz:
                        matchinfo = await get_match_od(matchid)
                        if matchinfo==0:
                            todel = await message.channel.send(f'{phr["error"]}. {phr["oddown"]}')
                            matchinfo = await get_match_stratz(matchid)
                            stratz=True
                            if matchinfo==0:
                                await message.channel.send(f'{phr["error"]}. {phr["later"]}')
                                await message.clear_reactions()
                                return
                    else:
                        matchinfo = await get_match_stratz(matchid)
                        if matchinfo==0:
                            await message.channel.send(f'{phr["error"]}. {phr["later"]}')
                            await message.clear_reactions()
                            return
                except:
                    await message.channel.send(f'{phr["error"]}. {phr["later"]}')
                    await message.clear_reactions()
                    return
                if stratz:
                    var=variables['stratz']
                else:
                    var=variables['od']
                        
                #цвет рамки
                if matchinfo[var['radiant_win']]==True:
                    radwin=u"\U0001F3C6"
                    direwin=''
                    color=discord.Colour(0xad36)
                else:
                    radwin=''
                    direwin=u"\U0001F3C6"
                    color=discord.Colour(0xd0021b)
  
                embed = discord.Embed(title=f'{phr["match"]} {matchid}',colour=color,url="https://discordapp.com")
                embed.set_footer(text=f"{client.user.name} | {pref}matchinfo | {strftime('%H:%M %d/%m/%y',gmtime(matchinfo['start_time']))} | {get_duration(matchinfo['duration'])}", icon_url=client.user.avatar_url_as(format='png'))

                for guild in client.guilds:
                        if guild.id==594200720048259083:
                            emojiguild=guild
                            break
                #турнир(если есть) или режим игры    
                if matchinfo.get('league',None)!=None:
                        embed.add_field(name='<a:aegis2015:591551743414763543>'+phr["league"],value=matchinfo["league"][var["league_name"]],inline=False)#добавить эмоджи 

                else:
                    lobby={-1:'Invalid',0:'Unranked',1:'Practice',2:'Tournament',3:'Tutorial',4:'Coop vs Bots',5:'Team Match',6:'Solo Queue',7:'Ranked',8:'Solo Mid',9:'Battle Cup'}
                    gamemodes={1:"All Pick",2:"Captains Mode",3:"Random Draft",4:"Single Draft",5:"All Random",11:"Mid Only",12:"Least Played",15:"Custom Mode",16:"Captains Draft",18:"Ability Draft",19:"Event",20:"All Random Deathmatch",21:"1v1 Solo Mid",22:"All Pick",23:"Turbo"}
                    emblobby=lobby.get(matchinfo.get(var["lobby_type"],-1))
                    embmode=gamemodes.get(matchinfo.get(var["game_mode"],-1))
                    if embmode!=-1:
                        gamee=embmode
                    else:
                        modefield_name="-"
                    if emblobby!=-1:
                        modee=" "+emblobby
                    else:
                        modefield_value=" -"
                    embed.add_field(name=phr["gamemode"],value=gamee+modee,inline=False) 
                #команды(если есть) или default названия сторон
                
                if matchinfo.get(var['radiant_team'],None)!=None: #лого сил света
                    rad=matchinfo[var['radiant_team']].get('name',phr["radiant_team"])
                    if not stratz:
                      try:
                        response = requests.get(matchinfo[var['radiant_team']][var["logo_url"]], stream=True)
                        with open(f'teamradiant{matchid}.png', 'wb') as out_file:
                            shutil.copyfileobj(response.raw, out_file)
                        with open(f'teamradiant{matchid}.png','rb') as r:
                            radiant=r.read()
                        radmoji = await emojiguild.create_custom_emoji(name=f'radiant{matchid}',image=radiant)
                        del response
                        remove(f'teamradiant{matchid}.png')
                        radiant_embed_name=f'{radmoji}{rad}'+radwin
                      except:
                        radiant_embed_name=f'<:radiant:591631740435431465>{rad}'+radwin
                    else:
                        radiant_embed_name=f'<:radiant:591631740435431465>{rad}'+radwin
                else:
                    radiant_embed_name=f'<:radiant:591631740435431465>{responses[f"{lang}"]["radiant_team"]}'+radwin

                
                if matchinfo.get(var['dire_team'],None)!=None:  #лого сил тьмы
                    ddire=matchinfo[var['dire_team']].get('name',phr["dire_team"])
                    if not stratz:
                      try:
                        response = requests.get(matchinfo[var['dire_team']][var["logo_url"]], stream=True)
                        with open(f'teamdire{matchid}.png', 'wb') as out_file:
                            shutil.copyfileobj(response.raw, out_file)
                        with open(f'teamdire{matchid}.png','rb') as d:
                            dire=d.read()
                        diremoji = await emojiguild.create_custom_emoji(name=f'dire{matchid}',image=dire)
                        del response
                        remove(f'teamdire{matchid}.png')
                        dire_embed_name=f'{diremoji}{ddire}'+direwin
                      except:
                        dire_embed_name=f'<:dire:561564058063732757>{ddire}'+direwin
                    else:
                        dire_embed_name=f'<:dire:561564058063732757>{ddire}'+direwin
                else:
                    dire_embed_name=f'<:dire:561564058063732757>{responses[f"{lang}"]["dire_team"]}'+direwin

                             
                #создание списка реакций с id героя и добавление полей с малой статистикой игроков
                heroemojis={}
                             
                with open('dotabase/heroes.txt', 'r', encoding='utf-8-sig') as f:
                    heroes=f.readlines()
                radscore,direscore=0,0
                if stratz:
                    radscore=sum(matchinfo['stats']['radiantKills'])
                    direscore=sum(matchinfo['stats']['direKills'])
                else:
                    radscore=matchinfo['radiant_score']
                    direscore=matchinfo['dire_score']
                radiant_hero_fields='__'+phr['rad_score']+": "+str(radscore)+'__\n'
                dire_hero_fields='__'+phr['dire_score']+": "+str(direscore)+'__\n'
                accounts_avail={}
                herocodes={}
                for i in range(10):
                    if i==5:
                        embed.add_field(name=radiant_embed_name,value=radiant_hero_fields,inline=True)
                    player=matchinfo["players"][i]
                    heroid=player.get(var["hero_id"])

                    if stratz:  #имя
                        try:
                            player_name=None
                            try:
                                account=player['steamAccount']['proSteamAccount']
                                player_name=account['name']
                            except:
                                account=player['steamAccount']
                                player_name=account['name']
                            finally:
                                 if player_name!=None:
                                     accounts_avail[heroid]=player['steamAccount']
                                 else:
                                     del player_name
                             
                        except:
                             pass

                    else:
                      if player["account_id"] != None:  
                        try:                    
                            async with aiohttp.ClientSession() as session:
                                async with session.get(f"https://api.opendota.com/api/players/{player['account_id']}") as r:
                                    account = json.loads(await r.text())
                                    accounts_avail[heroid]=account
                                    if account["profile"].get("name",None)!=None:
                                        player_name=account["profile"].get("name")
                                    else:
                                        player_name=account["profile"].get("personaname")
                        except:                           
                            pass
                                
                    for hero in heroes:
                        herores=dict(eval(hero))
                        if heroid==herores['id']:
                            herocodes[herores['shortname']]=f'<{herores["emoji"]}>'
                            heroinfo={}
                            heroinfo["id"]=herores["id"]
                            try:
                                heroinfo['name']=player_name
                                del player_name
                            except:
                                heroinfo["name"]=herores["name"]
                            if stratz:
                                nw=player['stats']['networth'][-1]
                            else:
                                nw=player["total_gold"]
                            heroinfo["img"]=herores['icon']
                            heroemojis[herores["emoji"]]=heroinfo
                            hero_field_name=f'<{herores["emoji"]}>**{heroinfo["name"]}** \n'
                            hero_field_stats='  {0}  \n  {1}  \n  {2} \n'.format(phr["kda_short"]+": "+f'{player[var["kills"]]}/{player[var["deaths"]]}/{player[var["assists"]]}',
                                                                          phr["lh_den_short"]+": "+f'{player[var["last_hits"]]}/{player[var["denies"]]}',
                                                                          phr["totalgold"]+": "+f'{nw}')
                            if i<5:
                                radiant_hero_fields+=hero_field_name
                                radiant_hero_fields+=hero_field_stats
                            else:
                                dire_hero_fields+=hero_field_name
                                dire_hero_fields+=hero_field_stats
                embed.add_field(name=dire_embed_name,value=dire_hero_fields,inline=True)
                #драфт и запреты
                draft=matchinfo.get(var["picks_bans"],None)
                if draft!=None:
                    radiant_draft='<:radiant:591631740435431465>'
                    dire_draft='<:dire:561564058063732757>'
                    for el in draft:   
                        for heroinf in heroes:  
                            hero=dict(eval(heroinf))
                            if el[var['hero_id']]==hero['id']:
                                if stratz:
                                    gud=False
                                    if not el['isPick'] and el['wasBannedSuccesfully']:
                                        heromoji='<'+hero['banmoji']+'>'
                                        gud=True
                                    elif el['isPick']:
                                        heromoji='<'+hero['emoji']+'>'
                                        gud=True
                                    if el['isRadiant'] and gud:
                                        radiant_draft+=f'{heromoji}'
                                        dire_draft+=u"\u2800"
                                    else:
                                        radiant_draft+=u"\u2800"
                                        dire_draft+=f'{heromoji}'                                        
                                else: #opendota
                                    if el['is_pick']==False:
                                        heromoji='<'+hero['banmoji']+'>'
                                    else:
                                        heromoji='<'+hero['emoji']+'>'                                    
                                    if el['team']==0:
                                        radiant_draft+=f'{heromoji}'
                                        dire_draft+=u"\u2800"
                                    else:
                                        radiant_draft+=u"\u2800"
                                        dire_draft+=f'{heromoji}'
                        
                    embed.add_field(name=phr['draft'],value='{0}\n{1}'.format(radiant_draft,dire_draft),inline=False)
                #график
                if stratz:
                    makeadvgraph(matchinfo['durationSeconds'],matchinfo['stats']['radiantNetworthLead'],matchinfo['stats']['radiantExperienceLead'],matchid)
                else:
                    makeadvgraph(matchinfo['duration'],matchinfo["radiant_gold_adv"],matchinfo['radiant_xp_adv'],matchid)
                graph=discord.File(fp=f"adv_graph{matchid}.png")
                embed.set_image(url=f"attachment://adv_graph{matchid}.png")
                embed.add_field(name=phr['adv_graph'], value='<:expline:588052749141147778> {0} \n<:goldline:588052749611171860> {1}'.format(phr["exp"],phr["nw"]),inline=False)
                
                msg = await message.channel.send(embed=embed,file=graph)

                
                
                #Удаление емоджи и картинок
                try:
                    await diremoji.delete()
                except:
                    pass
                try:
                    await radmoji.delete()
                except:
                    pass

                try:
                    remove(f"adv_graph{matchid}.png") 
                except:
                    pass                                                                                                                         

                for el in heroemojis:
                    await msg.add_reaction(el)
                if not stratz:
                    await msg.add_reaction(":mapemoji:561636043204329556")
                await msg.add_reaction("❌")

                await message.clear_reactions()                
                await message.add_reaction("✅")
                
                if len(command)>=3:
                    if command[2].upper()=='X' or command[2].upper()=="Х":
                        def check(reaction,user):
                            return user.id!=537272694018932754 and reaction.message.id==msg.id and user.id==user_msg.author.id
                    else:
                         def check(reaction,user):
                            return user.id!=537272694018932754 and reaction.message.id==msg.id
                else:
                    def check(reaction,user):
                        return user.id!=537272694018932754 and reaction.message.id==msg.id
        
                react = await client.wait_for("reaction_add",check=check)
                while str(react[0])!="❌":
                    
                    if str(react[0])=="<:mapemoji:561636043204329556>" and not stratz:
                        makemap(matchinfo)
                        img="map{}.png".format(matchid)  
                        fmap=discord.File(fp="map{}.png".format(matchid))
                        embedmap = discord.Embed(title=f'{phr["match"]} {matchid} | {phr["map"]}',colour=color,url="https://discordapp.com")
                        embedmap.set_footer(text=f"{client.user.name} | {pref}matchinfo", icon_url=client.user.avatar_url_as(format='png'))

                        embedmap.set_image(url="attachment://map{}.png".format(matchid))
                        mapmsg = await message.channel.send(embed=embedmap,file=fmap)
                        
                        remove(img)
   ######                                                                             
                    else:         #игрок
                        emji=str(react[0])
                        emji=emji[1:len(emji)-1]      
                        if heroemojis.get(emji,None)!=None:
                            try:
                                await playermsg.delete()
                            except:
                                pass
                            playercolors={0:0x0D00FF,1:0x50E3C2,2:0x9013FE,3:0xF8E71C,4:0xFFA000,128:0xFF5EF5,129:0x9ABD6A,130:0x00FFF6,131:0x579E04,132:0x80532B}
                            players = matchinfo["players"]

                            for i in range(10):
                                playerT=players[i]
                                t=heroemojis.get(emji)
                                if playerT[var['hero_id']]==t['id']:
                                   player=playerT
                                   #pp(player['gold_reasons'])
                                   break
                                
                            embedhero = discord.Embed(title=f'{matchid} | {phr["player_stats"]}',colour=discord.Colour(playercolors.get(player[var["player_slot"]])),url="https://discordapp.com")


                            if accounts_avail.get(player[var['hero_id']],None)!=None:  #ранг и имя
                                account = accounts_avail[player[var['hero_id']]]
                                if account.get(var["rank_tier"],None)!=None:
                                    rank=str(account[var["rank_tier"]])
                                else:
                                    rank="00"
                                makerang(rank)
                                frank=discord.File(fp=f"{rank}.png")
                                if stratz:
                                    try:
                                        if account["proSteamAccount"].get("name",None)!=None:
                                            embedhero_name=account["proSteamAccount"]["name"]
                                    except:
                                        if account.get("name",None)!=None:
                                            embedhero_name=account["name"]
                                        else:
                                            embedhero_name=heroemojis[emji]["name"]
                                else:
                                    if account["profile"].get("name",None)!=None:
                                        embedhero_name=account["profile"]["name"]
                                    elif account["profile"].get("personaname",None)!=None:
                                        embedhero_name=account["profile"]["personaname"]
                                    else:
                                        embedhero_name=heroemojis[emji]["name"]

                            else:
                                rank='00'
                                embedhero_name=heroemojis[emji]["name"]
                                makerang(rank)
                                frank=discord.File(fp=f"{rank}.png")

                            if stratz:
                                nw=player['stats']['networth'][-1]
                                xp=player['stats']['experienceCount']
                                obs=0
                                sen=0
                                for ward in player['stats']['wards']:
                                    if ward['type']==0:
                                        obs+=1
                                    else:
                                        sen+=1
                            else:
                                nw=player["total_gold"]
                                xp=player['total_xp']
                                obs=player['obs_placed']
                                sen=player['sen_placed']
                                killed=player['killed']
                                killed_by=player['killed_by']
                                killeds,killed_bys='',''
                                count=0
                                for entity in killed.keys():
                                    if entity.replace('npc_dota_hero_','') in herocodes.keys():
                                        killeds+=f"{herocodes[entity.replace('npc_dota_hero_','')]}: {killed[entity]} "
                                        count+=1
                                        if count==5:
                                            killeds+='\n'
                                            count=0
                                for entity in killed_by.keys():
                                    if entity.replace('npc_dota_hero_','') in herocodes.keys():
                                        killed_bys+=f"{herocodes[entity.replace('npc_dota_hero_','')]}: {killed_by[entity]} "
                                        count+=1
                                        if count==5:
                                            killeds+='\n'
                                            count=0
                                
                                
                            embedhero.set_footer(text=f"{client.user.name} | {pref}matchinfo", icon_url=client.user.avatar_url_as(format='png'))
                            embedhero.add_field(name=f'<{emji}> **{embedhero_name}**',
                                                value="{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(phr["kda"],
                                                                                            phr["lh_den"],
                                                                                            phr["gpm_expm"],
                                                                                            phr["totalgold_exp"],
                                                                                            phr["obs_sen"],
                                                                                            phr["towerdmg_herodmg"]),inline=True)
                            embedhero.add_field(name=phr["stats"],
                                                value="{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(f'{player[var["kills"]]}/{player[var["deaths"]]}/{player[var["assists"]]}',
                                                                                            f'{player[var["last_hits"]]}/{player[var["denies"]]}',
                                                                                            f"{player[var['gold_per_min']]}/{player[var['xp_per_min']]}",
                                                                                            f"{nw}/{xp}",
                                                                                            f"{obs}<:obs:591295557197103154>/{sen}<:sen:591295558077906944>",
                                                                                            f"{player[var['hero_damage']]}/{player[var['tower_damage']]}"),inline=True)

            ###############additional info

                            #журнал рун подобранных игроком
                            runemojis=["<:rune_0:591295557000101910>","<:rune_1:591295556970610695>","<:rune_2:591295557595693067>","<:rune_3:591295557738430464>","<:rune_4:591295557641699358>","<:rune_5:591295557851676673>","<:rune_6:591295557935300618>"]

                            if stratz:
                                runeslog=player['stats'].get("runes",[])
                            else:
                                runeslog=player.get("runes_log",[])
                                                             
                            if runeslog!=[]:
                                herorunes=''
                                for el in runeslog:
                                    if el['time']%60<10:
                                        sec="0"+str(el['time']%60)
                                    else:
                                        sec=str(el['time']%60)
                                    time=str(el['time']//60)+":"+sec
                                    herorunes+=runemojis[el[var['runetype']]]+" "+time+"\n"
                                embedhero.add_field(name=phr["runes"],value=herorunes,inline=True)
                            if not stratz:
                                #список постоянных усилений героя
                                playerbuffs=player.get("permanent_buffs",None)
                                if playerbuffs!=None:
                                    permbuffs=["0","<:1_:591306566725140493>","<:2_:591306566603636747>","<:3_:591306567043776515>","<:4_:591306568193277962>","<:5_:591306568398798848>","<:6_:591306568696463399>","<:7_:591306569027944458>","<:8_:591306569069756431>","<:9_:591306569770205311>","<:10:591306570311270413>"]
                                    herobuffs=''
                                    for el in playerbuffs:
                                        if el['permanent_buff']==1 or el['permanent_buff']==2:
                                            herobuffs+=permbuffs[el['permanent_buff']]+"\n"
                                        else:
                                            herobuffs+=permbuffs[el['permanent_buff']]+str(el['stack_count'])+"\n"
                                    embedhero.add_field(name=phr["permbuffs"],value=herobuffs,inline=True)
                                farm=player.get('gold_reasons',{})
                                if farm!={}:
                                    sources={'0':{'ru':'Прочее','en':'Other'},'1':{'ru':'Смерть','en':'Death'},'11':{'ru':'Постройки','en':'Buildings'},'12':{'ru':'Герои','en':'Heroes'},'13':{'ru':'Крипы','en':'Creeps'},'14':{'ru':'Рошан','en':'Roshan'},'6':{'ru':'Прочее','en':'Other'}}
                                    #for key in farm.keys():
                            if killeds!='':
                                embedhero.add_field(name=phr["killed"],value=killeds,inline=True)
                            if killed_bys!='':
                                embedhero.add_field(name=phr["killed_by"],value=killed_bys,inline=True)
                                        


                            makeplayerslots(player,stratz)#инвентарь
                            inv="inventory{0}_{1}.png".format(matchid,player[var["player_slot"]])
                            finv=discord.File(fp=f"{inv}")
                            embedhero.set_image(url=f"attachment://{inv}")
                            embedhero.set_thumbnail(url=f"attachment://{rank}.png")
                            playermsg = await message.channel.send(embed=embedhero,files=[finv,frank])
                            remove(f'{rank}.png')
                            remove(inv)
                    react = await client.wait_for("reaction_add",check=check)

                await msg.clear_reactions()



#префикс сервера
    if client.user.mentioned_in(message):
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'
        responses={"en":{"pref":"The prefix for commands on this server is "},
                   "ru":{"pref":"Префикс команд на этом сервере: "}}
        
        await message.channel.send(responses[f"{lang}"]['pref']+pref)

    if message.content.startswith('steamid',1):
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'
        responses={"en":{"bad_steamid":"User with this ID was not found",
                         "error":"An error occured"},
                         
                   "ru":{"bad_steamid":"Пользователь с таким ID не найден",
                         "error":"Возникла ошибка"}}


        phr=responses[f"{lang}"]
        playerid = message.content.split()[1]
        if pref[0]==message.content[0]:
            with open('dotabase/userprofiles.txt','r') as f:
                lines=f.readlines()
            user=None
            for line in lines:
                CurUser=dict(eval(line))
                if CurUser['discord_id']==message.author.id:
                    try:               
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"https://api.stratz.com/api/v1/Player/{playerid}") as r:
                                user=json.loads(await r.text())
                    except:
                        await message.channel.send(phr['error'])
                    if r.status==404:
                        await message.channel.send(phr['bad_steamid'])
                    elif r.status==200:
                        user=CurUser
                        f=open('dotabase/userprofiles.txt','w')
                        for line in lines:
                            t=dict(eval(line))
                            if t['discord_id']!=user['discord_id']:
                                f.write(line)
                            if t['discord_id']==user['discord_id']:
                                t['steam_id']=playerid
                                f.write("{0}\n".format(t))
                        f.close()
                        await message.add_reaction("✅")
                        break
                    else:
                        await message.channel.send(f'{phr["error"]}:{r.status_code}')
            if user==None:               #проверка существует ли такой юзер
                try:               
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"https://api.stratz.com/api/v1/Player/{playerid}") as r:
                            user=json.loads(await r.text())
                except:
                    await message.channel.send(phr['error'])
                if r.status==404:
                    await message.channel.send(phr['bad_steamid'])
                elif r.status==200:
                    base_profile={'discord_id':message.author.id,'steam_id':playerid}
                    with open('dotabase/userprofiles.txt', 'a') as f:
                        f.write("\n{0}".format(base_profile))
                    await message.add_reaction("✅")
                else:
                    await message.channel.send(f'{phr["error"]}:{r.status_code}')



    if message.content.startswith('flip',1):
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'

        command=message.content.split()
        responses={"en":{"flip":"That's a coinflip ༼ つ ◕_◕ ༽つ \nBut a better one ༼ つ ◕‿◕ ༽つ",
                         "bet":"You chose:",
                         "won":"You won",
                         'result':"Result",
                         "lost":"You lost"},
                         
                   "ru":{"flip":"Подбрасывание монетки ༼ つ ◕_◕ ༽つ \nТолько лучше ༼ つ ◕‿◕ ༽つ",
                         "flip_info":"Выберите вашу ставку нажав соответствущую реакцию\nВыберите сторону монеты<a:coinflip:594438507938709524>\nОжидайте результат",
                         "bet":"Вы выбрали:",
                         "chooseside":"Выберите сторону",
                         'result':"Результат",
                         "won":"Вы выиграли",
                         "lost":"Вы проиграли"}}

        phr=responses[lang]
        if pref==message.content[0]:
            player=get_user(message.author.id)
            #<:sange:594203284139540483>
            #<:yasha:594203285712273429>
            mainembed = discord.Embed(colour=discord.Colour(0xb42ece),url="https://discordapp.com")
            mainembed.set_footer(text=f"{client.user.name} | {pref}flip", icon_url=client.user.avatar_url_as(format='png'))
            mainembed.add_field(name="<:sange:594203284139540483>Sange and Yasha<:yasha:594203285712273429>\n",value=phr['flip'],inline=False)

            gamemsg = await message.channel.send(embed=mainembed)

            await gamemsg.add_reaction(":sange:594203284139540483")
            await gamemsg.add_reaction(":yasha:594203285712273429")
            
            def check(reaction,user):
                return user.id==message.author.id and reaction.message.id==gamemsg.id
        
            react = await client.wait_for("reaction_add",check=check)
     
            if str(react[0])=="<:sange:594203284139540483>" or str(react[0])=="<:yasha:594203285712273429>":
                    await gamemsg.clear_reactions()
                    choice=str(react[0])
                    choice=choice[2:7]
                    if choice=='yasha':
                        bet='<:yasha:594203285712273429>**Yasha**'
                    else:
                        bet="<:sange:594203284139540483>**Sange**"
                    res=flip()
                    f=discord.File(fp=res)
                    flipembed = discord.Embed(colour=discord.Colour(0xb42ece),url="https://discordapp.com")
                    flipembed.add_field(name="<:sange:594203284139540483>**Sange and Yasha**<:yasha:594203285712273429>",value=phr['bet']+bet,inline=False)
                    await gamemsg.edit(embed=flipembed)
                    coinflipmsg= await message.channel.send(file=f)
                    await asyncio.sleep(9)
                    await coinflipmsg.delete()
                    if res[19:24]=='yasha':
                        res='<:yasha:594203285712273429>**Yasha** \n'
                        if choice=='yasha':
                            res+=phr['won']
                        else:
                            res+=phr['lost']
                    else:
                        res="<:sange:594203284139540483>**Sange** \n"
                        if choice=='sange':
                            res+=phr['won']
                        else:
                            res+=phr['lost']
                    flipembed.remove_field(0)                                    
                    flipembed.add_field(name="<:sange:594203284139540483>**Sange and Yasha**<:yasha:594203285712273429>",value=phr['bet']+bet+'\n'+phr['result']+': '+res,inline=False)
                    await gamemsg.edit(embed=flipembed)
                    await gamemsg.clear_reactions()
                

                                                

#########################################################################################################################################################################                                    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(time.ctime(time.time()))
    print('------')

    '''
    channel = client.get_channel(593474878519377970)
    while True:
            r=requests.get("https://api.stratz.com/api/v1/Player/143597200")
            if r.status_code==200:
                note=channel.mention
                await channel.send(str(r.status_code)+note)
                await asyncio.sleep(300)
            else:
                await channel.send(r.status_code)
            await asyncio.sleep(60)
    '''
    async def pres():
        while not client.is_closed():
            await client.change_presence(activity=discord.Game(name="<prefix>help", type=2))
            await asyncio.sleep(20)
            await client.change_presence(activity=discord.Game(name="@ for server prefix", type=2))
            await asyncio.sleep(20)
    task = asyncio.create_task(pres())
    

client.run(TOKEN,reconnect=True)
