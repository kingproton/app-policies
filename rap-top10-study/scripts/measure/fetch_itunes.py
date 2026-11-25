"""Match each track to Apple's catalog (iTunes Search API): runtime, version, preview URL, Apple genre."""
import sys, os, re, json, unicodedata, urllib.parse, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from netlib import fetch
from mpaths import SP
OUT = SP + 'net/itunes/'
rows = json.load(open(SP + 'data/final_rows.json'))
T = {int(k): v for k, v in json.load(open(SP + 'data/tracks_merged.json')).items()}
cands = {o['cid']: o for o in json.load(open(SP + 'data/to_verify.json'))}
EXTRA = [22, 132, 133, 134, 135, 136, 2]       # Anxiety, Love All, Hurricane, Jail, Rumors, Industry Baby, Solar Eclipse
EXTRA += [1, 3, 65, 99, 71, 80, 104, 120, 121, 123]   # soft exclusions, in case one enters the list
def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower().replace('&', ' and ').replace('$', 's')
    s = re.sub(r'\((?:feat|with|ft)[^)]*\)|\[(?:feat|with|ft)[^\]]*\]', ' ', s)
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()
def base_title(t): return norm(re.sub(r'\s*[\(\[].*?[\)\]]', '', t)) or norm(t)
BAD = re.compile(r'karaoke|instrumental|tribute|originally performed|lullaby|cover|8d|sped up|slowed|remix|live|acoustic|clean|edit\b|mix\b|version', re.I)
def lead(a): return re.split(r' Featuring | & | X | With |, ', a.replace('¥$: ', ''))[0].strip()
def score(r, title, artist, runtime, want_remix):
    tn = r.get('trackName', ''); an = r.get('artistName', '')
    if base_title(tn) != base_title(title) and difflib.SequenceMatcher(None, base_title(tn), base_title(title)).ratio() < 0.86: return None
    la = norm(lead(artist)); na = norm(an)
    if not la or not na: return None
    if la.split()[0] not in na and na.split()[0] not in norm(artist): return None
    s = 0.0
    if r.get('trackExplicitness') == 'explicit': s += 3
    elif r.get('trackExplicitness') == 'cleaned': s -= 2
    extra = re.sub(re.escape(re.sub(r'\s*[\(\[].*', '', tn)), '', tn)
    if BAD.search(extra) and not (want_remix and 'remix' in extra.lower()): s -= 4
    if BAD.search(r.get('collectionName', '') or '') and 'deluxe' not in (r.get('collectionName') or '').lower(): s -= 1
    if runtime and r.get('trackTimeMillis'):
        d = abs(r['trackTimeMillis'] / 1000 - runtime)
        s += 3 if d <= 2 else 1 if d <= 5 else -2 if d > 15 else 0
    if norm(an) == norm(lead(artist)) or norm(an) in norm(artist): s += 1
    return s
todo = [(r['n'], r['cid'], r['title'], r['artists']) for r in rows] + [(None, c, cands[c]['title'], cands[c]['artist']) for c in EXTRA if c in cands]
res = {}
for n, cid, title, artist in todo:
    t = T.get(cid) or {}
    runtime = t.get('runtime_s'); want_remix = 'remix' in (t.get('version_used') or '').lower()
    best = None; allc = []
    queries = [f"{lead(artist)} {re.sub(r'[*]', '', re.sub(r'\\s*[\\(\\[].*', '', title))}", f"{title} {lead(artist)}"]
    if want_remix: queries.insert(0, f"{title} {artist} remix")
    for qi, q in enumerate(queries):
        url = 'https://itunes.apple.com/search?' + urllib.parse.urlencode(dict(term=q, entity='song', limit=50, country='US', explicit='Yes'))
        st, body = fetch(url, OUT + f'search_{cid}_{qi}.json')
        try: results = json.loads(body).get('results', []) if st == 200 else []
        except Exception: results = []
        for r in results:
            sc = score(r, title, artist, runtime, want_remix)
            if sc is not None: allc.append((sc, r))
        if allc and max(x[0] for x in allc) >= 4: break
    if allc:
        allc.sort(key=lambda x: (-x[0], x[1].get('releaseDate', '')))
        sc, r = allc[0]
        best = dict(score=sc, trackId=r.get('trackId'), trackName=r.get('trackName'), artistName=r.get('artistName'), collectionName=r.get('collectionName'),
                    ms=r.get('trackTimeMillis'), explicit=r.get('trackExplicitness'), previewUrl=r.get('previewUrl'), genre=r.get('primaryGenreName'),
                    releaseDate=(r.get('releaseDate') or '')[:10], n_candidates=len(allc),
                    alt=[(round(a, 1), b.get('trackName'), b.get('collectionName'), b.get('trackTimeMillis'), b.get('trackExplicitness')) for a, b in allc[1:4]])
    res[cid] = dict(n=n, title=title, artist=artist, runtime_known=runtime, match=best)
    print(n, cid, title[:28], '->', (best['trackName'][:34], best['collectionName'][:30], best['ms'], best['explicit'], best['score']) if best else 'NO MATCH', flush=True)
    json.dump(res, open(SP + 'net/itunes_matches.json', 'w'), indent=1)
print('matched', sum(1 for v in res.values() if v['match']), 'of', len(res))
