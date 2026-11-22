# Rap Top-10 Studio Study — King D Bird

This study looks at the 100 most recent distinct rap songs to reach the U.S. Billboard Hot 100 top 10. It counts back from the chart dated **2026-11-21**, with a research cutoff of **2026-11-22**. The findings are turned into a process you can follow from the first beat loop to a recorded demo.

## Read in this order (as requested)

1. [`01-studio-process.md`](01-studio-process.md) — the one-page checklist, then each step: an action, what to listen for, and one fix. It shows where verse-led rap, trap and drill differ.
2. [`02-worked-session.md`](02-worked-session.md) — an original bar map on a 144 BPM grid with a 72 BPM feel, with timestamps. It has two openings over the same beat and a listening test for choosing between them.
3. [`03-findings.md`](03-findings.md) — the ranked patterns behind the process. Each gives counts out of the songs assessed, named examples, a way to try it, and an exception. Measured findings and production judgment are labeled separately.
4. [`04-reference-list.md`](04-reference-list.md) — all 100 songs with first top-10 date, rank, genre tag and source, plus the per-track measurements and the close-call log.
5. [`05-codex-handoff.md`](05-codex-handoff.md) — a brief for Codex or a local agent to measure the listening-dependent fields from the audio.

## Capability verdict

**ACE WITH CONDITIONS** for the reference set and the process. The list is marked provisional, because 17 genre calls rest on indirect evidence: 5 inclusions and 12 exclusions ranked above the cut (see `04-reference-list.md`, 4d). **SUPPORT ONLY** for listening-level measurements.

| Area | Status |
|---|---|
| Hot 100 ranks and first top-10 dates | Verified against every weekly chart since 1958, via the `mhollingshead/billboard-hot-100` mirror of billboard.com. No missing weeks in the window. |
| Rap classification | Checked song by song against Billboard evidence: year-end Hot Rap Songs lists, same-week rap or R&B component charts, artist chart histories, Billboard chart reporting. 95 of the 100 have direct evidence. 4 rest on indirect evidence (†) and 1 on album-mates (‡). 12 exclusions above the cut rest on inference or indirect evidence; 6 of those rest on absence from all three year-end genre lists, which is strong but indirect. Most direct evidence was read from search-result summaries, because billboard.com could not be opened from this environment. |
| Runtime, tempo, samples, credits | From published sources, cross-checked by an independent verifier per album or group. A claim the verifier could not support is kept as **U** and never counted as sourced. Coverage counts are given with every number. |
| First-vocal entrance, hook timestamps, silence after punchlines, 808 and drum changes | **Not measured.** No audio was available and the lyric-timing hosts were blocked, so these are unknown unless a source documented them. `05-codex-handoff.md` closes this gap. |
| Process, worked session, demo lyrics | Original work. Production judgment is labeled **[J]**. |

## How the study was built (short)

- **Reference set:** first top-10 week per song, from the full weekly Hot 100 history.
  - 155 rap and possible-rap candidates were checked. 138 were resolved from chart evidence (109 rap, 29 not rap), and 17 are unverified: 4 counted in the 100 and marked †, 2 exclusions above the cut, and 11 below the cut, where they cannot change the list.
  - A targeted re-check of the 18 weakest calls settled 10 of them.
  - 209 other top-10 songs were pre-tagged non-rap by artist and genre. A separate audit specifically checked 37 of them and flagged none as rap. It left 6 rap-adjacent songs not conclusively checked and did not search the rest, which are plainly non-rap (see 4c).
- **Per-track study:** done album by album, with a hard search budget per agent.
  - Every claim carries a basis: **source** (cited page), **U** (cited, but the verifier could not find support), **unverified recollection**, or **unknown**. Only "source" counts as measured.
  - An independent verifier re-checked runtime, tempo, opening/hook claims, beat switches and samples for each group; its rejections are applied in `scripts/track_merge.py` from `scripts/corrections.py`.
  - Later gap sweeps filled missing fields with their own citations. A separate pass re-checked all 41 sweep structure claims: 29 confirmed; the rest were dropped to U, except two corrected codes.
- **Tempo:** listed BPMs often disagree by a factor of two, so both readings are kept. The grid BPM uses the DAW convention; the felt BPM is the rap-bar pulse (half of grid for half-time trap). No source describes the felt pulse of any track, so every felt value is a genre-convention inference (labeled in the data).
- **Environment limits:** the cloud environment's network policy blocked billboard.com, Wikipedia, lyric-timing and audio hosts for direct fetching, and an allowlist change was rejected. Search ran server-side, under a cap of 200 searches per turn, so the work ran in budgeted batches.

## Data files

| File | Contents |
|---|---|
| `data/reference_100.csv` | The 100 songs: date, rank, genre tag, classification basis and sources, chart path (debut or climb, peak, weeks in top 10), album-bomb flag |
| `data/track_measurements.csv` | Per-track measurements with basis codes, verifier status, borrowing type and status, return-change type, chart path, version notes |
| `data/classification_evidence.csv` | All 155 candidates with final status and best evidence |
| `data/raw/` | Frozen research data: `collected.json` (every research, verifier, sweep and classification record), `tracks_merged.json`, `classification_status.json`, `to_verify.json`, `chart_metrics.json`, `final_rows.json`, `stats.json`, `findings_stats.json`, plus the two re-check reports (`recheck_classification.md`, `recheck_sweep_claims.md`) |
| `scripts/corrections.py` | Every hand-coded correction (verifier rejections, credit fixes, tempo outliers, classification overrides, return-change coding), each traceable to a verifier flag or a review issue |
| `scripts/` | The scripts that rebuild the chart history, classify, merge, aggregate, render the tables and compute the bar map |

## Re-running the study

- `scripts/run_all.sh` re-runs the analysis from the frozen data in `data/raw/`. It regenerates `04-reference-list.md`, the CSVs, `findings_stats.json` (the counts in `03-findings.md`), the counts table and the bar-map tables in `02-worked-session.md`.
- `scripts/fetch_charts.py` downloads the weekly Hot 100 history (about 44 MB, not committed). Then `top10.py`, `candidates.py` and `chartmetrics.py` rebuild the chart dates, ranks and chart paths.
- `scripts/collect.py` is not re-runnable outside this session: it read the workflow journals. Its output is frozen in `data/raw/collected.json`.
- Search-dependent evidence is preserved with source URLs. Re-checking it needs network access to the listed hosts. billboard.com and wikipedia.org could not be opened from this environment.
