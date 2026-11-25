"""Fetch the Wikipedia list, year-end, discography and album pages named in wiki_pages.json as wikitext (action=raw).
Each page is cached in the working directory, so a second run makes no request. Song articles are a separate step
(fetch_wiki_articles.py), which needs the lists parsed first (parse_wiki_lists.py)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpaths import SP
from netlib import wiki_raw
P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wiki_pages.json')))
DIRS = {'lists': 'net/wikipedia/', 'discographies': 'net/wikipedia/disco/', 'albums': 'net/wikipedia/albums/'}
only = sys.argv[1:]                                   # optional: page titles to fetch instead of the whole list
ok = bad = 0
for group, sub in DIRS.items():
    os.makedirs(SP + sub, exist_ok=True)
    for title in P[group]:
        if only and title not in only: continue
        st, body = wiki_raw(title, SP + sub)
        if st == 200 and body: ok += 1
        else: bad += 1; print('FAILED', st, title)
print(f'{ok} pages present, {bad} failed')
