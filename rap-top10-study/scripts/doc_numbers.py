"""Print every number cited in 01/02/03 docs from the final data, for patching."""
import json, statistics, collections
SP = '/tmp/claude-0/-home-user-app-policies/08207d95-5f38-5913-acec-14c31ee115ad/scratchpad/'
F = json.load(open(SP + 'data/findings_stats.json'))
rows = json.load(open(SP + 'data/final_rows.json'))
T = {int(k): v for k, v in json.load(open(SP + 'data/tracks_merged.json')).items()}
A = F['all']
print('M-1 half/full', A['feel_half_time'], A['feel_full_time'], 'half felt', A['half_time_felt'], 'full bands', A['full_time_bands'])
full = F['full_time']; print('   full list', full)
print('   kendrick full', sum(1 for x in full if any(k in x for k in ['Squabble', 'TV Off', 'Wacced', 'Hey Now', 'Reincarnated', 'Man At', 'Not Like', 'United In', 'N95', 'Silent', 'Luther', 'Euphoria'])))
print('M-2 samples', A['samples'], 'climbers', F['climbers']['samples'], 'debuts', F['debuts']['samples'])
cl = [r for r in rows if not r['debut_in_top10']]; de = [r for r in rows if r['debut_in_top10']]
print('M-3 climbers', len(cl), 'debuts', len(de), 'feat', F['climbers']['features'], F['debuts']['features'],
      'wks med', statistics.median([r['weeks_in_top10'] for r in cl]), statistics.median([r['weeks_in_top10'] for r in de]),
      'total wks med', statistics.median([r['total_weeks'] for r in cl]), statistics.median([r['total_weeks'] for r in de]))
print('   climbers', [(r['title'], r['weeks_in_top10'], r['climbed_from']) for r in cl])
print('   doja in climbers', sum(1 for r in cl if 'Doja' in r['artists']))
print('M-4 hook V/U/abs/unk', A['hook_present_verified'], A['hook_present_unverified'], A['hook_absent'], A['hook_unknown'], F['hookless'])
op = collections.Counter(x.split(': ')[1] for x in F['opening_sourced'])
print('M-5 opening sourced n', len(F['opening_sourced']), dict(op))
print('   hook-first src yes/no', A['hook_first_yes_src'], A['hook_first_no_src'], 'rec', A['hook_first_yes_rec'], A['hook_first_no_rec'])
print('   yes list', F['hook_first_yes']); print('   no list', F['hook_first_no'])
print('M-6 features', A['features'], 'voice-change returns', len(F['voice_change_returns']), F['voice_change_returns'], 'bomb feat', F['album_bomb']['features'])
print('M-7 switch src/rec/unk', A['switch_yes_src'], A['switch_yes_rec'], A['switch_unknown'], 'drake-credited src', F['drake_credit']['switch_yes_src'])
print('   list', F['beat_switch_sourced'])
print('M-8 runtime', A['runtime'], A['runtime_le_3min'], A['runtime_ge_4min'], 'bomb', F['album_bomb']['runtime']['median'], 'not', F['not_bomb']['runtime']['median'],
      'climb', F['climbers']['runtime'], 'drake', F['drake_credit']['runtime']['median'], 'nodrake', F['no_drake']['runtime']['median'])
print('   shortest', F['shortest'], 'longest', F['longest'])
print('M-9 delivery tracks', F['tracks_with_sourced_delivery'], {k: v[0] for k, v in F['delivery_aspects'].items()})
print('M-10 debuts', len(de), 'one-week', sum(1 for r in rows if r['weeks_in_top10'] == 1), 'bomb', sum(1 for r in rows if r['album_bomb']),
      'bomb one-week', sum(1 for r in rows if r['album_bomb'] and r['weeks_in_top10'] == 1), 'leads', collections.Counter(r['lead_artist'] for r in rows).most_common(4), 'drill', F['drill'])
print('limits: returns tracks', F['tracks_with_sourced_returns'], 'timestamps', F['timestamps'])
print('runtime known', A['runtime']['n'], 'tempo known', A['felt']['n'])
print('cut', rows[-1]['title'], rows[-1]['first_top10'], '| provisional', [r['title'] for r in rows if 'provisional' in r['classification']])
