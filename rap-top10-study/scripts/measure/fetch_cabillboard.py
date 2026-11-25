"""Fetch every available weekly Hot 100 page from Billboard Canada (robots.txt permits /charts/) and parse rows."""
import sys, os, re, json, datetime, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from netlib import fetch
from mpaths import SP
OUT = SP + 'net/cabillboard/'
def parse(h):
    rows = []
    for m in re.finditer(r'<div class="chart-item" id="song-\d+".*?(?=<div class="chart-item" id="song-|\Z)', h, re.S):
        b = m.group(0)
        g = lambda cls: (re.search(r'class="%s"[^>]*>(.*?)</' % cls, b, re.S) or [None, ''])[1]
        txt = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s)).strip()
        pos = txt(g('chart-item-position'))
        if not pos.isdigit(): continue
        rows.append(dict(pos=int(pos), title=txt(g('chart-item-headline')), artist=txt(g('chart-item-subheadline')),
                         last=txt(g('chart-item-last-week')), peak=txt(g('chart-item-peak-pos')), weeks=txt(g('chart-item-weeks-on'))))
    return rows
def itemlist(h):
    for m in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        if '"ItemList"' in m:
            try: return [(e['position'], html.unescape(e['name'])) for e in json.loads(m)['itemListElement']]
            except Exception: return []
    return []
d = datetime.date(2026, 11, 21); stop = datetime.date(2023, 6, 3)
res = {}; misses = 0
while d >= stop:
    ds = d.isoformat()
    st, body = fetch(f'https://ca.billboard.com/charts/hot-100/{ds}', OUT + f'hot100_{ds}.html')
    rows = parse(body) if st == 200 else []
    if st == 200 and len(rows) >= 20:
        res[ds] = dict(rows=rows, titles100=itemlist(body)); misses = 0
    else:
        res[ds] = None; misses += 1
        if os.path.exists(OUT + f'hot100_{ds}.html') and len(rows) < 20: os.remove(OUT + f'hot100_{ds}.html')
        print('miss', ds, st, len(rows), flush=True)
        if misses >= 6: break
    d -= datetime.timedelta(days=7)
json.dump(res, open(SP + 'net/cabillboard_hot100.json', 'w'))
ok = sorted(k for k, v in res.items() if v)
print('weeks parsed:', len(ok), 'from', ok[0] if ok else None, 'to', ok[-1] if ok else None)
