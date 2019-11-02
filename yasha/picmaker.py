from PIL import Image, ImageDraw,ImageColor,ImageFont
import requests
import json
import glob, os
import random
from tools import get_duration

def chalstars(stars):
    starsimg=Image.open(f"dotabase/emoticons/{stars}star.png")
    starsimg.save(f'{stars}star.png','PNG')
    
def itempic(itemid):
    itemimg=Image.open(f"dotabase/items/{itemid}.png")
    itemimg.save(f'{itemid}.png','PNG')
    
def makerang(rank):
    ranktemplate=Image.open(f"dotabase/ranks/{rank}.png")
    if rank!="81":
        ranktemplate.save(f'{rank}.png','PNG')
    else:
        print(80)


def ban(heroname):
    heroimg="dotabase/hero_icons/{}.png".format(heroname)
    heroicon=Image.open(heroimg)
    heroicon = heroicon.convert("RGBA")
    draw = ImageDraw.Draw(heroicon)
    draw.line((0,0)+heroicon.size,fill="rgb(180,0,0)",width=3)
    heroicon.save(f'ban{heroname}.png')

def makeplayerslots(player,stratz):  
    inv=Image.open("dotabase/inventory.png")
    inv=inv.convert("RGBA")
    slots={}
    variables={'od':{'match_id':'match_id',
               "player_slot":"player_slot",
               'item_0':'item_0',
               'item_1':'item_1',
               'item_2':'item_2',
               'item_3':'item_3',
               'item_4':'item_4',
               'item_5':'item_5',
               'backpack_0':'backpack_0',
               'backpack_1':'backpack_1',
               'backpack_2':'backpack_2'},
     'stratz':{'match_id':'matchId',
               "player_slot":"playerSlot",
               'item_0':'item0Id',
               'item_1':'item1Id',
               'item_2':'item2Id',
               'item_3':'item3Id',
               'item_4':'item4Id',
               'item_5':'item5Id',
               'backpack_0':'backpack0Id',
               'backpack_1':'backpack1Id',
               'backpack_2':'backpack2Id'}}
    if stratz:
        var=variables['stratz']
    else:
        var=variables['od']
    for i in range(6): #main slots
        try:
            item=Image.open("dotabase/items/{}.png".format(player[var[f"item_{i}"]]))
        except:
            if player.get(f"item_{i}",0)!=0:
                item=Image.open("dotabase/items/recipe.png")
            else:
                item=None
        slots[f"item_{i}"]=item
    for i in range(3): #backpack
        try:
            item=Image.open("dotabase/items/{}.png".format(player[var[f"backpack_{i}"]]))
        except:
            if player.get(f"backpack_{i}",0)!=0:
                item=Image.open("dotabase/items/recipe.png")
            else:
                item=None
        slots[f"backpack_{i}"]=item
    if slots["item_0"]!=None:
        inv.paste(slots["item_0"],(8,12,93,76))
    if slots["item_1"]!=None:
        inv.paste(slots["item_1"],(101,12,186,76))        
    if slots["item_2"]!=None:
        inv.paste(slots["item_2"],(193,12,278,76))
    if slots["item_3"]!=None:
        inv.paste(slots["item_3"],(8,83,93,147))
    if slots["item_4"]!=None:
        inv.paste(slots["item_4"],(101,83,186,147))
    if slots["item_5"]!=None:
        inv.paste(slots["item_5"],(193,83,278,147))
    if slots["backpack_0"]!=None:
        slots["backpack_0"]=slots["backpack_0"].convert("L")
        slots["backpack_0"]=slots["backpack_0"].crop((1,6,82,57))
        inv.paste(slots["backpack_0"],(8,161,89,212))
    if slots["backpack_1"]!=None:
        slots["backpack_1"]=slots["backpack_1"].convert("L")
        slots["backpack_1"]=slots["backpack_1"].crop((1,6,82,57))
        inv.paste(slots["backpack_1"],(100,161,181,212))
    if slots["backpack_2"]!=None:
        slots["backpack_2"]=slots["backpack_2"].convert("L")
        slots["backpack_2"]=slots["backpack_2"].crop((1,6,82,57))
        inv.paste(slots["backpack_2"],(193,161,274,212))


    inv.resize((int(inv.width*0.75),int(inv.height*0.75)))
    inv.save("inventory{0}_{1}.png".format(player[var["match_id"]],player[var["player_slot"]]),"PNG")
        

def makeadvgraph(duration,gold_adv,xp_adv,matchid):

    #данные о матче
    adv_by_min=gold_adv
    times=[]
    for i in range(duration//60):
        times.append(60*i)
    #прод-ть матча строкой 
    end=get_duration(duration)

    #макс т мин преимущества в ед. золота и координата Y на шаблоне графика через которую проводится ось абсцисс
    mx=max(adv_by_min)
    mn=min(adv_by_min) 
    sm=abs(mx)+abs(mn)
    y=mx/sm*200+1
    
    tens=[] ###каждая 10 минута
    for el in times:
        if el//60%10==0:
            tens.append(str(el//60)+":00")
    tenkradiant=[] ###каждые 10к преимущества сил света
    tenkint=10000
    while tenkint<=abs(mx):
        tenkradiant.append(tenkint)
        tenkint+=10000
    tenkdire=[] ###каждые 10к преимущества сил тьмы
    tenkint=10000
    while tenkint<=abs(mn):
        tenkdire.append(tenkint)
        tenkint+=10000
    
    #создание картинки    
    font = ImageFont.truetype(r"C:\WINDOWS\Fonts\arialbd.ttf", 10)
    img=Image.open("dotabase/graphT.png")
    draw = ImageDraw.Draw(img)

    #####создание графика(оси,значения)
    draw.line([(400,0),(400,200)],fill="rgb(83,143,12)",width=2)
    draw.line([(0,0),(400,0)],fill="rgb(83,143,12)",width=1)
    draw.line([(0,200),(400,200)],fill="rgb(83,143,12)",width=1)
    draw.line([(0,y),(400,y)],fill="rgb(83,143,12)",width=2)
    draw.text((367,2),str(abs(mx)),font=font,fill="rgb(255,255,255)")
    draw.text((367,188),str(abs(mn)),font=font,fill="rgb(255,255,255)")
    n=len(tens)
    for i in range(1,n+1):  #каждые 10 минут + время окончания матча
            pos=(i-1)/n*400
            draw.text((pos,208),"| {}".format(tens[i-1]),font=font,fill="rgb(255,255,255)")
    draw.text((400,208),"| {}".format(end),font=font,fill="rgb(255,255,255)")

    for i in range(1,len(tenkradiant)+1):  #каждые 10k преимущества radiant
            pos=y-y*(tenkradiant[i-1]/(abs(mx)+1))
            draw.text((367,pos),"{}".format(tenkradiant[i-1]),font=font,fill="rgb(255,255,255)")
            draw.line([(0,pos-1),(400,pos-1)],fill="rgba(83,143,12,100)",width=1)
    for i in range(1,len(tenkdire)+1):  #каждые 10k преимущества dire
            pos=y+(200-y)*(tenkdire[i-1]/(abs(mn)+1))
            draw.text((367,pos),"{}".format(tenkdire[i-1]),font=font,fill="rgb(255,255,255)") 
            draw.line([(0,pos-1),(400,pos-1)],fill="rgba(83,143,12,100)",width=1)
    
    #####создание ломаной значений gold
    x1,y1=0,y
    n=len(adv_by_min)
    for i in range(n):
        if adv_by_min[i]>=0:
            x2=i/(n-1)*400
            y2=y-y*(adv_by_min[i]/(abs(mx)+1))
            draw.line([(x1,y1),(x2,y2)],fill="rgb(238,227,43)",width=2)
            x1,y1=x2,y2
        else:
            x2=i/(n-1)*400
            y2=y+(200-y)*(abs(adv_by_min[i])/(abs(mn)+1))
            draw.line([(x1,y1),(x2,y2)],fill="rgb(238,227,43)",width=2)
            x1,y1=x2,y2

    #####создание ломаной значений exp
    x1,y1=0,y
    exp_by_min=xp_adv
    n=len(exp_by_min)
    mx=max(exp_by_min)
    mn=min(exp_by_min)
    for i in range(n):
        if exp_by_min[i]>=0:
            x2=i/(n-1)*400
            y2=y-y*(exp_by_min[i]/(abs(mx)+1))
            draw.line([(x1,y1),(x2,y2)],fill="rgb(74,247,208)",width=2)
            x1,y1=x2,y2
        else:
            x2=i/(n-1)*400
            y2=y+(200-y)*(abs(exp_by_min[i])/(abs(mn)+1))
            draw.line([(x1,y1),(x2,y2)],fill="rgb(74,247,208)",width=2)
            x1,y1=x2,y2
    img.save("adv_graph{}.png".format(matchid),"PNG")

    
def makemap(matchinfo):
        
    radtower=str(bin(matchinfo["tower_status_radiant"]))
    radtower=radtower[2:]
    while len(radtower)<11:
        radtower='0'+radtower

    diretower=str(bin(matchinfo["tower_status_dire"]))
    diretower=diretower[2:]
    while len(diretower)<11:
        diretower='0'+diretower
    
    direbar=str(bin(matchinfo['barracks_status_dire']))
    direbar=direbar[2:]
    while len(direbar)<6:
        direbar='0'+direbar
    
    radbar=str(bin(matchinfo['barracks_status_radiant']))
    radbar=radbar[2:]
    while len(radbar)<6:
        radbar='0'+radbar

    win=matchinfo["radiant_win"]

#######    
    im=Image.open("dotabase/map_720.jpg")
    draw = ImageDraw.Draw(im)
    direlosefill="rgb(125,0,0)"
    direloseoutline="rgb(0,0,0)"

    radiantlosefill="rgb(0,125,0)"
    radiantloseoutline="rgb(0,0,0)"

########  постройки
    #Dire tron
    if win==False:
        draw.polygon([565, 91, 594, 111, 594, 96, 565, 76], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([594, 111, 613, 97, 613, 82,  594, 96], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([ 565, 76, 594, 96,613, 82, 585, 63], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([565, 91, 594, 111, 594, 96, 565, 76], fill=direlosefill,outline=direloseoutline)
        draw.polygon([594, 111, 613, 97, 613, 82,  594, 96], fill=direlosefill,outline=direloseoutline)
        draw.polygon([ 565, 76, 594, 96,613, 82, 585, 63], fill=direlosefill,outline=direloseoutline)

        
    #Bottom Ranged
    if direbar[0]=="1":
        
        draw.polygon([594, 198, 594, 192, 599, 197, 599, 203], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([599, 203, 604, 198, 604, 192, 599, 197], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([594, 192, 599, 197, 604, 192, 599, 188], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([594, 198, 594, 192, 599, 197, 599, 203], fill=direlosefill,outline=direloseoutline)
        draw.polygon([599, 203, 604, 198, 604, 192, 599, 197], fill=direlosefill,outline=direloseoutline)
        draw.polygon([594, 192, 599, 197, 604, 192, 599, 188], fill=direlosefill,outline=direloseoutline)
        
    #Bottom Melee
    if direbar[1]=="1":    
        draw.polygon([623, 198, 623, 192, 628, 197, 628, 203], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([628, 203, 633, 198, 633, 192, 628, 197], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([623, 192, 628, 197, 633, 192, 628, 188], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([623, 198, 623, 192, 628, 197, 628, 203], fill=direlosefill,outline=direloseoutline)
        draw.polygon([628, 203, 633, 198, 633, 192, 628, 197], fill=direlosefill,outline=direloseoutline)
        draw.polygon([623, 192, 628, 197, 633, 192, 628, 188], fill=direlosefill,outline=direloseoutline)
        
    #Middle Ranged
    if direbar[2]=="1":
        draw.polygon([512, 144, 512, 138, 517, 143, 517, 149], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([517, 149, 522, 144, 522, 138, 517, 143], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([512, 138, 517, 143, 522, 138, 517, 134], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([512, 144, 512, 138, 517, 143, 517, 149], fill=direlosefill,outline=direloseoutline)
        draw.polygon([517, 149, 522, 144, 522, 138, 517, 143], fill=direlosefill,outline=direloseoutline)
        draw.polygon([512, 138, 517, 143, 522, 138, 517, 134], fill=direlosefill,outline=direloseoutline)
        
    #Middle Melee
    if direbar[3]=="1":   
        draw.polygon([535, 163, 535, 157, 540, 162, 540, 168], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([540, 168, 545, 163, 545, 157, 540, 162], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([535, 157, 540, 162, 545, 157, 540, 153], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([535, 163, 535, 157, 540, 162, 540, 168], fill=direlosefill,outline=direloseoutline)
        draw.polygon([540, 168, 545, 163, 545, 157, 540, 162],fill=direlosefill,outline=direloseoutline)
        draw.polygon([535, 157, 540, 162, 545, 157, 540, 153], fill=direlosefill,outline=direloseoutline)
        
    #Top Ranged
    if direbar[4]=="1":
        draw.polygon([507, 56, 507, 50, 512, 55, 512, 61], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([512, 61, 517, 56, 517, 50, 512, 55], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([507, 50, 512, 55, 517, 50, 512, 46], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([507, 56, 507, 50, 512, 55, 512, 61], fill=direlosefill,outline=direloseoutline)
        draw.polygon([512, 61, 517, 56, 517, 50, 512, 55], fill=direlosefill,outline=direloseoutline)
        draw.polygon([507, 50, 512, 55, 517, 50, 512, 46], fill=direlosefill,outline=direloseoutline)
        
    #Top Melee
    if direbar[5]=="1":
        draw.polygon([507, 81, 507, 75, 512, 80, 512, 86], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([512, 86, 517, 81, 517, 75, 512, 80], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([507, 75, 512, 80, 517, 75, 512, 71], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([507, 81, 507, 75, 512, 80, 512, 86], fill=direlosefill,outline=direloseoutline)
        draw.polygon([512, 86, 517, 81, 517, 75, 512, 80], fill=direlosefill,outline=direloseoutline)
        draw.polygon([507, 75, 512, 80, 517, 75, 512, 71], fill=direlosefill,outline=direloseoutline)


    #Dire t4 bot
    if diretower[1]=="1":
        draw.polygon([550, 111, 550, 98, 558, 105, 558, 119], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([558, 119, 566, 111, 566, 98, 558, 105], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([558, 105, 550, 98, 558, 92, 566, 98], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([550, 111, 550, 98, 558, 105, 558, 119], fill=direlosefill,outline=direloseoutline)
        draw.polygon([558, 119, 566, 111, 566, 98, 558, 105], fill=direlosefill,outline=direloseoutline)
        draw.polygon([558, 105, 550, 98, 558, 92, 566, 98], fill=direlosefill,outline=direloseoutline)
    #Dire t4 top
    if diretower[0]=="1":
        draw.polygon([570, 125, 570, 112, 578, 119, 578, 133], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([578, 133, 586, 125, 586, 112, 578, 119], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([578, 119, 570, 112, 578, 106, 586, 112], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([570, 125, 570, 112, 578, 119, 578, 133], fill=direlosefill,outline=direloseoutline)
        draw.polygon([578, 133, 586, 125, 586, 112, 578, 119], fill=direlosefill,outline=direloseoutline)
        draw.polygon([578, 119, 570, 112, 578, 106, 586, 112], fill=direlosefill,outline=direloseoutline)
        
    #Dire Bottom Tier 3
    if diretower[2]=="1":
        draw.polygon([605, 203, 605, 190, 613, 196, 613, 211], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([613, 211, 621, 203, 621, 190, 613, 197], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([613, 197, 605, 190, 613, 184, 621, 190], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([605, 203, 605, 190, 613, 196, 613, 211], fill=direlosefill,outline=direloseoutline)
        draw.polygon([613, 211, 621, 203, 621, 190, 613, 197], fill=direlosefill,outline=direloseoutline)
        draw.polygon([613, 197, 605, 190, 613, 184, 621, 190], fill=direlosefill,outline=direloseoutline)
    #Dire Bottom Tier 2
    if diretower[3]=="1":
        draw.polygon([603, 290, 603, 277, 611, 284, 611, 298], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([611, 298, 619, 290, 619, 277, 611, 284], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([611, 284, 603, 277, 611, 271, 619, 277], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([603, 290, 603, 277, 611, 284, 611, 298], fill=direlosefill,outline=direloseoutline)
        draw.polygon([611, 298, 619, 290, 619, 277, 611, 284], fill=direlosefill,outline=direloseoutline)
        draw.polygon([611, 284, 603, 277, 611, 271, 619, 277], fill=direlosefill,outline=direloseoutline)
    #Dire Bottom Tier 1
    if diretower[4]=="1":
        draw.polygon([602, 422, 602, 409, 610, 416, 610, 430], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([610, 430, 618, 422, 618, 409, 610, 416], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([610, 416, 602, 409, 610, 403, 618, 409], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([602, 422, 602, 409, 610, 416, 610, 430], fill=direlosefill,outline=direloseoutline)
        draw.polygon([610, 430, 618, 422, 618, 409, 610, 416], fill=direlosefill,outline=direloseoutline)
        draw.polygon([610, 416, 602, 409, 610, 403, 618, 409], fill=direlosefill,outline=direloseoutline)
    #Dire Middle Tier 3
    if diretower[5]=="1":
        draw.polygon([515, 159, 515, 146, 523, 153, 523, 167], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([523, 167, 531, 159, 531, 146, 523, 153], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([523, 153, 515, 146, 523, 140, 531, 146], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([515, 159, 515, 146, 523, 153, 523, 167], fill=direlosefill,outline=direloseoutline)
        draw.polygon([523, 167, 531, 159, 531, 146, 523, 153], fill=direlosefill,outline=direloseoutline)
        draw.polygon([523, 153, 515, 146, 523, 140, 531, 146], fill=direlosefill,outline=direloseoutline)
    #Dire Middle Tier 2
    if diretower[6]=="1":
        draw.polygon([456, 223, 456, 210, 464, 217, 464, 231], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([464, 231, 472, 223, 472, 210, 464, 217], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([464, 217, 456, 210, 464, 204, 472, 210], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([456, 223, 456, 210, 464, 217, 464, 231], fill=direlosefill,outline=direloseoutline)
        draw.polygon([464, 231, 472, 223, 472, 210, 464, 217], fill=direlosefill,outline=direloseoutline)
        draw.polygon([464, 217, 456, 210, 464, 204, 472, 210], fill=direlosefill,outline=direloseoutline)

        
    #Dire Middle Tier 1
    if diretower[7]=="1":
        draw.polygon([354, 302, 354, 289, 362, 296, 362, 310], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([362, 310, 370, 302, 370, 289, 362, 296], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([362, 296, 354, 289, 362, 283, 370, 289], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([354, 302, 354, 289, 362, 296, 362, 310], fill=direlosefill,outline=direloseoutline)
        draw.polygon([362, 310, 370, 302, 370, 289, 362, 296], fill=direlosefill,outline=direloseoutline)
        draw.polygon([362, 296, 354, 289, 362, 283, 370, 289], fill=direlosefill,outline=direloseoutline)

        
    #Dire Top Tier 3
    if diretower[8]=="1":
        draw.polygon([488, 73, 488, 60, 496, 67, 496, 81], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([496, 81, 504, 73, 504, 60, 496, 67], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([496, 67, 488, 60, 496, 54, 504, 60], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([488, 73, 488, 60, 496, 67, 496, 81], fill=direlosefill,outline=direloseoutline)
        draw.polygon([496, 81, 504, 73, 504, 60, 496, 67], fill=direlosefill,outline=direloseoutline)
        draw.polygon([496, 67, 488, 60, 496, 54, 504, 60], fill=direlosefill,outline=direloseoutline)
    #Dire Top Tier 2
    if diretower[9]=="1":
        draw.polygon([329, 63, 329, 50, 337, 57, 337, 71], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([337, 71, 345, 63, 345, 50, 337, 57], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([337, 57, 329, 50, 337, 44, 345, 50], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([329, 63, 329, 50, 337, 57, 337, 71], fill=direlosefill,outline=direloseoutline)
        draw.polygon([337, 71, 345, 63, 345, 50, 337, 57], fill=direlosefill,outline=direloseoutline)
        draw.polygon([337, 57, 329, 50, 337, 44, 345, 50], fill=direlosefill,outline=direloseoutline)

        
    #Dire Top Tier 1
    if diretower[10]=="1":
        draw.polygon([128, 74, 128, 61, 136, 68, 136, 82], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([136, 82, 144, 74, 144, 61, 136, 68], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
        draw.polygon([136, 68, 128, 61, 136, 55, 144, 61], fill="rgb(255,0,0)",outline="rgb(125,0,0)")
    else:
        draw.polygon([128, 74, 128, 61, 136, 68, 136, 82], fill=direlosefill,outline=direloseoutline)
        draw.polygon([136, 82, 144, 74, 144, 61, 136, 68], fill=direlosefill,outline=direloseoutline)
        draw.polygon([136, 68, 128, 61, 136, 55, 144, 61], fill=direlosefill,outline=direloseoutline)


        
######################################


    #Radiant t4 Top
    if radtower[1]=="1":
        draw.polygon([85, 516, 85, 503, 93, 510, 93, 524], fill="rgb(0,255,0)",outline="green")
        draw.polygon([93, 524, 101, 516, 101, 503, 93, 510], fill="rgb(0,255,0)",outline="green")
        draw.polygon([93, 510, 85, 503, 93, 497, 101, 503], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([85, 516, 85, 503, 93, 510, 93, 524], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([93, 524, 101, 516, 101, 503, 93, 510], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([93, 510, 85, 503, 93, 497, 101, 503], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Radiant t4 Bottom
    if radtower[0]=="1":
        draw.polygon([105, 535, 105, 522, 113, 529, 113, 543], fill="rgb(0,255,0)",outline="green")
        draw.polygon([113, 543, 121, 535, 121, 522, 113, 529], fill="rgb(0,255,0)",outline="green")
        draw.polygon([113, 529, 105, 522, 113, 516, 121, 522], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([105, 535, 105, 522, 113, 529, 113, 543], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([113, 543, 121, 535, 121, 522, 113, 529], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([113, 529, 105, 522, 113, 516, 121, 522], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Radiant Bottom Tier 3
    if radtower[2]=="1":
        draw.polygon([169, 584, 169, 571, 177, 578, 177, 592], fill="rgb(0,255,0)",outline="green")
        draw.polygon([177, 592, 185, 584, 185, 571, 177, 578], fill="rgb(0,255,0)",outline="green")
        draw.polygon([177, 578, 169, 571, 177, 565, 185, 571], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([169, 584, 169, 571, 177, 578, 177, 592], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([177, 592, 185, 584, 185, 571, 177, 578], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([177, 578, 169, 571, 177, 565, 185, 571], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Radiant Bottom Tier 2
    if radtower[3]=="1":
        draw.polygon([316, 597, 316, 584, 324, 591, 324, 605], fill="rgb(0,255,0)",outline="green")
        draw.polygon([324, 605, 332, 597, 332, 584, 324, 591], fill="rgb(0,255,0)",outline="green")
        draw.polygon([324, 591, 316, 584, 324, 578, 332, 584], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([316, 597, 316, 584, 324, 591, 324, 605], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([324, 605, 332, 597, 332, 584, 324, 591], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([324, 591, 316, 584, 324, 578, 332, 584], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Radiant Bottom Tier 1
    if radtower[4]=="1":
        draw.polygon([565, 576, 565, 563, 573, 570, 573, 584], fill="rgb(0,255,0)",outline="green")
        draw.polygon([573, 584, 581, 576, 581, 563, 573, 570], fill="rgb(0,255,0)",outline="green")
        draw.polygon([573, 570, 565, 563, 573, 557, 581, 563], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([565, 576, 565, 563, 573, 570, 573, 584], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([573, 584, 581, 576, 581, 563, 573, 570], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([573, 570, 565, 563, 573, 557, 581, 563], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Radiant Middle Tier 3
    if radtower[5]=="1":
        draw.polygon([133, 495, 133, 482, 141, 489, 141, 503], fill="rgb(0,255,0)",outline="green")
        draw.polygon([141, 503, 149, 495, 149, 482, 141, 489], fill="rgb(0,255,0)",outline="green")
        draw.polygon([141, 489, 133, 482, 141, 476, 149, 482], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([133, 495, 133, 482, 141, 489, 141, 503], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([141, 503, 149, 495, 149, 482, 141, 489], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([141, 489, 133, 482, 141, 476, 149, 482], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Radiant Middle Tier 2
    if radtower[6]=="1":
        draw.polygon([202, 441, 202, 428, 210, 435, 210, 449], fill="rgb(0,255,0)",outline="green")
        draw.polygon([210, 449, 218, 441, 218, 428, 210, 435], fill="rgb(0,255,0)",outline="green")
        draw.polygon([210, 435, 202, 428, 210, 422, 218, 428], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([202, 441, 202, 428, 210, 435, 210, 449], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([210, 449, 218, 441, 218, 428, 210, 435], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([210, 435, 202, 428, 210, 422, 218, 428], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Radiant Middle Tier 1
    if radtower[7]=="1":
        draw.polygon([271, 373, 271, 360, 279, 367, 279, 381], fill="rgb(0,255,0)",outline="green")
        draw.polygon([279, 381, 287, 373, 287, 360, 279, 367], fill="rgb(0,255,0)",outline="green")
        draw.polygon([279, 367, 271, 360, 279, 354, 287, 360], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([271, 373, 271, 360, 279, 367, 279, 381], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([279, 381, 287, 373, 287, 360, 279, 367], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([279, 367, 271, 360, 279, 354, 287, 360], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Radiant Top Tier 3
    if radtower[8]=="1":
        draw.polygon([52, 454, 52, 441, 60, 448, 60, 462], fill="rgb(0,255,0)",outline="green")
        draw.polygon([60, 462, 68, 454, 68, 441, 60, 448], fill="rgb(0,255,0)",outline="green")
        draw.polygon([60, 448, 52, 441, 60, 435, 68, 441], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([52, 454, 52, 441, 60, 448, 60, 462], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([60, 462, 68, 454, 68, 441, 60, 448], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([60, 448, 52, 441, 60, 435, 68, 441], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Radiant Top Tier 2
    if radtower[9]=="1":
        draw.polygon([59, 382, 59, 369, 67, 376, 67, 390], fill="rgb(0,255,0)",outline="green")
        draw.polygon([67, 390, 75, 382, 75, 369, 67, 376], fill="rgb(0,255,0)",outline="green")
        draw.polygon([67, 376, 59, 369, 67, 363, 75, 369], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([59, 382, 59, 369, 67, 376, 67, 390], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([67, 390, 75, 382, 75, 369, 67, 376], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([67, 376, 59, 369, 67, 363, 75, 369], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Radiant Top Tier 1
    if radtower[10]=="1":
        draw.polygon([60,232,60,219,68,226,68,240], fill="rgb(0,255,0)",outline="green")
        draw.polygon([68,240,76,232,76,219,68,226], fill="rgb(0,255,0)",outline="green")
        draw.polygon([68,226,60,219,68,213,76,219], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([60,232,60,219,68,226,68,240], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([68,240,76,232,76,219,68,226], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([68,226,60,219,68,213,76,219], fill=radiantlosefill,outline=radiantloseoutline)

        


    #Bottom Ranged
    if radbar[0]=="1":
        draw.polygon([156, 571, 156, 565, 161, 570, 161, 576], fill="rgb(0,255,0)",outline="green")
        draw.polygon([161, 576, 166, 571, 166, 565, 161, 570], fill="rgb(0,255,0)",outline="green")
        draw.polygon([156, 565, 161, 570, 166, 565, 161, 561], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([156, 571, 156, 565, 161, 570, 161, 576], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([161, 576, 166, 571, 166, 565, 161, 570], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([156, 565, 161, 570, 166, 565, 161, 561], fill=radiantlosefill,outline=radiantloseoutline)


        
    #Bottom Melee
    if radbar[1]=="1":
        draw.polygon([156, 592, 156, 586, 161, 591, 161, 597], fill="rgb(0,255,0)",outline="green")
        draw.polygon([161, 597, 166, 592, 166, 586, 161, 591], fill="rgb(0,255,0)",outline="green")
        draw.polygon([156, 586, 161, 591, 166, 586, 161, 582], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([156, 592, 156, 586, 161, 591, 161, 597], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([161, 597, 166, 592, 166, 586, 161, 591], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([156, 586, 161, 591, 166, 586, 161, 582], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Middle Ranged
    if radbar[2]=="1":
        draw.polygon([117, 491, 117, 485, 122, 490, 122, 496], fill="rgb(0,255,0)",outline="green")
        draw.polygon([122, 496, 127, 491, 127, 485, 122, 490], fill="rgb(0,255,0)",outline="green")
        draw.polygon([117, 485, 122, 490, 127, 485, 122, 481], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([117, 491, 117, 485, 122, 490, 122, 496], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([122, 496, 127, 491, 127, 485, 122, 490], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([117, 485, 122, 490, 127, 485, 122, 481], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Middle Melee
    if radbar[3]=="1":
        draw.polygon([138, 509, 138, 503, 143, 508, 143, 514], fill="rgb(0,255,0)",outline="green")
        draw.polygon([143, 514, 148, 509, 148, 503, 143, 508], fill="rgb(0,255,0)",outline="green")
        draw.polygon([138, 503, 143, 508, 148, 503, 143, 499], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([138, 509, 138, 503, 143, 508, 143, 514], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([143, 514, 148, 509, 148, 503, 143, 508], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([138, 503, 143, 508, 148, 503, 143, 499], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Top Ranged
    if radbar[4]=="1":
        draw.polygon([43, 465, 43, 459, 48, 464, 48, 470], fill="rgb(0,255,0)",outline="green")
        draw.polygon([48, 470, 53, 465, 53, 459, 48, 464], fill="rgb(0,255,0)",outline="green")
        draw.polygon([43, 459, 48, 464, 53, 459, 48, 455], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([43, 465, 43, 459, 48, 464, 48, 470], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([48, 470, 53, 465, 53, 459, 48, 464], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([43, 459, 48, 464, 53, 459, 48, 455], fill=radiantlosefill,outline=radiantloseoutline)

        
    #Top Melee
    if radbar[5]=="1":
        draw.polygon([69, 465, 69, 459, 74, 464, 74, 470], fill="rgb(0,255,0)",outline="green")
        draw.polygon([74, 470, 79, 465, 79, 459, 74, 464], fill="rgb(0,255,0)",outline="green")
        draw.polygon([69, 459, 74, 464, 79, 459, 74, 455], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([69, 465, 69, 459, 74, 464, 74, 470], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([74, 470, 79, 465, 79, 459, 74, 464], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([69, 459, 74, 464, 79, 459, 74, 455], fill=radiantlosefill,outline=radiantloseoutline)

    #radiant tron
    if win==True:
        draw.polygon([61, 537, 90, 557, 90, 542, 61, 522], fill="rgb(0,255,0)",outline="green")
        draw.polygon([90, 557, 109, 543, 109, 528, 90, 542], fill="rgb(0,255,0)",outline="green")
        draw.polygon([61, 522, 90, 542, 109, 528, 81, 509], fill="rgb(0,255,0)",outline="green")
    else:
        draw.polygon([61, 537, 90, 557, 90, 542, 61, 522], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([90, 557, 109, 543, 109, 528, 90, 542], fill=radiantlosefill,outline=radiantloseoutline)
        draw.polygon([61, 522, 90, 542, 109, 528, 81, 509], fill=radiantlosefill,outline=radiantloseoutline)


    #########герои
    lines={"diretop":{"xy":[(100,15),(140,15),(180,15),(220,15),(260,15)],"is_taken":[0,0,0,0,0]},
           "diremid":{"xy":[(320,260),(355,250),(390,270),(385,305),(345,315)],"is_taken":[0,0,0,0,0]},
           "direbot":{"xy":[(625,395),(625,355),(625,315),(585,355),(585,315)],"is_taken":[0,0,0,0,0]},
           "direles":{"xy":[(275,120),(315,120),(355,120),(295,155),(335,155)],"is_taken":[0,0,0,0,0]},
           "radtop":{"xy":[(15,210),(15,250),(15,290),(55,250),(55,290)],"is_taken":[0,0,0,0,0]},
           "radmid":{"xy":[(295,360),(260,385),(225,365),(230,330),(265,320)],"is_taken":[0,0,0,0,0]},
           "radbot":{"xy":[(560,590),(520,590),(480,590),(520,550),(480,550)],"is_taken":[0,0,0,0,0]},
           "radles":{"xy":[(315,460),(355,460),(395,460),(335,495),(375,495)],"is_taken":[0,0,0,0,0]}}
    f=open("dotabase/heroes.txt","r", encoding='utf-8-sig')
    heroes=f.readlines()
    f.close()
    for i in range(10):
        heroid=matchinfo["players"][i]["hero_id"]
        is_radiant=matchinfo["players"][i]["isRadiant"]
        line=matchinfo["players"][i]['lane']  #les 4,5  top 3 mid 2 bot 1
        #определение иконки героя по его id
        l=0
        while True:
            curhero=dict(eval(heroes[l]))
            if curhero["id"]==heroid:
                heroname=curhero["name"]
                break
            l+=1
        heroimg="dotabase/hero_icons/{}.png".format(heroname)
        heroicon=Image.open(heroimg)
        heroicon = heroicon.convert("RGBA")
                
        #определение линии и выбор координат для отрисовки иконки героя
        if line==3 and is_radiant==False:
            j=0
            while lines["diretop"]["is_taken"][j]!=0:
                j+=1
            coords=lines["diretop"]["xy"][j]
            lines["diretop"]["is_taken"][j]=1
        if line==2 and is_radiant==False:
            j=0
            while lines["diremid"]["is_taken"][j]!=0:
                j+=1
            coords=lines["diremid"]["xy"][j]
            lines["diremid"]["is_taken"][j]=1
        if line==1 and is_radiant==False:
            j=0
            while lines["direbot"]["is_taken"][j]!=0:
                j+=1
            coords=lines["direbot"]["xy"][j]
            lines["direbot"]["is_taken"][j]=1
        if line==4 or line==5 and is_radiant==False:
            j=0
            while lines["direles"]["is_taken"][j]!=0:
                j+=1
            coords=lines["direles"]["xy"][j]
            lines["direles"]["is_taken"][j]=1
        if line==3 and is_radiant==True:
            j=0
            while lines["radtop"]["is_taken"][j]!=0:
                j+=1
            coords=lines["radtop"]["xy"][j]
            lines["radtop"]["is_taken"][j]=1
        if line==2 and is_radiant==True:
            j=0
            while lines["radmid"]["is_taken"][j]!=0:
                j+=1
            coords=lines["radmid"]["xy"][j]
            lines["radmid"]["is_taken"][j]=1
        if line==1 and is_radiant==True:
            j=0
            while lines["radbot"]["is_taken"][j]!=0:
                j+=1
            coords=lines["radbot"]["xy"][j]
            lines["radbot"]["is_taken"][j]=1
        if line==4 or line==5 and is_radiant==True:
            j=0
            while lines["radles"]["is_taken"][j]!=0:
                j+=1
            coords=lines["radles"]["xy"][j]
            lines["radles"]["is_taken"][j]=1
        im.paste(heroicon,coords,mask=heroicon)

    im.save("map{}.png".format(matchinfo["match_id"]),"PNG")
