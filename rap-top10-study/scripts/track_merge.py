"""Merge research + verify per track into a final measurement record.
Rules (documented in the report):
 - Prefer group-study (chunk) research over salvaged per-track research; prefer the record with more sources.
 - Runtime: verify 'corrected' value wins; 'confirmed' keeps research value; else research value marked unverified.
 - Tempo: verify corrected grid/felt win; 'conflict' -> keep research value, flag conflict; listed values pooled.
 - Opening/hook_first/hook_status/beat_switch: take the value with the stronger basis (source > unverified_recollection > unknown);
   if verify corrected a sourced claim, verify wins; flagged_claims recorded.
"""
import json, re, statistics
SP='/tmp/claude-0/-home-user-app-policies/08207d95-5f38-5913-acec-14c31ee115ad/scratchpad/'
c=json.load(open(SP+'data/collected.json'))
RANK={'source':3,'unverified_recollection':1,'unknown':0,None:0}
def best_research(rs):
    def score(r):
        chunk = 1 if 'chunk' in r.get('_run','') else 0
        return (chunk, len(r.get('sources') or []), 0 if r.get('runtime_mmss') else -1)
    rs=[r for r in rs if r.get('version_used')]
    return sorted(rs,key=score)[-1] if rs else None
def best_verify(vs):
    vs=[v for v in vs if 'chunk' in v.get('_run','')] or vs
    return vs[-1] if vs else None
def secs(m):
    if not m: return None
    m=str(m).strip()
    mm=re.match(r'^(\d+):(\d{2})$',m)
    return int(mm.group(1))*60+int(mm.group(2)) if mm else None
out={}
for cid,rs in c['research'].items():
    r=best_research(rs)
    if not r: continue
    v=best_verify(c['verify'].get(cid,[]))
    rec=dict(cid=int(cid), title=r.get('title'), artists=r.get('artists'), album=r.get('album'), version_used=r.get('version_used'),
             producers=r.get('producers'), style_tag=r.get('style_tag'), style_basis=r.get('style_basis'))
    # runtime
    rt=r.get('runtime_mmss'); rt_status='research_only'
    if v:
        if v.get('runtime_status')=='corrected' and v.get('runtime_mmss'): rt=v['runtime_mmss']; rt_status='corrected_by_verifier'
        elif v.get('runtime_status')=='confirmed': rt_status='verified'
        elif v.get('runtime_status')=='unverifiable': rt_status='verifier_could_not_confirm'
    rec.update(runtime_mmss=rt, runtime_s=secs(rt), runtime_status=rt_status)
    # tempo
    g,f=r.get('grid_bpm'),r.get('felt_bpm'); t_status='research_only'
    listed=[x for x in (r.get('tempo_listed') or [])]
    if v:
        listed+= [dict(x,_by='verifier') for x in (v.get('tempo_values_found') or [])]
        ts=v.get('tempo_status')
        if ts=='corrected' and v.get('grid_bpm'): g,f=v.get('grid_bpm'),v.get('felt_bpm'); t_status='corrected_by_verifier'
        elif ts=='confirmed': t_status='verified'
        elif ts=='conflict': t_status='conflict'
        elif ts=='unverifiable': t_status='verifier_could_not_confirm'
    rec.update(grid_bpm=g, felt_bpm=f, feel_basis=r.get('feel_basis'), tempo_status=t_status, tempo_listed=listed, key=r.get('key'))
    # structural fields
    def pick(field, basis_field, vfield=None, vbasis=None, vstatus=None):
        val, basis = r.get(field), r.get(basis_field) if basis_field else None
        if v and vfield and v.get(vfield) not in (None,'unknown'):
            vb = v.get(vbasis) if vbasis else ('source' if v.get(vstatus) in ('confirmed','corrected') else None)
            if v.get(vstatus)=='corrected' or RANK.get(vb,0) > RANK.get(basis,0):
                val, basis = v.get(vfield), vb or basis
            elif v.get(vstatus)=='confirmed' and basis=='unverified_recollection':
                basis='unverified_recollection'  # confirmation without explicit source does not upgrade
        return val, basis
    rec['opening_element'], rec['opening_basis'] = pick('opening_element','opening_basis','opening_element',None,'opening_status')
    rec['hook_first'], rec['hook_first_basis'] = pick('hook_first','hook_first_basis','hook_first','hook_first_basis','opening_status')
    hs=r.get('hook_status')
    if v and v.get('hook_status') and v['hook_status']!='unknown':
        order={'present_verified':3,'absent_verified':3,'present_unverified':1,'absent_unverified':1,'unknown':0}
        if order.get(v['hook_status'],0)>=order.get(hs,0): hs=v['hook_status']
    rec['hook_status']=hs
    rec['beat_switch'], rec['beat_switch_basis'] = pick('beat_switch','beat_switch_basis','beat_switch','beat_switch_basis','beat_switch_status')
    rec.update(beat_switch_detail=r.get('beat_switch_detail'), beat_switch_time=r.get('beat_switch_time'),
               producer_tag=r.get('producer_tag_present'), producer_tag_detail=r.get('producer_tag_detail'),
               first_lead_vocal_time=r.get('first_lead_vocal_time'), first_hook_time=r.get('first_hook_time'),
               hook_description=r.get('hook_description'), return_anchor=r.get('return_anchor'), hook_devices=r.get('hook_devices') or [],
               samples=r.get('samples') or [], features=r.get('features') or [],
               delivery=[d for d in (r.get('delivery_observations') or [])], returns=[d for d in (r.get('section_return_changes') or [])],
               section_order=r.get('section_order'), section_order_basis=r.get('section_order_basis'), most_audible_change=r.get('most_audible_change'),
               unknowns=r.get('unknowns') or [], sources=r.get('sources') or [],
               flagged=(v or {}).get('flagged_claims') or [], upgraded=(v or {}).get('upgraded_to_source') or [],
               verify_confidence=(v or {}).get('overall_confidence'), verified=bool(v), research_run=r.get('_run'))
    # ---- gap sweeps (chunk 3) ----
    sw=c.get('sweeps',{})
    for tsw in sw.get('tempo',{}).get(cid,[]):
        if tsw.get('values'):
            rec['tempo_listed']=rec['tempo_listed']+[dict(x,_by='tempo_sweep') for x in tsw['values']]
        if not rec['grid_bpm'] and tsw.get('grid_bpm'):
            rec['grid_bpm'],rec['felt_bpm']=tsw['grid_bpm'],tsw.get('felt_bpm'); rec['tempo_status']='tempo_sweep'; rec['feel_basis']=rec.get('feel_basis') or 'genre_convention_inference'
        if not rec['runtime_s'] and tsw.get('runtime_mmss'):
            rec['runtime_mmss']=tsw['runtime_mmss']; rec['runtime_s']=secs(tsw['runtime_mmss']); rec['runtime_status']='tempo_sweep'
    for ssw in sw.get('structure',{}).get(cid,[]):
        for f,b in [('opening_element','opening_basis'),('hook_first','hook_first_basis'),('beat_switch','beat_switch_basis')]:
            if ssw.get(f) and ssw.get(f)!='unknown' and RANK.get(ssw.get(b),0)>RANK.get(rec.get(b),0):
                rec[f],rec[b]=ssw[f],ssw[b]; rec.setdefault('structure_sweep_used',[]).append(f)
        order={'present_verified':3,'absent_verified':3,'present_unverified':1,'absent_unverified':1,'unknown':0}
        if order.get(ssw.get('hook_status'),0)>order.get(rec.get('hook_status'),0): rec['hook_status']=ssw['hook_status']
        if ssw.get('first_hook_time') and not rec.get('first_hook_time'): rec['first_hook_time']=ssw['first_hook_time']
        if ssw.get('section_order') and RANK.get(ssw.get('section_order_basis'),0)>RANK.get(rec.get('section_order_basis'),0):
            rec['section_order'],rec['section_order_basis']=ssw['section_order'],ssw['section_order_basis']
        rec['structure_notes']=ssw.get('notable') or []
        rec['hook_device_sweep']=ssw.get('hook_device'); rec['return_anchor_sweep']=ssw.get('return_anchor')
    # ---- critic-driven cleanups ----
    if not rec.get('grid_bpm'): rec['tempo_status']='missing'; rec['felt_bpm']=None if not rec.get('felt_bpm') else rec['felt_bpm']
    if rec.get('grid_bpm'): rec['grid_bpm']=round(float(rec['grid_bpm']))
    if rec.get('felt_bpm'): rec['felt_bpm']=round(float(rec['felt_bpm'])*2)/2
    if rec['title']=='Rich Flex':
        rec['samples']=[{'work':"'Welcome to the Hive'; 'I Want You, Girl' (credited in Wikipedia's sample notes, per verifier)",'how_used':'Credited samples; the earlier \'unidentified soundtrack\' attribution was contradicted by the verifier.','source':'https://en.wikipedia.org/wiki/Rich_Flex'}]+[x for x in rec['samples'] if 'Megan' in (x.get('work') or '')]
    for sm in rec['samples']:
        hu=(sm.get('how_used') or '').lower()+' '+(sm.get('work') or '').lower()
        sm['borrow_type']=('self-reuse' if ('own ' in hu or 'reuse' in hu or 'push ups' in hu) else
                           'audio clip' if any(w in hu for w in ['film','talking','skit','speech','scene','monologue','interview']) else
                           'interpolation' if 'interpol' in hu else 'sample')
        sm['credited']=not any(w in hu for w in ['without credit','uncredited','not credited'])
    out[int(cid)]=rec
json.dump(out,open(SP+'data/tracks_merged.json','w'),indent=1)
print(len(out),'tracks merged;', sum(1 for x in out.values() if x['verified']),'with verification')
