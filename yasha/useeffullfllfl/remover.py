with open('tips_ru.txt','r') as f:
    tips=f.readlines()
newtips=[]
for tip in tips:
    tip.find(':')
    newtips.append(tip[tip.find(':')+1:])
    
with open('tips_ru.txt','w') as f:
    for ntip in newtips:
        f.write(ntip)
