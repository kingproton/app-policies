"""Fetch the Wikipedia article (wikitext) for every Hot 100 top-ten arrival in the window, using the links in
Wikipedia's yearly top-ten lists. Extract Billboard chart ids from {{single chart}} rows, infobox genre and length."""
import sys, os, re, json, unicodedata, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from netlib import wiki_raw
from mpaths import SP, IN
L = json.load(open(SP + 'net/wiki_lists.json'))
arr = json.load(open(IN + 'arrivals.json'))
def nz(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower().replace('&', 'and')
    t = re.sub(r'\(.*?\)', '', s); s = t if re.sub(r'[^a-z0-9]', '', t) else s
    return re.sub(r'[^a-z0-9]', '', s)
LO = '2021-07-31'
byk = {}
for e in L['topten']:
    if e.get('article'): byk.setdefault(nz(e['title']), []).append(e)
todo = []
for d, rank, title, artist, lw, wk in arr:
    if d < LO: continue
    c = byk.get(nz(title), [])
    if not c:
        same = [e for e in L['topten'] if e.get('article') and e['entry'] and abs(int(e['entry'][:4]) - int(d[:4])) <= 1]
        best = max(same, key=lambda e: difflib.SequenceMatcher(None, nz(e['title']), nz(title)).ratio(), default=None)
        if best and difflib.SequenceMatcher(None, nz(best['title']), nz(title)).ratio() >= 0.8: c = [best]
    a0 = nz(artist)[:5]
    c2 = [e for e in c if a0 in nz(e['artist']) or nz(e['artist'])[:5] in nz(artist)] or c
    todo.append(dict(date=d, rank=rank, title=title, artist=artist, article=c2[0]['article'] if c2 else None))
print('arrivals since', LO, ':', len(todo), '| with article link:', sum(1 for t in todo if t['article']), flush=True)
out = []
for i, t in enumerate(todo):
    rec = dict(t)
    if t['article']:
        st, body = wiki_raw(t['article'], SP + 'net/wikipedia/articles/')
        m = re.match(r'\s*#REDIRECT\s*\[\[([^\]#|]+)', body or '', re.I)
        if st == 200 and m:
            rec['redirect'] = m.group(1).strip(); st, body = wiki_raw(rec['redirect'], SP + 'net/wikipedia/articles/')
        rec['status'] = st; rec['length_chars'] = len(body or '')
        if st == 200:
            ids = re.findall(r'\{\{\s*[Ss]ingle ?chart\s*\|\s*([A-Za-z0-9 &/\-]+?)\s*\|\s*(\d+)', body)
            rec['chart_ids'] = sorted({(a.strip(), int(b)) for a, b in ids})
            rec['rap_mentions'] = len(re.findall(r'Hot Rap Songs|Rap Songs|Rap Streaming|Rap Airplay', body))
            g = re.search(r'\|\s*genre\s*=\s*(.*?)(?=\n\s*\|\s*[a-z_ ]+\s*=|\n\}\})', body, re.S)
            rec['infobox_genre'] = re.sub(r'\s+', ' ', re.sub(r'<ref[^>]*/>|<ref[^>]*>.*?</ref>|\{\{(?:hlist|flatlist|plainlist|cn|citation needed)[^}]*\}\}|[\[\]\{\}\*]', ' ', g.group(1), flags=re.S)).strip()[:160] if g else None
            ln = re.search(r'\|\s*length\s*=\s*(?:\{\{[Dd]uration\|)?(?:m=)?(\d+)[:|](?:s=)?(\d{1,2})', body)
            rec['infobox_length'] = f"{int(ln.group(1))}:{int(ln.group(2)):02d}" if ln else None
    out.append(rec)
    if i % 25 == 0: print(i, t['title'][:30], rec.get('status'), flush=True); json.dump(out, open(SP + 'net/wiki_articles.json', 'w'), indent=1)
json.dump(out, open(SP + 'net/wiki_articles.json', 'w'), indent=1)
print('done', len(out), 'fetched ok', sum(1 for r in out if r.get('status') == 200))
