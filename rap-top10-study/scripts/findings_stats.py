"""Compute the counts behind each finding in 03-findings.md (k / n_assessed), with group splits and named examples."""
import json, statistics, collections, re
SP = '/tmp/claude-0/-home-user-app-policies/08207d95-5f38-5913-acec-14c31ee115ad/scratchpad/'
rows = json.load(open(SP + 'data/final_rows.json'))
T = {int(k): v for k, v in json.load(open(SP + 'data/tracks_merged.json')).items()}
R = [(r, T.get(r['cid'])) for r in rows]
studied = [(r, t) for r, t in R if t]
def mmss(s): return f"{int(s // 60)}:{int(round(s % 60)):02d}" if s is not None else '?'
def qd(v):
    v = sorted(v)
    if len(v) < 2: return {'n': len(v), 'median': v[0] if v else None}
    qs = statistics.quantiles(v, n=4)
    return {'n': len(v), 'median': statistics.median(v), 'q1': qs[0], 'q3': qs[2], 'min': v[0], 'max': v[-1]}
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
    rt = [t['runtime_s'] for r, t in S if t.get('runtime_s')]
    felt = [t['felt_bpm'] for r, t in S if t.get('felt_bpm') and t.get('tempo_status') != 'conflict']
    d = {'n_songs': len(allg), 'n_studied': len(S)}
    q = qd(rt); d['runtime'] = {k: (mmss(v) if k not in ('n',) and v is not None else v) for k, v in q.items()}
    d['runtime_le_3min'] = f"{sum(1 for x in rt if x <= 180)}/{len(rt)}"; d['runtime_ge_4min'] = f"{sum(1 for x in rt if x >= 240)}/{len(rt)}"
    d['felt'] = qd(felt)
    pairs = [(t['grid_bpm'], t['felt_bpm']) for r, t in S if t.get('felt_bpm') and t.get('grid_bpm') and t.get('tempo_status') != 'conflict']
    half = [f for g_, f in pairs if 1.8 <= g_ / f <= 2.2]; full = [f for g_, f in pairs if not (1.8 <= g_ / f <= 2.2)]
    d['feel_half_time'] = f"{len(half)}/{len(pairs)}"; d['feel_full_time'] = f"{len(full)}/{len(pairs)}"
    d['half_time_felt'] = qd(half); d['full_time_felt'] = qd(full)
    d['full_time_bands'] = dict(collections.Counter('<95 (verse-led/boom-bap)' if f < 95 else '95-115 (bounce/pop-rap)' if f <= 115 else '>115 (club)' for f in full))
    d['felt_half_60_85'] = f"{len(half)}/{len(pairs)}"; d['felt_full_95_115'] = f"{sum(1 for f in full if 95 <= f <= 115)}/{len(pairs)}"
    smp_n = len(S); d['samples'] = f"{sum(1 for r, t in S if any(sm.get('credited', True) for sm in (t.get('samples') or [])))}/{smp_n}"
    d['features'] = f"{sum(1 for r, t in S if t.get('features'))}/{smp_n}"
    hs = collections.Counter(t.get('hook_status') for r, t in S)
    d['hook_present_verified'] = hs.get('present_verified', 0); d['hook_present_unverified'] = hs.get('present_unverified', 0)
    d['hook_absent'] = hs.get('absent_verified', 0) + hs.get('absent_unverified', 0); d['hook_unknown'] = hs.get('unknown', 0) + hs.get(None, 0)
    hf = collections.Counter((t.get('hook_first'), t.get('hook_first_basis')) for r, t in S)
    d['hook_first_yes_src'] = hf.get(('yes', 'source'), 0); d['hook_first_no_src'] = hf.get(('no', 'source'), 0)
    d['hook_first_yes_rec'] = hf.get(('yes', 'unverified_recollection'), 0); d['hook_first_no_rec'] = hf.get(('no', 'unverified_recollection'), 0)
    bs = collections.Counter((t.get('beat_switch'), t.get('beat_switch_basis')) for r, t in S)
    d['switch_yes_src'] = bs.get(('yes', 'source'), 0); d['switch_yes_rec'] = bs.get(('yes', 'unverified_recollection'), 0)
    d['switch_no_any'] = bs.get(('no', 'source'), 0) + bs.get(('no', 'unverified_recollection'), 0); d['switch_unknown'] = sum(v for k, v in bs.items() if k[0] in (None, 'unknown'))
    d['style'] = dict(collections.Counter(t.get('style_tag') for r, t in S))
    OUT[g] = d
# named lists
OUT['beat_switch_sourced'] = [f"{r['title']} ({t.get('beat_switch_time') or 'time not documented'})" for r, t in studied if t.get('beat_switch') == 'yes' and t.get('beat_switch_basis') == 'source']
OUT['hookless'] = [f"{r['title']} [{t.get('hook_status')}]" for r, t in studied if (t.get('hook_status') or '').startswith('absent')]
OUT['hook_first_yes'] = [f"{r['title']} [{t.get('hook_first_basis')}]" for r, t in studied if t.get('hook_first') == 'yes']
OUT['hook_first_no'] = [f"{r['title']} [{t.get('hook_first_basis')}]" for r, t in studied if t.get('hook_first') == 'no']
OUT['opening_sourced'] = [f"{r['title']}: {t.get('opening_element')}" for r, t in studied if t.get('opening_basis') == 'source' and t.get('opening_element') not in (None, 'unknown')]
OUT['full_time_bounce'] = [f"{r['title']} {t['felt_bpm']:g}" for r, t in studied if t.get('felt_bpm') and 95 <= t['felt_bpm'] <= 115]
OUT['tempo_conflicts'] = [r['title'] for r, t in studied if t.get('tempo_status') == 'conflict']
bt = collections.Counter(); bt_tracks = collections.defaultdict(list)
for r, t in studied:
    for sm in (t.get('samples') or []):
        if sm.get('credited', True): bt[sm.get('borrow_type')] += 1; bt_tracks[sm.get('borrow_type')].append(r['title'])
OUT['borrow_types'] = {k: (v, sorted(set(bt_tracks[k]))[:10]) for k, v in bt.most_common()}
OUT['uncredited_only'] = [r['title'] for r, t in studied if t.get('samples') and not any(sm.get('credited', True) for sm in t['samples'])]
OUT['half_time'] = [f"{r['title']} {t['grid_bpm']:g}/{t['felt_bpm']:g}" for r, t in studied if t.get('felt_bpm') and t.get('grid_bpm') and t.get('tempo_status') != 'conflict' and 1.8 <= t['grid_bpm'] / t['felt_bpm'] <= 2.2]
OUT['full_time'] = [f"{r['title']} {t['grid_bpm']:g}/{t['felt_bpm']:g}" for r, t in studied if t.get('felt_bpm') and t.get('grid_bpm') and t.get('tempo_status') != 'conflict' and not (1.8 <= t['grid_bpm'] / t['felt_bpm'] <= 2.2)]
OUT['drill'] = [r['title'] for r, t in studied if t.get('style_tag') == 'drill']
OUT['climbers_detail'] = [dict(title=r['title'], runtime=t.get('runtime_mmss') if t else None, felt=t.get('felt_bpm') if t else None, samples=[s.get('work') for s in (t.get('samples') or [])][:2] if t else None,
                              hook=t.get('hook_status') if t else None, hook_first=(t.get('hook_first'), t.get('hook_first_basis')) if t else None, opening=(t.get('opening_element'), t.get('opening_basis')) if t else None,
                              weeks_top10=r['weeks_in_top10'], peak=r['peak'], climbed_from=r['climbed_from'], style=t.get('style_tag') if t else None) for r, t in R if not r['debut_in_top10']]
# voice-change returns and delivery aspects
vc = []
asp = collections.Counter(); asp_tracks = collections.defaultdict(set)
for r, t in studied:
    for d in t.get('delivery') or []:
        if d.get('basis') == 'source': asp[d['aspect']] += 1; asp_tracks[d['aspect']].add(r['title'])
    for d in t.get('returns') or []:
        txt = (d.get('change') or '').lower()
        if d.get('basis') == 'source' and any(w in txt for w in ['verse', 'voice', 'hand-off', 'feature', 'takes over', 'register', 'trade', 'guest']):
            vc.append(r['title'])
OUT['voice_change_returns'] = sorted(set(vc))
OUT['delivery_aspects'] = {k: (v, sorted(asp_tracks[k])[:8]) for k, v in asp.most_common()}
OUT['tracks_with_sourced_delivery'] = sum(1 for r, t in studied if any(d.get('basis') == 'source' for d in t.get('delivery') or []))
OUT['tracks_with_sourced_returns'] = sum(1 for r, t in studied if any(d.get('basis') == 'source' for d in t.get('returns') or []))
OUT['timestamps'] = dict(first_vocal=sum(1 for r, t in studied if t.get('first_lead_vocal_time')), first_hook=sum(1 for r, t in studied if t.get('first_hook_time')),
                         beat_switch_time=sum(1 for r, t in studied if t.get('beat_switch_time')))
OUT['runtime_status'] = dict(collections.Counter(t.get('runtime_status') for r, t in studied))
OUT['tempo_status'] = dict(collections.Counter(t.get('tempo_status') for r, t in studied))
OUT['shortest'] = sorted([(t['runtime_s'], r['title']) for r, t in studied if t.get('runtime_s')])[:6]
OUT['longest'] = sorted([(t['runtime_s'], r['title']) for r, t in studied if t.get('runtime_s')])[-6:]
OUT['sample_hook_examples'] = [f"{r['title']}: {t['samples'][0].get('work')}" for r, t in studied if t.get('samples') and 'sample_or_interpolation' in (t.get('hook_devices') or [])][:15]
json.dump(OUT, open(SP + 'data/findings_stats.json', 'w'), indent=1, default=str)
for k, v in OUT.items():
    print('##', k); print('  ', v)
