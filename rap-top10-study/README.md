# Rap Top-10 Studio Study — King D Bird

This study looks at the 100 most recent distinct rap songs to reach the U.S. Billboard Hot 100 top 10. It counts back from the chart dated **2026-11-21**, with a research cutoff of **2026-11-22**. The findings are turned into a process you can follow from the first beat loop to a recorded demo.

## Read in this order (as requested)

1. [`01-studio-process.md`](01-studio-process.md) — the one-page checklist, then each step: an action, what to listen for, and one fix. It shows where verse-led rap, trap and drill differ.
2. [`02-worked-session.md`](02-worked-session.md) — an original bar map on a 144 BPM grid with a 72 BPM feel, with timestamps. It has two openings over the same beat and a listening test for choosing between them.
3. [`03-findings.md`](03-findings.md) — the ranked patterns behind the process. Each gives counts out of the songs assessed, named examples, a way to try it, and an exception. Measured findings and production judgment are labeled separately.
4. [`04-reference-list.md`](04-reference-list.md) — all 100 songs with first top-10 date, rank, genre tag and source, plus the per-track measurements and the close-call log.
5. [`05-codex-handoff.md`](05-codex-handoff.md) — a brief for Codex or a local agent to measure the listening-dependent fields from the audio.

## Capability verdict

**ACE WITH CONDITIONS** for the reference set and the process. **SUPPORT ONLY** for listening-level measurements.

| Area | Status |
|---|---|
| Hot 100 ranks and first top-10 dates | Verified against every weekly chart since 1958, via the `mhollingshead/billboard-hot-100` mirror of billboard.com. No missing weeks in the window. |
| Rap classification | Checked song by song against Billboard evidence: year-end Hot Rap Songs lists, same-week rap or R&B component charts, artist chart histories, Billboard chart reporting. Remaining indirect calls are marked † in the list. |
| Runtime, tempo, samples, credits | From published sources, cross-checked by an independent verifier per album or group. Coverage counts are given with every number. |
| First-vocal entrance, hook timestamps, silence after punchlines, 808 and drum changes | **Not measured.** No audio was available and the lyric-timing hosts were blocked, so these are unknown unless a source documented them. `05-codex-handoff.md` closes this gap. |
| Process, worked session, demo lyrics | Original work. Production judgment is labeled **[J]**. |

## How the study was built (short)

- **Reference set:** first top-10 week per song, from the full weekly Hot 100 history. 155 rap and possible-rap candidates were classified with Billboard evidence. A separate audit checked 209 songs pre-tagged non-rap and found none that Billboard classified as rap.
- **Per-track study:** done album by album, with a hard search budget per agent. Every claim carries a basis: **source** (cited page), **unverified recollection** (reported separately, never counted as measured), or **unknown**. An independent verifier re-checked runtime, tempo, opening/hook claims, beat switches and samples for each group.
- **Tempo:** listed BPMs often disagree by a factor of two, so both are kept. The grid BPM uses the DAW convention; the felt BPM is the rap-bar pulse (half of grid for half-time trap). Felt values not described by a source are labeled genre-convention inference.
- **Environment limits:** the cloud environment's network policy blocked billboard.com, Wikipedia, lyric-timing and audio hosts for direct fetching, and an allowlist change was rejected. Search ran server-side, under a cap of 200 searches per turn, so the work ran in budgeted batches.

## Data files

| File | Contents |
|---|---|
| `data/reference_100.csv` | The 100 songs: date, rank, genre tag, classification basis and sources, chart path (debut or climb, peak, weeks in top 10), album-bomb flag |
| `data/track_measurements.csv` | Per-track measurements and their basis or verification status |
| `data/classification_evidence.csv` | All 155 candidates with final status and best evidence |
| `scripts/` | The scripts used to rebuild the chart history, classify, merge, aggregate and compute the bar map |

## Re-running the study

- `scripts/top10.py` rebuilds the first-top-10 arrivals from the public chart mirror.
- `scripts/aggregate.py` recomputes every count.
- Search-dependent evidence is preserved in the CSVs with source URLs. Re-checking it needs network access to the listed hosts.
