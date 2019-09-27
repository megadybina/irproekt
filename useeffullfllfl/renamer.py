import glob, os, requests, json

os.chdir(r"C:\Users\Morj\Desktop\bot\yasha\dotabase\items")
item=requests.get("https://api.stratz.com/api/v1/Item")
t=json.loads(item.text)
exists=[]
for file in glob.glob("*.png"):
    for key,value in t.items():
        if file=="{}.png".format(key):
            exists.append(key)

for key,value in t.items():
    if key not in exists:
        if not value["name"].startswith("item_recipe"):
            print(value["name"], key)




#193-279
#85*64

    
