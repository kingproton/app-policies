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
    rec = dict(status='agree' if not why else ('adjudicated' if cid in rulings else 'disputed_no_ruling'), why=why, reviewer=rv)
    if why and cid in rulings:
        ru = dict(rulings[cid]); ru['reason'] = clip_quotes(ru.get('reason')); rec['ruling'] = ru
    out[cid] = rec
json.dump(out, open(out_path, 'w'), indent=0, ensure_ascii=False)
import collections
print(len(out), 'tracks |', dict(collections.Counter(v['status'] for v in out.values())), '| rulings', dict(collections.Counter(v['ruling']['resolution'] for v in out.values() if v.get('ruling'))))
print('disagreement kinds:', dict(collections.Counter(w for v in out.values() for w in v['why'])))
