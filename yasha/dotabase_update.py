from dotabase import *
from pprint import pprint as pp
import requests
import json
import re
from tools import highlight



def removezero(llist):
    tt=[]
    for t in llist:
        if t==int(t):
            tt.append(str(int(t)))
        else:
            tt.append(str(t))
    return tt
'''
HERO DATA EXAMPLE
{'abilities': {'5069': 'Illusory Orb',
               '5070': 'Ethereal Jaunt',
               '5071': 'Waning Rift',
               '5072': 'Phase Shift',
               '5073': 'Dream Coil'},
 'agility': '22 + 1.7',
 'aliases': [],
 'armor': -1,
 'attack_damage_max': 41,
 'attack_damage_min': 30,
 'attack_range': 550,
 'attack_rate': 1.7,
 'attr_primary': 'intelligence',
 'banmoji': ':ban13:591513802605068289',
 'base_armor': -1,
 'base_attack_speed': 100,
 'base_health_regen': 0.5,
 'base_mana_regen': 0.0,
 'base_movement': 290,
 'emoji': ':puck:553951283485343744',
 'hype_en': 'Puck has a talent for confounding its enemies with playfully '
            'elusive mischief. By teleporting to its damaging orb in order to '
            'hop short distances, it attacks foes with bursts of silencing '
            'dust. By the time its enemies can react, Puck has long since '
            'escaped.',
 'hype_ru': 'Игривый и увёртливый Puck мастерски запутывает противников. Он '
            'может перемещаться на небольшие расстояния с помощью своей '
            'смертоносной сферы и обезмолвить врагов магической пылью. А когда '
            'противник опомнится, будет слишком поздно: Puck уже исчезнет за '
            'горизонтом.',
 'icon': 'puck_lg.png',
 'id': 13,
 'intelligence': '23 + 3.5',
 'magic_resistance': 25,
 'name': 'Puck',
 'shortname': 'puck',
 'strength': '17 + 2.4',
 'talents_en': ['+6 All Stats',
                '+150 Cast Range',
                '+15% Spell Amplification',
                '+90 Damage',
                '-8s Waning Rift Cooldown',
                '+40% Illusory Orb Distance/Speed',
                '+420 Gold/Min',
                'Dream Coil Rapid Fire'],
 'talents_ru': ['+6 ко всем атрибутам',
                '+150 к дальности способностей',
                '+15% к урону от способностей',
                '+90 к урону',
                '-8 сек. перезарядки Waning Rift',
                '+40% к скорости и дальности Illusory Orb',
                '+420 золота в минуту',
                'Быстрые атаки по жертвам Dream Coil'],
 'turn_rate': 0.5,
 'vision_day': 1800,
 'vision_night': 800}
 '''
    #структура
    #hero  DOTA_Patch_{patch}_[hero_short_name]_([talent])_n         (DOTA_Patch_7_22_meepo_talent_2)
    #item  DOTA_Patch_{patch}_[item_code_name]_n                     (DOTA_Patch_7_22_item_wraith_band)
    #ab    DOTA_Patch_{patch}_[hero_short_name]_[ab_code_name]_n     (DOTA_Patch_7_22_jakiro_jakiro_liquid_fire)
    #general DOTA_Patch_7_21_General_11

def parsenotes(patchnotes,lang):
    with open('dotabase/heroes.txt', 'r', encoding='utf-8-sig') as t:
        heroes=t.readlines()
    with open('dotabase/items.txt', 'r', encoding='utf-8-sig') as t:
        items=t.readlines()
    filenames=[]
    curnote=''
    for note in patchnotes:
        note['text']=note['text'].replace('<br>','\n')
        patchid = note['id'].split('_')
        patchnumber = patchid[2]+'_'+patchid[3]
        if patchnumber not in filenames:
            if filenames!=[]:
                with open(f'dotabase\patchnotes\{lang}\{filenames[-1]}.txt','w') as f:
                    f.write(str(version).replace('ó','o'))
                    print(filenames[-1])
            curnote=''
            filenames.append(patchnumber)
            version={}
            patch={}
        if note['id'].startswith(f'DOTA_Patch_{patchnumber}'):
            if note['id'].startswith(f'DOTA_Patch_{patchnumber}_General'):
                if curnote!='general':
                    if patch!={}:
                        version[curnote]=patch
                        patch={'changes':[]}
                        curnote='general'
                note['text']=note['text'].replace('<h2>','**')
                note['text']=note['text'].replace('</h2>','**')
                if patch=={}:
                    curnote='general'
                    patch={'changes':[]}
                patch['changes'].append(re.sub(r'<(.+?)>','',note['text']))
                
                continue
            for herof in heroes:
                hero = dict(eval(herof))
                if hero['shortname'] in note['id']:
                    if curnote!=hero['shortname']:
                        if patch!={}:
                            version[curnote]=patch
                        curnote=hero['shortname']
                        patch = {}
                    if note['id'].startswith(f'DOTA_Patch_{patchnumber}_{hero["shortname"]}_{hero["shortname"]}') or note['id'].startswith(f'DOTA_Patch_{patchnumber}_{hero["shortname"]}_{hero["shortname"].replace("_","")}'): #абилки
                        if patch.get('abilities',None)==None:
                            patch['abilities']={}
                        for ab in hero['abilities'].keys():
                            if ab in note['id']:
                                name=hero['abilities'][ab]['name']
                                if patch['abilities'].get(name,None)==None:
                                    patch['abilities'][name]=[]
                                patch['abilities'][name].append(re.sub(r'<(.+?)>','**',note['text']))
                    elif 'talent' in note['id'].lower():
                        if patch.get('talents',None)==None:
                            patch['talents']=[]
                        patch['talents'].append(re.sub(r'<(.+?)>','**',note['text']))
                    else:
                        if patch.get('general',None)==None:
                            patch['general']=[]
                        patch['general'].append(re.sub(r'<(.+?)>','**',note['text']))
                    break
            for itemf in items:
                item = dict(eval(itemf))
                if item['code_name'] in note['id']:         
                    if curnote!=item['code_name']:
                        if patch!={}:
                            version[curnote]=patch
                        curnote=item['code_name']
                        patch = {}
                    if patch.get('item',None)==None:
                        patch['item']=[]
                    patch['item'].append(re.sub(r'<(.+?)>','**',note['text']))
                    break
                
    with open(f'dotabase\patchnotes\{lang}\{filenames[-1]}.txt','w') as f:
        f.write(str(version).replace('ó','o'))
        print(filenames[-1])

                
def updatepatchnotes():
    
    r = requests.get('https://api.stratz.com/api/v1/Patch/notes?LanguageId=0')
    patchnotes_en = json.loads(r.text)
    r = requests.get(f"https://api.stratz.com/api/v1/Patch/notes?LanguageId=19")
    patchnotes_ru=json.loads(r.text)
    parsenotes(patchnotes_en,'en')
    parsenotes(patchnotes_ru,'ru')

def updateversion():
    r = requests.get('https://api.stratz.com/api/v1/GameVersion')
    versions = json.loads(r.text)
    fver={}
    with open('dotabase/version.txt','w') as f:
        for ver in versions:
            fver[ver['name']]=ver['id']
        f.write(str(fver))

     
def updateheroes():
    session = dotabase_session()
    r = requests.get(f"https://api.stratz.com/api/v1/Hero/?LanguageId=0")
    allheroesinfo_en=json.loads(r.text)
    r = requests.get(f"https://api.stratz.com/api/v1/Hero/?LanguageId=19")
    allheroesinfo_ru=json.loads(r.text)
    r = requests.get(f"https://api.stratz.com/api/v1/Ability?LanguageId=0")
    talentsinfo_en=json.loads(r.text)
    r = requests.get(f"https://api.stratz.com/api/v1/Ability?LanguageId=19")
    talentsinfo_ru=json.loads(r.text)
    
    count=0
    with open('dotabase/heroes.txt', mode='r', encoding='utf-8-sig') as f:
        lines=f.readlines()
    for line in lines:
            f=open('dotabase/heroes.txt', mode='r', encoding='utf-8-sig')
            lines=f.readlines()
            hero=dict(eval(line))
            
            for herobase in session.query(Hero):
                if herobase.id==hero['id']:
                    f.close()
                    f = open("dotabase/heroes.txt",mode="w", encoding='utf-8-sig')
                    for line in lines:
                        t=dict(eval(line))
                        if herobase.id!=t['id']:
                            f.write(line)
                        if herobase.id==t['id']:
                            heroesinfo_en=allheroesinfo_en.get(str(t['id']))
                            heroesinfo_ru=allheroesinfo_ru.get(str(t['id']))
                            t['name']=herobase.localized_name
                            t['shortname']=heroesinfo_en.get('shortName')
                            t['aliases']=heroesinfo_en.get('aliases',[])
                            t['hype_ru']=heroesinfo_ru['language'][0]['hype']
                            t['hype_en']=heroesinfo_en['language'][0]['hype']
                            t['hype_ru']=t['hype_ru'].replace('é','е')
                            t['hype_ru']=t['hype_ru'].replace('ó','о')
                            t['hype_en']=t['hype_en'].replace('é','e')
                            t['base_movement']=herobase.base_movement
                            t['turn_rate']=herobase.turn_rate
                            t['base_armor']=herobase.base_armor
                            t['attack_range']=herobase.attack_range
                            t['attack_damage_min']=herobase.attack_damage_min
                            t['attack_damage_max']=herobase.attack_damage_max
                            t['attack_rate']=herobase.attack_rate
                            t['attr_primary']=herobase.attr_primary
                            t['strength']=f'{int(herobase.attr_strength_base)} + {herobase.attr_strength_gain}'
                            t['intelligence']=f'{herobase.attr_intelligence_base} + {herobase.attr_intelligence_gain}'
                            t['agility']=f'{herobase.attr_agility_base} + {herobase.attr_agility_gain}'
                            t['vision_day']=herobase.vision_day
                            t['vision_night']=herobase.vision_night
                            t['magic_resistance']=herobase.magic_resistance
                            
                            habs={}
                            for ability in herobase.abilities:
                                habs[ability.name]={'name':ability.localized_name,'id':ability.id}
                            t['abilities']=habs
            
                            htals_ru=[]
                            htals_en=[]
                            for tal in heroesinfo_en['talents']:
                                tid=str(tal["abilityId"])
                                htals_en.append(talentsinfo_en[tid]['language'][0]['displayName'])
                                htals_ru.append(talentsinfo_ru[tid]['language'][0]['displayName'])
                            t['talents_en']=htals_en
                            t['talents_ru']=htals_ru
                            
                            
                            f.write("{0}\n".format(t))
                            count+=1
                            if count==1:
                                pp(t)
                            print(count)
                    f.close()
                    break

def updateitems_no_als():  ##без прозвищ (например Black King Bar - bkb) т.к. большинство было нужно вводить вручную 
    session = dotabase_session()
    itemswrec=[]
    count=0
    try:                    #запрос инфы о предметах
        r = requests.get(f"https://api.stratz.com/api/v1/Item?LanguageId=0")
        itemsinfo_en=json.loads(r.text)
        r = requests.get(f"https://api.stratz.com/api/v1/Item?LanguageId=19")
        itemsinfo_ru=json.loads(r.text)
    except Exception as e:                           
        raise

    for item in session.query(Item):
        if item.icon=='/panorama/images/items/recipe.png':
            itemswrec.append(item.localized_name[:-7])


    count=0
    with open('dotabase/items.txt', mode='r') as f:
        lines=f.readlines()
    for line in lines:
        f=open('dotabase/items.txt', mode='r')
        lines=f.readlines()
        itemf=dict(eval(line))
        for itembase in session.query(Item):
            if itembase.id==itemf['id']:
                f.close()
                f = open("dotabase/items.txt",mode="w")
                for line in lines:
                    t=dict(eval(line))
                    if itembase.id!=t['id']:
                        f.write(line)
                    if itembase.id==t['id']:
                        fullitem_en = itemsinfo_en.get(str(t['id']))
                        fullitem_ru = itemsinfo_ru.get(str(t['id']))
                        iteminfo=t
                        if item.icon=='/panorama/images/items/recipe.png':
                            continue
                        else:
                            if item.localized_name in itemswrec:
                                iteminfo['need_recipe']=True
                            else:
                                iteminfo['need_recipe']=False
                            iteminfo['icon']=f'dotabase/items/{item.id}.png'
                            iteminfo['code_name']=itembase.name
                        if fullitem_en['language'][0]['description']:  #абилки если есть
                                itemabs_en=''
                                for abil in fullitem_en['language'][0]['description']:
                                    desc=abil
                                    desc=desc.replace('<h1>','__')
                                    desc=desc.replace('</h1>','__$')
                                    desc=desc.replace('<br>','$')
                                    desc=desc.replace('<BR>','$')
                                    desc=re.sub(r'<(.+?)>','**',desc)
                                    nums_en=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",desc)
                                    res=''
                                    if 'Dagon' in iteminfo['name']:
                                        print(iteminfo['aliases'])
                                        n=int(iteminfo['aliases'][0][-1])-1
                                        dd=desc.index('$$')
                                        subs=desc[dd:].split('$')
                                        subsr=[]
                                        for sub in subs:
                                            nums_sub=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",sub)
                                            if len(nums_sub)>1:
                                                sub=sub.replace(nums_sub[n],'**'+nums_sub[n]+'**')
                                            elif len(nums_sub)==1:
                                                sub=sub.replace(nums_sub[0],'**'+nums_sub[0]+'**')
                                            subsr.append(sub)
                                        res=desc[:dd]+'$'.join(subsr)
                                        itemabs_en+=res+'$'
                                    elif iteminfo['name']=='Necronomicon':
                                        n=int(iteminfo['aliases'][0][-1])-1
                                        dd=desc.index('$$')
                                        subs=desc[dd:].split('$')
                                        subsr=[]
                                        for sub in subs:
                                            nums_sub=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",sub)
                                            if len(nums_sub)>1:
                                                sub=sub.replace(nums_sub[n],'**'+nums_sub[n]+'**')
                                            elif len(nums_sub)==1: 
                                                sub=sub.replace(nums_sub[0],'**'+nums_sub[0]+'**')
                                            subsr.append(sub)
                                        res=desc[:dd].replace('60','**60**')+'$'.join(subsr)
                                        itemabs_en+=res+'$'
                                    else:
                                      for num in nums_en:
                                        t=desc[:desc.index(num)+len(num)]
                                        t=t.replace(num,'**'+num+'**')
                                        desc=desc[desc.index(num)+len(num):]
                                        res+=t
                                      itemabs_en+=res+desc+'$'
                                iteminfo['itemabs_en']=itemabs_en



                                itemabs_ru=''                   
                                for abil in fullitem_ru['language'][0]['description']:
                                    desc=abil
                                    desc=desc.replace('<h1>','__')
                                    desc=desc.replace('</h1>','__$')
                                    desc=desc.replace('<br>','$')
                                    desc=desc.replace('<BR>','$')
                                    desc=re.sub(r'<(.+?)>','**',desc)
                                    nums_ru=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",desc)
                                    res=''
                                    if iteminfo['name']=='Dagon':
                                        n=int(iteminfo['aliases'][0][-1])-1
                                        dd=desc.index('$$')
                                        subs=desc[dd:].split('$')
                                        subsr=[]
                                        for sub in subs:
                                            nums_sub=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",sub)
                                            if len(nums_sub)>1:
                                                sub=sub.replace(nums_sub[n],'**'+nums_sub[n]+'**')
                                            elif len(nums_sub)==1:
                                                sub=sub.replace(nums_sub[0],'**'+nums_sub[0]+'**')
                                            subsr.append(sub)
                                        res=desc[:dd]+'$'.join(subsr)
                                        itemabs_ru+=res+'$'
                                    elif 'Necronomicon' in iteminfo['name']:
                                        n=int(iteminfo['aliases'][0][-1])-1
                                        dd=desc.index('$$')
                                        subs=desc[dd:].split('$')
                                        subsr=[]
                                        for sub in subs:
                                            nums_sub=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",sub)
                                            if len(nums_sub)>1:
                                                sub=sub.replace(nums_sub[n],'**'+nums_sub[n]+'**')
                                            elif len(nums_sub)==1:
                                                sub=sub.replace(nums_sub[0],'**'+nums_sub[0]+'**')
                                            subsr.append(sub)
                                        res=desc[:dd].replace('60','**60**')+'$'.join(subsr)
                                        itemabs_ru+=res+'$'
                                    else:
                                      for num in nums_ru:
                                        t=desc[:desc.index(num)+len(num)]
                                        t=t.replace(num,'**'+num+'**')
                                        desc=desc[desc.index(num)+len(num):]
                                        res+=t
                                      itemabs_ru+=res+desc+'$'
                                iteminfo['itemabs_ru']=itemabs_ru

                        if fullitem_en.get('stat',None)!=None:
                            iteminfo['cooldown']=removezero(fullitem_en['stat'].get('cooldown',[]))
                            if iteminfo['cooldown']!=[]:
                                if len(iteminfo['cooldown'])>1:
                                    iteminfo['cooldown'][int(iteminfo['aliases'][0][-1])-1]='**'+iteminfo['cooldown'][int(iteminfo['aliases'][0][-1])-1]+'**'
                            iteminfo['mana_cost']=removezero(fullitem_en['stat'].get('manaCost',[]))
                            if iteminfo['mana_cost']!=[]:
                                if len(iteminfo['mana_cost'])>1:
                                    iteminfo['mana_cost'][int(iteminfo['aliases'][0][-1])-1]='**'+iteminfo['mana_cost'][int(iteminfo['aliases'][0][-1])-1]+'**'
                            iteminfo['cost']=fullitem_en['stat'].get('cost',None)
                            iteminfo['stacks']=fullitem_en['stat']['isStackable']
                            iteminfo['side_shop'] = fullitem_en['stat']['isSideShop']
                            iteminfo['secret_shop'] = fullitem_en['stat']['isSecretShop']
                    
                        if fullitem_en['language'][0]['attributes']!=[]:
                                iteminfo['attr_en']=fullitem_en['language'][0]['attributes']
                                iteminfo['attr_ru']=fullitem_ru['language'][0]['attributes']

                                i=0
                                for atr in iteminfo['attr_en']:
                                    atr=re.sub(r'<(.+?)>','**',atr)
                                    nums_en=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",atr)
                                    res=''
                                    if iteminfo['aliases']:
                                      if iteminfo['aliases'][0][-1].isdigit() and len(nums_en)>1:
                                        res=atr.replace(nums_en[int(iteminfo['aliases'][0][-1])-1],'**'+nums_en[int(iteminfo['aliases'][0][-1])-1]+'**')
                                      else:
                                       for num in nums_en:
                                        res=atr.replace(num,'**'+num+'**')
                                    else:    
                                      for num in nums_en:
                                        res=atr.replace(num,'**'+num+'**')
                                    iteminfo['attr_en'][i]=res
                                    i+=1
                                j=0
                                for atr in iteminfo['attr_ru']:
                                    atr=re.sub(r'<(.+?)>','**',atr)
                                    nums_ru=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",atr)
                                    res=''
                                    if iteminfo['aliases']:
                                      if iteminfo['aliases'][0][-1].isdigit() and len(nums_ru)>1:
                                        res=atr.replace(nums_ru[int(iteminfo['aliases'][0][-1])-1],'**'+nums_ru[int(iteminfo['aliases'][0][-1])-1]+'**')
                                      else:
                                       for num in nums_ru:
                                        res=atr.replace(num,'**'+num+'**')
                              
                                    else:    
                                      for num in nums_ru:
                                        res=atr.replace(num,'**'+num+'**')
                                    iteminfo['attr_ru'][j]=res
                                    j+=1

                        iteminfo['note_en']=fullitem_en['language'][0].get('notes',None)
                        iteminfo['note_ru']=fullitem_ru['language'][0].get('notes',None)
                        if iteminfo['note_en']!=None:
                                i=0
                                for note in iteminfo['note_en']:
                                    nums_en=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",note)
                                    for num in nums_en:
                                        note=note.replace(num,'**'+num+'**')
                                    iteminfo['note_en'][i]=note
                                    i+=1
                                j=0
                                for note in iteminfo['note_ru']:
                                    nums_ru=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",note)
                                    for num in nums_ru:
                                        note=note.replace(num,'**'+num+'**')
                                    iteminfo['note_ru'][j]=note
                                    j+=1
                        iteminfo['lore_en']=fullitem_en['language'][0].get('lore',None)
                        iteminfo['lore_ru']=fullitem_ru['language'][0].get('lore',None)
                        f.write("{0}\n".format(iteminfo))
                        count+=1
                        print(count)
                        
def updateitems_with_als(): ##full update
    with open('dotabase/items.txt', 'w') as f:
        session = dotabase_session()
        itemswrec=[]
        count=0
        try:                    #запрос инфы о предметах
            r = requests.get(f"https://api.stratz.com/api/v1/Item?LanguageId=0")
            itemsinfo_en=json.loads(r.text)
            r = requests.get(f"https://api.stratz.com/api/v1/Item?LanguageId=19")
            itemsinfo_ru=json.loads(r.text)
        except Exception as e:                           
            raise

        for item in session.query(Item):
            if item.icon=='/panorama/images/items/recipe.png':
                print(item.localized_name[:-7])
                itemswrec.append(item.localized_name[:-7])
        for item in session.query(Item):
            fullitem_en = itemsinfo_en.get(str(item.id))
            fullitem_ru = itemsinfo_ru.get(str(item.id))
            iteminfo={}
            als=item.aliases.split('|')
            for al in als:
                if al==item.localized_name.lower():
                    als.remove(al)
            if als==['']:
                als=[]
            iteminfo['id']=item.id
            iteminfo['name']=item.localized_name
            iteminfo['aliases']=als
            if item.icon=='/panorama/images/items/recipe.png':
                continue
            else:
                if item.localized_name in itemswrec:
                    iteminfo['need_recipe']=True
                else:
                    iteminfo['need_recipe']=False
                iteminfo['icon']=f'dotabase/items/{item.id}.png'
            if fullitem_en['language'][0]['description']:  #абилки если есть
                    itemabs_en=''
                    for abil in fullitem_en['language'][0]['description']:
                        desc=abil
                        desc=desc.replace('<h1>','__')
                        desc=desc.replace('</h1>','__$')
                        desc=desc.replace('<br>','$')
                        desc=desc.replace('<BR>','$')
                        desc=re.sub(r'<(.+?)>','**',desc)
                        nums_en=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",desc)
                        res=''
                        if iteminfo['name']=='Dagon':
                            n=int(iteminfo['aliases'][0][-1])-1
                            dd=desc.index('$$')
                            subs=desc[dd:].split('$')
                            subsr=[]
                            for sub in subs:
                                nums_sub=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",sub)
                                if len(nums_sub)>1:
                                    sub=sub.replace(nums_sub[n],'**'+nums_sub[n]+'**')
                                elif len(nums_sub)==1:
                                    sub=sub.replace(nums_sub[0],'**'+nums_sub[0]+'**')
                                subsr.append(sub)
                            res=desc[:dd]+'$'.join(subsr)
                            itemabs_en+=res+'$'
                        elif iteminfo['name']=='Necronomicon':
                            n=int(iteminfo['aliases'][0][-1])-1
                            dd=desc.index('$$')
                            subs=desc[dd:].split('$')
                            subsr=[]
                            for sub in subs:
                                nums_sub=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",sub)
                                if len(nums_sub)>1:
                                    sub=sub.replace(nums_sub[n],'**'+nums_sub[n]+'**')
                                elif len(nums_sub)==1: 
                                    sub=sub.replace(nums_sub[0],'**'+nums_sub[0]+'**')
                                subsr.append(sub)
                            res=desc[:dd].replace('60','**60**')+'$'.join(subsr)
                            itemabs_en+=res+'$'
                        else:
                          for num in nums_en:
                            t=desc[:desc.index(num)+len(num)]
                            t=t.replace(num,'**'+num+'**')
                            desc=desc[desc.index(num)+len(num):]
                            res+=t
                          itemabs_en+=res+desc+'$'
                    iteminfo['itemabs_en']=itemabs_en



                    itemabs_ru=''                   
                    for abil in fullitem_ru['language'][0]['description']:
                        desc=abil
                        desc=desc.replace('<h1>','__')
                        desc=desc.replace('</h1>','__$')
                        desc=desc.replace('<br>','$')
                        desc=desc.replace('<BR>','$')
                        desc=re.sub(r'<(.+?)>','**',desc)
                        nums_ru=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",desc)
                        res=''
                        if iteminfo['name']=='Dagon':
                            n=int(iteminfo['aliases'][0][-1])-1
                            dd=desc.index('$$')
                            subs=desc[dd:].split('$')
                            subsr=[]
                            for sub in subs:
                                nums_sub=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",sub)
                                if len(nums_sub)>1:
                                    sub=sub.replace(nums_sub[n],'**'+nums_sub[n]+'**')
                                elif len(nums_sub)==1:
                                    sub=sub.replace(nums_sub[0],'**'+nums_sub[0]+'**')
                                subsr.append(sub)
                            res=desc[:dd]+'$'.join(subsr)
                            itemabs_ru+=res+'$'
                        elif iteminfo['name']=='Necronomicon':
                            n=int(iteminfo['aliases'][0][-1])-1
                            dd=desc.index('$$')
                            subs=desc[dd:].split('$')
                            subsr=[]
                            for sub in subs:
                                nums_sub=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",sub)
                                if len(nums_sub)>1:
                                    sub=sub.replace(nums_sub[n],'**'+nums_sub[n]+'**')
                                elif len(nums_sub)==1:
                                    sub=sub.replace(nums_sub[0],'**'+nums_sub[0]+'**')
                                subsr.append(sub)
                            res=desc[:dd].replace('60','**60**')+'$'.join(subsr)
                            itemabs_ru+=res+'$'
                        else:
                          for num in nums_ru:
                            t=desc[:desc.index(num)+len(num)]
                            t=t.replace(num,'**'+num+'**')
                            desc=desc[desc.index(num)+len(num):]
                            res+=t
                          itemabs_ru+=res+desc+'$'
                    iteminfo['itemabs_ru']=itemabs_ru

            if fullitem_en.get('stat',None)!=None:
                iteminfo['cooldown']=removezero(fullitem_en['stat'].get('cooldown',[]))
                if iteminfo['cooldown']!=[]:
                    if len(iteminfo['cooldown'])>1:
                        iteminfo['cooldown'][int(iteminfo['aliases'][0][-1])-1]='**'+iteminfo['cooldown'][int(iteminfo['aliases'][0][-1])-1]+'**'
                iteminfo['mana_cost']=removezero(fullitem_en['stat'].get('manaCost',[]))
                if iteminfo['mana_cost']!=[]:
                    if len(iteminfo['mana_cost'])>1:
                        iteminfo['mana_cost'][int(iteminfo['aliases'][0][-1])-1]='**'+iteminfo['mana_cost'][int(iteminfo['aliases'][0][-1])-1]+'**'
                iteminfo['cost']=fullitem_en['stat'].get('cost',None)
                iteminfo['stacks']=fullitem_en['stat']['isStackable']
                iteminfo['side_shop'] = fullitem_en['stat']['isSideShop']
                iteminfo['secret_shop'] = fullitem_en['stat']['isSecretShop']
                    
            if fullitem_en['language'][0]['attributes']!=[]:
                    iteminfo['attr_en']=fullitem_en['language'][0]['attributes']
                    iteminfo['attr_ru']=fullitem_ru['language'][0]['attributes']

                    i=0
                    for atr in iteminfo['attr_en']:
                        atr=re.sub(r'<(.+?)>','**',atr)
                        nums_en=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",atr)
                        res=''
                        if iteminfo['aliases']:
                          if iteminfo['aliases'][0][-1].isdigit() and len(nums_en)>1:
                            res=atr.replace(nums_en[int(iteminfo['aliases'][0][-1])-1],'**'+nums_en[int(iteminfo['aliases'][0][-1])-1]+'**')
                          else:
                           for num in nums_en:
                            res=atr.replace(num,'**'+num+'**')
                        else:    
                          for num in nums_en:
                            res=atr.replace(num,'**'+num+'**')
                        iteminfo['attr_en'][i]=res
                        i+=1
                    j=0
                    for atr in iteminfo['attr_ru']:
                        atr=re.sub(r'<(.+?)>','**',atr)
                        nums_ru=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",atr)
                        res=''
                        if iteminfo['aliases']:
                          if iteminfo['aliases'][0][-1].isdigit() and len(nums_ru)>1:
                            res=atr.replace(nums_ru[int(iteminfo['aliases'][0][-1])-1],'**'+nums_ru[int(iteminfo['aliases'][0][-1])-1]+'**')
                          else:
                           for num in nums_ru:
                            res=atr.replace(num,'**'+num+'**')
                              
                        else:    
                          for num in nums_ru:
                            res=atr.replace(num,'**'+num+'**')
                        iteminfo['attr_ru'][j]=res
                        j+=1

            iteminfo['note_en']=fullitem_en['language'][0].get('notes',None)
            iteminfo['note_ru']=fullitem_ru['language'][0].get('notes',None)
            if iteminfo['note_en']!=None:
                    i=0
                    for note in iteminfo['note_en']:
                        nums_en=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",note)
                        for num in nums_en:
                            note=note.replace(num,'**'+num+'**')
                        iteminfo['note_en'][i]=note
                        i+=1
                    j=0
                    for note in iteminfo['note_ru']:
                        nums_ru=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",note)
                        for num in nums_ru:
                            note=note.replace(num,'**'+num+'**')
                        iteminfo['note_ru'][j]=note
                        j+=1
            iteminfo['lore_en']=fullitem_en['language'][0].get('lore',None)
            iteminfo['lore_ru']=fullitem_ru['language'][0].get('lore',None)
            f.write("{0}\n".format(iteminfo))
            count+=1
            print(count)


'''
ABILITY DATA EXAMPLE
{'ags_en': None,
 'ags_ru': None,
 'attr_en': ['CAST RANGE: **900**',
             'WIDTH: **250**',
             'SILENCE DURATION: **3** / **4** / **5** / **6**',
             'KNOCKBACK DURATION: **0.6** / **0.7** / **0.8** / **0.9**',
             'KNOCKBACK MAX: **350**'],
 'attr_ru': ['ШИРИНА: **250**',
             'ДЛИТЕЛЬНОСТЬ: **3** / **4** / **5** / **6**',
             'ДАЛЬНОСТЬ ПРИМЕНЕНИЯ: **900**',
             'ПРОДОЛЖИТЕЛЬНОСТЬ ТОЛЧКА: **0.6** / **0.7** / **0.8** / **0.9**',
             'МАКС. ДАЛЬНОСТЬ ТОЛЧКА: **350**'],
 'cast_point': [0.25],
 'cast_range': [900],
 'cooldown': [16.0, 15.0, 14.0, 13.0],
 'desc_en': 'Releases a wave that silences and knocks back enemy units. '
            'Knockback distance is relative to how close they are to you.',
 'desc_ru': 'Выпускает волну, которая отбрасывает вражеских существ и '
            'запрещает им колдовать. Чем ближе враг к вам, тем дальше его '
            'отбросит.',
 'dmg_type_en': 'None',
 'dmg_type_ru': 'None',
 'hero': '<:drow:553950717283663928>Drow Ranger',
 'icon': '/panorama/images/spellicons/drow_ranger_wave_of_silence_png.png',
 'id': 5632,
 'lore_en': 'Traxex is rather fond of the tranquility of physical combat, '
            'calling on her Drow heritage to end the incantations of opposing '
            'magi.',
 'lore_ru': 'Траксекс предпочитает физический бой магическому, и, взывая к '
            'корням своей приёмной расы, запрещает использовать на поле боя '
            'любую магию.',
 'mana_cost': [90.0],
 'name': 'Gust',
 'note_en': [],
 'note_ru': [],
 'spell_imm_en': 'No',
 'spell_imm_ru': 'Нет'}
'''

def updateabils():
    with open('dotabase/abilities.txt', mode='w') as f:
        session = dotabase_session()
        count=0
        try:                    #запрос инфы о абилках
            r = requests.get(f"https://api.stratz.com/api/v1/Ability?LanguageId=0")
            absinfo_en=json.loads(r.text)
            r = requests.get(f"https://api.stratz.com/api/v1/Ability?LanguageId=19")
            absinfo_ru=json.loads(r.text)
        except Exception as e:                           
            raise
        with open('dotabase/heroes.txt', 'r', encoding='utf-8-sig') as t:
            heroes=t.readlines()
        for ab in session.query(Ability):
         en = absinfo_en.get(str(ab.id))
         if en['isTalent']==False and '_' not in ab.localized_name:
          for hero in heroes:
           herro=dict(eval(hero))
           if herro['abilities'].get(str(ab.name),None)!=None:
            ru = absinfo_ru.get(str(ab.id))
            abinfo={}
            abinfo['id']=ab.id
            abinfo['name']=ab.localized_name
            abinfo['code_name']=ab.name
            abinfo['hero']=f'<{herro["emoji"]}>{herro["name"]}'
            abinfo['icon']=ab.icon
            lang=en.get('language',None)
            if lang!=None:
                abinfo['desc_en']=en['language'][0].get('description',str(None))
                if abinfo['desc_en']:
                    abinfo['desc_ru']=ru['language'][0].get('description',str(None))
                    abinfo['desc_en']=re.sub(r'<(.+?)>','**',abinfo['desc_en'][0])
                    abinfo['desc_ru']=re.sub(r'<(.+?)>','**',abinfo['desc_ru'][0])
                    abinfo['desc_en']=abinfo['desc_en'].replace('é','e')
                    abinfo['desc_ru']=abinfo['desc_ru'].replace('é','е')
                    nums_en=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",str(abinfo['desc_en']))
                    nums_ru=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",str(abinfo['desc_ru']))
                    desc_en=abinfo['desc_en']
                    desc_ru=abinfo['desc_ru']
                    res=''
                    for num in nums_en:
                        t=desc_en[:desc_en.index(num)+len(num)]
                        t=t.replace(num,'**'+num+'**')
                        desc_en=desc_en[desc_en.index(num)+len(num):]
                        res+=t
                    abinfo['desc_en']=res+desc_en
                    res=''
                    for num in nums_ru:
                        t=desc_ru[:desc_ru.index(num)+len(num)]
                        t=t.replace(num,'**'+num+'**')
                        desc_ru=desc_ru[desc_ru.index(num)+len(num):]
                        res+=t
                    abinfo['desc_ru']=res+desc_ru
                abinfo['ags_en']=en['language'][0].get('aghanimDescription',None)
                abinfo['ags_ru']=ru['language'][0].get('aghanimDescription',None)
                if abinfo['ags_en']!=None:
                    nums_en=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",abinfo['ags_en'])
                    nums_ru=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",abinfo['ags_ru'])
                    ags_en=abinfo['ags_en']
                    ags_ru=abinfo['ags_ru']
                    res=''
                    for num in nums_en:
                        t=ags_en[:ags_en.index(num)+len(num)]
                        t=t.replace(num,'**'+num+'**')
                        ags_en=ags_en[ags_en.index(num)+len(num):]
                        res+=t
                    abinfo['ags_en']=res+ags_en
                    res=''
                    for num in nums_ru:
                        t=ags_ru[:ags_ru.index(num)+len(num)]
                        t=t.replace(num,'**'+num+'**')
                        ags_ru=ags_ru[ags_ru.index(num)+len(num):]
                        res+=t
                    abinfo['ags_ru']=res+ags_ru
                abinfo['attr_en']=en['language'][0].get('attributes',None)
                abinfo['attr_ru']=ru['language'][0].get('attributes',None)
                if abinfo['attr_en']!=None:
                    atrs=[]
                    for atr in abinfo['attr_en']:
                      ok=True
                      try:
                          if atr[0]=='%' or ':%' in atr:
                            ok=False
                      except:
                          ok=True
                      if ok:
                        atr=re.sub(r'<(.+?)>','**',atr)
                        nums_en=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",atr)
                        res=''
                        for num in nums_en:
                            t=atr[:atr.index(num)+len(num)]
                            t=t.replace(num,'**'+num+'**')
                            atr=atr[atr.index(num)+len(num):]
                            res+=t
                        atrs.append(res+atr)
                      else:
                          print(atr)
                    abinfo['attr_en']=atrs

                    atrs=[]
                    for atr in abinfo['attr_ru']:
                      ok=True
                      try:
                          if atr[0]=='%' or ':%' in atr:
                            ok=False
                      except:
                          ok==True
                      if ok:
                        atr=re.sub(r'<(.+?)>','**',atr)
                        nums_ru=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",atr)
                        res=''
                        for num in nums_ru:
                            t=atr[:atr.index(num)+len(num)]
                            t=t.replace(num,'**'+num+'**')
                            atr=atr[atr.index(num)+len(num):]
                            res+=t
                        atrs.append(res+atr)
                      else:
                          print(atr)
                    abinfo['attr_ru']=atrs
                abinfo['note_en']=en['language'][0].get('notes',None)
                abinfo['note_ru']=ru['language'][0].get('notes',None)
                if abinfo['note_en']!=None:
                    i=0
                    for note in abinfo['note_en']:
                        nums_en=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",note)
                        res=''
                        for num in nums_en:
                            t=note[:note.index(num)+len(num)]
                            t=t.replace(num,'**'+num+'**')
                            note=note[note.index(num)+len(num):]
                            res+=t
                        abinfo['note_en'][i]=res+note
                        i+=1
                    j=0
                    for note in abinfo['note_ru']:
                        nums_ru=re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",note)
                        res=''
                        for num in nums_ru:
                            t=note[:note.index(num)+len(num)]
                            t=t.replace(num,'**'+num+'**')
                            note=note[note.index(num)+len(num):]
                            res+=t
                        abinfo['note_ru'][j]=res+note
                        j+=1
                abinfo['lore_en']=str(en['language'][0].get('lore',None))
                abinfo['lore_ru']=str(ru['language'][0].get('lore',None))
                abinfo['lore_ru']=abinfo['lore_ru'].replace('é','е')  ##ерроры с кодировкой
                abinfo['desc_ru']=abinfo['desc_ru'].replace('ó','о')
                abinfo['lore_en']=abinfo['lore_en'].replace('é','e')
            stat=en.get('stat',None)
            if stat!=None:
                abinfo['cast_point']=removezero(en['stat'].get('castPoint',[]))
                abinfo['cast_range']=removezero(en['stat'].get('castRange',[]))
                abinfo['cooldown']=removezero(en['stat'].get('cooldown',[]))
                abinfo['mana_cost']=removezero(en['stat'].get('manaCost',[]))
                dmgtype={'pure':'Чистый','magical':'Магический','physical':'Физический'}
                abinfo['dmg_type_en']=str(ab.damage_type).title()
                abinfo['dmg_type_ru']=str(dmgtype.get(ab.damage_type,None)).title()
                spellimm={'yes':'Да','no':'Нет'}
                abinfo['spell_imm_en']=str(ab.spell_immunity).title()
                abinfo['spell_imm_ru']=str(spellimm.get(ab.spell_immunity,None)).title()
                disp={'en':{'yes':'Yes - __Basic__ dispel','no':'No','yes_strong':'Yes - __Strong__ dispel only'},'ru':{'yes':'Да - __Нормальным__ развеиванием','no':'Нет','yes_strong':'Да - Только __Сильным__ развеиванием'}}
                abinfo['dispel_en']=str(disp['en'].get(ab.dispellable,None))
                abinfo['dispel_ru']=str(disp['ru'].get(ab.dispellable,None))
            try:
                f.write("{0}\n".format(abinfo))
            except:
                print(abinfo)
            count+=1
            print(count)


'''
<:vision:591659960794873858>
<:turn_rate:591659960857788416>
<:str:591659961092669462>
<:move_speed:591659960753192960>
<:magic_resist:591659960249745460>
<:int:591659960551604234>
<:damage:591659959825989637>
<:attack_speed:591659960316723230>
<:attack_range:591659960027316224>
<:armor:591659959960469524>
<:agi:591659959905812500>
'''
## итемы ` ` , абилки __ __, герои ** **  <-- выделение 

#                 \n"+u"\u2022"+"       u"\u2800"


dota_mechanics = {'en':{'Attributes':{'Strength':{"__Strength__<:str:591659961092669462>":"For each point of strength<:str:591659961092669462>, a hero gains the following bonuses:\n"+u"\u2022"+"20 health\n"+u"\u2022"+"0.1 health regeneration\n"+u"\u2022"+"0.08% magic resistance\nAdditionally, strength heroes also get 1 attack damage per point."},
                                      'Agility':{"__Agility__<:agi:591659959905812500>":"For each point of agility<:agi:591659959905812500>, a hero gains the following bonuses:\n"+u"\u2022"+"0.16 armor\n"+u"\u2022"+"1 attack speed\n"+u"\u2022"+"0.05% movement speed\nAdditionally, agility heroes also get 1 attack damage per point."},
                                      'Intelligence':{"__Intelligence__<:int:591659960551604234>":"For each point of intelligence, a hero gains the following bonuses:\n"+u"\u2022"+"12 mana\n"+u"\u2022"+"0.05 mana regeneration\n"+u"\u2022"+"0.07% spell damage amplification\nAdditionally, intelligence heroes also get 1 attack damage per point of intelligence."},
                                      'Armor':{"__Armor__<:armor:591659959960469524>":"A stat that reduces (or increases, if negative) physical damage a unit takes from spells and attacks. Every unit is capable of gaining or losing armor, and most units start with a small amount of base armor, some even starting with negative armor. A hero's armor can be passively increased with agility (with agility heroes gaining more than other heroes), talents, certain items, and some abilities. Armor of any unit can also be temporarily increased or reduced with some abilities.\nEach point of agility<:agi:591659959905812500> increases a hero's armor by 0.16.","Base armor":"The part of the main armor that never changes throughout a game. It consists of one fixed value set for each unit individually. The base armor of a unit can be a negative number. Since only heroes have agility, the HUD of all non-hero units shows their base armor.","Main armor":"The armor value shown in white numbers near the shield icon in the HUD, consisting of base armor and the armor granted by a hero's agility. The only way to improve a hero's main armor is to increase its agility, which is gained by leveling up, acquiring certain items, or with the help of certain abilities.\nThe formula to calculate a hero's main armor is:\n`main armor = base armor + agility * 0.16`"},
                                      'Health':{"__Health / HP__":" A stat that represents the life force of a unit. When a unit's current health reaches 0, it dies. Every hero has a base health pool of 200. This value exists for all heroes and cannot be altered. This means that a hero's maximum health cannot drop below 200. Because each point of strength increases a hero's health by 20, a hero's health pool scales upwards with their strength points<:str:591659961092669462>. Similarly, because every hero has some measure of strength growth per level, all heroes gain more and more health as they continue to level up. A hero's base strength cannot drop below 1; however, it is possible to achieve 0 strength with the help of negative bonus strength.", "__HP Regen__":"The health regeneration value is visible on health bars in the HUD of every unit. Though the HUD shows only one decimal for health regeneration, it uses more decimals. The value in the HUD is rounded up."},
                                      'Mana':{"__Mana / MP__":"A stat that represents the magic power of a unit. It is used as a cost for the majority of active and even some passive abilities. Every hero has a base mana pool of 75, while most non-hero units only have a set mana pool if they have abilities which require mana, with a few exceptions. These values cannot be altered. This means that a hero's maximum mana cannot drop below 75. Because each point of intelligence increases a hero's mana by 12, a hero's mana pool scales upwards with their intelligence points<:int:591659960551604234>. Similarly, because every hero has some measure of intelligence growth per level, all heroes gain more and more mana as they continue to level up. A hero's base intelligence cannot drop below 1; however, it is possible to achieve 0 intelligence with the help of negative bonus intelligence.","MP Regen":"The mana regeneration value is visible on mana bars in the HUD of every unit. Though the HUD shows only one decimal for mana regeneration, it uses more decimals. The value in the HUD is rounded up. \n\nThe mana bar of all heroes can be seen in an over-head bar of the unit, though enemy heroes only show health bar"},
                                      'Magic resistance':{"__Magic resistance__<:magic_resist:591659960249745460>":"A stat that reduces (or increases, if negative) magical damage a unit takes from spells and attacks. Every unit is capable of gaining or losing magic resistance, and most units start with a small amount of base resistance. A hero's magic resistance can be passively increased with strength, talents, certain items, and some abilities. Magic resistance of any unit can also be temporarily increased or reduced with some abilities.\nEach point of strength increases a hero's magic resistance by 0.08.","Formula":"All sources of magic resistance stack multiplicatively. This means a unit's magic resistance value changes less the higher its magic resistance is, and more the lower it is. This prevents a unit from reaching 100% magic resistance by stacking different sources up.\n\n```Total magic resistance = 1 − ((1 − natural resistance) × (1 - strength × 0.08%) × (1 − first resistance bonus) × (1 − second resistance bonus) × (1 + first resistance reduction) × (1 + second resistance reduction))```\n\n```Actual damage = magical damage × (1 − natural resistance) × (1 - strength × 0.08%) × (1 − first resistance bonus) × (1 − second resistance bonus) × (1 + first resistance reduction) × (1 + second resistance reduction)```"},
                                      'Movement speed':{"__Movement speed / MS__<:move_speed:591659960753192960>":"The speed at which a unit can move over a second. The default movement speed caps are at 100 on the low end, and 550 on the high end, which can be bypassed by only a few abilities. Only units capable of moving can have a movement speed. This means granting a non-mobile unit movement speed with an ability does not allow them to move still. A unit's movement speed can be increased by abilities and by items. Some items grant passive speed bonuses to the wielder. Heroes also gain 0.05% movement speed for each point of agility<:agi:591659959905812500> they have.","Movement speed stacking":"Flat movement speed bonuses are simply added to the base movement speed of the unit, while percentage based bonuses get all summed up and then applied to the unit's total movement speed. However, most item-based speed bonuses have stacking restrictions. Passive movement speed bonuses from items are separated into groups. The movement speed bonuses of the items in their groups do not stack with each other or with multiple of themselves, but do stack with the bonuses from items from the other groups.\n"+u"\u2022"+"Group 1: Boots of Speed based items.\n"+u"\u2022"+"Group 2: Yasha based items.\n"+u"\u2022"+"Group 3: Wind Lace.\n"+u"\u2022"+"Drum of Endurance, Eul's Scepter of Divinity, Solar Crest, and Spirit Vessel are in no group, so they fully stack with each other, with multiple of themselves, and with all other item bonuses.\n"+u"\u2022"+"Ability-based bonuses have no such restrictions and stack with all other bonuses.","Formula":"```Movement Speed = (Base + Σ Flat Bonuses) × (1 + Σ Percentage Bonuses - Σ Slows)```"},
                                      'Status resistance':{"__Status resistance__ ":"An attribute of a hero that reduces the duration of most status debuffs and the slow values of slows. By default, every unit has a base status resistance of zero.","Formula":"All sources of status resistance stack diminishingly. This means a unit's status resistance value changes less, the higher its status resistance is, and more, the lower it is. However, this does not mean a reduction in effectiveness with multiple sources.\n```Total status resistance = 1 − ((1 − first resistance bonus) × (1 − second resistance bonus))```\n```Actual debuff duration = Debuff duration × (1 - Total status resistance)```"},
                                      'Turn rate':{"__Turn rate__<:turn_rate:591659960857788416>":"The speed at which a unit can turn. When moving to a location, a unit first turns to face that location, then begins walking. Similarly, when targeting another unit with an attack or spell, a unit first turns until it is facing the target, and then continues with the action.\n\nTurn rate is expressed in radians per 0.03 seconds. A 180 degrees turn is the same as π (3.14) radians.\n\n0.03π divided by the turn rate of the unit equals the time it takes to turn 180 degrees. A turn rate slow is directly applied to the base turn rate. For example, a turn rate slow of 70% on a unit's 0.5 base turn rate lowers the unit's actual turn rate to [0.5 × (1 - 0.7)] = 0.15.\n\n**Formula**\n\n`0.03π / T = t`, where T = turn rate and t = the time it takes to turn around."},
                                      'Vision':{"__Vision__<:vision:591659960794873858>":"A stat that describes what a unit can and cannot see from its current location and state. Places a unit cannot see are filled with the Fog of War, a dark mist that hides units inside of it. Invisible units cannot be seen even when outside of the Fog of War, unless they are spotted by a source of True Sight. Units cannot see through trees or to higher elevations - the only exceptions to this rule are flying units, who have unrestricted vision.\n\nAll units on your team share vision, which means that if a unit can see through the Fog of War, all allies can as well. This also applies to lane creeps, other controlled creeps, and buildings."}},
                        'Attack':{'Attack animation':{"__Attack immunity__":"A mechanic that makes the unit untargetable by basic attacks. An attack immune unit can neither be targeted, nor harmed or affected by already launched projectiles. Attacks which are mid-animation get canceled.\n\nInstant attacks may target attack immune units if they are ranged instant attacks, but will have no effect when the unit is still attack immune on impact. Instant melee attacks cannot target attack immune units."},
                                  'Attack damage':{"__Main attack damage__<:damage:591659959825989637>":"Main attack damage is the damage value shown in white numbers on a hero's statistics consisting of the base attack damage with the damage granted by a hero's primary attribute on top. A hero's main attack damage can only be increased by raising its primary attribute, or by very few specific abilities.\nBase attack damage is the part of the main attack damage that stays the same throughout a game. It consists of two values, a minimum and maximum amount. Every time an attack is issued, a random value between these two extremes is chosen to help decide the damage output.\n\nFormula\n```main attack damage = base attack damage + total primary attribute points + ability bonuses```","Damage amount modifiers":"**Bonus attack damage**\nBonus attack damage comprises the green number next to main attack damage. It comes in two types: Flat Bonus, Percentage Bonus\n\n**Critical strike multiplier**\nCritical Strike is an attack modifier that multiplies the total attack damage certain factor. If an attack activates more than one critical strike, only the highest multiplier is applied.\n\n**Blocked damage**\nDamage Block is a passive ability that gives the unit a chance to block a certain number of physical damage from an attack. If an attack activates more than one damage block ability, only the highest block value is applied.\n\n**Armor value multiplier**\nThe target's armor influences the attack damage by a factor that asymptotically lies between 0 and 2 and is 1 for a target that has no armor.\n`damage multiplier = 1 - ((0.052 × armor) ÷ (0.9 + 0.048 × |armor|)).`\n\n**General damage multipliers**\nA few abilities modify all incoming damage, including attack damage.","Formula":"```Damage = { [Main Attack Damage × (1 + Σ Percentage Bonuses) + Flat Bonuses] × Crit Multiplier - Blocked Damage } × Armor Multipliers × General Damage Multipliers```"},
                                  'Attack modifier':{u"\u2800"*20+"**__Attack modifiers__**":"*Modifiers which apply an effect to a unit's basic attacks. These effects can widely vary, from healing, to damaging or even disabling effects. Most of these modifiers have their own rules. For example, some modifiers may not stack with others, some may fully stack, some may be for melee units only and others for ranged or both. Attack modifiers can be active, in which case they require to be used manually, though most have an autocast option, but they also can be passive, proccing, or having a chance to proc on each attack.*",u"\u2022"+"Critical strike":"Critical strike causes the attacks to deal multiplied damage. Most critical strikes are chance-based, but not all.\nCritical Strikes fully stack with other attack modifiers. However, they do not fully stack with themselves. Multiple sources of critical strike have all their own proc chance. But if multiple of them proc on the same attack, only the one with the highest damage multiplier is applied. If they have the same multiplier, only one of them is applied still.",u"\u2022"+"Cleave and splash":"Cleave causes the unit's attack to deal damage in a trapezoid area in front of the attacking unit. The damage is based on the unit's attack damage values. Cleave can only be used by melee units, ranged units cannot cleave.\nCleaves fully stack with other attack modifiers. Multiple sources of cleave on the same unit work fully independently of each other. Each source applies its full damage within its area, without interacting with the other cleave sources.\n\nSplash causes the unit's attack to deal damage in a circular area around the attacked unit. Splash can only be used by ranged units, melee units cannot splash.\nSplash fully stacks with other attack modifiers. Multiple sources of splash on the same unit work fully independently of each other. Each source applies its full damage within its area, without interacting with other splash sources.",u"\u2022"+"Bash":"Bash causes the unit's attack to stun the target and in some cases to also deal additional damage. Most bash abilities are chance-based.\nBash fully stacks with other attack modifiers, except with other bashes. Multiple sources of bashes do not stack at all. The later acquired bash has absolutely no effect, only the first acquired bash works.",u"\u2022"+"Lifesteal":"Lifesteal causes the unit's attack to heal the attacking unit based on the damage dealt to the attack target.\nLifesteal fully stacks with other attack modifiers. Multiple sources of lifesteal stack additively with each other. Each source of lifesteal heals the attacking unit by its given value, and does not interfere with other lifesteal sources.",u"\u2022"+"Mana break":"Mana break causes the unit's attack to burn a portion of the target's mana and deal damage based on the amount of mana burned.\nMana Break fully stacks with other attack modifiers. Multiple sources of mana break stack additively with each other, with the only exception being <:am:553950525876338692>Anti-Mage's Mana Break, which does not stack with that from Diffusal Blade. In this case, the later acquired one works."},
                                  'Attack range':{"__Attack range__":"The range at which a hero may perform their basic attack on another unit. There are two main subdivisions of attacks: melee and ranged. Attack range can be extended by certain abilities.","Melee and ranged":"The attack range itself is not what decides if a unit is classified as ranged or melee. This characteristic is set for each unit individually, regardless of their actual attack range. This means that it is possible for a melee unit to have a higher attack range than a ranged unit. These are the differences between melee and ranged units:",u"\u2022"+"Melee heroes":u"\u2022"+" Attacks hit instantly upon reaching their attack point.\n"+u"\u2022"*2+" Melee heroes receive different (usually higher) values from certain items, such as Stout Shield or Quelling Blade.\n"+u"\u2022"*2+" Melee attacks miss if the target moves more than 350 range out of the hero's attack range, unless they have True Strike.\n"+u"\u2022"*2+" Melee heroes can attack up cliffs, provided the enemy is close enough to the edge to be within the hero's range.\n"+u"\u2022"*2+" Some abilities work exclusively for or against melee heroes.",u"\u2022"+"Ranged heroes":u"\u2022"+" Fire a projectile when they attack.\n"+u"\u2022"+" The time it takes for a ranged projectile to land is determined by the hero's projectile speed and their distance from the target.\n"+u"\u2022"+" Projectile attacks can be disjointed, and have a chance to miss when attacking a target on higher terrain.\n"+u"\u2022"+" Some abilities work exclusively for or against ranged heroes.\n"+u"\u2022"+" <:dk:553950717103177739>Dragon Knight, <:lonedruid:553951108259643402>Lone Druid, <:troll:553951535822798849>Troll Warlord, and <:terrorblade:553951283271303169>Terrorblade have abilities that allow them to switch between melee and ranged."},
                                  'Attack speed':{"__Attack speed__":"The frequency with which units attack is measured in attack speed. A unit's attack speed can be modified by items, agility, abilities, and auras.\n\nEvery unit has a base attack time (BAT), which refers to the default interval between attacks for an unbuffed unit with 0 agility and no attack speed bonus. For example, a melee lane creep has a BAT of 1.00 seconds, and thus attacks once every second by default. Similarly, if a hero with 1.7 BAT had 0 agility and no bonus attack speed, they would attack once every 1.70 seconds. While nearly every unit can have their attack speed modified, only a few heroes can actively change their BAT.","Attack speed representation":"The reciprocal of base attack time is base attack speed. For most heroes, this is 1 / 1.7 = 0.588 attacks per second. Attack speed is expressed in percent of base attack speed. The base is therefore expressed as 100. Each point of increased attack speed (IAS) adds 1 to that, giving 1% of base attack speed. Each point of agility increases IAS by 1. IAS is also modifiable by items, abilities, buffs, and debuffs. Attack speed works together with BAT to determine how often a unit can attack.\n\n`Attacks per second = [(100 + IAS) × 0.01] / BAT`\n`Attack time = BAT / [(100 + IAS) × 0.01] = 1 / (attacks per second)`","Example":"A lvl 1 <:axe:553950552493654066>Axe with no items has 1.7 BAT and 20 agility, which is converted to (0.20).\nAttacks per second = `[(100 + IAS) × 0.01] / BAT`\nAttacks per second = `[(100 + 20) × 0.01] / 1.7`\nAttacks per second = `1.2 / 1.7`\nAttacks per second = `~0.706`\n>> <:axe:553950552493654066>Axe attacks about `0.706` times per second.\n\nAttack time = `1 / 0.706`\nAttack time = `~1.417`\n>> <:axe:553950552493654066>Axe takes about `1.417` seconds between attacks."},
                                  'Damage types':{u"\u2800"*20+"**__Damage__**":"Damage is any means by which unit's current health can be reduced. Heroes, creeps, towers and fountains are all capable of dealing damage.","Damage types":"All forms of damage in Dota 2 are classified by damage types. There are 3 primary damage types: Physical, Magical, and Pure. Physical Damage can be reduced by Physical Armor or Damage Block, Magical Damage can be reduced by Magical Damage Resistance, while Pure Damage cannot be reduced by either armor or magical damage resistance.","Physical damage":"Physical damage can be inflicted by regular attacks from all units (including structures), and by certain abilities. Physical damage is modified by both armor and Damage Block, is unaffected by magic resistance, and cannot affect ethereal units. The abilities Guardian Angel and Cold Embrace make their targets completely immune to physical damage, although they can still be targeted by attacks and abilities.\n\nPhysical damage from abilities (and theoretically items) is usually unaffected by armor type, as they are not considered to be attacks. There are some exceptions to this. However, if a physical damage ability adds its damage directly to the hero's attack damage, then it is treated like hero attack damage and thus affected by armor types. The hero attack damage type deals 50% to structure armor type (used by all buildings and siege creeps), and 100% to all other types.","Magical Damage":"This type of damage is caused primarily by spells, although not all do magic damage. Magic damage is reduced by magic resistance, and deals higher damage against ethereal units. The majority of abilities in Dota 2 deal magical damage.","Pure Damage":"A damage type that is not reduced by magic resistance nor amplified by magical damage amplification like Veil of Discord or Ancient Seal. It also fully ignores armor and Damage Block. However, it can be reduced or amplified by skills which reduce/amplify every damage type, like Dispersion. Pure damage affects spell immune units (since spell immunity does not block damage by itself), but that does not mean that a spell with pure damage can target spell immune units (e.g. Laser deals pure damage, but cannot be cast on spell immune units). It does not affect invulnerable units."},
                                  'Projectile speed':{"__Projectile speed__":"The speed at which a units attack projectile travels. A projectile speed of 900 means the projectile travels 900 units per second. The base projectile speed is 900."}},
                        'Abilities':{'Abilities ':{"__Abilities__":"Unique skills that heroes and creeps have access to on the battlefield. They range from simple passive effects, to devastating explosions of energy, to complex, terrain changing feats. All heroes have four or more abilities, three or more basic abilities and an ultimate ability, that they can assign ability points to every time they level up. Every level in an ability makes it more powerful, sometimes increasing its mana cost as well.\nAbilities can consume mana, and may also be placed on cooldown when used. Abilities that are on cooldown cannot be used until their cooldown timer is up, at which point they can be cast again. Abilities with low cooldowns are sometimes referred to as 'spammable' abilities, because they can be used very frequently.\n\n There are three types of abilities in DOTA 2: Active, Passive and Autocast.","Active":"Active abilities must be used in order to apply their effects. Active abilities can consume mana, have cooldowns, and usually have some method of targeting related to them. The majority of abilities are active abilities. They can be activated by pressing their associated hotkey. If an ability can target the caster, double tapping the hotkey causes them to activate immediately on the caster.\nActive abilities are indicated by a bevel around the icon, which makes them look like a button. When an ability gets used and enters its cast animation, the bevel turns green and the icon shifts, looking like a pressed button. When selecting a targeted ability, the icon and the bevel appear brighter until the ability gets deselected or the cast begins. Active abilities also have a hotkey displayed at the top left corner.","Passive":"Passive abilities apply their effects either permanently as soon as they are learned, or activate by themselves if the ability is learned and its requirements met. These requirements can range from attacking a unit, casting a spell or even getting attacked. Most passive abilities do not consume mana and usually do not have cooldowns. Most heroes have at least one passive ability, though not all do.\nPassive abilities do not have a bevel and look like they are pressed into the hud. Since passive abilities cannot be used manually, their appearance never changes. Passive abilities only have an icon displayed upon learning.","Autocast abilities":"Special active abilities that can be toggled on or off, or manually cast. Most auto-castable spells are active attack modifiers, applying a modification to the user's attacks when activated. When an active attack modifier is manually cast, it is partially treated as a spell cast instead of as an attack. This causes nearby enemy creeps to not aggro when using them that way. This is also known as orb walking.\nNot all abilities with autocast are attack modifiers. A few of them are regular abilities, which, when toggled on, will automatically be cast when their requirements are met. An example of such is Bloodlust. When toggled on, <:ogre:553951283581681694>Ogre Magi will automatically cast Bloodlust on nearby allied heroes.\nThe autocast on Devour does not make <:doom:553950717245915136>Doom cast Devour automatically. Instead, the toggle state determines whether he will copy the target neutral creep's abilities or not. When toggled off, Doom does not acquire new neutral creep spells. When toggled on, he does."},
                                     'Aura':{"__Auras__":"Passive abilities that grant a buff or a debuff to units in an area of effect around the holder, or in some cases, over a short period at a targeted point or unit. By default, the buffs and debuffs linger on the affected units for 0.5 seconds after not being affected by the source any more, however, some auras have a different value. Generally, aura buffs and debuffs are not dispellable and multiple auras of the same kind do not stack, but there are various exceptions.\nMost auras cannot be controlled. They always affect units around the holder. Some auras can be toggled on or off. A few auras also have an extra active component, which ranges from temporarily boosting the aura to deciding whether it should affect surrounding heroes only or not. The active components or the toggle ability are treated like a regular spell, meaning they cannot be used or toggled while silenced or disabled. Beside these, there also are temporary auras, which are provided for a certain time period by casting a spell.","Unit affection":"There is no set rule for which units are generally affected by auras and which are not. It depends on the aura which units it affects and which it does not. If a unit does not meet the requirements for the aura, it is not affected. There are auras which affect only ranged units, or melee units, only heroes, or only non-heroes. As a rule of thumb, positive auras usually affect allied units (including the holder of the aura), while negative auras affect enemy units. There are a few exceptions.\n\nAuras usually also affect invisible units, and units in the Fog of War and are bestowed by them (which often allows to detect if an invisible enemy is nearby). However, almost all auras do not affect invulnerable or hidden units.\n\nIllusions can bestow most passive auras, but they usually do not benefit from them."},
                                     'Cast animation':{"__Cast animation__":"Every unit has unique cast animations for each of their spells. The cast animation of a spell is enacted as soon as a target for the spell is chosen, if it requires one, or its hotkey is pressed, if it does not require a target. These animations are not bound to specific spells, but rather to the ability slots of each unit and hero. The length of the animations varies for each spell as each of them is unique and made for the spell which is usually in the slot the animation is bound to. Although 'cast animation' only sounds like a visual part of the game, it does have a mechanical influence on the gameplay.\nEvery spell has a certain time frame the casting unit has to go through in order to successfully apply the effects of the spell. This time is commonly known as cast point. Cast point is set for each spell individually, and has nothing directly to do with the visual animation of the spells. However, since the animation starts playing immediately, it indicates the cast point of spells.","Interrupting a spell cast":"An ability only applies its effects, goes on cooldown and expends mana when the casting unit successfully reaches the cast point of the spell. This means when the unit gets interrupted by disables or their own actions before reaching the cast point of the spell, the cast gets canceled, the spell's effects do not get applied, it won't go into cooldown and won't draw mana. The player also can manually stop the spell cast by issuing a stop or halt command. When the spell cast gets interrupted during the cast time, the visual cast animation ends as well."},
                                     'Channeling':{"__Channeling__":"Channeling a spell causes the caster to stop acting for the duration of the spell. Channeled spells may be ended when the channeling unit takes another action or is interrupted by another spell. While spells are being channeled, a draining bar will appear on the screen, indicating how much time is left in the channel.","Interrupting channeled abilities":"There are certain abilities and items which do not interrupt channeling. For example you can use Blade Fury before or after using Teleportaion.\n\nThe only items that may be activated while channeling are Armlet of Mordiggian, Glimmer Cape, Mask of Madness, Observer and Sentry Wards (switching only), Phase Boots, Radiance, Ring of Basilius, Shadow Amulet, Shadow Blade, Shiva's Guard, and Silver Edge. Note that even though these items do not interrupt channelings upon cast, their effects after cast (like self-silence) may still interrupt the channeling. Activating any other item will interrupt channeling."},
                                     'Damage over time':{"__Damage over time__":"A condition that causes the affected unit to constantly take damage until the effect expires, is dispelled, or the target moves out of range. Damage is dealt at the end of each interval, the first of which begins when the spell lands. Some spells come with an initial damage, which may or may not be equal to the periodic damage.","Notes:":" **Initial Damage**: Many DoTs start immediately upon impact. The initial damage in this case is the same as damage per instance. Some DoTs have different initial damages. \n**Interval**: Time between instances in seconds. \n**Damage per Instance**: Damage of each tick after the initial damage. \n**Damage Duration**: Duration from start to the last instance of damage. In many cases this is shorter than effect duration, especially ones that start immediately. \n**Number of Intervals**: Generally equals `Damage Duration / Interval`. Does not include initial damage. \n**Max Total Damage**: Generally equals `Initial Damage + Damage per Instance × Number of Intervals`."},
                                     'Evasion':{"__Evasion__":"A mechanic that allows the unit to dodge an incoming attack. When evaded, the attack gets completely nullified. This means, anything that relies on attacks to hit their targets do not trigger, which includes most attack modifiers, and on-hit effects.\nA similar mechanic to evasion is blind. While evasion makes a unit evade incoming attacks from other units, blind makes a unit miss upon attacking other units. Just like evasion, when an attack misses to blindness, it gets completely nullified.","Stacking":"Multiple sources of evasion stack multiplicatively with each other, while sources of blind effects stack additively with each other and multiplicatively with evasion. The uphill miss chance stacks multiplicatively with evasion and blind. \nThe chances of all sources of evasion and blind are determined by pseudo-random distribution."}},
                        'Status effects':{'Attack immunity':{"__Attack immunity__":"A mechanic that makes the unit untargetable by basic attacks. An attack immune unit can neither be targeted, nor harmed or affected by already launched projectiles. Attacks which are mid-animation get canceled.\n\nInstant attacks may target attack immune units if they are ranged instant attacks, but will have no effect when the unit is still attack immune on impact. Instant melee attacks cannot target attack immune units."},
                                          'Disable':{u"\u2800"*20+"**__Disables__**":"*Any abilities or status effects that prevent, impede, or otherwise inhibit a Hero from acting. Disables come in many different varieties, and most Heroes have access to some form of disable. Sometimes 'disabled' or 'fully disabled' refer to stun.*","Stun":"Stuns are the most common and most dependable kind of disable. A Hero under the effect of a stun is unable to move, attack, use items, or use abilities until it wears off. Stuns will also interrupt any channeling abilities, such as using a Town Portal Scroll. Mini-stuns are a shorter version of a regular stun, usually lasting a fraction of a second, that are most useful in interrupting enemy spells or preventing enemies from moving effectively. General stuns have distinctive animation on the head of stunned heroes.","Shackle":"Shackle abilities, much like regular stuns, fully disable the target, rendering them unable to move, attack, use abilities or items and interrupt channeling spells. The difference to regular stuns is that the caster has to channel the effect, or apply other negative effects to it (e.g. slowing the caster).","Sleep":"A sleep works just like a stun, with the only difference being that the effect gets dispelled once the affected units is damaged or attacked. Sleeps also may turn the affected unit invulnerable for a while.","Cyclone":"A cyclone also works just like a stun, but on top of fully disabling the target, it also whirls it up into the air, so that other units can pass below it, and turns it invulnerable for the duration.","Slow":"A slow reduces the affected unit's movement speed or attack speed (or both).","Silence":"A silence prevents the affected unit from casting their spells for its duration. Toggled spells are stuck in their current state for the duration, but continue to function if enabled. It does not affect anything else, the affected unit is still free to move, attack and use items. Passive abilities are not disabled.","Mute":"A mute works just like a regular silence, except that it disables active items instead of the unit's spells. Mutes usually come together with a regular silence.","Break":"A Break disables the affected hero's passive abililties. Most passives are disabled, but not all. Generally, on-death passives (Reincarnation, Requiem of Souls passive activation) are not disabled. It also tends to not disable passive abilities which have a direct synergy with the hero's other abilities, like Grow which affects Toss' damage. Break does not disable any passive item abilities either.","Forced Movement":"Some spells forcefully move the affected units, preventing it from freely moving. Some of these also fully disable it for the duration, but some allow the unit to still turn, attack or cast spells and items.","Root":"A root (formerly known as Ensnare) is a form of disable which prevents a unit from moving and disables certain mobility-based abilities (e.g. Town Portal Scroll,  Teleportation, and blink from Blink Dagger, <:am:553950525876338692>Anti-Mage and <:qp:553951283481018378>Queen of Pain), however, it does not prevent the affected units from turning, casting other spells or using most items. Some roots also disarm the affected units (disarming roots were formerly known as Entangle).","Leash":"A Leash is a form of disable that restricts (but does not prevent) movement in some way while also disabling certain mobility-based abilities (similar to Root). Like Root, Leash does not prevent the affected units from turning, casting other spells or using most items.","Hex":"Hex turns the target Hero or unit into a critter, a weak unit that is incapable of attacking or using abilities and items. Hex silences, mutes, disarms and sets the target's base movement speed to a certain value, usually low value. It does not affect any other aspect of the unit (like turn rate, vision, collision size, etc), nor does it prevent it from gaining experience and gold.","Taunt":"A taunt forces the target to attack another unit. The target is unable to issue any other commands until the taunt wears off. The forced attacks caused by taunts will interrupt any ongoing order the affected unit has, including channeling spells. If the taunting unit cannot be attacked or the taunted unit cannot attack, the taunted unit will follow the taunting unit until attacks are possible again or the taunt wears off.\nSources of taunts are Berserker's Call, Duel, and Winter's Curse.","Fear":"Fear forces the target to run away from the cast point. The target is unable to issue any other commands until the fear wears off.","Hide":"Hiding (also referred as banishing) a unit causes it to temporarily disappear. While hidden, a unit cannot be affected by any spell (with a very few exceptions) and is fully disabled. It is unable to move, attack, cast spells or items. Usually hiding spells also turn the affected unit invulnerable.","Ethereal":"Ethereal is a status effect which prevents a unit from attacking, but also prevents it from getting attacked. It turns the unit immune to physical damage, but usually reduces magic resistance, making it take more magical damage. Ethereal effects apply a slow when targeted to enemies.","Disarm":"A disarm prevents the affected unit from attacking. It still can be attacked by other units.","Blind":"A blind causes a unit to gain a chance to miss on attacks. Blinds work fully independently from evasion."},
                                          'Invisibility':{"__Invisibility__":"A status effect which makes units and heroes not appear on their opponent's screen or minimap, and makes them unable to be targeted directly by the enemy. Invisibility makes the unit's model appear transparent, but clearly visible still for allies. If it is an allied hero, its dot on the minimap also turns into a ring for the duration.","Unit behavior during invisibility":u"\u2022"+" While invisible, a unit never automatically attacks any nearby enemy, not even when it is revealed by True Sight and being attacked. However, when issuing an attack ground order, the invisible unit attacks.\n"+u"\u2022"+" Generally, the invisibility is lost upon reaching the attack point.\n"+u"\u2022"+" Invisibility may or may not apply a phase effect on the unit.\n"+u"\u2022"+" The invisibility is lost upon reaching the cast point of the spell. This means that spells with extended effects like Eclipse or Epicenter do not cancel the invisibility upon each beam or pulse.\n"+u"\u2022"+" Channeling spells do not cancel it either when going invisible after the channeling started.\n"+u"\u2022"+" All ranged attacks and most projectiles of abilities are disjointed by invisibility.\n"+u"\u2022"+" It is enough for a unit to turn fully invisible even just for a split second as a disjointable projectile flies to fully disjoint it.\n"+u"\u2022"+" Invisible units are still affected by spells which affect an area."},
                                          'Spell immunity':{"__Spell immunity__":"A modifier which prevents most spells to target the affected unit. This includes single-targeted spells, area spells, passive and active abilities.","Mechanics":"Spell immunity is a status effect (also known as modifier). Most spells in the game first check whether or not the unit has the spell immunity modifier on. If the modifier is present, single target spells cannot target the unit at all, while area of effect spells ignore the unit and already ongoing effects may stop affecting it. However, some spells (and most ultimates) pierce spell immunity and can fully target and affect spell immune units.",u"\u2800":"Usually, a spell either fully pierces spell immunity, or it is fully blocked. However, there are a few exceptions to this rule. Whether or not a spell pierces spell immunity is noted down in the description boxes of each ability, right below the ability name.\n\nWhen a unit turns spell immune while a projectile from an ability is already flying towards it, the projectile has no effect upon impact if the spell it originates from does not pierce spell immunity. The same applies to most, but not all delayed effects.\n\nSpell immunity does not prevent regular attacks of any units. However, some attack modifiers do get blocked, but not all of them. Generally, all critical strikes, cleaves and most bashes pierce spell immunity.\n\nMost sources of spell immunity also dispel the target upon getting applied, removing all buffs or debuffs a basic dispel can remove"}},
                        'World':{'Experience':{"__Experience__":"An element heroes can gather by killing enemy units, or being present as enemy units get killed. On its own, experience does nothing, but when accumulated, it increases the hero's level, so that they grow more powerful. Only heroes can gather experience and therefore reach higher levels. With each level gained, a hero's base attributes increase by static values (unique for each hero).","Acquiring experience":"Experience is awarded in a 1500 radius when an enemy hero dies to any ally, or when an enemy non-hero (creep or summon) dies to any ally or any neutral creep. This experience is shared between all allied heroes within the area, splitting it evenly amongst them. Therefore, the more heroes there are, the less every individual hero gets, and if no hero is nearby, the experience is effectively lost or wasted. Additionally, heroes that are already level 25 still take their share of experience within range, also effectively wasting exp.\n\n**Formula**\n `(40 + 0.14 * DyingHeroXP ) / № of killers`\n\n Additionally, killing an enemy hero with a killing streak(>2) awards the killer with extra exp which equals `200 * ( killing streak - 1 )`. Note that the highest streak is 10, even if the hero actually had more kills."},
                                 'Gold':{u"\u2800"*24+"**__Gold__**":"The currency used to buy items or instantly revive your hero. Gold can be earned from killing heroes, creeps, or buildings.","A player's gold is split into two categories:":u"\u2022"+" **Reliable gold** - Any bounty you get from hero kills, Roshan, couriers, Hand of Midas, Track gold and global gold from towers is added to your reliable gold pool.\n"+u"\u2022"+" **Unreliable gold** - Everything else (starting gold, periodic gold, creep kills, neutrals, etc).\n\nThe only other difference between the two is how each one is spent:\n"+u"\u2022"+"Dying only takes away gold from your unreliable gold pool.\n"+u"\u2022"+"Buying items uses up your unreliable gold first before using your reliable gold.\n"+u"\u2022"+"Buyback uses reliable gold first.\n"+"Hovering your mouse over the amount of total gold shown in the HUD shows your reliable and unreliable gold totals.\n\n*The purpose of separating gold into these two categories is to encourage ganking and tower pushes, which give reliable gold, rather than passive farming, which grants unreliable gold.*","Periodic gold":"Each player receives 1 unreliable gold every 0.66 seconds (starting from 0:00 on the game clock), which results in 91 gold every minute. Some heroes may pick talents that increase that base rate.","<a:Emoticon_bountyrune:594813355303239700>Bounty Rune<a:Emoticon_bountyrune:594813355303239700>":"Activating a <a:Emoticon_bountyrune:594813355303239700>**Bounty Rune**<a:Emoticon_bountyrune:594813355303239700> grants the player and their team unreliable gold depending on the length of the game, starting at 40 gold, and growing by 2 gold per minute, increasing in 30 second intervals.","Hero kills":"Hero kills grant reliable gold to the killer. Bonus gold is awarded for stopping kill streaks. The first hero that is killed in a match gives a bonus 150 reliable gold to the killer; this is called 'First Blood'.\n\nWhen a hero dies to enemy creeps or an enemy tower and has not been damaged by any enemy heroes in the last 30 seconds (regardless of distance between heroes), the kill gold is split among all enemy heroes. When a hero dies to enemy creeps or an enemy tower and is assisted by only one enemy, that enemy is credited with the kill. When there are multiple enemies within 1300 range, the gold is split equally amongst all heroes that assisted.\n\nEvery time a hero kills an enemy hero, the killer is awarded reliable gold using the following formula: \n`110 + streak value + (killed hero level × 8)`\nThe streak value equals to `60 × (№ of kills - 2)` gold"},
                                 'Glyph of Fortification':{"__The Glyph of Fortification__":"An ability usable by any player that causes all friendly buildings and lane creeps to become impervious to damage for 6 seconds, while also granting tier 2 and higher towers a multishot attack, allowing them to attack multiple enemies at the same time. The effect has a cooldown of 300 seconds, making the timing of usage very important. The Glyph is used strategically to stop enemy pushes or slow them down long enough to organize a defense. It may also be used offensively to secure a push by granting the creep waves damage immunity at the right time, or even for finishing enemies off by using the multishot attacks.\n\nThe Glyph of Fortification can be activated by any player with a button at the right of the minimap or the shortcut they defined in the settings. The Glyph's cooldown is shared by the entire team, meaning if one player uses it, it goes on cooldown for all players of the team. However, whenever a tier 1 tower falls, the Glyph's cooldown gets refreshed 1 second later."},
                                 'Lines':{"__Lanes__":"Paths connecting the two Ancients. Lane creeps will push along these lanes after spawning.\n\nThere are three lanes:\n"+u"\u2022"+" **Top** line, which runs along the left and top edges of the map\n"+u"\u2022"+" **Middle** or **mid** line, where the lane creeps clash in the river\n"+u"\u2022"+" **Bottom** or **bot**, which runs along the bottom and right edges of the map\n\nThe lanes are also known by other names according to their function during the early game:",u"\u2800":u"\u2022"+" The **safe** / **easy** / **short** lane is the lane where the Tier 1 Tower is closest to the creep line. For Radiant, this is the bottom lane. For Dire, this is the top lane. The lane is named as such since it is easiest for a laning hero to retreat to the protection of their tower. Also, because this lane is close to the jungle, it is the easiest lane to use creep pulling to control the location of the creep line.\n"+u"\u2022"+" The **hard** / **off** / **long** lane  is the lane where the Tier 1 Tower is farthest from the creep line. For Radiant, this is the top lane. For Dire, this is the bottom lane."},   
                                 'Runes':{u"\u2800"*24+"**__Runes__**":"*There are two types of Runes:*","Bounty runes":"Spawn at 0:00 on the game clock, and every five minutes after that.\n\n<a:Emoticon_bountyrune:594813355303239700>**Bounty rune**: Grants 40 + 2 per minute gold to every player of the team that picks them up.","Power-up Runes":"Power-up Runes spawn at 2:00 on the game clock, and every two minutes after that at one of the two locations in the river until the 40 minute mark, after which they spawn simultaneously at both locations.",u"\u2800":u"\u2022"+"  <a:Emoticon_doubledamage:594813356964052993>**Double damage**: Increases base damage by 100% for 45 seconds\n"+u"\u2022"+" <a:Emoticon_illusion:594813357412843531>**Illusion**: Conjures 2 illusions of your hero which deal 35% damage. Melee illusions take 200% damage. Ranged illusions take 300% damage. Illusions last 75 seconds\n"+u"\u2022"+" <a:Emoticon_haste:594813358432190464>**Haste**: Increases movement speed to maximum and grants slow immunity for 22 seconds\n"+u"\u2022"+" <a:Emoticon_invisbility:594813359174713344>**Invisibility**: Becomes invisible for 45 seconds. This invisibility is broken by attacking or by using an ability or item\n"+u"\u2022"+" <a:Emoticon_regeneration:594813360264970260>**Regeneration**: Regenerates health and mana to maximum within 30 seconds**\n"+u"\u2022"+" <a:Emoticon_arcane:594823389001023501>**Arcane**: Reduces cooldowns and mana costs by 30% for 50 seconds**\n\n*Runes can be destroyed by normal attacks, using a forced attack command.\n Runes can be hooked using Meat Hook*"},
                                 'Jungle':{"__The Jungle__":"The forested area between lanes. This is where neutral creeps can be found, which can be killed for gold and experience. It is possible to level up by killing creeps in the jungle instead of in the lanes, though neutral creeps give less gold and exp than lane creeps. This practice is called Jungling."}},
                        'Gameplay':{'Denying':{u"\u2800"*20+"__Denying__":"The act of preventing enemy heroes from getting the last hit on a friendly unit by last hitting the unit oneself. Enemies earn reduced experience if the denied unit is not controlled by a player, and no experience if it is a player controlled unit. Enemies gain no gold from any denied unit. All allied units can be denied once they fall below a certain percentage of health: creeps, and non-hero units at 50%, heroes at 25%, and towers at 10%.\n\nBesides couriers, every non-hero unit can be denied, including creep-heroes. They can be denied once their health falls below 50%. Denying an allied, non-player-controlled unit (lane creeps which are not taken over by players) grants 40% of its experience bounty to enemies within the 1500 experience range, instead of 100%. The denying player also gains 20% of the creep's gold bounty when denying. Denying a player-controlled unit grants 0% experience to the enemy, and also none to the denying team.","Denying during laning stage":"Especially in the laning phase, denying allied lane creeps is important to create a gold and experience advantage. It can lead to having a level advantage over the enemy, opening up a chance to get a kill on them. Gold-wise, it cripples the enemy's farming, slowing them down significantly, if they depend on farming gold. Creeps should be denied whenever possible, although getting last hits should be prioritised. Denying creeps is also important to shift the creep equilibrium towards closer to the own tower and away from the enemy tower.","Denying heroes":"Heroes can also be denied under specific circumstances. A denied hero prevents the enemy from gaining any experience or gold from the kill, but still loses gold upon death.\nA hero under 25% health and under the effects of certain spells can be denied by an allied hero. The spells that allow denying allied heroes are: \n"+u"\u2022"+" <:doom:553950717245915136>Doom's Doom \n"+u"\u2022"+" <:qp:553951283481018378>Queen of Pain's Shadow Strike \n"+u"\u2022"+" <:venomancer:553951535474933782>Venomancer's Venomous Gale\nDuring Supernova, <:phoenix:553951283497664527>Phoenix may be denied in a similar fashion if the sun is below 50% health.","Denying oneself":"It is possible to deny oneself (commit suicide) in a variety of ways:\n"+u"\u2022"+" <a:miner:563374310572425225>Techies' Blast Off!\n"+u"\u2022"+" <:pudge:553951284454227968>Pudge's  Rot\n"+u"\u2022"+" <:alchemist:553950517324152863>Alchemist's  Unstable Concoction\n"+u"\u2022"+" <:abaddon:553950496516341783>Abaddon's  Mist Coil\n"+u"\u2022"+" <:pugna:553951283158056962>Pugna's  Life Drain cast on an ally\n"+u"\u2022"+" Neutrals (including Roshan) can deny you, which is useful if you are being chased with low HP and it's unlikely that you will escape","Denying allies":"It is also possible to deny allied heroes with some abilities:\n"+u"\u2022"+" <:centaur:553950671464955945>Centaur Warrunner's  Retaliate fully works against allied attacks, resulting in a deny when its damage kills an ally.\n"+u"\u2022"+" <:chen:553950671280406528>Chen's  Holy Persuasion, <:encha:553950883595943947>Enchantress'  Enchant, <:lifestealer:553950961169596417>Lifestealer's  Control and Helm of the Dominator's Dominate can be used on an enemy ranged unit that has a projectile attack in flight, and results in the denial of an allied hero if the attack deals the finishing blow.\n"+u"\u2022"+" <:venga:553951535789244432>Vengeance Spirit's illusion created by Vengeance Aura can deny allies\n"+u"\u2022"+" <:oracle:553951283262914591>Oracle's  False Promise, if cast on an ally under the effect of an enemy <:ww:553951535831318558>Winter Wyvern's  Winter's Curse that takes enough damage to die from allied heroes will be denied, rather than having the kill granted to Wyvern."},
                                    'Disjoint':{"Disjointing":"The act of dodging projectiles, or rather, to cause a projectile to fully lose track of its target. A disjoint is recognized when a projectile stops tracking a moving unit. Causing a projectile to run out (expire) before hitting the target does not count as disjointing in that sense, but rather avoiding the projectile by 'outrunning' it.\n\nDisjointing itself is not granted explicitly by any effects or spells, it is instead granted as a secondary effect to other abilities.\n\nThe most common forms of disjointing are blinking and becoming invisible. Although invulnerability and hiding causes projectiles to not affect the target, they do not disjoint, since the projectile still homes and technically hits the target. Not all projectiles can be disjointed, and not all types of repositioning abilities can disjoint."},
                                    'Dispel':{"Dispel":"The term used for a forced removal of status effects. Dispels usually come together with other mechanics and are rarely seen as a primary mechanic of a spell or item.","Mechanics":"Dispels remove status effects based on whether the casting unit is an ally or an enemy, and whether the status effect is positive or negative. Applying a dispel on an allied unit only removes negative effects (also known as debuffs). Positive effects (known as buffs) are never removed. Vice versa, applying a dispel on an enemy unit only removes buffs, debuffs are not removed.\n\nThere are 3 different variations of dispel: **basic dispel**, **strong dispel**, and **death**.\n"+u"\u2022"+" **Basic dispels** are able to remove most basic stats altering effects like speed or damage bonuses or slows and silences. However, they are unable to remove most hard disables like stuns or Forced Movement.",u"\u2800":"Spell immunity may also apply a basic dispel, although not all of them do. Their dispel does not differ from that of basic dispels, in fact, they use the exact same mechanic. However, some abilities periodically check for spell immunity and get their effect removed if such is detected. Spells and effects which periodically check for spell immunity are Ghost Form, Deafening Blast's disarm, Ghost Walk's slow, Ghost Shroud, and Pounce.\n\n"+u"\u2022"+" **Strong dispels** are capable of removing everything a basic dispel and spell immunity can remove. On top of that, these can also remove many more status effects, including hard disables. Whether or not strong dispels can remove positive effects is unknown, since there is no source of strong dispel which can be applied on enemy units.\n\n"+u"\u2022"+" **Death** applies the ultimate dispel on units. It removes almost everything. Only a few effects are not dispelled by death."},
                                    'Ganking':{"__Ganking__":"The act of actively moving around the map in order to kill an enemy hero.","The advantages of ganking":"Ganking is used to gain an overall experience and gold advantage. Successful ganks can significantly slow down an enemy carry's farm, help a teammate recover a difficult lane, and provide a time window to push down a tower or to kill Roshan. To gain an early advantage, active ganking and pushing are essentially mandatory. Additionally, ganking is often the easiest way to kill heroes when the other team has a large advantage in the late game.\n\nGanking also serves as a counter to enemies trying to push because they must move deep into your territory, where they are often isolated and have little vision. After the enemy pushers are ganked, your team can execute a counterpush to negate the advantage the other team was trying to gain."},
                                    'Harassment':{u"\u2800"*20+"__Harassment__":"Harassment is the process of damaging enemy heroes during the laning phase to keep them from farming, to gain lane dominance or to drop their health to prepare for a kill.\nStrong harassment can force the enemy to play extremely defensive, spend a lot of gold on consumables, repeatedly return to their base, and miss out on experience and last hits.","Ways of harassing":"The most basic form of harassment is simply damaging the enemy hero with physical attacks. This is most easily accomplished if your hero is a ranged one (with a greater range allowing for a greater degree of harassment) while the enemy hero or heroes are melee or have low range. Directly attacking an enemy hero will draw creep aggro, which means that nearby enemy creeps will attack you. \n\nWhen manually used, castable attack modifiers like <:viper:553951535852290048>Viper's  Poison Attack or <:huskar:553950961195024434>Huskar's  Burning Spear will not draw creep aggro at all, making them extremely powerful harassment tools.",u"\u2800":"Most damaging spells can be used for harassment purposes, and are especially effective because they do not draw creep aggro. Especially suited are slowing abilities like <:cm:553950671427076125>Crystal Maiden's Crystal Nova because they allow the user to perform some additional physical attacks on a retreating enemy, as well as spammable abilities with a low mana cost such as <:cloclwerk:553950671100051487>Clockwerk's Rocket Flare. Experienced players usually integrate this technique into their farming: A well-placed AoE ability can get a last hit on a creep while simultaneously damaging an opponent.\n\nItems that provide some early mana regeneration (e.g. Soul Ring, Clarity Potions or Arcane Boots) can greatly increase the harassment potential of a hero. Although ranged heroes are generally better suited for physical harassment, an Orb of Venom can allow some melee heroes like <:riki:553951283644727306>Riki to harass effectively.","Countering harassment":"Physical harassment should be countered with items that provide damage block, health regeneration or armor: Stout Shield, combined with a Ring of Health can render a hero almost immune to regular harassment.\n\nHarassment with Spells can be mitigated with a Magic Wand, as they will constantly gain charges and provide the holder with a steady supply of mana and health.\n\nSome abilities are excellent counter-harassment tools. If a player faces heavy harassment, they might consider adapting to a defensive skillbuild, (e.g. investing as many ability points as possible into Dragon Blood or Blur).\n\nRemember that trees block non-flying vision. In the laning stage it can be a good strategy to hide in them and move out only to make a last hit, and then retreat, and repeat.\n\nIn some laning situations, it is better to force a small skirmish and attempt to kill an enemy hero instead of just passively allowing the enemy to gain lane dominance through constant harassment."},
                                    'Item sharing':{"Item sharing":"Most items in Dota 2 cannot be shared with other heroes. The hero who bought an item is considered its owner, and only they can use, sell, or upgrade it.\n\nHowever, most consumables are completely shareable as they cannot be upgraded, and only grant temporary effects. These can be used also by heroes that do not own them. This allows support heroes to purchase items to share with their team.\n\nBottle is not muted when you share it with your allies"},
                                    'Creep stacking and pulling':{"Creep Stacking":"Creep Stacking is a process in which a Hero draws Neutral Creeps away from their camp so that they leave the area before a new wave of Creeps respawns. This allows players to significantly increase the number of Creeps in a particular Camp, allowing them to earn more Gold and Experience from a single Camp, or increasing the effectiveness of Creep Pulling. Stacking also grants the stacker 35% of the bounty if the Creep camp is cleared by allies. Creep Camps can be Stacked indefinitely, allowing there to be massive amounts of Creeps at one time.","Creep Pulling":"Creep Pulling allows a Hero to 'pull' a group of Neutral Creeps into their lane, causing them to attack their lane creeps. This is executed by getting the attention of a Creep Camp nearest to the lane and timing it with the spawns of the lane creeps. Pulling allows Heroes to avoid damage from Neutral Creeps and bring their abilities off Cooldown, while also denying friendly Creeps and preventing the enemy from earning Experience."},
                                    'Random distribution':{"Random destribution":"The **uniform** or **true random distribution** describes the probability of random event that underlies no manipulation of the chance depending on earlier outcomes. This means that every 'roll' operates independently.\n\nThe **pseudo-random distribution** (often shortened to PRD) in Dota 2 refers to a statistical mechanic of how certain probability-based items and abilities work. In this implementation the event's chance increases every time it does not occur, but is lower in the first place as compensation. This results in the effects occurring more consistently.","How PDR works":"For each instance which could trigger the effect but does not, the PRD augments the probability of the effect happening for the next instance by a constant C. This constant, which is also the initial probability, is lower than the listed probability of the effect it is shadowing. Once the effect occurs, the counter is reset.","<a:note:595915864231116801>Note":"Effects based on PRD rarely proc many times in a row, or go a long time without happening. This makes the game less luck based and adds a great deal of consistency to many probability-based abilities in Dota 2. Gameplay wise, PRD is difficult to exploit. It is theoretically possible to increase your chance to bash or critical strike on the next attack by attacking creeps several times without the effect happening, but in practice this is nearly impossible to do. Note that for instances that would not trigger the effect, the probability counter does not increase. So a hero with critical strike attacking buildings does not increase its chance to critical strike on its next attack, since critical strike does not work against buildings.", "True random events":"Some mechanics roll a random value between 0 and 1 and scale it along the minimum / maximum gradient. This includes attack damage, last hit bounty, certain abilities, like <:ck:553950671699705856>Chaos Knight's Phantasm and Chaos Bolt, <:ogre:553951283581681694>Ogre Magi's Multicast and others. Also all blinding skills use True random distribution"}},
                        'Units':{'Buildings':{"__Buildings__":"A type unit that are not controlled by any player. At the beginning of each match, a set of buildings spawn at set locations for both teams. Both factions have the same set of buildings, with only their appearance differing from each other. Buildings take mostly defensive roles and are the main objective of the game.\n\nAll buildings have the same base properties. They are immune to most spells (with only a few spells affecting them), have the structure armor type, deal siege damage if they can attack and are immobile. When destroyed, some buildings grant gold to the entire enemy team, while others grant gold only to whoever made the last hit. Once below 10% health, buildings (except for the Ancients) can be denied to prevent the enemy from getting their gold bounties, or to reduce the amount they get. Buildings do not grant experience. Once destroyed, a building is permanently lost, as they do not respawn.\n\nThere are a total of 29 buildings on each side.","Towers":"The main line of defense for both teams, attacking any non-neutral enemy that gets within their range. Both factions have all three lanes guarded by three towers each. Additionally, each faction's Ancient have two towers as well, resulting in a total of 11 towers per faction. \n\nTier 1 towers are invulnerable during the preparation phase, until the battle begins. Each Tier 2 and tier 3 tower is invulnerable until the lower tier tower preceding it in its lane is destroyed. The two tier 4 towers are invulnerable until any of the tier 3 towers have been destroyed. Barracks do not have to be destroyed to make tier 4 towers vulnerable. Both of the tier 4 towers must be destroyed in order to remove the Ancient's invulnerability. If you are attacked by an enemy tower you can switch its target by pressing on an ally","Barracks":"Buildings, defended by their tier 3 towers, that are responsible for keeping lane creeps as powerful as their counterparts. There are two Barracks for each lane per faction - one for melee creeps (called Melee Barracks or Melee Rax), and one for ranged creeps (called Ranged Barracks or Ranged Rax). The ranged barracks are always located to the left of the melee barracks on each lane and both factions.\n\nBarracks are invulnerable until the tier 3 tower guarding them is destroyed. The loss of barracks does not stop lane creeps from spawning. However, destroying Barracks grants the destroying team super creeps in that lane, corresponding to which one was destroyed, which are more powerful and grant less bounties than regular creeps. When all 6 Barracks of a team are destroyed, mega creeps start spawning on every lane for the enemy, even more powerful than super creeps.\n\n*Melee barracks have 5 HP regen, so you should be careful when choosing which barrack to push.","Backdoor protection":"A passive ability almost all buildings have. Tier 1 towers, Shrines and Fountains are the only buildings without this ability. While active, Backdoor Protection grants high damage resistance to the building, and causes it to heal back any damage it takes from enemy units, making them difficult to destroy. This protection deactivates when an enemy lane creep moves within range of the building (if it is a tower outside the base), or gets close to the team's base (if it is a building within the base). The creep must not be dominated by a player, only AI-controlled lane creeps can deactivate the protection. Once deactivated, it takes some time for the protection to activate again."},
                                 'Couriers':{"__Courier__":"A unit that transports items from the shops to the heroes. An Animal Courier can be recruited for a team by purchasing it at the base shop. It upgrades automatically at 3:00 minutes of the game to a Flying Courier. There is only one courier for the whole team. Each player can assign orders to courier that will cancel the current action unless shift-queued.","Inventory":"Like a hero, the courier possesses 6 inventory slots and 3 backpack slots. However, it has restrictions. Almost every item gets muted when in the courier's inventory, rendering all their stats and abilities disabled and unusable for the courier. Muted items are darkened out in its inventory\n\n**However**, only a few of them can be actually used by the Courier.\n"+u"\u2022"+" The courier can use Tango (Shared), Cheese and Refresher Shard.\n"+u"\u2022"+" The courier is not able to place or share Observer Wards and Sentry Wards.\n"+u"\u2022"+" It also can activate Dust of Appearance and Smoke of Deceit, but the latter does not affect the courier.\n"+u"\u2022"+" It is possible to buy a Divine Rapier with the Flying Courier and it can drop the Rapier. However, it cannot pick it back up again, as it cannot pick up Rapiers in general. It cannot pick up the Aegis of the Immortal either."},
                                 'Lane creeps':{"__Lane creeps__":"A type of creep that automatically moves down the three lanes towards the enemy faction's Ancient. Each and every 30 seconds a new group (the creep wave) spawns for each faction at each of their barracks, but the number in the group and their stats eventually change, as the game progresses. Lane creeps engage any hostile unit nearby, but when left unattended, the opposing creeps end up clashing each other in the lanes on their way towards the enemy base.","Spawning":"Lane creeps spawn the first time as the game timer reaches 00:00, right after the game horn sounds. After that, they spawn every 30 seconds. Unlike melee and ranged creeps, siege creeps start spawning on the eleventh wave, and then every tenth wave. This means siege creeps spawn every 5 minutes, with the first ones spawning at 5:00.","Behaviour":"Lane creeps have a set path from which they do not deviate normally. The creeps walk down the lane aggressively, means they attack any enemy which comes within their acquisition range. If a lane creep gets aggroed and the aggroing unit stays within the creep's acquisition range, it chases the aggroing unit until it is dead, or until it lost track of it, or until another enemy gets within range and draws the aggro off. If the aggroing enemy entered the fog of war, the lane creep walks up to the last spot it saw the enemy. If it then does not see the enemy again, it returns to the point at which it left the lane it belongs to. If the aggroing unit is outside of the lane creep's acquisition range, it chases the enemy for up to 2.3 seconds before returning to its lane. A creep which no longer is aggroed does not join other lanes even if they are closer.",u"\u2800":"<a:note:595915864231116801>*The creeps of the very first creep wave spawn on both side lanes cannot be aggroed by players, until they meet the opposing creep wave. The creeps of the first wave in the mid lane can be aggroed normally.*"},
                                 'Neutral creeps':{"__Neutral creeps__":"A type of creep that are not controlled by any player. They are aligned to neither of the teams, and offer an alternative source of gold and experience. Neutral creeps appear in small camps scattered in the jungle on both sides of the map. They come with different power levels and most of them have unique abilities. Roshan, who sits in his den at the river, is also considered a neutral creep.\n\nNeutral creeps get more valuable gold and experience wise, as their bounties increase as the game goes on, similar to how lane creeps get stronger. Every 7 minutes and 30 seconds, all neutral creeps (including Roshan) have their gold and experience bounties increased by 2% of their base bounties.\n\nNeutral creeps start spawning at 01:00, and then spawn on every minute. A creep camp can never spawn the same set of neutral creeps in a row.\n\nNeutral creeps do not belong to either faction. Most of the time, they just stand in their camps, doing nothing. They only fight when aggroed."},
                                 'Roshan':{u"\u2800"*20+"__Roshan__":"The most powerful neutral creep in Dota 2. It is the first unit which spawns, right as the match is loaded. During the early to mid game, he easily outmatches almost every hero in one-on-one combat. Very few heroes can take him on alone during the mid-game. Even in the late game, lots of heroes struggle fighting him one on one, since Roshan grows stronger as time passes.\n\nRoshan is not a creep which can just be farmed like the other neutral creep camps, fighting him is an important team decision, as it needs the correct timing and approach since it can decide the future of the match. Usually, it is fought as a team when it is safe to do so, meaning when the enemy team does not display a threat at the moment (for example after a successful team fight).","Roshan pit / Roshpit":"Roshan can be found inside his pit, which is located to the left of the top river rune spot. The pit is completely inside the river, with the river splitting up at its entrance and merging again right behind the pit. The entry of the pit faces south-east, towards the mid lane.\n\nRoshan can only be attacked from within the Roshpit, with the torches at the pit entry marking where it begins. Spells can target Roshan from anywhere and are not restricted like attacks. Roshan himself can also attack from anywhere, he does not have to be within his pit to attack. Roshan always stays at the end of the pit when not attacking and only attacks if enemy units come within 150 range of him, or damage him from within 1800 range.\n*Mischief has a unique behavior when used inside the pit, transforming the caster into Aegis, Cheese, or into Refresher Shard, based on how often Roshan respawned.*","Vision in Roshpit":"Vision is very restricted around the pit by a vision blocker, which prevents units with ground vision from seeing past the boundary of the pit in either direction (in or out), even if they are on high ground. The vision blocker affects units and spells alike, so if a spell grants ground vision, its center has to be within the pit to see into it. However, the vision blocker does not affect units or spells with flying vision: they can see through it normally in both directions.\nObserver Wards and Sentry Wards cannot be placed inside the pit. However, Sentry Wards placed outside of it, and their True Sight area overlapping with the pit will function normally.","Roshan's death and ressurection":"When Roshan is slain, he lets loose a deafening roar and an announcement from the is played for all 10 players. Along with that, a screen message appears, announcing its death and which team killed it.\n\nRoshan respawns after a random time between 8–11 minutes. Unlike with other neutral creeps, the respawn cannot be prevented by any means. The players do not get any indicator for when exactly he respawns, but spectators and casters can see a clock at Roshan's spawn point, showing the exact time left for the respawn (not until 5 minutes after Roshan was slain).","Kill rewards":"Each player of the killing team is rewarded with 150 reliable gold, and the hero who deals the killing blow gets an extra random bonus of 225‒325 gold, effectively gaining 375–475 gold.\n\nUpon each death, Roshan always drops the Aegis of the Immortal. The Aegis of the Immortal can be picked up by any hero (except clones, illusions, and creep-heroes). It is not restricted to the team that slew Roshan, meaning an enemy hero can 'snatch' the Aegis of the Immortal. It can also be denied by attacking it. If the Aegis of the Immortal is not picked up and left on the ground, it disappears once Roshan respawns.","Additional drop":"Upon Roshan's second death and onwards, he also drops the Cheese, a completely shareable consumable item, which can be sold for 500 gold by the player who initially picks it up, or used to instantly restore health and mana. Just like the Aegis, the Cheese can also be picked up by anyone.\n\nUpon Roshan's third death and onwards, he also drops either the Refresher Shard, or Aghanim's Blessing, both having an equal chance of appearing. On his fourth death and onwards, he drops the Refresher Shard and Aghanim's Blessing, on top of dropping the Aegis of the Immortal and the Cheese.\n\nThe Refresher Shard is another completely shareable consumable item, which can also be sold for 500 gold by the player who initially picks it up, or used to instantly restore the cooldowns of all abilities and items, and restore all charges of charge-based abilities of the user. The Refresher Shard can be picked up by anyone as well.",u"\u2800":"Aghanim's Blessing, when dropped by Roshan, cannot be sold at all, unlike the bought version from the shop. Just like the Cheese and Refresher Shard, it is sharable, but gets automatically used by the hero who picks it up, unless the item enters the backpack or when the hero already has the Aghanim's Blessing buff."}}},

                  'ru':{'Атрибуты':{'Сила':{'__Сила__<:str:591659961092669462>':"Для всех героев, каждое очко силы<:str:591659961092669462>\n"+u"\u2022"+" Увеличивает максимальный запас здоровья на 20\n"+u"\u2022"+" Увеличивает регенерацию здоровья на 0,1\n"+u"\u2022"+" Увеличивает сопротивление магии на 0,08%\nГероям силы увеличивает урон от атаки на 1."},
                                    'Ловкость':{'__Ловкость__<:agi:591659959905812500>':"Для всех героев, каждое очко ловкости<:agi:591659959905812500>\n"+u"\u2022"+" Увеличивает броню на 0,16\n"+u"\u2022"+" Увеличивает скорость атаки на 1\n"+u"\u2022"+" Увеличивает скорость передвижения на 0,05%\nГероям ловкости увеличивает урон от атаки на 1"},
                                    'Интеллект':{'__Интеллект__<:int:591659960551604234>':"Для всех героев, каждое очко интеллекта<:int:591659960551604234>\n"+u"\u2022"+" Увеличивает максимальный запас маны на 12\n"+u"\u2022"+" Увеличивает регенерацию маны на 0.05\n"+u"\u2022"+" Усиливает урон от способностей на 0.07%\nГероям интеллекта увеличивает урон от атаки на 1"},
                                    'Броня':{"__Броня__<:armor:591659959960469524>":"Атрибут, уменьшающий (или увеличивающий в случае отрицательного значения) физический урон, получаемый юнитом от заклинаний и атак. Броню каждого юнита можно увеличивать или уменьшать и у большинства юнитов есть небольшое количество начальной брони, хоть у некоторых это значение может быть и отрицательным. Броня героя пассивно увеличивается от ловкости (герои ловкости получаю больше брони, чем остальные), талантов, некоторых предметов и способностей. Броню каждого юнита можно также временно увеличить или уменьшить способностями \nКаждая единица ловкости<:agi:591659959905812500> увеличивает броню героя на 0.16","**Начальная броня**" :"Часть основной брони, которая никогда не меняется в течение игры. Она состоит из одного индивидуального для каждого юнита значения. Начальная броня юнита может быть и отрицательным значением. Так как только герои имеют ловкость, интерфейс всех юнитов не-героев отображает их начальную броню.","**Основная броня**":"Значение брони, отображаемое белыми цифрами рядом с иконкой щита на интерфейсе, состоящее из начальной брони и брони за ловкость героя. Единственный способ увеличить основную броню героя — увеличить его ловкость путем поднятия уровня, приобретения определенных предметов или с помощью некоторых способностей\nФормула для расчета основной брони героя: ```основная броня = начальная броня + ловкость * 0.16```"},
                                    'Сопротивление магии':{"__Сопротивление магии__<:magic_resist:591659960249745460>":"Показатель, который уменьшает (или увеличивает, если отрицательный) магический урон, получаемый юнитами от заклинаний и атак. Большинство юнитов начинают с небольшим базовым магическим сопротивлением и способны его получить или терять. Сопротивление магии героя может быть пассивно увеличено силой (Герои для которых сила является основным атрибутом получают больше сопротивления, чем другие герои), талантами, определенными предметами и некоторыми способностями. Сопротивление магии любого юнита также может быть временно увеличено или уменьшено с помощью некоторых способностей.\nКаждое очко силы увеличивает сопротивление магии героя на 0.08.","Формула":"Все источники сопротивления магии складываются мультипликативно. Это означает, что значение магического сопротивления юнита изменяется меньше, чем выше его сопротивление магии, и чем больше, тем ниже оно. Это препятствует достижению 100% сопротивления магии, складывая различные источники.\n\n```Итоговое сопротивление магии = 1 − ((1 − врождённое сопротивление) × (1 - сила × 0.08%) × (1 − первый бонус сопротивлению) × (1 − второй бонус сопротивлению) × ... × (1 - n-ый бонус сопротивлению) × (1 + первое уменьшение сопротивления) × (1 + второе уменьшение сопротивления) × ... × (1 + n-ое уменьшение сопротивления))```\n```Фактический урон способности, имеющей магический урон = магический урон × (1 − врождённое сопротивление) × (1 - сила × 0.08%) × (1 − первый бонус сопротивлению) × (1 − второй бонус сопротивлению) × ... × (1 - n-ый бонус сопротивлению) × (1 + первое уменьшение сопротивления) × (1 + второе уменьшение сопротивления) × ... × (1 + n-ое уменьшение сопротивления))```"},
                                    'Здоровье':{"__Здоровье__":"Жизненная сила героя. Если ваше здоровье достигнет 0, вы умрёте. Здоровье увеличивается при увеличении вашего уровня, наложении на вас определённых эффектов или приобретении предметов, дающих силу. У всех героев базовый показатель здоровья равен 200 единицам, плюс 20 единиц за каждое очко силы<:str:591659961092669462>. Так как все герои имеют начальную силу и прирост к силе с уровнем, их запас здоровья возрастает с уровнем. Базовая сила героя не может опуститься ниже 1, однако можно достигнуть общего значения 0 путём уменьшения дополнительной силы.","Регенерация здоровья":"Количество здоровья, которое юнит получает в секунду. Оно отображается маленькой цифрой со знаком + справа в полосе здоровья юнита."},
                                    'Мана':{"__Мана__":"Магическая сила юнита. Она используется как стоимость для большей части активных и меньшей части пассивных способностей. Каждый герой имеет начальный запас маны в 75 единиц, когда большинство не-героев имеют указанный запас маны лишь в случае, если у них есть способности, нуждающиеся в мане за несколькими исключениями. Значения маны фиксированы и не могут быть изменены. Это значит, что максимальный запас маны никогда не опустится ниже 75.\nКаждая единица интеллекта<:int:591659960551604234> увеличивает запас маны героя на 12. Так как каждый герой имеет начальный интеллект и получает интеллект за уровень, их запас маны становится тем больше, чем выше их уровень. Базовый интеллект героя не может упасть ниже 1, но при этом он может достигнуть 0 с помощью отрицательного бонусного интеллекта.","Регенерация маны":"Количество маны, которую юнит восстанавливает каждую секунду. Она отображается как маленькое число со знаком + с правой стороны полосы маны юнита."},
                                    'Скорость передвижения':{"__Скорость передвижения__<:move_speed:591659960753192960>" :"Cкорость, с которой герои и существа перемещаются за секунду. Нижнее её значение равно 100, а базовое максимальное — 550, хотя это значение может быть превышено некоторыми способностями. Каждое существо, способное двигаться, имеет начальную скорость передвижения, которая может быть увеличена или уменьшена различными предметами и способностями. Юниты без способности к передвижению не могут двигаться, даже получив скорость от способностей. Атрибут ловкость даёт 0.05% скорости передвижения за единицу.","Сочетание":"Фиксированные бонусы просто добавляются к базовой скорости передвижения юнита, процентные бонусы сначала складываются между собой, а затем добавляются к общей скорости. При этом у большинства предметов с бонусами есть ограничения по сочетанию. Пассивные бонусы разделены на группы. То есть несколько предметов из одной группы не будут складываться или дополнять друг друга, но будут сочетаться с бонусами предметов из другой группы.\n"+u"\u2022"+" 1-я группа: предметы, содержащие Boots of Speed\n"+u"\u2022"+" 2-я группа: предметы, содержащие Yasha\n"+u"\u2022"+" 3-я группа: Wind Lace\n"+u"\u2022"+" Drum of Endurance, Eul's Scepter of Divinity, Solar Crest и Spirit Vessel не входят в группу, поэтому сочетаются и усиливают как друг друга, так и другие бонусы предметов, включая Wind Lace.\n"+u"\u2022"+" У бонусов от способностей нет ограничений, поэтому они сочетаются с другими бонусами.\n\n**Формула**\n```Скорость передвижения = (начальная скорость передвижения + сумма фиксированных бонусов) × (1 + сумма процентных бонусов - сумма замедлений)```"},
                                    'Сопротивление эффектам':{"__Сопротивление эффектам__":"Характеристика героя, которая уменьшает длительность контроля и значения замедлений. Обычно у юнитов нет базового сопротивления эффектам.","Формула":"Все источники уменьшения сопротивления эффектам складываются по убыванию. \n```Суммарное сопротивление эффектам = 1 − ((1 − бонус первого сопротивления) × (1 − бонус второго сопротивления) × ... × (1 - бонус n-ого сопротивления))```\n```Фактическая длительность негативного эффекта = Длительность × (1 − (1 − бонус первого сопротивления) × (1 - бонус второго сопротивления) × ... × (1 - бонус n-ого сопротивления)```"},
                                    'Скорость поворота':{"__Скорость поворота__<:turn_rate:591659960857788416>" :"Скорость вращения юнита, не зависящая от его скорости передвижения. Каждый юнит имеет свою базовою скорость поворота, которая может уменьшиться от некоторых способностей и предметов. Базовая скорость поворота большинства героев составляет от 0,4 до 0,8.\n\nСкорость поворота выражается в радианах в 0,03 секунды. Иными словами скорость поворота юнита обозначает часть радианы, на которую юнит сможет повернуться за 0,03 секунды.\n\nУменьшение скорости поворота напрямую влияет на базовую скорость поворота юнита. Например, уменьшение скорости поворота на 70%, применённое к юниту с 0,5 базовой скорости поворота, снизит текущую скорость поворота до 0,15. (0,5 × (1-0,7))","Формула":"Если 0.03×π разделить на скорость поворота, то получим время, которое потребуется юниту для разворота на 180°.\n\n`(0,03 × π / T = t)`, где T — скорость поворота и t — время разворота на 180°"},
                                    'Обзор':{"__Обзор__<:vision:591659960794873858>":"Описывает то, что юнит может и не может увидеть с его текущего места и состояния. Места которые юнит не может видеть заполнены туманом войны, тёмным туманом который прячет юнитов внутри него. Невидимых юнитов нельзя увидеть даже если они не в тумане войны, но их можно обнаружить с источниками True Sight. Юниты не могут видеть сквозь деревья или возвышенности - единственными исключениями являются летающие юниты, которые имеют свободный обзор, Night Stalker/Keeper of the Light с Aghanim's Scepter в ночь/день и Monkey King который может прыгать по деревьях.\n\nВсе юниты вашей команды имеют общий обзор, это значит что если юнит видит через туман войны, все союзники также будут видеть. Это также применяется к линейным крипам, другим управляемым крипам и строениям."}},
                        'Атака':{'Анимация атаки':{"__Анимация атаки__":"Каждый герой в Dota 2 обладает анимацией атаки. В механике, это задержка между командой атаки и моментом, когда наносится урон (для юнитов ближнего боя) или вылетает снаряд (для юнитов дальнего боя).\nЮниты также обладают анимацией после атаки, которая является задержкой между моментом, когда наносится урон, и следующим действием героя. Анимацию после атаки можно остановить (прервать) действием.\nВремя перед атакой и после неё снижаются в зависимости от скорости атаки, или IAS.","Формула":"```\nвремя перед атакой = (базовое время перед атакой) / (1 + IAS)\nвремя после атаки = (базовое время после атаки) / (1 + IAS)\n```\nГде IAS - значение в процентах от -0.8 до 5.00. \nСкорость полета снаряда не может быть уменьшена или увеличена.\nСкорость атаки юнита полностью независима от его анимации атаки. Анимация атаки строго относится к задержке между моментом, когда была выдана команда атаки и когда атака была запущена. \n\n*Другими словами, отмена анимации атаки не увеличивает скорость атаки*"},
                                'Урон от атаки':{"__Основной урон__<:damage:591659959825989637>":"Значение основного урона отображается белыми цифрами в статистике героя, он складывается из начального урона и значения основной характеристики героя. Единственный способ увеличить основной урон героя — увеличить его основной атрибут.\n\n**Формула**\n```основной урон = начальный урон + очки основного атрибута```","Начальный урон":"Начальный урон это часть основного урона, которая никогда не изменится в течение игры. Состоит из двух значений, минимального и максимального. Каждый раз, когда герой атакует, выбирается случайное значение между этими двумя.", "Показатели, изменяющие количество урона":"**Дополнительный урон**\nЗначение дополнительного урона (прямой бонус) отображается зеленым(красным, если значение отрицательно) числом в статистике героя.\n\n**Блокировка урона**\nБлокировка урона это пассивная способность, которая дает юниту шанс блокировать какой-то физический урон от атаки.\n\n**Процентный бонус к урону**\nДополнительный урон от источников процентного увеличения\n\n**Множитель критического урона**\nВысочайший множитель урона увеличит основной и дополнительный урон в определённое количество раз.\n\n**Множитель брони**\nБроня цели влияет на урон от атаки по ней и находится в промежутке 0-2, притом для цели без брони значение равно 1.\n```множитель урона = 1 - ((0.052 × броня) ÷ (0.9 + 0.048 × |броня|))```\n**Общие множители урона**\nНекоторые способности изменяют весь входящий урон, включая физический от атаки.","Формула количества урона":"```Урон = { [Основной урон × (1 + Сумма процентных бонусов) + Прямые бонусы] × Множители критического удара - Блокировка урона } × Множители брони × Общие множители урона```"},
                                'Модификаторы атаки':{u"\u2800"*20+"**__Модификаторы атаки__**":"*Модификаторы, применяющие эффект к обычным атакам юнита. Эти эффекты могут быть самыми разнообразными, от лечащих к наносящим урон или даже обезвреживающим эффектам. Большинство из этих модификаторов имеют собственные правила. Например, некоторые модификаторы не сочетаются с другими, некоторые могут полностью сочетаться, некоторые работают только или для юнитов ближнего боя, или для дальнего, или для обоих типов. Модификатор атаки может быть активным (в данном случае они обязательно применяются, если включена опция авто-атаки), пассивным или имеющим шанс сработать при каждой атаке.*",u"\u2022"+" Критический удар":"Модификатор атаки, позволяющий наносить атакой умноженный урон. Большинство критических ударов основаны на шансе. Эти модификаторы могут быть использованы любым юнитом.\n\nКритические удары полностью сочетаются с другими модификаторами атаки, но не полностью сочетаются друг с другом. Несколько источников критического удара имеют свой собственный шанс срабатывания. При единовременном срабатывании нескольких источников применяется только модификатор с наибольшим множителем.",u"\u2022"+" Прорубающий удар и урон по области":"Прорубающий удар позволяет наносить урон атакой юнита в трапециевидной зоне перед ним. Урон основан на уроне от атаки юнита. Прорубающий удар может использоваться только юнитами ближнего боя.\nПрорубающие удары полностью сочетаются с другими модификаторами атаки. Несколько источников прорубающего удара у одного юнита будут работать полностью независимо друг от друга. Каждый источник применит свой полный урон в области, без взаимодействия с другими источниками прорубающего удара.\n\nУрон по области работает схоже с прорубающим ударом. Он позволяет атакам юнитов наносить урон по области, но эта область круглая и её центром является атакованный юнит. Урон по области может использоваться только юнитами дальнего боя.\nУрон по области полностью сочетается с другими модификаторами атаки. Несколько источников у одного юнита будут работать полностью независимо друг от друга. Каждый источник применит полный урон в области, без взаимодействия с другими источниками урона по области.",u"\u2022"+" Оглушающий удар":"Модификатор, позволяющий атаке юнита оглушить цель и в некоторых случаях нанести дополнительный фиксированный урон. \n\nОглушающие удары полностью сочетаются с другими модификаторами атаки, кроме других оглушающих ударов. Несколько источников оглушающего удара не сочетаются. Последний примененный оглушающий удар не подействует. ",u"\u2022"+" Вампиризм":"Модификатор, позволяющий атаке юнита лечить атакующего юнита. Кроме одного случая, лечение основано на уроне от атаки юнита. Вампиризм может использоваться любым юнитом.\n\nВампиризм может быть в форме обычного модификатора атаки (в данном случае он полностью сочетается с другими модификаторами атаки, включая другие источники вампиризма) или в форме уникального модификатора атаки (в данном случае он не будет сочетаться с другими источниками модификаторами атаки).",u"\u2022"+" Сжигание маны":"Модификатор, позволяющий атаке юнита сжигать порцию маны цели и наносить урон основанный на количестве сожжённой маны. \n\nСжигание маны может быть в форме обычного модификатора атаки, сочетающегося со всеми другими модификаторами атаки, или в форме уникального модификатора атаки, сочетающегося со всеми другими источниками атаки, кроме других уникальных модификаторов атаки. Несколько источников сжигания маны не сочетаются, не зависимо от типа."},
                                'Дальность атаки':{"__Дальность атаки__":"Расстояние, на котором герои могут использовать их обычную атаку, атакуя другого юнита. Дальность атаки является постоянным атрибутом и может изменяться только некоторыми способностями и предметами.","Ближний бой и дальний бой":"Юниты ближнего боя могут иметь большую дальность атаки, чем юниты дальнего боя. Также существуют некоторые отличия между героями дальнего и ближнего боя: \n"+u"\u2022"+" **Удар героя ближнего боя** проходит мгновенно по окончании атаки.\n"+u"\u2800"*2+u"\u2022"+" Герои ближнего боя имеют различные значения приобретенных предметов, таких как Stout Shield или Quelling Blade.\n"+u"\u2800"*2+u"\u2022"+" Некоторые способности работают лишь для или против героев ближнего боя.\n\n"+u"\u2022"+" **Герои дальнего боя** стреляют снарядами во время атаки.\n"+u"\u2800"*2+u"\u2022"+"Метательную атаку можно избежать, также есть вероятность промаха при атаке цели на более высокой местности.\n"+u"\u2800"*2+u"\u2022"+"<:dk:553950717103177739>Dragon Knight, <:lonedruid:553951108259643402>Lone Druid, <:troll:553951535822798849>Troll Warlord, и <:terrorblade:553951283271303169>Terrorblade имеют способности, позволяющие переключаться между ближним и дальним типом атаки."},
                                'Скорость атаки':{"__Скорость атаки__":"Частота с которой атакует юнит. Скорость атаки юнита может быть изменена предметами, ловкостью, способностями и аурами.\n\nКаждый юнит имеет базовое время атаки (БВА), которое является стандартным интервалом между атаками для юнита без эффектов, с 0 ловкости и без бонусов к скорости атаки. Например, крип-мечник имеет БВА в 1,00 секунды. Так же, если герой с 1,7 БВА имеет 0 ловкости и не имеет бонусов к скорости атаки, он будет атаковать каждые 1,70 секунды.","Расчет скорости атаки":"Эквивалентом базовому времени атаки является базовая скорость атаки. Для большинства героев это 1 / 1,7 = 0,588 атак в секунду. Скорость атаки выражается в процентах от базовой скорости атаки. База выражается как 100. Каждое очко увеличенной скорости атаки (УСА) добавляет 1 к базе, добавляя 1% к базовой скорости атаки. Каждое очко ловкости<:agi:591659959905812500> увеличивает УСА на 1. УСА также изменяема предметами, способностями, эффектами и негативными эффектами. Скорость атаки работает вместе с БВА чтобы определить, как часто будет атаковать юнит.\n\n`Атак в секунду = [(100 + УСА) × 0,01] / БВА`\n`Время атаки = БВА / [(100 + УСА) × 0,01] = 1 / (атак в секунду)`","Пример":"<:axe:553950552493654066>Axe 1-го уровня без предметов имеет БВА 1,7 и 20 ловкости, которые конвертируются в 0,20 УСА.\n\nАтак в секунду = `[(100 + УСА) × 0,01] / БВА`\nАтак в секунду = `[(100 + 20) × 0,01] / 1,7`\nАтак в секунду = `1,2 / 1,7`\nАтак в секунду = `~0,706`\n>> <:axe:553950552493654066>Axe атакует примерно `0,706` раз в секунду.\n\nВремя атаки = `1 / 0,706`\nВремя атаки = `~1,417`\n>> <:axe:553950552493654066>Axe имеет примерно `1,417` секунд между атаками."},
                                'Типы урона':{u"\u2800"*24+"**__Урон__**":"*Любое уменьшение текущего состояния здоровья юнита. Герои, крипы, древние, Рошан и фонтан способны наносить урон.*","Типы урона":"Все формы повреждений распределены по типам урона. В Dota 2 существуют 3 главных типа урона: **Чистый**, **Магический** и **Физический**. Физический урон может быть уменьшен бронёй или блокировкой урона, магический урон понижается благодаря сопротивлению к магии, в то время как чистый урон не может быть уменьшен сопротивлением к магии или бронёй.",u"\u2022"+"Физический урон":"Физический урон наносят обычные атаки всех юнитов в игре, а также некоторые заклинания. Этот урон изменяется бронёй и блокировкой урона, которую дают некоторые предметы и способности, но на него не влияет сопротивление магии или неуязвимость к ней, но в то же время он не может быть нанесён юнитам, находящимся в призрачной форме.\n\nЕдинственное исключение здесь - это урон от прорубающего удара, который уменьшается только в зависимости от типа брони, но не от её значения или блокировки урона. Говоря практически, броня бесполезна против прорубающего урона. Урон по области от дальних атак уменьшается как обычно.",u"\u2022"+"Магический урон":"Магический урон наносят большинство способностей. Этот урон уменьшается сопротивлением магии и его невозможно нанести юнитам с иммунитетом к магии.",u"\u2022"+"Чистый урон":"Чистый урон — это тип урона, который не уменьшается магическим сопротивлением и не усиливается благодаря предметам или способностям, увеличивающим магический урон, таким как Veil of Discord или  Ancient Seal. Также полностью игнорируется броня и блокировка урона. Однако, такой урон всё равно может быть увеличен или уменьшен способностями, которые влияют на любой тип урона, к примеру  Dispersion или  Soul Catcher. Чистый урон наносится юнитам с иммунитетом к заклинаниям, но это не значит, что наносящая чистый урон способность может быть направлена на цель с иммунитетом"},
                                'Скорость снаряда':{"__Скорость снаряда__":"Скорость, с которой движется снаряд атаки юнитов. Скорость снаряда в 900 значит что снаряд пролетает 900 единиц расстояния в секунду. Базовая скорость снаряда равна 900.\nСкорость снарядов героев разнится от 700 до 3000."}},
                        'Способности':{'Способности ':{"__Способности__":"Уникальные навыки, которыми могут обладать герои и крипы. В зависимости от принципа действия, все способности делятся на активные и пассивные. Герои могут обладать четырьмя и более способностями, одна из которых является особой. \nАктивные способности при использовании потребляют часть маны героя. После использования активной способности включается таймер её перезарядки. Таким образом, должно пройти некоторое время, прежде чем данной способностью можно будет воспользоваться снова.\n\nСуществует три типа способностей : **Активные**, **Пассивные**, **Авто-применяемые**",u"\u2022"+"Активные":"Активные способности применяются игроком вручную. Большинство способностей в игре активные. Такие способности как правило потребляют ману, имеют перезарядку, разные виды прицеливания. Например, при типе прицеливания 'направленная на юнита' игроку нужно нажать на иконку способности, а затем выбрать цель для её применения. Эти способности изображаются со скосом вокруг иконки, что делает её похожей на кнопку. Активация происходит нажатием на горячую клавишу или непосредственно курсором на иконку. Кроме того, активные способности могут быть прерываемыми. Это значит, что применение заклинания можно прекратить, совершив любое другое действие (оглушение также прерывает такие заклинания).",u"\u2022"+"Пассивные":"Пассивные способности активируются сразу после изучения. Они могут воздействовать на самого героя, а могут работать как аура вокруг него. Такие способности, как правило, не требуют маны, и чаще всего не имеют таймера перезарядки. Пассивные способности не имеют скосов и выглядят будто впрессованными в интерфейс. Так как пассивные способности невозможно активировать вручную, их вид не изменяется. Иконки пассивных способностей появляются только при их изучении.",u"\u2022"+"Авто-применяемые":"Вместо использования такой способности вручную, игрок может включить её автоматическое использование. Некоторые такие способности являются уникальными модификаторами атаки. Когда функция авто-применения включена, способность будет применяться самостоятельно, без нажатия на нее. Например,  Frost Arrows будет применяться каждый раз, когда <:drow:553950717283663928>Drow Ranger будет атаковать. При выключенном авто-применении это заклинание не будет активироваться самостоятельно. Не все способности имеют полное авто-применение. Некоторые из таких способностей являются базовыми способностями героев. Например, Bloodlust будет автоматически использоваться и выбирать союзника рядом по истечению перезарядки."},
                                       'Аура':{"__Аура__":"Пассивная способность, которая накладывает положительный или отрицательный эффект на всех юнитов вокруг обладателя ауры. Область действия ауры — круг определенного радиуса, в центре которого находится герой — обладатель ауры. Ауры действуют постоянно и не расходуют ману героя.\n\nВсе ауры можно разделить на два типа — положительные и отрицательные. Некоторые предметы обладают двойными аурами — на союзных героев они действуют положительно, а на вражеских юнитов — отрицательно.","Положительные ауры":"Действуют на всех дружественных героев вокруг обладателя ауры и на самого обладателя ауры. Они дают им положительные эффекты или бонусы — дополнительную скорость атаки, регенерацию здоровья и маны, дополнительную броню или урон, скорость передвижения и дополнительную магическую защиту. Ауры, от одинаковых предметов, схожие по действию или дающие одинаковые бонусы не сочетаются между собой – работать будет только аура с наивысшим значением.","Отрицательные ауры":"Действуют на всех вражеских юнитов поблизости обладателя ауры. Отрицательная аура действует как на видимых так и на невидимых врагов. Отрицательные ауры уменьшают броню, скорость атаки и скорость передвижения врагов, уменьшают наносимый ими урон или наносят им урон. Все отрицательные ауры, за исключением Radiance и  Rot нельзя выключить или включить — они работают постоянно. Одинаковые отрицательные ауры не будут сочетаться от нескольких предметов — работать будет только одна аура.\n\nАуры некоторых предметов могут работать в двух режимах — либо действовать только на героев, либо действовать и на героев и на других союзных юнитов вокруг. На переключение таких аур мана не требуется.\n\nДействие некоторых аур зависит от типа атаки героя — аура может действовать только на героев с ближним типом атаки, или только на героев с дальним типом атаки."},
                                       'Анимация применения':{'__Анимация применения__':"Каждый юнит имеет уникальные анимации применения для каждого их заклинания. Анимация применения заклинания будет принята, как только выбрана цель для заклинания, если она нужна, или нажата горячая клавиша, если цель не нужна.\n\nКаждое заклинание имеет определенный период времени за который должна пройти единица применения для успешного применения эффектов заклинания. Это время часто известно как точка применения или время применения.","Прерывание применения заклинания":"Когда юнит прерывается обезвреживаниями или его собственными действиями до точки применения заклинания, применение отменяется, эффекты заклинания не применяются, оно не идет на перезарядку и не потратит ману. Игрок также может вручную остановить применение заклинания нажав команды стоп или остановка. Когда применение заклинания прерывается в промежуток времени применения, анимация визуального применения также остановится."},
                                       'Произнесение':{"__Произнесение__":"Произнесение способности заставляет героя перестать действовать в течение всего действия способности. Произносимое заклинание может быть прервано другим действием или использованием другой способности. Пока идёт произнесение заклинания, внизу появится панель, указывающая, сколько осталось до конца произнесения.","Предметы, не прерывающие произнесение":"Единственными предметами, которые могут быть использованы во время произнесения являются Armlet of Mordiggian, Glimmer Cape, Mask of Madness, Варды (только при смене), Phase Boots, Radiance, Ring of Basilius, Shadow Amulet, Shadow Blade, Shiva's Guard и Silver Edge. Обратите внимание, что даже если сами предметы не прерывают произнесение, то их эффекты после использования (например, применяемое к заклинателю безмолвие) всё ещё прерывают произнесение. Активация любых других предметов прервёт произнесение заклинания."},
                                       'Периодический урон':{"__Периодический урон__":"Состояние в котором затронутый юнит будет получать урон пока время действие эффекта не прекратится, не развеется или цель не выйдет за области действия способности. Урон наносится с интервалом (с тиком), первый из которых начинается с применением заклинания. Некоторые заклинания наносят начальный урон, которые могут совпадать или не совпадать с периодическим уроном.","Примечание: ":"**Начальный урон**: большая часть способностей наносит урон сразу после применения. В данном случае начальный урон равен периодическому. У некоторых способностей базовый урон может отличаться.\n**Интервал**: время между срабатываниями в секундах. \n**Урон за интервал**: урон, наносимый при каждом срабатывании после начального. \n**Длительность урона**: длительность с начала применения до последнего нанесения урона. В большинстве случаев длительность нанесения урона меньше длительности эффекта, особенно если способность срабатывает сразу. \n**Число интервалов**: как правило выражается `Длительность урона / Длительность интервала`. Не включает в себя начальный урон. \n**Макс. общий урон**: как правило выражается `Базовый урон + Урон за применение × Число интервалов`"},
                                       'Уклонение':{"__Уклонение__":"Пассивная способность которая дает юниту шанс избежать входящую физическую атаку. Под действием уклонения, атака полностью обнуляется, будто она промахнулась. Это значит, что если атака имела модификатор атаки, то на неё не применяются никакие модификаторы (за несколькими исключениями).\n\nСхожую механику с уклонением имеет ослепление. Если уклонение позволяет юниту уклониться от входящих атак других юнитов, то ослепление заставляет юнита промахиваться при атаке других юнитов. Как и с уклонением, когда атака промахивается от ослепления, она ведет себя, будто её избежали.","Сочетание":"Несколько источников уклонения сочетаются мультипликативно, также, как и другие источники шанса промахнуться, такие, как ослепление и шанс промаха при атаке юнита на возвышености.\nШансы всех источников уклонения определяются псевдо-случайным распределением."}},
                        'Эффекты состояния':{'Иммунитет к атакам':{"__Иммунитет к атакам__":"Механика, не дающая выбрать юнита целью для обычных атак. Юнит под действием не выбирается целью и не получает урона или эффектов от уже запущенных снарядов. Уже начатые атаки отменяются.\n\nМгновенная атака может выбрать целью юнитов с иммунитетом, если она — дальнего боя, но все равно не подействует, если юнит останется под действием иммунитета при попадании. Мгновенные атаки ближнего боя не могут выбрать юнитов с иммунитетом."},
                                             'Обезвреживание':{u"\u2800"*20+'**__Обезвреживание__**':'*Процесс, описывающий любую способность или эффект состояния, которые препятствуют, запрещают или иным образом не дают герою действовать. Обезвреживание имеет множество вариаций, и большинство Героев имеют в своем арсенале обезвреживающие способности разных типов. Иногда под "обезвреживанием" подразумевают оглушение.*',u"\u2022"+" Оглушение":"Оглушение является наиболее распространенным и надежным способом обезвреживания противника. Герой под действием оглушения не может двигаться, атаковать, использовать заклинания и предметы до завершения действия эффекта. Оглушение прерывает произнесение способностей и предметов, например Town Portal Scroll. Обычно из-за оглушения над головой задетых героев появляется характерная анимация.",u"\u2022"+" Сковывание":"Сковывание так же, как и оглушение, полностью выводит цель из строя, не позволяя ей двигаться, атаковать, использовать способности или предметы и прерывая произносимые заклинания. Отличие сковывания от обычного оглушения состоит в том, что герой, применяющий сковывание, теряет способность атаковать и\или двигаться во время произнесения заклинания и на время его действия, либо же оно накладывает какие-либо негативные эффекты (например замедляет применяющего).",u"\u2022"+" Сон":"Сон действует так же, как и оглушение, с той лишь разницей, что эффект будет снят, если объект, на который он наложен, будет атакован или получит урон. Сон также может давать временную неуязвимость объекту, на который он накладывается.",u"\u2022"+" Ураган":"Ураган работает так же, как и оглушение, но, помимо полного обезвреживания, делает цель неуязвимой на всю длительность и поднимает её в воздух, поэтому остальные юниты могут под ней проходить.",u"\u2022"+" Замедление":"Замедление, как правило, снижает текущую скорость передвижения или скорость атаки (или оба показателя).\nЗамедления, влияющие на скорость передвижения, влияют на неё в процентном соотношении. Персонаж под действием ускорения имеет полный иммунитет к любым замедлениям.\nЗамедления, влияющие на скорость атаки, уменьшают скорость фиксированным, не процентным числом.",u"\u2022"+" Безмолвие":"Безмолвие заставляет вражеских героев замолчать, не давая им возможности использовать свои способности. Эффект не влияет на возможность героя перемещаться, использовать предметы и атаковать. Также безмолвие не отключает пассивные способности.",u"\u2022"+" Заглушение":"Заглушение похоже на безмолвие, за исключением того, что оно, помимо заклинаний, блокирует и активные предметы. Заглушение обычно накладывается вместе с обычным безмолвием.",u"\u2022"+" Истощение":"Истощение выключает пассивные способности затронутого героя. Большинство пассивных способностей отключаются, но не все. В основном, послесмертные пассивные способности ( Reincarnation, пассивная активация  Requiem of Souls) не отключаются. Также не отключаются пассивные способности, которые напрямую взаимодействуют с другими способностями героя, например  Grow которая влияет на урон от  Toss. Истощение также не выключает любые пассивные способности предметов.",u"\u2022"+" Принудительное движение":"Некоторые заклинания могут принудительно передвигать юнитов, не позволяя им своевольное передвижение. Некоторые полностью ограничивают возможность передвижения на протяжении их времени действия. Однако, некоторые заклинания всё же позволяют персонажам поворачиваться, атаковать, произносить заклятья или использовать предметы.",u"\u2022"+" Оцепенение":"Оцепенение (изначально известное как Ensnare(Ловля в сеть)) это способ обездвиживания врага, блокируя использование определенных заклинаний (например  Teleportation, Blink Dagger и собственные Blink героев), но при этом не запрещает им поворачиваться, использовать заклинания или предметы. Некоторые оцепенения также применяют обезоруживание (обезоруживающее опутывание также известно как Entangle(Стягивание)).",u"\u2022"+" Проклятие / Хекс":"Проклятие превращает героя в безобидную зверушку — юнита, неспособного атаковать или использовать навыки и предметы. Проклятие опускает базовую скорость передвижения до определенного значения (обычно достаточно низких) и применяет к цели безмолвие, заглушение и обезоруживание. Эффект не влияет на другие характеристики юнита (как, например, скорость поворота, обзор, размер столкновения и прочие) и не запрещает ему получать опыт и золото.\nПроклятие можно развеять **сильным** развеиванием\nВсе источники проклятия *не имеют времени применения* и мгновенно уничтожают иллюзии.",u"\u2022"+" Провокация":"Провокация заставляет цель атаковать определенного юнита. Цель не способна делать ничего иного, пока провокация не спадет. Цель прекращает любые текущие приказы, включая прерываемые способности. Если атакующий оказывается неспособным атаковать или цель становится неуязвимой, атакующий преследует цель, пока возможность атаки не возвратится, или эффект провокации не спадет.",u"\u2022"+" Страх":"Страх заставляет цель бежать от точки применения в сторону фонтана(герои) или лагеря(нейтральные крипы). При этом ей недоступны никакие действия до завершения эффекта.",u"\u2022"+" Исчезновение":"Исчезновение (так же известное как изгнание) временно убирает юнита с карты. Пока юнит отсутствует, он не может стать целью заклятий (некоторые заклятия все же способны на это) и не способен производить никаких действий. Он не способен двигаться, атаковать, применять заклинания или использовать предметы. Обычно, некоторые заклятия исчезновения накладывают неуязвимость.",u"\u2022"+" Призрачная форма":"Призрачная форма не ограничивает возможность юнита применять способности, но запрещает атаковать и делает его невосприимчивым к физическому урону, уменьшая сопротивление магии, тем самым увеличивая урон от магии.",u"\u2022"+" Обезоруживание":"Обезоруживание отнимает возможность цели атаковать, но не запрещает атаки по ней.",u"\u2022"+" Ослепление":"Ослепление заставляет юнита промахиваться при атаках. Промахи при слепоте рассчитываются отдельно от уклонения."},
                                             'Невидимость':{"__Невидимость__":"Эффект состояния, скрывающий юнитов и героев на экране или миникарте врага и не дающий противнику их напрямую выбрать. Невидимость делает модель юнита прозрачной, но она очерчивается для союзников. Если невидимым стал союзник, то его маркер на миникарте превращается из точки в круг.","Свойства":u"\u2022"+" В невидимости юнит никогда не будет автоматически атаковать ближайших врагов - даже если его начнут атаковать при выявлении с помощью True Sight. При этом, если юниту отдали приказ на атаку через выбор точки на земле, то невидимый юнит атаковать будет.\n"+u"\u2022"+" У героев дальнего боя невидимость пропадает в момент запуска снаряда. \n"+u"\u2022"+" В зависимости от источника невидимость может применять к юниту возможность проходить сквозь других юнитов.\n"+u"\u2022"+" Произносимые заклинания не отменяются, если заклинатель стал невидимым после начала произнесения.\n"+u"\u2022"+" Все дальние атаки и большинство снарядов способностей можно избежать невидимостью.\n"+u"\u2022"+" На невидимых юнитов продолжают частично или полностью воздействовать заклинания, действующие по области."},
                                             'Иммунитет к заклинаниям':{"__Иммунитет к заклинаниям__":"Модификатор, который запрещает применение множества способностей на юнита. Включает в себя заклинания на 1 цель, заклинания на область, пассивные и активные способности.\n\nБольшинство заклинаний в игре изначально проверяют есть ли у юнита иммунитет к заклинаниям или нет. Если модификатор действует, заклинания на одну цель не могут нацелится на юнита вообще, в отличии от заклинаний на область, которые игнорируют юнита и уже направленные эффекты не будут влиять на него.\n\nКогда юнит получает иммунитет к заклинаниям пока снаряд способности уже летит к нему, снаряд не оказывает никакого эффекта по достижению цели, если заклинание не проникает сквозь иммунитет к заклинаниям. \n\nВсе источники иммунитета к заклинаниям также дают затронутым юнитам 100%-е сопротивление магии. Это значит что затронутый юнит вообще не получит магический урон, даже от заклинаний которые проникают сквозь иммунитет к заклинаниям."}},
                        'Мир':{'Опыт':{"__Опыт__":"Элемент, получаемый героем за убийство вражеских юнитов или присутствие при их смерти. Сам по себе опыт ничего не делает, но при накоплении увеличивает уровень героя, наращивая его мощь. Только герои получают опыт и только они могут повышать свои уровни. С каждым уровнем базовые атрибуты героя увеличиваются на фиксированные значения (уникальные для каждого).","Распределение опыта при смерти героя":"Когда вражеский юнит умирает, дается опыт, распределяемый между всеми союзными героями на расстоянии 1500. Опыт делится между всеми союзными героями, давая тем меньше процентов опыта, чем больше героев находится в области. Герои, уже достигшие 25 уровня, все равно продолжают получать свою часть опыта.\n\n**Формула**\n `(40 + 0,14 * Опыт убитого героя ) / кол-во убивающих`\n\nТакже, если у убитого героя была действующая серия убийств (>2), то за него дают дополнительный опыт, помимо базовой награды, равный `200 * ( серия убийств - 1 )` Максимальная серия убийств - 10, то есть если игрок имеет серию из 10 / 15 / 25, убивший его получит 1800 дополнительного опыта в любом из этих случаев."},
                               'Золото':{u"\u2800"*20+"__Золото__":"Валюта используемая при покупке предметов или мгновенного возрождения героя. Золото можно заработать убийством героев, крипов или уничтожении строений.","Золото игрока делится на две категории:":u"\u2022"+"**Надежное золото** - Любая награда с убийств героев, Рошана, курьеров, Hand of Midas, золото с Track и глобальное золото из башен, добавляется к вашему надежному запасу золота.\n"+u"\u2022"+"**Ненадежное золото** - Всё остальное (начальное золото, периодическое золото, убийство крипов, нейтралов и т.п.).\n\nМежду этими категориями отличие в том как каждое золото тратится:\n"+u"\u2022"+"Смерть забирает только золото из ненадежного запаса золота.\n"+u"\u2022"+"При покупке предметов используется сначала ненадежное золото, а уже потом надежное.\n"+u"\u2022"+"Выкуп использует сначала надежное золото.\nЕсли навести мышкой на количество общего золота на интерфейсе, отобразится ваше надежное и ненадежное золото.\n\n*Целью разделения золота на эти две категории является поощрение ганков и уничтожение башен, которые дают надежное золото, вместо пассивного фарма, который дает ненадежное золото.*","Периодическое золото":"Каждый игрок получает 1 единицу ненадёжного золота каждые 0,66 секунды (начиная с 0:00 на игровых часах), что равно 91 единице золота в минуту. Некоторые герои могут выбирать таланты, которые увеличат базовую частоту получения золота.","<a:Emoticon_bountyrune:594813355303239700>Руна богатства<a:Emoticon_bountyrune:594813355303239700>":"Активация <a:Emoticon_bountyrune:594813355303239700>**Руны богатства**<a:Emoticon_bountyrune:594813355303239700> даёт игрокам подобравшей команды ненадежное золото в зависимости от длительности игры, начиная с 40 золота, и увеличиваясь на 2 золота в минуту, интервалами по 30 секунд.","Убийства героев":"Убийства героев дают убившему надежное золото. Бонусное золото выдается за остановку полосы убийств. Герою который сделал первое убийство в матче дается дополнительных 150 надежного золота; это называется «Первая кровь».\n\nКогда герой умирает от вражеских крипов или башни и не получал урона от вражеских героев в последние 20 секунд (не зависимо от дистанции между героями), золото за убийство разделяется между всеми вражескими героями. Когда герой умирает от вражеских крипов или башни и получил урон от одного героя, этому герою засчитается убийство. Когда в радиусе 1300 несколько вражеских героев, золото разделяется между всеми героями.\n\nКаждый раз, когда герой убивает вражеского героя, убийца награждается надежным золотом используя следующую формулу:\n`110 + значение полосы убийств + (уровень вражеского героя × 8)`\n\nТакже убийство героя, имеющего серию убийств задет дополнительное золото убившему, равное `60 × (кол-во убийств - 2)`. Максимальная серия убийств - 10"},
                               'Укрепление строений':{"__Укрепление строений (Глиф)__":"Способность, которую может использовать любой игрок в команде. При использовании все союзные строения и линейные крипы команды становятся неуязвимыми к урону на 6 секунд. Перезарядка способности - 300 секунд. \nИспользуется для прекращения осады или достаточной его задержки для организации контратаки. И наоборот, его можно использовать для осады, наложив защиту на союзных крипов в правильный момент.\n\nУкрепление строений может быть активировано любым игроком с помощью нажатия кнопки в правой части миникарты или горячей клавиши, закрепленной в настройках. Перезарядка распространяется на всех игроков в команде, это означает, что если один игрок активирует укрепление, то остальным придется ждать его перезарядки для повторного активирования. При этом, если 1-я башня разрушена, то перезарядка укрепления сбросится спустя 1 секунду."},
                               'Линии':{"__Линии__":"Дороги, соединяющие между собой две крепости. По линиям каждой стороны идут линейные крипы.\n\nВ игре есть три линии:\n"+u"\u2022"+"**Верхняя линия** / **top**, проходит вдоль левой и верхней части карты.\n"+u"\u2022"+"**Средняя линия** / **mid**, проходит посередине карты.\n"+u"\u2022"+"**Нижняя линия** / **bot**, проходит вдоль нижней и правой части карты.\n\nСуществуют также альтернативные названия для некоторых линий:\n"+u"\u2022"+"**Легкая линия** / **safe** / **short** — линейные крипы на этой линии находятся на близком расстоянии с первой башней. Для Сил Света, это нижняя линия. Для Сил Тьмы, верхняя. Название линии говорит само за себя, так как герою на линии легче отступить к союзной башне, что уменьшает шансы ганка из леса. Кроме того линия близка к лесу, что позволяет легко делать отводы крипов.\n"+u"\u2022"+"**Тяжёлая линия** / **hard** / **long** — линейные крипы на этой линии находятся на дальнем расстоянии с первой башней. Для Сил Света, это верхняя линия. Для Сил Тьмы, нижняя."},
                               'Лес':{"__Лес__":"Территория, располагающаяся между линиями с каждой стороны. В лесу находится 14 точек появления крипов: по 7 на каждой стороне. Из них по 6 точек появления обычных нейтральных крипов и по одной точке – древних крипов. При убийстве нейтральных крипов можно получить золото и опыт. Некоторые герои лучше получают золото и опыт в лесу, чем на линии. Такие герои относятся к роли **Лес**."},
                               'Руны':{u"\u2800"*24+"**__Руны__**":"*Существует два типа рун:*","**Руны богатства**":"Появляются каждые 5 минут, начиная с нулевой, в 4 точках карты, по 2 на половинах каждой фракции.\n\n<a:Emoticon_bountyrune:594813355303239700>**Руна богатства**: Даёт команде золото.\n В начале игры каждая руна даёт 40 золота. Начиная с 5 минуты игры, даёт +2 в минуту золота.","**Руны усиления**":"Появляются каждые 2 минуты в одном из двух мест на реке. С 40 минуты появляются в двух местах\n\n"+u"\u2022"+" <a:Emoticon_doubledamage:594813356964052993>**Руна двойного урона**: На 45 секунд даёт герою 100% дополнительного урона.\n"+u"\u2022"+" <a:Emoticon_illusion:594813357412843531>**Руна иллюзий**: Создаёт 2 иллюзии героя.\n"+u"\u2022"+" <a:Emoticon_invisbility:594813359174713344>**Руна невидимости**: Делает героя невидимым через 2 секунды после использования руны. Длится 45 секунд.\n"+u"\u2022"+" <a:Emoticon_regeneration:594813360264970260>**Руна регенерации**: Постепенно восстанавливает здоровье и ману героя. Пропадает, если герой получает урон. Действует 30 секунд.\n"+u"\u2022"+" <a:Emoticon_haste:594813358432190464>**Руна ускорения**: Позволяет герою перемещаться на скорости 550 и даёт иммунитет к любому замедлению. Действует 22 секунды.\n"+u"\u2022"+" <a:Emoticon_arcane:594823389001023501>**Руна волшебства**: Уменьшает время перезарядки способностей на 30% и затраты маны на 30%. Действует 50 секунд."}},
                        'Игровой процесс':{'Добивание':{"__Добивание (анг. Denying, рус. Денай)__":"Процесс добивания союзных крипов, героев, самого себя, башен с целью не дать это сделать врагу. За добивание, враги не получают золото. Враги получают уменьшенный опыт, если юнит не управляется игроком, и не получают опыт, если юнитом управлял игрок. Добить союзника можно только тогда, когда его здоровье ниже определенного порога: для крипов, не-героев и иллюзий этот порог 50% от полного здоровья, для героев 25%, для башен 10%.\n\nНа линейной стадии, добивание союзных линейных крипов является особенно важным, чтобы создать преимущество в виде золота и опыта. Это может привести к уровневому преимуществу над врагом, давая шанс убить его. В плане золота, добивание существенно вредит фарму врага, существенно замедляя его, если он зависит от фарма золота. Крипы должны добиваться всегда когда это возможно, однако добивание вражеских крипов является приоритетом. Добивание крипов также важно для поддержания баланса в их нахождении ближе к своей башне и дальше от вражеской.","Добивание героев":"Герои также могут быть добиты, находясь под действием некоторых способностей, либо герой может заденаиться об нейтрального крипа (или Рошана), если последний удар сделает нейтральный юнит. Добивание союзника не даст врагу получить золото и часть опыта за убийство. Однако, добитый герой все равно потеряет золото.\n\nГерой у которого меньше 25% здоровья может быть добит союзником, если он находится под действием этих заклинаний:\n"+u"\u2022"+" Doom героя <:doom:553950717245915136>Doom\n"+u"\u2022"+" Shadow Strike героя <:qp:553951283481018378>Queen of Pain\n"+u"\u2022"+" Venomous Gale героя <:venomancer:553951535474933782>Venomancer\n"+u"\u2022"+" Во время способности  Supernova, <:phoenix:553951283497664527>Phoenix может быть добит, если здоровье солнца меньше 50%.","Добивание себя / самоубийство":"Также возможно добить самого себя (совершить самоубийство) с помощью этих способностей:\n"+u"\u2022"+" Rot <:pudge:553951284454227968>Pudge\n"+u"\u2022"+" Blast Off! <a:miner:563374310572425225>Techies\n"+u"\u2022"+" Unstable Concoction <:alchemist:553950517324152863>Alchemist\n"+u"\u2022"+" Mist Coil <:abaddon:553950496516341783>Abaddon\n"+u"\u2022"+" Life Drain <:pugna:553951283158056962>Pugna при применении на союзника","Дополнительно":"Также еще некоторыми способностями можно добить союзного юнита:\n"+u"\u2022"+" Return <:centaur:553950671464955945>Centaur Warrunner реагирует на союзные атаки, засчитывая смерть от урона как добивание.\n"+u"\u2022"+" Holy Persuasion героя <:chen:553950671280406528>Chen, Enchant героя <:encha:553950883595943947>Enchantress, Control героя <:lifestealer:553950961169596417>Lifestealer и Dominate предмета Helm of the Dominator могут быть использованы на вражеском крипе с дальним типом атаки, который уже атакует героя, но снаряд еще не долетел до него. Если эта атака убьет героя, когда крип будет уже приручен, произойдет добивание.\n"+u"\u2022"+" Иллюзия Vengeance Aura <:venga:553951535789244432>Vengeful Spirit также может атаковать и добивать подходящих союзных юнитов.\n"+u"\u2022"+" False Promise <:oracle:553951283262914591>Oracle, при применении на союзника под действием Winter's Curse <:ww:553951535831318558>Winter Wyvern денаит союзника если урона достаточно."},
                                           'Избегание':{'__Избегание__':"Минование попадения тех или иных снарядов или способностей. Избегание происходит в момент, когда снаряд перестает считать юнита, бывшего целью заклинания или атаки, досягаемым. Когда снаряд не достигает цели, его называют промахнувшимся.\n\nИзбегание само по себе не является эффектом или заклинанием, оно служит вторичным эффектом от других способностей.\n\nСамые обычные формы избегания это блинк и вхождение в невидимость. Попадения не всех снарядов можно избежать, и не все типы соответствующих способностей могут не попасть."},
                                           'Развеивание':{"__Развеивание__":"Термин использующийся для принудительного снятия эффектов статуса. Развеивание само по себе не является эффектом или заклинанием, оно служит вторичным эффектом от других способностей.","Механика":"Развеивание убирает эффекты состояния основываясь на том, кто применивший юнит - союзник или враг, и какой эффект состояния, позитивный или негативный. Применение развеивания на союзного юнита убирает только негативные эффекты (также известны как дебаффы). Позитивные эффекты (также известны как баффы) никогда не убираются. И наоборот, применения развеивания на вражеского юнита уберет только баффы, дебаффы не будут убраны.\n\nЕсть 3 разных вариации развеивания: **базовое развеивание**, **сильное развеивание** и **смерть**.\n Если эффект состояния можно развеять, то об этом указано в описании способности, накладывающей этот эффект состояния, вместе с обозначением типа развеивания способного это сделать"},
                                           'Ганк':{"__Ганк__":"Способ активного перемещения по карте, целью которого является внезапное нападение на ничего не подозревающего вражеского героя.\n\nВ ганке могут участвовать как несколько, так и один герой. Успешность ганка зависит от нескольких факторов – наличия у ганкера дизейблов (способностей или предметов), показателя его урона и, конечно же, от мастерства ганкера. Успешным считается ганк, результатом которого стало убийство одного или нескольких героев.","Преимущества ганка":"Ганк в основном используется для получения общего преимущества команды в игре. Убив нескольких героев во время ганка, вы замедляете их прокачку. Часто основной целью ганка являются керри герои, способные на поздних этапах игры уничтожить всё живое на карте. Успешный ганк значительно замедлит прокачку вражеского хард-керри героя, поможет команде выиграть тяжёлую линию, обеспечит возможность для пуша башни или убийства Рошана.\n\nРанние ганки особенно важны, если команда противника будет сильнее на поздних стадиях игры. В таком случае вам нужно как можно раньше начать пушить линии и мешать качаться керри героям противника. Добравшись как можно раньше к базе врага, вы лишите его прокачки, без которой керри не смогут реализовать свой потенциал и для них игра закончится, так и не начавшись.\n\nИногда ганк используется как противодействие пушу врага. Когда враг пушит вашу линию, он отходит от своей вышки и становится более уязвим, тут его и можно подловить, зайдя, например, в спину."},
                                           'Агрессия':{u"\u2800"*20+"**__Агрессия__**":"Агрессия, или Харас, представляет собой процесс периодического нанесения повреждений вражеским героям, против которых вы стоите на линии. Так вражеский герой будет получать меньше золота и опыта, он будет терять дополнительное время, возвращаясь к своему фонтану для регенерации. В дополнение ко всему героя с не полным запасом здоровья будет проще ганкать вашим союзникам.","Способы агрессии":"Наиболее распространенной формой агрессии является нанесение урона вражескому герою физическими атаками. Это особенно легко сделать, если ваш герой дальнего боя (с большой дальностью атаки, позволяющей дольше преследовать и атаковать цель), а вражеские герои или герои ближнего боя или имеют низкую дальность атаки. Стоит помнить, что атакуя вражеского героя, вы будете привлекать внимание вражеских крипов. Это значит, что вражеские крипы, находящиеся поблизости, будут атаковать вас.\n\nВ то же время, ручное использование модификаторов атаки, таких как Poison Attack <:viper:553951535852290048>Viper'а или Burning Spear <:huskar:553950961195024434>Huskar'а не будет привлекать внимание вражеских крипов, что делает модификаторы чрезвычайно мощными для агрессии.",u"\u2800":"Большинство способностей наносящих урон можно использовать в качестве хараса практически постоянно, ведь они являются особенно эффективными, поскольку не вызывают внимания у вражеских крипов. В особенности замедляющие способности, такие как  Crystal Nova героя <:cm:553950671427076125>Crystal Maiden подходят для хараса, потому что они позволяют нанести больше ударов отступающему противнику, а также у них маленькая стоимость в мане, например как у  Rocket Flare <:cloclwerk:553950671100051487>Clockwerk'а. Опытные игроки обычно совмещаю эту технику с фармом: применяют способности по области на крипов, при этом стараются задеть ею врага.","Противодействия агрессии":"Получение физического урона можно снизить предметами, которые дают блокировку урона, регенерацию здоровья или броню. А такой предмет как Stout Shield, в сочетании с Ring of Health может сделать героя почти невосприимчивым к регулярному харасу.\n\nПостоянный харас способностями можно смягчить покупкой Magic Stick или Magic Wand, поскольку каждое применение способностей будет набирать заряды предмету, что обеспечит владельцу стабильное получение маны и здоровья.\n\nНекоторые герои обладают способностями, позволяющими спокойно выдерживать харас врага. Это способности дают герою дополнительную регенерацию здоровья, дополнительную броню, возможность уклониться от атак и т.д. (например, Dragon Blood и Blur)\n\nВ некоторых ситуациях на линии, лучше вызвать небольшой переполох и попытаться убить вражеского героя, а не просто пассивно позволить противнику получить господство на линии постоянным харасом."},
                                           'Передача предметов':{"__Передача предметов__":"Большинство предметов в Dota 2 не могут использоваться другими игроками. Герой, купивший предмет, считается его владельцем, и только он может использовать, продавать или улучшать купленный предмет.\n\nНо при этом большинство расходуемых предметов полностью передаваемые, поскольку их нельзя улучшить и они дают временные эффекты. Также эти предметы могут использовать герои, не приобретавшие их. Эта особенность позволяет героям поддержки покупать предметы и делиться ими с командой. \n\n Помимо расходуемых предметов, полностью передаваемым предметом является Bottle"},
                                           'Отводы и стаки крипов':{"__Стак крипов__":"Нагромождение крипов (Двойной\множественный лагерь (стак) нейтральных крипов) — это процесс взаимодействия с нейтральными крипами, во время которого вы отводите нейтралов с их лагеря перед новой волной возрождения. Нагромождая один и тот же лагерь, герой сможете существенно увеличить количество крипов в нём, что в дальнейшем позволит заработать больше золота и опыта на одном месте за короткий промежуток времени.\n\nЕсли вы хотите отвести нейтральных монстров к вашим союзным войскам, рекомендуется перед этим сделать хотя бы одно нагромождение лагеря.","__Отвод крипов__":"Отвод крипов (пул) — это процесс взаимодействия с нейтральными монстрами, во время которого вы вынуждаете их отойти от лагеря и вступить в драку с крипами ближайшей линии. Отводы делаются для замедления прокачки противника на линии и облегчение прокачки союзника.\n\nСоюзные войска появляются за своими казармами (если те не уничтожены) или с вершин ведущих на базу уклонов (если казармы уничтожены) каждые 30 секунд. Первая волна союзных войск состоит из трёх воинов ближнего боя и одного воина дальнего боя. Появившись на базе, крипы сразу же начинают идти по своей линии в направлении базы противника. У них есть определенная зона обзора: увидев героя противника или вражеских крипов, они нападают и будут вести бой или догонять врага, пока тот не умрет либо не пропадет из их зоны видимости."},
                                           'Псевдослучайное распределение':{"__Псевдослучайное распределение__":"Статистический показатель, отвечающий за вероятность срабатывания определенных эффектов у способностей и предметов. В истинно случайном распределении, каждый 'ролл' работает независимо, но в ПСР шанс срабатывания эффекта увеличивается каждый раз, когда он не сработал. В результате, срабатывание происходит более последовательно. В целом ПСР применяется к следующим типам способностей: Критический удар, Оглушающий удар, Блокировка урона, Chain Lightning, Greater Bash.","Суть работы":"Для каждого отдельного случая (удара, способности), который может вызвать эффект, ПСР увеличивает вероятность срабатывания этого эффекта при следующем случае на константу С, при условии, что n предыдущих атак этот эффект не срабатывал. Эта константа С, которая так же входит в расчет начальной вероятности, меньше, чем вероятность, указанная в описании. Как только эффект сработал, счетчик обновляется.\nНапример, у способности __Bash of the Deep__ <:slardar:553951283711574037>Slardar шанс срабатывания 25%. Однако, при первой атаке шанс на срабатывание эффекта всего ~8,5%. На следующей атаке шанс составляет уже ~17%, на третьей примерно 25% и так далее. После того, как __Bash of the Deep__ прошёл, счетчик обновляется и шанс опять становится ~8,5%. Поэтому, при сложении вероятностей, средний шанс на срабатывание способности на определённом отрезке времени будет примерно 25%","<a:note:595915864231116801> Примечание":"Теоретически, возможно увеличить шанс оглушающего или критического удара при следующей атаки, атакуя крипов без срабатывания ПСР, но на практике это сделать практически невозможно. Отметим, что при атаке существ, на которых не срабатывает эффект, вероятность выпадения эффекта при следующем ударе не увеличивается."},
                                           'Истинно случайное распределение':{"__Истинно случайное распределение__":"Описывает вероятность срабатывания случайного события, которое не является псевдо-случайным. В основном это относится к уклонению и ослеплению, также как и к большинству способностей, не наносящих урон или способностям не-героев.\n\n К способностям, использующим данный тип распределения, относятся Juxtapose <:pl:553951283468566539>Phantom Lancer, Multicast <:ogre:553951283581681694>Ogre Magi, Phantasm и Chaos Bolt <:ck:553950671699705856>Chaos Knight и все ослепляющие способности."}},
                        'Юниты':{'Строения':{"__Строения__":"Особый тип юнитов, неподконтрольный ни одному игроку. В начале каждого матча команды получают в распоряжение набор строений, появляющихся в заданных позициях. Обе фракции имеют одинаковый набор, отличающийся лишь визуально. Строения в большинстве своём выполняют защитную функцию и являются главной целью игры.\n\nВсе строения имеют схожие базовые характеристики. Они обладают иммунитетом к большинству заклинаний (который обходят лишь некоторые из них). При уничтожении некоторые строения дают золото уничтожившей их команде и награждают дополнительным игрока, нанесшего последний удар. При уровне здоровья ниже 10% строения (кроме Крепости) можно добить, чтобы не дать награду вражеской команде. Строения не дают опыт. Уничтоженное здание не восстанавливается, пропадая до конца игры.\n\nКаждая сторона имеет по 29 зданий.","Башни":"Основная линия защиты для каждой команды, атакующая любого не-нейтрального врага в своем радиусе. Все три линии фракций защищены 3-мя башнями, а их крепости - 2-мя. Общее количество башен - 11.\n\n1-е башни неуязвимы на стадии подготовки до начала битвы. Каждая 2-я и 3-я башни неуязвимы, пока живы предшествующие им на линии башни. Обе 4-е башни неуязвимы, пока не будет уничтожена хотя бы одна 3-я башня. Казармы можно не уничтожать для лишения 4-х башен неуязвимости. Обе 4-е башни необходимо уничтожить, чтобы сделать уязвимой крепость.\n\n Атаку вражеской башни можно переключить с себя на союзного юнита, нажав на этого юнита.","Казармы":"Строения, защищаемые башнями 3-го уровня и отвечающие за равновесие в силе линейных крипов обеих фракций. На каждой линии находятся две казармы - одна для крипов ближнего боя (казарма мечников) , другая - для крипов дальнего боя (казарма магов). Казарма магов на всех линиях и для всех фракций всегда размещается слева от казармы мечников.\n\nКазармы неуязвимы до тех пор, пока башня 3-го уровня, защищающая их, не будет уничтожена. Потеря казарм не прервет появление линейных крипов. При этом их разрушение даст сломавшей команде суперкрипов для этой линии, более сильных, чем обычные крипы, и дающих меньше награды за убийство. Суперкрипы ближнего боя появляются при разрушении казармы мечников, а дальнего - при разрушении казармы магов. Если разрушены все 6 казарм противника, то на каждой линии начнут появляться мегакрипы, которые в разы сильнее суперкрипов. Казарма мечников регенирируется, поэтому в разных ситуациях нужно по-разному расставлять приорететы при атаке вражеских казарм","Защита от обхода":"Пассивная способность большинства строений. Только 1-я Башня и Фонтаны не имеют её. Будучи активной, способность защищает строения, вылечивая любой наносимый вражескими юнитами урон, тем самым усложняя их уничтожение. Эта защита отключается, когда вражеский линейный крип подходит к 2 башне или к базе противника. Крип не должен быть под контролем игрока, только контролируемые ИИ линейные крипы могут отключать её. После отключения повторная активация проходит с задержкой."},
                                 'Курьеры':{"__Курьер__":"Юнит, который приносит предметы из лавок героям. Пеший Animal Courier может быть призван для команды покупкой Animal Courier. Он автоматически улучшается ровно на 3 минуте до Flying Courier. Может быть только один курьер для каждой команды. Каждый игрок может отдавать приказы курьеру, которые отменяются при новом приказе, если только приказы не были поставлены в очередь действий.","Инвентарь":"Как и герой, курьер имеет 6 ячеек в инвентаре и 3 в рюкзаке. Также есть ограничения. Почти каждый предмет теряет свои способности в инвентаре курьера, делая все их характеристики и способности отключенными и недоступными в использовании для курьера. Отключенные предметы затемнены в инвентаре.\n"+u"\u2022"+" Курьер может использовать Tango (не свой), Cheese и Refresher Shard.\n"+u"\u2022"+" Курьер получает регенерацию здоровья от Ring of Regen, Ring of Health и Perseverance.\n"+u"\u2022"+" Курьер не может устанавливать или делиться вардами\n"+u"\u2022"+" Курьер может активировать Dust of Appearance и Smoke of Deceit, но последний предмет на него не действует.\n"+u"\u2022"+" Gem of True Sight, и Divine Rapier выпадают с Flying Courier после его смерти."},
                                 'Линейные крипы':{"__Линейные крипы__":"Тип крипов неподконтрольных никакому игроку. Эти крипы появляются маленькими группами (называемыми «волнами крипов») у обоих фракций, на каждой из 3 линий возле казарм каждые полминуты, начиная со старта битвы. Они постоянно продвигаются в сторону вражеской им базы, двигаясь по стандартному пути по линии на которой появились. На своем пути они атакуют вражеских или нейтральных крипов в радиусе агрессии.","Время появления":"Линейные крипы первый раз появляются на отметке игрового таймера в 00:00, сразу после звука игрового рога. После этого, они будут появляться каждые 30 секунд. В отличии от крипов-мечников и крипов-магов, катапульты начинают появляться на 11-й волне, и после каждые 10 волн. Это значит что катапульты появляются каждые 5 минут, впервые появившись на 5:00.","Поведение":"Линейные крипы имеют установленный путь с которого они не должны сходить при нормальных условиях. Крипы агрессивны когда идут по линии, то есть атакуют любого врага в дальности их обнаружения. Если линейный крип будет спровоцирован, он последует за спровоцировавшим его юнитом пока тот не умрет, или пока он не потеряет его след, или пока другой враг не попадет в дальность обнаружения и снимет провокацию. Если спровоцировавший враг войдет в туман войны, линейный крип пойдет в последнюю точку где видел врага. Если он вновь не увидит врага, он вернется на точку на линии с которой ушел. Если спровоцировавший юнит вне дальности обнаружения линейного крипа, он будет следовать за ним 2,3 секунды до того как вернется на свою линию. Крип который более не спровоцирован не присоединится к другим линиям даже если они ближе. \n<a:note:595915864231116801>*Данная манера поведения не распространяется на первую волну крипов: они двигаются до встречи со вражескими линейными крипами, игнорируя все прочие юниты*"},
                                 'Нейтральные крипы':{"__Нейтральные крипы__":"Тип крипов неподконтрольных никакому игроку. Они не пренадлежат никакой из команд, и являются альтернативным источником золота и опыта. Нейтральные крипы появляются в маленьких лагерях разбросанных по лесу с обеих сторон на карте. Они имеют силу разного уровня и большинство из них имеют уникальные способности. Рошан, который находится в своем логове на реке, также считается нейтральным крипом.\n\nНейтральные крипы дают больше золота и опыта, так как награда за их убийство растёт с течением игры, схоже с тем как усиливаются линейные крипы. Каждые 7 минут и 30 секунд, награда за убийство всех нейтральных крипов (включая Рошана) увеличивается на 2%.\n\nПервые нейтральные крипы появляются каждую минуту ,начиная с первой(1:00 игрового времени). Лагерь крипов не может повторить появление одних и тех же нейтралов несколько раз подряд.\n\nВ основном, нейтралы просто стоят в своих лагерях, ничего не делая. Они лишь сражаются, когда спровоцированы."},
                                 'Рошан':{"__Рошан__":"Самый сильный нейтральный монстр в Dota 2. Он с легкостью одолевает большинство героев один на один. Игроки обычно ждут поздней фазы игры, когда фарм-герои соберут свои лучшие предметы, или пробуют убить его всей командой.","Логово Рошана":"Рошана можно найти в его логове, которое находится немного выше верхней руны. Вход соединен с рекой и повернут к югу. Рошан всегда стоит в конце логова если не атакует, и будет атаковать только если вражеские юниты подойдут к нему на расстояние 150 или нанесут урон с расстояния 1800. Рошан не может быть атакован вне логова;но сам может атаковать везде.\n\nЕдинственный способ получить обзор внутри логова — войти в него. Юниты с наземным обзором (включая варды и другие заклинания) из вне не могут видеть логово, не важно как близко их дальность обзора или если они на возвышености, например, на местах вардов. Варды не могут быть поставлены внутри логова. Юниты с летающим обзором могут видеть внутри логова даже если они вне его.","Смерть Рошана":"Каждый игрок убившей команды получает 150 надёжного золота. Герой который лично добил Рошана получит 150‒400 золота, в среднем получая 300–550 золота.\nПосле каждой смерти из Рошана всегда выпадает Aegis of the Immortal, непередаваемый предмет при поднятии, который дает владельцу вторую жизнь, реинкарнируя после смерти с задержкой в 5 секунд на месте смерти. Если носитель Aegis of the Immortal не умрёт в течении 5 минут после поднятия, он пропадёт из инвентаря и полностью восстановит здоровье и ману за краткий период времени. Восстановление отменяется при получении любого урона свыше 20, включая урон самому себе. Если Aegis of the Immortal не был подобран и был оставлен на земле, он исчезнет при возрождении Рошана.\nAegis of the Immortal может быть украден игроком команды, не совершившей убийство Рошана. Его также можно добить обычной атакой.",u"\u2800":"После второй смерти Рошана и следующие разы, с него также выпадает Cheese, передаваемый расходуемый предмет, который может быть продан за 500 золота игроком который первым его поднимет, или использован для мгновенного восстановления здоровья и маны. Как и Aegis, Cheese может также подобрать каждый. После третьей смерти Рошана с него может выпасть Aghanim's Scepter (Consumable) или Refresher Shard, передаваемый предмет, можно продать за 500 золота, при использовании сбрасывает перезарядки способностей и предметов, не тратит ману. При выделении Рошана можно узнать, какой именно предмет выпадет после его смерти. После четвёрой смерти Рошана и следующие разы, с него гарантировано выпадает Aghanim's Scepter (Consumable) и Refresher Shard.","Возрождение Рошана":"Рошан возрождается как и другие нейтральные монстры, однако не в фиксированный момент времени, а через 8-11 минут после своей смерти (время выбирается случайным образом). Воскрешение Рошана невозможно предотвратить(в отличие от остальных нейтральных монстров), установив варды и/или стоя в месте его воскрешения."}}}}

'''
with open('dotabase/tome.txt', 'w', encoding='utf-8') as f:
    f.write(str(dota_mechanics))
'''

updatepatchnotes()

updateitems_no_als()
updateabils()
updateheroes()
#updateversion()








