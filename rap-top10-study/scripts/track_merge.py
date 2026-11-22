"""Merge research + verify + gap sweeps per track into one measurement record.

Order of operations (documented in README / 03):
 1. Pick the best research record (prefer group-study chunk runs, then more sources).
 2. Merge the independent verifier: a 'corrected' value wins; 'confirmed' keeps the research value.
 3. Apply the verifier's rejections (corrections.VERIFIER_DOWNGRADES): a sourced claim the verifier
    could not support drops to basis 'unconfirmed' (kept, never counted as sourced).
 4. Apply the gap sweeps (run after the verifier): a sweep value replaces the current one only when
    its basis is stronger (source > unconfirmed > recollection > unknown).
 5. Apply credit, typing and tempo corrections (corrections.py) and label every felt value's basis.
"""
import json, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrections as C
from paths import WORK
c = json.load(open(WORK + 'collected.json'))
RANK = {'source': 3, 'unconfirmed': 2, 'unverified_recollection': 1, 'unknown': 0, None: 0}
HOOK_ORDER = {'present_verified': 3, 'absent_verified': 3, 'present_unverified': 1, 'absent_unverified': 1, 'unknown': 0, None: 0}


def best_research(rs):
    def score(r):
        chunk = 1 if 'chunk' in r.get('_run', '') else 0
        return (chunk, len(r.get('sources') or []), 0 if r.get('runtime_mmss') else -1)
    rs = [r for r in rs if r.get('version_used')]
    return sorted(rs, key=score)[-1] if rs else None


def best_verify(vs):
    vs = [v for v in vs if 'chunk' in v.get('_run', '')] or vs
    return vs[-1] if vs else None


def secs(m):
    if not m: return None
    mm = re.match(r'^(\d+):(\d{2})$', str(m).strip())
    return int(mm.group(1)) * 60 + int(mm.group(2)) if mm else None


def borrow_type(sm):
    hu = (sm.get('how_used') or '').lower() + ' ' + (sm.get('work') or '').lower()
    if re.search(r'\b(own|reuses?|reused)\b', hu) or 'push ups' in hu: return 'self-reuse'
    if any(w in hu for w in ['dialogue', 'talking', 'skit', 'speech', 'scene', 'monologue', 'interview', 'speaking voice']): return 'audio clip'
    if 'interpol' in hu: return 'interpolation'
    return 'sample'


out = {}
for cid, rs in c['research'].items():
    r = best_research(rs)
    if not r: continue
    icid = int(cid)
    v = best_verify(c['verify'].get(cid, []))
    rec = dict(cid=icid, title=r.get('title'), artists=r.get('artists'), album=r.get('album'), version_used=r.get('version_used'),
               producers=r.get('producers'), style_tag=r.get('style_tag'), style_basis=r.get('style_basis'))
    # ---- runtime
    rt = r.get('runtime_mmss'); rt_status = 'research_only'
    if v:
        if v.get('runtime_status') == 'corrected' and v.get('runtime_mmss'): rt = v['runtime_mmss']; rt_status = 'corrected_by_verifier'
        elif v.get('runtime_status') == 'confirmed': rt_status = 'verified'
        elif v.get('runtime_status') == 'unverifiable': rt_status = 'verifier_could_not_confirm'
    rec.update(runtime_mmss=rt, runtime_s=secs(rt), runtime_status=rt_status)
    # ---- tempo
    g, f = r.get('grid_bpm'), r.get('felt_bpm'); t_status = 'research_only'
    listed = list(r.get('tempo_listed') or [])
    if v:
        listed += [dict(x, _by='verifier') for x in (v.get('tempo_values_found') or [])]
        ts = v.get('tempo_status')
        if ts == 'corrected' and v.get('grid_bpm'): g, f = v.get('grid_bpm'), v.get('felt_bpm'); t_status = 'corrected_by_verifier'
        elif ts == 'confirmed': t_status = 'verified'
        elif ts == 'conflict': t_status = 'conflict'
        elif ts == 'unverifiable': t_status = 'verifier_could_not_confirm'
    rec.update(grid_bpm=g, felt_bpm=f, feel_basis=r.get('feel_basis'), tempo_status=t_status, tempo_listed=listed, key=r.get('key'))

    # ---- structural fields (research vs verifier)
    def pick(field, basis_field, vfield=None, vbasis=None, vstatus=None):
        val, basis = r.get(field), r.get(basis_field) if basis_field else None
        if v and vfield and v.get(vfield) not in (None, 'unknown'):
            vb = v.get(vbasis) if vbasis else ('source' if v.get(vstatus) in ('confirmed', 'corrected') else None)
            if v.get(vstatus) == 'corrected' or RANK.get(vb, 0) > RANK.get(basis, 0):
                val, basis = v.get(vfield), vb or basis
        return val, basis
    rec['opening_element'], rec['opening_basis'] = pick('opening_element', 'opening_basis', 'opening_element', None, 'opening_status')
    rec['hook_first'], rec['hook_first_basis'] = pick('hook_first', 'hook_first_basis', 'hook_first', 'hook_first_basis', 'opening_status')
    hs = r.get('hook_status')
    if v and v.get('hook_status') and v['hook_status'] != 'unknown' and HOOK_ORDER.get(v['hook_status'], 0) >= HOOK_ORDER.get(hs, 0):
        hs = v['hook_status']
    rec['hook_status'] = hs
    rec['beat_switch'], rec['beat_switch_basis'] = pick('beat_switch', 'beat_switch_basis', 'beat_switch', 'beat_switch_basis', 'beat_switch_status')
    rec.update(beat_switch_detail=r.get('beat_switch_detail'), beat_switch_time=r.get('beat_switch_time'),
               producer_tag=r.get('producer_tag_present'), producer_tag_detail=r.get('producer_tag_detail'),
               first_lead_vocal_time=r.get('first_lead_vocal_time'), first_hook_time=r.get('first_hook_time'),
               hook_description=r.get('hook_description'), return_anchor=r.get('return_anchor'), hook_devices=r.get('hook_devices') or [],
               samples=[dict(s) for s in (r.get('samples') or [])], features=r.get('features') or [],
               delivery=[dict(d) for d in (r.get('delivery_observations') or [])], returns=[dict(d) for d in (r.get('section_return_changes') or [])],
               section_order=r.get('section_order'), section_order_basis=r.get('section_order_basis'), most_audible_change=r.get('most_audible_change'),
               unknowns=r.get('unknowns') or [], sources=r.get('sources') or [],
               flagged=(v or {}).get('flagged_claims') or [], upgraded=(v or {}).get('upgraded_to_source') or [],
               verify_confidence=(v or {}).get('overall_confidence'), verified=bool(v), research_run=r.get('_run'))

    # ---- 3. verifier rejections
    applied = []
    for fld, act in C.VERIFIER_DOWNGRADES.get(icid, {}).items():
        if fld == 'hook_status':
            if act == 'unknown' or rec['hook_status'] == 'present_verified':
                rec['hook_status'] = act; applied.append(f'hook_status->{act}')
        elif fld == 'beat_switch_time':
            if rec.get('beat_switch_time'): rec['beat_switch_time'] = None; applied.append('beat_switch_time dropped')
        else:
            vf, bf = {'opening': ('opening_element', 'opening_basis'), 'hook_first': ('hook_first', 'hook_first_basis'),
                      'beat_switch': ('beat_switch', 'beat_switch_basis')}[fld]
            if rec.get(bf) == 'source':
                if act == 'unknown': rec[vf], rec[bf] = 'unknown', 'unknown'
                else: rec[bf] = 'unconfirmed'
                applied.append(f'{fld}->{act}')
    if icid in C.RETURNS_UNCONFIRMED:
        for d in rec['returns']:
            if d.get('basis') == 'source': d['basis'] = 'unconfirmed'
        applied.append('returns->unconfirmed')
    rec['verifier_applied'] = applied

    # ---- 4. gap sweeps
    sw = c.get('sweeps', {})
    for tsw in sw.get('tempo', {}).get(cid, []):
        if tsw.get('values'):
            rec['tempo_listed'] = rec['tempo_listed'] + [dict(x, _by='tempo_sweep') for x in tsw['values']]
        if not rec['grid_bpm'] and tsw.get('grid_bpm'):
            rec['grid_bpm'], rec['felt_bpm'] = tsw['grid_bpm'], tsw.get('felt_bpm'); rec['tempo_status'] = 'tempo_sweep'
        if not rec['runtime_s'] and tsw.get('runtime_mmss'):
            rec['runtime_mmss'] = tsw['runtime_mmss']; rec['runtime_s'] = secs(tsw['runtime_mmss']); rec['runtime_status'] = 'tempo_sweep'
    for ssw in sw.get('structure', {}).get(cid, []):
        for fv, fb in [('opening_element', 'opening_basis'), ('hook_first', 'hook_first_basis'), ('beat_switch', 'beat_switch_basis')]:
            if ssw.get(fv) and ssw.get(fv) != 'unknown' and RANK.get(ssw.get(fb), 0) > RANK.get(rec.get(fb), 0):
                rec[fv], rec[fb] = ssw[fv], ssw[fb]; rec.setdefault('structure_sweep_used', []).append(fv)
        if HOOK_ORDER.get(ssw.get('hook_status'), 0) > HOOK_ORDER.get(rec.get('hook_status'), 0):
            rec['hook_status'] = ssw['hook_status']; rec.setdefault('structure_sweep_used', []).append('hook_status')
        if ssw.get('first_hook_time') and not rec.get('first_hook_time'): rec['first_hook_time'] = ssw['first_hook_time']
        if ssw.get('section_order') and RANK.get(ssw.get('section_order_basis'), 0) > RANK.get(rec.get('section_order_basis'), 0):
            rec['section_order'], rec['section_order_basis'] = ssw['section_order'], ssw['section_order_basis']
        rec['structure_notes'] = ssw.get('notable') or []
        rec['hook_device_sweep'] = ssw.get('hook_device'); rec['return_anchor_sweep'] = ssw.get('return_anchor')
        rec['opening_source_sweep'] = ssw.get('opening_source')

    # ---- 5a. tempo corrections
    removed = []
    keep = []
    for x in rec['tempo_listed']:
        site = (x.get('site') or x.get('source') or '').lower()
        if any(x.get('bpm') == b and s.lower() in site for b, s in C.TEMPO_OUTLIERS.get(icid, [])): removed.append(x)
        else: keep.append(x)
    rec['tempo_listed'], rec['tempo_outliers_removed'] = keep, removed
    if not rec.get('grid_bpm'): rec['tempo_status'] = 'missing'; rec['felt_bpm'] = None
    if rec.get('grid_bpm'): rec['grid_bpm'] = round(float(rec['grid_bpm']))
    if rec.get('felt_bpm'): rec['felt_bpm'] = round(float(rec['felt_bpm']) * 2) / 2
    if icid in C.FEEL_UNRESOLVED_VERIFIER:
        if icid == 9: rec['grid_bpm'] = 193      # the only listed value; 96 was a halving, not a listing
        rec['felt_bpm'] = None; rec['tempo_status'] = 'feel_unresolved'; rec['tempo_note'] = C.FEEL_UNRESOLVED_VERIFIER[icid]
    if rec['title'] == 'Just Wanna Rock':
        rec['grid_bpm'] = rec['felt_bpm'] = None; rec['tempo_status'] = 'feel_unresolved'
        rec['tempo_note'] = 'One site lists 75 (the 122 listing could not be reproduced); 150 would be a doubling. Pulse unresolved.'
    if rec.get('grid_bpm') and not rec.get('felt_bpm') and rec['tempo_status'] not in ('feel_unresolved',):
        rec['tempo_status'] = 'feel_unresolved'; rec['tempo_note'] = 'One listed value; the verifier left the half/double-time reading unresolved.'
    if rec.get('felt_bpm') and rec.get('feel_basis') in (None, 'unknown', ''): rec['feel_basis'] = 'genre_convention_inference'
    if not rec.get('felt_bpm'): rec['feel_basis'] = None

    # ---- 5b. credits
    if rec['title'] == 'Rich Flex':
        rec['samples'] = [{'work': "'Welcome to the Hive'; 'I Want You, Girl' (credited in Wikipedia's sample notes, per verifier)", 'how_used': "Credited samples; the earlier 'unidentified soundtrack' attribution was contradicted by the verifier.", 'source': 'https://en.wikipedia.org/wiki/Rich_Flex', 'status': 'confirmed'}] + [x for x in rec['samples'] if 'Megan' in (x.get('work') or '')]
    if icid in C.SAMPLE_REPLACE:
        drop, new = C.SAMPLE_REPLACE[icid]
        rec['samples'] = [x for x in rec['samples'] if drop not in (x.get('work') or '')] + [dict(n) for n in new]
    rec['samples'] += [dict(n) for n in C.SAMPLE_ADD.get(icid, [])]
    for sm in rec['samples']:
        w = sm.get('work') or ''
        for (k, sub), new in C.SAMPLE_RENAME.items():
            if k == icid and sub in w: sm['work_original'] = w; sm['work'] = new
        sm['borrow_type'] = ('interpolation' if any(k == icid and sub in w for k, sub in C.FORCE_INTERPOLATION) else
                             'sample' if any(k == icid and sub in w for k, sub in C.FORCE_SAMPLE) else borrow_type(sm))
        hu = (sm.get('how_used') or '').lower()
        sm['credited'] = not any(x in hu for x in ['without credit', 'uncredited', 'not credited'])
        sm.setdefault('status', 'cited' if 'http' in (sm.get('source') or '') else 'uncited')
        for (k, sub), st in C.SAMPLE_STATUS.items():
            if k == icid and sub in w: sm['status'] = st
        for (k, sub), ov in C.SAMPLE_FORCE.items():
            if k == icid and sub in w: sm.update(ov)
    out[icid] = rec

json.dump(out, open(WORK + 'tracks_merged.json', 'w'), indent=1)
print(len(out), 'tracks merged;', sum(1 for x in out.values() if x['verified']), 'with verification;',
      sum(1 for x in out.values() if x['verifier_applied']), 'with verifier rejections applied')
