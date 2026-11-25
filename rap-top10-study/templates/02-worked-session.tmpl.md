# 2 — Worked session: 144 BPM grid, 72 BPM feel

An original bar map you can load into the DAW as markers. The beat, the bar map, and every demonstration lyric are original. The demo lines are there to show *placement* (where rhymes land, where the gap sits), so replace them with your own writing.

## Session math (set this up first)

| Item | Value |
|---|---|
| DAW tempo / meter | **144 BPM, 4/4** (the grid) |
| Felt pulse | **72 BPM** (half-time): the snare lands on grid beat 3 of every grid bar, which is felt beats 2 and 4 |
| 1 grid beat | 60 ÷ 144 = **0.4167 s** |
| 1 grid bar | 4 × 60 ÷ 144 = **1.6667 s** |
| 1 felt bar (one written "rap bar") | 2 grid bars = **3.3333 s** |
| Landmarks | 36 grid bars = 60.0 s exactly, so **grid bar 37 = 1:00.0**, **bar 73 = 2:00.0**, **bar 109 = 3:00.0** |
| Formula | start time of grid bar *n*, beat *b* = (n − 1) × 1.6667 + (b − 1) × 0.4167 s |

Bars are counted on the 144 grid, as requested. The felt-bar column is there because you write in felt bars: a "16" at this tempo is 16 felt bars = 32 grid bars = 53.3 s.

**The beat (original; build it or brief a producer):** a 4-grid-bar loop (2 felt bars). The parts:
- A minor-key keys/pluck figure (F minor works).
- 808 on the roots, with a slide into grid bar 4.
- Kick on grid beat 1, plus a pickup on the last 16th of beat 2.
- Clap/snare on grid beat 3.
- Hats in grid 8ths, with a 16th or triplet roll at the end of every second grid bar.

Leave 1–4 kHz open in the melody so the voice has its own lane.

## Bar map

| Block | Grid bars (144) | Grid count | Felt bars (72) | Felt count | Start | End |
|---|---|---|---|---|---|---|
| Intro — beat with the 808 filtered out (A: title tag at 3.1 · B: pickup at 4.4½) | 1–4 | 4 | 1–2 | 2 | 0:00.0 | 0:06.7 |
| Block 1 — **A:** Hook 1 · **B:** Verse 1a (cold image) | 5–20 | 16 | 3–10 | 8 | 0:06.7 | 0:33.3 |
| Block 2 — **A:** Verse 1a · **B:** Hook 1 | 21–36 | 16 | 11–18 | 8 | 0:33.3 | 1:00.0 |
| Verse 1b — pocket change 1 (triplet run) | 37–44 | 8 | 19–22 | 4 | 1:00.0 | 1:13.3 |
| Verse 1c — home pocket; ends on silence | 45–52 | 8 | 23–26 | 4 | 1:13.3 | 1:26.7 |
| Hook 2 — title phrase doubled | 53–68 | 16 | 27–34 | 8 | 1:26.7 | 1:53.3 |
| Verse 2 — home pocket, pocket change 2 at felt bars 39–40 | 69–84 | 16 | 35–42 | 8 | 1:53.3 | 2:20.0 |
| Drop — full mix out | 85–86 | 2 | 43 | 1 | 2:20.0 | 2:23.3 |
| Hook 3 — full stack, ad-lib answers | 87–102 | 16 | 44–51 | 8 | 2:23.3 | 2:50.0 |
| Outro — beat rides out | 103–106 | 4 | 52–53 | 2 | 2:50.0 | 2:56.7 |

Total length is **2:56.7**. That deliberately sits at the short end of the measured range. It is just under the 25th percentile of the runtimes (Q1 = {{ q('all','runtime','q1') }}). The median is {{ q('all','runtime','median') }} (n = {{ g('all','runtime')['n'] }}): album-bomb cuts have a median of {{ q('album_bomb','runtime','median') }}, other songs {{ q('not_bomb','runtime','median') }}, and songs that climbed into the top 10 {{ q('climbers','runtime','median') }} (see the findings, M-10). **[J]** A tight demo is easier to judge and easier to finish in one session.

### How this map sits against the measured hits

| Block | This map | The measured hits | Finding |
|---|---|---|---|
| Felt tempo | 72 on a 144 grid | Median felt {{ q('all','felt_clear','median','{:g}') }} across {{ g('all','felt_clear')['n'] }} clear clips; published BPMs usually show the doubled number | M-1 |
| Intro | 2 felt bars (6.7 s) | Median {{ q('all','intro_len_bars','median','{:.1f}') }} felt bars, middle half {{ q('all','intro_len_bars','q1','{:.1f}') }}–{{ q('all','intro_len_bars','q3','{:.1f}') }}. This map uses two, half the four that step 3 of the process recommends, to keep the demo short [J]. For the standard intro, repeat it to grid bars 1–8 and move everything after it back 4 grid bars (6.7 s) | M-4 |
| First vocal | 0:03.3 (A) or 0:06.5 (B) | First lyric line within 5 s in {{ g('all','first_line_le_5s') }}. Opening B comes later than that, because nothing is said over its intro | M-4 |
| First hook | 0:06.7 (A) or 0:33.3 (B) | Median {{ q('all','first_hook','median') }} overall; {{ q('climbers','first_hook','median') }} for the songs that climbed. Opening A is hook-first, like {{ g('climbers','hook_before_first_verse') }} of the climbers, but earlier than their middle half ({{ q('climbers','first_hook','q1') }}–{{ q('climbers','first_hook','q3') }}); Opening B sits near the overall median | M-3 |
| Hook length | 8 felt bars | About 8 felt bars in {{ sm('all','hook1_len_bar_bands_map','7-9 (about 8)') }} of {{ g('all','hook1_len_bars_map')['n'] }} mapped songs, about 4 in {{ sm('all','hook1_len_bar_bands_map','3-5 (about 4)') }} | M-5 |
| Verse 1 | 16 felt bars in one run (A); 8 before Hook 1 and 8 after it (B) | About 16 in {{ sm('all','verse_len_bar_bands','14-18 (about 16)') }}, about 12 in {{ sm('all','verse_len_bar_bands','10-14 (about 12)') }}, about 8 in {{ sm('all','verse_len_bar_bands','6-10 (about 8)') }} of {{ g('all','first_verse_len_bars')['n'] }} | M-5 |
| Verse 2 | 8 felt bars (A: shorter than verse 1; B: the same length as each 8-bar verse part) | Verse 2 is shorter in {{ num(g('all','verse2_shorter')) }}, similar in {{ num(g('all','verse2_similar')) }} and longer in {{ num(g('all','verse2_longer')) }} of {{ den(g('all','verse2_longer')) }}. The long version below evens it out | M-6 |
| Hook occurrences | 3, same words, full stack on the last | Two or three in most songs; words identical or nearly so in {{ sm('all','hook_return','identical') + sm('all','hook_return','minor_variation') }} of {{ sm('all','hook_return','identical') + sm('all','hook_return','minor_variation') + sm('all','hook_return','extended') + sm('all','hook_return','shortened') + sm('all','hook_return','new_lyrics') }} | M-6 |

The map was drawn before these measurements and has not been changed. Where it leaves the middle of the range, that is a choice **[J]**: a two-felt-bar intro, and with it Opening A's early hook and Opening B's 6.5-second first vocal; a short second verse in Opening A; and a runtime just under the 25th percentile. The process (step 3) and M-4 default to a four-felt-bar intro; this demo halves it to keep the A/B test short.

**Long version (3:23.3):** insert a 16-grid-bar Verse 2b (8 felt bars) after grid bar 84, then move the drop, Hook 3 and the outro back 16 grid bars:
- drop: grid 101–102 (2:46.7–2:50.0);
- Hook 3: grid 103–118 (2:50.0–3:16.7);
- outro: grid 119–122 (3:16.7–3:23.3).

Every event before grid bar 85 is unchanged.

## Event map: first vocal, hook, pocket change, breaths, punches, silence

| Opening | Event | Grid bar.beat | Felt bar | Time |
|---|---|---|---|---|
| A | FIRST VOCAL — title phrase spoken dry, once | 3.1 | 2 | 0:03.3 |
| B | FIRST VOCAL — verse pickup on the last 8th of the intro · punch P1 drops in at 4.4 (pre-roll from 3.1) | 4.4½ | 2 | 0:06.5 |
| A | HOOK 1 downbeat (808 enters) | 5.1 | 3 | 0:06.7 |
| both | Breath — end of felt bar 4 | 8.4 | 4 | 0:12.9 |
| both | Breath — end of felt bar 6 | 12.4 | 6 | 0:19.6 |
| B | Punch P1b — second half of the cold verse (pre-roll from 11.1, 0:16.7) | 13.1 | 7 | 0:20.0 |
| both | Breath — end of felt bar 8 | 16.4 | 8 | 0:26.3 |
| B | Title phrase first heard — last word of the cold verse, on the snare | 19.3 | 10 | 0:30.8 |
| both | Breath — end of felt bar 10 | 20.4 | 10 | 0:32.9 |
| B | HOOK 1 downbeat | 21.1 | 11 | 0:33.3 |
| A | Verse 1a · punch P2 (pre-roll from 19.1) | 21.1 | 11 | 0:33.3 |
| both | Breath B1 | 24.4 | 12 | 0:39.6 |
| both | Breath B2 | 28.4 | 14 | 0:46.3 |
| A | Punch P2b — second half of Verse 1a (pre-roll from 27.1, 0:43.3) | 29.1 | 15 | 0:46.7 |
| both | Breath B3 | 32.4 | 16 | 0:52.9 |
| both | Breath B4 — full breath before the run | 36.3½ | 18 | 0:59.4 |
| both | **POCKET CHANGE 1** — triplet run starts · punch P3 | 37.1 | 19 | 1:00.0 |
| both | Breath B5 — catch breath inside the run | 40.4 | 20 | 1:06.3 |
| both | Breath B6 — before the return | 44.4 | 22 | 1:12.9 |
| both | Pocket returns home · punch P4 | 45.1 | 23 | 1:13.3 |
| both | Breath — end of felt bar 24 | 48.4 | 24 | 1:19.6 |
| both | Verse 1 punchline — last word on the snare | 51.3 | 26 | 1:24.2 |
| both | **SILENCE** — vocal and 808 out, hats and clap keep time (≈2.3 s, to 1:26.7) | 51.3½ | 26 | 1:24.4 |
| both | HOOK 2 downbeat · paste point P5 (the comped Hook 1) | 53.1 | 27 | 1:26.7 |
| both | Breath — hook answer bar | 56.4 | 28 | 1:32.9 |
| both | Breath — hook answer bar | 60.4 | 30 | 1:39.6 |
| both | Breath — hook answer bar | 64.4 | 32 | 1:46.3 |
| both | Breath — before Verse 2 | 68.4 | 34 | 1:52.9 |
| both | Verse 2 · punch P6 | 69.1 | 35 | 1:53.3 |
| both | Breath | 72.4 | 36 | 1:59.6 |
| both | Breath | 76.4 | 38 | 2:06.3 |
| both | **POCKET CHANGE 2** — half-density 8ths, rhymes on the snare only · punch P7 | 77.1 | 39 | 2:06.7 |
| both | Breath | 80.4 | 40 | 2:12.9 |
| both | Pocket returns home | 81.1 | 41 | 2:13.3 |
| both | Breath — before the drop | 84.4 | 42 | 2:19.6 |
| both | Drop — full mix out for one felt bar | 85.1 | 43 | 2:20.0 |
| both | HOOK 3 downbeat · paste point P8 (comp + full stack) | 87.1 | 44 | 2:23.3 |
| both | Breath — hook answer bar | 90.4 | 45 | 2:29.6 |
| both | Breath — hook answer bar | 94.4 | 47 | 2:36.3 |
| both | Breath — hook answer bar | 98.4 | 49 | 2:42.9 |
| both | End of song (end of felt bar 53) | 106 end | 53 | 2:56.7 |

Punches go in **4-felt-bar units** (8 grid bars), each with a **one-felt-bar pre-roll**. Hooks are not punched: you track Hook 1 straight through and paste the comp into Hooks 2 and 3. So the verse punch points are P2, P2b, P3, P4 in Opening A and P1, P1b, P3, P4 in Opening B, then P6 and P7 in Verse 2. Breaths sit at the end of every second felt bar (grid beat 4). B4 is the one exception: it moves half a grid beat earlier (36.3½) for a full breath before the run. B5 (40.4) is the catch breath inside it.

## The two openings (same beat, same body after 1:00)

The openings differ only before grid bar 37: in the intro vocal (A: the dry title phrase at 3.1; B: the verse pickup at 4.4½) and in the order of the two 16-grid-bar blocks. Everything from grid bar 37 (1:00.0) onward is identical. That makes this a clean A/B test, and you can keep both: one as the single edit, one as the album version.

### Opening A — hook-first ("say the name before anything else")

- **0:03.3 (grid 3.1):** you say the title phrase once, dry, over the filtered beat. That is the first vocal.
- **0:06.7 (grid 5.1):** the 808 enters and Hook 1 starts.
- **0:33.3:** Verse 1a.

Demonstration hook (8 felt bars: four lines, each line in one felt bar with the answer space in the next):

> **Load-bearin'** — pull me out, watch the whole house *fold* &nbsp;&nbsp;(space / ad-lib answer)
> Rebar in my back, I was poured in the *cold* &nbsp;&nbsp;(space)
> **Load-bearin'** — every beam in the frame know my *weight* &nbsp;&nbsp;(space)
> Whole city backed up like the Brent Spence — &nbsp;&nbsp;·&nbsp;&nbsp; *wait.*

What it demonstrates:
- The title phrase starts on the Hook 1 downbeat (grid 5.1): "Load" takes the downbeat, and the open vowel in "bear" follows straight after it.
- The end words *fold / cold* and *weight / wait* rhyme hard.
- The last line drops its final word after a beat of space. "Wait" pays off "weight" and the bridge-traffic image together, and the gap lets it land.

### Opening B — image-first ("make them lean in, then give them the name")

- **0:06.5 (grid 4.4½):** the verse pickup. That is the first vocal.
- The cold verse opens with the sharpest image you have and ends on the title phrase.
- **0:30.8 (grid 19.3):** the title phrase is the last word, on the snare.
- **0:33.3 (grid 21.1):** Hook 1 starts.

Demonstration cold-verse opening (felt bars 3–6):

> Floodwall murals — they ain't never painted *me*
> So I paint it in the booth, every shade that they ain't *see*
> **Cold** concrete — they **told** on me, the **load's** on me
> **Hold** the beam while the **whole** street swore it **owed** to me

What it demonstrates:
- **Dense internal rhyme:** a long-O chain (cold / told / load's / hold / whole / owed) runs inside the bars, under the *on me / to me* end chain. Cold, told and hold are full rhymes; load's, whole and owed share the vowel without the full rhyme.
- **Pointed local imagery:** the Covington floodwall murals.
- **Bars 7–10 build to the title phrase as the last word on felt beat 2 of bar 10.** Felt beats 3–4 then stay empty (≈1.7 s) before the hook downbeat.

## Pockets used in this session

Felt bar at 72 BPM, counted in felt 16ths (one felt 16th = one grid 8th):

```
felt beat:   | 1  e  &  a  | 2  e  &  a  | 3  e  &  a  | 4  e  &  a  |
drums:         K             S             k             S
home pocket:   x  .  x  x    X  .  x  x    x  .  x  x    X  .  -  -
                             ^rhyme                      ^last word, then air
triplet run:   x x x x x x   x x x x x x   x x x x x x   x x x x x x
               (16th-note triplets at 72 = grid 8th-note triplets at 144; 7.2 syllables/s with every slot filled.
                In felt bars 20 and 22 leave the last three slots empty for breaths B5 and B6: about 6.8/s over the run.)
half-density:  x  .  x  .    X  .  x  .    x  .  x  .    X  .  -  .
                             ^rhyme                      ^rhyme, then air (2.1 syllables/s)
```

- **Home pocket (verses 1a, 1c, 2):**
  - About 3 syllables per second as drawn (10 of the 16 felt-16th slots). A fully packed 16th bar is 4.8 per second, against 7.2 for the triplet run.
  - Measured hit verses run at a median {{ q('all','verse_sylls_per_s','median','{:.1f}') }} syllables a second (middle half {{ q('all','verse_sylls_per_s','q1','{:.1f}') }}–{{ q('all','verse_sylls_per_s','q3','{:.1f}') }}; findings, M-2). At 72 that is 13 to 14 of the 16 slots. So the drawing is the *open* version of the pocket: fill toward 13 slots when a bar should read dense, and keep the last two clear. [J]
  - Stressed rhyme syllables sit **on the snare (felt 2 and 4)** or the 16th after it.
  - Internal rhymes go on the "&" of 1 and 3.
  - The back half of felt beat 4 stays open every second bar, for a breath or an ad-lib.
- **Triplet run (verse 1b, grid 37–44, 1:00.0–1:13.3):**
  - Four felt bars of 16th-note triplets.
  - Carry one rhyme family through all four bars. The density is the change, so don't change the subject at the same time.
  - No ad-libs inside the run.
  - At 1:13.3 (grid 45.1), drop back to the home pocket. The return is what makes the run audible.
- **Half-density pocket (verse 2, grid 77–80, 2:06.7–2:13.3):**
  - Two felt bars of 8th-note phrasing, about 2 syllables per second, with rhymes only on the snare.
  - It is the opposite move to the triplet run: space instead of density. It suits a punchline you want heard, because the last word of felt bar 40 lands on the snare at grid 80.3 (2:12.5) with air behind it.
  - No ad-libs in it. The space is the point.
  - At 2:13.3 (grid 81.1), return to the home pocket for the last two felt bars before the drop.

## Where silence does more than an ad-lib: 1:24.4–1:26.7

Verse 1's final punchline lands its last word on the snare at **grid 51.3 (1:24.2)**. Then everything vocal stops, and the 808 mutes for the rest of grid bar 51 and all of grid bar 52. Hats and clap keep time. Hook 2 hits at **grid 53.1 (1:26.7)**.

**Why silence instead of an ad-lib:**
- The last word *is* the image. An ad-lib there just restates it.
- 2.3 s of air lets the listener finish the thought themselves.
- It turns the Hook 2 downbeat into a release rather than one more event.

**Test it:** bounce 1:20–1:30 twice, once with the silence and once with your best ad-lib in that gap. Play each three times in random order. Keep the version that makes you want to rewind to the punchline.

A second, arrangement-level silence comes at **2:20.0–2:23.3** (grid 85–86): the full mix drops for one felt bar before Hook 3. Either leave it empty, or put the title phrase there once, dry. Not both.

## Punch plan for a one-session record (built for punch-in tracking)

1. **Recording order:**
   - **Opening A:** hook first.
   - **Opening B:** the cold verse first (P1, P1b), then the hook. The cold verse sets the voice for the whole song.
2. **Hook:**
   - Track Hook 1 straight through, 3 passes. Comp one lead and one double, on the title phrase and end words only.
   - Paste the comp into Hook 2 and Hook 3. Hook 3 gets the full stack: lead, double, ad-lib answers.
3. **Verse 1:**
   - Do two full passes for feel, then punch in 4-felt-bar units, each with a one-felt-bar pre-roll: **P2, P2b, P3, P4** (Opening A) or **P1, P1b, P3, P4** (Opening B).
   - Never punch in the middle of an internal-rhyme chain. If one word in a chain is wrong, re-punch the whole 4-felt-bar unit from its punch point.
4. **Verse 2:** punch at P6 and P7 the same way. P7 is also where pocket change 2 starts, so the punch catches the change cleanly.
5. **Opening A tag:** record the dry title-phrase line (grid 3.1) after Verse 2, as the last lead line, once your voice matches the hook take.
6. **Ad-libs last.** Use only the gaps marked above, at most one per felt bar in the verses. None in the triplet run, none in the half-density bars, and none in the 1:24 silence.

Mic and consistency rules for punching:
- Mark your floor position.
- Keep the same distance and the same input gain all session.
- Crossfade punches at breaths, not consonants (10–20 ms).
- Re-punch the whole 4-felt-bar unit rather than a single word if the room tone or energy jumps.

## Listening test: choose between Opening A and Opening B

1. **Bounce both openings** from 0:00 to 1:00, with the same mix, loudness-matched within 0.5 LU. Play from a phone speaker.
2. **Get 4 or 6 cold listeners and split them evenly.** Each listener hears **one** opening only. Once someone has heard the title and the hook, the other opening is no longer cold for them.
3. **Run the test** with each listener:
   - **Stop at 0:15** and ask: (a) "What do you think the song is called, or what one line or image do you remember?" Note whether they gave the title or an image.
   - **Play to 1:00** and ask: (b) "Say or sing the hook." (c) "Want to hear the rest?"
4. **Score each listener** (5 at most, and both openings can earn every point):
   - Names the title *or* says back a line or image at 0:15: **2**
   - Hook said back at 1:00: **2**
   - "Yes" to hearing the rest: **1**
5. **Decide:**
   - Average the scores for each opening (total ÷ the listeners who heard it). The higher average wins.
   - **Tie:** the opening with more "yes" answers to (c) wins.
   - **Still tied, or within half a point:** keep both. Use A as the single or short-form edit and B as the album version. They share everything after 1:00, so you lose nothing. The notes from question (a) tell you what each opening plants: usually the title for A and an image for B.
6. **Only three listeners:** play both openings to each, alternating the order, but score only the first one each person hears. After the second, ask "Which would you keep playing?" and use that as the tie-break.
7. **Testing alone:** you already know both, so recall cannot be scored. Wait at least 12 hours, play each from the top, and note the timestamp where you first feel the urge to skip or check your phone. The opening that pushes that moment later wins.
