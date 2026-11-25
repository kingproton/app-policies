"""Add measured values to each track record (tracks_merged.json, key 'm').

Inputs, all in data/measured/ (derived numbers only: no lyric text, no audio):
  apple_catalog.json              runtime of the Apple catalog track matched by title and artist (where several editions
                                  matched, the one closest to the earlier cited runtime was preferred)
  lyric_structure_algorithm.json  timing and structure from one LRCLIB time-synced lyric record per track (repetition detector)
  lyric_structure_review.json     an independent read of the same record, with a ruling wherever the two readings disagreed
  lyric_structure_second_run.json a second, separate run of that read and ruling; used only as a consistency check
  audio_feel.json                 pulse tempo and backbeat (felt) tempo of Apple's 30-second preview clip
  page_claims.json                page-level verdicts on the earlier sourced claims (applied here, in apply_page_claims)

Basis codes written here
  lyric timing   A = algorithm and reviewer agree; J = they disagreed and a second reader ruled; G = algorithm only;
                 X = unresolved or unusable record (not counted)
  feel           M = clear in the clip (margin >= 0.15 and score >= 0.25); L = leaning (margin >= 0.07, score >= 0.15);
                 I = unclear in the clip, but only one of the two octave readings lies in 55-150 BPM; ? = unresolved
                 (an L or I reading whose pulse matches no published listing at the same, half or double tempo is also
                 set to ?, because an unclear clip reading that the listings contradict is not resolved)
Nothing in this stage comes from recollection.
"""
import json, os, sys, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrections as C
from paths import WORK, REPO
MD = REPO + 'data/measured/'


def load(name, default=None):
    p = MD + name
    return json.load(open(p)) if os.path.exists(p) else default


T = json.load(open(WORK + 'tracks_merged.json'))
AP = load('apple_catalog.json', {}); LA = load('lyric_structure_algorithm.json', {}); LR = load('lyric_structure_review.json', {}); AF = load('audio_feel.json', {})
LR2 = load('lyric_structure_second_run.json', {})
FELT_RANGE = (55.0, 150.0)


def feel_block(a):
    if not a or 'felt_bpm' not in a: return None
    est, alt = a['felt_bpm'], a.get('runner_up')
    conf = 'clear' if (a['margin'] >= 0.15 and a['score'] >= 0.25) else ('leaning' if (a['margin'] >= 0.07 and a['score'] >= 0.15) else 'unclear')
    inr = lambda x: x is not None and FELT_RANGE[0] <= x <= FELT_RANGE[1]
    felt, basis = None, '?'
    if conf == 'clear': felt, basis = est, 'M'
    elif inr(est) != inr(alt):                      # exactly one reading is in the plausible range
        if inr(est): felt, basis = est, ('L' if conf == 'leaning' else 'I')
        else: felt, basis = alt, 'I'
    elif conf == 'leaning': felt, basis = est, 'L'
    cls = None if felt is None else ('slow' if felt < 90 else 'mid' if felt < 120 else 'fast')
    # grid tempo for display: the faster of the two readings in play (a DAW grid is never slower than the felt pulse)
    grid = max(a['pulse_bpm'], felt) if felt is not None else max(a['pulse_bpm'], est, alt or 0)
    return dict(pulse_bpm=a['pulse_bpm'], grid_bpm=grid, estimate_bpm=est, other_reading_bpm=alt, score=a['score'], margin=a['margin'], confidence=conf,
                felt_bpm=felt, basis=basis, feel_class=cls, displaced_backbeat=a.get('displaced_backbeat'), clip_s=a.get('duration_s'))


def _run_final(v):
    """Final values of one review run for a track: the ruling where its readings disagreed, the reader's where they agreed."""
    rv = (v or {}).get('reviewer') or {}; ru = (v or {}).get('ruling')
    if (v or {}).get('status') == 'adjudicated' and ru and ru.get('resolution') != 'unresolved': src = ru
    elif (v or {}).get('status') == 'agree': src = rv
    else: return None
    sec = rv.get('sections') or []
    has = src['has_recurring_hook']; fh = src.get('first_hook_s')
    return dict(has_hook=has, first_hook_s=fh, first_line_s=src['first_line_s'], hook_count=len(src.get('hook_starts_s') or []) if has else 0,
                hook_before_first_verse=None if (not has or fh is None) else not any(x['label'] == 'verse' and x['start_s'] < fh - 1.0 for x in sec),
                first_section=sec[0]['label'] if sec else None, n_verses=sum(1 for x in sec if x['label'] == 'verse'),
                first_line_kind=rv.get('first_line_kind'), hook_return=rv.get('hook_return'))


def lyric_block(cid):
    a = LA.get(cid)
    if not a or a.get('status') != 'ok': return None
    r = LR.get(cid) or {}
    rv = r.get('reviewer'); ru = r.get('ruling'); status = r.get('status')
    b = dict(record_id=a.get('lrclib_id'), record_duration_s=a.get('lrc_duration'), match_tier=a.get('match_tier'), n_records_agreeing=a.get('n_records'),
             first_line_spread_s=a.get('first_line_spread_s'), first_hook_spread_s=a.get('first_hook_spread_s'), n_lines=a.get('n_lines'))
    alg = dict(first_line_s=a['first_line_s'], has_hook=a['has_returning_hook'], first_hook_s=a['first_hook_s'], lines_before_hook=a['lines_before_first_hook'],
               hook_starts=[s['start'] for s in a['sections'] if s['label'] == 'HOOK'],
               first_hook_len_s=(a['hook_durations_s'] or [None])[0])
    if status == 'agree' and rv and rv.get('record_ok', True):
        fin = dict(first_line_s=rv['first_line_s'], has_hook=rv['has_recurring_hook'], first_hook_s=rv['first_hook_s'], lines_before_hook=rv['lines_before_first_hook'],
                   hook_starts=rv['hook_starts_s'], first_hook_len_s=(rv['first_hook_end_s'] - rv['first_hook_s']) if (rv.get('first_hook_end_s') and rv.get('first_hook_s') is not None) else alg['first_hook_len_s'])
        basis = 'A'
    elif status == 'adjudicated' and ru:
        if ru['resolution'] == 'unresolved': fin, basis = dict(alg), 'X'
        else:
            fin = dict(first_line_s=ru['first_line_s'], has_hook=ru['has_recurring_hook'], first_hook_s=ru['first_hook_s'], lines_before_hook=ru['lines_before_first_hook'],
                       hook_starts=ru['hook_starts_s'], first_hook_len_s=None)
            # keep a hook length only from a reading whose first hook time the ruling kept
            if rv and rv.get('first_hook_s') is not None and fin['first_hook_s'] is not None and abs(rv['first_hook_s'] - fin['first_hook_s']) <= 1.0 and rv.get('first_hook_end_s'):
                fin['first_hook_len_s'] = rv['first_hook_end_s'] - rv['first_hook_s']
            elif alg['first_hook_s'] is not None and fin['first_hook_s'] is not None and abs(alg['first_hook_s'] - fin['first_hook_s']) <= 1.0:
                fin['first_hook_len_s'] = alg['first_hook_len_s']
            basis = 'J'
    elif rv and not rv.get('record_ok', True) and status != 'adjudicated': fin, basis = dict(alg), 'X'
    elif status == 'disputed_no_ruling': fin, basis = dict(alg), 'X'      # the two readings disagree and nothing ruled: not counted
    else: fin, basis = dict(alg), 'G'
    b.update(fin); b['basis'] = basis
    b['hook_first'] = None if not b['has_hook'] or b['lines_before_hook'] is None else (b['lines_before_hook'] <= 3)
    # first return anchor: the earliest line of ANY block that comes back later (repetition detector; definition-free)
    cl = {}
    for sct in a['sections']:
        if sct.get('cluster') is not None: cl[sct['cluster']] = cl.get(sct['cluster'], 0) + 1
    rec = [sct['start'] for sct in a['sections'] if sct.get('cluster') is not None and cl[sct['cluster']] >= 2]
    b['first_anchor_s'] = min(rec) if rec else None
    if b['has_hook'] and b['first_hook_s'] is not None and (b['first_anchor_s'] is None or b['first_hook_s'] < b['first_anchor_s']): b['first_anchor_s'] = b['first_hook_s']
    b['anchor_is_hook'] = None if b['first_anchor_s'] is None or b['first_hook_s'] is None else abs(b['first_anchor_s'] - b['first_hook_s']) <= 2.5
    b['hook_count'] = len(b['hook_starts'] or []) if b['has_hook'] else 0
    b['resolution'] = (ru or {}).get('resolution') if status == 'adjudicated' else None
    b['disagreed_on'] = r.get('why') or []
    if rv:
        b['first_line_kind'] = rv.get('first_line_kind'); b['hook_return'] = rv.get('hook_return'); b['reviewer_confidence'] = rv.get('confidence')
        b['sections'] = rv.get('sections'); b['reviewer_note'] = rv.get('note')
        # first verse: start, and length up to the next section
        sec = rv.get('sections') or []
        for i, s in enumerate(sec):
            if s['label'] == 'verse':
                b['first_verse_s'] = s['start_s']; b['first_verse_len_s'] = (sec[i + 1]['start_s'] - s['start_s']) if i + 1 < len(sec) else None
                break
        b['first_section'] = sec[0]['label'] if sec else None
        # section lengths from the reviewer's coarse map (the last section runs to the end of the record)
        # The last section ends two typical line gaps after the last lyric line (never past the end of the record), so that
        # an instrumental outro or fade after a final hook is not counted as hook.
        end_rec = a.get('lrc_duration') or (a.get('last_line_s') or 0) + 4
        end = min(end_rec, (a.get('last_line_s') or end_rec) + 2 * (a.get('median_line_gap_s') or 2.5))
        dur = [(sct['label'], (sec[i + 1]['start_s'] if i + 1 < len(sec) else end) - sct['start_s']) for i, sct in enumerate(sec)]
        b['verse_lens_s'] = [round(d, 1) for lab, d in dur if lab == 'verse' and d > 0]
        b['hook_lens_s'] = [round(d, 1) for lab, d in dur if lab == 'hook' and d > 0]
        b['n_verses'] = len(b['verse_lens_s']); b['section_labels'] = ' '.join({'intro': 'I', 'verse': 'V', 'pre_hook': 'p', 'hook': 'H', 'post_hook': 'q', 'bridge': 'B', 'outro': 'O', 'other': 'x'}[sct['label']] for sct in sec)
        b['has_bridge'] = any(sct['label'] == 'bridge' for sct in sec); b['has_pre_hook'] = any(sct['label'] == 'pre_hook' for sct in sec); b['has_post_hook'] = any(sct['label'] == 'post_hook' for sct in sec)
        b['ends_on'] = sec[-1]['label'] if sec else None
        # hook before the first verse: no verse section starts before the (final) first hook time
        if b['has_hook'] and b['first_hook_s'] is not None:
            b['hook_before_first_verse'] = not any(s['label'] == 'verse' and s['start_s'] < b['first_hook_s'] - 1.0 for s in sec)
        main = [s['start_s'] for s in sec if s['label'] in ('verse', 'hook')]
        # the ruled first hook counts too, where the reader's map labels it otherwise (#37 Young Metro: the ruling takes the title chant at 0:01)
        if b['has_hook'] and b['first_hook_s'] is not None: main.append(b['first_hook_s'])
        b['intro_len_s'] = min(main) if main else None
    # second, separate run of the read and ruling (consistency check only: it never changes a value)
    if cid in LR2 and basis in ('A', 'J'):
        r2 = _run_final(LR2[cid])
        if r2 is None: b['second_run'] = dict(status='no final reading'); b['second_run_code'] = 'n/a'
        else:
            same = dict(has_hook=r2['has_hook'] == b['has_hook'], first_line=abs(r2['first_line_s'] - b['first_line_s']) <= 1.0)
            if b['has_hook'] and r2['has_hook'] and b['first_hook_s'] is not None and r2['first_hook_s'] is not None:
                same['first_hook'] = abs(r2['first_hook_s'] - b['first_hook_s']) <= 2.5
                same['hook_count'] = abs(r2['hook_count'] - b['hook_count']) <= 1
                if b.get('hook_before_first_verse') is not None and r2['hook_before_first_verse'] is not None:
                    same['hook_before_first_verse'] = r2['hook_before_first_verse'] == b['hook_before_first_verse']
                same['hook_return'] = r2['hook_return'] == b.get('hook_return')
            same['first_section'] = r2['first_section'] == b.get('first_section')
            same['n_verses'] = r2['n_verses'] == b.get('n_verses')
            same['first_line_kind'] = r2['first_line_kind'] == b.get('first_line_kind')
            core = [same[k] for k in ('has_hook', 'first_line', 'first_hook', 'hook_count', 'hook_before_first_verse') if k in same]
            b['second_run'] = dict(status='compared', same=same, first_hook_s=r2['first_hook_s'], hook_count=r2['hook_count'], has_hook=r2['has_hook'],
                                   hook_before_first_verse=r2['hook_before_first_verse'])
            b['second_run_code'] = '=' if all(core) else 'differs: ' + ', '.join(k.replace('_', ' ') for k in ('has_hook', 'first_line', 'first_hook', 'hook_count', 'hook_before_first_verse') if same.get(k) is False)
    # algorithm-only density metrics (section boundaries from the repetition detector)
    for k in ('verse_words_per_s', 'hook_words_per_s', 'verse_sylls_per_s', 'hook_sylls_per_s', 'verse_median_line_gap_s', 'hook_median_line_gap_s', 'longest_gap_s', 'longest_gap_at_s', 'order'):
        b[k] = a.get(k)
    b['algorithm'] = alg
    return b


PC = load('page_claims.json', {})


def apply_page_claims(t, pc):
    """Apply page-level verdicts (first reader + skeptic + mechanical quote check) to the documented fields.
    supported         -> basis 'page' (P): the saved page text states it
    partly supported  -> a borrowing becomes P when the quoted words are in the saved page (the work is on the page; the
                         detail that is not is kept as a note and not counted); a beat switch becomes P only for the
                         songs hand-listed in corrections.PAGE_CORE; other fields keep their basis and get a note
    contradicted      -> opening, hook order, beat switch, return and delivery claims drop to 'unconfirmed' (U); never counted
    not addressed     -> nothing changes (the pages are silent)
    new page statements that survived the skeptic can set an unknown field or add a borrowing (corrections section 10)
    Each P records where it came from in *_page_origin: supported, partly_supported, statement or recoded."""
    log = dict(supported=0, partly_supported=0, contradicted=0, not_addressed=0, other=0)
    vd = {v['id']: v for v in pc.get('verdicts', [])}
    def fin(i): return (vd.get(i) or {}).get('final')
    for i, v in vd.items(): log[v['final'] if v['final'] in log else 'other'] += 1
    for fld, key in (('opening', 'opening_basis'), ('beat_switch', 'beat_switch_basis'), ('hook_first', 'hook_first_basis')):
        f = fin(fld)
        if f == 'supported' and t.get(key) in ('source', 'unconfirmed', 'unverified_recollection'): t[key] = 'page'; t[fld + '_page_origin'] = 'supported'
        elif f == 'contradicted' and t.get(key) in ('source', 'unconfirmed', 'unverified_recollection'):
            t[key] = 'unconfirmed'; t[fld + '_page_note'] = vd[fld]['note']
        elif f == 'partly_supported': t[fld + '_page_note'] = vd[fld]['note']
    for k, smp in enumerate(t.get('samples') or []):
        f = fin(f'borrow_{k + 1}')
        if f == 'supported' and smp.get('status') in ('cited', 'confirmed', 'not_reconfirmed'): smp['status'] = 'page'; smp['page_origin'] = 'supported'
        elif f == 'partly_supported':
            smp['page_note'] = vd[f'borrow_{k + 1}']['note']
            # the work itself is on the page even where a detail of the claim is not: count the borrowing, keep the note
            if smp.get('status') in ('cited', 'confirmed', 'not_reconfirmed') and vd[f'borrow_{k + 1}'].get('quote_in_page'): smp['status'] = 'page'; smp['page_origin'] = 'partly_supported'
        elif f == 'contradicted': smp['page_note'] = 'page text conflicts: ' + vd[f'borrow_{k + 1}']['note']
    for lst_key, pre in (('returns', 'return_'), ('delivery', 'delivery_')):
        for k, d in enumerate(t.get(lst_key) or []):
            f = fin(f'{pre}{k + 1}')
            if f == 'supported' and d.get('basis') in ('source', 'unconfirmed'): d['basis'] = 'page'
            elif f == 'contradicted' and d.get('basis') in ('source', 'unconfirmed'): d['basis'] = 'unconfirmed'; d['page_note'] = vd[f'{pre}{k + 1}']['note']
    # ---- hand-coded page maps (corrections.py, section 10); each applies only if its verdict or statement was kept
    kept = pc.get('new_facts', [])
    def has_fact(cat, words): return any(f['category'] == cat and words.lower() in f['statement'].lower() for f in kept)
    cid = t['cid']; applied = []
    if cid in C.PAGE_CORE.get('beat_switch', ()) and fin('beat_switch') == 'partly_supported' and t.get('beat_switch') == 'yes':
        t['beat_switch_basis'] = 'page'; t['beat_switch_page_origin'] = 'partly_supported'; applied.append('beat switch: core supported by page')
    if cid in C.PAGE_RECODE:
        fld, val = C.PAGE_RECODE[cid]
        if fin('opening') in ('contradicted', 'partly_supported'):
            t['opening_recoded_from'] = t.get(fld); t[fld] = val; t['opening_basis'] = 'page'; t['opening_page_origin'] = 'recoded'; applied.append(f'opening recoded to {val}')
    for c2, cat, words, fld, val in C.PAGE_FACT_SET:
        if c2 != cid or not has_fact(cat, words): continue
        bkey = 'beat_switch_basis' if fld == 'beat_switch' else 'opening_basis'
        if t.get(bkey) in ('source', 'page'): continue                       # already sourced: leave it
        t[fld] = val; t[bkey] = 'page'; t[('beat_switch' if fld == 'beat_switch' else 'opening') + '_page_origin'] = 'statement'; applied.append(f'{fld} set to {val} from a page statement')
    for words, work, btype, credited in C.PAGE_SAMPLE_ADD.get(cid, []):
        if not has_fact('borrowing', words): continue
        if any(words.lower() in (smp.get('work') or '').lower() for smp in t.get('samples') or []): continue
        t.setdefault('samples', []); t['samples'] = (t['samples'] or []) + [dict(work=work, borrow_type=btype, credited=credited,
                                                                              status='page', page_origin='statement', source='page statement', how_used='')]
        applied.append(f'borrowing added: {work[:40]}')
    hd = fin('hook_description')
    return dict(verdict_counts=log, applied=applied, hook_described_on_page=hd in ('supported', 'partly_supported', 'contradicted'),
                new_facts=pc.get('new_facts', []))


n_ap = n_ly = n_fe = n_pc = 0
for cid, t in T.items():
    m = {}
    if cid in PC:
        m['page'] = apply_page_claims(t, PC[cid]); n_pc += 1
    ap = (AP.get(cid) or {}).get('match')
    if ap and ap.get('duration_ms'):
        m['runtime_s'] = round(ap['duration_ms'] / 1000.0, 1); m['runtime_edition'] = ap.get('explicitness'); m['runtime_track'] = ap.get('track'); m['runtime_collection'] = ap.get('collection'); m['runtime_release_date'] = ap.get('release_date')
        if t.get('runtime_s'): m['runtime_minus_earlier_s'] = round(m['runtime_s'] - t['runtime_s'], 1)
        n_ap += 1
    # best available runtime: the Apple catalog duration, else the earlier cited runtime
    if m.get('runtime_s'): m['runtime_best_s'], m['runtime_best_basis'] = m['runtime_s'], 'catalog'
    elif t.get('runtime_s'): m['runtime_best_s'], m['runtime_best_basis'] = float(t['runtime_s']), 'cited'
    ly = lyric_block(cid)
    if ly: m['lyr'] = ly; n_ly += 1
    fe = feel_block(AF.get(cid))
    if fe:
        listed = sorted({x.get('bpm') for x in (t.get('tempo_listed') or []) if isinstance(x.get('bpm'), (int, float))})
        def related(p, l): return any(abs(l - p * k) / (p * k) <= 0.025 for k in (0.5, 1, 2))   # same test as measured_stats
        fe['listed_bpm'] = listed
        fe['pulse_matches_listing'] = None if not listed else any(related(fe['pulse_bpm'], l) for l in listed)
        if fe['basis'] in ('L', 'I') and fe['pulse_matches_listing'] is False:
            fe['basis_from_clip'] = fe['basis']; fe['felt_bpm_from_clip'] = fe['felt_bpm']
            fe['basis'] = '?'; fe['felt_bpm'] = None; fe['feel_class'] = None; fe['listing_conflict'] = True
            fe['grid_bpm'] = max(fe['pulse_bpm'], fe['estimate_bpm'], fe.get('other_reading_bpm') or 0)
        m['feel'] = fe; n_fe += 1
    # bars on the felt grid (4 felt beats per bar), only where a felt tempo was resolved
    if ly and fe and fe['felt_bpm']:
        bar = 240.0 / fe['felt_bpm']
        beat = 60.0 / fe['felt_bpm']
        m['ride'] = dict(verse_sylls_per_beat=None if not ly.get('verse_sylls_per_s') else round(ly['verse_sylls_per_s'] * beat, 2),
                         hook_sylls_per_beat=None if not ly.get('hook_sylls_per_s') else round(ly['hook_sylls_per_s'] * beat, 2),
                         verse_line_beats=None if not ly.get('verse_median_line_gap_s') else round(ly['verse_median_line_gap_s'] / beat, 2))
        m['bars'] = dict(bar_s=round(bar, 3),
                         verse_lens=[round(x / bar, 1) for x in (ly.get('verse_lens_s') or [])], hook_lens=[round(x / bar, 1) for x in (ly.get('hook_lens_s') or [])],
                         intro_len=None if ly.get('intro_len_s') is None else round(ly['intro_len_s'] / bar, 2),
                         first_line=round(ly['first_line_s'] / bar, 2),
                         first_hook=None if ly['first_hook_s'] is None else round(ly['first_hook_s'] / bar, 2),
                         first_hook_len=None if not ly.get('first_hook_len_s') else round(ly['first_hook_len_s'] / bar, 2),
                         first_verse_len=None if not ly.get('first_verse_len_s') else round(ly['first_verse_len_s'] / bar, 2))
    t['m'] = m
json.dump(T, open(WORK + 'tracks_merged.json', 'w'), indent=1)
print(f'measured blocks: runtime {n_ap}, lyric timing {n_ly}, feel {n_fe}, page claims {n_pc} of {len(T)} records; review file {"present" if LR else "absent"}')
