"""Grade every excluded candidate in the reference window, in one place.
direct     Billboard lists it on Hot R&B Songs or an R&B-only component chart (the study's working rule: R&B means not rap)
yearend    deduced from year-end lists read directly
indirect   anything weaker, including a listing on a country, rock or dance chart with no rap-chart row found
unresolved the candidate was never settled
Written to data/raw/exclusion_grades.json; render_reference.py imports GRADE and ev_best from here, and render_docs.py
reads the JSON, so the two renderers cannot disagree."""
import json, re, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrections as C
from paths import WORK
rows = json.load(open(WORK + 'final_rows.json'))
status = {r['cid']: r for r in json.load(open(WORK + 'classification_status.json'))}
col = json.load(open(WORK + 'collected.json'))
cands = json.load(open(WORK + 'to_verify.json'))


def ev_best(cid):
    ov = C.CLASSIFICATION_OVERRIDES.get(cid)
    if ov: return dict(evidence_type=ov['evidence_type'], confidence=ov['confidence'], evidence_summary=ov['summary'], source_urls=[ov['source_url']] if ov.get('source_url') else [])
    ev = col['classify'].get(str(cid), [])
    ev = sorted(ev, key=lambda e: ({'high': 3, 'medium': 2, 'low': 1}.get(e['confidence'], 0), e['evidence_type'] != 'model_knowledge_only'))
    return ev[-1] if ev else None


def nonrap_grade(o):
    """direct = Billboard lists it on Hot R&B Songs or an R&B-only component chart (this study's working rule: a song filed
    as R&B is not rap); yearend = deduced from year-end lists; indirect = anything else. A listing on a country, rock,
    dance, Latin or Afrobeats chart is NOT direct evidence: such charts can overlap with Hot Rap Songs ("All The Way" is on
    a year-end rap list and on a country chart)."""
    st = status[o['cid']]; b = ev_best(o['cid']) or {}
    txt = (b.get('evidence_summary') or '') + ' ' + st.get('basis', '') + ' ' + st.get('earlier_basis', '')
    if o['cid'] in C.NONRAP_GRADE: return C.NONRAP_GRADE[o['cid']]
    if o['cid'] in C.GENRE_INFERENCE_EXCLUSIONS: return 'indirect'
    if o['cid'] in C.YEAREND_ABSENCE_EXCLUSIONS: return 'yearend'
    rb_only = re.search(r'Hot R&B Songs|R&B Streaming Songs|R&B Digital|Adult R&B', txt)
    if rb_only and b.get('confidence') in ('high', 'medium') and not txt.lstrip().lower().startswith('inferred'): return 'direct'
    if st.get('ye_rbhh') or st.get('ye_hot100'): return 'yearend'
    return 'indirect'


final_ids = {r['cid'] for r in rows}
cut_date = rows[-1]['first_top10']
in_window = [o for o in cands if o['first_top10'] >= cut_date]
excl = [o for o in in_window if o['cid'] not in final_ids and status[o['cid']]['status'] != 'rap']
GRADE = {o['cid']: ('unresolved' if status[o['cid']]['status'] == 'unverified' else nonrap_grade(o)) for o in excl}

if __name__ == '__main__':
    json.dump({str(k): v for k, v in GRADE.items()}, open(WORK + 'exclusion_grades.json', 'w'), indent=0)
    print('exclusion grades:', dict(collections.Counter(GRADE.values())))
