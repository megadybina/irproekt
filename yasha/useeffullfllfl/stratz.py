import requests
import pprint
import json
import time#4986461644          5001195046
r = requests.get("https://api.stratz.com/api/v1/match/4986461644/breakdown")
#r=requests.get("https://api.stratz.com/api/v1/Player/143597200")
#r=requests.get('https://api.stratz.com/api/v1/Player/173323577/matches?lobbyType=9&take=30')
#team = requests.get("https://api.stratz.com/api/v1/Team/2163")
#r = requests.get("https://api.stratz.com/api/v1/Patch/notes")
#r=requests.get("https://api.stratz.com/api/v1/Hero")
#r=requests.get("https://api.opendota.com/api/matches/4886743348")
#r = requests.get("https://api.stratz.com/api/v1/lobbyType")
#r=requests.get('https://api.stratz.com/api/v1/Ability?languageId=19')
t=json.loads(r.text)
'''
countbk=0
countt=0
countparts=0
for el in reversed(t):
    if el['didRadiantWin'] == el['players'][0]['isRadiant']:
        res=True
        countt+=1
        if countt==3:
            countbk+=1
            countparts+=1
            countt=0
    else:
        countt=0
        countparts+=1
        res=False
    print(time.ctime(el['startDateTime']),res)
print(countparts,countbk)

{'X': 168, 'Y': 92, 'time': 418, 'type': 0} rad t1 bot
{'X': 82, 'Y': 170, 'time': -9, 'type': 0} dire t1 top
'''
pprint.pprint(t['players'][0])

'''
pprint.pprint(t.get('2'))
pprint.pprint(t.get('269'))
pprint.pprint(t.get('1'))
pprint.pprint(t.get('114'))

for key,value in t.items():
    if value['stat']['isStackable']:
        print(value['language'][0]['displayName'])
#    print(t[0]["players"][i].get("numLastHits"))
#pprint.pprint(t[0]["players"][8]) #игрок
'''

#руский 19
# англ 0
