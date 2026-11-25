"""Check each list song's first top-10 date and rank against two sources read directly:
  BC = Billboard Canada's licensed Hot 100 page for that chart week (hosted for chart weeks from 2023-09-02)
  W  = the entry date in Wikipedia's "List of Billboard Hot 100 top-ten singles in <year>"
Writes chart_check.json in the working directory."""
import json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK, REPO
rows = json.load(open(WORK + 'final_rows.json'))
cv = {w['date']: w for w in json.load(open(REPO + 'data/measured/chart_verification.json'))['weeks']}
wl = json.load(open(REPO + 'data/measured/wikipedia_lists.json'))['topten']
ALIAS = {'fen': 'fein', 'pmillions': 'pussymillions', 'imdatna': 'imdatnigga', 'superheroheroesvillains': 'superhero'}
def nz(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\([^)]*\)', '', s)
    s = re.sub(r'[^a-z0-9]+', '', s.replace('&', 'and'))
    return ALIAS.get(s, s)
wby = {}
for e in wl: wby.setdefault(nz(e['title']), []).append(e)
out = {}
for r in rows:
    d, rk = r['first_top10'], r['rank']
    w = cv.get(d)
    if not w or w['status'] != 'compared': bc = 'not hosted' if d < '2023-09-02' else 'week missing on site'
    else:
        hit = next((t for pos, t in w.get('top10', []) if pos == rk), None)
        bc = 'match' if hit and (nz(hit) == nz(r['title']) or nz(hit)[:8] == nz(r['title'])[:8]) else f'differs ({hit})'
        if w['titles_matching'] < 90: bc = 'page shows another week'
    cands = [e for e in wby.get(nz(r['title']), []) if abs(int(e['entry'][:4]) - int(d[:4])) <= 1]
    if not cands: wk = 'not listed'
    else:
        e = min(cands, key=lambda e: abs((int(e['entry'][:4]) - int(d[:4])) * 12 + int(e['entry'][5:7]) - int(d[5:7])))
        wk = 'match' if e['entry'] == d else f"differs ({e['entry']})"
    out[r['cid']] = dict(n=r['n'], title=r['title'], first_top10=d, rank=rk, billboard_canada=bc, wikipedia_entry_date=wk)
json.dump(out, open(WORK + 'chart_check.json', 'w'), indent=1)
import collections
print('Billboard Canada:', dict(collections.Counter(v['billboard_canada'].split(' (')[0] for v in out.values())))
print('Wikipedia entry date:', dict(collections.Counter(v['wikipedia_entry_date'].split(' (')[0] for v in out.values())))
print('neither source:', [v['title'] for v in out.values() if v['billboard_canada'] != 'match' and v['wikipedia_entry_date'] != 'match'])
print('differs:', [(v['title'], v['billboard_canada'], v['wikipedia_entry_date']) for v in out.values() if 'differs' in v['billboard_canada'] or 'differs' in v['wikipedia_entry_date']])
