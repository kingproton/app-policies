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
