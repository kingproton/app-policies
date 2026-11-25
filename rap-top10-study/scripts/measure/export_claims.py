"""Build page_claims.json from the claims-check workflow journals.
Per track: each claim's verdict after the skeptic's ruling, and the new facts the skeptic upheld. Every quote is also
checked mechanically against the saved page text. Quotes are trimmed (Songfacts to 12 words, Wikipedia to 30) and any
quoted span of more than five words inside them is cut, so no lyric lines are carried.
Usage: export_claims.py <out.json> <journal.jsonl> [...]"""
import json, os, re, sys, collections, unicodedata
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpaths import SP
out_path = sys.argv[1]; journals = sys.argv[2:]
CORPUS = SP + 'net/corpus/'


def norm(s):
    s = unicodedata.normalize('NFKC', s or '').lower()
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-')
    s = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', s)
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


_cache = {}
def page(cid, src):
    k = (cid, src)
    if k not in _cache:
        p = CORPUS + f'{cid}_{src}.txt'
        _cache[k] = norm(open(p, encoding='utf-8').read()) if os.path.exists(p) else ''
    return _cache[k]


def quote_found(cid, src, quote):
    q = norm(quote)
    if len(q) < 8: return False                    # short infobox lines such as "length = 3:57" are legitimate quotes
    srcs = ['wikipedia', 'songfacts'] if src in ('both', 'none', None) else [src]
    for s in srcs:
        t = page(cid, s)
        if (' ' + q + ' ') in (' ' + t + ' '): return True
        # allow an elided middle ("..." or a cut): first and last eight words both present, in order
        w = q.split()
        if len(w) >= 14:
            a, b = ' '.join(w[:7]), ' '.join(w[-7:])
            i = t.find(a)
            if i >= 0 and t.find(b, i) >= 0: return True
    return False


def clip(quote, src):
    def cut(m):
        words = m.group(2).split()
        return m.group(1) + (' '.join(words[:5]) + ' …' if len(words) > 5 else m.group(2)) + m.group(3)
    q = re.sub(r'(["“])([^"”]{1,400})(["”])', cut, quote or '')
    w = q.split(); lim = 12 if src == 'songfacts' else 30
    return ' '.join(w[:lim]) + (' …' if len(w) > lim else '')


checks, skeptics = {}, {}
for jp in journals:
    rows = [json.loads(l) for l in open(jp) if l.strip()]
    lab = {r['key']: r['label'] for r in rows if 'label' in r}
    for r in rows:
        if 'result' not in r or not r['result']: continue
        L = lab.get(r['key'], '')
        if L.startswith('check:'):
            for t in r['result'].get('tracks', []): checks[str(t['cid'])] = t
        elif L.startswith('skeptic:'):
            for x in r['result'].get('rulings', []): skeptics[(str(x['cid']), x['kind'], x['ref'])] = x
out = {}; tally = collections.Counter()
for cid, t in checks.items():
    vs = []
    for v in t.get('verdicts', []):
        sk = skeptics.get((cid, 'verdict', v['id']))
        final = v['verdict']; found = None
        if v['verdict'] != 'not_addressed':
            found = quote_found(cid, v['source'], v['quote'])
            if sk is None: final = v['verdict'] + '_unreviewed'
            elif not sk['upheld']: final = sk['corrected_verdict'] if sk['corrected_verdict'] not in ('no_change', 'drop_new_fact') else 'not_addressed'
            if final in ('supported', 'partly_supported', 'contradicted') and not found: final = final + '_quote_not_found'
        tally[final] += 1
        vs.append(dict(id=v['id'], first_verdict=v['verdict'], final=final, source=v['source'], quote=clip(v['quote'], v['source']), quote_in_page=found,
                       note=clip(v['note'], 'wikipedia'), skeptic_upheld=None if sk is None else sk['upheld'], skeptic_reason=None if sk is None else clip(sk['reason'], 'wikipedia')))
    nf = []
    for k, f in enumerate(t.get('new_facts', [])):
        sk = skeptics.get((cid, 'new_fact', f'new_{k + 1}')); found = quote_found(cid, f['source'], f['quote'])
        keep = bool(sk and sk['upheld'] and found)
        tally['new_fact_kept' if keep else 'new_fact_dropped'] += 1
        if keep: nf.append(dict(category=f['category'], statement=clip(f['statement'], 'wikipedia'), source=f['source'], quote=clip(f['quote'], f['source'])))
    out[cid] = dict(verdicts=vs, new_facts=nf)
json.dump(out, open(out_path, 'w'), indent=0, ensure_ascii=False)
man = json.load(open(CORPUS + 'manifest.json'))
summary = dict(tracks=len(out), wikipedia_pages=sum(1 for m in man if m['wikipedia']), songfacts_pages=sum(1 for m in man if m['songfacts']), claims=sum(len(t['verdicts']) for t in out.values()),
               final=dict(tally), skeptic_rulings=len(skeptics), skeptic_upheld=sum(1 for x in skeptics.values() if x['upheld']),
               new_facts_by_category=dict(collections.Counter(f['category'] for t in out.values() for f in t['new_facts'])))
json.dump(summary, open(out_path.replace('.json', '_summary.json'), 'w'), indent=1)
print(len(out), 'tracks |', dict(tally))
print('skeptic rulings:', len(skeptics), '| upheld', sum(1 for x in skeptics.values() if x['upheld']), '| quote found by skeptic', sum(1 for x in skeptics.values() if x['quote_found_in_file']))
