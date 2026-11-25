# 5 — How the measurements were made

This file says what was measured, from what, how it was checked, and where it stops. All of it was done inside this study on 2026-11-25.

**Who did the reading.** Nobody listened to the recordings, and no person read the lyric records or the pages. "Reader", "second reader" and "skeptic" below are separate AI agents run inside this study, each given only the files and rules for its step. Their agreement is a consistency check, not a human one.

## What was measured

| Measure | Source read | Method | Coverage of the 100 | Check |
|---|---|---|---|---|
| First top-10 date and rank | Weekly Hot 100 mirror; Billboard Canada chart pages; Wikipedia yearly top-ten lists | First week in positions 1–10, per song | 100 | Date matches Wikipedia for {{ cc('wikipedia_entry_date','match') }}; date and rank match Billboard Canada for {{ cc('billboard_canada','match') }} of the {{ bc_hosted() }} songs whose week is hosted |
| Rap classification | Wikipedia's year-end Hot Rap Songs lists (2021–2025) and Hot Rap Songs peak columns in {{ n_rap_tables() }} artist discography tables | A number on either is a Billboard rap-chart figure | {{ tier('table') }} from tables; {{ tier('summary') }} from search summaries of Billboard pages | Column identity is taken from each table header's link, not its position |
| Runtime | Apple catalog (public search API) | Duration of the track matched by title and artist | {{ top('runtime_basis')['catalog'] }} ({{ top('runtime_basis').get('cited',0) }} more from cited sources) | Within 2 s of the earlier cited runtime in {{ top('runtime_vs_earlier')['within_2s'] }} of {{ top('runtime_vs_earlier')['n'] }} comparable tracks |
| Grid and felt tempo | Apple's 30-second preview clip | Backbeat template on drum onsets (below) | {{ g('all','n_clip') }} clips: {{ g('all','feel_basis')['M'] }} clear, {{ g('all','feel_basis').get('L',0) }} leaning, {{ g('all','feel_basis').get('I',0) }} by range, {{ g('all','feel_basis').get('?',0) }} open | 24 of 24 synthetic drum patterns; pulse agrees with an earlier BPM listing for {{ top('pulse_vs_listings')['agree'] }} of {{ top('pulse_vs_listings')['agree'] + top('pulse_vs_listings')['disagree'] }} |
| First lyric line, first hook, hook count | LRCLIB time-synced lyric record matching the track's length within 3 s | Repetition detector plus an independent read; a second reader rules on disagreements | {{ g('all','n_lyric') }} | Two readings per track; matching records agree on the first line within 1 s for {{ ra('first_line_within_1s') }} |
| Section map (intro, verses, hooks, bridge) | Same record | The independent reader's coarse map | {{ g('all','n_section_map') }} | One reader; lengths in bars need a resolved felt tempo |
| Verse and hook density | Same record | Words and estimated syllables per second inside the detector's sections | {{ g('all','verse_sylls_per_s')['n'] }} | Medians only; single tracks can be off by about 10% |
| Documented facts (samples, openings, beat switches, how it was made) | Saved text of {{ top('claims_summary')['run']['wikipedia_pages'] }} Wikipedia articles and {{ top('claims_summary')['run']['songfacts_pages'] }} Songfacts pages | A reader rules on each earlier claim against the page text; a skeptic re-checks; every quote is matched mechanically | {{ top('claims_summary')['tracks'] }} tracks, {{ top('claims_summary')['claims'] }} claims | Counted only if the skeptic upheld it and the quote is in the saved page |

## Sources and access

- **Read directly:** `ca.billboard.com` (Billboard Canada's licensed chart pages and syndicated Chart Beat articles), `en.wikipedia.org`, `itunes.apple.com` and its preview host, `lrclib.net`, `www.songfacts.com`. Each site's robots.txt was read first, requests were spaced, and a plain client name was sent.
- **Not read:** `www.billboard.com`. Its robots.txt bars Anthropic's agents from everything except two sections. Billboard chart pages and reports cited in this study are known through web-search summaries from the earlier pass, and are labelled that way. You can remove that host from the environment's allowed list.
- **Kept out of the repository:** lyric text, audio, and raw page downloads. The repository holds derived numbers and labels only (`data/measured/`). Short quotes from pages are kept for verification, trimmed to 30 words for Wikipedia and 12 for Songfacts.

## Chart dates and ranks

- The weekly mirror gives every Hot 100 chart since 1958. Billboard Canada hosts {{ cv_weeks() }} chart weeks from {{ cv_first() }} to {{ cv_last() }}, including your starting issue. In {{ cv_full() }} of them all 100 titles match the mirror position for position (two weeks differ by a title spelling), and the 25 rows per page that show last week, peak and weeks on chart match as well. The page labelled 2023-09-30 shows the previous week's chart.
- Wikipedia's yearly top-ten lists give the same entry date for all 100 list songs.
- The {{ 100 - bc_hosted() }} list songs whose first top-10 week falls before {{ cv_first() }} have their **rank** from the mirror alone. The mirror's agreement with every hosted week is the reason to trust it there.

## Rap classification

- A song counts as rap on direct evidence when it appears on a year-end Hot Rap Songs list or has a number in the Hot Rap Songs column of an artist's discography table. {{ tier('table') }} of the 100 do.
- The other {{ tier('summary') }} are Drake album cuts. Drake's own tables carry no rap column, so those entries rest on Billboard's rap component charts as relayed by search summaries (†).
- A **dash** in a rap column is weak evidence. Two 2026 J. Cole songs show a dash in one collaborator's table and rap peaks of 8 and 9 in J. Cole's own. Dashes were never used to exclude a song on their own.
- Year-end deduction: a song high on the year-end Hot R&B/Hip-Hop list but absent from that year's 50-title rap list is treated as not rap. The two orders invert in 13 to 17 places a year, so the deduction is used only well away from the bottom of the lists.

## Felt tempo from a 30-second clip

1. Separate the percussive part of the clip and take onset envelopes in three bands. A "snare or clap" envelope is the geometric mean of the mid and high bands, so a hat alone or a kick alone scores low.
2. Find the clip's steady pulse from the envelope spectrum. Commercial rap is grid-locked, so one tempo per clip is assumed.
3. For the pulse, its half and its double, fold the envelopes into one bar of sixteen steps at every bar phase and score a backbeat template: strong on beats 2 and 4, weak on 1 and 3, kick on 1. A displaced second backbeat (the "and" of 4, as in drill) is allowed.
4. The best-scoring tempo is the felt tempo. The margin over the next reading sets the label: **M** clear (margin ≥ 0.15, score ≥ 0.25), **L** leaning, **I** unclear but only one reading inside 55–150 BPM, **?** unresolved.

**Checks.** The estimator recovers the felt tempo of 24 of 24 synthetic patterns built to break it: trap, boom-bap, bounce, drill with a displaced backbeat, four-on-the-floor with a clap over the kick, club kicks, and kicks with a snare-like click. On the real clips its pulse matches an earlier published BPM, or half or double of it, for {{ top('pulse_vs_listings')['agree'] }} of {{ top('pulse_vs_listings')['agree'] + top('pulse_vs_listings')['disagree'] }} tracks that had one; most of the rest are tracks whose listings disagreed with each other.

**Limits.**
- A clip is one section, usually around the first hook. A beat switch elsewhere is not seen.
- Beats with several percussion layers on different beats (a clap on 2 and 4 plus a snare on 3) can read either way. Those are the leaning, range-resolved and unresolved cases; they are listed in M-1 and marked in table 4b.
- An earlier version of the estimator muted the clap wherever a kick landed with it and misread bounce and four-on-the-floor beats as half-time. That was found by inspecting folded drum profiles and removed before any number was used.

## Lyric timing and structure

1. **Record choice.** For each track, LRCLIB records whose artist and title match and whose length is within 3 seconds of the Apple duration. {{ g('all','n_lyric') }} tracks have one; {{ cnt('lyric_missing') }} do not.
2. **Repetition detector.** Lines are normalized and matched; a block of two or more lines that returns, or a line repeated four times, is hook-like. The largest returning cluster is taken as the hook.
3. **Independent read.** A separate AI reader, which never sees the detector's output, reads the same record and marks the first line, the hook and its returns, and a coarse section map. Every time must come from the record.
4. **Comparison and ruling.** The two readings are compared by fixed rules (hook exists or not; first hook time within 2.5 s; hook inside the first three lines; hook count within one; first line within 1 s). Of {{ top('review_summary')['reviewed'] }} tracks read, **{{ top('review_summary')['agree'] }} agreed** and **{{ top('review_summary')['ruled'] }} went to a second reader**, who was asked to try to overturn the first reader before accepting either. Rulings: the reader was right in {{ top('review_summary')['resolution'].get('reviewer_right', 0) }}, the detector in {{ top('review_summary')['resolution'].get('algorithm_right', 0) }}, neither in {{ top('review_summary')['resolution'].get('both_wrong_corrected', 0) }}, and {{ top('review_summary')['resolution'].get('unresolved', 0) }} stayed unresolved.
5. **Why they disagreed.** Mostly over *which* returning block is the hook when an intro chant, a pre-hook and a chorus all come back. That is a judgment, so the findings also report the first return anchor, which needs no such call.

**Limits.**
- Timestamps are crowd-synced and line-level: good to about a second, silent about anything inside a line. The gap after a last word and the place of an ad-lib in the bar cannot be read from them.
- The first line is the first *transcribed* line. A wordless intro is invisible.
- Section labels are one reader's. Syllables are estimated from spelling.
- **Outside knowledge in reader notes.** {{ top('review_summary')['asides_removed'] }} reader notes carried an aside that could not have come from the file: a remark "from memory", or a mention of a beat switch, which a lyric record cannot show. None of them changed a recorded time. The asides were cut from the stored notes, and on {{ top('review_summary')['kinds_reset'] }} tracks the label for the kind of first line, which such an aside could have influenced, was reset to "unclear".
- The label for the kind of first line (ad-lib, sample, spoken, sung, rap) is the weakest item here. It is judged from text, and a reader may recognize a well-known borrowed lyric, which is outside knowledge and not a measurement. Treat that split as a rough guide.
- Lyric text was used in memory to find repeats and count words. None of it is stored.

## Documented facts

- For each track the saved Wikipedia article text and, where one exists, the Songfacts page were checked against every claim on file from the earlier search-based pass. The first reader returned **supported**, **partly supported**, **contradicted** or **not addressed**, with the page's own words. A skeptic then tried to refute each verdict against the same file, and each quote was searched for in the saved text.
- Result for the {{ top('claims_summary')['claims'] }} claims on the {{ top('claims_summary')['tracks'] }} list tracks: {{ top('claims_summary')['final'].get('supported', 0) }} supported, {{ top('claims_summary')['final'].get('partly_supported', 0) }} partly supported, {{ top('claims_summary')['final'].get('contradicted', 0) }} contradicted, {{ top('claims_summary')['final'].get('not_addressed', 0) }} not addressed by either page. The pages also yielded {{ top('claims_summary')['new_facts'] }} further statements that survived both checks.
- A supported claim is marked **P** in table 4c. A contradicted one drops to **U** and is not counted. "Not addressed" changes nothing: the pages are silent, which is not a denial.

## What is still unknown

- The length of the silence after a punchline, and where ad-libs sit inside the bar.
- What the drums, the 808 and the vocal stack do when a section returns.
- The felt tempo of the {{ g('all','feel_basis').get('?',0) }} open clips and of any second beat in a beat-switch record.
- First-vocal time to better than about a second.

Closing those needs the full recordings and word-level timing, which this study did not have.

## Check one record yourself in five minutes

You can test any row of table 4b against your own copy of the record:
1. Load the track in your DAW and measure the time from one snare to the next. The snares fall on felt beats 2 and 4, two felt beats apart, so the felt BPM is 120 divided by that time in seconds (1.67 s between snares is 72 BPM).
2. Drop a marker on the first word and on the first line of the hook. Compare with the first-line and first-hook columns.
3. Count felt bars from the hook's first line to the first line of the next section. Compare with the hook length.

If a row is off by more than a couple of seconds, the lyric record or the edit differs from your copy; trust your ears and the DAW.

## Rebuilding the numbers

- `scripts/measure/` holds the fetch and analysis scripts. They write to a working directory (`MEASURE_WORK`, default `work/`, not committed): chart pages, article text, lyric records and preview audio.
- Order: `fetch_cabillboard.py`, `parse_wiki_lists.py`, `fetch_wiki_articles.py`, `genre_matrix.py`, `parse_discog.py`, `discog_match.py` (charts and genre); `fetch_itunes.py`, `run_audio.py` (runtime and feel; `synth_test.py` re-runs the estimator check); `fetch_lrclib.py`, `run_lrc.py` (lyric timing); `fetch_songfacts.py`, `build_corpus.py` (page text); then `export_measured.py`, `export_review.py` and `export_claims.py` write `data/measured/`.
- The independent lyric read and the page check were run as reviewed agent batches in this session; their outputs are frozen in `data/measured/lyric_structure_review.json` and `data/measured/page_claims.json`.
- `scripts/run_all.sh` then rebuilds every table and document from `data/raw/` and `data/measured/`.
