"""Render 04-reference-list.md from final_rows.json, tracks_merged.json, classification evidence and chart metrics."""
import json, re, os, csv
SP = '/tmp/claude-0/-home-user-app-policies/08207d95-5f38-5913-acec-14c31ee115ad/scratchpad/'
REPO = '/home/user/app-policies/rap-top10-study/'
rows = json.load(open(SP + 'data/final_rows.json'))
t = {int(k): v for k, v in json.load(open(SP + 'data/tracks_merged.json')).items()}
status = {r['cid']: r for r in json.load(open(SP + 'data/classification_status.json'))}
col = json.load(open(SP + 'data/collected.json'))
S = json.load(open(SP + 'data/stats.json'))
cands = json.load(open(SP + 'data/to_verify.json'))
def esc(s): return (s or '').replace('|', '/').replace('\n', ' ')
def ev_best(cid):
    ev = col['classify'].get(str(cid), [])
    ev = sorted(ev, key=lambda e: ({'high': 3, 'medium': 2, 'low': 1}.get(e['confidence'], 0), e['evidence_type'] != 'model_knowledge_only'))
    return ev[-1] if ev else None
def src_link(r):
    cid = r['cid']; st = status[cid]
    chart = f"[Hot 100 {r['first_top10']}](https://www.billboard.com/charts/hot-100/{r['first_top10']}/)"
    if st['basis'].startswith('Year-End'):
        yr = re.search(r'(\d{4})', st['basis']).group(1); rk = re.search(r'#(\d+)', st['basis'])
        g = f"[YE Hot Rap Songs {yr}{' #' + rk.group(1) if rk else ''}](https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_Rap_Songs_of_{yr})"
    else:
        b = ev_best(cid)
        if b and b.get('source_urls'):
            lab = {'billboard_chart_page': 'Billboard chart page', 'billboard_article': 'Billboard report', 'wikipedia_chart_table': 'Wikipedia chart table', 'other_press': 'press citing Billboard', 'model_knowledge_only': 'unverified', 'none': 'unverified'}.get(b['evidence_type'], b['evidence_type'])
            g = f"[{lab}]({b['source_urls'][0]})"
        else: g = 'genre unverified'
    return chart + ' · ' + g
out = []
out.append('# 4 — Full reference list (100 songs)\n')
out.append(f"**Reference window:** first Hot 100 top-10 weeks from the chart dated **{S['span'].split(' to ')[1]}** back to **{S['span'].split(' to ')[0]}**. That is the 100 most recent distinct rap songs, counting back from the chart dated 2026-11-21 (research cutoff 2026-11-22).\n")
out.append("**Ordering rule:** by the chart week each song *first* reached positions 1–10, newest first. Ties within a week are sorted by position that week. Each song is counted once. Billboard's combined credits and remixes are followed, so Billboard's mid-run re-credit of \"Carnival\" from Kanye West to Ye counts as one song.\n")
out.append("**Genre rule:** rap = Billboard placed the song on Hot Rap Songs or on a rap-only component chart (Rap Streaming Songs, Rap Airplay), or Billboard reporting says so. Hot R&B Songs and Hot Rap Songs are mutually exclusive halves of Hot R&B/Hip-Hop Songs, so R&B-classified songs by rappers are excluded and logged below.\n")
out.append("**Rank and date source:** every weekly Hot 100 chart since 1958, from the public `mhollingshead/billboard-hot-100` mirror of billboard.com. It has no missing weeks since 2015. All 155 candidate dates and ranks were re-derived from the weekly charts. Billboard and press reporting confirmed the rank in a sample of weeks (see `data/classification_evidence.csv`).\n")
prov = [r for r in rows if 'provisional' in r['classification']]
out.append(f"**Status: {'PROVISIONAL' if prov else 'FINAL'}.** {len(prov)} entries are counted as rap from strong but indirect evidence; they are marked † in the table. See *Boundary and open items* at the end.\n")
out.append('\n## 4a. The list\n')
out.append('| # | Title | Credited artists | First top-10 chart | Rank that week | Genre tag | Source |')
out.append('|---|---|---|---|---|---|---|')
for r in rows:
    mark = ' †' if 'provisional' in r['classification'] else ''
    out.append(f"| {r['n']} | {esc(r['title'])}{mark} | {esc(r['artists'])} | {r['first_top10']} | {r['rank']} | {esc(r['genre_tag'])} | {src_link(r)} |")
out.append('\n## 4b. Per-track measurements used in the findings\n')
out.append("Version = the original explicit album or single version unless noted. Basis codes: **S** = a cited source; **R** = unverified recollection (reported separately, never counted as measured); **?** = unknown. Tempo status: ✔ = an independent verifier agreed; ✎ = the verifier corrected the value; ⚠ = sources conflict; · = one source or the tempo sweep only. \"Path\" = whether the song **D**ebuted in the top 10 or **C**limbed in from a lower position; wk = weeks in the top 10.\n")
out.append('| # | Title | Runtime | Grid / felt BPM | Opening | Hook-first | Hook | Beat switch | Samples / interpolations | Path |')
out.append('|---|---|---|---|---|---|---|---|---|---|')
code = {'source': 'S', 'unverified_recollection': 'R', 'unknown': '?', None: '?'}
tst = {'verified': '✔', 'corrected_by_verifier': '✎', 'conflict': '⚠', 'research_only': '·', 'tempo_sweep': '·', 'verifier_could_not_confirm': '·'}
hk = {'present_verified': 'yes (S)', 'present_unverified': 'yes (R)', 'absent_verified': 'none (S)', 'absent_unverified': 'none (R)', 'unknown': '?', None: '?'}
for r in rows:
    x = t.get(r['cid'])
    path = ('D' if r['debut_in_top10'] else f"C from #{r['climbed_from']}") + f", {r['weeks_in_top10']} wk"
    if not x:
        out.append(f"| {r['n']} | {esc(r['title'])} | not studied | | | | | | | {path} |"); continue
    bpm = f"{x['grid_bpm']:g} / {x['felt_bpm']:g} {tst.get(x['tempo_status'], '·')}" if x.get('grid_bpm') and x.get('felt_bpm') else '?'
    op = f"{(x['opening_element'] or 'unknown').replace('_', ' ')} ({code.get(x['opening_basis'], '?')})" if x.get('opening_element') not in (None, 'unknown') else '?'
    hf = f"{x['hook_first']} ({code.get(x['hook_first_basis'], '?')})" if x.get('hook_first') not in (None, 'unknown') else '?'
    bs = f"{x['beat_switch']} ({code.get(x['beat_switch_basis'], '?')})" + (f" @{re.match(r'[~≈]?[0-9:.]+', x['beat_switch_time']).group(0) if re.match(r'[~≈]?[0-9:.]+', x['beat_switch_time']) else ''}" if x.get('beat_switch_time') else '') if x.get('beat_switch') not in (None, 'unknown') else '?'
    sm = '; '.join(esc(s.get('work', ''))[:60] for s in x.get('samples') or [])[:140] or '—'
    rt = (x.get('runtime_mmss') or '?') + (' ✔' if x.get('runtime_status') == 'verified' else ' ✎' if x.get('runtime_status') == 'corrected_by_verifier' else '')
    out.append(f"| {r['n']} | {esc(r['title'])} | {rt} | {bpm} | {op} | {hf} | {hk.get(x.get('hook_status'), '?')} | {bs} | {sm} | {path} |")
# close calls
out.append('\n## 4c. Close calls and exclusions (genre)\n')
out.append('Songs that reached the top 10 inside the window and were checked as possible rap. **Included** = Billboard classified it as rap despite a crossover profile. **Excluded** = Billboard placed it on Hot R&B Songs or another non-rap chart, or on no R&B/Hip-Hop chart at all.\n')
out.append('| First top-10 | Title | Artists | Decision | Evidence |')
out.append('|---|---|---|---|---|')
final_ids = {r['cid'] for r in rows}
cut_date = rows[-1]['first_top10']
for o in cands:
    if o['prior'] != 'close': continue
    if o['first_top10'] < cut_date: continue
    st = status[o['cid']]
    dec = 'Included (rap)' if o['cid'] in final_ids else ('Excluded' if st['status'] == 'not_rap' else ('Excluded (inferred — see note)' if st['status'] == 'unverified' else 'Rap, but outside the 100' if st['status'] == 'rap' else st['status']))
    b = ev_best(o['cid'])
    evs = esc(st['basis'])[:230]
    url = (b or {}).get('source_urls', [''])[0] if b and b.get('source_urls') else ''
    out.append(f"| {o['first_top10']} | {esc(o['title'])} | {esc(o['artist'])} | {dec} | {evs}{' ([src](' + url + '))' if url else ''} |")
out.append('\n**Exclusion audit.** A separate check covered 209 top-10 songs from the same window that were pre-tagged non-rap (pop, country, Latin, rock, R&B). It found none that Billboard classified as rap. It also documented the reported rap top-10 drought: no hip-hop song reached the top 10 from "What Did I Miss?" (July 2025) until spring 2026, and Billboard reported no rap songs in the top 40 on the charts dated 2025-10-25 and 2025-11-01, a first since 1990.\n')
# boundary
out.append('\n## 4d. Boundary and open items\n')
out.append(f"- **#100 is {rows[-1]['title']}** ({rows[-1]['first_top10']}, #{rows[-1]['rank']}). The next rap songs in line are " + '; '.join(S['boundary_next'][:5]) + '.')
if prov:
    out.append('- **Provisional (†):** ' + '; '.join(f"#{r['n']} {r['title']}" for r in prov) + '. Each is counted as rap from strong but indirect evidence: album-mates on rap charts, rap component charts, or Billboard rap chart-history pages. If any one is reclassified, every later song moves up one place, and the next song in line enters at #100.')
if S.get('open_close_calls_before_cut'):
    out.append('- **Unresolved close calls ranked above the cut** (treated as not rap on indirect evidence; if any were rap, #100 would drop out): ' + '; '.join(S['open_close_calls_before_cut']) + '.')
out.append('- **Newest end.** No rap-classified song first reached the top 10 between the chart dated 2026-05-30 and the 2026-11-21 starting chart. The only rap-artist top-10 arrival in that span, "Solar Eclipse" (Drake & Don Toliver, first top 10 on 2026-10-17 at #5), is R&B-classified: Billboard reported it debuting at No. 1 on Hot R&B Songs.')
out.append('- **The cut splits one chart week, as the ordering rule requires.** *Certified Lover Boy* put nine songs in the top 10 on the chart dated 2021-09-18. Ties in a week are broken by position that week, so "TSU" (#9) is #100 and "Love All" (#10) is the first song outside the list.')
out.append('- **No missing chart weeks** were found in the weekly Hot 100 series for the window.')
open(REPO + '04-reference-list.md', 'w').write('\n'.join(out) + '\n')
# evidence CSV
with open(REPO + 'data/classification_evidence.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['cid', 'first_top10', 'rank', 'title', 'artists', 'prior_tag', 'final_status', 'basis', 'best_evidence_type', 'best_confidence', 'source_urls', 'hot100_rank_reported'])
    for o in cands:
        st = status[o['cid']]; b = ev_best(o['cid']) or {}
        w.writerow([o['cid'], o['first_top10'], o['rank'], o['title'], o['artist'], o['prior'], st['status'], st['basis'], b.get('evidence_type'), b.get('confidence'), ' '.join(b.get('source_urls') or []), b.get('hot100_rank_reported')])
print('rendered', len(rows), 'rows;', len(prov), 'provisional')
