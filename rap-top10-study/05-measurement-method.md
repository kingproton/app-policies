# 5 — How the measurements were made

This file says what was measured, from what, how it was checked, and where it stops. All of it was done inside this study on 2026-11-25.

**Who did the reading.** Nobody listened to the recordings, and no person read the lyric records or the pages. "Reader", "second reader" and "skeptic" below are separate AI agents run inside this study, each given only the files and rules for its step. The "verifier" named in the other files is the earlier, search-based pass: an AI agent that read web-search summaries, not pages. The lyric reading and ruling was also run a second time by separate agents, as a check. Agreement between agents is a consistency check, not a human one.

## What was measured

| Measure | Source read | Method | Coverage of the 100 | Check |
|---|---|---|---|---|
| First top-10 date and rank | Weekly Hot 100 mirror; Billboard Canada chart pages; Wikipedia yearly top-ten lists | First week in positions 1–10, per song | 100 | Date matches Wikipedia for 100; date and rank match Billboard Canada for 51 of the 51 songs whose week is hosted |
| Rap classification | Wikipedia's year-end Hot Rap Songs lists (2021–2025) and the Hot Rap Songs columns of artist discography tables (65 pages read, 41 with a rap column, 27 of them listing a top-10 arrival) | A number on either is a Billboard rap-chart figure | 86 from tables; 14 from search summaries of Billboard pages | Column identity is taken from each table header's link, not its position |
| Runtime | Apple catalog (public search API) | Duration of the track matched by title and artist; where several editions matched, the one closest to the earlier cited runtime was preferred | 96 (4 more from cited sources) | For 94 of the 94 tracks with an earlier cited runtime, the catalog holds an edition within 2 s of it. Not an independent check: closeness to that runtime was a selection criterion |
| Grid and felt tempo | Apple's 30-second preview clip | Backbeat template on drum onsets (below) | 96 clips: 72 clear, 6 leaning, 7 by range, 11 open | 24 of 24 synthetic drum patterns; pulse agrees with an earlier BPM listing for 67 of 83 |
| First lyric line, first hook, hook count | LRCLIB time-synced lyric record matching the track's length within 3 s | Repetition detector plus an independent read; a second reader rules on disagreements | 98 | Two readings per track, and a second separate run of both; matching records agree on the first line within 1 s for 75/97 |
| Section map (intro, verses, hooks, bridge) | Same record | The independent reader's coarse map | 98 | One reader; lengths in bars need a resolved felt tempo |
| Verse and hook density | Same record | Words and estimated syllables per second inside the detector's sections | 97 | Medians only; single tracks can be off by about 10% |
| Documented facts (samples, openings, beat switches, how it was made) | Saved text of 100 Wikipedia articles and 84 Songfacts pages | A reader rules on each earlier claim against the page text; a skeptic re-checks; every quote is matched mechanically | 100 tracks, 888 claims | P: after the skeptic's check, the saved page states the fact or names the work, and the quoted words are in the saved text (the routes are listed below). Claims the pages do not address keep their earlier basis; those coded S (search summary, not rejected) are still counted and marked S |

## Sources and access

- **Read directly:** `ca.billboard.com` (Billboard Canada's licensed chart pages and syndicated Chart Beat articles), `en.wikipedia.org`, `itunes.apple.com` and its preview host, `lrclib.net`, `www.songfacts.com`. Each site's robots.txt was read first, requests were spaced, and a plain client name was sent.
- **Not read:** `www.billboard.com`. Its robots.txt bars Anthropic's agents from everything except two sections. Billboard chart pages and reports cited in this study are known through web-search summaries from the earlier pass, and are labelled that way. You can remove that host from the environment's allowed list.
- **Allowed but never used:** `songbpm.com`. Nothing was fetched from it; tempo was measured from the preview clips instead, and the published BPM figures used for comparison come from the earlier search-based pass. That host can be removed as well.
- **Kept out of the repository:** lyric text, audio, and raw page downloads. The repository holds derived numbers and labels only (`data/measured/`). Short quotes from pages are kept for verification, trimmed to 30 words when credited to Wikipedia alone and to 12 otherwise (Songfacts, or a claim both pages support).

## Chart dates and ranks

- The weekly mirror gives every Hot 100 chart since 1958. Billboard Canada hosts 162 chart weeks from 2023-09-02 to 2026-11-21, including your starting issue. In 159 of them all 100 titles match the mirror position for position, and in 2 more (2024-01-20, 2025-11-29) one title is spelled differently; in all 161 the 25 rows per page that show last week, peak and weeks on chart match as well. The page labelled 2023-09-30 shows the previous week's chart. 7 later weeks are not hosted (2024-05-04, 2024-08-24, 2025-06-14, 2025-09-13, 2025-12-27, 2026-01-03, 2026-02-14); no list song and no close call first reached the top 10 in any of them.
- Wikipedia's yearly top-ten lists give the same entry date for 100 of the 100 list songs.
- The 49 list songs whose first top-10 week falls before 2023-09-02 have their **rank** from the mirror alone. The mirror's agreement with 161 of the 162 hosted weeks is the reason to trust it there; the one exception is the page labelled 2023-09-30.

## Rap classification

- A song counts as rap on direct evidence when it appears on a year-end Hot Rap Songs list or has a number in the Hot Rap Songs column of an artist's discography table. 86 of the 100 do.
- The other 14 are Drake album cuts. No discography table read gives a Hot Rap Songs peak for any of them (2 show only a dash in another artist's rap column, which is not evidence), so those entries rest on Billboard's rap component charts as relayed by search summaries (†).
- A **dash** in a rap column is not evidence. Across the 41 discography tables with a rap column, 18 songs show a dash in one table and a numbered rap peak in another (`data/measured/discography_dash_conflicts.json`), among them "Carnival" (dash in Rich the Kid's table, No. 1 in Kanye West's, Playboi Carti's, Ty Dolla Sign's) and "Knife Talk" (dash in Metro Boomin's production table, No. 2 in 21 Savage's). Dashes were never used to exclude a song on their own.
- Year-end deduction: a song that sits on a year-end Hot R&B/Hip-Hop or Hot 100 list at a rank where a rap title would also make that year's 50-title Hot Rap Songs list, and is not on it, is treated as not rap. The two orders are not identical: taking titles in rap-list order, the R&B/hip-hop rank falls from one title to the next in 11 to 17 places a year (2021: 11, 2022: 17, 2023: 16, 2024: 17, 2025: 13), so the deduction is used only well away from the bottom of the lists.
- This study treats a listing on Hot R&B Songs, or on an R&B-only component chart, as meaning the song is not rap. That is a working rule, not a Billboard statement read here. A listing on a country, rock or dance chart is not treated the same way, because one list song is on a year-end rap list and on a country chart; exclusions that rest on such a listing alone are graded indirect in table 4d.

## Felt tempo from a 30-second clip

1. Separate the percussive part of the clip and take onset envelopes in a mid and a high band from it, plus a low (kick and 808) band from the full signal. A "snare or clap" envelope is the geometric mean of the mid and high bands, so a hat alone or a kick alone scores low.
2. Find the clip's steady pulse from the envelope spectrum. Commercial rap is grid-locked, so one tempo per clip is assumed.
3. For each octave multiple of the pulse that falls between 46 and 185 BPM (in practice two readings per clip: the pulse and its half, or for one slow-pulse clip the pulse and its double), fold the envelopes into one bar of sixteen steps at every bar phase and score a backbeat template: strong on beats 2 and 4, weak on 1 and 3, kick on 1. A displaced second backbeat (the "and" of 4, as in drill) is allowed.
4. A clear reading (margin ≥ 0.15, score ≥ 0.25) is taken as scored: **M**. Otherwise, if exactly one of the two readings lies in 55–150 BPM, that one is taken even when it scored lower (5 of the 7 I tracks): **L** if it is also the leaning best score (margin ≥ 0.07, score ≥ 0.15), else **I**. If both or neither lie in the range, a leaning best score is taken (**L**); anything else is unresolved (**?**).
5. Last, an L or I reading whose pulse matches no published tempo at the same, half or double speed (within 2.5%) is also set to **?** (4 tracks). An unclear clip reading that the listings contradict is not resolved; table 4b shows both numbers.

**Checks.** The estimator recovers the felt tempo of 24 of 24 synthetic patterns built to break it: trap, boom-bap, bounce, drill with a displaced backbeat, four-on-the-floor with a clap over the kick, club kicks, and kicks with a snare-like click (`data/measured/synthetic_feel_test.json`). On the real clips its pulse matches an earlier published BPM, or half or double of it, for 67 of 83 tracks that had one. Of the other 16, 4 have listings that disagree with each other and 12 have a single or repeated listing that the pulse does not match (counted against the listings kept after the earlier pass set outliers aside). 1 of the 12 ("United In Grief") does match a listing that the earlier pass set aside as an outlier. Those mismatches are not explained. 8 of them are clear clips and keep their reading; the unclear ones are the open cases of step 5 and the unresolved clips.

**Limits.**
- A clip is one section, usually around the first hook. A beat switch elsewhere is not seen.
- Beats with several percussion layers on different beats (a clap on 2 and 4 plus a snare on 3) can read either way. Those are the leaning, range-resolved and unresolved cases; all three kinds are listed by name in M-1 and marked in table 4b.
- An earlier version of the estimator muted the clap wherever a kick landed with it and misread bounce and four-on-the-floor beats as half-time. That was found by inspecting folded drum profiles and removed before any number was used.

## Lyric timing and structure

1. **Record choice.** For each track, LRCLIB records whose artist and title match and whose length is within 3 seconds of the track's runtime: the Apple catalog duration, or the earlier cited runtime for the 4 tracks with no catalog match (#13 Evil J0rdan, #14 Rather Lie, #30 Euphoria, #75 Vegas). 98 tracks have one; 2 do not ("Staying Alive" and "I'm Dat N***a").
2. **Repetition detector.** Lines are normalized and matched; a block of two or more lines that returns, or a line of two or more words repeated four times, is hook-like. The largest returning cluster is taken as the hook.
3. **Independent read.** A separate AI reader, which never sees the detector's output, reads the same record and marks the first line, the hook and its returns, and a coarse section map. Every time must come from the record.
4. **Comparison and ruling.** The two readings are compared by fixed rules (hook exists or not; first hook time within 2.5 s; hook after at most three lines; hook count within one; first line within 1 s). Of 98 tracks read, **58 agreed** and **40 went to a second reader**, who was asked to try to overturn the first reader before accepting either. Rulings: the reader was right in 38, the detector in 1, neither in 1, and 0 stayed unresolved.
5. **Why they disagreed.** Mostly over *which* returning block is the hook when an intro chant, a pre-hook and a chorus all come back. That is a judgment, so the findings also report the first return anchor, which needs no such call.
6. **A second run.** The reading and the ruling were run a second time by separate AI agents with the same rules (`data/measured/lyric_structure_second_run.json`). It reached a final value for 94 of the 98 tracks and left 4 unruled. Against the values used here it agrees on whether there is a hook in 94/94, on the first line within 1 s in 94/94, on the first hook within 2.5 s in 83/87, on the hook count within one in 86/87 and on hook-before-first-verse in 85/87. The softer labels agree less: first section 92/94, number of verses 83/94, kind of first line 86/94, hook-on-return label 80/87. The second run never changes a value. Table 4b-2 marks each track, and no first-hook time quoted as an example in the findings comes from a track where the two runs place the first hook differently.

**Limits.**
- Timestamps are crowd-synced and line-level: good to about a second, silent about anything inside a line. The gap after a last word and the place of an ad-lib in the bar cannot be read from them.
- The first line is the first *transcribed* line. A wordless intro is invisible.
- Section labels are one reader's. Syllables are estimated from spelling.
- A section's length runs to the start of the next section. The last section ends two typical line gaps after the last lyric line (never past the end of the record), so a fade or instrumental outro is not counted as part of a final hook or verse.
- **Outside knowledge in reader notes.** 6 reader notes carried an aside that could not have come from the file: a remark "from memory", or a mention of a beat switch, which a lyric record cannot show. None of them changed a recorded time. The asides were cut from the stored notes, and on 3 tracks the label for the kind of first line, which such an aside could have influenced, was reset to "unclear".
- The label for the kind of first line (ad-lib, sample, spoken, sung, rap) is the weakest item here. It is judged from text, and a reader may recognize a well-known borrowed lyric, which is outside knowledge and not a measurement. Treat that split as a rough guide.
- Lyric text was used in memory to find repeats and count words. None of it is stored.

## Documented facts

- For each track the saved Wikipedia article text and, where one exists, the Songfacts page were checked against every claim on file from the earlier search-based pass. The first reader returned **supported**, **partly supported**, **contradicted** or **not addressed**, with the page's own words. A skeptic then tried to refute each supported, partly supported or contradicted verdict (609 of the 888) and every new statement against the same file, and each quote was searched for in the saved text. The 279 verdicts the first reader returned as not addressed were not re-checked; they are one reader's.
- Result for the 888 claims on the 100 list tracks: 298 supported, 279 partly supported, 30 contradicted, 281 not addressed by either page. The pages also yielded 879 further statements that survived both checks.
- A claim is marked **P** when, after the skeptic's check, the saved page states the fact or names the work: the final verdict is supported; or it is partly supported and the quoted words are in the saved page (for beat switches, only the songs hand-listed in `scripts/corrections.py`, section 10); or the fact comes from a new page statement that survived the skeptic; or the claim was recoded to what the page states (`PAGE_RECODE`, 1 opening). The final verdict is the skeptic's: it downgraded 27 verdicts from supported to partly supported, and those count as partly supported. Of the 79 P borrowings, 27 are supported, 41 partly supported and 11 added from page statements; of the 18 page-based beat switches, 2, 12 and 4. A partly supported verdict means a detail of the earlier claim is not on the page; that detail is not counted.
- A contradicted opening, hook-order, beat-switch, return or delivery claim drops to **U** and is not counted (3 of the 30 contradicted claims). 1 more, the opening of "Family Matters", was recoded to what the page states and is marked P. The others (hook descriptions, runtimes, structure notes, key, producers) carry no basis code and feed no count. "Not addressed" changes nothing: the pages are silent, which is not a denial, so a claim coded **S** stays S and is still counted.

## What is still unknown

- Where phrases start and stop against the drums, and where rhymes land in the bar.
- The length of the silence after a punchline, and where ad-libs sit inside the bar.
- What the drums, the 808, the melody and the vocal stack do when a section returns, and which of those changes is audible enough to matter.
- The felt tempo of the 11 open clips and of any second beat in a beat-switch record.
- Which voice the first transcribed line belongs to, and the first-vocal time to better than about a second.

Closing those needs the full recordings and word-level timing, which this study did not have.

## Check one record yourself in five minutes

You can test any row of table 4b against your own copy of the record:
1. Load the track in your DAW and measure the time from one snare to the second snare after it. That is one felt bar, so the felt BPM is 240 divided by that time in seconds (3.33 s is 72 BPM). Measuring a whole bar also works where the second backbeat is displaced.
2. Drop a marker on the first word and on the first line of the hook. Compare with the first-line and first-hook columns.
3. Count felt bars from the hook's first line to the first line of the next section. Compare with the hook length.

If a row is off by more than a couple of seconds, the lyric record or the edit differs from your copy; trust your ears and the DAW.

## Rebuilding the numbers

- `scripts/measure/` holds the fetch and analysis scripts. Downloads go to a working directory (`MEASURE_WORK`, default `work/`, not committed): chart pages, article text, lyric records and preview audio. The scripts read the study's own inputs from `data/raw/` (`MEASURE_INPUTS`); run `scripts/fetch_charts.py` and `scripts/top10.py` first so that `all.json` and `arrivals.json` exist there.
- Order, charts and genre: `fetch_cabillboard.py`; `fetch_wiki_lists.py` (the pages named in `wiki_pages.json`); `parse_wiki_lists.py`; `fetch_wiki_articles.py`; `genre_matrix.py`; `parse_discog.py <work>/net/wikipedia/disco/ <work>/net/discog_peaks.json`; `discog_match.py`.
- Runtime and feel: `fetch_itunes.py`, `run_audio.py`. `synth_test.py data/measured` re-runs the estimator check and stores its result.
- Lyric timing: `fetch_lrclib.py`, `run_lrc.py`. Page text: `fetch_songfacts.py`, `build_corpus.py`. Then `export_measured.py data/measured` writes the derived files.
- **Not re-runnable from the repository:** the lyric reading (both runs) and the page check were run as AI-agent batches in the original session. `export_review.py` and `export_claims.py` turned that session's journals into `data/measured/lyric_structure_review.json`, `lyric_structure_second_run.json` and `page_claims.json`, which are frozen. The two workflow scripts are kept for reference.
- `scripts/run_all.sh` then rebuilds every table and document from `data/raw/` and `data/measured/`. It checks that every template fills before it writes any of the six documents.
