"""Parse Wikipedia's yearly 'top-ten singles' lists and year-end genre lists (wikitext) into JSON."""
import re, json, os, sys, unicodedata, glob, urllib.parse
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpaths import SP
W = SP + 'net/wikipedia/'
def strip_markup(s):
    s = re.sub(r'<ref[^>]*/>', '', s); s = re.sub(r'<ref[^>]*>.*?</ref>', '', s, flags=re.S)
    s = re.sub(r'\{\{ref label[^}]*\}\}', '', s); s = re.sub(r'\{\{(?:up-arrow|dagger|double-dagger|small)[^}]*\}\}', '', s)
    s = re.sub(r'<small>.*?</small>', '', s); s = re.sub(r"'{2,}", '', s)
    return s
def links(s): return re.findall(r'\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]', s)
def plain(s):
    s = strip_markup(s)
    s = re.sub(r'\[\[([^\]|]+)\|([^\]]*)\]\]', r'\2', s); s = re.sub(r'\[\[([^\]]+)\]\]', r'\1', s)
    s = re.sub(r'\{\{[^}]*\}\}', '', s); s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', s).strip()
def cell_content(c):
    c = c.strip()
    # drop leading attributes "style=...|" but not pipes inside links/templates
    m = re.match(r'^((?:[a-zA-Z\-]+\s*=\s*(?:"[^"]*"|[^|\s]+)\s*)+)\|(?!\|)(.*)$', c, re.S)
    return m.group(2).strip() if m else c
def rows_of(text):
    for tbl in re.findall(r'\{\|.*?\n\|\}', text, re.S):
        for row in re.split(r'\n\|-[^\n]*', tbl)[1:]:
            cells = []
            for line in row.split('\n'):
                if line.startswith('|') and not line.startswith('|}'):
                    for part in re.split(r'\s*\|\|\s*', line[1:]): cells.append(part)
                elif line.startswith('!'): cells.append('!HEADER')
                elif cells: cells[-1] += '\n' + line
            yield cells
def topten(year):
    text = open(W + f'List_of_Billboard_Hot_100_top-ten_singles_in_{year}.wiki').read()
    out = []; cur = None
    for cells in rows_of(text):
        if not cells or '!HEADER' in cells[0]: continue
        cc = [cell_content(c) for c in cells]
        idx = 0
        m = re.search(r'\{\{sort\|(\d{8})\|', cc[0])
        if m: cur = f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:]}"; idx = 1
        if idx >= len(cc) or '"' not in cc[idx] and '[[' not in cc[idx]: continue
        single = cc[idx]; lk = links(strip_markup(single))
        tm = re.search(r'"(.*)"', strip_markup(single), re.S)
        title = plain(tm.group(1) if tm else single)
        artist = plain(cc[idx + 1]) if idx + 1 < len(cc) else ''
        nums = [int(plain(x)) for x in cc[idx + 2:] if re.fullmatch(r'\d+', plain(x))]
        out.append(dict(entry=cur, title=title, article=(lk[0][0].strip() if lk else None), artist=artist,
                        peak=nums[0] if nums else None, weeks_top10=nums[-1] if len(nums) >= 2 else None, list_year=year))
    return out
def yearend(prefix, year):
    fn = W + urllib.parse.quote(f'{prefix}_of_{year}'.replace(' ', '_'), safe='') + '.wiki'
    if not os.path.exists(fn): return []
    out = []; artist = ''
    for cells in rows_of(open(fn).read()):
        if not cells or '!HEADER' in cells[0]: continue
        cc = [cell_content(c) for c in cells]
        if not re.fullmatch(r'\d+', plain(cc[0])) or len(cc) < 2: continue
        lk = links(strip_markup(cc[1])); tm = re.search(r'"(.*)"', strip_markup(cc[1]), re.S)
        if len(cc) >= 3: artist = plain(cc[2])
        out.append(dict(rank=int(plain(cc[0])), title=plain(tm.group(1) if tm else cc[1]), article=(lk[0][0].strip() if lk else None), artist=artist, year=year))
    return out
if __name__ == '__main__':
    res = dict(topten=[], yearend_rap=[], yearend_rbhh=[])
    for y in range(2021, 2027):
        t = topten(y); res['topten'] += t
        r = yearend('Billboard Year-End Hot Rap Songs', y); res['yearend_rap'] += r
        h = yearend('Billboard Year-End Hot R&B/Hip-Hop Songs', y); res['yearend_rbhh'] += h
        print(y, 'top-ten rows', len(t), '| YE rap', len(r), '| YE R&B/HH', len(h))
    json.dump(res, open(SP + 'net/wiki_lists.json', 'w'), indent=1)
    print(res['topten'][5]); print(res['yearend_rap'][0], res['yearend_rap'][-1])
