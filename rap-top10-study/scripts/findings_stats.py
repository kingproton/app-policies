"""Compute the counts behind each finding in 03-findings.md (k / n assessed), with group splits and named lists.

Basis ladder: 'source' counts as sourced. 'unconfirmed' (the researcher cited a source the verifier could
not re-find) and 'unverified_recollection' are reported separately and never counted as sourced.
Unknown never counts as "no".
"""
import json, statistics, collections, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrections as C
from paths import WORK
rows = json.load(open(WORK + 'final_rows.json'))
T = {int(k): v for k, v in json.load(open(WORK + 'tracks_merged.json')).items()}
R = [(r, T.get(r['cid'])) for r in rows]
studied = [(r, t) for r, t in R if t]
DOC = {'confirmed', 'cited'}                              # sample statuses that count as sourced
DOC_U = DOC | {'not_reconfirmed'}                         # ... plus credits the verifier could not re-find (U)
NON_VOCAL = {'Metro Boomin'}                                # credited producer-artists who do not take a verse or hook


def mmss(s): return f"{int(s // 60)}:{int(round(s % 60)):02d}" if s is not None else '?'


def qd(v):
    v = sorted(v)
    if len(v) < 2: return {'n': len(v), 'median': v[0] if v else None}
    qs = statistics.quantiles(v, n=4)
    return {'n': len(v), 'median': statistics.median(v), 'q1': qs[0], 'q3': qs[2], 'min': v[0], 'max': v[-1]}


def credit_names(a):
    a = a.replace('Tyler, The Creator', 'Tyler The Creator').replace('¥$: ', '')
    return [x.strip() for x in re.split(r' Featuring | With | & | X |, ', a) if x.strip()]


def second_vocalist(r):
    names = credit_names(r['artists'])
    return len([n for n in names if n not in NON_VOCAL]) >= 2


def is_half(t): return 1.8 <= t['grid_bpm'] / t['felt_bpm'] <= 2.2


def pair_ok(t): return bool(t.get('felt_bpm') and t.get('grid_bpm') and t.get('tempo_status') != 'conflict')


def doc_samples(t): return [s for s in (t.get('samples') or []) if s.get('status') in DOC]
def doc_samples_u(t): return [s for s in (t.get('samples') or []) if s.get('status') in DOC_U]
def returning(r): return C.RETURNING.get(r['cid'], 'uncoded')


def rtype(r, t):
    """Return-change type for tracks with a sourced (not verifier-rejected) return description."""
    if not any(d.get('basis') == 'source' for d in t.get('returns') or []): return None
    return C.RETURN_TYPES.get(r['cid'], 'uncoded')


OUT = {}
groups = {
    'all': lambda r, t: True,
    'climbers': lambda r, t: not r['debut_in_top10'],
    'debuts': lambda r, t: r['debut_in_top10'],
    'album_bomb': lambda r, t: r['album_bomb'],
    'not_bomb': lambda r, t: not r['album_bomb'],
    'drake_credit': lambda r, t: 'Drake' in r['artists'],
    'no_drake': lambda r, t: 'Drake' not in r['artists'],
}
for g, f in groups.items():
    S = [(r, t) for r, t in studied if f(r, t)]
    allg = [(r, t) for r, t in R if f(r, t)]
    d = {'n_songs': len(allg), 'n_studied': len(S)}
    rt = [t['runtime_s'] for r, t in S if t.get('runtime_s')]
    q = qd(rt); d['runtime'] = {k: (mmss(v) if k != 'n' and v is not None else v) for k, v in q.items()}
    d['runtime_le_3min'] = f"{sum(1 for x in rt if x <= 180)}/{len(rt)}"; d['runtime_ge_4min'] = f"{sum(1 for x in rt if x >= 240)}/{len(rt)}"
    P = [t for r, t in S if pair_ok(t)]
    d['felt'] = qd([t['felt_bpm'] for t in P])
    half = [t for t in P if is_half(t)]; full = [t for t in P if not is_half(t)]
    d['feel_half_time'] = f"{len(half)}/{len(P)}"; d['feel_full_time'] = f"{len(full)}/{len(P)}"
    d['half_time_felt'] = qd([t['felt_bpm'] for t in half]); d['full_time_felt'] = qd([t['felt_bpm'] for t in full])
    d['half_in_band_110_129'] = sum(1 for t in half if 110 <= t['grid_bpm'] < 130)
    d['felt_full_95_115'] = f"{sum(1 for t in full if 95 <= t['felt_bpm'] <= 115)}/{len(P)}"
    d['tempo_listed_any'] = sum(1 for r, t in S if t.get('tempo_listed') or t.get('grid_bpm'))
    ds = [(r, t) for r, t in S if doc_samples(t)]
    d['borrow_documented'] = f"{len(ds)}/{len(S)}"
    d['borrow_credited'] = f"{sum(1 for r, t in ds if any(s.get('credited', True) for s in doc_samples(t)))}/{len(S)}"
    d['borrow_documented_u'] = f"{sum(1 for r, t in S if doc_samples_u(t))}/{len(S)}"
    d['borrow_not_reconfirmed_only'] = sum(1 for r, t in S if doc_samples_u(t) and not doc_samples(t))
    d['second_vocalist_credit'] = f"{sum(1 for r, t in allg if second_vocalist(r))}/{len(allg)}"
    d['guest_documented_any'] = f"{sum(1 for r, t in S if t.get('features'))}/{len(S)}"
    hs = collections.Counter(t.get('hook_status') for r, t in S)
    d['hook_present_verified'] = hs.get('present_verified', 0); d['hook_present_unverified'] = hs.get('present_unverified', 0)
    d['hook_absent'] = hs.get('absent_verified', 0) + hs.get('absent_unverified', 0); d['hook_unknown'] = hs.get('unknown', 0) + hs.get(None, 0)
    hf = collections.Counter((t.get('hook_first'), t.get('hook_first_basis')) for r, t in S)
    for val in ('yes', 'no'):
        for b, lab in (('source', 'src'), ('unconfirmed', 'unc'), ('unverified_recollection', 'rec')):
            d[f'hook_first_{val}_{lab}'] = hf.get((val, b), 0)
    op = collections.Counter(t.get('opening_basis') for r, t in S if t.get('opening_element') not in (None, 'unknown'))
    d['opening_src'] = op.get('source', 0); d['opening_unc'] = op.get('unconfirmed', 0); d['opening_rec'] = op.get('unverified_recollection', 0)
    d['opening_sample_src'] = sum(1 for r, t in S if t.get('opening_basis') == 'source' and t.get('opening_element') == 'sample_or_interpolation')
    bs = collections.Counter((t.get('beat_switch'), t.get('beat_switch_basis')) for r, t in S)
    d['switch_yes_src'] = bs.get(('yes', 'source'), 0); d['switch_yes_unc'] = bs.get(('yes', 'unconfirmed'), 0)
    d['switch_yes_rec'] = bs.get(('yes', 'unverified_recollection'), 0)
    d['switch_no_any'] = sum(v for k, v in bs.items() if k[0] == 'no'); d['switch_unknown'] = sum(v for k, v in bs.items() if k[0] in (None, 'unknown'))
    d['switch_assessed'] = sum(v for k, v in bs.items() if k[0] in ('yes', 'no'))
    rtc = collections.Counter(rtype(r, t) for r, t in S if rtype(r, t))
    d['return_sourced_tracks'] = sum(rtc.values())
    d['return_beat'] = rtc.get('beat', 0) + rtc.get('beat+voice', 0); d['return_voice'] = rtc.get('voice', 0) + rtc.get('beat+voice', 0)
    d['return_register'] = rtc.get('register', 0); d['return_delivery'] = rtc.get('delivery', 0); d['return_none'] = rtc.get('none', 0)
    rr = [(rtype(r, t), returning(r)) for r, t in S if rtype(r, t)]
    d['return_oneway'] = sum(1 for ty, rt_ in rr if rt_ is False)
    d['returning_total'] = sum(1 for ty, rt_ in rr if rt_ is True)
    d['returning_voice'] = sum(1 for ty, rt_ in rr if rt_ is True and 'voice' in ty)
    d['returning_beat'] = sum(1 for ty, rt_ in rr if rt_ is True and 'beat' in ty)
    d['returning_register'] = sum(1 for ty, rt_ in rr if rt_ is True and ty == 'register')
    d['returning_none'] = sum(1 for ty, rt_ in rr if rt_ is True and ty == 'none')
    d['style'] = dict(collections.Counter(t.get('style_tag') for r, t in S))
    OUT[g] = d

# ---- named lists
def who(r): return 'Drake' if 'Drake' in r['artists'] else ('Kendrick Lamar' if 'Kendrick' in r['artists'] else r['lead_artist'])
OUT['beat_switch_sourced'] = [f"{r['title']} [{who(r)}{'; album-bomb' if r['album_bomb'] else ''}]" for r, t in studied if t.get('beat_switch') == 'yes' and t.get('beat_switch_basis') == 'source']
OUT['beat_switch_unconfirmed'] = [r['title'] for r, t in studied if t.get('beat_switch') == 'yes' and t.get('beat_switch_basis') == 'unconfirmed']
OUT['beat_switch_recollection'] = [r['title'] for r, t in studied if t.get('beat_switch') == 'yes' and t.get('beat_switch_basis') == 'unverified_recollection']
OUT['beat_switch_times'] = [f"{r['title']}: {t.get('beat_switch_time')}" for r, t in studied if t.get('beat_switch_time')]
OUT['hookless'] = [f"{r['title']} [{t.get('hook_status')}; style {t.get('style_tag')}]" for r, t in studied if (t.get('hook_status') or '').startswith('absent')]
OUT['hook_present_sourced'] = [r['title'] for r, t in studied if t.get('hook_status') == 'present_verified']
for val in ('yes', 'no'):
    OUT[f'hook_first_{val}'] = [f"{r['title']} [{t.get('hook_first_basis')}]" for r, t in studied if t.get('hook_first') == val]
OUT['opening_sourced'] = [f"{r['title']}: {t.get('opening_element')}{' [sweep]' if 'opening_element' in (t.get('structure_sweep_used') or []) else ''}" for r, t in studied if t.get('opening_basis') == 'source' and t.get('opening_element') not in (None, 'unknown')]
OUT['opening_unconfirmed'] = [f"{r['title']}: {t.get('opening_element')}" for r, t in studied if t.get('opening_basis') == 'unconfirmed']
OUT['opening_sourced_types'] = dict(collections.Counter(x.split(': ')[1].replace(' [sweep]', '') for x in OUT['opening_sourced']))
OUT['sample_open_and_hook_first_src'] = [r['title'] for r, t in studied if t.get('opening_basis') == 'source' and t.get('opening_element') == 'sample_or_interpolation' and t.get('hook_first') == 'yes' and t.get('hook_first_basis') == 'source']
OUT['hook_first_src_drake'] = {v: sum(1 for r, t in studied if 'Drake' in r['artists'] and t.get('hook_first') == v and t.get('hook_first_basis') == 'source') for v in ('yes', 'no')}
OUT['sample_open_src_drake'] = sum(1 for r, t in studied if 'Drake' in r['artists'] and t.get('opening_basis') == 'source' and t.get('opening_element') == 'sample_or_interpolation')
# tempo
OUT['half_time'] = [f"{r['title']} {t['grid_bpm']:g}/{t['felt_bpm']:g}" for r, t in studied if pair_ok(t) and is_half(t)]
OUT['full_time'] = [f"{r['title']} {t['grid_bpm']:g}/{t['felt_bpm']:g} [{t.get('style_tag')}]" for r, t in studied if pair_ok(t) and not is_half(t)]
OUT['half_band_110_129'] = [f"{r['title']} {t['grid_bpm']:g}/{t['felt_bpm']:g}" for r, t in studied if pair_ok(t) and is_half(t) and 110 <= t['grid_bpm'] < 130]
OUT['half_time_drake'] = sum(1 for r, t in studied if pair_ok(t) and is_half(t) and 'Drake' in r['artists'])
OUT['full_time_kendrick'] = sum(1 for r, t in studied if pair_ok(t) and not is_half(t) and 'Kendrick' in r['artists'])
def excl_reason(t):
    st = t.get('tempo_status')
    vals = sorted({float(x['bpm']) for x in t.get('tempo_listed') or [] if x.get('bpm')})
    if st == 'conflict': return 'conflicting listings'
    if st == 'feel_unresolved': return 'half/full feel unresolved'
    if any('LOW CONFIDENCE' in (x.get('site') or x.get('source') or '') for x in t.get('tempo_listed') or []): return 'low-confidence listing'
    if len(vals) >= 2: return 'conflicting listings'
    return 'single unconfirmed listing'
OUT['tempo_excluded'] = [f"{r['title']} ({excl_reason(t)}; listed {', '.join(f'{v:g}' for v in sorted({float(x['bpm']) for x in t.get('tempo_listed') or [] if x.get('bpm')}))})"
                         for r, t in studied if (t.get('tempo_listed') or t.get('grid_bpm')) and not pair_ok(t)]
OUT['tempo_none_listed'] = [r['title'] for r, t in studied if not t.get('tempo_listed') and not t.get('grid_bpm')]
OUT['tempo_status'] = dict(collections.Counter(t.get('tempo_status') for r, t in studied if pair_ok(t)))
OUT['feel_basis'] = dict(collections.Counter(t.get('feel_basis') for r, t in studied if t.get('felt_bpm')))
OUT['outliers_removed'] = {r['title']: [x.get('bpm') for x in t.get('tempo_outliers_removed') or []] for r, t in studied if t.get('tempo_outliers_removed')}
# style splits used in 01
def style_rows(tags): return [(r, t) for r, t in studied if t.get('style_tag') in tags]
OUT['style_tempo'] = {}
for lab, tags in (('verse_led', {'boom_bap_or_verse_led'}), ('trap', {'trap', 'melodic_trap'}), ('drill', {'drill'}), ('bounce', {'west_coast_bounce'}), ('pop_rap', {'pop_rap'})):
    P = [t for r, t in style_rows(tags) if pair_ok(t)]
    OUT['style_tempo'][lab] = dict(n_tagged=len(style_rows(tags)), n_tempo=len(P), half=sum(1 for t in P if is_half(t)),
                                   felt=sorted(t['felt_bpm'] for t in P), grid=sorted(t['grid_bpm'] for t in P),
                                   in_130_170_felt_65_85=sum(1 for t in P if 130 <= t['grid_bpm'] <= 170 and 65 <= t['felt_bpm'] <= 85))
# borrowing
bt = collections.Counter(); bt_tracks = collections.defaultdict(set); bt_cred = collections.Counter()
for r, t in studied:
    for sm in doc_samples(t):
        bt[sm.get('borrow_type')] += 1; bt_tracks[sm.get('borrow_type')].add((r['cid'], r['title']))
        if sm.get('credited', True): bt_cred[sm.get('borrow_type')] += 1
OUT['borrow_types'] = {k: (v, len(bt_tracks[k]), sorted(x[1] for x in bt_tracks[k]), bt_cred[k]) for k, v in bt.most_common()}
OUT['borrow_not_reconfirmed_only'] = [r['title'] for r, t in studied if doc_samples_u(t) and not doc_samples(t)]
OUT['borrow_unconfirmed_credits'] = [f"{r['title']}: {s['work'][:50]}" for r, t in studied for s in t.get('samples') or [] if s.get('status') == 'not_reconfirmed']
OUT['borrow_rejected'] = [f"{r['title']}: {s['work'][:60]}" for r, t in studied for s in t.get('samples') or [] if s.get('status') == 'rejected']
OUT['borrow_added_by_verifier'] = [r['title'] for r, t in studied if r['cid'] in C.SAMPLE_ADD and any(s.get('status') == 'confirmed' and s.get('work') in {a['work'] for a in C.SAMPLE_ADD[r['cid']]} for s in t.get('samples') or [])]
OUT['borrow_added_only_credit'] = [r['title'] for r, t in studied if r['cid'] in C.SAMPLE_ADD and {s['work'] for s in doc_samples(t)} <= {a['work'] for a in C.SAMPLE_ADD[r['cid']]}]
OUT['borrow_uncredited_only'] = [r['title'] for r, t in studied if doc_samples(t) and not any(s.get('credited', True) for s in doc_samples(t))]
OUT['borrow_none_documented'] = len([1 for r, t in studied if not doc_samples(t)])
# returns
rt_lists = collections.defaultdict(list)
for r, t in studied:
    ty = rtype(r, t)
    if ty: rt_lists[ty].append(r['title'])
OUT['return_types'] = dict(rt_lists)
OUT['return_unconfirmed_tracks'] = [r['title'] for r, t in studied if any(d.get('basis') == 'unconfirmed' for d in t.get('returns') or [])]
OUT['climber_return_types'] = {r['title']: rtype(r, t) for r, t in studied if not r['debut_in_top10'] and rtype(r, t)}
OUT['returning_lists'] = {k: [r['title'] for r, t in studied if rtype(r, t) and returning(r) is True and f(rtype(r, t))] for k, f in
                          (('voice', lambda ty: 'voice' in ty), ('beat', lambda ty: 'beat' in ty), ('register', lambda ty: ty == 'register'), ('none', lambda ty: ty == 'none'))}
OUT['oneway_list'] = [r['title'] for r, t in studied if rtype(r, t) and returning(r) is False]
OUT['trap_return_split'] = dict(collections.Counter(x for r, t in studied if rtype(r, t) and t.get('style_tag') in ('trap', 'melodic_trap') for x in (['voice'] if 'voice' in rtype(r, t) else []) + (['beat'] if 'beat' in rtype(r, t) else [])))
OUT['trap_return_tracks'] = sum(1 for r, t in studied if rtype(r, t) and t.get('style_tag') in ('trap', 'melodic_trap'))
# delivery
asp = collections.Counter(); asp_tracks = collections.defaultdict(set)
for r, t in studied:
    for dd in t.get('delivery') or []:
        if dd.get('basis') == 'source': asp[dd['aspect']] += 1; asp_tracks[dd['aspect']].add(r['title'])
OUT['delivery_aspects'] = {k: (v, sorted(asp_tracks[k])) for k, v in asp.most_common()}
OUT['tracks_with_sourced_delivery'] = sum(1 for r, t in studied if any(dd.get('basis') == 'source' for dd in t.get('delivery') or []))
OUT['timestamps'] = dict(first_vocal=sum(1 for r, t in studied if t.get('first_lead_vocal_time')), first_hook=sum(1 for r, t in studied if t.get('first_hook_time')),
                         beat_switch_time=sum(1 for r, t in studied if t.get('beat_switch_time')))
OUT['runtime_status'] = dict(collections.Counter(t.get('runtime_status') for r, t in studied if t.get('runtime_s')))
OUT['shortest'] = sorted([(t['runtime_s'], r['title']) for r, t in studied if t.get('runtime_s')])[:6]
OUT['longest'] = sorted([(t['runtime_s'], r['title']) for r, t in studied if t.get('runtime_s')])[-6:]
OUT['drill'] = [r['title'] for r, t in studied if t.get('style_tag') == 'drill']
OUT['climbers_detail'] = [dict(title=r['title'], runtime=t.get('runtime_mmss'), felt=t.get('felt_bpm'), borrow=[s.get('work')[:40] for s in doc_samples(t)][:2],
                              hook=t.get('hook_status'), hook_first=(t.get('hook_first'), t.get('hook_first_basis')), opening=(t.get('opening_element'), t.get('opening_basis')),
                              switch=(t.get('beat_switch'), t.get('beat_switch_basis')), weeks_top10=r['weeks_in_top10'], total_weeks=r['total_weeks'], peak=r['peak'],
                              climbed_from=r['climbed_from'], style=t.get('style_tag'), second_vocalist=second_vocalist(r), guests=len(t.get('features') or []))
                         for r, t in studied if not r['debut_in_top10']]
json.dump(OUT, open(WORK + 'findings_stats.json', 'w'), indent=1, default=str)
if __name__ == '__main__':
    for k, v in OUT.items():
        print('##', k); print('  ', v)
