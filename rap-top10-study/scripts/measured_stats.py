"""Counts behind the measured findings (runtime, first vocal line, hook timing, section lengths, density, felt tempo).

Every count is k / n assessed. A track is "assessed" for a measure only when that measure exists for it with a usable
basis (see measure_merge.py). Lyric-timing measures use basis A, J or G; X is excluded. Feel measures state which bases
they include. Output: measured_stats.json in the working directory.
"""
import json, os, sys, statistics, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
rows = json.load(open(WORK + 'final_rows.json'))
T = {int(k): v for k, v in json.load(open(WORK + 'tracks_merged.json')).items()}
R = [(r, T.get(r['cid']) or {}) for r in rows]


def mmss(s):
    if s is None: return '?'
    s = int(round(s)); return f"{s // 60}:{s % 60:02d}"


def qd(v, fmt=None):
    v = sorted(x for x in v if x is not None)
    if not v: return dict(n=0)
    if len(v) < 4: d = dict(n=len(v), median=statistics.median(v), min=v[0], max=v[-1])
    else:
        q = statistics.quantiles(v, n=4); d = dict(n=len(v), median=statistics.median(v), q1=q[0], q3=q[2], min=v[0], max=v[-1])
    if fmt: d = {k: (fmt(x) if k != 'n' else x) for k, x in d.items()}
    else: d = {k: (round(x, 2) if k != 'n' else x) for k, x in d.items()}
    return d


def hbpm(x): return f"{round(float(x) * 2) / 2:g}"          # nearest half BPM
_dup = {k for k, v in collections.Counter(r['title'] for r in rows).items() if v > 1}
def ttl(r):
    """Title, with the lead artist added when two list songs share it."""
    return f"{r['title']} ({r['lead_artist']})" if r['title'] in _dup else r['title']
def M(t): return t.get('m') or {}
def lyr(t):
    l = M(t).get('lyr')
    return l if l and l.get('basis') in ('A', 'J', 'G') else None
def feel(t, bases=('M',)):
    f = M(t).get('feel')
    return f if f and f.get('basis') in bases else None
def who(r): return 'Drake' if 'Drake' in r['artists'] else ('Kendrick Lamar' if 'Kendrick' in r['artists'] else r['lead_artist'])
def tag(r, l=None): return f"{r['title']} ({who(r)})"


GROUPS = {
    'all': lambda r, t: True,
    'climbers': lambda r, t: not r['debut_in_top10'],
    'debuts': lambda r, t: r['debut_in_top10'],
    'album_bomb': lambda r, t: r['album_bomb'],
    'not_bomb': lambda r, t: not r['album_bomb'],
    'drake_credit': lambda r, t: 'Drake' in r['artists'],
    'no_drake': lambda r, t: 'Drake' not in r['artists'],
}
STYLE = {'verse_led': {'boom_bap_or_verse_led'}, 'trap': {'trap', 'melodic_trap'}, 'drill': {'drill'}, 'bounce': {'west_coast_bounce'}, 'pop_rap': {'pop_rap'}}
for k, tags in STYLE.items(): GROUPS['style_' + k] = (lambda tags: (lambda r, t: t.get('style_tag') in tags))(tags)

OUT = {'groups': {}}
for g, f in GROUPS.items():
    S = [(r, t) for r, t in R if f(r, t)]
    d = dict(n_songs=len(S))
    # runtime
    rt = [M(t).get('runtime_best_s') for r, t in S if M(t).get('runtime_best_s')]
    d['runtime'] = qd(rt, mmss); d['runtime_le_3min'] = f"{sum(1 for x in rt if x <= 180)}/{len(rt)}"; d['runtime_ge_4min'] = f"{sum(1 for x in rt if x >= 240)}/{len(rt)}"
    d['runtime_lt_2m30'] = f"{sum(1 for x in rt if x < 150)}/{len(rt)}"
    # lyric timing
    L = [(r, t, lyr(t)) for r, t in S if lyr(t)]
    d['n_lyric'] = len(L)
    fl = [l['first_line_s'] for r, t, l in L]
    d['first_line'] = qd(fl)
    for lim in (1, 2, 5, 10, 15):
        d[f'first_line_le_{lim}s'] = f"{sum(1 for x in fl if x <= lim)}/{len(fl)}"
    d['first_line_gt_15s'] = f"{sum(1 for x in fl if x > 15)}/{len(fl)}"
    H = [(r, t, l) for r, t, l in L if l['has_hook']]
    d['has_hook'] = f"{len(H)}/{len(L)}"; d['no_hook'] = f"{len(L) - len(H)}/{len(L)}"
    hf = [(r, t, l) for r, t, l in H if l['hook_first'] is True]
    d['hook_first'] = f"{len(hf)}/{len(H)}"; d['hook_first_of_all'] = f"{len(hf)}/{len(L)}"
    lb = [l['lines_before_hook'] for r, t, l in H if l['lines_before_hook'] is not None]
    d['lines_before_hook'] = qd(lb)
    d['lines_before_hook_bands'] = {b: sum(1 for x in lb if lo <= x <= hi) for b, lo, hi in (('0', 0, 0), ('1-3', 1, 3), ('4-8', 4, 8), ('9-16', 9, 16), ('17-32', 17, 32), ('33+', 33, 9999))}
    fh = [l['first_hook_s'] for r, t, l in H if l['first_hook_s'] is not None]
    d['first_hook'] = qd(fh, mmss); d['first_hook_s'] = qd(fh)
    for lim in (15, 30, 45, 60, 90):
        d[f'first_hook_le_{lim}s'] = f"{sum(1 for x in fh if x <= lim)}/{len(L)}"       # of all assessed songs, hookless ones included
    d['first_hook_gt_90s'] = f"{sum(1 for x in fh if x > 90)}/{len(L)}"
    an = [l['first_anchor_s'] for r, t, l in L if l.get('first_anchor_s') is not None]
    d['first_anchor'] = qd(an, mmss); d['first_anchor_s'] = qd(an)
    for lim in (15, 30, 45, 60):
        d[f'first_anchor_le_{lim}s'] = f"{sum(1 for x in an if x <= lim)}/{len(L)}"
    ah = [l['anchor_is_hook'] for r, t, l in H if l.get('anchor_is_hook') is not None]
    d['anchor_is_hook'] = f"{sum(1 for x in ah if x)}/{len(ah)}"
    hbv = [l['hook_before_first_verse'] for r, t, l in H if l.get('hook_before_first_verse') is not None]
    d['hook_before_first_verse'] = f"{sum(1 for x in hbv if x)}/{len(hbv)}"
    d['first_section'] = dict(collections.Counter(l.get('first_section') for r, t, l in L if l.get('first_section')))
    d['intro_len_s'] = qd([l['intro_len_s'] for r, t, l in L if l.get('intro_len_s') is not None])
    d['reviewer_confidence'] = dict(collections.Counter(l.get('reviewer_confidence') for r, t, l in L if l.get('reviewer_confidence')))
    # section map (reviewer): verse counts, verse 2 against verse 1, last hook against first hook
    SM = [(r, t, l) for r, t, l in L if l.get('section_labels')]
    d['n_section_map'] = len(SM)
    d['n_verses'] = dict(sorted(collections.Counter(min(l['n_verses'], 4) for r, t, l in SM).items()))
    v12 = [(l['verse_lens_s'][0], l['verse_lens_s'][1]) for r, t, l in SM if len(l.get('verse_lens_s') or []) >= 2]
    d['verse2_shorter'] = f"{sum(1 for a, b in v12 if b < 0.85 * a)}/{len(v12)}"; d['verse2_similar'] = f"{sum(1 for a, b in v12 if 0.85 * a <= b <= 1.15 * a)}/{len(v12)}"; d['verse2_longer'] = f"{sum(1 for a, b in v12 if b > 1.15 * a)}/{len(v12)}"
    h1l = [(l['hook_lens_s'][0], l['hook_lens_s'][-1]) for r, t, l in SM if len(l.get('hook_lens_s') or []) >= 2]
    d['last_hook_longer'] = f"{sum(1 for a, b in h1l if b > 1.25 * a)}/{len(h1l)}"; d['last_hook_shorter'] = f"{sum(1 for a, b in h1l if b < 0.75 * a)}/{len(h1l)}"; d['last_hook_similar'] = f"{sum(1 for a, b in h1l if 0.75 * a <= b <= 1.25 * a)}/{len(h1l)}"
    d['has_bridge'] = f"{sum(1 for r, t, l in SM if l.get('has_bridge'))}/{len(SM)}"; d['has_pre_hook'] = f"{sum(1 for r, t, l in SM if l.get('has_pre_hook'))}/{len(SM)}"; d['has_post_hook'] = f"{sum(1 for r, t, l in SM if l.get('has_post_hook'))}/{len(SM)}"
    d['ends_on'] = dict(collections.Counter(l.get('ends_on') for r, t, l in SM))
    d['verse1_len_s_map'] = qd([l['verse_lens_s'][0] for r, t, l in SM if l.get('verse_lens_s')])
    d['hook1_len_s_map'] = qd([l['hook_lens_s'][0] for r, t, l in SM if l.get('hook_lens_s')])
    # riding the beat: syllables per felt beat and felt beats per lyric line (resolved feel only)
    RD = [(r, t, M(t)['ride']) for r, t in S if M(t).get('ride') and lyr(t) and feel(t, ('M', 'L', 'I'))]
    d['n_ride'] = len(RD)
    d['verse_sylls_per_beat'] = qd([x['verse_sylls_per_beat'] for r, t, x in RD if x.get('verse_sylls_per_beat')])
    d['hook_sylls_per_beat'] = qd([x['hook_sylls_per_beat'] for r, t, x in RD if x.get('hook_sylls_per_beat')])
    lb_ = [x['verse_line_beats'] for r, t, x in RD if x.get('verse_line_beats')]
    d['verse_line_beats'] = qd(lb_)
    d['verse_line_beats_bands'] = {k: sum(1 for x in lb_ if lo <= x < hi) for k, lo, hi in (('under 1.5', 0, 1.5), ('1.5-2.5 (about 2)', 1.5, 2.5), ('2.5-3.5', 2.5, 3.5), ('3.5-4.5 (about 4)', 3.5, 4.5), ('4.5+', 4.5, 99))}
    d['verse_line_gap_s'] = qd([l.get('verse_median_line_gap_s') for r, t, l in L if l.get('verse_median_line_gap_s')])
    for cls in ('slow', 'mid', 'fast'):
        # only tracks that have a verse rate (a record with no mapped verse has none), so n matches the medians
        C_ = [(r, t, x) for r, t, x in RD if M(t)['feel']['feel_class'] == cls and x.get('verse_sylls_per_beat')]
        d[f'ride_{cls}'] = dict(n=len(C_), sylls_per_beat=qd([x['verse_sylls_per_beat'] for r, t, x in C_ if x.get('verse_sylls_per_beat')]).get('median'),
                               sylls_per_s=qd([lyr(t).get('verse_sylls_per_s') for r, t, x in C_ if lyr(t).get('verse_sylls_per_s')]).get('median'),
                               line_beats=qd([x['verse_line_beats'] for r, t, x in C_ if x.get('verse_line_beats')]).get('median'))
    hc = collections.Counter(min(l['hook_count'], 5) for r, t, l in H)
    d['hook_count'] = {('5+' if k == 5 else str(k)): v for k, v in sorted(hc.items())}
    hl = [l['first_hook_len_s'] for r, t, l in H if l.get('first_hook_len_s')]
    d['first_hook_len_s'] = qd(hl)
    vl = [l.get('first_verse_len_s') for r, t, l in L if l.get('first_verse_len_s')]
    d['first_verse_len_s'] = qd(vl)
    vw = [l.get('verse_words_per_s') for r, t, l in L if l.get('verse_words_per_s')]; hw = [l.get('hook_words_per_s') for r, t, l in H if l.get('hook_words_per_s')]
    d['verse_words_per_s'] = qd(vw); d['hook_words_per_s'] = qd(hw)
    both = [(l['verse_words_per_s'], l['hook_words_per_s']) for r, t, l in H if l.get('verse_words_per_s') and l.get('hook_words_per_s')]
    d['verse_denser_than_hook'] = f"{sum(1 for a, b in both if a > b)}/{len(both)}"
    d['verse_sylls_per_s'] = qd([l.get('verse_sylls_per_s') for r, t, l in L if l.get('verse_sylls_per_s')])
    lg = [l.get('longest_gap_s') for r, t, l in L if l.get('longest_gap_s') is not None]
    d['gap_ge_8s'] = f"{sum(1 for x in lg if x >= 8)}/{len(lg)}"; d['gap_ge_12s'] = f"{sum(1 for x in lg if x >= 12)}/{len(lg)}"
    d['lyric_basis'] = dict(collections.Counter(l['basis'] for r, t, l in L))
    d['hook_return'] = dict(collections.Counter(l.get('hook_return') for r, t, l in H if l.get('hook_return')))
    d['first_line_kind'] = dict(collections.Counter(l.get('first_line_kind') for r, t, l in L if l.get('first_line_kind')))
    # feel
    allf = [(r, t, M(t).get('feel')) for r, t in S if M(t).get('feel')]
    d['n_clip'] = len(allf); d['feel_basis'] = dict(collections.Counter(f['basis'] for r, t, f in allf))
    for lab, bases in (('clear', ('M',)), ('clear_or_leaning', ('M', 'L')), ('all_resolved', ('M', 'L', 'I'))):
        F = [f for r, t, f in allf if f['basis'] in bases]
        d[f'felt_{lab}'] = qd([f['felt_bpm'] for f in F])
        d[f'feel_class_{lab}'] = dict(collections.Counter(f['feel_class'] for f in F))
    # bars (felt grid) where both lyric timing and a resolved feel exist
    B = [(r, t, M(t)['bars'], lyr(t)) for r, t in S if M(t).get('bars') and lyr(t) and feel(t, ('M', 'L', 'I'))]
    d['n_bars'] = len(B)
    d['first_hook_bars'] = qd([b['first_hook'] for r, t, b, l in B if l['has_hook'] and b.get('first_hook') is not None])
    hb = [b['first_hook_len'] for r, t, b, l in B if l['has_hook'] and b.get('first_hook_len')]
    d['first_hook_len_bars'] = qd(hb)
    d['hook_len_bar_bands'] = {k: sum(1 for x in hb if lo <= x < hi) for k, lo, hi in (('under 3', 0, 3), ('3-5 (about 4)', 3, 5), ('5-7', 5, 7), ('7-9 (about 8)', 7, 9), ('9-13', 9, 13), ('13+', 13, 999))}
    vb = [b['verse_lens'][0] for r, t, b, l in B if b.get('verse_lens')] or [b['first_verse_len'] for r, t, b, l in B if b.get('first_verse_len')]
    hb2 = [b['hook_lens'][0] for r, t, b, l in B if b.get('hook_lens')]
    d['hook1_len_bars_map'] = qd(hb2)
    d['hook1_len_bar_bands_map'] = {k: sum(1 for x in hb2 if lo <= x < hi) for k, lo, hi in (('under 3', 0, 3), ('3-5 (about 4)', 3, 5), ('5-7', 5, 7), ('7-9 (about 8)', 7, 9), ('9-13', 9, 13), ('13+', 13, 999))}
    ib = [b['intro_len'] for r, t, b, l in B if b.get('intro_len') is not None]
    d['intro_len_bars'] = qd(ib)
    d['intro_len_bar_bands'] = {k: sum(1 for x in ib if lo <= x < hi) for k, lo, hi in (('under 3', 0, 3), ('3-5 (about 4)', 3, 5), ('5-7', 5, 7), ('7-9 (about 8)', 7, 9), ('9+', 9, 999))}
    d['first_verse_len_bars'] = qd(vb)
    d['verse_len_bar_bands'] = {k: sum(1 for x in vb if lo <= x < hi) for k, lo, hi in (('under 6', 0, 6), ('6-10 (about 8)', 6, 10), ('10-14 (about 12)', 10, 14), ('14-18 (about 16)', 14, 18), ('18-26', 18, 26), ('26+', 26, 999))}
    OUT['groups'][g] = d

# ---------------- named lists (list tracks only)
L = [(r, t, lyr(t)) for r, t in R if lyr(t)]
def hk(l): return f"{mmss(l['first_hook_s'])} after {l['lines_before_hook']} line{'s' if l['lines_before_hook'] != 1 else ''} [{l['basis']}]"
OUT['hook_first_list'] = [f"#{r['n']} {tag(r)}: hook at {hk(l)}" for r, t, l in L if l['has_hook'] and l['hook_first']]
OUT['hook_before_verse_list'] = [f"#{r['n']} {tag(r)}: hook at {hk(l)}" for r, t, l in L if l['has_hook'] and l.get('hook_before_first_verse')]
OUT['anchor_before_hook_list'] = [f"#{r['n']} {tag(r)}: anchor at {mmss(l['first_anchor_s'])}, hook at {mmss(l['first_hook_s'])}" for r, t, l in L if l['has_hook'] and l.get('anchor_is_hook') is False]
OUT['hook_late_list'] = [f"#{r['n']} {tag(r)}: hook at {hk(l)}" for r, t, l in sorted(L, key=lambda x: -(x[2]['first_hook_s'] or 0)) if l['has_hook'] and (l['first_hook_s'] or 0) > 75]
OUT['no_hook_list'] = [f"#{r['n']} {tag(r)} [{l['basis']}; {mmss(M(t).get('runtime_s'))}; style {t.get('style_tag')}]" for r, t, l in L if not l['has_hook']]
OUT['late_first_line'] = [f"#{r['n']} {tag(r)}: first line at {mmss(l['first_line_s'])} [{l['basis']}]" for r, t, l in sorted(L, key=lambda x: -x[2]['first_line_s']) if l['first_line_s'] > 10]
OUT['immediate_first_line'] = [f"#{r['n']} {r['title']}" for r, t, l in L if l['first_line_s'] <= 1.0]
OUT['lyric_missing'] = [f"\"{ttl(r)}\"" for r, t in R if not M(t).get('lyr')]
OUT['lyric_unusable'] = [f"#{r['n']} {r['title']}" for r, t in R if M(t).get('lyr') and M(t)['lyr'].get('basis') == 'X']
OUT['lyric_adjudicated'] = [f"#{r['n']} {r['title']}: {l.get('resolution')} ({'; '.join(l.get('disagreed_on') or [])})" for r, t, l in L if l['basis'] == 'J']
OUT['hook_return_lists'] = {cat: [f"\"{ttl(r)}\"" for r, t, l in L if l['has_hook'] and l.get('hook_return') == cat and l['basis'] in ('A', 'J')] for cat in ('identical', 'minor_variation', 'extended', 'shortened', 'new_lyrics')}
OUT['verse_first_section_list'] = [f"\"{ttl(r)}\"" for r, t, l in L if l.get('first_section') == 'verse']
OUT['hook_first_section_list'] = [f"\"{ttl(r)}\"" for r, t, l in L if l.get('first_section') == 'hook']
OUT['hook_count_4plus'] = [f"#{r['n']} {r['title']} ({l['hook_count']})" for r, t, l in L if l['has_hook'] and l['hook_count'] >= 4]
OUT['dense_verses'] = [f"\"{ttl(r)}\" ({who(r)}) {l['verse_words_per_s']:.1f}" for r, t, l in sorted(L, key=lambda x: -(x[2].get('verse_words_per_s') or 0))[:8]]
OUT['sparse_verses'] = [f"\"{ttl(r)}\" ({who(r)}) {l['verse_words_per_s']:.1f}" for r, t, l in sorted([x for x in L if x[2].get('verse_words_per_s')], key=lambda x: x[2]['verse_words_per_s'])[:8]]
OUT['long_gaps'] = [f"\"{ttl(r)}\" ({l['longest_gap_s']:.0f} s with no lyric line from {mmss(l['longest_gap_at_s'])})" for r, t, l in sorted(L, key=lambda x: -(x[2].get('longest_gap_s') or 0)) if (l.get('longest_gap_s') or 0) >= 12]
# agreement between LRCLIB records of the same track (where two or more matched the duration)
multi = [l for r, t, l in L if (l.get('n_records_agreeing') or 0) >= 2]
fsp = [l['first_line_spread_s'] for l in multi if l.get('first_line_spread_s') is not None]
hsp = [l['first_hook_spread_s'] for l in multi if l.get('first_hook_spread_s') is not None]
OUT['record_agreement'] = dict(tracks_with_2plus_records=len(multi), first_line_spread=qd(fsp), first_line_within_1s=f"{sum(1 for x in fsp if x <= 1.0)}/{len(fsp)}",
                               first_hook_spread=qd(hsp), first_hook_within_2s=f"{sum(1 for x in hsp if x <= 2.0)}/{len(hsp)}")
OUT['match_tier'] = dict(collections.Counter(l.get('match_tier') for r, t, l in L))
# feel lists
F = [(r, t, M(t).get('feel')) for r, t in R if M(t).get('feel')]
OUT['clip_missing'] = [f"#{r['n']} {r['title']}" for r, t in R if not M(t).get('feel')]
OUT['feel_fast'] = [f"#{r['n']} {tag(r)}: felt {hbpm(f['felt_bpm'])} [{f['basis']}]" for r, t, f in F if f['feel_class'] == 'fast']
OUT['feel_mid'] = [f"#{r['n']} {tag(r)}: felt {hbpm(f['felt_bpm'])} [{f['basis']}]" for r, t, f in F if f['feel_class'] == 'mid']
OUT['feel_unresolved'] = [f"\"{ttl(r)}\" ({hbpm(min(f['estimate_bpm'], f['other_reading_bpm']))} or {hbpm(max(f['estimate_bpm'], f['other_reading_bpm']))})" for r, t, f in F if f['basis'] == '?' and not f.get('listing_conflict')]
# an unclear clip reading that no published listing matches (at the same, half or double tempo): shown, not resolved
OUT['feel_listing_conflict'] = [f"\"{ttl(r)}\" (clip {hbpm(f['felt_bpm_from_clip'])}, listed {' and '.join(f'{v:g}' for v in f['listed_bpm'])})" for r, t, f in F if f.get('listing_conflict')]
OUT['feel_range_lower_score'] = [f"\"{ttl(r)}\"" for r, t, f in F if f['basis'] == 'I' and f['felt_bpm'] != f['estimate_bpm']]
OUT['feel_range_leaned_away'] = [f"\"{ttl(r)}\" (toward {hbpm(f['estimate_bpm'])}, margin {f['margin']:.2f})" for r, t, f in F if f['basis'] == 'I' and f.get('confidence') == 'leaning' and f['felt_bpm'] != f['estimate_bpm']]
OUT['feel_range_unclear_max_margin'] = max([f['margin'] for r, t, f in F if f['basis'] == 'I' and f.get('confidence') != 'leaning'] or [0])
OUT['feel_range_rule'] = [f"\"{ttl(r)}\" {hbpm(f['felt_bpm'])} (not {hbpm(f['other_reading_bpm'] if f['felt_bpm'] == f['estimate_bpm'] else f['estimate_bpm'])})" for r, t, f in F if f['basis'] == 'I']
OUT['feel_leaning'] = [f"\"{ttl(r)}\" {hbpm(f['felt_bpm'])} (not {hbpm(f['other_reading_bpm'] if f['felt_bpm'] == f['estimate_bpm'] else f['estimate_bpm'])})" for r, t, f in F if f['basis'] == 'L']
OUT['feel_displaced'] = [f"#{r['n']} {r['title']}" for r, t, f in F if f['basis'] == 'M' and f.get('displaced_backbeat')]
OUT['feel_ranges'] = {c: [hbpm(min(f['felt_bpm'] for r, t, f in F if f['basis'] == 'M' and f['feel_class'] == c)), hbpm(max(f['felt_bpm'] for r, t, f in F if f['basis'] == 'M' and f['feel_class'] == c))]
                      for c in ('slow', 'mid', 'fast') if any(f['basis'] == 'M' and f['feel_class'] == c for r, t, f in F)}
vs = [l['verse_sylls_per_s'] for r, t, l in L if l.get('verse_sylls_per_s')]
OUT['verse_sylls_share'] = dict(n=len(vs), above_4_8=sum(1 for x in vs if x > 4.8), below_3_0=sum(1 for x in vs if x < 3.0))
hs = [l['hook_sylls_per_s'] for r, t, l in L if l['has_hook'] and l.get('hook_sylls_per_s')]
OUT['hook_sylls_per_s'] = qd(hs)
OUT['slow_by_artist'] = dict(collections.Counter(who(r) for r, t, f in F if f['basis'] == 'M' and f['feel_class'] == 'slow').most_common(8))
# pulse against earlier listings: does any listed BPM sit within 2.5% of the measured pulse, its half or its double?
agree, disagree, nolist = [], [], []; n_conf_list = 0; clear_dis = []
for r, t, f in F:
    lv = sorted({float(x['bpm']) for x in t.get('tempo_listed') or [] if x.get('bpm')})
    if not lv: nolist.append(r['title']); continue
    p = f['pulse_bpm']
    ok = any(abs(v - p * k) / (p * k) <= 0.025 for v in lv for k in (0.5, 1.0, 2.0))
    (agree if ok else disagree).append(f"{r['title']} (pulse {p:g}; listed {', '.join(f'{v:g}' for v in lv)})")
    if not ok:
        if max(lv) / min(lv) > 1.025: n_conf_list += 1          # the listings themselves disagree
        if f['basis'] == 'M': clear_dis.append(f"\"{ttl(r)}\"")
# a mismatch whose pulse does match a listing that the earlier pass set aside as an outlier
dis_removed = []
for r, t, f in F:
    lv = sorted({float(x['bpm']) for x in t.get('tempo_listed') or [] if x.get('bpm')})
    rm = [float(x['bpm']) for x in t.get('tempo_outliers_removed') or [] if isinstance(x, dict) and x.get('bpm')]
    if not lv or not rm: continue
    p = f['pulse_bpm']
    if not any(abs(v - p * k) / (p * k) <= 0.025 for v in lv for k in (0.5, 1.0, 2.0)) and any(abs(v - p * k) / (p * k) <= 0.025 for v in rm for k in (0.5, 1.0, 2.0)):
        dis_removed.append(f"\"{ttl(r)}\"")
OUT['pulse_vs_listings'] = dict(agree=len(agree), disagree=len(disagree), no_listing=len(nolist), disagree_list=disagree,
                                disagree_listings_conflict=n_conf_list, disagree_single_listing=len(disagree) - n_conf_list, disagree_clear=clear_dis,
                                disagree_matches_removed_outlier=dis_removed)
# how published listings relate to the felt tempo (clear readings only)
rel = collections.Counter()
for r, t, f in F:
    if f['basis'] != 'M': continue
    lv = sorted({float(x['bpm']) for x in t.get('tempo_listed') or [] if x.get('bpm')})
    if not lv: rel['no listing'] += 1; continue
    ks = set()
    for v in lv:
        for k, lab in ((1.0, 'listed at the felt tempo'), (2.0, 'listed at double the felt tempo'), (0.5, 'listed at half the felt tempo')):
            if abs(v - f['felt_bpm'] * k) / (f['felt_bpm'] * k) <= 0.025: ks.add(lab)
    rel[' and '.join(sorted(ks)) if ks else 'listing matches neither'] += 1
OUT['listing_vs_felt'] = dict(rel)
# runtime check against the earlier sourced runtime
dl = [(r, M(t).get('runtime_minus_earlier_s')) for r, t in R if M(t).get('runtime_minus_earlier_s') is not None]
OUT['runtime_vs_earlier'] = dict(n=len(dl), within_2s=sum(1 for r, x in dl if abs(x) <= 2), differ_gt_5s=[f"#{r['n']} {r['title']}: {x:+.0f} s" for r, x in dl if abs(x) > 5])
OUT['runtime_edition'] = dict(collections.Counter(M(t).get('runtime_edition') for r, t in R if M(t).get('runtime_s')))
OUT['runtime_basis'] = dict(collections.Counter(M(t).get('runtime_best_basis') for r, t in R))
OUT['runtime_cited_only'] = [f"#{r['n']} {r['title']}" for r, t in R if M(t).get('runtime_best_basis') == 'cited']
OUT['runtime_missing'] = [f"#{r['n']} {r['title']}" for r, t in R if not M(t).get('runtime_best_s')]
rts = sorted([(M(t)['runtime_best_s'], ttl(r)) for r, t in R if M(t).get('runtime_best_s')])
OUT['shortest'] = [f"\"{x[1]}\" {mmss(x[0])}" for x in rts[:6]]; OUT['longest'] = [f"\"{x[1]}\" {mmss(x[0])}" for x in rts[-6:]]
# cross-tab: hook-first by path and by Drake credit
def ct(pred):
    A = [(r, t, l) for r, t, l in L if l['has_hook'] and pred(r, t)]
    return f"{sum(1 for r, t, l in A if l['hook_first'])}/{len(A)}"
def ctv(pred):
    A = [(r, t, l) for r, t, l in L if l['has_hook'] and l.get('hook_before_first_verse') is not None and pred(r, t)]
    return f"{sum(1 for r, t, l in A if l['hook_before_first_verse'])}/{len(A)}"
OUT['hook_before_verse_cross'] = dict(climbers=ctv(lambda r, t: not r['debut_in_top10']), debuts=ctv(lambda r, t: r['debut_in_top10']), album_bomb=ctv(lambda r, t: r['album_bomb']),
                                      not_bomb=ctv(lambda r, t: not r['album_bomb']), drake=ctv(lambda r, t: 'Drake' in r['artists']), no_drake=ctv(lambda r, t: 'Drake' not in r['artists']))
OUT['hook_first_cross'] = dict(climbers=ct(lambda r, t: not r['debut_in_top10']), debuts=ct(lambda r, t: r['debut_in_top10']), album_bomb=ct(lambda r, t: r['album_bomb']),
                               not_bomb=ct(lambda r, t: not r['album_bomb']), drake=ct(lambda r, t: 'Drake' in r['artists']), no_drake=ct(lambda r, t: 'Drake' not in r['artists']),
                               second_voice=ct(lambda r, t: len([x for x in r['artists'].replace('¥$: ', '').replace(' Featuring ', '|').replace(' & ', '|').replace(', ', '|').replace(' X ', '|').replace(' With ', '|').split('|') if x.strip() and x.strip() != 'Metro Boomin']) >= 2))
# ---- documented "how it was made" statements, coded by rule (corrections.PROCESS_RULES)
import re as _re
import corrections as C
def process_code(cid, statement):
    for (c2, lead), code in C.PROCESS_OVERRIDES.items():
        if c2 == cid and statement.startswith(lead): return code
    for code, pat in C.PROCESS_RULES:
        if _re.search(pat, statement, _re.I): return code
    return 'other'
proc = collections.defaultdict(list); n_proc = 0
for r, t in R:
    for f in (M(t).get('page') or {}).get('new_facts') or []:
        if f['category'] != 'recording_process': continue
        n_proc += 1; proc[process_code(r['cid'], f['statement'])].append((r['n'], ttl(r), f['statement'], f['source']))
OUT['process'] = dict(statements=n_proc, tracks=len({x[0] for v in proc.values() for x in v}),
                      beat_first_union=len({x[0] for c in ('beat_sent', 'beat_preexisting') for x in proc.get(c, [])}),
                      beat_or_sample_first_union=len({x[0] for c in ('beat_sent', 'beat_preexisting', 'sample_first') for x in proc.get(c, [])}),
                      by_code={k: dict(statements=len(v), tracks=len({x[0] for x in v}), titles=sorted({x[1] for x in v}),
                                       items=[f"#{x[0]} {x[1]}: {x[2]} [{x[3]}]" for x in v]) for k, v in proc.items()})
pf = collections.Counter(); pft = collections.defaultdict(set)
for r, t in R:
    for f in (M(t).get('page') or {}).get('new_facts') or []:
        pf[f['category']] += 1; pft[f['category']].add(r['n'])
OUT['page_facts'] = {k: dict(statements=v, tracks=len(pft[k])) for k, v in pf.items()}
OUT['page_fact_items'] = {cat: [f"#{r['n']} {r['title']}: {f['statement']} [{f['source']}]" for r, t in R for f in (M(t).get('page') or {}).get('new_facts') or [] if f['category'] == cat]
                          for cat in ('beat_switch', 'opening', 'hook', 'structure', 'delivery', 'borrowing', 'producer_tag', 'tempo_or_key', 'guest_or_credit')}

# ---- how the two lyric readings compared, and what the page check returned (list tracks only)
from paths import REPO
ids = {str(r['cid']) for r in rows}
rp = REPO + 'data/measured/lyric_structure_review.json'
if os.path.exists(rp):
    RV = {k: v for k, v in json.load(open(rp)).items() if k in ids}
    OUT['review_summary'] = dict(reviewed=len(RV), agree=sum(1 for v in RV.values() if v['status'] == 'agree'), ruled=sum(1 for v in RV.values() if v['status'] == 'adjudicated'),
                                 no_ruling=sum(1 for v in RV.values() if v['status'] == 'disputed_no_ruling'),
                                 asides_removed=sum(1 for v in RV.values() if v['reviewer'].get('recollection_aside_removed') or (v.get('ruling') or {}).get('recollection_aside_removed')),
                                 kinds_reset=sum(1 for v in RV.values() if v['reviewer'].get('first_line_kind_reader')),
                                 resolution=dict(collections.Counter(v['ruling']['resolution'] for v in RV.values() if v.get('ruling'))),
                                 disagreed_on=dict(collections.Counter(w for v in RV.values() for w in v['why'])),
                                 hook_time_disputed=sum(1 for v in RV.values() if 'first hook time' in v['why'] or 'whether a recurring hook exists' in v['why']))
cp = REPO + 'data/measured/page_claims.json'
if os.path.exists(cp):
    PCL = {k: v for k, v in json.load(open(cp)).items() if k in ids}
    fin = collections.Counter(v['final'] for t in PCL.values() for v in t['verdicts'])
    OUT['claims_summary'] = dict(tracks=len(PCL), claims=sum(fin.values()), final=dict(fin), new_facts=sum(len(t['new_facts']) for t in PCL.values()),
                                 new_facts_by_category=dict(collections.Counter(f['category'] for t in PCL.values() for f in t['new_facts'])))
    sp = cp.replace('.json', '_summary.json')
    if os.path.exists(sp): OUT['claims_summary']['run'] = json.load(open(sp))
    # how the skeptic step was applied, and where each kind of P came from
    OUT['claims_summary']['sent_to_skeptic'] = sum(1 for t in PCL.values() for v in t['verdicts'] if v['first_verdict'] != 'not_addressed')
    OUT['claims_summary']['first_reader_only'] = sum(1 for t in PCL.values() for v in t['verdicts'] if v['first_verdict'] == 'not_addressed')
    coded = lambda i: i in ('opening', 'beat_switch', 'hook_first') or i.startswith('return_') or i.startswith('delivery_')
    con = [v['id'] for t in PCL.values() for v in t['verdicts'] if v['final'] == 'contradicted']
    OUT['claims_summary']['contradicted_with_basis_code'] = sum(1 for i in con if coded(i)); OUT['claims_summary']['contradicted_no_basis_code'] = sum(1 for i in con if not coded(i))
    OUT['claims_summary']['skeptic_downgraded'] = sum(1 for t in PCL.values() for v in t['verdicts'] if v['first_verdict'] == 'supported' and v['final'] == 'partly_supported')
    _rec = {str(r['cid']): r for r, t in R if t.get('opening_page_origin') == 'recoded'}
    _rec_con = [k for k, t in PCL.items() if str(k) in _rec and any(v['id'] == 'opening' and v['final'] == 'contradicted' for v in t['verdicts'])]
    OUT['claims_summary']['contradicted_recoded'] = len(_rec_con)
    OUT['claims_summary']['contradicted_recoded_titles'] = [ttl(_rec[k]) for k in _rec_con]
    OUT['claims_summary']['contradicted_to_u'] = OUT['claims_summary']['contradicted_with_basis_code'] - len(_rec_con)
OUT['page_origins'] = dict(
    borrowings=dict(collections.Counter(x.get('page_origin') for r, t in R for x in (t.get('samples') or []) if x.get('status') == 'page')),
    borrowings_search_summary_only=[f"#{r['n']} {r['title']}: {x.get('work', '')[:50]}" for r, t in R for x in (t.get('samples') or []) if x.get('status') == 'confirmed'],
    beat_switch=dict(collections.Counter(t.get('beat_switch_page_origin') for r, t in R if t.get('beat_switch') == 'yes' and t.get('beat_switch_basis') == 'page')),
    opening=dict(collections.Counter(t.get('opening_page_origin') for r, t in R if t.get('opening_element') not in (None, 'unknown') and t.get('opening_basis') == 'page')))

# ---- second, separate run of the lyric read and ruling: how often it lands on the same values (consistency check only)
SRall = [(r, t, l) for r, t, l in L if l.get('second_run')]
cmp_ = [(r, t, l) for r, t, l in SRall if l['second_run']['status'] == 'compared']
def _fr(key):
    xs = [l['second_run']['same'][key] for r, t, l in cmp_ if key in l['second_run']['same']]
    return f"{sum(xs)}/{len(xs)}"
def _hookstats(vals):
    v = sorted(vals)
    return dict(n=len(v), median=mmss(statistics.median(v)) if v else None, le_30s=sum(1 for x in v if x <= 30), le_60s=sum(1 for x in v if x <= 60))
prim = [l['first_hook_s'] for r, t, l in L if l['has_hook']]
alt = [(l['second_run']['first_hook_s'] if (l.get('second_run') or {}).get('status') == 'compared' and l['second_run'].get('has_hook') and l['second_run'].get('first_hook_s') is not None else l['first_hook_s'])
       for r, t, l in L if l['has_hook']]
hb_p = [l['hook_before_first_verse'] for r, t, l in L if l['has_hook'] and l.get('hook_before_first_verse') is not None]
hb_a = [(l['second_run']['hook_before_first_verse'] if (l.get('second_run') or {}).get('status') == 'compared' and l['second_run'].get('hook_before_first_verse') is not None else l['hook_before_first_verse'])
        for r, t, l in L if l['has_hook'] and l.get('hook_before_first_verse') is not None]
OUT['second_run'] = dict(
    tracks=len(SRall), compared=len(cmp_), no_final=len(SRall) - len(cmp_),
    no_final_list=[f"\"{ttl(r)}\"" for r, t, l in SRall if l['second_run']['status'] != 'compared'],
    has_hook=_fr('has_hook'), first_line=_fr('first_line'), first_hook=_fr('first_hook'), hook_count=_fr('hook_count'), hook_before_first_verse=_fr('hook_before_first_verse'),
    first_section=_fr('first_section'), n_verses=_fr('n_verses'), first_line_kind=_fr('first_line_kind'), hook_return=_fr('hook_return'),
    core_agree=sum(1 for r, t, l in cmp_ if l.get('second_run_code') == '='),
    differ_list=[f"\"{ttl(r)}\" ({l['second_run_code'].replace('differs: ', '')})" for r, t, l in cmp_ if l.get('second_run_code') != '='],
    hook_time_differs=[f"\"{ttl(r)}\" ({mmss(l['first_hook_s'])} here, {mmss(l['second_run']['first_hook_s'])} in the second run)" for r, t, l in cmp_ if l['second_run']['same'].get('first_hook') is False],
    primary=_hookstats(prim), with_second_run_values=_hookstats(alt),
    hook_before_first_verse_primary=f"{sum(hb_p)}/{len(hb_p)}", hook_before_first_verse_second=f"{sum(hb_a)}/{len(hb_a)}")
json.dump(OUT, open(WORK + 'measured_stats.json', 'w'), indent=1, default=str)
if __name__ == '__main__':
    a = OUT['groups']['all']
    for k, v in a.items(): print(k, '=>', v)
    for k, v in OUT.items():
        if k != 'groups': print('##', k, '=>', v if not isinstance(v, list) else (len(v), v[:12]))
