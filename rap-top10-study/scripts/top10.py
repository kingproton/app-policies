import json, re, sys, datetime
D='/tmp/claude-0/-home-user-app-policies/08207d95-5f38-5913-acec-14c31ee115ad/scratchpad/data/'
charts=json.load(open(D+'all.json'))
charts.sort(key=lambda c:c['date'])
def norm(s):
    s=s.lower().replace('&','and')
    s=re.sub(r"[’'`\"]","",s)
    s=re.sub(r"[^a-z0-9$!]+"," ",s).strip()
    return s
def prim(a):
    a=a.lower()
    a=re.split(r"\s+(featuring|feat\.|with|x|&|,|and)\s+|,",a)[0]
    return norm(a)
first={}   # key -> (date,pos,song,artist)
titles={}
# also gaps check
dates=[c['date'] for c in charts]
gaps=[]
for i in range(1,len(dates)):
    d0=datetime.date.fromisoformat(dates[i-1]); d1=datetime.date.fromisoformat(dates[i])
    if (d1-d0).days!=7 and d0.year>=2015: gaps.append((dates[i-1],dates[i]))
for c in charts:
    for e in c['data']:
        if e['this_week']<=10:
            k=(norm(e['song']),prim(e['artist']))
            if k not in first:
                first[k]=(c['date'],e['this_week'],e['song'],e['artist'],e.get('last_week'),e.get('weeks_on_chart'))
print('gaps since 2015:',gaps)
# arrivals since 2019
arr=[(v[0],v[1],v[2],v[3],v[4],v[5]) for k,v in first.items() if v[0]>='2019-01-01']
arr.sort(key=lambda x:(x[0],-x[1]),reverse=True)
json.dump(arr,open(D+'arrivals.json','w'),indent=0)
print(len(arr),'top-10 arrivals since 2019-01-01')
# title duplicates with different primary artists among arrivals since 2018
from collections import defaultdict
bt=defaultdict(set)
for k,v in first.items():
    if v[0]>='2018-01-01': bt[k[0]].add((v[3],v[0]))
for t,s in bt.items():
    if len(s)>1: print('DUP TITLE',t,s)
