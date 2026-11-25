# Rap Top-10 Studio Study — King D Bird

This study looks at the 100 most recent distinct rap songs to reach the U.S. Billboard Hot 100 top 10. It counts back from the chart dated **2026-11-21**, with a research cutoff of **2026-11-22**. The findings are turned into a process you can follow from the first beat loop to a recorded demo.

## Read in this order (as requested)

1. [`01-studio-process.md`](01-studio-process.md) — the one-page checklist, then each step: an action, what to listen for, and one fix. It shows where verse-led rap, trap and drill differ.
2. [`02-worked-session.md`](02-worked-session.md) — an original bar map on a 144 BPM grid with a 72 BPM feel, with timestamps. It has two openings over the same beat and a listening test for choosing between them.
3. [`03-findings.md`](03-findings.md) — the ranked patterns behind the process. Each gives counts out of the songs assessed, named examples with timestamps, a way to try it, and an exception. Measured findings, documented findings and production judgment are labeled separately.
4. [`04-reference-list.md`](04-reference-list.md) — all 100 songs with first top-10 date, rank, genre tag and source, the per-track measurements, the documented facts and the close-call log.
5. [`05-measurement-method.md`](05-measurement-method.md) — how each measurement was made, how it was checked, and where it stops.

## Capability verdict

**ACE WITH CONDITIONS.** The reference list, the process, the worked session and the measurements are complete and usable. The conditions are stated limits, not missing work: the list is provisional at the margins, and the listening-level details in the *Not measured* row below could not be measured.

| Area | Status |
|---|---|
| Hot 100 first top-10 dates | **Verified** for {{ w_match() }} of {{ g('all','n_songs') }} against Wikipedia's yearly top-ten lists. |
| Hot 100 ranks | **Verified** for {{ cc('billboard_canada','match') }} of the {{ bc_hosted() }} list songs whose chart week Billboard Canada hosts (from {{ cv_first() }}). The other {{ 100 - bc_hosted() }} ranks come from the weekly mirror, which matches Billboard Canada in {{ cv_full() }} of {{ cv_weeks() }} hosted weeks ({{ cv_all100() }} on every title, {{ cv_one_off() }} with one title spelled differently). |
| Rap classification | **{{ tier('table') }} of 100** rest on a Billboard rap-chart figure read directly from a table. **{{ tier('summary') }}** (all Drake album cuts, marked †) rest on Billboard pages known only through search summaries. No dispute found changes the list. Above the cut, {{ n_indirect() }} excluded candidates rest on indirect evidence and {{ n_yearend() }} on a deduction from year-end lists; see `04-reference-list.md`, 4d and 4e. |
| Runtime | **Measured** for {{ top('runtime_basis')['catalog'] }} from the Apple catalog; cited for the other {{ top('runtime_basis').get('cited', 0) }}. |
| Felt tempo (half or full time) | **Measured** from 30-second clips: {{ g('all','feel_basis')['M'] }} of {{ g('all','n_clip') }} clear, {{ g('all','feel_basis').get('L',0) + g('all','feel_basis').get('I',0) }} resolved with a caveat, {{ g('all','feel_basis').get('?',0) }} open, {{ cnt('clip_missing') }} without a clip. |
| First lyric line, first hook, hook order, section sizes, density | **Measured** for {{ g('all','n_lyric') }} tracks from time-synced lyric records (density for {{ g('all','verse_sylls_per_s')['n'] }}; section sizes in felt bars for the {{ min(g('all','hook1_len_bars_map')['n'], g('all','first_verse_len_bars')['n'], g('all','intro_len_bars')['n']) }} to {{ max(g('all','hook1_len_bars_map')['n'], g('all','first_verse_len_bars')['n'], g('all','intro_len_bars')['n']) }} that also have a resolved felt tempo). {{ 'Each was' if not detector_only() else str(read_twice()) + ' were' }} read twice (a repetition detector and an AI reader) and ruled on by a second AI reader where the two disagreed. A second, separate run of that reading agrees on the first hook within 2.5 seconds for {{ sr('first_hook') }}. Good to about a second. The first line is the first *transcribed* line, which is not always the lead artist. |
| Samples, openings, beat switches, how records were made | **Documented.** Earlier claims were re-checked against saved Wikipedia and Songfacts page text. A claim counts if the page text supports it (P), or if the pages are silent and its cited source, known only through a search summary, was not rejected (S). The S share is small: {{ bs_n() - bs_page_n() }} of {{ bs_n() }} beat switches and {{ num(fs('all','borrow_documented')) - num(fs('all','borrow_page')) }} of {{ num(fs('all','borrow_documented')) }} songs with a borrowing. |
| Phrase and rhyme placement against the drums, silence after punchlines, ad-lib placement, layer changes on return, which change is audible | **Not measured:** {{ UNMEASURED() }}. Line-level lyric timing and a 30-second clip cannot show them, and nobody listened to the recordings. They stay unknown. |
| Process, worked session, demo lyrics | Original work. Production judgment is labeled **[J]**. |

**What I could not verify:** `www.billboard.com` was not read, because its robots.txt bars Anthropic's agents. Billboard chart pages are therefore cited, not opened. The licensed Billboard Canada pages, which you named as the starting issue, were read instead.

## How the study was built (short)

- **Reference set:** first top-10 week per song, from the full weekly Hot 100 history.
  - {{ n_candidates() }} rap and possible-rap candidates were checked song by song. Full year-end Hot Rap Songs lists for 2021–2025 and the Hot Rap Songs columns of artist discography tables ({{ dash_read() }} pages read, {{ dash_tables() }} with a rap column, {{ n_rap_tables() }} of them listing a top-10 arrival) were then read directly and applied.
  - 209 other top-10 songs were pre-tagged non-rap by artist and genre. A separate audit checked 37 of them and flagged none as rap; none of the excluded songs appears on any year-end rap list.
- **Measurements (2026-11-25):** Apple catalog durations and preview clips, and LRCLIB time-synced lyric records. No lyric text and no audio is stored; only derived numbers are.
  - Felt tempo comes from a backbeat estimator that was tested on {{ synth('patterns') }} synthetic drum patterns before use ({{ synth('correct') }} read correctly).
  - Lyric structure was read twice{{ ' per track' if not detector_only() else ' for ' + str(read_twice()) + ' tracks' }}, by a repetition detector and by an independent AI reader, with a second AI reader ruling on disagreements. The whole reading was run a second time by separate agents as a consistency check.
  - Nobody listened to the recordings and no person read the lyric records or pages. The checks are machine checks, described in file 05.
- **Documented facts:** the earlier search-based research recorded claims with a basis code. In this pass every claim was checked against saved page text, and a skeptic re-checked every verdict that asserted support or contradiction ({{ cs('sent_to_skeptic') }} of {{ cs('claims') }}; the rest were "not addressed", one reader's call). Basis codes: **P** after the skeptic's check, the page states the fact or names the work (a supported verdict, a partly supported one whose quoted words are on the page, a new page statement, or a claim recoded to what the page states); **S** cited source known through a search summary, not rejected; **U** not confirmed (never counted); **R** recollection (never counted).
- **Review:** each stage was re-checked by independent agents told to refute it, and the corrections are applied in `scripts/corrections.py`.

## Data files

| File | Contents |
|---|---|
| `data/reference_100.csv` | The 100 songs: date, rank, genre tag, classification basis, evidence tier and sources, chart path (debut or climb, peak, weeks in top 10), album-bomb flag |
| `data/track_measurements.csv` | Per-track documented facts with basis codes, and the measured columns (`m_…`): runtime, `m_grid_bpm` and `m_felt_bpm` (`m_pulse_bpm` is the raw detected pulse; the grid is the larger of pulse and felt), first line, hook timing, section order and lengths, density, and the second-run check. Columns without the `m_` prefix (`grid_bpm`, `felt_bpm`, `hook_before_first_verse`, …) are the earlier search-based research values, not measurements |
| `data/classification_evidence.csv` | All {{ n_candidates() }} candidates with final status, evidence tier, year-end ranks and discography rap peaks |
| `data/measured/` | Derived measurement data: chart checks, Wikipedia list transcriptions, genre tables, discography dash conflicts, Apple catalog matches, lyric structure (detector, review and the second review run), audio feel and the synthetic-pattern test, page-claim verdicts |
| `data/raw/` | Frozen research data from the search-based pass, plus the computed statistics (`findings_stats.json`, `measured_stats.json`) |
| `scripts/` | The build: classification, merges, statistics and renderers. `scripts/measure/` holds the fetch and measurement scripts. `scripts/corrections.py` holds every hand-coded correction |
| `templates/` | The document templates. Counts and medians in files 01, 02, 03 and 05 and in this README are filled in from the statistics by `scripts/render_docs.py`, and named examples are guarded: the build stops if the data no longer supports one. The exceptions are the sizes of the earlier pass's exclusion audit (209 pre-tagged songs, 37 audited), which are typed because that pass's candidate file is not committed |

## Re-running the study

- `scripts/run_all.sh` rebuilds `04-reference-list.md`, the CSVs and the statistics from `data/raw/` and `data/measured/`. `scripts/render_docs.py` then fills the templates.
- `scripts/measure/` re-fetches and re-measures (see `05-measurement-method.md` for the order and arguments). Downloads go to a working directory that is not committed. The AI-agent steps (the lyric reading and the page check) are not re-runnable from the repository; their outputs are frozen in `data/measured/`.
- `scripts/fetch_charts.py` downloads the weekly Hot 100 history (about 44 MB, not committed). Then `top10.py`, `candidates.py` and `chartmetrics.py` rebuild the chart dates, ranks and chart paths.
- `scripts/collect.py` is not re-runnable outside the original session: it read that session's research journals. Its output is frozen in `data/raw/collected.json`.
