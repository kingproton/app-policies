"""Parse Wikipedia discography tables: per song, the peak in the Billboard Hot 100, Hot R&B/Hip-Hop Songs and
Hot Rap Songs columns. Column identity comes from the header cell's wikilink target, never from position."""
import re, json, sys, os, glob, unicodedata

def strip_refs(s):
    s = re.sub(r'<ref[^>]*/>', '', s)
    s = re.sub(r'<ref[^>]*>.*?</ref>', '', s, flags=re.S)
    # drop templates such as {{efn|...}} (nested)
    for _ in range(6):
        s2 = re.sub(r'\{\{[^{}]*\}\}', '', s)
        if s2 == s: break
        s = s2
    return s

def split_cells(line):
    """Split a wikitable data line on || outside links/templates."""
    out, depth, cur, i = [], 0, '', 0
    while i < len(line):
        two = line[i:i + 2]
        if two in ('[[', '{{'): depth += 1; cur += two; i += 2; continue
        if two in (']]', '}}'): depth = max(0, depth - 1); cur += two; i += 2; continue
        if two == '||' and depth == 0: out.append(cur); cur = ''; i += 2; continue
        cur += line[i]; i += 1
    out.append(cur); return out

def cell_text(c):
    """Drop a leading attribute block (rowspan=..|) and references."""
    c = strip_refs(c)
    m = re.match(r'\s*((?:[a-zA-Z-]+\s*=\s*"[^"]*"\s*)+)\|(.*)$', c, flags=re.S)
    if m: c = m.group(2)
    return c.strip()

def nz(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '', s)

def title_of(cell):
    c = strip_refs_keep_links(cell)
    m = re.search(r'"(.+?)"', c)
    t = m.group(1) if m else c
    t = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', t)
    return re.sub(r"'{2,}", '', t).strip()

def strip_refs_keep_links(s):
    s = re.sub(r'<ref[^>]*/>', '', s); s = re.sub(r'<ref[^>]*>.*?</ref>', '', s, flags=re.S)
    return re.sub(r'\{\{small\|.*', '', s, flags=re.S)

COLS = {'Billboard Hot 100': 'us', 'Hot R&B/Hip-Hop Songs': 'rbhh', 'Hot Rap Songs': 'rap', 'Hot R&B Songs': 'rnb',
        'Rhythmic (chart)': 'rhythmic', 'Rhythmic Airplay': 'rhythmic', 'Hot Rock & Alternative Songs': 'rock'}

def parse(wikitext):
    rows = []
    for tm in re.finditer(r'\{\|.*?\n\|\}', wikitext, flags=re.S):
        tab = tm.group(0)
        blocks = re.split(r'\n\|-[^\n]*', tab)
        # header: the peak-position columns in order (cells with scope="col" that carry a chart link, in the 2nd header row)
        peaks = None
        for b in blocks[:4]:
            cells = [l for l in b.split('\n') if l.startswith('!') and 'scope="row"' not in l and 'rowspan' not in l and 'colspan' not in l and '[[' in l]
            if len(cells) >= 2 and any('Billboard Hot 100' in c for c in cells):
                peaks = []
                for c in cells:
                    m = re.search(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', c)
                    peaks.append(COLS.get(m.group(1).strip(), m.group(1).strip()) if m else '?')
                break
        if not peaks or 'us' not in peaks: continue
        for b in blocks:
            lines = b.strip('\n').split('\n')
            head = [l for l in lines if l.startswith('!') and 'scope="row"' in l]
            if not head: continue
            title = title_of(head[0].split('|', 1)[1] if '|' in head[0] else head[0])
            data = []
            for l in lines:
                if l.startswith('|') and not l.startswith('|}') and not l.startswith('|+'):
                    data += [cell_text(c) for c in split_cells(l[1:])]
            if data and re.fullmatch(r'\d{4}', data[0]): data = data[1:]
            vals = data[:len(peaks)]
            if len(vals) < len(peaks): vals += [''] * (len(peaks) - len(vals))
            rec = dict(title=title, key=nz(title), feat=re.sub(r'\s+', ' ', strip_refs(re.sub(r'^.*?"\s*', '', head[0].split('|', 1)[-1], count=1)))[:120])
            for name, v in zip(peaks, vals):
                if name in ('us', 'rbhh', 'rap', 'rnb', 'rock', 'rhythmic'):
                    v2 = v.replace('&mdash;', '—').strip()
                    rec[name] = int(v2) if re.fullmatch(r'\d+', v2) else ('—' if v2 in ('—', '-', '–') else v2[:20])
            rec['has_rap_col'] = 'rap' in peaks; rec['cols'] = [p for p in peaks if p in ('us', 'rbhh', 'rap', 'rnb', 'rock', 'rhythmic')]
            rows.append(rec)
    return rows

if __name__ == '__main__':
    out = {}
    for p in sorted(glob.glob(sys.argv[1] + '*.wiki')):
        r = parse(open(p, encoding='utf-8').read())
        out[os.path.basename(p)[:-5]] = r
        print(os.path.basename(p), len(r), 'rows;', sum(1 for x in r if x.get('has_rap_col')), 'with a Hot Rap Songs column')
    json.dump(out, open(sys.argv[2], 'w'), indent=0, ensure_ascii=False)
