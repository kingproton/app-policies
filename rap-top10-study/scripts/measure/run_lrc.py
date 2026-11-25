"""Pick the LRCLIB records that match each track's measured version (by duration) and derive structure metrics.
Writes numbers only: no lyric text leaves this process."""
import sys, os, json, re, glob, statistics, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lrc_analyze import analyze
from mpaths import SP
M = json.load(open(SP + 'net/itunes_matches.json'))
T = {int(k): v for k, v in json.load(open(SP + 'data/tracks_merged.json')).items()}
def nz(s): return re.sub(r'[^a-z0-9]+', ' ', unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()).strip()
def lead(a): return re.split(r' Featuring | & | X | With |, ', a.replace('¥$: ', ''))[0].strip()
out = {}
for cid, v in M.items():
    target = (v['match']['ms'] / 1000.0) if v.get('match') else (v.get('runtime_known') or (T.get(int(cid)) or {}).get('runtime_s'))
    recs = []
    for f in sorted(glob.glob(SP + f'net/lrclib/search_{cid}_*.json')):
        try: recs += json.load(open(f))
        except Exception: pass
    seen = set(); cands = []
    la = nz(lead(v['artist'])).split()[0] if nz(lead(v['artist'])) else ''
    bt = nz(re.sub(r'\s*[\(\[].*', '', v['title']).replace('*', ''))
    for x in recs:
        if x.get('id') in seen or not x.get('syncedLyrics'): continue
        seen.add(x.get('id'))
        if la and la not in nz(x.get('artistName', '')): continue
        tn = nz(re.sub(r'\s*[\(\[].*', '', x.get('trackName', '')))
        if not (tn == bt or bt in tn or tn in bt): continue
        if re.search(r'instrumental|karaoke|remix|sped|slowed|live', x.get('trackName', ''), re.I) and 'remix' not in (T.get(int(cid)) or {}).get('version_used', '').lower(): continue
        cands.append(x)
    if not cands: out[cid] = dict(title=v['title'], n=v['n'], status='no synced lyrics found', target_s=target); continue
    def dd(x): return abs((x.get('duration') or 0) - target) if target else 0
    good = [x for x in cands if target is None or dd(x) <= 3.0]
    tier = 'duration within 3 s'
    if not good:
        good = [x for x in cands if dd(x) <= 8.0]; tier = 'duration within 8 s (check version)'
    if not good: out[cid] = dict(title=v['title'], n=v['n'], status='no version with matching duration', target_s=target, durations=sorted({x.get('duration') for x in cands})[:8]); continue
    res = []
    for x in good[:8]:
        a = analyze(x['syncedLyrics'], x.get('duration'))
        if a: a['lrclib_id'] = x['id']; a['lrc_duration'] = x.get('duration'); res.append(a)
    if not res: out[cid] = dict(title=v['title'], n=v['n'], status='lyrics too short to analyse', target_s=target); continue
    med_first = statistics.median(r['first_line_s'] for r in res)
    fh = [r['first_hook_s'] for r in res if r['first_hook_s'] is not None]
    med_hook = statistics.median(fh) if fh else None
    rep = min(res, key=lambda r: abs(r['first_line_s'] - med_first) + (abs((r['first_hook_s'] or 0) - (med_hook or 0)) if med_hook is not None else 0))
    rep = dict(rep)
    rep.update(status='ok', title=v['title'], n=v['n'], target_s=target, match_tier=tier, n_records=len(res),
               first_line_spread_s=round(max(r['first_line_s'] for r in res) - min(r['first_line_s'] for r in res), 2),
               first_hook_spread_s=(round(max(fh) - min(fh), 2) if len(fh) >= 2 else None),
               hook_votes=f"{sum(1 for r in res if r['has_returning_hook'])}/{len(res)}")
    out[cid] = rep
json.dump(out, open(SP + 'net/lrc_structure.json', 'w'))
ok = [v for v in out.values() if v.get('status') == 'ok']
print('tracks analysed:', len(ok), 'of', len(out), '| list tracks ok:', sum(1 for v in ok if v['n']), '| problems:', [(v['n'], v['title'], v['status']) for v in out.values() if v.get('status') != 'ok'])
print('match tiers:', {t: sum(1 for v in ok if v['match_tier'] == t) for t in {v['match_tier'] for v in ok}})
