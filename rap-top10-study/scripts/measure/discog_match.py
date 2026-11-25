"""Match Hot 100 top-10 arrivals to Wikipedia discography rows and read off the Hot Rap Songs / R&B-Hip-Hop peaks.
A row matches when (1) the normalised title is equal, (2) the discography's US (Hot 100) peak equals the song's peak in the
chart data, and (3) the row belongs to this song: the page's artist is named in the song's Billboard credit, or the row's
own credit text names the song's lead artist, or the row has the same Hot 100 and R&B/Hip-Hop peaks as a row already
accepted (a producer's production discography). Rule 3 keeps a same-title song by other artists out: the 2009 "Forever"
also peaked at No. 8, like the 2022 Lil Baby song.)"""
import json, re, unicodedata, sys
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpaths import SP, IN
D = json.load(open(SP + 'net/discog_peaks.json')); G = json.load(open(SP + 'net/genre_matrix.json'))
allc = json.load(open(IN + 'all.json'))
def nz(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\([^)]*\)', '', s)
    return re.sub(r'[^a-z0-9]+', '', s)
ALIAS = {'imdatna': 'imdatnigga', 'fen': 'fein', 'neenah': 'neenah', 'pussymillions': 'pussymillions', 'pmillions': 'pussymillions',
         'superherovillains': 'superhero', 'superhero': 'superhero', 'ilikeyou': 'ilikeyou', 'boysaliarpt2': 'boysaliarpt2'}
peak = {}
for wk in allc:
    if wk['date'] < '2021-01-01': continue
    for r in wk['data']:
        k = (nz(r['song']), nz(r['artist'].split(' Featuring')[0].split(' &')[0].split(',')[0].split(' X ')[0].split(' With')[0]))
        peak[k] = min(peak.get(k, 999), r['this_week'])
idx = {}
for page, rows in D.items():
    for r in rows:
        idx.setdefault(r['key'], []).append((page, r))
        k2 = nz(r['title'])
        if k2 != r['key']: idx.setdefault(k2, []).append((page, r))
def page_artist(page):
    a = page.replace('%2C', ',')
    for suf in ('_singles_discography', '_production_discography', '_discography'): a = a.replace(suf, '')
    return nz(a.replace('_', ' ').replace('$', 's'))
out = []
for g in G:
    kt = nz(g['title']); kt = ALIAS.get(kt, kt)
    ka = nz(g['artist'].split(' Featuring')[0].split(' &')[0].split(',')[0].split(' X ')[0].split(' With')[0])
    pk = peak.get((nz(g['title']), ka))
    hits = []
    for key in {kt, nz(g['title'])}:
        for page, r in idx.get(key, []):
            if isinstance(r.get('us'), int) and pk is not None and r['us'] == pk:
                hits.append(dict(page=page, us=r.get('us'), rbhh=r.get('rbhh'), rap=r.get('rap'), has_rap_col=r.get('has_rap_col'), feat=r.get('feat') or ''))
    seen = set(); hits = [h for h in hits if not (h['page'] in seen or seen.add(h['page']))]
    def flat(x): return re.sub(r'[^a-z0-9]+', '', unicodedata.normalize('NFKD', x.replace('$', 's')).encode('ascii', 'ignore').decode().lower())
    credit = flat(g['artist'])
    own = [h for h in hits if page_artist(h['page']) in credit or (ka and ka in flat(re.sub(r'^.*?"', '', h['feat'])))]
    peaks_own = {(h['us'], h['rbhh']) for h in own}
    dropped = [h['page'] for h in hits if h not in own and (h['us'], h['rbhh']) not in peaks_own]
    hits = [h for h in hits if h in own or (h['us'], h['rbhh']) in peaks_own]
    for h in hits: h.pop('feat', None)
    rapcol = [h for h in hits if h['has_rap_col']]
    raps = sorted({h['rap'] for h in rapcol if isinstance(h['rap'], int)})
    dash = [h['page'] for h in rapcol if h['rap'] == '—']
    out.append(dict(date=g['date'], rank=g['rank'], title=g['title'], artist=g['artist'], in_final=g['in_final'], status=g['status'], hot100_peak=pk,
                    discog_rap_peak=raps[0] if raps else None, discog_rap_pages=[h['page'] for h in rapcol if isinstance(h['rap'], int)],
                    discog_rap_dash_pages=dash, discog_rbhh=sorted({h['rbhh'] for h in hits if isinstance(h.get('rbhh'), int)}),
                    discog_rbhh_dash=[h['page'] for h in hits if h.get('rbhh') == '—'], n_rows=len(hits), rows_dropped_other_artist=dropped, ye_rap=g['ye_rap'], ye_rbhh=g['ye_rbhh'], ye_hot100=g['ye_hot100'],
                    wiki_genre_charts=g['wiki_genre_charts']))
json.dump(out, open(SP + 'net/discog_match.json', 'w'), indent=0, ensure_ascii=False)
fin = [o for o in out if o['in_final']]
print('final list:', len(fin), '| with a Hot Rap Songs peak in a discography table:', sum(1 for o in fin if o['discog_rap_peak']),
      '| with year-end rap entry:', sum(1 for o in fin if o['ye_rap']), '| either:', sum(1 for o in fin if o['discog_rap_peak'] or o['ye_rap']))
print('\nFINAL-LIST songs with neither:')
for o in fin:
    if not o['discog_rap_peak'] and not o['ye_rap']:
        print('  ', o['date'], o['rank'], o['title'], '|', o['artist'][:40], '| rows', o['n_rows'], '| dash pages', o['discog_rap_dash_pages'], '| rbhh', o['discog_rbhh'])
print('\nFINAL-LIST songs with a DASH in a rap column somewhere:')
for o in fin:
    if o['discog_rap_dash_pages']:
        print('  ', o['date'], o['rank'], o['title'], '| rap peak elsewhere', o['discog_rap_peak'], o['discog_rap_pages'], '| dash', o['discog_rap_dash_pages'], '| ye_rap', o['ye_rap'])
print('\nNON-FINAL arrivals since 2021-09-11 with a rap peak or rap-column row:')
for o in out:
    if not o['in_final'] and o['date'] >= '2021-09-11' and (o['discog_rap_peak'] or o['discog_rap_dash_pages']):
        print('  ', o['date'], o['rank'], o['title'][:28].ljust(28), '|', o['artist'][:30].ljust(30), '| rap', o['discog_rap_peak'], o['discog_rap_pages'], '| dash', o['discog_rap_dash_pages'], '| rbhh', o['discog_rbhh'], o['discog_rbhh_dash'], '| status', o['status'])
