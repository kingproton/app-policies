"""Build the final reference list (first 100 rap songs by first top-10 week, then rank) and
compute every count used in the findings. Writes CSV/JSON into the repo data folder and a stats JSON.
Counts are always reported as k / n_assessed, where n_assessed excludes 'unknown'."""
import json, csv, re, statistics, collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrections as C
from paths import WORK
from paths import REPO
cands = json.load(open(WORK + 'to_verify.json'))
status = {r['cid']: r for r in json.load(open(WORK + 'classification_status.json'))}
cm = {int(k): v for k, v in json.load(open(WORK + 'chart_metrics.json')).items()}
tracks = {int(k): v for k, v in json.load(open(WORK + 'tracks_merged.json')).items()} if os.path.exists(WORK + 'tracks_merged.json') else {}
col = json.load(open(WORK + 'collected.json'))

# ---------- 1. final list ----------
final, provisional_ids = [], []
for o in cands:
    st = status[o['cid']]['status']
    inc = st == 'rap' or (st == 'unverified' and o['prior'] == 'rap')
    if inc:
        final.append(o)
        if st != 'rap': provisional_ids.append(o['cid'])
    if len(final) == 100: break
boundary_next = []
seen = False
for o in cands:
    if o['cid'] == final[-1]['cid']: seen = True; continue
    if seen:
        st = status[o['cid']]['status']
        if st == 'rap' or (st == 'unverified' and o['prior'] == 'rap'): boundary_next.append(o)
    if len(boundary_next) >= 5: break
# unresolved close calls ranked ahead of the boundary (could push songs out if they turn out rap)
cut_cid = final[-1]['cid']
open_close = [o for o in cands if o['cid'] < cut_cid and status[o['cid']]['status'] == 'unverified' and o['prior'] == 'close']

# ---------- 2. genre tag ----------
SINGERS = ['SZA', 'The Weeknd', 'Tems', 'Chris Brown', 'Daniel Caesar', 'Bailey Zimmerman', 'Aqua', 'Fridayy', 'Giveon', 'Bad Bunny',
           'PinkPantheress', 'Amanda Reifer', '6LACK', 'Justin Bieber']
def best_class(cid):
    ev = col['classify'].get(str(cid), [])
    ev = sorted(ev, key=lambda e: {'high': 3, 'medium': 2, 'low': 1}.get(e['confidence'], 0))
    return ev[-1] if ev else None
def genre_tag(o, t):
    tags = []
    for s in SINGERS:
        if s.lower() in o['artist'].lower(): tags.append(f'feat./co-lead {s}')
    style = (t or {}).get('style_tag') or ''
    cross = {'pop_rap': 'pop', 'rnb_rap': 'R&B', 'dance_or_house_rap': 'dance/house', 'country_rap': 'country', 'afro_or_latin_rap': 'Latin/Afro', 'jersey_club': 'Jersey club'}
    if style in cross: tags.append(cross[style] + ' style')
    b = best_class(o['cid'])
    other = ' '.join((b or {}).get('other_genre_charts') or []).lower()
    for k, lab in [('country', 'country chart'), ('dance/electronic', 'dance chart'), ('pop airplay', 'pop radio'), ('latin', 'Latin chart')]:
        if k in other: tags.append(lab)
    # other genre charts shown in Wikipedia's chart table for the song (read directly)
    for c in status[o['cid']].get('wiki_genre_charts') or []:
        lab = {'Country': 'country chart', 'Rock & Alt': 'rock chart', 'Dance/Pop': 'dance chart', 'Dance/Electronic': 'dance chart', 'Christian': 'Christian chart',
               'Afrobeats': 'Afrobeats chart', 'Latin': 'Latin chart'}.get(c)
        if lab: tags.append(lab)
    return ('Rap — crossover (' + '; '.join(dict.fromkeys(tags)) + ')') if tags else 'Rap'
def class_source(cid):
    st = status[cid]
    b = best_class(cid)
    url = ''
    if b and b.get('source_urls'): url = b['source_urls'][0]
    ov = C.CLASSIFICATION_OVERRIDES.get(cid)                      # a targeted re-check replaces the earlier evidence and its URL
    if ov and ov.get('source_url'): url = ov['source_url']
    if st['basis'].startswith('Year-End'):
        yr = re.search(r'(\d{4})', st['basis']).group(1)
        url = f'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_Rap_Songs_of_{yr}'
    elif st['basis'].startswith('Hot Rap Songs peak'):
        url = 'https://en.wikipedia.org/wiki/' + re.search(r'Wikipedia table: (.*)\)', st['basis']).group(1).replace(' ', '_')
    return st['basis'][:140], url

# ---------- 3. album-bomb flag ----------
by_week_artist = collections.Counter()
def lead(a): return re.split(r' Featuring | & | X | With |, ', a)[0].strip()
for o in cands: by_week_artist[(o['first_top10'], lead(o['artist']))] += 1
def album_bomb(o): return by_week_artist[(o['first_top10'], lead(o['artist']))] >= 3

# ---------- 4. write reference list ----------
rows = []
for i, o in enumerate(final, 1):
    t = tracks.get(o['cid'])
    m = cm[o['cid']]
    basis, url = class_source(o['cid'])
    rows.append(dict(n=i, cid=o['cid'], title=o['title'], artists=o['artist'], first_top10=o['first_top10'], rank=o['rank'],
                     genre_tag=genre_tag(o, t), classification=status[o['cid']]['status'] if o['cid'] not in provisional_ids else 'rap (provisional — unverified)',
                     classification_basis=basis, classification_source=url, evidence_tier=status[o['cid']].get('tier'),
                     chart_source=f"https://www.billboard.com/charts/hot-100/{o['first_top10']}/",
                     debut_in_top10=m['debut_in_top10'], climbed_from=m['climbed_from'], peak=m['peak'], weeks_in_top10=m['weeks_in_top10'],
                     total_weeks=m['total_weeks'], album_bomb=album_bomb(o), lead_artist=lead(o['artist'])))
os.makedirs(REPO + 'data', exist_ok=True)
with open(REPO + 'data/reference_100.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# ---------- 5. measurements ----------
NON_VOCAL = {'Metro Boomin'}
def credit_names(a):
    a = a.replace('Tyler, The Creator', 'Tyler The Creator').replace('¥$: ', '')
    return [x.strip() for x in re.split(r' Featuring | With | & | X |, ', a) if x.strip()]
def return_type(r, t):
    if not any(d.get('basis') in ('source', 'page') for d in t.get('returns') or []):
        return 'not re-confirmed' if any(d.get('basis') == 'unconfirmed' for d in t.get('returns') or []) else None
    return C.RETURN_TYPES.get(r['cid'], 'uncoded')
def measured_cols(t):
    m = (t or {}).get('m') or {}; l = m.get('lyr') or {}; f = m.get('feel') or {}; b = m.get('bars') or {}
    return dict(m_runtime_s=m.get('runtime_s'), m_runtime_edition=m.get('runtime_edition'),
                m_catalog_track=m.get('runtime_track'), m_catalog_collection=m.get('runtime_collection'), m_catalog_release_date=m.get('runtime_release_date'),
                m_grid_bpm=f.get('grid_bpm'), m_pulse_bpm=f.get('pulse_bpm'), m_felt_bpm=f.get('felt_bpm'), m_feel_basis=f.get('basis'),
                m_feel_other_reading_bpm=(f.get('other_reading_bpm') if f.get('felt_bpm') == f.get('estimate_bpm') else f.get('estimate_bpm')) if f.get('felt_bpm') else None,
                m_feel_readings_bpm=' '.join(f'{x:g}' for x in sorted({round(v, 2) for v in (f.get('estimate_bpm'), f.get('other_reading_bpm')) if v})),
                m_feel_score=f.get('score'), m_feel_margin=f.get('margin'), m_feel_listing_conflict=f.get('listing_conflict'),
                m_listed_bpm=' '.join(f'{x:g}' for x in (f.get('listed_bpm') or [])),
                m_lyric_record=l.get('record_id'), m_lyric_basis=l.get('basis'), m_first_line_s=l.get('first_line_s'), m_first_line_kind=l.get('first_line_kind'),
                m_has_hook=l.get('has_hook'), m_first_hook_s=l.get('first_hook_s'), m_lines_before_hook=l.get('lines_before_hook'), m_hook_first=l.get('hook_first'),
                m_hook_count=l.get('hook_count'), m_hook_starts_s=' '.join(f'{x:g}' for x in (l.get('hook_starts') or [])), m_first_hook_len_s=l.get('first_hook_len_s'),
                m_first_verse_len_s=l.get('first_verse_len_s'), m_hook_return=l.get('hook_return'),
                m_verse_words_per_s=l.get('verse_words_per_s'), m_hook_words_per_s=(l.get('hook_words_per_s') if l.get('has_hook') else None),
                m_verse_sylls_per_s=l.get('verse_sylls_per_s'), m_verse_sylls_per_beat=(m.get('ride') or {}).get('verse_sylls_per_beat'),
                m_first_anchor_s=l.get('first_anchor_s'), m_anchor_is_hook=l.get('anchor_is_hook'), m_hook_before_first_verse=l.get('hook_before_first_verse'),
                m_first_section=l.get('first_section'), m_intro_len_s=l.get('intro_len_s'), m_intro_len_bars=b.get('intro_len'), m_n_verses=l.get('n_verses'),
                m_section_order=' '.join(f"{x['label']}@{x['start_s']:g}" for x in (l.get('sections') or [])),
                m_verse_lens_s=' '.join(f'{x:g}' for x in (l.get('verse_lens_s') or [])), m_hook_lens_s=' '.join(f'{x:g}' for x in (l.get('hook_lens_s') or [])),
                m_second_run=l.get('second_run_code'),
                m_longest_lyric_gap_s=l.get('longest_gap_s'), m_longest_lyric_gap_at_s=l.get('longest_gap_at_s'),
                m_bar_s=b.get('bar_s'), m_first_hook_bars=b.get('first_hook'), m_first_hook_len_bars=b.get('first_hook_len'), m_first_verse_len_bars=b.get('first_verse_len'))
mrows = []
for r in rows:
    t = tracks.get(r['cid']) or {}
    sm = t.get('samples') or []
    mrows.append(dict(n=r['n'], title=r['title'], version_used=t.get('version_used'), runtime=t.get('runtime_mmss'), runtime_s=t.get('runtime_s'),
                      runtime_status=t.get('runtime_status'), grid_bpm=t.get('grid_bpm'), felt_bpm=t.get('felt_bpm'), feel_basis=t.get('feel_basis'),
                      tempo_status=t.get('tempo_status'), tempo_note=t.get('tempo_note'),
                      tempo_listed='; '.join(f"{x.get('bpm')}" for x in (t.get('tempo_listed') or [])),
                      tempo_outliers_removed='; '.join(f"{x.get('bpm')}" for x in (t.get('tempo_outliers_removed') or [])),
                      style=t.get('style_tag'), opening=t.get('opening_element'), opening_basis=t.get('opening_basis'),
                      hook_before_first_verse=t.get('hook_first'), hook_before_first_verse_basis=t.get('hook_first_basis'), hook_status=t.get('hook_status'),
                      first_vocal=t.get('first_lead_vocal_time'), first_hook=t.get('first_hook_time'),
                      beat_switch=t.get('beat_switch'), beat_switch_basis=t.get('beat_switch_basis'), beat_switch_time=t.get('beat_switch_time'),
                      borrowings=' | '.join(f"{s.get('work', '')} [{s.get('borrow_type')}; {'credited' if s.get('credited', True) is True else ('uncredited' if s.get('credited', True) is False else 'credit not stated')}; {s.get('status')}]" for s in sm),
                      borrowing_documented=any(s.get('status') in ('confirmed', 'cited', 'page', 'not_reconfirmed') for s in sm),
                      return_change_type=return_type(r, t),
                      second_vocalist_credit=len([x for x in credit_names(r['artists']) if x not in NON_VOCAL]) >= 2,
                      guests_documented=len(t.get('features') or []),
                      album_bomb=r['album_bomb'], debut_in_top10=r['debut_in_top10'], climbed_from=r['climbed_from'],
                      weeks_in_top10=r['weeks_in_top10'], total_weeks=r['total_weeks'],
                      sourced_delivery_obs=sum(1 for d in (t.get('delivery') or []) if d.get('basis') in ('source', 'page')),
                      sourced_return_changes=sum(1 for d in (t.get('returns') or []) if d.get('basis') in ('source', 'page')),
                      verifier_flags=len(t.get('flagged') or []), verifier_rejections_applied='; '.join(t.get('verifier_applied') or []),
                      verified=t.get('verified'), studied=bool(t), **measured_cols(t)))
with open(REPO + 'data/track_measurements.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(mrows[0].keys())); w.writeheader(); w.writerows(mrows)

# ---------- 6. stats ----------
S = {}
studied = [r for r in mrows if r['studied']]
S['n_final'] = len(rows); S['n_studied'] = len(studied); S['provisional'] = provisional_ids
def q(vals):
    vals = sorted(vals)
    if not vals: return None
    qs = statistics.quantiles(vals, n=4) if len(vals) >= 4 else [vals[0], statistics.median(vals), vals[-1]]
    return dict(n=len(vals), median=statistics.median(vals), q1=qs[0], q3=qs[2], min=vals[0], max=vals[-1], mean=round(statistics.mean(vals), 1))
rt = [r['runtime_s'] for r in studied if r['runtime_s']]
S['runtime_all'] = q(rt)
S['runtime_le_180'] = sum(1 for x in rt if x <= 180); S['runtime_le_150'] = sum(1 for x in rt if x <= 150); S['runtime_ge_240'] = sum(1 for x in rt if x >= 240)
grp = lambda pred: [r2['runtime_s'] for r2, r in zip(mrows, rows) if r2['runtime_s'] and pred(r)]
S['runtime_album_bomb'] = q(grp(lambda r: r['album_bomb'])); S['runtime_not_bomb'] = q(grp(lambda r: not r['album_bomb']))
S['runtime_climbers'] = q(grp(lambda r: not r['debut_in_top10'])); S['runtime_debuts'] = q(grp(lambda r: r['debut_in_top10']))
S['runtime_drake'] = q(grp(lambda r: 'Drake' in r['artists'])); S['runtime_nondrake'] = q(grp(lambda r: 'Drake' not in r['artists']))
felt = [r['felt_bpm'] for r in studied if r['felt_bpm']]
grid = [r['grid_bpm'] for r in studied if r['grid_bpm']]
S['felt_bpm'] = q(felt); S['grid_bpm'] = q(grid)
S['felt_bands'] = dict(collections.Counter('<65' if x < 65 else '65-74' if x < 75 else '75-84' if x < 85 else '85-99' if x < 100 else '100-115' if x <= 115 else '>115' for x in felt))
S['tempo_status'] = dict(collections.Counter(r['tempo_status'] for r in studied))
S['runtime_status'] = dict(collections.Counter(r['runtime_status'] for r in studied))
S['style'] = dict(collections.Counter(r['style'] for r in studied))
def cnt(field, basis=None):
    c = collections.Counter()
    for r in studied:
        v = r[field]; b = r[basis] if basis else None
        c[(v, b)] += 1
    return {f'{k[0]}|{k[1]}': v for k, v in c.items()}
S['opening'] = cnt('opening', 'opening_basis'); S['hook_first'] = cnt('hook_before_first_verse', 'hook_before_first_verse_basis'); S['hook_status'] = dict(collections.Counter(r['hook_status'] for r in studied))
S['beat_switch'] = cnt('beat_switch', 'beat_switch_basis')
S['with_borrowing'] = sum(1 for r in studied if r['borrowing_documented']); S['with_guests'] = sum(1 for r in studied if r['guests_documented'])
S['timestamps_known'] = dict(first_vocal=sum(1 for r in studied if r['first_vocal']), first_hook=sum(1 for r in studied if r['first_hook']), beat_switch_time=sum(1 for r in studied if r['beat_switch_time']))
S['with_sourced_delivery'] = sum(1 for r in studied if r['sourced_delivery_obs']); S['with_sourced_returns'] = sum(1 for r in studied if r['sourced_return_changes'])
S['lead_artists'] = collections.Counter(r['lead_artist'] for r in rows).most_common(12)
S['drake_any_credit'] = sum(1 for r in rows if 'Drake' in r['artists'])
S['album_bomb_songs'] = sum(1 for r in rows if r['album_bomb']); S['debuts'] = sum(1 for r in rows if r['debut_in_top10'])
S['weeks_in_top10'] = q([r['weeks_in_top10'] for r in rows])
S['one_week_top10'] = sum(1 for r in rows if r['weeks_in_top10'] == 1)
S['boundary_next'] = [f"{o['first_top10']} #{o['rank']} {o['title']} — {o['artist']}" + (' (†-grade evidence: no direct rap-chart listing)' if status[o['cid']]['status'] != 'rap' else '') for o in boundary_next]
S['open_close_calls_before_cut'] = [f"{o['first_top10']} #{o['rank']} {o['title']} — {o['artist']}" for o in open_close]
S['cut'] = f"{final[-1]['first_top10']} #{final[-1]['rank']} {final[-1]['title']}"
S['span'] = f"{final[-1]['first_top10']} to {final[0]['first_top10']}"
json.dump(S, open(WORK + 'stats.json', 'w'), indent=1, default=str)
json.dump(rows, open(WORK + 'final_rows.json', 'w'), indent=1)
for k, v in S.items(): print(k, '=>', v)
