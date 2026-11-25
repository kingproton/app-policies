import json, re
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK, REPO
import corrections as C
c=json.load(open(WORK+'collected.json'))
cands=json.load(open(WORK+'to_verify.json'))
def n(s): return re.sub(r'[^a-z0-9]','',s.lower().replace('&','and'))
# year-end Hot Rap Songs membership
ye={}
for y in c['yearend']:
    for L in y['lists']:
        if 'Rap' in L['chart'] and L['entries']:
            for e in L['entries']:
                ye.setdefault(n(e['title']),[]).append((L['year'],e.get('rank'),e.get('artist',''),L.get('source_url','')))
STRONG={'billboard_chart_page','billboard_article','wikipedia_chart_table','other_press'}
# Tables read directly (data/measured/genre_tables.json): full year-end Hot Rap Songs lists and the Hot Rap Songs
# peak column of artist discography tables, both on Wikipedia. A number in either is direct chart evidence.
GT={}
gt_path=REPO+'data/measured/genre_tables.json'
if os.path.exists(gt_path):
    for g in json.load(open(gt_path)): GT[(g['date'],g['rank'])]=g
def table_evidence(o):
    g=GT.get((o['first_top10'],o['rank'])) or {}
    if g.get('ye_rap'):
        yr,rk=sorted(g['ye_rap'],key=lambda x:x[1])[0]
        return 'rap',f"Year-End Hot Rap Songs {yr} #{rk}",g
    if g.get('discog_rap_peak'):
        lead=n(o['artist'].replace('¥$: ','').split(' Featuring ')[0].split(' & ')[0].split(',')[0].split(' X ')[0].split(' With ')[0])[:5]
        pages=sorted(g['discog_rap_pages'],key=lambda p:(lead not in n(p),p))
        page=pages[0].replace('_',' ').replace('%2C',',')
        return 'rap',f"Hot Rap Songs peak No. {g['discog_rap_peak']} (Wikipedia table: {page})",g
    return None,None,g
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
    ov=C.CLASSIFICATION_OVERRIDES.get(cid)
    if ov: stat=ov['status']; basis=ov['evidence_type']+': '+ov['summary']+' [targeted re-check]'
    # evidence tier: table = a chart figure read directly from a table; summary = Billboard pages known only through
    # web-search summaries; indirect = everything else
    tstat,tbasis,g=table_evidence(o)
    prev=basis
    if tstat=='rap':
        stat='rap'; basis=tbasis; tier='table'
    elif stat=='rap': tier='summary'
    elif stat=='not_rap': tier='table' if cid in C.NONRAP_TABLE_EVIDENCE else ('summary' if (ov or {}).get('confidence') in ('high','medium') or any(e in STRONG for e in [x['evidence_type'] for x in good]) else 'indirect')
    else: tier='none'
    rows.append(dict(cid=cid,date=o['first_top10'],rank=o['rank'],title=o['title'],artist=o['artist'],prior=o['prior'],status=stat,basis=basis,n_ev=len(ev),tier=tier,
                     earlier_basis=prev if prev!=basis else '',
                     ye_rap=g.get('ye_rap') or [],ye_rbhh=g.get('ye_rbhh') or [],ye_hot100=g.get('ye_hot100') or [],discog_rap_peak=g.get('discog_rap_peak'),
                     discog_rap_pages=g.get('discog_rap_pages') or [],discog_rap_dash_pages=g.get('discog_rap_dash_pages') or [],discog_rbhh=g.get('discog_rbhh') or [],
                     discog_rbhh_dash=g.get('discog_rbhh_dash') or [],wiki_genre_charts=g.get('wiki_genre_charts') or []))
json.dump(rows,open(WORK+'classification_status.json','w'),indent=1)
k=0
from collections import Counter
print(Counter(r['status'] for r in rows))
for r in rows:
    mark=''
    if r['status'] in ('rap','DISPUTED') or (r['status']=='unverified' and r['prior']=='rap'):
        k+=1; mark=f'{k:>3}'
    print(f"{mark:>3} c{r['cid']:<3} {r['date']} #{r['rank']:<2} {r['title'][:26]:26} {r['status']:10} {r['basis'][:110]}")
