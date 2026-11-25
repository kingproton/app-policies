"""Fetch LRCLIB search results (synced lyrics) for each track. Raw responses stay in the working directory only and are never committed."""
import sys, os, re, json, urllib.parse, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from netlib import fetch
from mpaths import SP, IN
OUT = SP + 'net/lrclib/'
rows = json.load(open(IN + 'final_rows.json'))
cands = {o['cid']: o for o in json.load(open(IN + 'to_verify.json'))}
EXTRA = [22, 132, 133, 134, 135, 136, 2, 1, 3, 65, 99, 71, 80, 104, 120, 121, 123]
def lead(a): return re.split(r' Featuring | & | X | With |, ', a.replace('¥$: ', ''))[0].strip()
def clean_title(t): return re.sub(r'\s*[\(\[].*?[\)\]]', '', t).replace('*', '').strip() or t
todo = [(r['cid'], r['title'], r['artists']) for r in rows] + [(c, cands[c]['title'], cands[c]['artist']) for c in EXTRA if c in cands]
n_ok = 0
for cid, title, artist in todo:
    got = 0
    for qi, params in enumerate([dict(track_name=clean_title(title), artist_name=lead(artist)), dict(q=f"{clean_title(title)} {lead(artist)}")]):
        st, body = fetch('https://lrclib.net/api/search?' + urllib.parse.urlencode(params), OUT + f'search_{cid}_{qi}.json')
        try: res = json.loads(body) if st == 200 else []
        except Exception: res = []
        got += sum(1 for x in res if x.get('syncedLyrics'))
        if got >= 3: break
    n_ok += got > 0
    print(cid, title[:30], 'synced candidates:', got, flush=True)
print('tracks with at least one synced candidate:', n_ok, 'of', len(todo))
