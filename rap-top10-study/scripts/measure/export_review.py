"""Build lyric_structure_review.json from the review workflow journals: per track, the independent reading of the
time-synced lyric record, whether it agrees with the repetition detector, and the ruling where they disagreed.
Usage: export_review.py <out.json> <journal.jsonl> [<journal.jsonl> ...]
No lyric text is written: reviewer notes are kept, with any quoted span longer than five words cut."""
import json, os, re, sys
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpaths import SP
out_path = sys.argv[1]; journals = sys.argv[2:]
ALG = json.load(open(SP + 'net/lrc_structure.json'))


def clip_quotes(s):
    def cut(m):
        words = m.group(2).split()
        return m.group(1) + (' '.join(words[:5]) + ' …' if len(words) > 5 else m.group(2)) + m.group(3)
    s = re.sub(r'(["“])([^"”]{1,400})(["”])', cut, s or '')
    return re.sub(r"(')([^']{30,400})(')", cut, s)


# A reader's note sometimes carried an aside from recollection instead of from the file. Nothing recorded may rest on
# recollection, so the aside is cut from the stored note, the record is flagged, and a first-line label that the aside
# could have influenced (who or what the opening voice is) is set to 'unclear'.
MEM = re.compile(r'\bmemory\b|\brecall|\bremember|\bwell-known\b|\bfamous', re.I)
KIND_RESET = {'52', '108', '127'}     # Carnival, United In Grief, Champagne Poetry
def scrub(note):
    note = note or ''
    cut = re.sub(r'\s*\([^()]*(?:memory|recall|remember)[^()]*\)', '', note, flags=re.I)
    # a lyric record cannot show a beat switch: a mention of one comes from outside the file
    cut = re.sub(r';\s*no section returns after the beat switch[^;.]*\.?\s*$', '.', cut, flags=re.I)
    cut = re.sub(r'\s*(?:just )?(?:before|after) the beat switch(?: near [\d.]+ s)?', '', cut, flags=re.I)
    parts = re.split(r'(?<=[;.])\s+', cut)
    kept = [p for p in parts if not MEM.search(p)]
    out = ' '.join(kept).strip()
    out = re.sub(r';$', '.', out)
    return out, out != re.sub(r';$', '.', note.strip())


def disagreements(a, r):
    """Same rule as the workflow script."""
    out = []; a_has = a['first_hook_s'] is not None
    if not r.get('record_ok', True): out.append('reviewer says the record is not usable')
    if a_has != r['has_recurring_hook']: out.append('whether a recurring hook exists')
    if a_has and r['has_recurring_hook'] and r.get('first_hook_s') is not None:
        if abs(round(a['first_hook_s'], 1) - r['first_hook_s']) > 2.5: out.append('first hook time')
        a_first = a['lines_before_first_hook'] is not None and a['lines_before_first_hook'] <= 3
        r_first = r.get('lines_before_first_hook') is not None and r['lines_before_first_hook'] <= 3
        if a_first != r_first: out.append('whether the hook comes within the first three lines')
        if abs(len(a['hook_starts']) - len(r['hook_starts_s'])) >= 2: out.append('how many times the hook occurs')
    if abs(round(a['first_line_s'], 1) - r['first_line_s']) > 1.0: out.append('first line time')
    return out


readers, rulings = {}, {}
for jp in journals:
    rows = [json.loads(l) for l in open(jp) if l.strip()]
    lab = {r['key']: r['label'] for r in rows if 'label' in r}
    for r in rows:
        if 'result' not in r or not r['result']: continue
        L = lab.get(r['key'], '')
        if L.startswith('read:'):
            for t in r['result'].get('tracks', []): readers[str(t['cid'])] = t
        elif L.startswith('adjudicate:'):
            for x in r['result'].get('rulings', []): rulings[str(x['cid'])] = x
out = {}
for cid, rv in readers.items():
    a0 = ALG.get(cid)
    if not a0 or a0.get('status') != 'ok': continue
    a = dict(first_line_s=a0['first_line_s'], first_hook_s=a0['first_hook_s'], lines_before_first_hook=a0['lines_before_first_hook'],
             hook_starts=[s['start'] for s in a0['sections'] if s['label'] == 'HOOK'])
    why = disagreements(a, rv)
    rv = dict(rv); rv['note'] = clip_quotes(rv.get('note'))
    rv['note'], aside = scrub(rv['note'])
    if aside:
        rv['recollection_aside_removed'] = True
        if cid in KIND_RESET: rv['first_line_kind_reader'] = rv.get('first_line_kind'); rv['first_line_kind'] = 'unclear'
    rec = dict(status='agree' if not why else ('adjudicated' if cid in rulings else 'disputed_no_ruling'), why=why, reviewer=rv)
    if why and cid in rulings:
        ru = dict(rulings[cid]); ru['reason'] = clip_quotes(ru.get('reason'))
        ru['reason'], aside2 = scrub(ru['reason'])
        if aside2: ru['recollection_aside_removed'] = True
        rec['ruling'] = ru
    out[cid] = rec
json.dump(out, open(out_path, 'w'), indent=0, ensure_ascii=False)
import collections
print(len(out), 'tracks |', dict(collections.Counter(v['status'] for v in out.values())), '| rulings', dict(collections.Counter(v['ruling']['resolution'] for v in out.values() if v.get('ruling'))))
print('recollection asides removed:', sorted(k for k, v in out.items() if v['reviewer'].get('recollection_aside_removed') or (v.get('ruling') or {}).get('recollection_aside_removed')))
print('disagreement kinds:', dict(collections.Counter(w for v in out.values() for w in v['why'])))
