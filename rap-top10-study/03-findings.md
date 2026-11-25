# 3 — Findings behind the process

These findings describe what the 100 most recent rap Hot 100 top-10 songs have in common. None of them claims that a technique *causes* chart success.

**How to read the counts:**
- Every count is **k / n assessed**. *n* leaves out tracks where the fact could not be measured or is unknown. Unknown never counts as "no".
- **Measured** findings (M-1 to M-6, M-9, M-10, and the timing rows of M-8) come from three sources read directly on 2026-11-25: Apple catalog durations, Apple's 30-second preview clips, and time-synced lyric records from LRCLIB. Nobody listened to the recordings; the numbers come from signal analysis of the clips and from reading the lyric records. `05-measurement-method.md` gives the method, the checks and the limits.
- **Documented** findings (M-7, M-11, M-12, and parts of M-8) come from what published pages say. A claim counts when saved page text supports it (**P**), or when the pages are silent and its cited source, known only through a web-search summary, was not rejected (**S**). Claims that could not be confirmed (**U**) and recollection (**R**) are never counted. The verifier (the earlier pass, which read web-search summaries) and the skeptic (this pass, which read the saved pages) were AI agents; no person read the pages.
- **Production judgment is labeled [J]:** every "Try it" block and the final section.

**What was assessed:**
- **Runtime:** 100 of 100 (96 from the Apple catalog, 4 from cited sources).
- **Felt tempo:** 96 preview clips. 72 show a clear backbeat; 13 more are resolved with a stated caveat; 11 stay open (7 where both readings fit, 4 where an unclear clip reading matches no published tempo). 4 tracks had no clip.
- **Lyric timing and structure:** 98 tracks have a time-synced lyric record whose length matches the track within 3 seconds. Each record was read twice, by a repetition detector and by an independent AI reader; where the two disagreed, a second AI reader ruled. No person read them. Timing basis: 58 agreed (A), 40 ruled (J). 2 tracks had no matching record ("Staying Alive" and "I'm Dat N***a").
- **A second run as a check.** The whole reading and ruling was run a second time by separate AI agents. For the 94 tracks it also resolved, it agrees on whether there is a hook in 94/94, on the first line within one second in 94/94, on the first hook within 2.5 seconds in 83/87, and on hook-before-first-verse in 85/87. Softer labels agree less often: the number of verses in 83/94, the kind of first line in 86/94, the hook-on-return label in 80/87. The second run never changes a value; table 4b-2 marks each track.
- **Timestamps** are crowd-synced line times. Where two or more matching records exist (97 tracks), their first-line times agree within one second for 75/97. Treat every timestamp below as good to about a second, not to the frame.
- **Not measured:** where phrases start and stop against the drums and where rhymes land; the silence after a punchline; where ad-libs sit inside a bar; what the drums, the 808, the melody and the vocal stack do when a section returns; and which of those changes is audible enough to matter. Line-level lyric timing and a 30-second clip cannot show them, and nobody listened. They stay unknown.

## Measured counts at a glance

| Measure | All 100 | Climbed into top 10 | Debuted in top 10 | Album-bomb cuts | Not album-bomb | Drake credited | No Drake | Trap-tagged | Verse-led-tagged |
|---|---|---|---|---|---|---|---|---|---|
| Songs | 100 | 12 | 88 | 55 | 45 | 41 | 59 | 50 | 8 |
| Median runtime | 3:31 (IQR 2:58–4:10; n=100) | 3:25 (IQR 2:27–4:23; n=12) | 3:33 (IQR 3:00–4:07; n=88) | 3:43 (IQR 3:04–4:18; n=55) | 3:17 (IQR 2:54–3:56; n=45) | 3:59 (IQR 3:10–4:21; n=41) | 3:20 (IQR 2:53–3:48; n=59) | 3:26 (IQR 2:58–4:02; n=50) | 4:26 (IQR 3:37–5:28; n=8) |
| Runtime ≤ 3:00 / ≥ 4:00 | 26/100 / 32/100 | 4/12 / 4/12 | 22/88 / 28/88 | 13/55 / 21/55 | 13/45 / 11/45 | 7/41 / 20/41 | 19/59 / 12/59 | 13/50 / 13/50 | 0/8 / 5/8 |
| **Felt tempo** — clips with a clear backbeat | 72/96 | 8/10 | 64/86 | 42/55 | 30/41 | 32/41 | 40/55 | 40/47 | 2/7 |
|   median felt BPM (clear) | 72 (IQR 65–81; n=72) | 74 (IQR 62.5–95; n=8) | 72 (IQR 65–81; n=64) | 72 (IQR 65.5–81; n=42) | 73.5 (IQR 64.5–80.5; n=30) | 70 (IQR 65–79; n=32) | 74 (IQR 66–81; n=40) | 71 (IQR 63.5–78; n=40) | 76 (n=2) |
|   slow (under 90) / mid (90–119) / fast (120+), clear | 63 / 6 / 3 | 6 / 1 / 1 | 57 / 5 / 2 | 38 / 4 / 0 | 25 / 2 / 3 | 30 / 2 / 0 | 33 / 4 / 3 | 39 / 1 / 0 | 2 / 0 / 0 |
|   same split, all resolved readings | 69 / 13 / 3 | 6 / 3 / 1 | 63 / 10 / 2 | 41 / 7 / 0 | 28 / 6 / 3 | 32 / 3 / 0 | 37 / 10 / 3 | 43 / 1 / 0 | 3 / 1 / 0 |
| **First lyric line** — median time | 1.4 s (IQR 0.3–5.0; n=98) | 0.9 s (IQR 0.4–8.0; n=12) | 1.5 s (IQR 0.3–5.0; n=86) | 1.5 s (IQR 0.3–5.8; n=54) | 0.9 s (IQR 0.2–4.3; n=44) | 1.5 s (IQR 0.2–4.0; n=40) | 1.4 s (IQR 0.3–5.3; n=58) | 1.4 s (IQR 0.4–4.3; n=48) | 2.1 s (IQR 0.3–21.4; n=8) |
|   within 5 s / after 15 s | 74/98 / 7/98 | 9/12 / 0/12 | 65/86 / 7/86 | 40/54 / 4/54 | 34/44 / 3/44 | 31/40 / 4/40 | 43/58 / 3/58 | 37/48 / 3/48 | 6/8 / 2/8 |
| **Recurring hook** present | 91/98 | 11/12 | 80/86 | 50/54 | 41/44 | 37/40 | 54/58 | 45/48 | 6/8 |
|   first hook — median time | 0:31 (IQR 0:12–1:04; n=91) | 0:18 (IQR 0:10–0:31; n=11) | 0:36 (IQR 0:13–1:11; n=80) | 0:45 (IQR 0:14–1:12; n=50) | 0:19 (IQR 0:10–0:55; n=41) | 0:44 (IQR 0:14–1:12; n=37) | 0:22 (IQR 0:11–0:57; n=54) | 0:36 (IQR 0:14–1:13; n=45) | 0:43 (IQR 0:02–1:56; n=6) |
|   first hook by 0:30 / by 1:00 (of all assessed) | 45/98 / 67/98 | 8/12 / 11/12 | 37/86 / 56/86 | 20/54 / 33/54 | 25/44 / 34/44 | 15/40 / 25/40 | 30/58 / 42/58 | 20/48 / 32/48 | 3/8 / 3/8 |
|   hook before the first verse | 48/91 | 8/11 | 40/80 | 22/50 | 26/41 | 16/37 | 32/54 | 20/45 | 3/6 |
|   first return anchor — median time | 0:15 (IQR 0:05–0:58; n=92) | 0:10 (IQR 0:01–0:14; n=11) | 0:23 (IQR 0:07–1:03; n=81) | 0:37 (IQR 0:11–1:07; n=51) | 0:12 (IQR 0:04–0:36; n=41) | 0:33 (IQR 0:07–1:06; n=38) | 0:14 (IQR 0:04–0:47; n=54) | 0:23 (IQR 0:03–1:00; n=45) | 0:42 (IQR 0:02–1:46; n=6) |
|   hook occurrences: 2 / 3 / 4+ | 43 / 42 / 6 | 4 / 5 / 2 | 39 / 37 / 4 | 28 / 21 / 1 | 15 / 21 / 5 | 24 / 11 / 2 | 19 / 31 / 4 | 25 / 16 / 4 | 4 / 2 / 0 |
| **Section lengths** — intro (felt bars) | 4.4 (IQR 3.8–8.1; n=83) | 4.4 (IQR 3.8–7.9; n=10) | 4.4 (IQR 3.7–8.2; n=73) | 4.7 (IQR 3.8–8.2; n=47) | 4.2 (IQR 3.7–7.7; n=36) | 5.2 (IQR 3.6–9.0; n=34) | 4.3 (IQR 3.7–7.8; n=49) | 4.1 (IQR 3.5–8.0; n=42) | 6.0 (IQR 1.6–8.1; n=4) |
|   first hook (felt bars) | 7.5 (IQR 4.0–8.1; n=79) | 7.5 (IQR 5.1–8.2; n=10) | 7.5 (IQR 4.0–8.1; n=69) | 6.2 (IQR 4.0–8.1; n=44) | 7.6 (IQR 3.9–8.1; n=35) | 4.3 (IQR 3.8–8.1; n=32) | 7.7 (IQR 4.1–8.1; n=47) | 6.0 (IQR 4.0–8.0; n=41) | 7.6 (n=3) |
|   first verse (felt bars) | 11.9 (IQR 8.0–16.2; n=82) | 9.3 (IQR 7.6–14.5; n=10) | 12.0 (IQR 8.0–17.8; n=72) | 11.9 (IQR 8.0–15.9; n=47) | 12.0 (IQR 8.0–17.1; n=35) | 10.0 (IQR 8.0–15.8; n=34) | 12.2 (IQR 8.0–19.0; n=48) | 10.0 (IQR 8.0–15.9; n=41) | 24.1 (IQR 18.5–29.0; n=4) |
|   verse 2 shorter / similar / longer than verse 1 | 23 / 28 / 40 (of 91) | 2 / 7 / 1 (of 10) | 21 / 21 / 39 (of 81) | 12 / 15 / 24 (of 51) | 11 / 13 / 16 (of 40) | 9 / 8 / 21 (of 38) | 14 / 20 / 19 (of 53) | 6 / 15 / 23 (of 44) | 4 / 1 / 3 (of 8) |
|   last hook longer than the first (by 25%+) | 8/91 | 0/11 | 8/80 | 6/50 | 2/41 | 8/37 | 0/54 | 3/45 | 2/6 |
| **Riding the beat** — verse syllables per second | 4.1 (IQR 3.7–4.5; n=97) | 4.4 (IQR 4.0–4.7; n=12) | 4.1 (IQR 3.7–4.5; n=85) | 4.0 (IQR 3.6–4.5; n=54) | 4.3 (IQR 3.9–4.7; n=43) | 4.0 (IQR 3.5–4.3; n=40) | 4.3 (IQR 3.8–4.8; n=57) | 4.0 (IQR 3.6–4.5; n=47) | 4.7 (IQR 4.0–5.1; n=8) |
|   verse syllables per felt beat | 3.1 (IQR 2.6–3.8; n=82) | 2.9 (IQR 2.3–4.1; n=10) | 3.2 (IQR 2.7–3.7; n=72) | 3.2 (IQR 2.9–3.7; n=47) | 3.0 (IQR 2.4–3.9; n=35) | 3.1 (IQR 2.9–3.6; n=34) | 3.1 (IQR 2.5–3.9; n=48) | 3.6 (IQR 2.9–3.9; n=41) | 3.2 (IQR 2.9–3.7; n=4) |
|   verse denser than hook (words per second) | 72/87 | 11/11 | 61/76 | 44/48 | 28/39 | 29/34 | 43/53 | 35/43 | 3/4 |

*Album-bomb* = a song that first entered the top 10 in the same chart week as at least two other songs by the same lead artist (an album-release week). *Climbed* = the song charted below the top 10 before first entering it. *Felt bars* are bars of four felt beats; on a doubled DAW grid (your 144 grid for a 72 feel) the bar count doubles. Style tags come from source descriptions, not from Billboard.

---

## Ranked patterns

Ranked by how directly each one changes a writing, arrangement or delivery decision, weighted by how many songs back it.

### M-1. The pocket is a slow backbeat: felt 65–81 BPM in the middle half, whatever the published BPM says

- **Effect:** delivery and writing. The felt pulse sets how long a bar lasts and where the snare answers you. Ranked first because it is the first decision in the session.
- **Count:**
  - Of 96 preview clips, **72** show a clear backbeat (a snare or clap on felt beats 2 and 4).
  - Of those 72: **63 are slow** (felt under 90), **6 are mid-tempo** (felt 100–107) and **3 are fast** (felt 127–143.5). Median felt tempo **72 BPM**, middle half 65–81.
  - Adding the 13 readings resolved with a caveat gives 69 slow / 13 mid / 3 fast of 85.
  - **Published BPMs mostly show the doubled number.** Among clear clips with an earlier BPM listing, the listing sits at double the felt tempo for 35, at the felt tempo for 14, at both for 3, and matches neither for 8. That is the "144 on the grid, 72 in the pocket" convention you already use.
- **Examples (pulse/felt from the clip):**
  - *Slow:* "Like That" 162/81, "Luther" 138/69, "Cinderella" 130/65, "Pushin P" 155/77.5, "Carnival" 148/74, "Wait For U" 170/85.
  - *Mid:* "Paint The Town Red" 100, "Hey Now" 102, "Squabble Up" 104, "Circo Loco" 104, "2 Hard 4 The Radio" 105, "First Class" 107.
  - *Fast:* "Houdini" 127, "Super Freaky Girl" 133, "Noid" 143.5.
- **Leaning (6):** the clip favours one reading by a small margin: "Redrum" 86 (not 172), "First Person Shooter" 61 (not 122), "Players" 105 (not 52.5), "N95" 70 (not 140), "Big Energy" 106 (not 53), "TSU" 65 (not 130).
- **Resolved by range, not by the clip (7):** one of the two readings falls outside 55–150 BPM, so the other is shown: "National Treasures" 96.5 (not 48.5), "TV Off" 101 (not 50.5), "Reincarnated" 91 (not 182), "Not Like Us" 101 (not 50.5), "7 Minute Drill" 85.5 (not 171), "Hiss" 83.5 (not 167), "Lovin On Me" 105 (not 52.5). On 6 of them the clip did not separate the two readings (margin 0.05 or less); on "National Treasures" (toward 48.5, margin 0.09) it leaned to the reading that was ruled out. For 5 of these the reading shown scored lower in the clip than the one ruled out ("National Treasures", "Reincarnated", "Not Like Us", "Hiss", "Lovin On Me").
- **Not resolved (11):**
  - Both readings fit the clip (7): "Ran To Atlanta" (72.5 or 145), "All The Way" (67.5 or 135), "Nokia" (63 or 126), "IDGAF" (68.5 or 136.5), "FE!N" (74 or 148), "United In Grief" (65.5 or 131.5), "Fair Trade" (58.5 or 117).
  - An unclear clip reading that no published tempo matches at the same, half or double speed (4): "Man At The Garden" (clip 80.5, listed 92), "Calling For You" (clip 76, listed 121), "Barbie World" (clip 108, listed 144), "Champagne Poetry" (clip 70.5, listed 87). The clip may have been read on a dotted pulse, or the listing may be wrong; neither is settled here.
- **Try it [J]:**
  - Before you write, clap 2 and 4 against the loop at the felt tempo and say your central phrase over it. If the clap feels rushed, you are counting the doubled grid.
  - In a slow pocket, aim rhymes at the snare (felt beats 2 and 4) and leave the back half of beat 4 open. That is the room your last word or ad-lib needs.
- **Exception:** the 3 fast records keep a full snare on 2 and 4 at 127–143.5. A fast, fully felt pulse leaves less room per syllable (see M-2): good for a chant, hard on dense bars. [J]
- **Flags:**
  - Drake-credited songs supply **30 of the 63** clear slow readings.
  - A 30-second clip is one section. A beat switch elsewhere in the track is not seen, so a song with two beats has one of them measured.
  - On 8 *clear* clips the measured pulse also matches no published tempo ("Make Them Cry", "2 Hard 4 The Radio", "Noid", "Daylight", "Fear Of Heights", "Search & Rescue", "Forever", "Jimmy Cooks"). The clip reading is kept because the backbeat is clear; the mismatch is not explained.
  - **Drill:** only two list songs carry a drill tag ("Barbie World" and "Princess Diana"), and the tempo of one of them is unresolved. Nothing about drill can be generalized from two songs.

### M-2. Mouth speed holds near four syllables a second; the beat decides how that feels

- **Effect:** writing (how many syllables a bar can hold) and delivery (pocket). Ranked second because it converts directly into a syllable budget.
- **Count:**
  - Across verse sections, the median track delivers **4.1 syllables per second** (middle half 3.7–4.5; n=97), or 3.4 words per second.
  - The rate barely moves with tempo: 4.0 per second on slow beats (n=66), 4.2 on mid-tempo beats (n=13), 4.0 on the 3 fast ones.
  - So the **syllables per felt beat** change instead: about **3.5** on slow beats, **2.4** on mid-tempo beats and 1.8 on fast ones. A slow pocket fills most of the four sixteenth-note slots in a beat; at 100 BPM the same mouth speed sits between eighth notes and triplets.
  - A lyric line lasts **2.4 seconds** at the median (middle half 2.0–3.0). In felt beats that is about four beats for 44 tracks and about two for 26 (of 82).
  - Verses are denser than hooks in **72/87** tracks: 3.4 words a second against 2.6.
- **Examples:**
  - *Densest verses (words per second):* "All The Way" (BigXthaPlug) 5.3, "Puffin On Zootiez" (Future) 4.6, "Barbie World" (Nicki Minaj) 4.6, "Hiss" (Megan Thee Stallion) 4.3, "Forever" (Lil Baby) 4.2.
  - *Sparsest:* "K-POP" (Travis Scott) 2.1, "Just Wanna Rock" (Lil Uzi Vert) 2.3, "Knife Talk" (Drake) 2.4, "Pushin P" (Gunna) 2.4, "Luther" (Kendrick Lamar) 2.5.
- **Try it [J]:**
  - At a 72 feel, one felt beat is 0.83 seconds, so the median rate gives you about 3.4 syllables a beat and 13 to 14 a felt bar. Write the dense bar to that budget, then cut two syllables from the bar that carries the punchline so the last word has air.
  - Count one line you already like. At 72, 16 syllables a felt bar is 4.8 a second: only 15 of 97 verses in this set run faster. Ten a bar is 3.0 a second, which is about where hooks sit (median 3.0).
- **Exception:** "All The Way" runs far above the rest and "K-POP" far below; both reached the top 10. Density is a choice, not a requirement. [J]
- **Flags:**
  - Syllables are estimated from spelling, and section boundaries come from the repetition detector, so individual figures can be off by 10% or so. The medians are steadier than any single track.
  - Line timing cannot show where inside the bar a syllable falls, or the gap after a last word.

### M-3. Getting to the hook: two shapes, and the songs that climbed use the fast one

- **Effect:** arrangement (what comes first) and writing (how long the first verse can run). Ranked third: it is the hook-first or verse-first decision, now measured.
- **Count:**
  - **91/98** assessed tracks have a main section that recurs. **7/98** have none (see M-9).
  - The first hook starts at a median **0:31** (middle half 0:12–1:04). It has arrived by 0:30 in 45/98 tracks, by 1:00 in 67/98, and comes after 1:30 in 11/98.
  - The hook comes **before the first verse** in **48/91** tracks with a section map. With at most three lyric lines before it: 28/91.
  - **The first return anchor** (the earliest line of any block that comes back, hook or not) lands at a median 0:15. In 72 of 91 tracks that anchor is the hook itself; in the rest an intro chant, tag or pre-hook returns first.
  - **By chart path:** songs that **climbed** into the top 10 reach the hook at a median **0:18** (n=11) and put it before the first verse in 8/11. Songs that **debuted** there: **0:36** and 40/80. Album-bomb cuts: 0:45; other songs: 0:19.
- **Examples with timestamps:**
  - *Hook first:* "First Class" (hook at 0:04 after 1 line), "Type Shit" (0:03), "BackOutsideBoyz" (0:03), "Barbie World" (0:03), "Rather Lie" (0:06), "Pussy & Millions" (0:01), "Carnival" (0:00), "Players" (0:10, the first line of the record).
  - *Verse first, long wait:* "Not Like Us" (hook at 1:15 after 27 lines), "Like That" (1:28 after 26), "On BS" (1:37 after 30), "National Treasures" (1:42 after 45), "K-POP" (1:27 after 26), "Houdini" (0:59 after 27).
- **Try it [J]:**
  - Single or short-form: put a line that will come back inside the first 15 seconds. 9 of the 12 climbers have a returning line by then, and the hook itself has started by 0:15 in 5 and by 0:30 in 8.
  - Statement record: you can hold the hook past a minute, as "Not Like Us" and "Like That" do, but give the listener a return anchor earlier: a tag, a chant or a refrain line that will come back.
- **Exception:** "Not Like Us" spent 28 weeks in the top 10 with its hook at 1:15. A late hook did not stop it. [J]
- **Flags:**
  - "Which block is the hook" is a judgment when two blocks recur. The two readings disagreed on whether there is a hook or when it starts for 30 of 98 tracks before the ruling; those are marked J in table 4b.
  - The second, separate run of the reading puts the first hook more than 2.5 seconds away on 4 of 87 tracks ("What Did I Miss?" (0:23 here, 0:04 in the second run), "Gimme A Hug" (2:16 here, 2:13 in the second run), "Hey Now" (0:19 here, 0:57 in the second run), "Cinderella" (0:29 here, 0:03 in the second run)). With its times, the median first hook is 0:31 and 44 hooks start by 0:30, against 0:31 and 45 here; hook-before-first-verse is 48/91 against 48/91.
  - Drake-credited songs put the hook before the first verse in 16/37; the rest in 32/54. Album-bomb weeks pull the whole set toward later hooks.
  - Only 12 songs climbed. The gap is large, but the group is small and not controlled.

### M-4. The first voice is rarely a rap line, and the intro is most often about four felt bars, with a smaller group at eight

- **Effect:** arrangement (the opening) and delivery (how you enter). Ranked fourth: it governs the first seconds, which is where your A/B test lives.
- **Count:**
  - The first lyric line starts at a median **1.4 seconds**: within 5 seconds in 74/98 tracks and after 15 seconds in 7/98.
  - **What that first line is** (the AI reader's call, from the text alone): an ad-lib or vocalization in 35, a sample or another voice in 22, spoken in 12, sung in 9, a rap line in 9, unclear in 11.
  - The first section in the map is an intro in 81 of 98 section maps, the hook in 13, a verse in 3 and a pre-hook in 1.
  - **Intro length** (the time before the first hook or verse): median 14 seconds, or **4.4 felt bars** (middle half 3.8–8.1). About four bars (3 to 5) in 29 tracks and about eight (7 to 9) in 17; under three in 16, five to seven in 8, nine or more in 13 (of 83 with a resolved felt tempo).
- **Examples:** "Evil J0rdan" waits until 0:54 for its first line; "Real Spill" until 0:12; "Redrum" until 0:24. "Not Like Us", "Houdini" and "Carnival" have a voice inside the first second.
- **Try it [J]:** treat the intro as four felt bars (eight on your 144 grid) with one identity sound in it: a tag, an ad-lib, a chopped phrase. Enter with the lead on bar five. If the record needs more runway, take eight and nothing in between.
- **Exception:** in 3 section maps the first transcribed line is already a verse line ("Gimme A Hug", "Man At The Garden", "Sticky (Drake)"). These are not cold opens: in the record used, that line comes at 0:28, 0:32 and 0:27, so each has a long opening that the lyric record does not show. The matching records for "Gimme A Hug" differ on that time by 60 seconds, so treat it as a late entry, not as a measured time. 13 maps start on the hook. [J]
- **Flags:** the lyric record shows the first *transcribed* line. A wordless intro, a beat tag or an instrumental sample before it is invisible here. The kind of line is the weakest label in this study: the reader judged it from text, which often cannot tell a sample from the artist, and may have recognized a well-known borrowed lyric. Treat that split as a rough guide (see `05-measurement-method.md`).

### M-5. Section sizes: hooks of four or eight felt bars, first verses of eight, twelve or sixteen

- **Effect:** writing and arrangement. Ranked fifth: it sizes every block in the session plan.
- **Count (one reader's section map, 98 tracks; bars need a resolved felt tempo):**
  - **First hook:** median 19 seconds, **7.5 felt bars**. About four bars in 27 tracks and about eight in 38 (of 79).
  - **First verse:** median 36 seconds, **12 felt bars**. About eight bars in 25, about twelve in 14, about sixteen in 17, longer in 18 (of 82).
  - **Verses per song:** two in 50, three in 29, four or more in 12, one in 6, none in 1 ("Carnival", whose record has no verse lines).
  - **Hook occurrences:** two in 43 tracks, three in 42, four or more in 6.
  - A bridge appears in 15/98, a pre-hook in 16/98 and a post-hook in 22/98. The record ends on an outro in 54 maps, on the hook or post-hook in 37 and on a verse in 7.
- **Examples (first hook start from table 4b; first hook / first verse in felt bars, from the section map in table 4b-2):**
  - *Four-bar hook:* "Pussy & Millions" (0:01; 4 / 8), "Whisper My Name" (1:21; 3.9 / 15.6).
  - *Eight-bar hook, eight-bar verse:* "4X4" (0:14; 8 / 8.2), "Princess Diana" (0:13; 8 / 8), "Puffin On Zootiez" (0:15; 8 / 8).
  - *Twelve-bar verse:* "All My Life" (0:20; 8 / 12), "Spin Bout U" (0:58; 8.3 / 12).
  - *Sixteen-bar verse:* "Houdini" (0:59; 8.1 / 16), "Outside" (0:13; 8.1 / 15.8).
- **Try it [J]:** plan the demo as intro 4, hook 8, verse 12 or 16, hook 8, verse 8 to 16, hook 8 in felt bars. Double each number on the 144 grid. That is the commonest skeleton in the set, not a rule.
- **Exception:** "Rich Flex", "Family Matters" and "Meltdown" are built in parts, each with a documented beat switch (M-11), and do not fit the skeleton. [J]
- **Flags:** section labels are one reader's call, and a hook sung twice in a row is counted as one long hook. Trap-tagged songs run shorter first verses (median 10 felt bars) than the set as a whole. Two hooks is the usual count on Drake-credited songs (24 of 37); elsewhere three is commoner (31 of 54, against 19 with two).

### M-6. When the hook comes back it is nearly the same words; what changes around it was not measured

- **Effect:** arrangement (transitions) and delivery. Ranked sixth: it says where these songs do not spend variation, which is the hook's words.
- **Count:**
  - The hook returns with **identical words in 28** tracks and with **minor variation in 46** (a few words or ad-libs). It comes back extended in 8, shortened in 7 and with new lyrics in 2.
  - The last hook is at least a quarter longer than the first in 8/91 tracks and at least a quarter shorter in 7/91; in the rest it is about the same length.
  - **Verse 2 against verse 1:** shorter in 23, about the same in 28, longer in 40/91. There is no "short second verse" rule in this set.
  - A stretch of 12 seconds or more between transcribed lines appears in 21/98 tracks. It can be a break, a beat change or a sample interlude, but also a passage the transcriber left out, so it is a hint and not a count of breaks.
  - What lyric timing cannot show: drums, 808 and doubles. Documented changes between sections are in M-11.
- **Examples:**
  - *Same words every time:* "Ran To Atlanta", "Whisper My Name", "National Treasures", "2 Hard 4 The Radio", "What Did I Miss?", "All The Way".
  - *Extended on return (the reader's label for the words):* "We Don't Trust You", "Meltdown", "Search & Rescue", "Just Wanna Rock", "Rich Flex".
  - *Shortened on return:* "TV Off", "Luther", "FE!N", "Sticky (Drake)", "712PM".
- **Try it [J]:** keep the hook's words fixed so it reads as the anchor, and move the change to its edges: drop the drums for the last felt bar before it, or add the stack and ad-libs only on the final pass. Give verse 2 the same length as verse 1 unless the song is short of ideas.
- **Exception:** the hook comes back with new lyrics on "Janice STFU" and "Major Distribution". [J]
- **Flags:**
  - Word-level sameness says nothing about the mix. A hook can keep its words and still gain doubles, harmonies or a new bed that this method cannot hear.
  - A hook's length runs to the start of the next section. When the hook is the last section, its end is set two typical line gaps after the last lyric line, so that a fade or instrumental outro is not counted as hook. That choice moves the longer-last-hook count: measured to the end of the record it would be higher.
  - Drake-credited songs supply all 8 longer last hooks (8/37, against 0/54 for the rest), and verse 2 runs longer than verse 1 on 21/38 of them against 19/53 elsewhere.

### M-7. Documented borrowing: a sample, interpolation or clip on 66 of the 100

- **Effect:** writing (the central phrase or recognition device) and arrangement (what opens the song and what comes back). Ranked seventh because it rests on what pages document, not on a measurement; it shapes both the hook and the opening.
- **Count:**
  - **66/100** songs have at least one documented borrowing. For **64** of them the saved Wikipedia or Songfacts page states it (P); the others rest on a cited source read through a search summary (S). The remaining songs are unknown, not "no".
  - Counting borrowings, not songs: 79 are page-based. 27 rest on a supported verdict, 41 on a partly supported one (the page names the work; a detail of the earlier claim is not on the page and is not counted), and 11 were added from page statements.
  - Climbers **10/12**; debuts **56/88**.
  - **By type:** samples on 51 songs; interpolations on 17; dialogue or spoken clips on 4; self-reuse on 1.
  - The page check added a borrowing that was not on file for 11 entries, among them "Real Spill" (Sade), "Knife Talk" (a Project Pat verse), "712PM" and "Fear Of Heights".
- **Where a page says what the borrowing does:**
  - *It opens the record:* "Make Them Pay", "Luther", "IDGAF", "Virginia Beach", "Daylight", "Paint The Town Red", "Real Spill", "Super Freaky Girl", "Super Gremlin".
  - *It carries the hook:* "Janice STFU" (the chorus interpolates Lykke Li's "I Follow Rivers"), "Staying Alive" (the chorus interpolates the Bee Gees), "Super Gremlin" (the sampled vocal is heard at the start and in the choruses), "Forever" (the chorus came from an existing Vory and Fridayy hook).
- **Try it [J]:**
  - As an independent artist, budget for clearance or build an *original* recognition device that works the same way.
  - Options: a motif you or your producer replay; a vocal chop of your own title phrase; or a regional sonic signature that's yours.
  - Put it in the intro and bring it back with every hook.
- **Exception:** "Pushin P" has no borrowing documented (unknown, not "no"), and its hook is a title chant that first arrives as a block at 0:56. A slogan people repeat can do a sample's job. [J]
- **Flags:**
  - Drake-credited songs: **31/41**; the rest: **35/59**.
  - Whether listeners already knew the borrowed record ("recognition") was not measured.
  - Credit status is known only where a page states it; a credit "not stated" in table 4c is not a claim that the use was uncleared.

### M-8. The 12 songs that *climbed* into the top 10 look different from the 88 that debuted there

- **Effect:** arrangement (how soon the hook comes, solo vs guests) and which patterns to weight. Ranked eighth only because the group is small. [J] I treat the climbers as the nearest comparison for a single released on its own, because they rose over weeks and did not debut in an album week; nothing in the data records label or release type, so that reading is not tested.
- **Count:** 12/100 climbed in; 88 debuted directly. Compared with the debuts:
  - **First hook:** median **0:18** vs **0:36**; by 0:30 in 8/12 vs 37/86.
  - **Hook before the first verse:** 8/11 vs 40/80.
  - **A second credited vocalist:** **1/12** vs **43/88**.
  - **Documented borrowing:** **10/12** vs **56/88**. These are floors, not rates: a song with nothing documented is unknown, not "no" (see M-7).
  - **Runtime:** median 3:25 vs 3:33.
  - **Chart run:** median weeks in the top 10 **5** vs **1**.
- **Examples:** "Paint The Town Red" (20 weeks in the top 10, climbed from #15); "Super Gremlin" (17 weeks in the top 10, climbed from #16); "Fukumean" (15 weeks in the top 10, climbed from #12); "Big Energy" (14 weeks in the top 10, climbed from #11); "Favorite Song" (9 weeks in the top 10, climbed from #11); "Agora Hills" (7 weeks in the top 10, climbed from #35).
- **Try it [J]:** if you want a comparison group for your demo, use these 12 rather than the 88 direct debuts (55 of the 100 are album-bomb cuts): mostly solo (11 of 12), with the hook started by 0:30 in 8/12. That describes 12 songs; it is not a way to climb.
- **Exception:** "Euphoria" climbed with no recurring hook at 6:24, and "Noid" entered the top 10 in the week its album-mate "St. Chroma" debuted there. Both climbs coincided with outside events, a public feud and an album release; the study can't say what drove them.
- **Flags:**
  - **Small sample (12).**
  - Doja Cat has 3 of the climbers ("Agora Hills", "Paint The Town Red", "Vegas") and Tyler, The Creator 2.
  - Comparing climbers with debuts shows correlation inside this set, not a recipe.

### M-9. 7 of 98 assessed records have no recurring hook

- **Effect:** writing, i.e. whether to build a chorus at all. Ranked ninth: few songs, but a clear alternative shape.
- **Count:** in **7/98** tracks no block of lyric comes back as a hook: "Make Them Cry", "Evil J0rdan", "Reincarnated", "Euphoria", "Hiss", "Calling For You", "Papi's Home".
  - 2 of the 7 carry the verse-led tag, and 3 are Drake-credited.
  - Their runtimes run from 2:59 to 6:24.
- **What comes back instead, song by song** (the lyric-record column is the AI reader's description of the record; the page column is page text, basis P):

| Song | In the lyric record | On the pages |
|---|---|---|
| "Make Them Cry" | One continuous rap; only short ad-lib tags repeat, at both ends | One word is repeated in the intro and again in the outro, bookending the song |
| "Evil J0rdan" | One verse after a 0:54 wait; nothing returns | A long intro built on a sample links it to the album track before it |
| "Reincarnated" | Three verses; verses 1 and 2 end on the title word | Three verses and no chorus; a sung Spanish intro by another singer; the third verse changes speaker |
| "Euphoria" | Three verse parts; one line recurs once | The beat is the landmark: a soft start, then it picks up, and the instrumental grows more aggressive |
| "Hiss" | Three verses separated by ad-lib breaks | A spoken-word intro, and a second spoken break between the first and second verse |
| "Calling For You" | No section returns; a one-off refrain passage, a sung title chant and a long skit | A sample "anchors the song"; a skit of about 90 seconds sits halfway through |
| "Papi's Home" | One verse framed by a sampled intro and outro | The sample is used in the intro and again in the outro; one verse only |

- **Try it [J]:**
  - If you go hookless, build a **return anchor**: a spoken frame that comes back, a beat change, or one line repeated as a refrain.
  - Make the record's context obvious: the target, the occasion, the stakes.
- **Exception:** "Man At The Garden" sits between the two shapes: one short line recurs through the verses as a litany before a chant block arrives at 1:15. [J]
- **Flags:** "no hook" here means no *lyric* block returns. A wordless or instrumental refrain would not show in a lyric record. Two of these are diss records ("Euphoria", "Hiss"), so part of this shape belongs to one kind of record.

### M-10. Runtime: album-bomb cuts run long; other songs sit nearer 3:15–3:20

- **Effect:** arrangement, i.e. how many sections to build. Ranked tenth.
- **Count:**
  - Median **3:31** (middle half 2:58–4:10; n=100).
  - **26/100** are 3:00 or under; **32/100** are 4:00 or over.
  - Source: the Apple catalog duration for 96 tracks, a cited runtime for 4 (#13 Evil J0rdan, #14 Rather Lie, #30 Euphoria, #75 Vegas).
- **By group:**
  - Album-bomb cuts: median **3:43**; other songs: **3:17**.
  - Climbers: **3:25** (n=12).
  - Drake-credited: **3:59**, vs **3:20** for everything else.
- **Examples:**
  - *Shortest:* "Barbie World" 1:50, "Just Wanna Rock" 2:04, "Fukumean" 2:05, "Pushin P" 2:16, "Lovin On Me" 2:18.
  - *Longest:* "Make Them Cry" 5:08, "TSU" 5:09, "Wacced Out Murals" 5:17, "Champagne Poetry" 5:36, "Euphoria" 6:24, "Family Matters" 7:37.
- **Try it [J]:**
  - Build the demo between about 2:45 and 3:30.
  - Add a section only if it brings a new bed, a new voice or a new device (M-6, M-11).
- **Exception:** "Family Matters" (7:37) and "Euphoria" (6:24) are long feud records built in several distinct parts (M-11).
- **Flags:** the long tail is mostly Drake album cuts and feud records.

### M-11. Documented changes: beat switches on 18 songs, and a second credited voice on 44

- **Effect:** arrangement, i.e. what changes at a block boundary and whether to split a song into parts. Ranked eleventh: documented, not measured.
- **Count:**
  - A **beat switch** is documented on **18** songs (all on saved page text): "Ran To Atlanta", "National Treasures", "Dust", "What Did I Miss?", "Gimme A Hug", "Nokia", "TV Off", "Euphoria", "Family Matters", "7 Minute Drill", "First Person Shooter", "Daylight", "Meltdown", "Superhero (Heroes & Villains)", "Rich Flex", "Major Distribution", "Jimmy Cooks", "Champagne Poetry". For 81 of the other 82 songs no page or cited source addresses a switch (60 with nothing on file, 21 with only an unverified recollection, 18 of those saying "no"); the remaining one is "Not Like Us", covered below. So 18 is a minimum.
  - Where the 18 page-based ones come from: 2 rest on a supported verdict, 12 on a partly supported one whose core (that the beat changes) the page states, and 4 on a new page statement.
  - "Not Like Us" is not counted. One search summary mentions a switch, the research record for the same song says no source settles whether its late breakdown is one, and neither saved page mentions it.
  - A page does not always use the words "beat switch". A described change of instrumental partway through is counted: a different sample bed in the second half of "First Person Shooter", a shift into harder production on "Dust", a move into new synths for the outro of "Superhero".
  - **14** of the 18 are Drake-credited and **2** are Kendrick Lamar's.
  - The Billboard credit names a **second vocalist** on **44/100** songs: 1/12 of the climbers and 43/88 of the debuts.
  - From the earlier search-based pass, 26 songs have a cited description of what changes between sections (one more is coded as naming no specific change): a beat or bed change in 14, a new voice in 9, a register change in 2 and a delivery change in 2 (1 song with both a beat and a voice change). Where the change sits in a section that comes back, it is a new voice in 8 and a bed change in 4.
- **Where the switch falls, as pages describe it:** "TV Off" splits into two parts around the two-minute mark; "Daylight" switches two minutes in; "Champagne Poetry" and "What Did I Miss?" switch about halfway; "Rich Flex" switches over halfway through; "Gimme A Hug" has two switches and "Meltdown" three; "Family Matters" changes beat between its verses.
- **Try it [J]:**
  - On a single, use the *small* version: a one-felt-bar drop or a vocal-only bar before the last hook.
  - Save a full beat switch for a statement or feud record, or for the back half of a long song.
  - If you're solo, make verse 2 sound like a different speaker: lower your register, change your point of view, or switch pockets.
- **Exception:** only 1 of the 12 climbers has a documented switch ("Euphoria"). For records such as "Lovin On Me" and "First Class" nothing is documented either way. [J]
- **Flags:**
  - **One-artist dominance:** Drake and Kendrick Lamar account for 16 of the 18 documented switches.
  - The return-change coding is mine, from cited descriptions (`scripts/corrections.py`: `RETURN_TYPES`, `RETURNING`).
  - Layer-level changes (808s, doubles, ad-libs) are not documented and were not measured.

### M-12. How the records were made, as pages tell it: on 14 of 71 songs the beat or the song existed earlier or was sent in

- **Effect:** process (who is in the room, what exists before the vocal) and delivery. Ranked last because it depends on which stories happened to be written down. It is still the only evidence here about the session itself.
- **Count:** the saved pages carry 140 statements about how 71 of the songs were made that survived the skeptic. Coded by rule (`scripts/corrections.py`):
  - **The beat was made away from the artist and sent, handed over or picked from a batch:** 6 songs ("Fair Trade", "Janice STFU", "Not Like Us", "Sticky (Drake)", "TV Off", "Way 2 Sexy").
  - **The beat or the song was older, or meant for someone or something else:** 9 ("Big Energy", "Carnival", "Champagne Poetry", "Hey Now", "IDGAF", "Knife Talk", "Sticky (Drake)", "Super Gremlin", "TSU").
  - **Built from a sample that came first:** 3 ("Barbie World", "Luther", "Super Freaky Girl").
  - **The hook, melody or title shout came first or already existed:** 5 ("Forever", "Fukumean", "Luther", "Players", "Way 2 Sexy").
  - **Fast: freestyled, made on the spot or in minutes:** 7 ("7 Minute Drill", "BackOutsideBoyz", "Carnival", "FE!N", "Fukumean", "Players", "Silent Hill").
  - **A guest verse added, swapped or recorded apart, after the song existed:** 9 ("All My Life", "All The Way", "Barbie World", "IDGAF", "Like That", "National Treasures", "Search & Rescue", "Superhero (Heroes & Villains)", "Tomorrow 2").
  - **Tracked in the last day or two before release:** 2 ("First Person Shooter", "Knife Talk").
  - **Previewed, teased or leaked before release:** 16 (among them "4X4", "All The Way", "Cinderella", "Enough (Miami)", "Evil J0rdan", "Favorite Song"). That is release strategy, outside the studio.
  - 33 songs have a statement that gives only a studio or a date, and 27 have statements that fit none of these headings. A song can appear under more than one heading.
- **Delivery, as sources describe it:** 54 songs have at least one cited delivery observation, most of them general. The pages add 93 delivery statements on 64 songs.
- **Named examples (page statements, paraphrased):**
  - "Forever": the hook existed first, as another artist's snippet; Lil Baby's brief for the beat was a kick and a snare, simple, with few hi-hats (Songfacts).
  - "Fukumean": it began as a freestyle in a late-night session, and the title phrase is a shout recorded by everyone in the room (Songfacts).
  - "Way 2 Sexy": Future came up with the hook first and chose the beat from fifteen to twenty played to him in one night (Songfacts).
  - "Fair Trade": the beat arrived in a beat pack and the track grew by sending files back and forth (Songfacts).
  - "First Person Shooter": recorded the day before the album came out (Wikipedia).
  - "BackOutsideBoyz": the producer says the beat took four minutes (Songfacts).
- **Try it [J]:**
  - Your one-session, punch-in habit is inside what these accounts describe: a finished beat arrives, the hook is found first, and the vocal is cut quickly. Lock the hook before you write verse two.
  - If a beat is close but busy, give your producer a brief as plain as Lil Baby's: name the two drums you want and what to remove.
- **Exception:** "Luther" and "N95" are described as built up over time, from a hummed melody or from ideas the artist then reworked alone. Slow builds are documented too. [J]
- **Flags:**
  - These are stories that were told, on 71 of 100 songs. They are not a sample of how hits are made, and absence of a story means nothing.
  - The codes come from keyword rules with a few hand corrections; each statement and its source page is in `data/raw/measured_stats.json` under `process`.

---

## Concentration and sample-size flags (read before generalizing)

- **Chart pattern:**
  - **88/100** debuted in the top 10.
  - **59/100** spent exactly one week there.
  - **55/100** are album-bomb cuts.
- **Artist concentration:**
  - **Drake** is lead artist on **38** and credited on 41.
  - Kendrick Lamar leads **12**; Future **9**.
  - Wherever a count above splits by Drake credit, the split is shown, because one artist's habits can pass for a pattern.
- **Drill:** only **2** tracks are tagged drill, "Barbie World" and "Princess Diana", both with Ice Spice. Every drill-specific recommendation in the process is therefore **judgment [J]**, not a finding.
- **Verse-led:** only 8 tracks carry the tag, and 2 of them have no recurring hook. Their medians are shown for orientation, not as rules.
- **The rap top-10 drought:** Billboard and the press reported no rap song in the top 10 from "What Did I Miss?" (July 2025) until spring 2026, and no rap song in the top 40 on the charts dated 2025-10-25 and 2025-11-01, a first since 1990 (both known through web-search summaries from the earlier pass; the articles were not opened in this study). That gap is why the 100 reach back to September 2021.

---

## What could and could not be measured

| Question asked | Status | Basis |
|---|---|---|
| Runtime | **Measured** for 96, cited for 4 | Apple catalog duration |
| Tempo and felt pulse, half and double time normalized | **Measured**: 72 clear, 13 with a caveat, 11 open, 4 no clip | Backbeat in a 30-second preview clip |
| First lead-vocal entrance | **Proxy only.** The first transcribed lyric line is measured for 98, to about a second. Whether that line is the lead artist is a text-only label: a rap or sung line in 18, an ad-lib or spoken line in 47, a sample or another voice in 22, unclear in 11. The lead-vocal entrance itself was not measured | Time-synced lyric record |
| First hook or return anchor | **Measured** for 98; no hook found in 7 | Two readings of the same record, ruled where they differed |
| Section order and lengths | **Measured**: section order and lengths in seconds for 98 (one reader's map, table 4b-2); lengths in felt bars for the 79 to 83 that also have a resolved felt tempo | Same record plus the felt tempo |
| How densely the rapper rides the beat | **Measured** as syllables per second for 97 and per felt beat for 82 | Same record; syllables estimated from spelling |
| Vocal density between sections | **Measured by section type**: verse against hook, words per second, for 87 (M-2). Not computed for each return of a section | Same record |
| How the performance changes between sections | **Documented only**: cited delivery observations on 54 songs and page statements on 64 (M-12); return codes in table 4c. Not measured | Page text and cited sources |
| Where phrases start and stop against the drums; where rhymes land | **Unknown** | Needs word-level timing against the audio |
| Silence after punchlines | **Unknown for 100/100** | Line-level timing cannot show a gap inside or after a line |
| Changes in drums, 808, melody, doubles and ad-libs when a section returns | **Unknown** at the layer level. Documented instead (M-11): a beat switch on 18 songs, and, in the earlier pass's coding of what changes between sections, a beat or bed change on 14 of 26 coded songs | Needs the full recording or stems |
| Which change is audible enough to matter | **Unknown for 100/100** as a listening judgment, because nobody listened. What sources single out is coded for 26 tracks in table 4c (M-11), and 1 more is coded as naming no specific change | — |
| A hook that is absent vs one that is unverified | **Separated**: "none" in table 4b means the record was read and no returning block was accepted (6 where both readings agree, 1 where a second reader ruled); "no matching record" means there was no usable record | — |

`05-measurement-method.md` says how each measured row was produced and checked.

## Production judgment used in the process (not measured) [J]

- **Rhyme placement:** stressed rhyme syllables on or just after the snare; internal rhymes mid-bar; the last word kept clean with air after it. This is standard rap-writing craft, and the hits neither prove nor disprove it.
- **Silence before or after the punchline as an accent**, instead of an ad-lib.
- **The punch-in method:** hook first and comped (the opening verse first when the song opens on a verse), 4-felt-bar punch units, one-felt-bar pre-roll, never mid-chain, mic position marked.
- **Ad-lib density:** at most one per felt bar in verses, and only in gaps.
- **One audible change per block boundary**, with the biggest before the last hook.
- **At least one pocket change per verse.**
- **Rough-mix checks:** phone speaker, mono, car; carve 2–4 kHz in the beat under the lead; high-pass the vocal at 80–100 Hz.
- **Drill-specific choices:** pickups, 808-slide space, phrase-level punching.
- **Every "Try it" above**, including the 2:45–3:30 demo length (informed by M-10, but a judgment) and the syllable budget (informed by M-2).

## Definitions and method notes

- **Basis codes for measured values** are in table 4b: feel **M / L / I / ?**; lyric timing **A / J / G / X**. Definitions are in `05-measurement-method.md`.
- **Basis ladder for documented facts:**
  - **P**: after the skeptic's check, the saved Wikipedia or Songfacts page text states the fact or names the work, and the quoted words were found in the saved page. A P can rest on a supported verdict, on a partly supported one (the page states the core; the detail it does not state is not counted; this includes verdicts the skeptic downgraded from supported), on a new page statement, or on a claim recoded to what the page states (1 opening). `05-measurement-method.md` gives the split.
  - **S**: a cited source supports the claim and the earlier verifier did not reject it. These were read through web-search summaries.
  - **U**: cited but not confirmed, or contradicted by page text. Kept for transparency, never counted.
  - **R**: unverified recollection. Never counted.
  - **?**: unknown.
- **Grid BPM:** the fastest steady pulse that carries the beat, which is what a DAW project would be set to. **Felt BPM:** the backbeat tempo, with the snare or clap on beats 2 and 4. On a slow pocket the grid is double the felt tempo.
- **Felt bar:** four felt beats. Bar counts in this file are felt bars; double them for a doubled DAW grid.
- **Hook:** the main block of lyric that comes back in substantially the same words. **Return anchor:** the first line of *any* block that comes back. **Hook before the first verse:** no verse section starts before the first hook; a short intro, tag or sample may come before it.
- **Borrowings** are typed as sample, interpolation, dialogue clip or self-reuse. Page-supported credits count, as do the 2 credits the earlier verifier added from search summaries and credits cited by research that were not flagged; unconfirmed and rejected credits do not.
- **Return-change coding** (M-11) is mine, from the cited descriptions. Each song's code is in `scripts/corrections.py` (`RETURN_TYPES`, `RETURNING`).
- **Second credited vocalist** = the Billboard credit names at least two vocalists. Producer-only credits such as Metro Boomin don't count.
- **Style tags** (trap, West Coast bounce, boom-bap/verse-led, pop-rap, R&B-rap, drill, Jersey club, rage) were assigned by the research agents from source descriptions and credits. They're descriptive, not Billboard categories.
- **Earlier re-check reports** from the search-based pass are kept in `data/raw/` (`recheck_sweep_claims.md`, `recheck_classification.md`). They predate the page-level check and are superseded by it where the two differ.
