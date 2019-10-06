import requests
import pprint
import json
import shutil
r = requests.get("https://api.opendota.com/api/matches/4875616323")#bk-4742780539  pro-4799474584
#r = requests.get("https://api.opendota.com/api/players/143597200/matches?limit=1")
t=json.loads(r.text)
path=['players',2,'last_hits']
pprint.pprint(t)
'''
response = requests.get(t["dire_team"]["logo_url"], stream=True)
with open('team1.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response
'''
#pprint.pprint(t["league"])
#pprint.pprint(t["dire_team"])
#pprint.pprint(t["radiant_team"])
'''
f=open("dotabase/heroes.txt","r")
heroes=f.readlines()
f.close()
for i in range(10):
    heroid=matchinfo["players"][i]["hero_id"]
    l=0
    while True:
        curhero=dict(eval(heroes[l]))
        if curhero["id"]==heroid:
            heroname=curhero["localname"]
            break
        l+=1
    print(heroname,t["players"][i]["lane_efficiency"])
'''
