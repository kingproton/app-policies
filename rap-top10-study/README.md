# Rap Top-10 Studio Study — King D Bird

This study looks at the 100 most recent distinct rap songs to reach the U.S. Billboard Hot 100 top 10. It counts back from the chart dated **2026-11-21**, with a research cutoff of **2026-11-22**. The findings are turned into a process you can follow from the first beat loop to a recorded demo.

## Read in this order (as requested)

1. [`01-studio-process.md`](01-studio-process.md) — the one-page checklist, then each step: an action, what to listen for, and one fix. It shows where verse-led rap, trap and drill differ.
2. [`02-worked-session.md`](02-worked-session.md) — an original bar map on a 144 BPM grid with a 72 BPM feel, with timestamps. It has two openings over the same beat and a listening test for choosing between them.
3. [`03-findings.md`](03-findings.md) — the ranked patterns behind the process. Each gives counts out of the songs assessed, named examples with timestamps, a way to try it, and an exception. Measured findings, documented findings and production judgment are labeled separately.
4. [`04-reference-list.md`](04-reference-list.md) — all 100 songs with first top-10 date, rank, genre tag and source, the per-track measurements, the documented facts and the close-call log.
5. [`05-measurement-method.md`](05-measurement-method.md) — how each measurement was made, how it was checked, and where it stops.

## Capability verdict

**ACE WITH CONDITIONS.** The reference list, the process, the worked session and the measurements are complete and usable. The conditions are stated limits, not missing work: the list is provisional at the margins, and three listening-level details could not be measured.

| Area | Status |
|---|---|
| Hot 100 first top-10 dates | **Verified** for 100 of 100 against Wikipedia's yearly top-ten lists. |
| Hot 100 ranks | **Verified** for 51 of the 51 list songs whose chart week Billboard Canada hosts (from 2023-09-02). The other 49 ranks come from the weekly mirror, which matches Billboard Canada in 161 of 162 hosted weeks. |
| Rap classification | **86 of 100** rest on a Billboard rap-chart figure read directly from a table. **14** (all Drake album cuts, marked †) rest on Billboard pages known only through search summaries. No dispute found changes the list; see `04-reference-list.md`, 4e. |
| Runtime | **Measured** for 96 from the Apple catalog; cited for the other 4. |
| Felt tempo (half or full time) | **Measured** from 30-second clips: 72 of 96 clear, 17 resolved with a caveat, 7 open, 4 without a clip. |
| First vocal line, first hook, hook order, section sizes, density | **Measured** for 98 tracks from time-synced lyric records. 76 were read twice (a repetition detector and an AI reader) and ruled on by a second AI reader where the two disagreed; 22 rest on the detector alone. Good to about a second. |
| Samples, openings, beat switches, how records were made | **Documented.** Earlier claims were re-checked against saved Wikipedia and Songfacts page text; only supported ones are counted. |
| Silence after punchlines, ad-lib placement in the bar, drum and 808 changes on return | **Not measured.** Line-level lyric timing and a 30-second clip cannot show them. They stay unknown. |
| Process, worked session, demo lyrics | Original work. Production judgment is labeled **[J]**. |

**What I could not verify:** `www.billboard.com` was not read, because its robots.txt bars Anthropic's agents. Billboard chart pages are therefore cited, not opened. The licensed Billboard Canada pages, which you named as the starting issue, were read instead.

## How the study was built (short)

- **Reference set:** first top-10 week per song, from the full weekly Hot 100 history.
  - 155 rap and possible-rap candidates were checked song by song. Full year-end Hot Rap Songs lists for 2021–2025 and the Hot Rap Songs columns of 28 artist discography tables were then read directly and applied.
  - 209 other top-10 songs were pre-tagged non-rap by artist and genre. A separate audit checked 37 of them and flagged none as rap; none of the excluded songs appears on any year-end rap list.
- **Measurements (2026-11-25):** Apple catalog durations and preview clips, and LRCLIB time-synced lyric records. No lyric text and no audio is stored; only derived numbers are.
  - Felt tempo comes from a backbeat estimator that was tested on 24 synthetic drum patterns before use.
  - Lyric structure was read twice per track, by a repetition detector and by an independent AI reader, with a second AI reader ruling on disagreements.
  - Nobody listened to the recordings and no person read the lyric records or pages. The checks are machine checks, described in file 05.
- **Documented facts:** the earlier search-based research recorded claims with a basis code. In this pass every claim was checked against saved page text, and a skeptic re-checked every verdict. Basis codes: **P** page text supports it; **S** cited source, not rejected; **U** not confirmed (never counted); **R** recollection (never counted).
- **Review:** each stage was re-checked by independent agents told to refute it, and the corrections are applied in `scripts/corrections.py`.

## Data files

| File | Contents |
|---|---|
| `data/reference_100.csv` | The 100 songs: date, rank, genre tag, classification basis, evidence tier and sources, chart path (debut or climb, peak, weeks in top 10), album-bomb flag |
| `data/track_measurements.csv` | Per-track documented facts with basis codes, and the measured columns (`m_…`): runtime, grid and felt tempo, first line, hook timing, section lengths, density |
| `data/classification_evidence.csv` | All 155 candidates with final status, evidence tier, year-end ranks and discography rap peaks |
| `data/measured/` | Derived measurement data: chart checks, Wikipedia list transcriptions, genre tables, Apple catalog matches, lyric structure (detector and review), audio feel, page-claim verdicts |
| `data/raw/` | Frozen research data from the search-based pass, plus the computed statistics (`findings_stats.json`, `measured_stats.json`) |
| `scripts/` | The build: classification, merges, statistics and renderers. `scripts/measure/` holds the fetch and measurement scripts. `scripts/corrections.py` holds every hand-coded correction |
| `templates/` | The document templates. Every figure in files 01, 03 and 05 and in this README is filled in from the statistics by `scripts/render_docs.py` |

## Re-running the study

- `scripts/run_all.sh` rebuilds `04-reference-list.md`, the CSVs and the statistics from `data/raw/` and `data/measured/`. `scripts/render_docs.py` then fills the templates.
- `scripts/measure/` re-fetches and re-measures (see `05-measurement-method.md` for the order). Downloads go to a working directory that is not committed.
- `scripts/fetch_charts.py` downloads the weekly Hot 100 history (about 44 MB, not committed). Then `top10.py`, `candidates.py` and `chartmetrics.py` rebuild the chart dates, ranks and chart paths.
- `scripts/collect.py` is not re-runnable outside the original session: it read that session's research journals. Its output is frozen in `data/raw/collected.json`.
