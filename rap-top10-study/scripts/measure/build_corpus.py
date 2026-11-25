"""Build a per-track reading corpus (Wikipedia article text + Songfacts facts) and a claims file for page-level re-checks.
Everything stays in the working directory."""
import json, re, os, html, urllib.parse, sys
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpaths import SP, IN
OUT = SP + 'net/corpus/'; os.makedirs(OUT, exist_ok=True)
F = json.load(open(IN + 'final_rows.json'))
T = json.load(open(IN + 'tracks_merged.json'))
W = json.load(open(SP + 'net/wiki_articles.json'))
SF = json.load(open(SP + 'net/songfacts_pages.json')) if os.path.exists(SP + 'net/songfacts_pages.json') else {}
wiki_by = {(w['date'], w['rank']): w for w in W}
def wiki_text(article):
    fn = SP + 'net/wikipedia/articles/' + urllib.parse.quote(article.replace(' ', '_'), safe="_(),'!$*") + '.wiki'
    cands = [fn, SP + 'net/wikipedia/articles/' + urllib.parse.quote(article.replace(' ', '_')) + '.wiki', SP + 'net/wikipedia/articles/' + article.replace(' ', '_') + '.wiki']
    for c in cands:
        if os.path.exists(c):
            s = open(c, encoding='utf-8').read(); break
    else:
        return None
    s = re.sub(r'<ref[^>]*/>', '', s); s = re.sub(r'<ref[^>]*>.*?</ref>', '', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    m = re.search(r'\n==\s*(Charts|Weekly charts|Certifications|Release history|References|Notes|External links)\s*==', s)
    if m: s = s[:m.start()]
    s = re.sub(r'\[\[(?:File|Image):[^\]]*\]\]', '', s)
    s = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', s)
    s = re.sub(r"'{2,}", '', s)
    return s.strip()
def songfacts_text(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    i = s.find('<ul class="songfacts-results"'); j = s.find('songfacts-more', i)
    if i < 0: return None
    block = s[i:j if j > 0 else i + 60000]
    items = re.findall(r'<div class="inner">(.*?)</div>\s*</li>', block, flags=re.S) or re.findall(r'<li[^>]*>(.*?)</li>', block, flags=re.S)
    out = []
    for it in items:
        t = html.unescape(re.sub(r'<[^>]+>', ' ', it)); t = re.sub(r'\s+', ' ', t).strip()
        if len(t) > 30: out.append('- ' + t)
    return '\n'.join(out) if out else None
man = []
for r in F:
    cid = r['cid']; t = T.get(str(cid)) or {}
    w = wiki_by.get((r['first_top10'], r['rank']))
    wt = wiki_text(w['article']) if w and w.get('article') else None
    wpath = spath = None
    if wt:
        wpath = OUT + f'{cid}_wikipedia.txt'
        open(wpath, 'w', encoding='utf-8').write(f"SOURCE: English Wikipedia article \"{w['article']}\" (https://en.wikipedia.org/wiki/{w['article'].replace(' ', '_')}), wikitext with references, chart tables and later sections removed.\n\n" + wt)
    sf = (SF.get(str(cid)) or {}).get('hit')
    if sf:
        st = songfacts_text(sf['path'])
        if st:
            spath = OUT + f'{cid}_songfacts.txt'
            open(spath, 'w', encoding='utf-8').write(f"SOURCE: Songfacts page \"{sf['page_title']}\" ({sf['url']}), the list of facts only.\n\n" + st)
    claims = []
    def add(i, text, basis=None):
        if text: claims.append(dict(id=i, claim=text, current_basis=basis))
    if t.get('opening_element') not in (None, 'unknown'): add('opening', f"The first thing heard on the recording is: {t['opening_element']}", t.get('opening_basis'))
    if t.get('hook_first') not in (None, 'unknown'): add('hook_first', f"The hook or chorus comes before the first verse: {t['hook_first']}", t.get('hook_first_basis'))
    if t.get('beat_switch') not in (None, 'unknown'): add('beat_switch', f"The track has a beat switch: {t['beat_switch']}. Detail on file: {t.get('beat_switch_detail') or 'none'}", t.get('beat_switch_basis'))
    if t.get('producer_tag') not in (None, 'unknown'): add('producer_tag', f"A producer tag is heard: {t['producer_tag']}. Detail on file: {t.get('producer_tag_detail') or 'none'}")
    for k, s in enumerate(t.get('samples') or []):
        add(f'borrow_{k+1}', f"Borrows from {s.get('work')} as {s.get('borrow_type')}; credited: {s.get('credited')}. How used (on file): {s.get('how_used')}", s.get('status'))
    if t.get('producers'): add('producers', 'Producers: ' + ', '.join(t['producers']))
    if t.get('features'): add('features', 'Guest or second vocalists on file: ' + json.dumps(t['features'], ensure_ascii=False)[:600])
    if t.get('runtime_mmss'): add('runtime', f"Runtime of the studied version: {t['runtime_mmss']}", t.get('runtime_status'))
    if t.get('key'): add('key', f"Key on file: {t['key']}")
    if t.get('tempo_listed'): add('tempo', 'Tempo listings on file (BPM): ' + ', '.join(str(x.get('bpm')) for x in t['tempo_listed']))
    if t.get('hook_description'): add('hook_description', f"Hook description on file: {t['hook_description']}", t.get('hook_status'))
    for k, s in enumerate(t.get('structure_notes') or []): add(f'structure_note_{k+1}', s.get('claim'))
    for k, s in enumerate(t.get('delivery') or []): add(f'delivery_{k+1}', f"{s.get('aspect')}: {s.get('observation')}", s.get('basis'))
    for k, s in enumerate(t.get('returns') or []): add(f'return_{k+1}', json.dumps(s, ensure_ascii=False)[:500])
    cpath = OUT + f'{cid}_claims.json'
    json.dump(dict(cid=cid, n=r['n'], title=r['title'], artists=r['artists'], version_used=t.get('version_used'), claims=claims), open(cpath, 'w'), indent=1, ensure_ascii=False)
    man.append(dict(cid=cid, n=r['n'], title=r['title'], wikipedia=bool(wpath), songfacts=bool(spath), n_claims=len(claims), wiki_chars=len(wt or ''), sf_chars=os.path.getsize(spath) if spath else 0))
json.dump(man, open(OUT + 'manifest.json', 'w'), indent=0)
print(len(man), 'tracks | wikipedia', sum(m['wikipedia'] for m in man), '| songfacts', sum(m['songfacts'] for m in man), '| claims', sum(m['n_claims'] for m in man),
      '| wiki chars', sum(m['wiki_chars'] for m in man), '| sf chars', sum(m['sf_chars'] for m in man))
print('no wikipedia text:', [m['title'] for m in man if not m['wikipedia']])
