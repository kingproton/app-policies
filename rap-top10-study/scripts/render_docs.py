"""Fill the document templates (templates/*.tmpl.md) with numbers from the computed statistics, so that every figure in
01-studio-process.md, 03-findings.md, 05-measurement-method.md and README.md is read from the data rather than typed.

Template syntax: {{ python expression }} evaluated against the helpers below. An expression that fails stops the build.
"""
import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK, REPO
import shared_facts as SF
MS_ALL = json.load(open(WORK + 'measured_stats.json'))
MS = MS_ALL['groups']
FS = json.load(open(WORK + 'findings_stats.json'))
ST = json.load(open(WORK + 'stats.json'))
rows = json.load(open(WORK + 'final_rows.json'))
T = {int(k): v for k, v in json.load(open(WORK + 'tracks_merged.json')).items()}
status = {r['cid']: r for r in json.load(open(WORK + 'classification_status.json'))}
CC = {int(k): v for k, v in json.load(open(WORK + 'chart_check.json')).items()}
_dupt = {r['title'] for r in rows if sum(1 for x in rows if x['title'] == r['title']) > 1}
BY = {(f"{r['title']} ({r['lead_artist']})" if r['title'] in _dupt else r['title']): (r, T.get(r['cid']) or {}) for r in rows}


def mmss(s):
    if s is None: return '?'
    s = int(round(s)); return f"{s // 60}:{s % 60:02d}"


def bpm(x):
    """Show a tempo to the nearest half BPM (a 30-second clip does not support more)."""
    v = round(float(x) * 2) / 2
    return f"{v:g}"


def _t(title):
    if title not in BY: raise KeyError(f'no list song titled {title!r}')
    return BY[title]


def _l(title):
    l = (_t(title)[1].get('m') or {}).get('lyr')
    if not l or l.get('basis') not in ('A', 'J', 'G'): raise KeyError(f'no usable lyric timing for {title!r}')
    return l


def _f(title):
    f = (_t(title)[1].get('m') or {}).get('feel')
    if not f: raise KeyError(f'no clip for {title!r}')
    return f


# ---- per-track helpers (each raises if the value is missing, so a template can never print an empty number)
def n(title): return _t(title)[0]['n']
def hook(title):
    """First hook time for a named example. Refuses a track where the second, separate review run put the first hook
    more than 2.5 s away, and (for tracks the readers agreed on, basis A or G) a track whose matching lyric records
    disagree by more than 2.5 s. For ruled tracks (basis J) the records' spread is not tested: the ruling chose the block."""
    l = _l(title)
    if not l['has_hook']: raise KeyError(f'{title!r} has no recurring hook')
    if ((l.get('second_run') or {}).get('same') or {}).get('first_hook') is False: raise KeyError(f'{title!r}: the second review run put the first hook elsewhere')
    if l['basis'] in ('A', 'G') and (l.get('first_hook_spread_s') or 0) > 2.5: raise KeyError(f'{title!r}: lyric records disagree on the hook time by {l["first_hook_spread_s"]} s')
    return mmss(l['first_hook_s'])
def lbh(title): return _l(title)['lines_before_hook']
def fl(title):
    if (_l(title).get('first_line_spread_s') or 0) > 2.0: raise KeyError(f'{title!r}: lyric records disagree on the first line time')
    x = _l(title)['first_line_s']
    return mmss(x) if x >= 10 else f"{x:.1f} s"
def fl_any(title):
    """First-line time in the record used, with no test of how well the other matching records agree. Use only where the sentence says so."""
    return mmss(_l(title)['first_line_s'])
def fl_spread(title): return f"{_l(title).get('first_line_spread_s') or 0:.0f}"
def hooks(title): return _l(title)['hook_count']
def basis(title): return _l(title)['basis']
def felt(title):
    f = _f(title)
    if f['felt_bpm'] is None: raise KeyError(f'feel unresolved for {title!r}')
    return bpm(f['felt_bpm'])
def pulse(title): return bpm(_f(title)['grid_bpm'])
def pf(title):
    """'pulse 162, felt 81' style."""
    f = _f(title)
    if f['felt_bpm'] is None: raise KeyError(f'feel unresolved for {title!r}')
    return f"{bpm(f['grid_bpm'])}/{bpm(f['felt_bpm'])}" if abs(f['grid_bpm'] - f['felt_bpm']) > 1 else bpm(f['felt_bpm'])
def fbasis(title): return _f(title)['basis']
def rt(title): return mmss((_t(title)[1].get('m') or {})['runtime_best_s'])
def bars(title, key):
    b = (_t(title)[1].get('m') or {}).get('bars') or {}
    v = b.get(key)
    if isinstance(v, list): v = v[0] if v else None
    if v is None: raise KeyError(f'no {key} bars for {title!r}')
    return f"{v:.1f}".rstrip('0').rstrip('.')
def secs(title, key):
    v = _l(title).get(key)
    if isinstance(v, list): v = v[0] if v else None
    if v is None: raise KeyError(f'no {key} for {title!r}')
    return f"{v:.0f}"
def wps(title): return f"{_l(title)['verse_words_per_s']:.1f}"
def sps(title): return f"{_l(title)['verse_sylls_per_s']:.1f}"
def spb(title):
    r = (_t(title)[1].get('m') or {}).get('ride') or {}
    if not r.get('verse_sylls_per_beat'): raise KeyError(f'no syllables per beat for {title!r}')
    return f"{r['verse_sylls_per_beat']:.1f}"
def anchor(title): return mmss(_l(title)['first_anchor_s'])
def kind(title): return (_l(title).get('first_line_kind') or '?').replace('_', ' ')
def gap(title): return f"{_l(title)['longest_gap_s']:.0f} s from {mmss(_l(title)['longest_gap_at_s'])}"


# ---- group helpers
def g(group, key): return MS[group][key]
def q(group, key, part='median', fmt='{}'):
    v = MS[group][key][part]
    return fmt.format(v) if not isinstance(v, str) else v
def hq(group, key, part='median'):
    """A felt-tempo statistic to the nearest half BPM, as the counts table prints it."""
    return f"{round(float(MS[group][key][part]) * 2) / 2:g}"
def num(frac): return int(str(frac).split('/')[0])
def den(frac): return int(str(frac).split('/')[1])
def pct(frac): return f"{100 * num(frac) / den(frac):.0f}%"
def lst(key, k=None, sep='; '):
    v = MS_ALL[key]
    return sep.join(v if k is None else v[:k])
def cnt(key): return len(MS_ALL[key])
def titles(key, k=None):
    """Titles only from a named list of '#n Title (Artist): detail' strings."""
    out = []
    for x in MS_ALL[key][: k or None]:
        m = re.match(r'#\d+ (.*?)(?: \([^()]*\))?(?::| \[|$)', x)
        out.append(f'"{m.group(1)}"' if m else x)
    return ', '.join(out)
def fs(group, key): return FS[group][key]
def tier(t): return sum(1 for r in rows if status[r['cid']].get('tier') == t)
def cc(field, value): return sum(1 for v in CC.values() if v[field] == value)
def cls(group, key, c): return (MS[group].get(key) or {}).get(c, 0)
def ra(key, part=None):
    v = MS_ALL['record_agreement'][key]
    return v if part is None else v[part]
def top(key):
    return MS_ALL[key]
def sm(group, key, k): return (MS[group].get(key) or {}).get(k, 0)
def fr(c): return '–'.join(MS_ALL['feel_ranges'][c])
def sub(key, k, limit=None, sep=', '):
    v = MS_ALL[key][k]
    return sep.join(v if limit is None else v[:limit])


_CV = json.load(open(REPO + 'data/measured/chart_verification.json'))['weeks']
_GT = json.load(open(REPO + 'data/measured/genre_tables.json'))
def cv_weeks(): return SF.bc_weeks()['hosted']
def cv_full(): return SF.bc_weeks()['matching']          # every title, or all but one spelling variant, and all 25 detail rows
def cv_all100(): return SF.bc_weeks()['all100']
def cv_one_off(): return len(SF.bc_weeks()['one_title_differs'])
def cv_one_off_dates(): return ', '.join(SF.bc_weeks()['one_title_differs'])
def cv_other(): return SF.bc_weeks()['other'][0]
def cv_missing_dates(): return ', '.join(SF.bc_weeks()['missing_later'])
def inv_min(): return min(SF.yearend_inversions().values())
def inv_max(): return max(SF.yearend_inversions().values())
def inv_years(): return ', '.join(f'{y}: {k}' for y, k in sorted(SF.yearend_inversions().items()))
def dash_n(): return len(SF.dash_conflicts()['songs'])
def dash_tables(): return SF.dash_conflicts()['tables_with_rap_column']
def dash_read(): return SF.dash_conflicts()['tables_read']
def dash_example(title):
    x = [d for d in SF.dash_conflicts()['songs'] if d['title'] == title]
    if not x: raise KeyError(f'no dash conflict stored for {title!r}')
    x = x[0]
    def poss(p):
        nm = SF.page_name(p)
        return nm.replace(' (production)', '') + chr(39) + ('s production' if '(production)' in nm else 's')
    return (f"\"{x['title']}\" (dash in {' and '.join(poss(p) for p in x['dash_pages'])} table, No. {x['rap_peak_pages'][0][1]} in "
            f"{', '.join(poss(p) for p, n in x['rap_peak_pages'])})")
def cv_first(): return min(w['date'] for w in _CV if w['status'] == 'compared')
def cv_last(): return max(w['date'] for w in _CV if w['status'] == 'compared')
def cv_missing_later(): return sum(1 for w in _CV if w['status'] != 'compared' and w['date'] >= cv_first())
def bc_hosted(): return sum(1 for v in CC.values() if v['billboard_canada'] == 'match' or v['billboard_canada'].startswith('differs'))
def n_rap_tables(): return len({p for g_ in _GT for p in (g_.get('discog_rap_pages') or []) + (g_.get('discog_rap_dash_pages') or [])})   # tables that list a top-10 arrival in a rap column
def _med(v):
    v = sorted(v); n_ = len(v)
    m = v[n_ // 2] if n_ % 2 else (v[n_ // 2 - 1] + v[n_ // 2]) / 2
    return f"{m:g}"
def ST_climb_weeks(): return _med([r['weeks_in_top10'] for r in rows if not r['debut_in_top10']])
def ST_debut_weeks(): return _med([r['weeks_in_top10'] for r in rows if r['debut_in_top10']])
def climber_examples(k):
    c = sorted([r for r in rows if not r['debut_in_top10']], key=lambda r: -r['weeks_in_top10'])[:k]
    return '; '.join(f"\"{r['title']}\" ({r['weeks_in_top10']} weeks in the top 10, climbed from #{r['climbed_from']})" for r in c)
def _nohook_rts():
    v = [(T.get(r['cid']) or {}).get('m', {}).get('runtime_best_s') for r in rows
         if ((T.get(r['cid']) or {}).get('m', {}).get('lyr') or {}).get('basis') in ('A', 'J', 'G') and not (T[r['cid']]['m']['lyr']['has_hook'])]
    return [x for x in v if x]
def no_hook_rt_min(): return mmss(min(_nohook_rts()))
def no_hook_rt_max(): return mmss(max(_nohook_rts()))
SRCB = ('source', 'page')
def _sw(): return [(r, T[r['cid']]) for r in rows if (T.get(r['cid']) or {}).get('beat_switch') == 'yes' and T[r['cid']].get('beat_switch_basis') in SRCB]
def bs_n(): return len(_sw())
def bs_page_n(): return sum(1 for r, t in _sw() if t.get('beat_switch_basis') == 'page')
def bs_titles(): return ', '.join(f'"{_disp(r)}"' for r, t in _sw())
def bs_by(artist): return sum(1 for r, t in _sw() if artist in r['artists'])
def bs_unknown(): return sum(1 for r in rows if (T.get(r['cid']) or {}).get('beat_switch') in (None, 'unknown'))
def _disp(r): return f"{r['title']} ({r['lead_artist']})" if r['title'] in _dupt else r['title']
def _op(): return [(r, T[r['cid']]) for r in rows if (T.get(r['cid']) or {}).get('opening_element') not in (None, 'unknown') and T[r['cid']].get('opening_basis') in SRCB]
def op_n(): return len(_op())
def op_page_n(): return sum(1 for r, t in _op() if t.get('opening_basis') == 'page')
def op_kind(k): return sum(1 for r, t in _op() if t.get('opening_element') == k)
def op_titles(k, limit=None, basis=None):
    v = [f'"{_disp(r)}"' for r, t in _op() if t.get('opening_element') == k and (basis is None or t.get('opening_basis') == basis)]
    return ', '.join(v if limit is None else v[:limit])
def proc_total(): return MS_ALL['process']['statements']
def proc_tracks(): return MS_ALL['process']['tracks']
def proc_n(code): return (MS_ALL['process']['by_code'].get(code) or {}).get('tracks', 0)
def proc_titles(code, limit=None):
    """Titles under a process heading; 'among them' is prefixed when the list is cut short of the count."""
    v = [f'"{x}"' for x in (MS_ALL['process']['by_code'].get(code) or {}).get('titles', [])]
    if limit is None or len(v) <= limit:
        if len(v) != proc_n(code): raise KeyError(f'{code}: {len(v)} titles for a count of {proc_n(code)}')
        return ', '.join(v)
    return 'among them ' + ', '.join(v[:limit])
def fsx(key): return FS[key]
def bt(kind, i): return (FS['borrow_types'].get(kind) or [0, 0, [], 0])[i]
def pagefacts(cat, part='tracks'): return (MS_ALL['page_facts'].get(cat) or {}).get(part, 0)
_PCL = json.load(open(REPO + 'data/measured/page_claims.json')) if os.path.exists(REPO + 'data/measured/page_claims.json') else {}
def need(title, category, words):
    """Guard for a named example: a kept page statement of this category must contain these words. Prints nothing."""
    r, t = _t(title)
    for f in ((t.get('m') or {}).get('page') or {}).get('new_facts') or []:
        if f['category'] == category and words.lower() in (f['statement'] + ' ' + f['quote']).lower(): return ''
    raise KeyError(f'no kept {category} statement containing {words!r} for {title!r}')
def needv(title, verdict_id, words=''):
    """Guard for a named example: this claim's final verdict must be supported or partly supported, with these words in its quote or note."""
    r, t = _t(title)
    for v in (_PCL.get(str(r['cid'])) or {}).get('verdicts', []):
        if v['id'] == verdict_id and v['final'] in ('supported', 'partly_supported') and words.lower() in (v['quote'] + ' ' + v['note']).lower(): return ''
    raise KeyError(f'no supported verdict {verdict_id!r} containing {words!r} for {title!r}')
# ---- guards for hard-coded example sentences: each prints nothing and stops the build if the data no longer supports the sentence
def isfirst(key, title):
    if not MS_ALL[key] or not MS_ALL[key][0].startswith(f'"{title}"'): raise KeyError(f'{title!r} is not first in {key}')
    return ''
def fl_under(title, s):
    if _l(title)['first_line_s'] >= s: raise KeyError(f'first line of {title!r} is not under {s} s')
    return ''
def hook_after(title, s):
    l = _l(title)
    if not l['has_hook'] or l['first_hook_s'] <= s: raise KeyError(f'first hook of {title!r} is not after {s} s')
    return ''
def nohook(title):
    if _l(title)['has_hook']: raise KeyError(f'{title!r} has a recurring hook')
    return ''
def same_week(a, b):
    if _t(a)[0]['first_top10'] != _t(b)[0]['first_top10']: raise KeyError(f'{a!r} and {b!r} did not enter the top 10 in the same week')
    return ''
def climber(title):
    if _t(title)[0]['debut_in_top10']: raise KeyError(f'{title!r} debuted in the top 10')
    return ''
def needswitch(title):
    r, t = _t(title)
    if not (t.get('beat_switch') == 'yes' and t.get('beat_switch_basis') in SRCB): raise KeyError(f'no documented beat switch for {title!r}')
    return ''
def switch_undocumented(title):
    """No source or page documents a switch either way (a value held only from recollection does not count)."""
    t = _t(title)[1]
    if t.get('beat_switch') not in (None, 'unknown') and t.get('beat_switch_basis') in SRCB: raise KeyError(f'a beat switch value is documented for {title!r}')
    return ''
def noborrow(title):
    if any(x.get('status') in ('confirmed', 'cited', 'page', 'not_reconfirmed') for x in _t(title)[1].get('samples') or []): raise KeyError(f'{title!r} has a documented borrowing')
    return ''
def added(title):
    if not any(x.startswith(title + ':') for x in FS['borrow_page_added']): raise KeyError(f'no page-added borrowing for {title!r}')
    return ''
def rnote(title, words):
    """Guard: the AI reader's stored note on this track's lyric record contains these words."""
    if words.lower() not in (_l(title).get('reviewer_note') or '').lower(): raise KeyError(f'reader note for {title!r} does not contain {words!r}')
    return ''
# ---- second review run, page origins, claims summary, beat-switch status
def sr(key): return MS_ALL['second_run'][key]
def srn(key): return int(str(MS_ALL['second_run'][key]).split('/')[0])
def srd(key): return int(str(MS_ALL['second_run'][key]).split('/')[1])
def po(kind, key): return (MS_ALL['page_origins'].get(kind) or {}).get(key, 0)
def cs(key): return MS_ALL['claims_summary'][key]
def fsa(key): return FS['all'][key]
def sw_recollection(): return FS['all']['switch_no_any'] + FS['all']['switch_yes_rec']
_CC = json.load(open(WORK + 'chart_check.json'))
def w_match():
    """List songs whose first top-10 date matches Wikipedia's top-ten entry date."""
    return sum(1 for r in rows if (_CC.get(str(r['cid'])) or {}).get('wikipedia_entry_date', '').startswith('match'))
def n_candidates():
    import csv as _csv
    return sum(1 for _ in _csv.DictReader(open(REPO + 'data/classification_evidence.csv')))
_GT = json.load(open(REPO + 'data/measured/genre_tables.json'))
def summ_dash():
    """Summary-tier list songs whose only rap-column entry in a discography table is a dash."""
    ids = {r['title'] for r in rows if r['evidence_tier'] == 'summary'}
    v = [g for g in _GT if g.get('in_final') and g['title'] in ids]
    if any(g.get('discog_rap_peak') is not None for g in v): raise KeyError('a summary-tier song now has a table rap peak')
    return sum(1 for g in v if g.get('discog_rap_dash_pages'))
def rec_titles(): return ' and '.join(f'"{x}"' for x in cs('contradicted_recoded_titles'))
def mismatch_tail():
    return 'The other mismatches are not explained.' if MS_ALL['pulse_vs_listings'].get('disagree_matches_removed_outlier') else 'Those mismatches are not explained.'
def pulse_removed_clause():
    v = MS_ALL['pulse_vs_listings'].get('disagree_matches_removed_outlier') or []
    if not v: return ''
    return f" {len(v)} of the {MS_ALL['pulse_vs_listings']['disagree_single_listing']} ({', '.join(v)}) does match a listing that the earlier pass set aside as an outlier."
def leaned_clause():
    v = MS_ALL.get('feel_range_leaned_away') or []
    n = cnt('feel_range_rule')
    if not v: return f"On all {n} the clip did not separate the two readings."
    return (f"On {n - len(v)} of them the clip did not separate the two readings (margin {MS_ALL['feel_range_unclear_max_margin']:.2f} or less); "
            f"on {', '.join(v)} it leaned to the reading that was ruled out.")
def ret_sum():
    """Return-change types: say how many songs have both a beat and a voice change, and check the parts add up. Prints the clause or nothing."""
    a = FS['all']; both = a['return_beat'] + a['return_voice'] + a['return_register'] + a['return_delivery'] - (a['return_sourced_tracks'] - a['return_none'])
    if both != a.get('return_beat_voice', -1): raise KeyError('the return-change overlap is not only beat plus voice; reword the sentence')
    return '' if both == 0 else f" ({both} song{'s' if both > 1 else ''} with both a beat and a voice change)"
def sw_unconfirmed_only(title):
    """Guard: exactly one song holds a 'yes' that no page or cited source confirmed, and it is this one. Prints nothing."""
    v = [r['title'] for r in rows if (T.get(r['cid']) or {}).get('beat_switch') == 'yes' and T[r['cid']].get('beat_switch_basis') == 'unconfirmed']
    if v != [title]: raise KeyError(f'unconfirmed beat-switch songs are {v!r}, not [{title!r}]')
    if bs_n() + FS['all']['switch_unknown'] + sw_recollection() + 1 != len(rows): raise KeyError('beat-switch counts do not add up to the list')
    return ''
def UNMEASURED(): return ('where phrases start and stop against the drums and where rhymes land; the silence after a punchline; where ad-libs sit inside a bar; '
                          'what the drums, the 808, the melody and the vocal stack do when a section returns; and which of those changes is audible enough to matter')
def ex5(title):
    """M-5 example: first hook time, then first hook and first verse lengths in felt bars. Refuses a track that is not basis A with a clear felt tempo."""
    l = _l(title); f = _f(title)
    if l['basis'] != 'A' or f['basis'] != 'M': raise KeyError(f'{title!r} is not a both-readings-agree, clear-tempo example')
    b = _t(title)[1]['m']['bars']
    if not b.get('hook_lens') or b.get('first_hook_len') is None or abs(b['hook_lens'][0] - b['first_hook_len']) > 0.5:
        raise KeyError(f'{title!r}: the two first-hook lengths (tables 4b and 4b-2) disagree')
    return f"\"{title}\" ({hook(title)}; {bars(title, 'hook_lens')} / {bars(title, 'verse_lens')})"
def isverse3():
    """Guard for the M-4 exception sentence: the three named records are exactly the maps whose first section is a verse."""
    want = {'"Gimme A Hug"', '"Man At The Garden"', '"Sticky (Drake)"'}
    if set(MS_ALL['verse_first_section_list']) != want: raise KeyError(f"verse-first maps are now {MS_ALL['verse_first_section_list']}")
    return ''
def nohook_basis(code):
    return sum(1 for r in rows if ((T.get(r['cid']) or {}).get('m', {}).get('lyr') or {}).get('basis') == code and not T[r['cid']]['m']['lyr']['has_hook'])
def conflict(title):
    """'clip X, listed Y' for a track whose unclear clip reading matches no published tempo; refuses any other track."""
    f = _f(title)
    if not f.get('listing_conflict'): raise KeyError(f'{title!r} is not a clip-versus-listing conflict')
    return f"clip {bpm(f['felt_bpm_from_clip'])}, listed {' and '.join(f'{v:g}' for v in f['listed_bpm'])}"
_SY = json.load(open(REPO + 'data/measured/synthetic_feel_test.json'))
def synth(key): return _SY[key]
def _grades():
    """Exclusion grades as table 4d shows them (written by exclusion_grades.py)."""
    g_ = json.load(open(WORK + 'exclusion_grades.json')).values()
    return sum(1 for x in g_ if x in ('indirect', 'unresolved')), sum(1 for x in g_ if x == 'yearend')
def n_indirect(): return _grades()[0]
def n_yearend(): return _grades()[1]
def bs_climbers(): return sum(1 for r, t in _sw() if not r['debut_in_top10'])
def allof(a, b, mid='of those'):
    """'all 8' when the two counts are equal, otherwise '5 of those 8'."""
    return f'all {b}' if a == b else f'{a} {mid} {b}'
def bs_page_phrase():
    """How many of the documented beat switches rest on saved page text."""
    return 'all on saved page text' if bs_page_n() == bs_n() else f'{bs_page_n()} on saved page text'
def read_twice(): return sm('all', 'lyric_basis', 'A') + sm('all', 'lyric_basis', 'J')
def detector_only(): return sm('all', 'lyric_basis', 'G')
def climbers_by(artist): return sum(1 for r in rows if not r['debut_in_top10'] and artist in r['artists'])
def wk10(title): return _t(title)[0]['weeks_in_top10']
def peak(title): return _t(title)[0]['peak']
def open_table(name): return open(WORK + name).read().rstrip('\n')
def open_template(name): return render(open(REPO + 'templates/' + name).read(), name).rstrip('\n')


# The expressions come only from this repository's own template files (never from downloaded or user-supplied text),
# and they are evaluated with no builtins beyond the few named here, so a template can call the helpers above and
# nothing else (no imports, no file access).
SAFE_BUILTINS = {'len': len, 'min': min, 'max': max, 'round': round, 'int': int, 'float': float, 'str': str, 'sorted': sorted, 'sum': sum, 'abs': abs}
NS = {k: v for k, v in globals().items() if not k.startswith('_') and k not in ('json', 'os', 're', 'sys', 'glob')}
NS['__builtins__'] = SAFE_BUILTINS


# RENDER_DRAFT=1 marks a failing expression in the output instead of stopping, for proofreading while data is still
# arriving. The normal build (run_all.sh) never sets it, so a missing value always stops the build.
DRAFT = os.environ.get('RENDER_DRAFT') == '1'
ERRORS = []


def render(text, name):
    def sub(m):
        expr = m.group(1).strip()
        try: return str(eval(expr, NS))   # trusted template expression, restricted namespace (see note above)
        except Exception as e:
            msg = f'{name}: cannot evaluate {{{{ {expr} }}}}: {type(e).__name__}: {e}'
            if not DRAFT: raise SystemExit(msg)
            ERRORS.append(msg)
            return f'[[BUILD ERROR: {expr}]]'
    return re.sub(r'\{\{(.+?)\}\}', sub, text)


if __name__ == '__main__':
    # Render every template before writing any file, so a failed render leaves the previous 01, 02, 03, 05 and README
    # untouched. run_all.sh calls this once with --check (render only, write nothing) before 04 is written, so that a
    # template that cannot fill stops the build while all six documents still agree with each other.
    outs = []
    for tp in sorted(glob.glob(REPO + 'templates/*.tmpl.md')):
        outs.append((REPO + os.path.basename(tp).replace('.tmpl.md', '.md'), render(open(tp).read(), os.path.basename(tp))))
    if '--check' in sys.argv:
        print(f'checked {len(outs)} templates: every expression fills'); sys.exit(0)
    for out, text in outs:
        open(out, 'w').write(text)
        print('rendered', os.path.basename(out))
    if not outs: print('no templates found')
    for e in ERRORS: print('DRAFT ERROR', e)
