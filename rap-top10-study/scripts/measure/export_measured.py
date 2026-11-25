"""Export the derived measurement data (numbers and labels only, no lyric text, no audio) for the repository."""
import json, os, re, sys, statistics
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpaths import SP, IN
OUT = sys.argv[1].rstrip('/') + '/'
os.makedirs(OUT, exist_ok=True)
def dump(name, obj):
    json.dump(obj, open(OUT + name, 'w'), indent=0, ensure_ascii=False, sort_keys=False)
    print(name, os.path.getsize(OUT + name), 'bytes')

# 1. chart verification: Billboard Canada's licensed Hot 100 pages against the weekly mirror
allc = {w['date']: w['data'] for w in json.load(open(IN + 'all.json'))}
cab = json.load(open(SP + 'net/cabillboard_hot100.json'))
def nz(s): return re.sub(r'[^a-z0-9]+', '', (s or '').lower().replace('&', 'and'))
weeks = []
def num(x):
    try: return int(x)
    except Exception: return None
for date in sorted(cab):
    v = cab[date]; mir = allc.get(date)
    if not v or not v.get('titles100'):
        weeks.append(dict(date=date, status='not available on Billboard Canada')); continue
    if not mir:
        weeks.append(dict(date=date, status='not in mirror')); continue
    bypos = {r['this_week']: r for r in mir}
    same = sum(1 for pos, t in v['titles100'] if pos in bypos and (nz(bypos[pos]['song']) == nz(t) or nz(bypos[pos]['song'])[:10] == nz(t)[:10]))
    rows = v.get('rows') or []
    rmatch = 0
    for r in rows:
        m = bypos.get(r.get('pos'))
        if not m: continue
        ok = nz(m['song'])[:10] == nz(r.get('title'))[:10]
        if num(r.get('peak')) is not None: ok = ok and num(r['peak']) == m.get('peak_position')
        if num(r.get('weeks')) is not None: ok = ok and num(r['weeks']) == m.get('weeks_on_chart')
        if num(r.get('last')) is not None: ok = ok and num(r['last']) == m.get('last_week')
        rmatch += ok
    diffs = [[pos, t, bypos[pos]['song']] for pos, t in v['titles100'] if pos in bypos and not (nz(bypos[pos]['song']) == nz(t) or nz(bypos[pos]['song'])[:10] == nz(t)[:10])]
    weeks.append(dict(date=date, status='compared', titles_compared=len(v['titles100']), titles_matching=same, full_rows_compared=len(rows), full_rows_matching=int(rmatch),
                      top10=[[pos, t] for pos, t in v['titles100'] if pos <= 10],
                      title_differences=diffs if len(diffs) <= 3 else None))      # [position, Billboard Canada title, mirror title]; kept only for near-matches
dump('chart_verification.json', dict(source='https://ca.billboard.com/charts/hot-100/<date> (Billboard Canada, licensed chart pages)', compared_with='mhollingshead/billboard-hot-100 weekly mirror',
                                     note='titles = the 100-title list on each page; full rows = the 25 rows that carry last week, peak and weeks on chart', weeks=weeks))

# 2. Wikipedia list transcriptions (year-end lists and yearly top-ten lists)
dump('wikipedia_lists.json', json.load(open(SP + 'net/wiki_lists.json')))

# 3. genre evidence tables per top-10 arrival
dm = json.load(open(SP + 'net/discog_match.json'))
dump('genre_tables.json', dm)

# 4. Apple catalog matches (runtime source)
M = json.load(open(SP + 'net/itunes_matches.json'))
ap = {}
for cid, v in M.items():
    m = v.get('match')
    ap[cid] = dict(n=v.get('n'), title=v['title'], artist=v['artist'],
                   match=None if not m else dict(track=m.get('trackName'), collection=m.get('collectionName'), duration_ms=m.get('ms'), explicitness=m.get('explicit'), release_date=m.get('releaseDate'), genre=m.get('genre')))
dump('apple_catalog.json', ap)

# 5. synced-lyric structure (derived; per-line arrays dropped)
L = json.load(open(SP + 'net/lrc_structure.json'))
ls = {}
for cid, v in L.items():
    ls[cid] = {k: x for k, x in v.items() if k not in ('line_times', 'line_ids', 'line_words')}
dump('lyric_structure_algorithm.json', ls)

# 6. audio feel
dump('audio_feel.json', json.load(open(SP + 'net/audio_feel.json')))

# 7. how reliable a dash in a rap column is: songs that show a dash in one discography table and a numbered Hot Rap Songs
#    peak in another (same normalised title, same Hot 100 peak and same R&B/Hip-Hop peak, so it is the same song)
import collections
DP = json.load(open(SP + 'net/discog_peaks.json'))
by = collections.defaultdict(list)
for page, rows_ in DP.items():
    for r in rows_:
        if r.get('has_rap_col') and isinstance(r.get('us'), int): by[(r['key'], r['us'], r.get('rbhh'))].append((page, r['title'], r.get('rap')))
conf = []
for (key, us, rbhh), v in sorted(by.items(), key=lambda kv: (kv[0][0], kv[0][1], str(kv[0][2]))):
    nums = [(p, n) for p, t, n in v if isinstance(n, int)]; dash = [p for p, t, n in v if n == '—']
    if nums and dash: conf.append(dict(title=v[0][1], hot100_peak=us, rbhh_peak=rbhh, rap_peak_pages=[[p, n] for p, n in nums], dash_pages=dash))
dump('discography_dash_conflicts.json', dict(
    note='Wikipedia artist discography tables read on 2026-11-25. A dash in a Hot Rap Songs column is not evidence that a song missed the chart: '
         'these songs show a dash in one table and a numbered rap peak in another.',
    tables_read=len(DP), tables_with_rap_column=sum(1 for rows_ in DP.values() if any(r.get('has_rap_col') for r in rows_)), songs=conf))
