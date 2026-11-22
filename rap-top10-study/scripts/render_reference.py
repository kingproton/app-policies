"""Render 04-reference-list.md from final_rows.json, tracks_merged.json, classification evidence and chart metrics."""
import json, re, os, csv, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrections as C
from paths import WORK
from paths import REPO
rows = json.load(open(WORK + 'final_rows.json'))
T = {int(k): v for k, v in json.load(open(WORK + 'tracks_merged.json')).items()}
status = {r['cid']: r for r in json.load(open(WORK + 'classification_status.json'))}
col = json.load(open(WORK + 'collected.json'))
S = json.load(open(WORK + 'stats.json'))
cands = json.load(open(WORK + 'to_verify.json'))
SITE = {'hypebeast.com': 'Hypebeast', 'yahoo.com': 'Yahoo (Billboard syndication)', 'en.wikipedia.org': 'Wikipedia', 'uproxx.com': 'Uproxx',
        'aceshowbiz.com': 'AceShowbiz', 'radiox.cms.socastsrm.com': 'radio-station site', 'stereogum.com': 'Stereogum', 'npr.org': 'NPR',
        'thesource.com': 'The Source', 'rated-rnb.com': 'Rated R&B', 'musictimes.com': 'Music Times', 'hotnewhiphop.com': 'HotNewHipHop'}
EVLAB = {'billboard_chart_page': 'Billboard chart page', 'billboard_article': 'Billboard report', 'wikipedia_chart_table': 'Wikipedia chart table',
         'other_press': 'press citing Billboard'}


def esc(s): return (s or '').replace('|', '/').replace('\n', ' ')


def short(s, n=70):
    s = esc(s)
    if len(s) <= n: return s
    cut = s[:n].rsplit(' ', 1)[0]
    return cut.rstrip(',;:(') + '…'


def domain(u): return re.sub(r'^https?://(www\.)?', '', u).split('/')[0]


def ev_best(cid):
    ov = C.CLASSIFICATION_OVERRIDES.get(cid)
    if ov: return dict(evidence_type=ov['evidence_type'], confidence=ov['confidence'], evidence_summary=ov['summary'] + ' [targeted re-check]', source_urls=[ov['source_url']] if ov.get('source_url') else [])
    ev = col['classify'].get(str(cid), [])
    ev = sorted(ev, key=lambda e: ({'high': 3, 'medium': 2, 'low': 1}.get(e['confidence'], 0), e['evidence_type'] != 'model_knowledge_only'))
    return ev[-1] if ev else None


def yearend_links(text):
    yrs = []
    for m in re.finditer(r'(?:Year-End Hot Rap Songs(?: of)? (\d{4})|(\d{4}) year-end Hot Rap Songs|YE Hot Rap Songs (\d{4}))', text or '', re.I):
        y = next(g for g in m.groups() if g)
        if y not in yrs: yrs.append(y)
    return [f"[YE Hot Rap Songs {y}](https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_Rap_Songs_of_{y})" for y in yrs]


def link_for(cid):
    st = status[cid]
    if st['basis'].startswith('Year-End'):
        yr = re.search(r'(\d{4})', st['basis']).group(1); rk = re.search(r'#(\d+)', st['basis'])
        return f"[YE Hot Rap Songs {yr}{' #' + rk.group(1) if rk else ''}](https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_Rap_Songs_of_{yr})"
    ye = yearend_links(st['basis'])
    if ye: return ' · '.join(ye)
    b = ev_best(cid)
    if not (b and b.get('source_urls')): return 'genre unverified'
    u = b['source_urls'][0]; d = domain(u)
    if b['evidence_type'] in ('model_knowledge_only', 'none'):
        return f"genre unverified ([page]({u}) confirms the Hot 100 position only)"
    lab = EVLAB.get(b['evidence_type'], b['evidence_type'])
    if 'billboard.com' in d: lab = 'Billboard chart page' if ('/charts/' in u or '/chart-history/' in u) else 'Billboard report'
    else: lab = SITE.get(d, d) + (' (reporting Billboard)' if b['evidence_type'] in ('billboard_article', 'billboard_chart_page', 'other_press') else '')
    return f"[{lab}]({u})"


def mark(r):
    if 'provisional' in r['classification']: return ' †'
    if r['cid'] in C.ALBUM_MATE_INFERRED: return ' ‡'
    return ''


out = []
prov = [r for r in rows if 'provisional' in r['classification']]
inf = [r for r in rows if r['cid'] in C.ALBUM_MATE_INFERRED and 'provisional' not in r['classification']]
final_ids = {r['cid'] for r in rows}
cut_date = rows[-1]['first_top10']
in_window = [o for o in cands if o['first_top10'] >= cut_date]
def soft_kind(o):
    st = status[o['cid']]
    if o['cid'] in final_ids: return None
    if st['status'] == 'unverified': return 'unresolved'
    if o['cid'] in C.GENRE_INFERENCE_EXCLUSIONS: return 'genre'
    if o['cid'] in C.YEAREND_ABSENCE_EXCLUSIONS: return 'yearend'
    if st['status'] == 'not_rap' and st['basis'].split(':', 1)[-1].strip().startswith('Inferred'): return 'inferred'
    return None
soft_excl = [o for o in in_window if soft_kind(o)]
out.append('# 4 — Full reference list (100 songs)\n')
out.append(f"**Reference window:** first Hot 100 top-10 weeks from the chart dated **{S['span'].split(' to ')[1]}** back to **{S['span'].split(' to ')[0]}**. That is the 100 most recent distinct rap songs, counting back from the chart dated 2026-11-21 (research cutoff 2026-11-22).\n")
out.append("**Ordering rule:** by the chart week each song *first* reached positions 1–10, newest first. Ties within a week are sorted by position that week. Each song is counted once. Billboard's combined credits and remixes are followed, so Billboard's mid-run re-credit of \"Carnival\" from Kanye West to Ye counts as one song.\n")
out.append("**Genre rule:** rap = Billboard placed the song on Hot Rap Songs or on a rap-only component chart (Rap Streaming Songs, Rap Airplay), or Billboard reporting says so. Hot R&B Songs and Hot Rap Songs are mutually exclusive halves of Hot R&B/Hip-Hop Songs, so R&B-classified songs by rappers are excluded and logged below.\n")
out.append("**Rank and date source:** every weekly Hot 100 chart since 1958, from the public `mhollingshead/billboard-hot-100` mirror of billboard.com. It has no missing weeks since 2015. All 155 candidate dates and ranks were re-derived from the weekly charts, and Billboard or press reporting confirmed the rank in a sample of weeks (see `data/classification_evidence.csv`).\n")
status_bits = []
def plural(n, one, many): return one if n == 1 else many
if prov: status_bits.append(f"{len(prov)} {plural(len(prov), 'entry is', 'entries are')} included without direct classification evidence: each was pre-tagged rap, and a targeted re-check found only indirect evidence (a Hot R&B/Hip-Hop Songs peak, which does not separate rap from R&B, or album-mates on rap charts). {plural(len(prov), 'It is', 'They are')} marked †")
if inf: status_bits.append(f"{len(inf)} {plural(len(inf), 'entry is', 'entries are')} included because album-mates from the same release week were on a rap chart, with no page showing the title itself; marked ‡")
if soft_excl: status_bits.append(f"{len(soft_excl)} excluded {plural(len(soft_excl), 'candidate', 'candidates')} above the cut {plural(len(soft_excl), 'rests', 'rest')} on inference or indirect evidence, not a direct non-rap listing ({sum(1 for o in soft_excl if soft_kind(o) == 'yearend')} of them are absent from all three year-end genre lists, which is strong but indirect)")
out.append(f"**Status: {'PROVISIONAL' if (prov or inf or soft_excl) else 'FINAL'}.** " + '. '.join(status_bits) + ". Any one of these could move the cut. See *4d. Boundary and open items*.\n")
out.append('\n## 4a. The list\n')
out.append("Style = the research agents' descriptive tag from source descriptions (not a Billboard category); it drives the verse-led / trap / drill splits in files 01 and 03. Genre tag: \"Rap\" = Billboard classified it as rap (see the genre rule). \"Rap — crossover (…)\" = rap-classified, but the credit includes a non-rap vocalist (feat./co-lead) and/or the style tag is pop, R&B, dance/house, country or Jersey club; the parenthesis names which. This is the study's own label, not a Billboard category.\n")
out.append('| # | Title | Credited artists | First top-10 chart | Rank that week | Genre tag | Style | Source |')
out.append('|---|---|---|---|---|---|---|---|')
for r in rows:
    x = T.get(r['cid']) or {}
    style = (x.get('style_tag') or '?').replace('_', ' ').replace('boom bap or verse led', 'boom-bap / verse-led')
    out.append(f"| {r['n']} | {esc(r['title'])}{mark(r)} | {esc(r['artists'])} | {r['first_top10']} | {r['rank']} | {esc(r['genre_tag'])} | {style} | "
               f"[Hot 100 {r['first_top10']}](https://www.billboard.com/charts/hot-100/{r['first_top10']}/) · {link_for(r['cid'])} |")

# ---------------- 4b
out.append('\n## 4b. Per-track measurements used in the findings\n')
out.append('**Legend.**')
out.append('- **Basis:** **S** = a cited source the verifier did not reject, or a later gap sweep\'s own citation that the separate re-check confirmed (two sweep openings, "Houdini" and "Carnival", were recoded to what the re-check\'s sources support); **U** = cited, but the verifier (or, for a sweep claim, the re-check) could not confirm it, so it is *not* counted as sourced; **R** = unverified recollection, never counted; **?** = unknown.')
out.append('- **Runtime:** ✔ = verifier confirmed; ✎ = verifier corrected; ◦ = verifier could not confirm; ♪ = taken from a BPM-site listing.')
out.append('- **Grid / felt BPM:** grid = DAW tempo convention, felt = rap-bar pulse. Every felt value is a genre-convention inference; no source describes the feel. Marks: ✔ = verifier agreed; ✎ = corrected; ◦ = verifier could not confirm; · = one listing or the tempo sweep only; ⚠ = conflicting listings. "unresolved" = half- or full-time cannot be told from the listings. "listed X (not used)" = a published BPM exists but M-1 does not use it (conflicting listings, a single listing found only by the verifier, or a low-confidence listing; reasons in M-1). Rows marked ⚠, unresolved or not used are excluded from M-1.')
out.append('- **Hook first** = the hook arrives before the first verse (a short spoken line, tag or sample intro may come before it).')
out.append('- **Return change** = coded by me from a cited description of what changes between sections: beat = a beat or bed change; voice = a new voice; register = the same rapper\'s register or character; delivery = a spoken insert or break; none specific = sources say nothing specific changes; beat + voice = both. "(one-way)" = a one-way switch or an intro/outro hand-off, not a section that comes back. "beat (U)" = described, but the verifier could not confirm the matching switch or intro claim (excluded from M-6). — = not documented.')
out.append('- **Borrowing:** s = sample, i = interpolation, c = dialogue clip, r = self-reuse; (u) = uncredited. ✓ = confirmed or added by the verifier; no mark = cited by research, not flagged; U = the verifier could not re-find it (not counted as sourced); ✗ = rejected (not counted); (no URL) = named by research without a source link and not checked by the verifier. — = none documented (unknown, not a verified absence). Full credits are in `data/track_measurements.csv`.')
out.append('- **Hook:** (S) = sourced; (unv.) = not sourced: a cited claim the verifier could not confirm, a source that itself calls it unverified, an inference from described sections, or recollection (the hook field has no finer basis code).')
out.append('- **2nd voice** = the Billboard credit names a second vocalist (producer-only credits such as Metro Boomin do not count).')
out.append('- **Path:** **D** = debuted in the top 10; **C** = climbed in from the rank shown. wk = weeks in the top 10; tot = total Hot 100 weeks; AB = album-bomb cut (3+ songs by the same lead artist first entering the top 10 that week).\n')
out.append('| # | Title | Runtime | Grid / felt | Opening | Hook first | Hook | Beat switch | Return change | Borrowing | 2nd voice | Path |')
out.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
CODE = {'source': 'S', 'unconfirmed': 'U', 'unverified_recollection': 'R', 'unknown': '?', None: '?'}
TST = {'verified': ' ✔', 'corrected_by_verifier': ' ✎', 'verifier_could_not_confirm': ' ◦', 'research_only': ' ·', 'tempo_sweep': ' ·', 'conflict': ' ⚠'}
RTS = {'verified': ' ✔', 'corrected_by_verifier': ' ✎', 'verifier_could_not_confirm': ' ◦', 'tempo_sweep': ' ♪'}
HK = {'present_verified': 'yes (S)', 'present_unverified': 'yes (unv.)', 'absent_verified': 'none (S)', 'absent_unverified': 'none (unv.)'}
OPN = {'sample_or_interpolation': 'sample/interp.', 'ad_lib_or_spoken_intro': 'spoken/ad-lib intro', 'hook_or_chorus': 'hook', 'rap_verse': 'rap verse',
       'sung_intro': 'sung intro', 'producer_tag': 'producer tag', 'instrumental': 'instrumental', 'chant': 'crowd chant'}
BT = {'sample': 's', 'interpolation': 'i', 'audio clip': 'c', 'self-reuse': 'r'}
SM = {'confirmed': ' ✓', 'not_reconfirmed': ' U', 'rejected': ' ✗', 'cited': '', 'uncited': ' (no URL)'}
NON_VOCAL = {'Metro Boomin'}


def credit_names(a):
    a = a.replace('Tyler, The Creator', 'Tyler The Creator').replace('¥$: ', '')
    return [x.strip() for x in re.split(r' Featuring | With | & | X |, ', a) if x.strip()]


for r in rows:
    x = T.get(r['cid'])
    path = ('D' if r['debut_in_top10'] else f"C from #{r['climbed_from']}") + f" · {r['weeks_in_top10']} wk · {r['total_weeks']} tot" + (' · AB' if r['album_bomb'] else '')
    second = 'yes' if len([n for n in credit_names(r['artists']) if n not in NON_VOCAL]) >= 2 else 'no'
    if not x:
        out.append(f"| {r['n']} | {esc(r['title'])} | not studied |  |  |  |  |  |  |  | {second} | {path} |"); continue
    lv = sorted({f"{float(v['bpm']):g}" for v in x.get('tempo_listed') or [] if v.get('bpm')}, key=float)
    if x.get('tempo_status') == 'conflict': bpm = 'listed ' + ', '.join(lv) + ' ⚠ (not used)'
    elif x.get('grid_bpm') and x.get('felt_bpm'): bpm = f"{x['grid_bpm']:g} / {x['felt_bpm']:g}{TST.get(x['tempo_status'], ' ·')}"
    elif x.get('tempo_status') == 'feel_unresolved': bpm = (f"{x['grid_bpm']:g}" if x.get('grid_bpm') else 'listed ' + ', '.join(lv)) + ' / unresolved'
    elif lv: bpm = 'listed ' + ', '.join(lv) + (' ⚠' if len(lv) >= 2 else '') + ' (not used)'
    else: bpm = '?'
    op = f"{OPN.get(x['opening_element'], x['opening_element'])} ({CODE.get(x['opening_basis'], '?')})" if x.get('opening_element') not in (None, 'unknown') else '?'
    hf = f"{x['hook_first']} ({CODE.get(x['hook_first_basis'], '?')})" if x.get('hook_first') not in (None, 'unknown') else '?'
    bs = f"{x['beat_switch']} ({CODE.get(x['beat_switch_basis'], '?')})" if x.get('beat_switch') not in (None, 'unknown') else '?'
    if any(d.get('basis') == 'source' for d in x.get('returns') or []):
        rc = C.RETURN_TYPES.get(r['cid'], 'uncoded').replace('beat+voice', 'beat + voice').replace('none', 'none specific') + (' (one-way)' if C.RETURNING.get(r['cid']) is False else '')
    elif any(d.get('basis') == 'unconfirmed' for d in x.get('returns') or []): rc = 'beat (U)'
    else: rc = '—'
    sm = '; '.join(f"{short(s.get('work', ''))} [{BT.get(s.get('borrow_type'), '?')}{'' if s.get('credited', True) else ' (u)'}{SM.get(s.get('status'), '')}]" for s in x.get('samples') or []) or '—'
    rt = (x['runtime_mmss'] + RTS.get(x.get('runtime_status'), '')) if x.get('runtime_mmss') else '?'
    out.append(f"| {r['n']} | {esc(r['title'])} | {rt} | {bpm} | {op} | {hf} | {HK.get(x.get('hook_status'), '?')} | {bs} | {rc} | {sm} | {second} | {path} |")
vn = [(r['n'], r['title'], C.VERSION_NOTES[r['title']]) for r in rows if r['title'] in C.VERSION_NOTES]
out.append('\n**Version notes.** Measurements use the original explicit album or single version except where noted here:')
for n, title, note in vn: out.append(f"- #{n} {title}: {note}")

# ---------------- 4c
out.append('\n## 4c. Close calls and exclusions (genre)\n')
out.append('Every song in the window that was checked as possible rap and either included despite a crossover profile or left out. **Included** = Billboard classified it as rap. **Excluded** = Billboard placed it on Hot R&B Songs or another non-rap chart, which rules out Hot Rap Songs. **Excluded (year-end absence)** = absent from the year-end Hot Rap, Hot R&B/Hip-Hop and Hot R&B lists despite a run that would rank there (strong but indirect). **Excluded (inferred)**, **(inferred from genre)**, **(unresolved)** and **(not searched)** rest on weaker inference or recollection. Every one of these is carried into 4d.\n')
out.append('| First top-10 | Rank | Title | Artists | Decision | Evidence |')
out.append('|---|---|---|---|---|---|')
for o in in_window:
    if not (o['prior'] == 'close' or o['cid'] not in final_ids): continue
    st = status[o['cid']]
    if o['cid'] in final_ids: dec = 'Included (rap)'
    elif st['status'] == 'rap': dec = 'Rap, but outside the 100'
    elif st['status'] == 'unverified': dec = 'Excluded (not searched)' if (ev_best(o['cid']) or {}).get('evidence_type') in ('model_knowledge_only', 'none', None) else 'Excluded (unresolved)'
    elif soft_kind(o) == 'genre': dec = 'Excluded (inferred from genre)'
    elif soft_kind(o) == 'yearend': dec = 'Excluded (year-end absence)'
    elif soft_kind(o) == 'inferred': dec = 'Excluded (inferred)'
    else: dec = 'Excluded'
    b = ev_best(o['cid'])
    full = (b or {}).get('evidence_summary') or ''
    if st['basis'].startswith('Year-End'): basis = st['basis'] + '. ' + full
    elif st['status'] == 'unverified' and b and b.get('evidence_type') not in ('model_knowledge_only', 'none'):
        basis = 'Unresolved (no direct rap/R&B listing), ' + EVLAB.get(b['evidence_type'], b['evidence_type']) + ': ' + full
    elif st['status'] == 'unverified':
        rest = re.sub(r'Not searched[^.]*\.\s*|From memory,?\s*|\bUnverified\.?\s*|The prior expectation, which is not evidence, is that\s*', '', full).strip(' .;')
        basis = 'Model recollection only, not searched. Expected: ' + (rest[:1].lower() + rest[1:] if rest else 'not rap') + '.'
    elif b: basis = EVLAB.get(b['evidence_type'], b['evidence_type']) + ': ' + full
    else: basis = st['basis']
    ye = yearend_links(st['basis'] + ' ' + full)
    lk = ' · '.join(ye) if (ye and (dec.startswith('Included') or dec in ('Excluded (inferred)', 'Excluded (year-end absence)'))) else (f"[{SITE.get(domain(b['source_urls'][0]), 'Billboard' if 'billboard.com' in domain(b['source_urls'][0]) else domain(b['source_urls'][0]))}]({b['source_urls'][0]})" if b and b.get('source_urls') else '')
    out.append(f"| {o['first_top10']} | {o['rank']} | {esc(o['title'])} | {esc(o['artist'])} | {dec} | {short(basis, 300)}{' (' + lk + ')' if lk else ''} |")
out.append('\n**Exclusion audit.** 209 other top-10 songs from the window were pre-tagged non-rap by artist and genre (pop, country, Latin, rock, R&B). A separate audit specifically checked 37 of them (8 searches plus year-end-list and rap-drought reasoning) and flagged none as rap. It left 6 rap-adjacent songs not conclusively checked ("Fancy Like", "Permission To Dance", "My Universe", "Fortnight", "I Had Some Help", "I Ain\'t Coming Back") and did not search the rest, which are plainly non-rap. Those exclusions therefore rest on the genre pre-tag. The audit also documented the reported rap top-10 drought: no hip-hop song reached the top 10 from "What Did I Miss?" (July 2025) until spring 2026, and Billboard reported no rap songs in the top 40 on the charts dated 2025-10-25 and 2025-11-01, a first since 1990.\n')

# ---------------- 4d
out.append('\n## 4d. Boundary and open items\n')
out.append(f"- **#100 is {rows[-1]['title']}** ({rows[-1]['first_top10']}, #{rows[-1]['rank']}). The next rap songs in line are " + '; '.join(S['boundary_next'][:5]) + '.')
if prov:
    out.append('- **Included without direct classification evidence (†):** ' + '; '.join(f"#{r['n']} {r['title']}" for r in prov) + '. Each was pre-tagged rap. A targeted re-check (four searches each) found only indirect evidence: a Hot R&B/Hip-Hop Songs peak, which does not separate rap from R&B, or album-mates on rap charts. If one is not rap, every later song moves up one place and the next song in line enters at #100. One look at Rap Streaming Songs for the release week settles each (2024-04-06 for "Cinderella" and "We Don\'t Trust You", 2024-01-27 for "Nee-nah", 2023-08-12 for "FE!N"). For "FE!N" the re-check is weakly contrary: searches of Rap Streaming Songs pages from August–September 2023 returned other Utopia songs but never FE!N, though search snippets show only partial pages.')
if inf:
    out.append('- **Included by album-mate inference (‡):** ' + '; '.join(f"#{r['n']} {r['title']}" for r in inf) + '. Album-mates from the same release week were on Hot Rap Songs or Rap Streaming Songs, but no retrieved page shows ' + plural(len(inf), 'this title', 'these titles') + ' on a rap chart. For "Reincarnated" the inference is this: on the Hot Rap Songs page dated 2024-12-07, "Man At The Garden" (Hot 100 #9) is a new entry at #7, so six rap songs outranked it, and the six GNX tracks above it on the Hot 100 would be those six (five of them are confirmed rap). That assumes the other songs in the Hot 100 top 8 that week were not rap, which was not checked. The targeted re-check found a Hot R&B/Hip-Hop Songs peak of No. 6 and no Hot Rap Songs row in Wikipedia\'s chart table (search-result summary; see `data/raw/recheck_classification.md`). Reading the full 2024-12-07 Hot Rap Songs page settles it.')
if soft_excl:
    def why(o):
        k = soft_kind(o); b = (ev_best(o['cid']) or {}).get('evidence_summary') or status[o['cid']]['basis']
        if k == 'unresolved': return 'not searched; model recollection only' if (ev_best(o['cid']) or {}).get('evidence_type') in ('model_knowledge_only', 'none', None) else 'unresolved: ' + short(b, 140)
        if k == 'genre': return 'inferred from genre; the Hot Rap Songs page for that week was not checked'
        return short(re.sub(r'^Inferred absence\.\s*', 'inferred absence: ', re.sub(r'^Inferred:\s*', 'inferred: ', b)), 160)
    weak = [o for o in soft_excl if soft_kind(o) != 'yearend']; ye_abs = [o for o in soft_excl if soft_kind(o) == 'yearend']
    out.append('- **Excluded on inference, recollection or unresolved evidence, ranked above the cut** (if any is rap, it enters at its date and rank, and #100 drops out): ' +
               '; '.join(f"{o['first_top10']} #{o['rank']} {o['title']} — {o['artist']} ({why(o)})" for o in weak) + '.')
    if ye_abs:
        out.append('- **Excluded because they are absent from all three year-end genre lists** (Hot Rap, Hot R&B/Hip-Hop and Hot R&B Songs) despite top-10 runs that would rank there: ' +
                   '; '.join(f"{o['first_top10']} #{o['rank']} {o['title']} — {o['artist']}" for o in ye_abs) + '. This is strong but indirect evidence; no weekly rap-chart page was checked for these.')
out.append('- **Newest end.** No rap-classified song is known to have first reached the top 10 between the chart dated 2026-05-30 and the 2026-11-21 starting chart. "Solar Eclipse" (Drake & Don Toliver, 2026-10-17 #5) is R&B-classified (Billboard: a No. 1 debut on Hot R&B Songs) and "Boston" (2026-07-25 #6) is a country song. "Babydoll" (2026-10-24 #10) and "Nicole Kidman" (2026-10-17 #9) are excluded on genre inference only; if either is rap, it becomes #1 or #2 and TSU drops out.')
out.append('- **The cut splits one chart week, as the ordering rule requires.** *Certified Lover Boy* put nine songs in the top 10 on the chart dated 2021-09-18. Ties in a week are broken by position that week, so "TSU" (#9) is #100 and "Love All" (#10) is the first song outside the list.')
out.append('- **No missing chart weeks** were found in the weekly Hot 100 series for the window.')
open(REPO + '04-reference-list.md', 'w').write('\n'.join(out) + '\n')
with open(REPO + 'data/classification_evidence.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['cid', 'first_top10', 'rank', 'title', 'artists', 'prior_tag', 'final_status', 'basis', 'best_evidence_type', 'best_confidence', 'source_urls', 'hot100_rank_reported'])
    for o in cands:
        st = status[o['cid']]; b = ev_best(o['cid']) or {}
        w.writerow([o['cid'], o['first_top10'], o['rank'], o['title'], o['artist'], o['prior'], st['status'], st['basis'], b.get('evidence_type'), b.get('confidence'), ' '.join(b.get('source_urls') or []), b.get('hot100_rank_reported')])
print('rendered', len(rows), 'rows;', len(prov), 'provisional;', len(inf), 'album-mate inferred;', len(soft_excl), 'soft exclusions')
