"""Render the 'measured counts at a glance' table for 03-findings.md from findings_stats.json."""
import json
SP = '/tmp/claude-0/-home-user-app-policies/08207d95-5f38-5913-acec-14c31ee115ad/scratchpad/'
F = json.load(open(SP + 'data/findings_stats.json'))
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
    ('Median felt BPM', felt),
    ('Half-time feel (grid ≈ 2× felt)', lambda d: d['feel_half_time']),
    ('  median felt, half-time', lambda d: f"{d['half_time_felt'].get('median','?')}"),
    ('Full-time feel', lambda d: d['feel_full_time']),
    ('  of which 95–115 bounce/pop-rap', lambda d: d['felt_full_95_115']),
    ('Documented sample / interpolation', lambda d: d['samples']),
    ('Credited featured artist', lambda d: d['features']),
    ('Hook present — sourced / unverified', lambda d: f"{d['hook_present_verified']} / {d['hook_present_unverified']}"),
    ('No conventional hook (unverified)', lambda d: str(d['hook_absent'])),
    ('Hook status unknown', lambda d: str(d['hook_unknown'])),
    ('Opens on hook — sourced yes / no', lambda d: f"{d['hook_first_yes_src']} / {d['hook_first_no_src']}"),
    ('Opens on hook — recollection yes / no', lambda d: f"{d['hook_first_yes_rec']} / {d['hook_first_no_rec']}"),
    ('Beat switch — sourced / recollection', lambda d: f"{d['switch_yes_src']} / {d['switch_yes_rec']}"),
    ('Beat switch unknown', lambda d: str(d['switch_unknown'])),
]
out = ['| Measure | ' + ' | '.join(l for _, l in G) + ' |', '|---|' + '---|' * len(G)]
for name, fn in rows:
    out.append(f'| {name} | ' + ' | '.join(fn(F[g]) for g, _ in G) + ' |')
open(SP + 'out/counts_table.md', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
