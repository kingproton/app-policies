"""Render 04-reference-list.md from final_rows.json, tracks_merged.json, classification status, chart checks and measured data."""
import json, re, os, csv, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrections as C
import shared_facts as SF
from exclusion_grades import GRADE, ev_best
from paths import WORK, REPO
rows = json.load(open(WORK + 'final_rows.json'))
T = {int(k): v for k, v in json.load(open(WORK + 'tracks_merged.json')).items()}
status = {r['cid']: r for r in json.load(open(WORK + 'classification_status.json'))}
col = json.load(open(WORK + 'collected.json'))
S = json.load(open(WORK + 'stats.json'))
cands = json.load(open(WORK + 'to_verify.json'))
CC = {int(k): v for k, v in json.load(open(WORK + 'chart_check.json')).items()} if os.path.exists(WORK + 'chart_check.json') else {}
CV = json.load(open(REPO + 'data/measured/chart_verification.json'))['weeks']
WL = json.load(open(REPO + 'data/measured/wikipedia_lists.json'))
SITE = {'hypebeast.com': 'Hypebeast', 'yahoo.com': 'Yahoo (Billboard syndication)', 'en.wikipedia.org': 'Wikipedia', 'uproxx.com': 'Uproxx',
        'aceshowbiz.com': 'AceShowbiz', 'radiox.cms.socastsrm.com': 'radio-station site', 'stereogum.com': 'Stereogum', 'npr.org': 'NPR',
        'thesource.com': 'The Source', 'rated-rnb.com': 'Rated R&B', 'musictimes.com': 'Music Times', 'hotnewhiphop.com': 'HotNewHipHop'}
EVLAB = {'billboard_chart_page': 'Billboard chart page', 'billboard_article': 'Billboard report', 'wikipedia_chart_table': 'Wikipedia table',
         'other_press': 'press citing Billboard'}


def esc(s): return (s or '').replace('|', '/').replace('\n', ' ')


def short(s, n=70):
    s = esc(s)
    if len(s) <= n: return s
    cut = s[:n].rsplit(' ', 1)[0]
    return cut.rstrip(',;:(') + '…'


def domain(u): return re.sub(r'^https?://(www\.)?', '', u).split('/')[0]
def mmss(s):
    if s is None: return '?'
    s = int(round(s)); return f"{s // 60}:{s % 60:02d}"
def plural(n, one, many): return one if n == 1 else many


def table_link(st):
    """Markdown link for a table-tier basis string."""
    b = st['basis']
    if b.startswith('Year-End'):
        yr = re.search(r'(\d{4})', b).group(1); rk = re.search(r'#(\d+)', b).group(1)
        return f"[year-end Hot Rap Songs {yr}, No. {rk}](https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_Rap_Songs_of_{yr})"
    m = re.match(r'Hot Rap Songs peak No\. (\d+) \(Wikipedia table: (.*)\)', b)
    if m: return f"[Hot Rap Songs peak No. {m.group(1)}](https://en.wikipedia.org/wiki/{m.group(2).replace(' ', '_')}) ({m.group(2)} table)"
    return None


def summary_link(cid):
    b = ev_best(cid)
    if not (b and b.get('source_urls')): return 'no source on file'
    u = b['source_urls'][0]; d = domain(u)
    if 'billboard.com' in d: lab = 'Billboard chart page' if ('/charts/' in u or '/chart-history/' in u) else 'Billboard report'
    else: lab = SITE.get(d, d) + (' (reporting Billboard)' if b['evidence_type'] in ('billboard_article', 'billboard_chart_page', 'other_press') else '')
    return f"[{lab}]({u}) via search summary"


def genre_evidence(cid):
    st = status[cid]
    return table_link(st) if st.get('tier') == 'table' and table_link(st) else summary_link(cid)


# ---- year-end deduction helpers (lists read directly on Wikipedia)
def nz(s): return re.sub(r'[^a-z0-9]+', '', (s or '').lower().replace('&', 'and'))
ye_rap = collections.defaultdict(dict); ye_rb = collections.defaultdict(dict)
for e in WL['yearend_rap']: ye_rap[e['year']][nz(e['title'])] = e['rank']
for e in WL['yearend_rbhh']: ye_rb[e['year']][nz(e['title'])] = e['rank']
WORST_RB = {y: max([ye_rb[y][t] for t in ye_rap[y] if t in ye_rb[y]] or [0]) for y in ye_rap}   # worst R&B/Hip-Hop year-end rank held by a rap-list title


def table_note(o):
    """What the tables read directly add for an excluded song."""
    st = status[o['cid']]; bits = []
    for yr, rk in st.get('ye_rbhh') or []:
        w = WORST_RB.get(yr)
        bits.append(f"{yr} year-end Hot R&B/Hip-Hop Songs No. {rk}, not on the {yr} year-end Hot Rap Songs list" + (f" (titles on the rap list rank as low as No. {w} on that R&B/Hip-Hop list, so a rap title at No. {rk} would be on the rap list)" if w and rk < w else ''))
    if not st.get('ye_rbhh'):
        for yr, rk in st.get('ye_hot100') or []: bits.append(f"{yr} year-end Hot 100 No. {rk}, on neither the rap nor the R&B/Hip-Hop year-end list")
    if st.get('discog_rap_dash_pages'): bits.append('dash in the Hot Rap Songs column of the ' + ', '.join(p.replace('_', ' ').replace('%2C', ',') for p in st['discog_rap_dash_pages']) + ' table (a dash can be an unfilled cell; it is not evidence on its own)')
    other = [c for c in st.get('wiki_genre_charts') or [] if c != 'R&B/Hip-Hop']
    if other: bits.append("Wikipedia's chart table lists it on " + ' and '.join({'Rock & Alt': 'Hot Rock & Alternative Songs', 'Country': 'Hot Country Songs', 'Dance/Pop': 'Hot Dance/Pop Songs', 'Dance/Electronic': 'Hot Dance/Electronic Songs', 'Afrobeats': 'U.S. Afrobeats Songs', 'Latin': 'Hot Latin Songs', 'Christian': 'Hot Christian Songs'}.get(c, c) for c in other))
    return '; '.join(bits)


out = []
final_ids = {r['cid'] for r in rows}
cut_date = rows[-1]['first_top10']
in_window = [o for o in cands if o['first_top10'] >= cut_date]
summ = [r for r in rows if status[r['cid']].get('tier') != 'table']
excl = [o for o in in_window if o['cid'] not in final_ids and status[o['cid']]['status'] != 'rap']
grade = GRADE                                    # computed once in exclusion_grades.py
soft = [o for o in excl if grade[o['cid']] in ('indirect', 'unresolved')]
yend = [o for o in excl if grade[o['cid']] == 'yearend']

# ---- chart-check counts
comp = [w for w in CV if w['status'] == 'compared']
full = sum(1 for w in comp if w['titles_matching'] >= w['titles_compared'] - 1 and w['full_rows_matching'] == w['full_rows_compared'])
bc_match = sum(1 for v in CC.values() if v['billboard_canada'] == 'match'); bc_host = sum(1 for v in CC.values() if v['billboard_canada'] in ('match',) or v['billboard_canada'].startswith('differs'))
w_match = sum(1 for v in CC.values() if v['wikipedia_entry_date'] == 'match')

BCW = SF.bc_weeks()
_in_missing = [o['title'] for o in cands if o['first_top10'] in BCW['missing_later']]
assert not _in_missing, f'a candidate first reached the top 10 in a week Billboard Canada does not host: {_in_missing}'
_chk_missing = ''
_spell = '; '.join(f"{d}: #{x[0][0]} \"{x[0][1]}\" against \"{x[0][2]}\"" for d, x in BCW['differences'].items() if x)
out.append('# 4 — Full reference list (100 songs)\n')
out.append(f"**Reference window:** first Hot 100 top-10 weeks from the chart dated **{S['span'].split(' to ')[1]}** back to **{S['span'].split(' to ')[0]}**. That is the 100 most recent distinct rap songs, counting back from the chart dated 2026-11-21 (research cutoff 2026-11-22).\n")
out.append("**Ordering rule:** by the chart week each song *first* reached positions 1–10, newest first. Ties within a week are sorted by position that week. Each song is counted once. Billboard's combined credits and remixes are followed, so Billboard's mid-run re-credit of \"Carnival\" from Kanye West to Ye counts as one song.\n")
out.append("**Genre rule:** rap = Billboard placed the song on Hot Rap Songs or on a rap-only component chart (Rap Streaming Songs, Rap Airplay), or Billboard reporting says so. This study treats a listing on Hot R&B Songs, or on an R&B-only component chart, as an R&B classification and therefore not rap; that is a working rule, not a Billboard statement read in this study. R&B-classified songs by rappers are therefore excluded and logged in 4d. A listing on another genre chart (country, rock, dance, Christian) does not rule out rap: \"All The Way\" (#12) is on the 2025 year-end Hot Rap Songs list and on a country chart. (Hot Rap Songs is not a strict subset of Hot R&B/Hip-Hop Songs: a few pop-leaning rap titles appear on the year-end rap list but not on the year-end R&B/Hip-Hop list.)\n")
out.append(f"**Rank and date sources.** Dates and ranks come from every weekly Hot 100 chart in the public `mhollingshead/billboard-hot-100` mirror of billboard.com. Two sources read directly on 2026-11-25 check them:\n"
           f"- **Billboard Canada's licensed Hot 100 pages** (`ca.billboard.com/charts/hot-100/<date>`, the site you named for the starting issue). It hosts {BCW['hosted']} chart weeks from {BCW['first']} to {BCW['last']}. In {BCW['all100']} of them every title matches the mirror at every position, and in {len(BCW['one_title_differs'])} more one title is spelled differently ({_spell}); in all {BCW['matching']} the 25 rows per page that carry last week, peak and weeks on chart match too. The remaining page, labelled {BCW['other'][0]}, shows the previous week's chart; the following week's \"last week\" column agrees with the mirror. {len(BCW['missing_later'])} later weeks are missing from that site ({', '.join(BCW['missing_later'])}); for those the chart comes from the mirror only, and no list song and no candidate in 4d first reached the top 10 in any of them{_chk_missing}. Weeks before {BCW['first']} are not hosted.\n"
           f"- **Wikipedia's yearly \"List of Billboard Hot 100 top-ten singles\" pages**, which give each song's top-ten entry date.\n\n"
           f"For the 100 list songs: the first top-10 **date** matches Wikipedia's entry date for **{w_match} of 100**, and the **date and rank** match the Billboard Canada page for **{bc_match} of the {bc_host}** whose week is hosted there. The other {100 - bc_host} ranks rest on the mirror alone. `www.billboard.com` was not read: its robots.txt bars Anthropic's agents, so the Billboard links below are citations, not pages opened in this study.\n")
st_bits = [f"{100 - len(summ)} of the 100 entries rest on a Billboard rap-chart figure read directly from a table (a year-end Hot Rap Songs list or a Hot Rap Songs peak in an artist's discography table)"]
if summ: st_bits.append(f"{len(summ)} {plural(len(summ), 'entry rests', 'entries rest')} on Billboard rap-chart rows known only through web-search summaries of Billboard pages ({'all Drake album cuts, whose Wikipedia tables have no rap column' if all('Drake' in r['artists'] for r in summ) else 'no table with a rap column lists them'}); marked †")
if soft: st_bits.append(f"{len(soft)} excluded {plural(len(soft), 'candidate', 'candidates')} above the cut {plural(len(soft), 'rests', 'rest')} on indirect evidence")
if yend: st_bits.append(f"{len(yend)} more are excluded by deduction from year-end lists (strong, but not a weekly chart row)")
out.append(f"**Status: {'PROVISIONAL at the margins' if (summ or soft) else 'FINAL'}.** " + '. '.join(st_bits) + ". No dispute found in this pass changes the list; each remaining item could move the cut by one place. See *4e. Boundary and open items*.\n")

# ---------------- 4a
out.append('\n## 4a. The list\n')
out.append("Style = the research agents' descriptive tag from source descriptions (not a Billboard category); it drives the verse-led / trap / drill splits in files 01 and 03. Genre tag: \"Rap\" = Billboard classified it as rap (see the genre rule). \"Rap — crossover (…)\" adds the crossover reason: a credited singer from a hand-made list in `scripts/aggregate.py` (singer-rappers not on that list, such as Ty Dolla $ign on \"Carnival\", are not flagged), a pop, dance, country or R&B style tag, or another genre chart. **Chart check:** BC = date and rank match Billboard Canada's licensed chart page; W = date matches Wikipedia's top-ten entry date. **Genre evidence:** a table figure read directly, or † = a Billboard page known only through a web-search summary.\n")
out.append('| # | Title | Credited artists | First top-10 chart | Rank that week | Genre tag | Style | Chart check | Genre evidence |')
out.append('|---|---|---|---|---|---|---|---|---|')
for r in rows:
    x = T.get(r['cid']) or {}
    style = (x.get('style_tag') or '?').replace('_', ' ').replace('boom bap or verse led', 'boom-bap / verse-led')
    cc = CC.get(r['cid']) or {}
    chk = ' + '.join(([f"[BC](https://ca.billboard.com/charts/hot-100/{r['first_top10']})"] if cc.get('billboard_canada') == 'match' else []) + (['W'] if cc.get('wikipedia_entry_date') == 'match' else [])) or 'mirror only'
    mark = '' if status[r['cid']].get('tier') == 'table' else ' †'
    out.append(f"| {r['n']} | {esc(r['title'])}{mark} | {esc(r['artists'])} | [{r['first_top10']}](https://www.billboard.com/charts/hot-100/{r['first_top10']}/) | {r['rank']} | {esc(r['genre_tag'])} | {style} | {chk} | {genre_evidence(r['cid'])} |")

# ---------------- 4b measured
out.append('\n## 4b. Per-track measurements\n')
out.append('Measured on 2026-11-25 from three sources by signal analysis and by reading lyric records; nobody listened to the recordings, and nothing in this table comes from recollection. Method, checks and limits: `05-measurement-method.md`.\n')
out.append('**Legend.**')
out.append("- **Runtime:** duration of the Apple catalog track matched by title and artist; where several editions matched, the one closest to the earlier cited runtime was preferred, so agreement with that runtime (within 2 seconds wherever one exists) is not an independent check. **(cited)** = no Apple catalog match (#13, #14, #30, #75): the runtime is the earlier cited figure and there is no clip, so the tempo cell shows a dash.")
out.append("- **Grid / felt BPM:** from Apple's 30-second preview clip, shown to the nearest half BPM. Grid = the fastest steady pulse that carries the beat (what a DAW project would be set to). Felt = the backbeat tempo (snare or clap on beats 2 and 4), which is the grid or half of it. **M** = clear in the clip; **L** = leaning: the clip favours this reading by a small margin; **I** = resolved by range, not by the clip: only one of the two readings lies in 55–150 BPM, and it is shown even where the other scored slightly higher; **?** = unresolved: either both readings fit (both shown), or an unclear clip reading matches no published tempo at the same, half or double speed (shown as *clip … / listed …*). A clip is one section of the track: a beat switch elsewhere is not seen.")
out.append("- **First line:** time of the first line in the LRCLIB time-synced lyric record that matches the track's length. It is the first *transcribed* line, not necessarily the lead artist: it can be an ad-lib, a spoken line or a transcribed sample (the kind is in table 4b-2), and a wordless intro before it is not counted.")
def _lyr(r): return ((T.get(r['cid']) or {}).get('m') or {}).get('lyr')
def _ruled(l): return bool(l) and l.get('basis') in ('A', 'J')
_mapdiff = []                       # tracks whose section map labels the hook differently from the ruled hook
for r in rows:
    l = _lyr(r)
    if not _ruled(l) or not l['has_hook']: continue
    mh = [sct['start_s'] for sct in (l.get('sections') or []) if sct['label'] == 'hook']
    if not mh or abs(mh[0] - l['first_hook_s']) > 2.5 or len(mh) != l['hook_count']: _mapdiff.append((r, l, mh))
_lendiff = [r for r in rows if _ruled(_lyr(r)) and _lyr(r)['has_hook'] and _lyr(r).get('first_hook_len_s') and _lyr(r).get('hook_lens_s')
            and abs(_lyr(r)['first_hook_len_s'] - _lyr(r)['hook_lens_s'][0]) >= 1.0]
_nohookdens = [r for r in rows if _ruled(_lyr(r)) and _lyr(r)['has_hook'] and not _lyr(r).get('hook_words_per_s')]
_noverse = [r for r in rows if _ruled(_lyr(r)) and not _lyr(r).get('verse_lens_s')]
def _nl(v): return ', '.join(f"#{r['n']}" for r in v)
out.append("- **First hook:** time of the first line of the ruled hook (the main recurring section), with the number of lyric lines before it. *none* = no returning block was accepted as the hook; a short tag can still come back (see the return anchor in table 4b-2). **Hooks** = how many times it occurs.")
out.append(f"- **Hook length** = the ruled first hook from its first line to the end of its last line, as marked in the reading (or the detector's block length). **Verse 1 length** = the first verse section of the reader's map, to the start of the next section. Both are in seconds, and in bars of four felt beats where the felt tempo is resolved (double the bar count on a doubled DAW grid). Table 4b-2 measures every hook as a map section instead, to the start of the next section, so it also takes in any gap before that section; its first hook length differs from this column by a second or more on {len(_lendiff)} tracks ({_nl(_lendiff)}).")
out.append("- **Verse w/s:** words per second across verse sections (section boundaries from the repetition detector).")
out.append("- **Timing basis:** **A** = the repetition detector and an independent AI read of the same lyric record agree; **J** = they disagreed and a second AI reader ruled; **G** = detector only; **X** = unresolved (not counted); G and X do not occur in this table. **no matching record** = no LRCLIB time-synced record within 3 seconds of the track length (#78, #87). Lyric timestamps are crowd-synced; treat them as good to about one second.")
out.append("- **—** = not measured or not applicable: no clip, no lyric record, " + (f"no verse section in the record ({_nl(_noverse)}), " if _noverse else '') + "or no recurring section.\n")
out.append('| # | Title | Runtime | Grid / felt BPM | First line | First hook (lines before) | Hooks | Hook length | Verse 1 length | Verse w/s | Timing basis |')
out.append('|---|---|---|---|---|---|---|---|---|---|---|')
for r in rows:
    x = T.get(r['cid']) or {}; m = x.get('m') or {}; l = m.get('lyr'); f = m.get('feel'); b = m.get('bars') or {}
    rt = (mmss(m['runtime_best_s']) + (' (cited)' if m.get('runtime_best_basis') == 'cited' else '')) if m.get('runtime_best_s') else '—'
    hb = lambda v: f"{round(float(v) * 2) / 2:g}"          # nearest half BPM
    if not f: fe = '—'
    elif f['basis'] == '?' and f.get('listing_conflict'): fe = f"clip {hb(f['felt_bpm_from_clip'])} / listed {' and '.join(f'{v:g}' for v in f['listed_bpm'])} (?)"
    elif f['basis'] == '?': fe = f"{hb(f['grid_bpm'])} / {hb(min(f['estimate_bpm'], f['other_reading_bpm']))} or {hb(max(f['estimate_bpm'], f['other_reading_bpm']))} (?)"
    else: fe = f"{hb(f['grid_bpm'])} / {hb(f['felt_bpm'])} ({f['basis']})"
    if not l: out.append(f"| {r['n']} | {esc(r['title'])} | {rt} | {fe} | — | — | — | — | — | — | no matching record |"); continue
    def sb(sec, bars): return '—' if not sec else (f"{sec:.0f} s" + (f" / {bars:.1f} bars" if bars else ''))
    fh = 'none' if not l['has_hook'] else f"{mmss(l['first_hook_s'])} ({l['lines_before_hook']})"
    out.append(f"| {r['n']} | {esc(r['title'])} | {rt} | {fe} | {l['first_line_s']:.1f} s | {fh} | {l['hook_count'] if l['has_hook'] else '—'} | {sb(l.get('first_hook_len_s') if l['has_hook'] else None, b.get('first_hook_len'))} | "
               f"{sb(l.get('first_verse_len_s'), b.get('first_verse_len'))} | {l['verse_words_per_s'] if l.get('verse_words_per_s') else '—'} | {l['basis']} |")

_rn = [(r['n'], r['title'], C.LYRIC_RECORD_NOTES[r['cid']]) for r in rows if r['cid'] in C.LYRIC_RECORD_NOTES]
if _rn:
    out.append('\n**Record notes.** Lyric records the reader flagged as incomplete:')
    for n_, title_, note_ in _rn: out.append(f"- #{n_} {title_}: {note_}.")
# ---------------- 4b-2 structure per track (the columns behind the M-2 to M-6 counts)
out.append('\n## 4b-2. Per-track structure\n')
out.append("The per-track values behind the structure counts in `03-findings.md`. Everything here comes from the same time-synced lyric record as table 4b; the section map is **one AI reader's call**, a hook sung twice in a row counts as one long hook, and the last section is measured to two typical line gaps after the last lyric line (never past the end of the record). Tracks with no lyric record are left out.\n")
out.append('**Legend and which finding each column backs.**')
out.append("- **First line is** (M-4): the reader's label for the first transcribed line, judged from text: ad-lib, sample or another voice, spoken, sung, rap, or unclear. It is the weakest label in the study.")
out.append("- **Return anchor** (M-3): the time of the earliest line of any block that comes back later (repetition detector). *= hook* means it is within 2.5 seconds of the ruled first hook in table 4b.")
out.append("- **Hook before verse 1** (M-3, M-8): yes when no verse section of the map starts before the ruled first hook in table 4b.")
out.append("- **Intro** (M-4): time before the first hook or verse: the earlier of the map's first verse or hook section and the ruled first hook in table 4b, in seconds and in felt bars where the felt tempo is resolved.")
out.append("- **Section order** (M-5): I intro, V verse, p pre-hook, H hook, q post-hook, B bridge, O outro, x other, each with its start time.")
out.append("- **Verse lengths** and **Hook lengths** (M-5, M-6): every verse section and every hook section of the map, in order, each from its start to the start of the next section, in felt bars where the felt tempo is resolved, otherwise in seconds. The section sizes in M-5, and verse 2 against verse 1 and last hook against first hook in M-6, are read from these. The hook count in M-5 is the ruled count in table 4b.")
_md = '; '.join(f"#{r['n']} {r['title']}: the map has {len(mh)} hook section{'s' if len(mh) != 1 else ''}" + (f" from {mmss(mh[0])}" if mh else '') + f", the ruling {l['hook_count']} from {mmss(l['first_hook_s'])}" for r, l, mh in _mapdiff)
out.append(f"- **Map against ruling:** the section map is the first reader's own. On {len(_mapdiff)} tracks its hook sections differ from the ruled hook in table 4b ({_md}). Where they differ, the first-hook time, the hook count, hook before verse 1 and the intro follow the ruling; the section order and the lengths follow the map." if _mapdiff else "- **Map against ruling:** on every track the map's hook sections match the ruled hook in table 4b.")
out.append("- **Hook on return** (M-6): the reader's label for the words when the hook comes back.")
out.append("- **Verse syll/s · hook w/s** (M-2): verse syllables per second (estimated from spelling) and hook words per second, inside the detector's sections.")
out.append("- **—** = not applicable (no ruled hook" + (f", or no verse section in the record: {_nl(_noverse)}" if _noverse else '') + ")"
           + (f" or not computed: hook words per second needs a hook section from the repetition detector, which marked none on {_nl(_nohookdens)}." if _nohookdens else '.'))
out.append("- **2nd run**: a second, separate run of the reading and ruling. **=** means it reached the same values for hook presence, first line (within 1 s), first hook (within 2.5 s), hook count (within one) and hook-before-verse; otherwise the item that differs is named; *n/a* means that run left the track unruled. It is a consistency check and never changes a value.")
out.append("- In `data/track_measurements.csv` these are the columns `m_first_line_kind`, `m_first_anchor_s`, `m_hook_before_first_verse`, `m_intro_len_s`, `m_section_order`, `m_verse_lens_s`, `m_hook_lens_s`, `m_hook_return`, `m_verse_sylls_per_s`, `m_hook_words_per_s` and `m_second_run`. The column `m_hook_first` is a different measure (the hook has at most three lyric lines before it), and `hook_before_first_verse` without the `m_` prefix is the earlier documented field, not a measurement.\n")
out.append('| # | Title | First line is | Return anchor | Hook before verse 1 | Intro | Section order (start times) | Verse lengths | Hook lengths | Hook on return | Verse syll/s · hook w/s | 2nd run |')
out.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
KIND = {'adlib_or_vocalization': 'ad-lib', 'sample_or_other_voice': 'sample / other voice', 'spoken': 'spoken', 'sung': 'sung', 'rap': 'rap', 'unclear': 'unclear'}
RET = {'identical': 'same words', 'minor_variation': 'small changes', 'extended': 'extended', 'shortened': 'shortened', 'new_lyrics': 'new lyrics', 'not_applicable': '—'}
LAB = {'intro': 'I', 'verse': 'V', 'pre_hook': 'p', 'hook': 'H', 'post_hook': 'q', 'bridge': 'B', 'outro': 'O', 'other': 'x'}
for r in rows:
    x = T.get(r['cid']) or {}; m = x.get('m') or {}; l = m.get('lyr'); b = m.get('bars') or {}
    if not l or l.get('basis') not in ('A', 'J', 'G'): continue
    anchor = 'none' if l.get('first_anchor_s') is None else mmss(l['first_anchor_s']) + (' = hook' if l.get('anchor_is_hook') else '')
    hbv = '—' if not l['has_hook'] or l.get('hook_before_first_verse') is None else ('yes' if l['hook_before_first_verse'] else 'no')
    intro = '—' if l.get('intro_len_s') is None else f"{l['intro_len_s']:.0f} s" + (f" / {b['intro_len']:.1f} bars" if b.get('intro_len') is not None else '')
    order = ' · '.join(f"{LAB.get(sec['label'], '?')} {mmss(sec['start_s'])}" for sec in (l.get('sections') or [])) or '—'
    def lens(key):
        if b.get(key): return ' · '.join(f"{v:g}" for v in b[key]) + ' bars'
        v = l.get(key + '_s') or []
        return (' · '.join(f"{y:.0f}" for y in v) + ' s') if v else '—'
    dens = (f"{l['verse_sylls_per_s']:.1f}" if l.get('verse_sylls_per_s') else '—') + ' · ' + (f"{l['hook_words_per_s']:.1f}" if (l['has_hook'] and l.get('hook_words_per_s')) else '—')
    out.append(f"| {r['n']} | {esc(r['title'])} | {KIND.get(l.get('first_line_kind'), '—')} | {anchor} | {hbv} | {intro} | {order} | {lens('verse_lens')} | {lens('hook_lens') if l['has_hook'] else '—'} | "
               f"{RET.get(l.get('hook_return'), '—') if l['has_hook'] else '—'} | {dens} | {l.get('second_run_code') or '—'} |")

# ---------------- 4c documented
out.append('\n## 4c. Per-track documented facts\n')
out.append('**Legend.**')
out.append("- **Basis:** **P** = the saved Wikipedia or Songfacts page text states the fact or names the work, and a skeptic upheld that. A P can come from a supported verdict, from a partly supported one whose quoted words are in the saved page (the detail that is not on the page is not counted), or from a new page statement; `05-measurement-method.md` gives the split. **S** = a cited source the earlier verifier did not reject, known only through web-search summaries; **U** = cited, but not confirmed (never counted); **R** = unverified recollection (never counted); **?** = unknown. Unknown never counts as \"no\". The reader, the skeptic and the earlier verifier were AI agents; no person read the pages.")
out.append("- **Opening** = what is heard first, as a source describes it. **Beat switch** = a source describes a change of beat or instrumental.")
out.append("- **Return change** = coded from a cited description of what changes between sections: beat = a beat or bed change; voice = a new voice; register = the same rapper's register or character; delivery = a spoken insert or break; (one-way) = a switch that does not return; none specific = the cited descriptions say nothing specific changes; **?** = no cited description of a return was coded (unknown, not \"no\").")
out.append("- **Borrowing:** s = sample, i = interpolation, c = dialogue clip, r = self-reuse; (u) = uncredited; (credit not stated) = the source does not say whether it is credited; (no URL) = named by research with no source link. ✓ = stated in the saved page text; (S) = credited per the earlier verifier's web-search summary and not found on a saved page; no mark = cited by research, not flagged; U = could not be re-found (not counted); **?** = no borrowing on file (unknown, not \"none\").")
out.append("- **2nd voice** = the Billboard credit names a second vocalist (producer-only credits such as Metro Boomin do not count).")
out.append("- **Path:** **D** = debuted in the top 10; **C** = climbed in from the rank shown. wk = weeks in the top 10; tot = total Hot 100 weeks; AB = album-bomb cut (3+ songs by the same lead artist first entering the top 10 that week).\n")
out.append('| # | Title | Opening | Beat switch | Return change | Borrowing | 2nd voice | Path |')
out.append('|---|---|---|---|---|---|---|---|')
CODE = {'page': 'P', 'source': 'S', 'unconfirmed': 'U', 'unverified_recollection': 'R', 'unknown': '?', None: '?'}
OPN = {'sample_or_interpolation': 'sample/interp.', 'ad_lib_or_spoken_intro': 'spoken/ad-lib intro', 'hook_or_chorus': 'hook', 'rap_verse': 'rap verse',
       'sung_intro': 'sung intro', 'producer_tag': 'producer tag', 'instrumental': 'instrumental', 'chant': 'crowd chant'}
BT = {'sample': 's', 'interpolation': 'i', 'audio clip': 'c', 'self-reuse': 'r'}
SM = {'confirmed': ' (S)', 'page': ' ✓', 'not_reconfirmed': ' U', 'rejected': ' ✗', 'cited': '', 'uncited': ' (no URL)'}
NON_VOCAL = {'Metro Boomin'}


def credit_names(a):
    a = a.replace('Tyler, The Creator', 'Tyler The Creator').replace('¥$: ', '')
    return [x.strip() for x in re.split(r' Featuring | With | & | X |, ', a) if x.strip()]


for r in rows:
    x = T.get(r['cid'])
    path = ('D' if r['debut_in_top10'] else f"C from #{r['climbed_from']}") + f" · {r['weeks_in_top10']} wk · {r['total_weeks']} tot" + (' · AB' if r['album_bomb'] else '')
    second = 'yes' if len([n for n in credit_names(r['artists']) if n not in NON_VOCAL]) >= 2 else 'no'
    if not x:
        out.append(f"| {r['n']} | {esc(r['title'])} | not studied |  |  |  | {second} | {path} |"); continue
    op = f"{OPN.get(x['opening_element'], x['opening_element'])} ({CODE.get(x['opening_basis'], '?')})" if x.get('opening_element') not in (None, 'unknown') else '?'
    bs = f"{x['beat_switch']} ({CODE.get(x['beat_switch_basis'], '?')})" if x.get('beat_switch') not in (None, 'unknown') else '?'
    if any(d.get('basis') in ('source', 'page') for d in x.get('returns') or []):
        rc = C.RETURN_TYPES.get(r['cid'], 'uncoded').replace('beat+voice', 'beat + voice').replace('none', 'none specific') + (' (one-way)' if C.RETURNING.get(r['cid']) is False else '')
    elif any(d.get('basis') == 'unconfirmed' for d in x.get('returns') or []): rc = 'beat (U)'
    else: rc = '?'
    sm = '; '.join(f"{short(s.get('work', ''))} [{BT.get(s.get('borrow_type'), '?')}{'' if s.get('credited', True) is True else (' (u)' if s.get('credited', True) is False else ' (credit not stated)')}{SM.get(s.get('status'), '')}]" for s in x.get('samples') or [] if s.get('status') != 'rejected') or '?'
    out.append(f"| {r['n']} | {esc(r['title'])} | {op} | {bs} | {rc} | {sm} | {second} | {path} |")
vn = [(r['n'], r['title'], C.VERSION_NOTES[r['title']]) for r in rows if r['title'] in C.VERSION_NOTES]
out.append('\n**Version notes.** The study treats the original album or single version as the recording, except where noted here:')
for n, title, note in vn: out.append(f"- #{n} {title}: {note}")
# which catalog recording the measurements in 4b were taken from
_ed = collections.Counter(((T.get(r['cid']) or {}).get('m') or {}).get('runtime_edition') for r in rows)
_nocat = [f"#{r['n']} {r['title']}" for r in rows if not ((T.get(r['cid']) or {}).get('m') or {}).get('runtime_track')]
_diff = []
import unicodedata
def _nm(x):
    """Title without a (feat. ...) or (with ...) suffix, accents, case or punctuation."""
    x = re.sub(r'\s*[\(\[](?:feat\.?|with|featuring)[^\)\]]*[\)\]]', '', x, flags=re.I)
    x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', x.lower())
for r in rows:
    m_ = (T.get(r['cid']) or {}).get('m') or {}
    tr_ = m_.get('runtime_track')
    if tr_ and _nm(tr_) != _nm(r['title']):
        _diff.append(f"#{r['n']} {r['title']}: \"{tr_}\" on *{m_.get('runtime_collection')}*")
out.append(f"\n**Recording measured (table 4b).** The runtime and the preview clip come from the Apple catalog track matched by title and artist: "
           f"{_ed.get('cleaned', 0)} are clean editions of explicit songs and {_ed.get('notExplicit', 0)} are entries Apple does not flag as explicit. "
           f"Where an earlier cited runtime for the explicit version exists, the catalog track is within 2 seconds of it in every case, so a clean edition is treated as the same recording with words muted or replaced (an inference from length, not a listening check). "
           f"The lyric record was matched to the track's length within 3 seconds. "
           f"No catalog match: {', '.join(_nocat) or 'none'} (runtime cited, no clip). "
           f"The catalog track name, collection and release date for the {len(rows) - len(_nocat)} matched songs are in `data/track_measurements.csv` (`m_catalog_track`, `m_catalog_collection`, `m_catalog_release_date`), with the edition in `m_runtime_edition` and the LRCLIB record id in `m_lyric_record`; the catalog columns are blank for the unmatched songs.")
if _diff:
    out.append('Catalog track names that differ from the chart title beyond a featuring credit (clean-edition titles):')
    for d in _diff: out.append(f"- {d}")

# ---------------- 4d
out.append('\n## 4d. Close calls and exclusions (genre)\n')
_x4a = [r for r in rows if 'crossover' in r['genre_tag']]
_x4d = {o['cid'] for o in in_window if o['prior'] == 'close'}
_xmiss = [f"#{r['n']}" for r in _x4a if r['cid'] not in _x4d]
_xplain = [f"#{r['n']}" for r in rows if r['cid'] in _x4d and 'crossover' not in r['genre_tag']]
_xnote = (f"{len(_xmiss)} crossover-tagged songs were not pre-flagged and are not repeated here ({', '.join(_xmiss)}), and {len(_xplain)} pre-flagged songs carry the plain Rap tag ({', '.join(_xplain)}). "
          "The pre-check flag comes from a hand-made list (`CLOSE` in `scripts/candidates.py`), written before any chart evidence was read, of songs whose genre the author judged ambiguous; it records no reason for each song. "
          f"The {len(_xplain)} with the plain Rap tag were then classified as rap on chart evidence, and none of them has a credited singer from the 4a list, a crossover style tag or another genre chart, so 4a gives them no crossover reason.")
out.append("Every candidate in the window that was flagged as a close genre call before checking, whether it ended up included or left out, plus every other candidate that was left out. This is the pre-check flag, not the \"Rap — crossover\" tag in 4a, which is assigned from credits and style tags: " + _xnote + " **Included** = Billboard classified it as rap. **Excluded (non-rap chart)** = Billboard charts it on Hot R&B Songs or an R&B-only component chart (the working rule in the header). **Excluded (year-end lists)** = deduced from year-end lists read directly: the song is on a year-end Hot R&B/Hip-Hop or Hot 100 list at a rank where a rap title would also make the 50-title year-end Hot Rap Songs list, and it is not there. **Excluded (indirect)** and **(unresolved)** rest on weaker evidence, including a listing on a country, rock or dance chart with no rap-chart row found, and are carried into 4e. Evidence that begins *Search summary* was read in a web-search summary of the page named; the page itself was not opened.\n")
out.append('| First top-10 | Rank | Title | Artists | Decision | Evidence |')
out.append('|---|---|---|---|---|---|')
DEC = {'direct': 'Excluded (non-rap chart)', 'yearend': 'Excluded (year-end lists)', 'indirect': 'Excluded (indirect)', 'unresolved': 'Excluded (unresolved)'}
for o in in_window:
    if not (o['prior'] == 'close' or o['cid'] not in final_ids): continue
    st = status[o['cid']]; b = ev_best(o['cid']) or {}
    if o['cid'] in final_ids: dec = 'Included (rap)'; ev = genre_evidence(o['cid'])
    elif st['status'] == 'rap': dec = 'Rap, but outside the 100'; ev = genre_evidence(o['cid'])
    else:
        dec = DEC[grade[o['cid']]]
        full_ = b.get('evidence_summary') or st['basis']
        full_ = full_.replace('visible)', 'in the summary)')
        # a research agent's gloss, not something a page was read to say (the R&B / rap split is this study's working rule)
        full_ = full_.replace(", the R&B half of Hot R&B/Hip-Hop Songs (Hot Rap Songs is the rap half)", "")
        if o['cid'] in C.EVIDENCE_DISPLAY: full_ = C.EVIDENCE_DISPLAY[o['cid']]
        elif st.get('tier') == 'summary' and not re.search(r'search summar|search-result|search results|read directly|recollection', full_, re.I): full_ = 'Search summary (page not opened): ' + full_
        if b.get('evidence_type') in ('model_knowledge_only', 'none', None) and not table_note(o): full_ = 'Model recollection only, not searched. ' + re.sub(r'Not searched[^.]*\.\s*|From memory,?\s*|\bUnverified\.?\s*', '', full_).strip()
        tn = table_note(o)
        lk = ''
        if b.get('source_urls'):
            u = b['source_urls'][0]; d = domain(u)
            lk = f" ([{SITE.get(d, 'Billboard' if 'billboard.com' in d else d)}]({u}))"
        ev = short(full_, 330 if o['cid'] in C.EVIDENCE_DISPLAY else 290) + lk + (f" **Tables read directly:** {tn}." if tn else '')
    out.append(f"| {o['first_top10']} | {o['rank']} | {esc(o['title'])} | {esc(o['artist'])} | {dec} | {ev} |")
out.append('\n**Exclusion audit.** 209 other top-10 songs from the window were pre-tagged non-rap by artist and genre (pop, country, Latin, rock, R&B). A separate audit specifically checked 37 of them (8 searches plus year-end-list and rap-drought reasoning) and flagged none as rap. It left 6 rap-adjacent songs not conclusively checked ("Fancy Like", "Permission To Dance", "My Universe", "Fortnight", "I Had Some Help", "I Ain\'t Coming Back") and did not search the rest, which are plainly non-rap. A cross-check in this pass against the full year-end Hot Rap Songs lists for 2021–2025 found none of the excluded songs on any of them. The audit also recorded, from web-search summaries of articles it did not open, the reported rap top-10 drought: no hip-hop song reached the top 10 from "What Did I Miss?" (July 2025) until spring 2026, and Billboard reported no rap songs in the top 40 on the charts dated 2025-10-25 and 2025-11-01, a first since 1990.\n')

_inv = SF.yearend_inversions()
_dc = SF.dash_conflicts()
# the weakest year-end deduction: the excluded song with the lowest year-end Hot 100 rank and no R&B/Hip-Hop year-end rank
def _weakest():
    c = [(rk, yr, o) for o in yend for yr, rk in (status[o['cid']].get('ye_hot100') or []) if not status[o['cid']].get('ye_rbhh')]
    best = {}
    for rk, yr, o in c:                                   # a song's best (lowest-numbered) year-end rank is the one the deduction uses
        if o['cid'] not in best or rk < best[o['cid']][0]: best[o['cid']] = (rk, yr, o)
    if not best: return ''
    rk, yr, o = max(best.values(), key=lambda x: x[0])
    h = {nz(e['title']): e['rank'] for e in WL['yearend_hot100'] if e['year'] == yr}
    below = sorted(e['rank'] for e in WL['yearend_rap'] if e['year'] == yr and h.get(nz(e['title']), 0) > rk)
    if not below: return ''
    return (f" The weakest is \"{o['title']}\" (No. {rk} on the {yr} year-end Hot 100): the rap-list titles that rank below it on that Hot 100 list sit at "
            f"Nos. {', '.join(str(x) for x in below[:-1])} and {below[-1]} of the 50-title rap list, so a rap title at No. {rk} would have made the rap list.")
_weak = _weakest()
_fut = ['\"' + x['title'] + '\"' for x in _dc['songs'] if 'Future_singles_discography' in x['dash_pages']]
# ---------------- 4e
out.append('\n## 4e. Boundary and open items\n')
out.append(f"- **#100 is {rows[-1]['title']}** ({rows[-1]['first_top10']}, #{rows[-1]['rank']}). The next rap songs in line are " + '; '.join(S['boundary_next'][:5]) + '.')
if summ:
    out.append('- **Included on search-summary evidence (†):** ' + '; '.join(f"#{r['n']} {r['title']}" for r in summ) + ". For each, a web-search summary of a Billboard chart page or report places the song on Rap Streaming Songs, Rap Airplay or Hot Rap Songs (rows in `data/classification_evidence.csv`), and Wikipedia gives a Hot R&B/Hip-Hop Songs peak, but no table with a rap column lists it and the Billboard page itself was not opened. Two collaborators' tables show a dash in the rap column: Future's for \"Ran To Atlanta\" and Quavo's for \"Shabang\". A dash is not evidence. Across the " + f"{_dc['tables_with_rap_column']} discography tables with a rap column, {len(_dc['songs'])} songs show a dash in one table and a numbered Hot Rap Songs peak in another (`data/measured/discography_dash_conflicts.json`), {len(_fut)} of them in Future's table ({', '.join(_fut)})" + ", so those dashes are treated as unfilled cells. If any of these is not rap, every later song moves up one place and \"Love All\" enters at #100.")
if soft:
    def why(o):
        b = (ev_best(o['cid']) or {}).get('evidence_summary') or status[o['cid']]['basis']
        return short(b, 170) + (f" Tables: {table_note(o)}." if table_note(o) else '')
    out.append('- **Excluded on indirect or unresolved evidence, ranked above the cut** (if any is rap, it enters at its date and rank, and #100 drops out): ' + '; '.join(f"{o['first_top10']} #{o['rank']} {o['title']} — {o['artist']} ({why(o)})" for o in soft) + '.')
if yend:
    out.append('- **Excluded by deduction from year-end lists:** ' + '; '.join(f"{o['first_top10']} #{o['rank']} {o['title']} — {o['artist']}" for o in yend) + '. The year-end rap and R&B/hip-hop orders are not identical: taking titles in rap-list order, the R&B/hip-hop rank falls from one title to the next in ' + f"{min(_inv.values())} to {max(_inv.values())}" + ' places a year (' + ', '.join(f"{y}: {k}" for y, k in sorted(_inv.items())) + '). The deduction is therefore strong only away from the bottom of the lists; none of these sits near it.' + _weak)
out.append('- **Newest end.** No rap-classified song is known to have first reached the top 10 between the chart dated 2026-05-30 and the 2026-11-21 starting chart. "Solar Eclipse" (Drake & Don Toliver, 2026-10-17 #5) is R&B-classified (Billboard reporting, read in search summaries: a No. 1 debut on Hot R&B Songs). The other three are excluded on indirect evidence, with no rap-chart row found for any of them: "Babydoll" (2026-10-24 #10) is on Hot Rock & Alternative Songs (peak No. 2) and on no R&B/hip-hop chart in its Wikipedia table; "Boston" (2026-07-25 #6) is reported as a country-radio No. 1; "Nicole Kidman" (2026-10-17 #9) is called a pop hit in a Billboard headline. A rock or country listing does not by itself rule out rap under the genre rule above, which is why these are graded indirect.')
out.append('- **The cut splits one chart week, as the ordering rule requires.** *Certified Lover Boy* put nine songs in the top 10 on the chart dated 2021-09-18. Ties in a week are broken by position that week, so "TSU" (#9) is #100 and "Love All" (#10) is the first song outside the list.')
out.append(f"- **No missing chart weeks** were found in the weekly Hot 100 series for the window. The {len(BCW['missing_later'])} weeks Billboard Canada does not host (named under *Rank and date sources*) contain no first top-10 entry by a list song or a candidate in 4d.")
open(REPO + '04-reference-list.md', 'w').write('\n'.join(out) + '\n')
with open(REPO + 'data/classification_evidence.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['cid', 'first_top10', 'rank', 'title', 'artists', 'prior_tag', 'final_status', 'evidence_tier', 'basis', 'earlier_basis', 'year_end_rap', 'year_end_rbhh', 'year_end_hot100',
                                   'discography_rap_peak', 'discography_rap_pages', 'discography_rap_dash_pages', 'wikipedia_genre_charts', 'best_evidence_type', 'best_confidence', 'source_urls', 'hot100_rank_reported'])
    for o in cands:
        st = status[o['cid']]; b = ev_best(o['cid']) or {}
        fmt = lambda xs: ' '.join(f'{y}:{k}' for y, k in xs)
        w.writerow([o['cid'], o['first_top10'], o['rank'], o['title'], o['artist'], o['prior'], st['status'], st.get('tier'), st['basis'], st.get('earlier_basis'), fmt(st.get('ye_rap') or []), fmt(st.get('ye_rbhh') or []), fmt(st.get('ye_hot100') or []),
                    st.get('discog_rap_peak'), ' '.join(st.get('discog_rap_pages') or []), ' '.join(st.get('discog_rap_dash_pages') or []), ' '.join(st.get('wiki_genre_charts') or []),
                    b.get('evidence_type'), b.get('confidence'), ' '.join(b.get('source_urls') or []), b.get('hot100_rank_reported')])
print('rendered', len(rows), 'rows;', len(summ), 'summary-tier;', len(soft), 'soft exclusions;', len(yend), 'year-end deductions;', 'grades', dict(collections.Counter(grade.values())))
