import json, re
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK, REPO
D = WORK
charts=sorted(json.load(open(D+'all.json')), key=lambda c:c['date'])
def norm(s):
    s=s.lower().replace('&','and'); s=re.sub(r"[’'`\"]","",s); return re.sub(r"[^a-z0-9$!]+"," ",s).strip()
def prim(a):
    a=a.lower(); a=re.split(r"\s+(featuring|feat\.|with|x|&|,|and)\s+|,",a)[0]; return norm(a)
def key(song, artist):
    k=(norm(song), prim(artist))
    # Carnival credit changed from "Kanye West" to "Ye" mid-run; treat as one song
    if k[0]=='carnival' and k[1] in ('$ kanye west','$ ye'): k=('carnival','$ ye')
    return k
hist={}
for c in charts:
    if c['date']<'2020-06-01': continue
    for e in c['data']:
        k=key(e['song'],e['artist'])
        h=hist.setdefault(k,{'weeks':[], 'artists':set()})
        h['weeks'].append((c['date'],e['this_week'])); h['artists'].add(e['artist'])
cands=json.load(open(D+'to_verify.json'))
out={}
for o in cands:
    k=key(o['title'],o['artist']); h=hist.get(k)
    if not h: print('MISSING',o['title']); continue
    w=h['weeks']; first_chart=w[0][0]
    top10=[x for x in w if x[1]<=10]
    first10=top10[0]
    # position in the week before first top-10 week
    idx=[x[0] for x in w].index(first10[0])
    prev=w[idx-1] if idx>0 else None
    import datetime
    debut_in_top10 = (first_chart==first10[0])
    climbed_from = None if debut_in_top10 else (prev[1] if prev and (datetime.date.fromisoformat(first10[0])-datetime.date.fromisoformat(prev[0])).days==7 else 're-entry')
    peak=min(x[1] for x in w)
    out[o['cid']]=dict(cid=o['cid'],title=o['title'],first_chart_week=first_chart,first_top10=first10[0],rank_first_top10=first10[1],
        debut_in_top10=debut_in_top10, climbed_from=climbed_from, weeks_to_top10=len([x for x in w if x[0]<first10[0]]),
        peak=peak, weeks_in_top10=len(top10), total_weeks=len(w), last_chart_week=w[-1][0], artist_credits=sorted(h['artists']))
    assert first10[0]==o['first_top10'] and first10[1]==o['rank'], (o, first10)
json.dump(out,open(D+'chart_metrics.json','w'),indent=1)
print(len(out),'songs; all first-top-10 dates/ranks re-confirmed against weekly charts')
for cid in sorted(out):
    m=out[cid]
    if not m['debut_in_top10'] or len(m['artist_credits'])>1:
        print(cid, m['title'], '| debut' if m['debut_in_top10'] else f"| climbed from {m['climbed_from']} after {m['weeks_to_top10']} wks", '| peak',m['peak'],'| wks top10',m['weeks_in_top10'],'| total',m['total_weeks'], '| credits:',m['artist_credits'] if len(m['artist_credits'])>1 else '')
