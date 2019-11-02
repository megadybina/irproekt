import requests
import json
import time
from time import time as currenttime
import asyncio
import discord
import aiohttp

client = discord.Client()

####discord tools
def get_user(user_discord_id):
    with open('dotabase/userprofiles.txt','r') as f:
        for line in f:
            t=dict(eval(line))
            if user_discord_id==t["discord_id"]:
                user=t
                break
            else:
                user=None
        return user
    
                
def getpref(serverid):
    with open("dotabase\serversettings.txt","r") as f:
        for line in f:
            t=dict(eval(line))
            if serverid==t["server_id"]:
                pref=t["prefix"]
                break
            else:
                pref="!"
        
        return pref

def getlang(serverid):
    with open("dotabase\serversettings.txt","r") as f:
        for line in f:
            t=dict(eval(line))
            if serverid==t["server_id"]:
                lang=t["lang"]
                break
            else:
                lang="en"
        return lang

########dota tools
def highlight(string):  #highlights hero names with bold text, item names with codeblocks and abilities with underscore 
    with open('dotabase/heroes.txt', 'r', encoding='utf-8-sig') as t:
        heroes=t.readlines()
    with open('dotabase/items.txt', 'r') as t:
        items=t.readlines()
    with open('dotabase/abilities.txt', 'r') as t:
        abils=t.readlines()
        
    for herof in heroes:
        hero=dict(eval(herof))
        if hero['name'] in string:
            ind=string.index(hero['name'])
            indr=ind+len(hero['name'])
            if string[ind-1]!='>':
                string=string[:ind]+'<'+hero['emoji']+'>'+'**'+string[ind:indr]+'**'+string[indr:]
            else:
                string=string[:ind]+'**'+string[ind:indr]+'**'+string[indr:]
    for itemf in items:
        item=dict(eval(itemf))
        if item['name'] in string:
            ind=string.index(item['name'])
            indr=ind+len(item['name'])
            string=string[:ind]+'`'+string[ind:indr]+'`'+string[indr:]
    for abf in abils:
        ab=dict(eval(abf))
        if ab['name'] in string:
            ind=string.index(ab['name'])
            indr=ind+len(ab['name'])
            string=string[:ind]+'__'+string[ind:indr]+'__'+string[indr:]
    return string


async def is_parsed(matchid):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.opendota.com/api/matches/{}".format(matchid)) as r:
                match=json.loads(await r.text())
        return match.get("version", None) is not None
    except:
        return False
    
def get_player_in_match(steamid,match):
    for player in match['players']:
        if player['account_id']==int(steamid):
            break
    return player


async def get_match_od(matchid):
    try:               
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.opendota.com/api/matches/{}".format(matchid)) as r:
                matchinfo=json.loads(await r.text())
    except:
        matchinfo=0
    return matchinfo


async def get_match_stratz(matchid):
    try:               
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.stratz.com/api/v1/match/{}/breakdown".format(matchid)) as r:
                matchinfo=json.loads(await r.text())
    except:
        matchinfo=0
    return matchinfo

            
async def get_lm_od(steamid):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.opendota.com/api/players/{steamid}/matches?limit=1&significant=0") as r:
                lastmatch_ins = json.loads(await r.text())
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.opendota.com/api/players/{steamid}/matches?limit=1&significant=1") as r:
                lastmatch_s = json.loads(await r.text())
        if lastmatch_s[0]['start_time']>lastmatch_ins[0]['start_time']:
            matchid=lastmatch_s[0]['match_id']
        else:
            matchid=lastmatch_ins[0]['match_id']
                    
    except:
        matchid='error'
    return matchid

def hero_by_id(heroid):
    with open('dotabase\heroes.txt', 'r', encoding='utf-8-sig') as f:
        lines=f.readlines()
    for line in lines:
        hero=dict(eval(line))
        if heroid == hero['id']:
            return hero

def hero_by_alias(heroname):
    with open('dotabase/heroes.txt', 'r', encoding='utf-8-sig') as f:
        lines=f.readlines()
    for line in lines:
        hero=dict(eval(line))
        for alias in hero['aliases']:
            if heroname.upper()==alias.upper():
                return hero
def get_duration(duration):
    mins=duration//60
    if duration%60<10:  
        sec="0"+str(duration%60)
    else:
        sec=duration%60
    time="{0}:{1}".format(mins,sec)
    return time
###challenges
async def waitchallenge(time,msg_chan,reset):
                try:
                    if reset==0:
                        savechallenge(challenge['raw'],message.author.id,int(currenttime()))
                    await asyncio.sleep(time)
                    if type(msg_chan)==discord.message.Message:
                        await msg_chan.clear_reactions()
                    
                except asyncio.CancelledError:
                    if type(msg_chan)==discord.message.Message:
                        await msg_chan.channel.send("checking...")
                    else:
                        msg_chan.send("checking...")
                    raise
                finally:
                    if type(msg_chan)==discord.message.Message:
                        await checkchallenge(challenge['raw'],msg_chan.channel)
                    else:
                        await checkchallenge(challenge['raw'],msg_chan)

def savechallenge(chal,userid,starttime):
                with open('dotabase/ongoing_challenges.txt','a') as f:
                    chal['discord_user']=userid
                    chal['steam_id']=steamid
                    chal['chnl_id']=message.channel.id
                    chal['start_time']=starttime
                    f.write(str(chal)+'\n')

async def checkchallenge(chal,channel):
                    steamid=chal['steam_id']
                    matchid=get_lm(steamid)
                    if matchid==None:
                        await channel.send(f'{phr["error"]}: {r.status_code}. {phr["later"]}')
                        return
                    else:
                        try:                
                            r = requests.get("https://api.opendota.com/api/matches/{}".format(matchid))
                            matchinfo=json.loads(r.text)
                        except Exception as e:                           
                            await channel.send(f'{phr["error"]}: {r.status_code}. {phr["willcheck"]}')
                            while True:
                                r = requests.get("https://api.opendota.com/api/matches/{}".format(matchid))
                                if r.status_code==200:
                                    matchinfo=json.loads(r.text)
                                else:
                                    await asyncio.sleep(180)
                        if chal['type']=='player':
                            user_player=get_player_in_match(chal['steam_id'],matchinfo)
                            valuecheck=user_player.get(chal['value']['od'])
                            await channel.send(valuecheck)
                
async def check_on_restart():
                with open('dotabase/ongoing_challenges.txt','r') as f:
                    ongoings=f.readlines()
                for ongoing in ongoings:
                    chal=dict(eval(ongoing))
                    chalchan=client.get_channel(chal['chnl_id'])
                    if chal['start_time']+chal['comp_time']>=int(currenttime()):
                        checkchallenge(chal,chalchan)
                        ongoings.remove(ongoing)
                        with open('dotabase/ongoing_challenges.txt','w') as f:
                            for el in ongoings:
                                f.write(el)
                    elif chal['start_time']+chal['comp_time']<int(currenttime()):
                        reset=1
                        task = asyncio.create_task(waitchallenge(int(currenttime())-(chal['start_time']+chal['comp_time']),chalchan,reset))
                        def check(reaction,user):
                            return user.id==chal['discord_user']
                        react = await client.wait_for("reaction_add",check=check)
                        if str(react[0])=="<a:Emoticon_obs:593495627342676040>":
                            task.cancel()
            
