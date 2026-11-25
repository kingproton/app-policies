"""Facts computed from data/measured/ that more than one renderer states, kept in one place so the documents cannot drift."""
import json, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import REPO
MD = REPO + 'data/measured/'


def bc_weeks():
    """Billboard Canada chart pages against the weekly mirror."""
    cv = json.load(open(MD + 'chart_verification.json'))['weeks']
    comp = [w for w in cv if w['status'] == 'compared']
    rows_ok = lambda w: w['full_rows_matching'] == w['full_rows_compared']
    all100 = [w['date'] for w in comp if w['titles_matching'] == w['titles_compared'] and rows_ok(w)]
    one_off = [w['date'] for w in comp if w['titles_matching'] == w['titles_compared'] - 1 and rows_ok(w)]
    other = [w['date'] for w in comp if w['date'] not in all100 and w['date'] not in one_off]
    first = min(w['date'] for w in comp)
    diffs = {w['date']: w.get('title_differences') or [] for w in comp if w['date'] in one_off}
    return dict(hosted=len(comp), first=first, last=max(w['date'] for w in comp), all100=len(all100), one_title_differs=one_off, other=other, differences=diffs,
                matching=len(all100) + len(one_off), missing_later=[w['date'] for w in cv if w['status'] != 'compared' and w['date'] >= first])


def _nz(s): return re.sub(r'[^a-z0-9]+', '', (s or '').lower().replace('&', 'and'))


def yearend_inversions():
    """Per year: how many times the year-end R&B/Hip-Hop rank falls from one title to the next when titles are taken in
    year-end Hot Rap Songs order (titles on both lists only). Zero would mean the two lists rank rap titles identically."""
    wl = json.load(open(MD + 'wikipedia_lists.json'))
    out = {}
    for y in sorted({e['year'] for e in wl['yearend_rap']}):
        rb = {_nz(e['title']): e['rank'] for e in wl['yearend_rbhh'] if e['year'] == y}
        seq = [rb[_nz(e['title'])] for e in sorted((e for e in wl['yearend_rap'] if e['year'] == y), key=lambda e: e['rank']) if _nz(e['title']) in rb]
        out[y] = sum(1 for a, b in zip(seq, seq[1:]) if b < a)
    return out


def dash_conflicts():
    """Songs that show a dash in the rap column of one discography table and a numbered rap peak in another."""
    return json.load(open(MD + 'discography_dash_conflicts.json'))


def page_name(p): return p.replace('%2C', ',').replace('_singles_discography', '').replace('_production_discography', ' (production)').replace('_discography', '').replace('_', ' ')
