import asyncio
import discord
import random
from picmaker import *
from os import remove
import requests
import json
from tools import *
import shutil
from dotabase import *
from pprint import pprint as pp
import glob

async def hero(message,client):
    if message.content.startswith('hero',1):
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'
        responses={"en":{"bad_hero":"Hero not found",
                         "error":"An error occured",
                         "later":"Try again in a bit",
                         "heroinfo":"Hero information",
                         "hype":"Short decription",
                         "stats":"Hero attributes",
                         "talents":"Hero talents",
                         "abils":"Hero abilities",
                         "hero":"Hero"},
                         
                   "ru":{"bad_hero":"Герой не найден",
                         "error":"Возникла ошибка",
                         "later":"Попробуйте через пару минут",
                         "heroinfo":"Информация о герое",
                         "hype":"Краткое описание",
                         "stats":"Показатели героя",
                         "talents":"Таланты героя",
                         "abils":"Способности героя",
                         "hero":"Герой"}}

        #https://api.stratz.com/api/v1/Hero/{id}/purchasePattern
        phr=responses[f"{lang}"]
        command=message.content.split()
        heroname = message.content[5:].strip()
        if pref==message.content[0]:
            with open('dotabase/heroes.txt', 'r', encoding='utf-8-sig') as f:
                heroes=f.readlines()
                found=False
            for hero in heroes:
                herores=dict(eval(hero))
                if heroname==herores['name'].lower() or heroname in herores.get('aliases',[]) or heroname==herores['shortname']:
                    found=True
                    break


            if found==True:
                await message.add_reaction("⏳")
                
                colors={'agility':discord.Colour(0x29c53f),'intelligence':discord.Colour(0x1e7fac),'strength':discord.Colour(0xb91c1f)}
            
                embed = discord.Embed(title=f'{phr["heroinfo"]}',colour=colors.get(herores['attr_primary']),url="https://discordapp.com")
                embed.set_footer(text=f"{client.user.name} | {pref}hero", icon_url=client.user.avatar_url_as(format='png'))
                als=herores.get('aliases')
                if als:
                    aliases=' | '
                    aliases=aliases.join(als)
                else:
                    aliases=u"\u2800"
                embed.set_thumbnail(url=f'http://cdn.dota2.com/apps/dota2/images/heroes/{herores["icon"]}')
                embed.add_field(name="<"+herores["emoji"]+">**"+herores["name"]+'**',value=aliases,inline=False)
                embed.add_field(name=phr['hype'],value=herores[f'hype_{lang}'],inline=False)
                
                stats_values=['<:agi:591659959905812500>',herores['agility'],'\n',
                             '<:str:591659961092669462>',herores['strength'],'\n',
                             '<:int:591659960551604234>',herores['intelligence'],'\n',
                             '<:damage:591659959825989637>',str(herores['attack_damage_min']),'-',str(herores['attack_damage_max']),'\n',
                             '<:armor:591659959960469524>',"%.2f" %(herores['armor']+int(herores["agility"][:2])*0.16),f' ({herores["armor"]})','\n',
                             '<:magic_resist:591659960249745460>',str(herores['magic_resistance']),'%\n',
                             '<:attack_speed:591659960316723230>',str(herores['attack_rate']),'\n',
                             '<:attack_range:591659960027316224>',str(herores['attack_range']),'\n',
                             '<:move_speed:591659960753192960>',str(herores['base_movement']),'\n',
                             '<:turn_rate:591659960857788416>',str(herores['turn_rate']),'\n',
                             '<:vision:591659960794873858>',str(herores['vision_day']),'/',str(herores['vision_night'])]
                stats_value=''
                for value in stats_values:
                    stats_value+=value


                embed.add_field(name=phr['stats'],value=stats_value,inline=True)

                tal=[]
                talents=herores[f'talents_{lang}']
                for talent in reversed(talents):
                        tal.append(talent)
                    
                talents_values=['<:talent_left:594201130905632770>','<:lvl25:591896705339883540>',tal[0],'\n','<:lvl25:591896705339883540>','<:talent_right:594201131325063177>',tal[1],'\n',
                                '<:talent_left:594201130905632770>','<:lvl20:591896705465712649>',tal[2],'\n','<:lvl20:591896705465712649>','<:talent_right:594201131325063177>',tal[3],'\n',
                                '<:talent_left:594201130905632770>','<:lvl15:591896704807075841>',tal[4],'\n','<:lvl15:591896704807075841>','<:talent_right:594201131325063177>',tal[5],'\n',
                                '<:talent_left:594201130905632770>','<:lvl10:591896705071448074>',tal[6],'\n','<:lvl10:591896705071448074>','<:talent_right:594201131325063177>',tal[7],'\n']
                talents_value=''
                for value in talents_values:
                    talents_value+=value
                abils=''
                for abid,abinf in herores['abilities'].items():
                    abils+='__'+abinf['name']+'__\n'
                embed.add_field(name=phr['abils'],value=abils,inline=True)
                embed.add_field(name=phr['talents'],value=talents_value,inline=True)
                await message.channel.send(embed=embed)
                await message.clear_reactions()
            else:
                await message.channel.send(phr['bad_hero'])
                await message.clear_reactions()
                return
            
async def ability(message,client):
    if message.content.startswith('ability',1):
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'
        responses={"en":{"bad_ab":"Ability not found",
                         "error":"An error occured",
                         "later":"Try again in a bit",
                         "abinfo":"Ability information",
                         "desc":"Decription",
                         "addinfo":"Additional info",
                         "cast_point":"Cast point",
                         "stacks":"Stackable?",
                         "y":"Yes",
                         "n":"No",
                         "abs":"Abilities",
                         "spellimm":"Pierces spell immunity?",
                         "dispel":"Dispellable?",
                         "dmgtype":"Damage type",
                         "lore":"Lore",
                         "note":"Note",
                         "hero":"Hero"},
                         
                   "ru":{"bad_ab":"Способность не найдена",
                         "error":"Возникла ошибка",
                         "later":"Попробуйте через пару минут",
                         "abinfo":"Информация о способности",
                         "desc":"Описание",
                         "addinfo":"Доп. информация",
                         "cast_point":"Время применения",
                         "stacks":"Стакается?",
                         "abs":"Способности",
                         "spellimm":"Сквозь невосприимчивость к магии?",
                         "dispel":"Можно развеять?",
                         "dmgtype":"Тип урона",
                         "lore":"Лор",
                         "note":"Примечание",
                         "hero":"Герой"}}

        phr=responses[f"{lang}"]
        command=message.content.split()
        abname = message.content[8:].strip()
        if pref==message.content[0]:
            with open('dotabase/abilities.txt', 'r') as f:
                abss=f.readlines()
                found=False
            for ab in abss:
                abres=dict(eval(ab))
                if abname==abres['name'].lower() or abname==abres['name'].lower().replace("'",""):
                    found=True
                    break


            if found==True:
                await message.add_reaction("⏳")
                
                embed = discord.Embed(title=f'{phr["abinfo"]}',colour=discord.Colour(0x0000aa),url="https://discordapp.com")
                embed.set_footer(text=f"{client.user.name} | {pref}ability", icon_url=client.user.avatar_url_as(format='png'))
                embed.set_thumbnail(url=f'http://dotabase.dillerm.io/dota-vpk{abres["icon"]}')
                embed.add_field(name=f'__**{abres["name"]}**__',value=abres['hero'],inline=False)
                desc=''
                if abres.get(f'desc_{lang}')!=str(None):
                    desc=abres.get(f'desc_{lang}')+'\n'*2
                    if abres.get(f'attr_{lang}',[])!=[]:
                        atrs=''
                        for atr in abres.get(f'attr_{lang}'):
                            desc+=atr+'\n'
                    if abres.get('cast_point')!=None:
                        castpoint=abres.get('cast_point')
                        if castpoint[1:]==castpoint[:-1]:
                            desc+=phr['cast_point'].upper()+': **'+str(castpoint[0])+'**\n'
                        else:
                            desc+=phr['cast_point'].upper()+': **'+'** / **'.join(str(i) for i in castpoint)+'**\n'
                    else:
                        desc+='\n'
                    if abres.get('cooldown')!=[]:
                        cd=abres.get('cooldown')
                        if cd[1:]==cd[:-1]:
                            desc+='\n<:cooldown:595171442652479518> **'+str(cd[0])+'**'
                        else:
                            desc+='\n<:cooldown:595171442652479518> **'+'** / **'.join(str(i) for i in cd)+'**'
                    if abres.get('mana_cost')!=[]:
                        mc=abres.get('mana_cost')
                        if mc[1:]==mc[:-1]:
                            desc+='\n<:manacost:595172991567134721> **'+str(int(mc[0]))+'**'
                        else:
                            desc+='\n<:manacost:595172991567134721>'+'**'+'** / **'.join(str(int(i)) for i in mc)+'**'
                    if abres[f'ags_{lang}']!=None:
                        desc+='\n'+'<:2_:591306566603636747>'+abres[f'ags_{lang}']+'\n'
                    if abres.get(f'dmg_type_{lang}')!=str(None):
                        desc+='\n'+phr['dmgtype']+': **'+abres[f'dmg_type_{lang}']+'**'
                    if abres.get(f'spell_imm_{lang}')!=str(None):
                        desc+='\n'+phr['spellimm']+': **'+abres[f'spell_imm_{lang}']+'**'
                    if abres.get(f'dispel_{lang}')!=str(None):
                        desc+='\n'+phr['dispel']+': **'+abres[f'dispel_{lang}']+'**'
                    embed.add_field(name=phr['desc'],value=desc,inline=False)
                add=''
                if abres[f'note_{lang}']!=[]:
                    add+='ℹ**'+phr['note']+'**\n'
                    for note in abres[f'note_{lang}']:
                        add+=note+'\n'
                if abres[f'lore_{lang}']!=str(None):
                    add+='<:exp:593470312088338441>**'+phr['lore']+'**\n*'+abres[f'lore_{lang}']+'*\n'
                if add!='':
                    embed.add_field(name=phr['addinfo'],value=add,inline=True)

                await message.channel.send(embed=embed)
                await message.clear_reactions()
                
            else:
                await message.channel.send(phr['bad_ab'])
                await message.clear_reactions()
                return

async def item(message,client):
    if message.content.startswith('item',1):
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'
        responses={"en":{"bad_item":"Item not found",
                         "error":"An error occured",
                         "later":"Try again in a bit",
                         "iteminfo":"Item information",
                         "desc":"Decription",
                         "addinfo":"Additional info",
                         "stacks":"Stackable?",
                         "y":"Yes",
                         "n":"No",
                         "abs":"Abilities",
                         "attributes":"Item attributes",
                         "lore":"Lore",
                         "note":"Note"},
                         
                   "ru":{"bad_item":"Предмет не найден",
                         "error":"Возникла ошибка",
                         "later":"Попробуйте через пару минут",
                         "iteminfo":"Информация о предмете",
                         "desc":"Описание",
                         "addinfo":"Доп. информация",
                         "stacks":"Стакается?",
                         "y":"Да",
                         "n":"Нет",
                         "abs":"Способности",
                         "attributes":"Показатели предмета",
                         "lore":"Лор",
                         "note":"Примечание"}}

        phr=responses[f"{lang}"]
        command=message.content.split()
        itemname = message.content[5:].strip()
        if pref==message.content[0]:
            with open('dotabase/items.txt', 'r') as f:
                items=f.readlines()
                found=False
            for item in items:
                itemres=dict(eval(item))
                if itemname==itemres['name'].lower() or itemname in itemres.get('aliases',[]):
                    found=True
                    break


            if found==True:
                await message.add_reaction("⏳")

                embed = discord.Embed(title=f'{phr["iteminfo"]}',colour=discord.Colour(0x9b9b9b),url="https://discordapp.com")
                embed.set_footer(text=f"{client.user.name} | {pref}item", icon_url=client.user.avatar_url_as(format='png'))
                als=itemres.get('aliases')
                if als:
                    aliases=' | '
                    aliases=aliases.join(als)
                else:
                    aliases=u"\u2800"
                embed.add_field(name=f'`{itemres["name"]}`',value=aliases,inline=False)

                if itemres.get(f'itemabs_{lang}',None)!=None:  #абилки если есть
                    abss=itemres[f'itemabs_{lang}']
                    if itemres['cooldown']!=[]:
                        abss+='<:cooldown:595171442652479518>'+'/'.join(i for i in itemres['cooldown'])
                    if itemres['mana_cost']!=[]:
                        abss+='\n<:manacost:595172991567134721>'+'/'.join(i for i in itemres['mana_cost'])
                    embed.add_field(name=phr['abs'],value=abss.replace('$','\n'),inline=False)
                description=''
                if itemres.get(f'attr_{lang}',None)!=None:
                    description+='**'+phr['attributes']+'**\n'+'\n'.join(itemres[f'attr_{lang}'])+'\n<:gold:553976492779110410>'+str(itemres['cost'])+'\n'*2
                if itemres.get(f'note_{lang}',[])!=[]:
                    description+='ℹ**'+phr['note']+'**\n'+'\n'.join(itemres[f'note_{lang}'])+'\n'*2
                if itemres.get(f'lore_{lang}',None)!=None:
                    description+='<:exp:593470312088338441>**'+phr['lore']+'**\n'+'*'+'\n'.join(itemres[f'lore_{lang}'])+'*'
                embed.add_field(name=phr['desc'],value=description,inline=True)
                addinfo=''
                if itemres['stacks']:
                    addinfo+='\n'+phr['stacks']+': **'+phr['y']+'**\n'
                else:
                    addinfo+='\n'+phr['stacks']+': **'+phr['n']+'**\n'
                if itemres['side_shop']:
                    addinfo+='<:side_shop:595167454875877377>'
                if itemres['secret_shop']:
                    addinfo+='<:secret_shop:595167454901174273>'
                embed.add_field(name=phr['addinfo'],value=addinfo,inline=True)
                
                itempic(itemres['id'])
                f=discord.File(fp=f"{itemres['id']}.png")
                embed.set_thumbnail(url=f"attachment://{itemres['id']}.png") 
                await message.channel.send(embed=embed,file=f)
                await message.clear_reactions()
                remove(f"{itemres['id']}.png")
                
            else:
                await message.channel.send(phr['bad_item'])
                await message.clear_reactions()
                return

async def patch(message,client):
    if message.content.startswith('patch',1):
        try:
            lang=getlang(message.guild.id)
        except:
            lang='en'
        try:
            pref=getpref(message.guild.id)
        except:
            pref='!'
        responses={"en":{"bad_req":f"Bad request. Use {pref}patch to get the list of all available game versions",
                         "vers":"List of available versions",
                         "spec":"List of changes in patch ",
                         "no":"No changes in this patch",
                         "general":"General changes",
                         "gen":"General changes available",
                         "nogen":"General changes for this patch are not available",
                         "notes":"Patch notes",
                         "patch":"Patch",
                         "abs":"Abilities",
                         "talents":"<:talents:601688277367652402>Talents<:talents:601688277367652402>",
                         "item":"Items",
                         "hero":"Heroes"},
                         
                   "ru":{"bad_req":f"Проверьте корректность запроса. Список доступных версий можно получить, использовав команду {pref}patch",
                         "vers":"Список доступных версий",
                         "spec":"Список изменений в версии ",
                         "no":"Нет изменений в этом патче",
                         "general":"Общие изменения",
                         "gen":"Доступны общие изменения",
                         "nogen":"Общие изменения недоступны",
                         "notes":"Списки изменений",
                         "patch":"Версия",
                         "abs":"Способности",
                         "talents":"<:talents:601688277367652402>Таланты<:talents:601688277367652402>",
                         "item":"Предметы",
                         "hero":"Герои"}}
        phr=responses[f"{lang}"]
        
        if pref==message.content[0]:
            await message.add_reaction("⏳")
            
            query=message.content.split()
            if len(query)==1:                #game versions available
                embed = discord.Embed(title=phr['notes'],colour=discord.Colour(0x13a788),url=f"http://www.dota2.com/patches/")
                embed.set_footer(text=f"{client.user.name} | {pref}patch", icon_url=client.user.avatar_url_as(format='png'))
                versions=[]
                for notes in glob.glob(f'dotabase\patchnotes\{lang}\*.txt'):
                    versions.append('\n'+u"\u2022"+notes.split('\\')[-1][:-4].replace('_','.'))
                    
                embed.add_field(name=phr['vers'],value=''.join(versions[:21]),inline=True)
                embed.add_field(name=u"\u2800",value=''.join(versions[21:]),inline=True)
                await message.channel.send(embed=embed)
                await message.clear_reactions()
                return
                
            patch=query[-1]
            patch=patch.replace('.','_')
            if patch.startswith('7'): #if the user entered patch number    '\n'+u"\u2022"
                name=' '.join(query[1:-1])
                if len(query) == 2 and name=='':             #list of patch notes for specific version
                    embed = discord.Embed(title=phr['spec'] + query[-1],colour=discord.Colour(0x13a788),url=f"http://www.dota2.com/patches/")
                    embed.set_footer(text=f"{client.user.name} | {pref}patch", icon_url=client.user.avatar_url_as(format='png'))
                    notes_heroes=[]
                    notes_items=[]
                    with open(f'dotabase\patchnotes\{lang}\{patch}.txt') as f:
                        version=dict(eval(f.read()))
                    with open('dotabase\heroes.txt', encoding='utf-8-sig') as f:
                        heroes=f.readlines()
                    with open('dotabase\items.txt') as f:
                        items=f.readlines()
                    #general hz
                    has_gen=False
                    for change in version.keys():
                        found=False
                        if change=='general':
                            embed.title=embed.title+' | '+phr['gen']
                            continue
                        for herof in heroes:
                            hero=dict(eval(herof))
                            if hero['shortname']==change:
                                notes_heroes.append('\n'+u"\u2022"+"<"+hero['emoji']+">**"+hero['name']+'**')
                                found=True
                                break
                        if found==False:
                          for itemf in items:
                            item=dict(eval(itemf))
                            if item['code_name']==change:
                                notes_items.append('\n'+u"\u2022"+'`'+item['name']+'`')
                                break

                    def add_fields(embed,notes,objects):
                        last=len(notes)%20
                        fields=len(notes)//20
                        for i in range(fields+1):
                            if i==0:
                                if fields==0:
                                    embed.add_field(name=phr[objects],value=''.join(notes),inline=True)
                                else:
                                    embed.add_field(name=phr[objects],value=''.join(notes[:20]),inline=True)
                            else:
                                if i!=fields:
                                    embed.add_field(name=u"\u2800",value=''.join(notes[20*i:20*(i+1)]),inline=True)
                                else:
                                    embed.add_field(name=u"\u2800",value=''.join(notes[20*i:]),inline=True)
                                    
                    if notes_heroes!=[]:
                        add_fields(embed,notes_heroes,'hero')
                    if notes_items!=[]:
                        add_fields(embed,notes_items,'item')
                        
                    await message.channel.send(embed=embed)
                    await message.clear_reactions()
                    return




                    
            else: # no number -> retrning info from latest patch
                vers=glob.glob('dotabase\patchnotes\en\*.txt')   
                patch=vers[-1].split('\\')[-1][:-4]
                name=' '.join(query[1:])

            
            if f'dotabase\\patchnotes\\en\\{patch}.txt' in glob.glob('dotabase\patchnotes\en\*.txt'):
                if name=='general':
                    embed = discord.Embed(title=f'{phr["patch"]} {query[-1]} | {phr["general"]}',colour=discord.Colour(0x13a788),url=f"http://www.dota2.com/patches/{patch.replace('_','.')}")
                    embed.set_footer(text=f"{client.user.name} | {pref}patch", icon_url=client.user.avatar_url_as(format='png'))                    
                    with open(f'dotabase/patchnotes/{lang}/{patch}.txt', 'r') as f:
                        version=dict(eval(f.read()))
                    if version.get("general",None)!=None:
                        changes=version["general"]['changes']
                        embed = discord.Embed(title=f'{phr["patch"]} {query[-1]} | {phr["general"]}',description='',colour=discord.Colour(0x13a788),url=f"http://www.dota2.com/patches/{patch.replace('_','.')}")
                        
                        field=False
                        for n in changes:
                            if field==False:
                                t=embed.description
                                embed.description+=u"\u2022"+highlight(n)+'\n'
                            if len(embed.description)>2048:
                                field=True
                                embed.description=t
                                embed.add_field(name=u"\u2800",value=u"\u2800")
                                i=0
                            if field==True:
                                t=embed.fields[i].value
                                embed.fields[i].value+=u"\u2022"+highlight(n)+'\n'
                                if len(embed.fields[i].value)>1024:
                                    embed.fields[i].value=t
                                    embed.add_field(name=u"\u2800",value=u"\u2022"+highlight(n)+'\n')
                                    i+=1                                                                    
                                
                        embed.set_footer(text=f"{client.user.name} | {pref}patch", icon_url=client.user.avatar_url_as(format='png'))
                        embed.description=embed.description.replace(u"\u2022"+'\n','\n')
                        await message.channel.send(embed=embed)
                        await message.clear_reactions()
                        return
                    else:
                        await message.channel.send(phr["nogen"])
                        await message.clear_reactions()
                        return
                else:  
                  with open('dotabase/heroes.txt', 'r', encoding='utf-8-sig') as f:
                    heroes=f.readlines()
                    for herof in heroes:
                        hero=dict(eval(herof))
                        if name in hero['aliases'] or name.lower()==hero['name'].lower():
                            shortname=hero['shortname']
                            icon=hero['icon']
                            embed = discord.Embed(title=f'{phr["patch"]} {query[-1]} | <{hero["emoji"]}>**{hero["name"]}**',colour=discord.Colour(0x13a788),url=f"http://www.dota2.com/patches/{patch.replace('_','.')}")
                            embed.set_footer(text=f"{client.user.name} | {pref}patch", icon_url=client.user.avatar_url_as(format='png'))
                            embed.set_thumbnail(url=f'http://cdn.dota2.com/apps/dota2/images/heroes/{icon}')
                            with open(f'dotabase/patchnotes/{lang}/{patch}.txt', 'r') as f:
                                version=dict(eval(f.read()))
                            if version.get(shortname,None)!=None:
                                hero=version[shortname]
                                if hero.get('general',None)!=None:
                                    embed.add_field(name=phr['general'],value='\n'.join(u"\u2022"+highlight(n) for n in hero['general']))
                                if hero.get('abilities',None)!=None:
                                    for ab in hero['abilities'].keys():
                                         embed.add_field(name=f'__{ab}__',value='\n'.join(u"\u2022"+highlight(n) for n in hero['abilities'][ab]))
                                if hero.get('talents',None)!=None:
                                    embed.add_field(name=phr['talents'],value='\n'.join(u"\u2022"+highlight(n) for n in hero['talents']))
                                await message.channel.send(embed=embed)
                                await message.clear_reactions()
                                return
                            else:
                                await message.channel.send(phr['no'])
                                await message.clear_reactions()
                                return


                  with open('dotabase/items.txt', 'r') as f:
                    items=f.readlines()
                    for itemf in items:
                        item=dict(eval(itemf))
                        if name in item['aliases'] or name.lower()==item['name'].lower():
                            shortname=item['code_name']
                            icon=item['icon']
                            embed = discord.Embed(title=f'{phr["patch"]} {query[-1]} | `{item["name"]}`',colour=discord.Colour(0x13a788),url=f"http://www.dota2.com/patches/{patch.replace('_','.')}")
                            embed.set_footer(text=f"{client.user.name} | {pref}patch", icon_url=client.user.avatar_url_as(format='png'))
                                                    
                            with open(f'dotabase/patchnotes/{lang}/{patch}.txt', 'r') as f:
                                version=dict(eval(f.read()))
                            if version.get(shortname,None)!=None:
                                itempatch=version[shortname]
                                if itempatch.get('item',None)!=None:
                                    embed.add_field(name=phr['general'],value='\n'.join(u"\u2022"+highlight(n) for n in itempatch['item']))
                                itempic(item['id'])
                                f=discord.File(fp=f"{item['id']}.png")
                                embed.set_thumbnail(url=f"attachment://{item['id']}.png") 
                                await message.channel.send(embed=embed,file=f)
                                await message.clear_reactions()
                                remove(f"{item['id']}.png")
                                return
                            else:
                                await message.channel.send(phr['no'])
                                await message.clear_reactions()
                                return
                  await message.channel.send(phr['bad_req'])
                  await message.clear_reactions()
                  return


            else:
                await message.channel.send(phr['bad_req'])
                await message.clear_reactions()
                return
        
def info(message,client,page):
        if message.content.startswith('info',1) and message.content.endswith('info') or message.content.startswith('tome',1) and message.content.endswith('tome'):
            try:
                lang=getlang(message.guild.id)
            except:
                lang='en'
            try:
                pref=getpref(message.guild.id)
            except:
                pref='!'
        with open('dotabase/tome.txt','r', encoding='utf-8') as f:
            dota_mechanics=dict(eval(f.read()))
            

        page_emojis=['<:page_1:599965301496348722>','<:page_2:599965301466988545>','<:page_3:599965301504999444>','<:page_4:599965301496348711>','<:page_5:599965301500542995>','<:page_6:599965301295153153>','<:page_7:599965301366456342>','<:page_8:599965301513125898>','<:page_9:599965301500542987>','<:page_10:599965301525839897>','<:page_11:600339370871881768>']
        responses={"en":{"conts":"__Contents__",
                         "error":"An error occured"},
                         
                   "ru":{"conts":"__Содержание__",
                         "error":"Возникла ошибка"}}
        phr=responses[f"{lang}"]

        
        if pref==message.content[0]:

                if page=='main':
                        embed = discord.Embed(title='<:exp:593470312088338441>Tome of Knowledge<:exp:593470312088338441>',colour=discord.Colour(0x9d10bb))
                        embed.set_thumbnail(url="https://gamepedia.cursecdn.com/dota2_gamepedia/f/fc/Tome_of_Knowledge_icon.png")
                        embed.set_footer(text=f"{client.user.name} | {pref}info", icon_url=client.user.avatar_url_as(format='png'))
                        i=0
                        cats=''
                        categories={}
                        for cat in dota_mechanics[lang].keys():
                            categories[page_emojis[i]]=cat
                            cats+=page_emojis[i]+cat+'\n'
                            i+=1
                        embed.add_field(name=phr['conts'],value=cats,inline=False)
                        return {'msg':embed,'emojis':categories}


                elif page in dota_mechanics[lang].keys():
                        embed = discord.Embed(title='<:exp:593470312088338441>Tome of Knowledge<:exp:593470312088338441>',colour=discord.Colour(0x9d10bb))
                        embed.set_thumbnail(url="https://gamepedia.cursecdn.com/dota2_gamepedia/f/fc/Tome_of_Knowledge_icon.png")
                        embed.set_footer(text=f"{client.user.name} | {pref}info", icon_url=client.user.avatar_url_as(format='png'))
                        i=0
                        mecs=''
                        mechanics={}
                        for mec in dota_mechanics[lang][page].keys():
                            mechanics[page_emojis[i]]=mec
                            mecs+=page_emojis[i]+mec+'\n'
                            i+=1
                        embed.add_field(name="__"+page+"__",value=mecs,inline=False)
                        return {'msg':embed,'emojis':mechanics}

                else:
                    for cat in dota_mechanics[lang].keys():
                        for mec in dota_mechanics[lang][cat].keys():
                            if page == mec:
                                embed = discord.Embed(title='<:exp:593470312088338441>Tome of Knowledge<:exp:593470312088338441>',colour=discord.Colour(0x9d10bb))
                                #embed.set_thumbnail(url="https://gamepedia.cursecdn.com/dota2_gamepedia/f/fc/Tome_of_Knowledge_icon.png")
                                embed.set_footer(text=f"{client.user.name} | {pref}info", icon_url=client.user.avatar_url_as(format='png'))
                                for field in dota_mechanics[lang][cat][mec].keys():
                                    embed.add_field(name=field,value=dota_mechanics[lang][cat][mec][field],inline=True)
                                return embed
def highlight(string):
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
