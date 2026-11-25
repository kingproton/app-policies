"""Render the 'measured counts at a glance' table for 03-findings.md from findings_stats.json."""
import json, os
from paths import WORK
OUTF = os.environ.get('STUDY_OUT', WORK + 'counts_table.md')
F = json.load(open(WORK + 'findings_stats.json'))
G = [('all', 'All 100'), ('climbers', 'Climbed into top 10'), ('debuts', 'Debuted in top 10'), ('album_bomb', 'Album-bomb cuts'), ('not_bomb', 'Not album-bomb'), ('drake_credit', 'Drake credited'), ('no_drake', 'No Drake')]
def rt(d):
    r = d['runtime']
    return f"{r.get('median','?')} (IQR {r.get('q1','?')}–{r.get('q3','?')}; n={r['n']})" if r.get('n') else '?'
def felt(d):
    f = d['felt']
    return f"{f['median']:g} (n={f['n']})" if f.get('n') else '?'
rows = [
    ('Songs / studied', lambda d: f"{d['n_songs']} / {d['n_studied']}"),
    ('Median runtime', rt),
    ('Runtime ≤ 3:00', lambda d: d['runtime_le_3min']),
    ('Runtime ≥ 4:00', lambda d: d['runtime_ge_4min']),
    ('Median felt BPM (resolved tempo)', felt),
    ('Half-time feel (grid ≈ 2× felt) [inferred]', lambda d: d['feel_half_time']),
    ('  of which grid 110–129 (feel ambiguous)', lambda d: str(d['half_in_band_110_129'])),
    ('  median felt, half-time', lambda d: f"{d['half_time_felt'].get('median','?')}"),
    ('Full-time feel [inferred]', lambda d: d['feel_full_time']),
    ('  of which 95–115 bounce/pop-rap', lambda d: d['felt_full_95_115']),
    ('Sourced borrowing (sample, interpolation, clip, reuse)', lambda d: d['borrow_documented']),
    ('  with a credit', lambda d: d['borrow_credited']),
    ('  incl. credits the verifier could not re-find (U)', lambda d: d['borrow_documented_u']),
    ('Second credited vocalist (Billboard credit)', lambda d: d['second_vocalist_credit']),
    ('Hook present — sourced / unverified', lambda d: f"{d['hook_present_verified']} / {d['hook_present_unverified']}"),
    ('No conventional hook (unverified)', lambda d: str(d['hook_absent'])),
    ('Hook status unknown', lambda d: str(d['hook_unknown'])),
    ('Sourced opening / of which a sample', lambda d: f"{d['opening_src']} / {d['opening_sample_src']}"),
    ('Hook before first verse — sourced yes / no', lambda d: f"{d['hook_first_yes_src']} / {d['hook_first_no_src']}"),
    ('  not re-confirmed (U) yes / no', lambda d: f"{d['hook_first_yes_unc']} / {d['hook_first_no_unc']}"),
    ('  recollection yes / no', lambda d: f"{d['hook_first_yes_rec']} / {d['hook_first_no_rec']}"),
    ('Beat switch — sourced / U / recollection', lambda d: f"{d['switch_yes_src']} / {d['switch_yes_unc']} / {d['switch_yes_rec']}"),
    ('Beat switch unknown', lambda d: str(d['switch_unknown'])),
    ('Sourced change between sections — beat or bed / new voice', lambda d: f"{d['return_beat']} / {d['return_voice']}"),
    ('  in a section that comes back — new voice / bed', lambda d: f"{d['returning_voice']} / {d['returning_beat']}"),
]
out = ['| Measure | ' + ' | '.join(l for _, l in G) + ' |', '|---|' + '---|' * len(G)]
for name, fn in rows:
    out.append(f'| {name} | ' + ' | '.join(fn(F[g]) for g, _ in G) + ' |')
os.makedirs(os.path.dirname(OUTF), exist_ok=True)
open(OUTF, 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))


# ---------------- measured table (runtime, lyric timing, section map, riding the beat, felt tempo)
MS = json.load(open(WORK + 'measured_stats.json'))['groups']
OUTM = os.environ.get('STUDY_OUT_MEASURED', WORK + 'measured_table.md')
def iq(d, unit='', f='{}'):
    if not d or not d.get('n'): return '?'
    if 'q1' in d: return f"{f.format(d['median'])}{unit} (IQR {f.format(d['q1'])}–{f.format(d['q3'])}; n={d['n']})"
    return f"{f.format(d['median'])}{unit} (n={d['n']})"
def cls(d, key):
    c = d.get(key) or {}
    return f"{c.get('slow', 0)} / {c.get('mid', 0)} / {c.get('fast', 0)}"
mrows = [
    ('Songs', lambda d: str(d['n_songs'])),
    ('Median runtime', lambda d: iq(d['runtime'])),
    ('Runtime ≤ 3:00 / ≥ 4:00', lambda d: f"{d['runtime_le_3min']} / {d['runtime_ge_4min']}"),
    ('**Felt tempo** — clips with a clear backbeat', lambda d: f"{(d['feel_basis'] or {}).get('M', 0)}/{d['n_clip']}"),
    ('  median felt BPM (clear)', lambda d: iq({k: (v if k == 'n' else round(float(v) * 2) / 2) for k, v in d['felt_clear'].items()}, f='{:g}')),
    ('  slow (under 90) / mid (90–119) / fast (120+), clear', lambda d: cls(d, 'feel_class_clear')),
    ('  same split, all resolved readings', lambda d: cls(d, 'feel_class_all_resolved')),
    ('**First lyric line** — median time', lambda d: iq(d['first_line'], ' s', '{:.1f}')),
    ('  within 5 s / after 15 s', lambda d: f"{d['first_line_le_5s']} / {d['first_line_gt_15s']}"),
    ('**Recurring hook** present', lambda d: d['has_hook']),
    ('  first hook — median time', lambda d: iq(d['first_hook'])),
    ('  first hook by 0:30 / by 1:00 (of all assessed)', lambda d: f"{d['first_hook_le_30s']} / {d['first_hook_le_60s']}"),
    ('  hook before the first verse', lambda d: d['hook_before_first_verse']),
    ('  first return anchor — median time', lambda d: iq(d['first_anchor'])),
    ('  hook occurrences: 2 / 3 / 4+', lambda d: f"{d['hook_count'].get('2', 0)} / {d['hook_count'].get('3', 0)} / {d['hook_count'].get('4', 0) + d['hook_count'].get('5+', 0)}"),
    ('**Section lengths** — intro (felt bars)', lambda d: iq(d['intro_len_bars'], f='{:.1f}')),
    ('  first hook (felt bars)', lambda d: iq(d['hook1_len_bars_map'], f='{:.1f}')),
    ('  first verse (felt bars)', lambda d: iq(d['first_verse_len_bars'], f='{:.1f}')),
    ('  verse 2 shorter / similar / longer than verse 1', lambda d: f"{d['verse2_shorter'].split('/')[0]} / {d['verse2_similar'].split('/')[0]} / {d['verse2_longer'].split('/')[0]} (of {d['verse2_longer'].split('/')[1]})"),
    ('  last hook longer than the first (by 25%+)', lambda d: d['last_hook_longer']),
    ('**Riding the beat** — verse syllables per second', lambda d: iq(d['verse_sylls_per_s'], f='{:.1f}')),
    ('  verse syllables per felt beat', lambda d: iq(d['verse_sylls_per_beat'], f='{:.1f}')),
    ('  verse denser than hook (words per second)', lambda d: d['verse_denser_than_hook']),
]
GM = G + [('style_trap', 'Trap-tagged'), ('style_verse_led', 'Verse-led-tagged')]
outm = ['| Measure | ' + ' | '.join(l for _, l in GM) + ' |', '|---|' + '---|' * len(GM)]
for name, fn in mrows:
    cells = []
    for g, _ in GM:
        try: cells.append(fn(MS[g]))
        except Exception as e: cells.append('?')
    outm.append(f'| {name} | ' + ' | '.join(cells) + ' |')
open(OUTM, 'w').write('\n'.join(outm) + '\n')
print('\n'.join(outm))
