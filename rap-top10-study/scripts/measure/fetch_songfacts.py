"""Fetch Songfacts pages for the list tracks (permitted by the site's robots.txt; /search is not used)."""
import sys, os, re, json, html, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from netlib import fetch
from mpaths import SP
OUT = SP + 'net/songfacts/'
F = json.load(open(SP + 'data/final_rows.json'))
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = s.replace('&', ' ').replace("'", '').replace('.', '').replace('!', 'i' if False else '').replace('*', '')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')
def artists(a):
    a = a.replace('¥$: ', '')
    parts = re.split(r' Featuring | Feat\. | & | X | x | With |, | and ', a)
    return [p.strip() for p in parts if p.strip()]
res = {}
for r in F:
    title = r['title']; arts = artists(r['artists'])
    t_variants = []
    base = re.sub(r'\s*[\(\[].*?[\)\]]', '', title).strip()
    for t in (title, base, title.replace('!', 'i'), base.replace('N***a', 'Nigga'), base.replace('Pussy', 'P****')):
        s = slug(t)
        if s and s not in t_variants: t_variants.append(s)
    a_variants = []
    for a in arts + ['-'.join(arts[:2])]:
        s = slug(a)
        if s and s not in a_variants: a_variants.append(s)
    hit = None; tried = 0
    for a in a_variants[:3]:
        for t in t_variants[:3]:
            url = f'https://www.songfacts.com/facts/{a}/{t}'
            path = OUT + f"{r['cid']}__{a}__{t}.html"
            st, body = fetch(url, path); tried += 1
            if st == 200 and body and '<title>' in body and 'Songfacts' in body and '404' not in body[:400]:
                tt = re.search(r'<title>(.*?)</title>', body, flags=re.S).group(1).strip()
                hit = dict(url=url, path=path, page_title=html.unescape(tt)); break
            if os.path.exists(path) and st != 200: os.remove(path)
        if hit: break
    res[r['cid']] = dict(n=r['n'], title=title, artists=r['artists'], hit=hit, tried=tried)
    print(r['n'], title[:28], '->', hit['page_title'][:70] if hit else f'none ({tried} tried)', flush=True)
    json.dump(res, open(SP + 'net/songfacts_pages.json', 'w'), indent=0)
print('found', sum(1 for v in res.values() if v['hit']), 'of', len(res))
