import json, re
SP='/tmp/claude-0/-home-user-app-policies/08207d95-5f38-5913-acec-14c31ee115ad/scratchpad/'
c=json.load(open(SP+'data/collected.json'))
cands=json.load(open(SP+'data/to_verify.json'))
def n(s): return re.sub(r'[^a-z0-9]','',s.lower().replace('&','and'))
# year-end Hot Rap Songs membership
ye={}
for y in c['yearend']:
    for L in y['lists']:
        if 'Rap' in L['chart'] and L['entries']:
            for e in L['entries']:
                ye.setdefault(n(e['title']),[]).append((L['year'],e.get('rank'),e.get('artist',''),L.get('source_url','')))
STRONG={'billboard_chart_page','billboard_article','wikipedia_chart_table','other_press'}
rows=[]
for o in cands:
    cid=o['cid']; ev=c['classify'].get(str(cid),[])
    t=n(o['title'])
    yhit=None
    for yr,rk,art,url in ye.get(t,[]):
        fy=int(o['first_top10'][:4])
        prim=n(o['artist'].split(' Featuring ')[0].split(' & ')[0].split(',')[0].split(' X ')[0].split(' With ')[0])
        if abs(yr-fy)<=1 and (prim[:5] in n(art) or n(art)[:5] in n(o['artist']) or art=='' ):
            yhit=(yr,rk,url)
    good=[e for e in ev if e['evidence_type'] in STRONG and e['hot_rap_songs']!='unverified' and e['confidence'] in ('high','medium')]
    stat='unverified'; basis=''
    if yhit:
        stat='rap'; basis=f"Year-End Hot Rap Songs {yhit[0]} #{yhit[1]}"
    pos=[e for e in good if e['hot_rap_songs']=='charted']; neg=[e for e in good if e['hot_rap_songs']=='not_charted']
    if pos and not stat=='rap': stat='rap'; basis=pos[0]['evidence_type']+': '+pos[0]['evidence_summary'][:120]
    if neg:
        if stat=='rap': stat='DISPUTED'; basis+=' || NEG: '+neg[0]['evidence_summary'][:120]
        else: stat='not_rap'; basis=neg[0]['evidence_type']+': '+neg[0]['evidence_summary'][:160]
    if stat=='unverified' and ev:
        basis='weak: '+ev[-1]['evidence_type']+' '+ev[-1]['hot_rap_songs']+' '+ev[-1]['evidence_summary'][:120]
    rows.append(dict(cid=cid,date=o['first_top10'],rank=o['rank'],title=o['title'],artist=o['artist'],prior=o['prior'],status=stat,basis=basis,n_ev=len(ev)))
json.dump(rows,open(SP+'data/classification_status.json','w'),indent=1)
k=0
from collections import Counter
print(Counter(r['status'] for r in rows))
for r in rows:
    mark=''
    if r['status'] in ('rap','DISPUTED') or (r['status']=='unverified' and r['prior']=='rap'):
        k+=1; mark=f'{k:>3}'
    print(f"{mark:>3} c{r['cid']:<3} {r['date']} #{r['rank']:<2} {r['title'][:26]:26} {r['status']:10} {r['basis'][:110]}")
