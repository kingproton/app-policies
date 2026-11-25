"""Genre-evidence matrix for every Hot 100 top-ten arrival in the window, from fetched pages only."""
import json, re, unicodedata, collections, os, sys
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpaths import SP, IN
L = json.load(open(SP + 'net/wiki_lists.json'))
A = json.load(open(SP + 'net/wiki_articles.json'))
status = {(r['title'], r['date']): r for r in json.load(open(IN + 'classification_status.json'))}
rows = json.load(open(IN + 'final_rows.json'))
final = {(r['title'], r['first_top10']) for r in rows}
def nz(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower().replace('&', 'and')
    t = re.sub(r'\(.*?\)', '', s); s = t if re.sub(r'[^a-z0-9]', '', t) else s
    return re.sub(r'[^a-z0-9]', '', s)
ALIAS = {'fen': 'fein', 'neenah': 'nenah'}
def key(t): k = nz(t); return ALIAS.get(k, k)
def art_ok(a, b):
    ta = [w for w in re.split(r'[^a-z0-9]+', unicodedata.normalize('NFKD', a).encode('ascii', 'ignore').decode().lower()) if len(w) > 2 and w not in ('featuring', 'and', 'with', 'the')]
    nb = nz(b)
    return any(w in nb for w in ta[:3])
def ye(listname, title, artist):
    return [(e['year'], e['rank']) for e in L[listname] if key(e['title']) == key(title) and art_ok(artist, e['artist'])]
# year-end Hot 100 lists
import urllib.parse
from parse_wiki_lists import rows_of, cell_content, plain, links, strip_markup
ye100 = []
for y in range(2021, 2026):
    fn = SP + 'net/wikipedia/' + urllib.parse.quote(f'Billboard Year-End Hot 100 singles of {y}'.replace(' ', '_'), safe='') + '.wiki'
    artist = ''
    for cells in rows_of(open(fn).read()):
        if not cells or '!HEADER' in cells[0]: continue
        cc = [cell_content(c) for c in cells]
        if not re.fullmatch(r'\d+', plain(cc[0])) or len(cc) < 2: continue
        tm = re.search(r'"(.*)"', strip_markup(cc[1]), re.S)
        if len(cc) >= 3: artist = plain(cc[2])
        ye100.append(dict(year=y, rank=int(plain(cc[0])), title=plain(tm.group(1) if tm else cc[1]), artist=artist))
L['yearend_hot100'] = ye100
print('YE Hot 100 rows:', collections.Counter(e['year'] for e in ye100))
GENRE_IDS = {'Billboardrandbhiphop': 'R&B/Hip-Hop', 'Billboardrapsongs': 'Rap', 'Billboardcountrysongs': 'Country', 'Billboardrocksongs': 'Rock & Alt',
             'Billboardlatinsongs': 'Latin', 'Billboarddanceelectronic': 'Dance/Electronic', 'Billboarddancepop': 'Dance/Pop', 'Billboardafrobeats': 'Afrobeats',
             'Billboardchristiansongs': 'Christian', 'Billboardhotalternativesongs': 'Alternative'}
out = []
for a in A:
    if a['date'] < '2021-08-07': continue
    st = status.get((a['title'], a['date']))
    ids = {GENRE_IDS[c] for c, p in (a.get('chart_ids') or []) if c in GENRE_IDS}
    rec = dict(date=a['date'], rank=a['rank'], title=a['title'], artist=a['artist'], in_final=(a['title'], a['date']) in final,
               prior=(st or {}).get('prior', 'nonrap'), status=(st or {}).get('status', 'pretagged_nonrap'),
               ye_rap=ye('yearend_rap', a['title'], a['artist']), ye_rbhh=ye('yearend_rbhh', a['title'], a['artist']),
               ye_hot100=ye('yearend_hot100', a['title'], a['artist']), wiki_genre_charts=sorted(ids), wiki_article=a.get('article'),
               wiki_infobox_genre=a.get('infobox_genre'), has_wiki=a.get('status') == 200)
    out.append(rec)
json.dump(out, open(SP + 'net/genre_matrix.json', 'w'), indent=1)
json.dump(L, open(SP + 'net/wiki_lists.json', 'w'), indent=1)
W = [r for r in out if r['date'] >= '2021-09-18']
print('arrivals in window:', len(W), '| in final 100:', sum(r['in_final'] for r in W))
print('\n== A. excluded songs that ARE on a year-end Hot Rap Songs list (possible wrong exclusions):')
for r in W:
    if not r['in_final'] and r['ye_rap']: print('  ', r['date'], r['rank'], r['title'], '|', r['artist'], '|', r['status'], r['ye_rap'])
print('\n== B. final-100 songs NOT on any year-end Hot Rap Songs list:')
for r in W:
    if r['in_final'] and not r['ye_rap']: print('  ', r['date'], r['rank'], r['title'], '| status', r['status'], '| YE R&B/HH', r['ye_rbhh'], '| YE Hot100', r['ye_hot100'], '| wiki charts', r['wiki_genre_charts'])
print('\n== C. excluded songs with R&B/Hip-Hop family evidence (rap vs R&B must be settled):')
for r in W:
    if not r['in_final'] and (r['ye_rbhh'] or 'R&B/Hip-Hop' in r['wiki_genre_charts']) and not r['ye_rap']:
        print('  ', r['date'], r['rank'], r['title'], '|', r['artist'][:30], '|', r['status'], '| YE R&B/HH', r['ye_rbhh'], '| YE Hot100', r['ye_hot100'], '| wiki', r['wiki_genre_charts'])
