import asyncio
import discord
from picmaker import *
import requests
import json

def is_parsed(match):
	return match.get("version", None) is not None
    
def getmatch(match_id):
    '''
    codes:
    0 - match not found (status_code=404,  {"error":"Not Found"}) -> requestparse(matchid) st
    1 - match parsed succesfully (status_code=200)
    2 - match partially analyzed (status_code=200, 'radiant_gold_adv':None/null) |-> requestparse(matchid) 
                                                                                 |-> no heroes on map, no graph
    '''
    try:                    #запрос инфы о матче
        r = requests.get("https://api.opendota.com/api/matches/{}".format(matchid))
        matchinfo=json.loads(r.text)
    except Exception as e:                           
        print("an error occured:{}".format(e))


    #цвет рамки
    if matchinfo['radiant_win']==True:
        color=discord.Colour(0xad36)
    else:
        color=discord.Colour(0xd0021b)
    #команды(если есть)
    if matchinfo.get('radiantTeam')!=None:
        rad=matchinfo['radiantTeam'].get('name','Команда сил света')


   #lanestory 'lane_efficiency'
                try:                    #запрос инфы о матче
                    r = requests.get("https://api.opendota.com/api/matches/{}".format(matchid))
                    matchinfo=json.loads(r.text)
                except Exception as e:                           
                    print("an error occured:{}".format(e))

                makeadvgraph(matchid)


                #цвет рамки
                if matchinfo['radiant_win']==True:
                    color=discord.Colour(0xad36)
                else:
                    color=discord.Colour(0xd0021b)
                #команды(если есть)
                if matchinfo.get('radiantTeam')!=None:
                    rad=matchinfo['radiantTeam'].get('name','Команда сил света')

                    
                embed = discord.Embed(title=f'{matchid} | {responses[f"{lang}"]["summary"]}',colour=color,url="https://discordapp.com")
                embed.set_footer(text="yasha | !matchinfo", icon_url="https://cdn.discordapp.com/avatars/537272694018932754/4835f928e3fffa4ef29a35d2c586f9c0.png")
                embed.add_field(name=f'<:dire:561564058063732757>{responses[f"{lang}"]["dire_score"]}', value=matchinfo['dire_score'],inline=True)
                embed.add_field(name=f'<:radiant:561564058042630161>{responses[f"{lang}"]["rad_score"]}', value=matchinfo['radiant_score'],inline=True)
                graph=discord.File(fp=f"adv_graph{matchid}.png")
                embed.set_image(url=f"attachment://adv_graph{matchid}.png")
                embed.add_field(name=f'<:expline:588052749141147778> {responses[f"{lang}"]["exp"]}', value=f'<:goldline:588052749611171860> {responses[f"{lang}"]["nw"]}',inline=True)
                msg = await message.channel.send(embed=embed,file=graph)
                remove(f"adv_graph{matchid}.png")

                #coздание реакций
                for i in range(10):
                    f=open('dotabase/heroes.txt', 'r')
                    heroid=matchinfo["players"][i].get("hero_id")
                    for line in f:
                        herores=dict(eval(line))
                        if heroid==herores['id']:
                           await msg.add_reaction(herores["emoji"])
                await msg.add_reaction(":mapemoji:561636043204329556")
                await msg.add_reaction("❌")


                await message.clear_reactions()
                await message.add_reaction("✅")

                
                def check(reaction,user):
                    return user.id!=537272694018932754 and reaction.message.id==msg.id
        
                react = await client.wait_for("reaction_add",check=check)
                
                while str(react[0])!="❌":
                    
                    if str(react[0])=="<:mapemoji:561636043204329556>":
                        makemap(matchid)
                        img="map{}.png".format(matchid)  
                        fmap=discord.File(fp="map{}.png".format(matchid))
                        embedmap=embed
                        embedmap.set_image(url="attachment://map{}.png".format(matchid))
                        mapmsg = await message.channel.send(embed=embedmap,file=fmap)
                        
                        remove(img)
   ######                                                                             
                    else:         #игрок
                    
                        r=str(react[0])             

                        f=open('dotabase/heroes.txt', 'r')
                        is_hero_emoji=False
                        for line in f:
                            herores=dict(eval(line))
                            if r[1:len(r)-1]==herores['emoji']:
                                heroid=herores['id']
                                heroembed=herores
                                is_hero_emoji=True
                                break
                        if is_hero_emoji==True:
                            try:
                                await playermsg.delete()
                            except:
                                pass
                            playercolors={0:0x0D00FF,1:0x50E3C2,2:0x9013FE,3:0xF8E71C,4:0xFFA000,128:0xFF5EF5,129:0x9ABD6A,130:0x00FFF6,131:0x579E04,132:0x80532B}
                            players = matchinfo["players"]

                            for i in range(10):
                                playerT=players[i]
                                if playerT['hero_id']==heroid:
                                   player=playerT
                                   break
                            makeplayerslots(player)
                            inv="inventory{0}_{1}.png".format(player["match_id"],player["player_slot"])
                            embedhero = discord.Embed(title=f'{matchid} | {responses[f"{lang}"]["player_stats"]}',colour=discord.Colour(playercolors.get(player["player_slot"])),url="https://discordapp.com")
                            embedhero.set_thumbnail(url=f"http://cdn.dota2.com/apps/dota2/images/heroes/{heroembed['url_small']}")
                            embedhero.set_footer(text="yasha | !matchinfo", icon_url="https://cdn.discordapp.com/avatars/537272694018932754/4835f928e3fffa4ef29a35d2c586f9c0.png")
                            embedhero.add_field(name=f'{responses[f"{lang}"]["hero"]}', value=f'<{heroembed["emoji"]}> {heroembed["localname"]}',inline=False)
                            embedhero.add_field(name=f'{responses[f"{lang}"]["kda"]}', value=f'{player["kills"]}/{player["deaths"]}/{player["assists"]}',inline=True)
                            embedhero.add_field(name=f'{responses[f"{lang}"]["lh_den"]}', value=f"{player['last_hits']}/{player['denies']}",inline=True)
                            embedhero.add_field(name=f'{responses[f"{lang}"]["gpm_expm"]}', value=f"{player['gold_per_min']}/{player['xp_per_min']}",inline=True)
                            embedhero.add_field(name=f'{responses[f"{lang}"]["totalgold_exp"]}', value=f"{player['total_gold']}/{player['total_xp']}",inline=True)
                            embedhero.add_field(name=f'{responses[f"{lang}"]["obs_sen"]}', value=f"{player['obs_placed']}/{player['sen_placed']}",inline=True)
                            embedhero.add_field(name=f'{responses[f"{lang}"]["towerdmg_herodmg"]}', value=f"{player['tower_damage']}/{player['hero_damage']}",inline=True)
                            f=discord.File(fp=f"{inv}")
                            embedhero.set_image(url=f"attachment://{inv}")
                            playermsg = await message.channel.send(embed=embedhero,file=f)
                            remove(inv)
                    react = await client.wait_for("reaction_add",check=check)
                await msg.clear_reactions()
