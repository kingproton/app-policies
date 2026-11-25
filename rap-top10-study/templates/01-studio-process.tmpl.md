# 1 — Studio process: first beat loop → recorded demo

Built for King D Bird's way of working:
- you punch in, often finishing in one session;
- you write pointed imagery and dense internal rhymes;
- you favor pockets that leave room for the last word or an ad-lib to land.

**Evidence tags:**
- **[M-n]** = backed by a finding in `03-findings.md`, with counts out of the songs actually assessed. M-1 to M-6, M-9 and M-10 are measured from clips, catalog data and time-synced lyric records; M-7, M-11 and M-12 are documented in published pages; M-8 uses both.
- **[J]** = my production judgment. It was not measured, and the hits don't prove it. Every rule of thumb, timing target and mix setting below is [J] unless a tag says otherwise.

Nothing here claims a technique *causes* chart success. The measured items describe what these 100 hits have in common.

---

## The one-page checklist (keep this open beside the session)

| # | Step | Do this | Listen for on playback | If it falls flat (one fix) |
|---|---|---|---|---|
| 0 | **Set up** | Time one felt bar (snare to the second snare after it): felt BPM = 240 ÷ seconds. Set the grid, note both tempos. Markers at every block start. Mark your mic spot. | Snare on felt beats 2 and 4, bar after bar; markers on downbeats. | Snare on 1 and 3: slide the loop one felt beat. |
| 1 | **Beat + pocket** | Clap 2 and 4 and name the felt tempo ({{ cls('all','feel_class_clear','slow') }} of {{ g('all','feel_basis')['M'] }} clear clips are slow; the median of the {{ g('all','feel_basis')['M'] }} is {{ q('all','felt_clear','median','{:g}') }}) [M-1]. Rap an old 4 bars laid back, on top and double-time. Keep the beat that leaves a hole for your last word. | Stressed syllable on or just after the snare? A gap at the end of every second felt bar? | Mute the 808 for the last beat of every second felt bar. |
| 2 | **Central phrase** | Write 10 candidates of 4 words or fewer. Keep the one that is a picture, fits one breath and has an open vowel on a strong beat. Say it 8 times over the loop. | Could a stranger say it back after one phone-speaker listen? | Cut a word so it fits one breath. |
| 3 | **Hook or verse first** | Single: title phrase inside 15 s. {{ num(g('climbers','first_anchor_le_15s')) }} of {{ den(g('climbers','first_anchor_le_15s')) }} climbers have a returning line by 0:15; their median first hook is {{ q('climbers','first_hook','median') }} [M-3]. Statement record: sharpest image first, a return anchor by 0:30. Intro of 4 felt bars, or 8 [M-4]. | At 0:15, does a cold listener know the title or one image? | Put a dry, one-bar title phrase in the intro. |
| 4 | **Verse** | Write in 4-felt-bar units: set-up, set-up, turn, payoff. About {{ '%.0f' % (g('all','ride_slow')['sylls_per_beat'] * 4) }} syllables a felt bar in a slow pocket [M-2]. Verse 1 of 8, 12 or 16 felt bars [M-5]. One pocket change per verse. | Do internal rhymes blur? Does every 4th bar pay off? | Drop one internal rhyme from a crowded bar. |
| 5 | **Transitions** | Keep the hook's words fixed [M-6]. Change its edges: drum drop, 808 cut, filter, new bed or new voice. Biggest change before the last hook. | Does each hook arrival lift? Fatigue around 1:30? | Mute the drums for the felt bar before Hook 2. |
| 6 | **Punch the lead** | Hook first, then comp it (verse-first opening: opening verse, then hook). Two full verse passes, then punch 4-felt-bar units at breaths with a one-bar pre-roll. Never mid-rhyme-chain. | Energy, mic distance and room tone match; breaths intact; no clipped consonants. | Re-punch the whole 4-bar unit. |
| 7 | **Ad-libs + doubles** | Ad-libs only in the gap after a last word, at most one per felt bar. Double the title phrase and hook end-words. Full stack on the last hook only. | Any ad-lib on a rhyme or punchline? Doubles smearing consonants? | Delete it. |
| 8 | **Rough mix** | Phone speaker, mono, car. Loudness-match the bounces. | Every word clear at low volume; title phrase clearest; 808 not masking the voice. | Dip 2–4 kHz in the beat under the lead. |
| ✓ | **Done when** | One bounce passes the 0:15 test (title or image) and the 1:00 test (hook said back). | | Re-run the A/B test in `02-worked-session.md`. |

**Tags:** [M-n] points to a finding in `03-findings.md`. Everything else on this page is production judgment [J].

---

## Step-by-step

### 0 — Session setup
- **Action:**
  - Find the felt tempo first: time one felt bar, from a snare to the second snare after it. Felt BPM = 240 ÷ that time in seconds (3.33 s is 72). Count snares or claps, not hats.
  - Set the DAW to the grid tempo you work on (144 for a 72 feel) and write the felt tempo next to it.
  - Under a half-time trap feel, one felt bar = 2 grid bars. At 144 BPM, one grid bar = 1.667 s and one felt bar = 3.333 s.
  - Put markers at every planned block start, colour the hooks, and add a punch track.
  - Trim the loop so the first kick sits on bar 1, beat 1.
- **Listen for:** with the click on, the snare should land on felt beats 2 and 4, bar after bar. One snare a bar or a snare on every beat means the tempo is an octave out: go back and time the felt bar again.
- **One fix:** if the snare lands on 1 and 3, the tempo is right and the start is wrong. Slide the loop, or the bar start, by one felt beat (half a grid bar, 0.833 s at 144).

### 1 — Choose the beat and the pocket
- **Action:**
  - Before writing new bars, rap something you already know over the loop in three pockets: laid back (just behind the snare), on top, and double-time.
  - Keep the beat and pocket where your stressed rhyme syllables can sit on or just after the snare, *and* where the drums leave a hole at the end of every second felt bar for your last word or an ad-lib.
- **Listen for:**
  - kick and 808 hits colliding with your stressed syllables every bar;
  - hi-hat rolls eating your consonants;
  - whether the felt pulse is in a range you can stay articulate in for 16 felt bars.
- **One fix:** if the last word keeps getting buried, mute the 808 for the last beat of every second felt bar.
- **What the hits show [M-1]:**
  - Measured from 30-second clips: {{ g('all','feel_basis')['M'] }} of {{ g('all','n_clip') }} show a clear backbeat (felt median {{ q('all','felt_clear','median','{:g}') }} BPM, middle half {{ q('all','felt_clear','q1','{:.0f}') }}–{{ q('all','felt_clear','q3','{:.0f}') }}). Of those, **{{ cls('all','feel_class_clear','slow') }} are slow**, {{ cls('all','feel_class_clear','mid') }} sit at {{ fr('mid') }} and {{ cls('all','feel_class_clear','fast') }} at {{ fr('fast') }}.
  - Published BPMs usually show double the felt number ({{ top('listing_vs_felt').get('listed at double the felt tempo', 0) }} of the clear clips that have a listing), which is your 144-grid, 72-feel convention.
  - Drake-credited songs supply {{ top('slow_by_artist').get('Drake', 0) }} of the {{ cls('all','feel_class_clear','slow') }} slow readings, so the slow pocket is partly one artist's habit.
- **Verse-led vs trap vs drill:**
  - *Verse-led:* only {{ g('style_verse_led','n_songs') }} songs carry the tag and just {{ sm('style_verse_led','feel_basis','M') }} of their clips are clear, so the data says little about their tempo. Sparse midrange lets density read, because the hats aren't fighting you. [J]
  - *Trap:* {{ cls('style_trap','feel_class_all_resolved','slow') }} of {{ g('style_trap','felt_all_resolved')['n'] }} trap-tagged songs with a resolved reading are slow (felt median {{ q('style_trap','felt_clear','median','{:.0f}') }}) [M-1]. Cadence, repetition and space for ad-libs matter more than syllable count. [J]
  - *Drill:* only two drill-tagged hits ("Barbie World", "Princess Diana"), and the tempo of "Barbie World" is unresolved ({{ conflict('Barbie World') }}). That's too few to call a pattern, so treat this as judgment: syncopated kicks and sliding 808s, lines that start as pickups *before* the downbeat, and space for the 808 slide. [J]

### 2 — Find the central phrase
- **Action:**
  - Write 10 candidates of four words or fewer.
  - Choose the one that is an *image* (something you can see), fits in one breath, and has a stressed open vowel you can put on a downbeat or the snare.
  - Say it eight times over the loop before you write anything around it.
- **Listen for:** whether a stranger could repeat it after one phone-speaker listen, and whether it still means something on the eighth pass.
- **One fix:** cut a word so it fits one breath, with the stress on the downbeat or the snare.
- **What the hits show:**
  - **[M-7]** {{ num(fs('all','borrow_documented')) }} of 100 songs have a documented borrowing: a sample, interpolation, dialogue clip or reused beat. In several, the page says the borrowing carries the chorus ("Janice STFU", "Staying Alive", "Super Gremlin", "Forever").{{ needv('Janice STFU','borrow_1','chorus') }}{{ needv('Staying Alive','opening','chorus') }}{{ needv('Super Gremlin','opening','choruses') }}{{ needv('Forever','borrow_1','chorus') }} Whether listeners already knew the borrowed record was not measured, and the rest are unknown, not "no".
  - **[M-6]** When the hook returns its words are identical or nearly so in {{ sm('all','hook_return','identical') + sm('all','hook_return','minor_variation') }} of {{ sm('all','hook_return','identical') + sm('all','hook_return','minor_variation') + sm('all','hook_return','extended') + sm('all','hook_return','shortened') + sm('all','hook_return','new_lyrics') }} tracks. The phrase you pick is the phrase you will repeat unchanged.
  - **[J]** For you, clearance cost makes an *original* signature the practical version: a replayed motif, a vocal chop of your own phrase, a consistent tag.

### 3 — Decide: open with the hook or the verse
- **Action:**
  - Decide by the record's job.
  - **Single or short-form:** the hook or title phrase should be heard within about the first 15 seconds, as a spoken tag or by going hook-first.
  - **Statement record (verse-led):** open on the sharpest image and give the listener a *return anchor* by about 0:30. That can be a refrain line, a chant, the title as a verse-ending tag, or a beat change.
  - Keep the intro to four felt bars (eight on your 144 grid), or eight if the record needs runway. The worked session uses a two-felt-bar intro as a tight-demo choice [J]; that is shorter than the measured middle half ({{ q('all','intro_len_bars','q1','{:.1f}') }}–{{ q('all','intro_len_bars','q3','{:.1f}') }} felt bars).
- **Listen for:** at 0:15, can a cold listener name the song or repeat one image?
- **One fix:** put a one-felt-bar, dry version of the title phrase into the intro (see Opening A in the worked session).
- **What the hits show:**
  - **[M-3]** {{ g('all','has_hook') }} assessed tracks have a recurring hook. It starts at a median {{ q('all','first_hook','median') }} and comes before the first verse in {{ g('all','hook_before_first_verse') }}.
  - **[M-3]** The {{ g('climbers','n_songs') }} songs that *climbed* into the top 10 reach the hook at a median **{{ q('climbers','first_hook','median') }}** and put it before the first verse in {{ g('climbers','hook_before_first_verse') }}; {{ num(g('climbers','first_anchor_le_15s')) }} of {{ den(g('climbers','first_anchor_le_15s')) }} have a returning line by 0:15. The songs that debuted there take {{ q('debuts','first_hook','median') }}. [J] I treat the climbers as the closest thing here to an independent single; nothing in the data tests that.
  - **[M-4]** The first lyric line arrives within 5 seconds in {{ g('all','first_line_le_5s') }} tracks, and it is usually an ad-lib, a sample or a spoken line rather than a rap bar. The intro before the first hook or verse runs a median {{ q('all','intro_len_bars','median','{:.1f}') }} felt bars.
  - **[M-9]** {{ g('all','no_hook') }} have no recurring hook at all; {{ num(g('style_verse_led','no_hook')) }} of those are verse-led-tagged records.
- **Verse-led vs trap vs drill:**
  - *Verse-led:* image-first is viable, but plan the return anchor. {{ num(g('style_verse_led','no_hook')) }} of the {{ den(g('style_verse_led','no_hook')) }} verse-led-tagged hits have no recurring hook. [M-9][J]
  - *Trap:* hook before the first verse in {{ g('style_trap','hook_before_first_verse') }} trap-tagged songs, so either order is normal; hook-first or tag-first suits a single. [M-3][J]
  - *Drill:* both drill-tagged hits put the hook before the first verse, at {{ hook('Barbie World') }} and {{ hook('Princess Diana') }} [M-3]. Two songs, so anything built on them is judgment. [J]

### 4 — Develop the verse
- **Action:**
  - Build in 4-felt-bar units: set-up, set-up, turn, payoff. The last word is the punch.
  - Run internal rhyme chains through the *middle* of bars and keep the final word clean.
  - Plan at least one pocket change per verse (every 8–16 felt bars): a density switch (e.g. a triplet run), a half-density bar, a stop-time bar, or a register change.
  - Give the punchline a felt beat of air. Silence before the last word works as an accent.
- **Listen for:**
  - Do internal rhymes blur at full speed?
  - Does every fourth bar pay off?
  - Does the pocket change register as a change, or just as "more words"?
- **One fix:** remove one internal rhyme from each crowded bar.
- **What the hits show:**
  - **[M-2]** Verses run at a median {{ q('all','verse_sylls_per_s','median','{:.1f}') }} syllables a second (middle half {{ q('all','verse_sylls_per_s','q1','{:.1f}') }}–{{ q('all','verse_sylls_per_s','q3','{:.1f}') }}), and that rate hardly changes with tempo. In a slow pocket it works out to about {{ '%.1f' % g('all','ride_slow')['sylls_per_beat'] }} syllables a felt beat. Verses are denser than hooks in {{ g('all','verse_denser_than_hook') }} tracks.
  - **[M-5]** First verses run a median {{ q('all','first_verse_len_bars','median','{:.0f}') }} felt bars, clustering near 8 ({{ sm('all','verse_len_bar_bands','6-10 (about 8)') }} tracks), 12 ({{ sm('all','verse_len_bar_bands','10-14 (about 12)') }}) and 16 ({{ sm('all','verse_len_bar_bands','14-18 (about 16)') }}). Most songs have two verses ({{ sm('all','n_verses','2') }}) or three ({{ sm('all','n_verses','3') }}).
  - **[M-6]** Verse 2 is shorter than verse 1 in {{ num(g('all','verse2_shorter')) }} tracks, similar in {{ num(g('all','verse2_similar')) }} and longer in {{ num(g('all','verse2_longer')) }} of {{ den(g('all','verse2_longer')) }}. There is no short-second-verse rule.
  - [J] If you're solo, a register or pocket change is your version of a guest verse, and a bed change under verse 2 is the producer's version.
- **Verse-led vs trap vs drill:**
  - *Verse-led:* first verses run long here, a median {{ q('style_verse_led','first_verse_len_bars','median','{:.0f}') }} felt bars across {{ g('style_verse_led','first_verse_len_bars')['n'] }} mapped songs [M-5]; flow switches every 8. [J]
  - *Trap:* a median {{ q('style_trap','first_verse_len_bars','median','{:.0f}') }} felt bars [M-5], with repetition and call-and-response with ad-libs. [J]
  - *Drill:* a first verse of {{ bars('Princess Diana','first_verse_len') }} felt bars on "Princess Diana" and {{ secs('Barbie World','first_verse_len_s') }} seconds on "Barbie World" (no bar count: its tempo is unresolved) [M-5]; front-loaded with pickups, staccato endings. [J]

### 5 — Arrange the transitions
- **Action:**
  - Give every block boundary one audible change: a drum drop, an 808 cut, a filter sweep, a new bed, or a new voice.
  - Put the biggest change in the last third, before the final hook.
- **Listen for:** "same beat for three minutes" fatigue around 1:30, and whether each hook arrival actually lifts.
- **One fix:** mute the drums for the last felt bar before Hook 2.
- **What the hits show:**
  - **[M-6]** The hook's words come back identical or with small changes in {{ sm('all','hook_return','identical') + sm('all','hook_return','minor_variation') }} of {{ num(g('all','has_hook')) }} tracks. The last hook is at least a quarter longer than the first in only {{ g('all','last_hook_longer') }} ({{ num(g('drake_credit','last_hook_longer')) }} of those {{ num(g('all','last_hook_longer')) }} are Drake-credited). Lyric timing cannot hear what surrounds the hook, so whether drums, 808 or doubles change there was not measured; putting the change at the hook's edges is judgment. [J]
  - **[M-6]** A stretch of 12 seconds or more between transcribed lines appears in {{ g('all','gap_ge_12s') }} tracks. It can be a break or a beat change, but also a passage the transcriber left out, so treat it as a hint.
  - **[M-11]** {{ bs_n() }} songs have a documented beat switch ({{ bs_page_n() }} on saved page text), {{ bs_by('Drake') + bs_by('Kendrick') }} of them on Drake- or Kendrick Lamar-credited records.
  - [J] Treat a full switch as a statement-record move. A one-bar drop is the single-sized version.

### 6 — Punch the lead (one-session workflow)
- **Action:**
  - Track the hook first (3 passes), then comp one lead and one double. Paste it into every hook slot. If the song opens on a verse (Opening B in the worked session), track that opening verse first, then the hook.
  - For each verse, do two full passes for feel, then punch in 4-felt-bar units at marked breath points with a one-felt-bar pre-roll.
  - Punch on rests, never mid-rhyme-chain.
  - Keep the same mic distance (mark the floor) and the same gain all session; crossfade punches at breaths, 10–20 ms. [J]
- **Listen for:**
  - energy, mic distance and room tone matching across punches;
  - breaths that are intact;
  - first consonants that aren't clipped.
- **One fix:** re-punch the whole 4-bar unit rather than one word.
- **What the hits show [M-6][M-12]:** pasting one comped hook into every slot matches the measurement that hooks return with the same or nearly the same words [M-6]. Published accounts of how these records were tracked are thin and are collected in M-12.

### 7 — Place ad-libs and doubles
- **Action:**
  - Ad-libs go only in the gap after a last word (usually the back half of felt beat 4), at most one per felt bar in verses.
  - Double the title phrase and hook end-words; save full stacks for the last hook.
  - Leave at least one spot where **silence** answers the punchline instead of an ad-lib.
  - Pan ad-libs 30–60% L/R, sitting 6–10 dB under the lead. [J]
- **Listen for:** any ad-lib stepping on a rhyme or punchline, and doubles smearing consonants.
- **One fix:** delete the ad-lib that lands on the rhyme or punchline.
- **What the hits show [M-4]:** the first transcribed line is an ad-lib or vocalization in {{ sm('all','first_line_kind','adlib_or_vocalization') }} of {{ g('all','n_section_map') }} tracks, so an ad-lib often *is* the entrance. Placement inside the bar and the silence after punchlines could not be measured from line-level timing: unknown. The placement rules above are **[J]**.

### 8 — Check the rough mix
- **Action:**
  - Check on a phone speaker, in mono, and in the car. Bounce loudness-matched versions for A/B (around −12 to −10 LUFS integrated is fine for a demo; this is not mastering).
  - Before you judge, set the basics: high-pass the vocal at 80–100 Hz, de-ess, and ride each punchline up about 1 dB. [J]
- **Listen for:** every word intelligible at low volume; the title phrase the clearest word in the song; the 808 not masking the 100–250 Hz body of your voice.
- **One fix:** dip 2–4 kHz in the beat under the lead.

---

## Where the decisions split: verse-led vs trap vs drill

Counts are from the style-tagged groups: trap or melodic trap {{ g('style_trap','n_songs') }} songs, verse-led {{ g('style_verse_led','n_songs') }}, drill {{ g('style_drill','n_songs') }}. The drill column is judgment throughout.

| Decision | Verse-led | Trap | Drill |
|---|---|---|---|
| Tempo / feel | Too few clear clips to say ({{ sm('style_verse_led','feel_basis','M') }} of {{ g('style_verse_led','n_clip') }}); {{ cls('style_verse_led','feel_class_all_resolved','slow') }} of the {{ cls('style_verse_led','feel_class_all_resolved','slow') + cls('style_verse_led','feel_class_all_resolved','mid') + cls('style_verse_led','feel_class_all_resolved','fast') }} resolved readings are slow [M-1] | Slow pocket: felt median {{ q('style_trap','felt_clear','median','{:.0f}') }}, middle half {{ q('style_trap','felt_clear','q1','{:.0f}') }}–{{ q('style_trap','felt_clear','q3','{:.0f}') }} ({{ g('style_trap','felt_clear')['n'] }} clear clips) [M-1] | Two hits only: "Princess Diana" {{ pf('Princess Diana') }} (clear); "Barbie World" unresolved ({{ conflict('Barbie World') }}) [M-1] |
| Pocket | Straight felt 16ths; rhymes on 2 & 4 plus internal [J] | Triplets and repeated cadences; room for ad-libs [J] | Pickups into the bar; staccato; rests around 808 slides [J] |
| Central phrase | Refrain line, or no hook with a return anchor ({{ g('style_verse_led','no_hook') }} have no hook) [M-9] | Chant or title repetition; hook in {{ g('style_trap','has_hook') }} [M-3] | Ad-lib/catchphrase identity plus a short hook [J] |
| Opening | Sharpest image first [J] | Hook before verse 1 in {{ g('style_trap','hook_before_first_verse') }}; first hook at a median {{ q('style_trap','first_hook','median') }} [M-3] | Hook before verse 1 in both tagged hits [M-3]; tag or ad-lib, then pickup into the verse [J] |
| Verse length | Median {{ q('style_verse_led','first_verse_len_bars','median','{:.0f}') }} felt bars (n={{ g('style_verse_led','first_verse_len_bars')['n'] }}) [M-5] | Median {{ q('style_trap','first_verse_len_bars','median','{:.0f}') }} felt bars (n={{ g('style_trap','first_verse_len_bars')['n'] }}) [M-5] | {{ bars('Princess Diana','first_verse_len') }} felt bars on "Princess Diana"; {{ secs('Barbie World','first_verse_len_s') }} s on "Barbie World" [M-5] |
| Density | {{ q('style_verse_led','verse_sylls_per_s','median','{:.1f}') }} syllables a second [M-2] | {{ q('style_trap','verse_sylls_per_s','median','{:.1f}') }} syllables a second, about {{ q('style_trap','verse_sylls_per_beat','median','{:.1f}') }} a felt beat [M-2] | Staccato; leave rests [J] |
| Main change on return | Beat switch or new bed [J] | New voice or beat change; 808/drum drop [J] | 808 pattern/slide change, drum drop [J] |
| Punching | Longer takes (8 felt bars) to keep momentum [J] | Short punches are fine (cadences repeat) [J] | Punch by phrase *including* the pickup [J] |
| Ad-libs | Sparse; protect the bars [J] | Frequent; call-and-response [J] | Signature ad-libs in the gaps [J] |
| Rough-mix risk | Midrange clutter hiding words [J] | 808 masking the voice at low volume [J] | 808 slides fighting the vocal low-mids [J] |

## What this process cannot promise

- **Superstar album launches dominate the reference set.** {{ ST['debuts'] }} of the 100 debuted directly in the top 10, {{ ST['one_week_top10'] }} spent exactly one week there, and Drake is lead artist on {{ ST['lead_artists'][0][1] }}. Patterns that come mostly from album-bomb cuts describe what *superstar launches* sound like. The {{ g('climbers','n_songs') }} climbers are a closer but small, uncontrolled comparison ([M-8]).
- **Some listening-level details are still unknown.** Timing, section sizes, density and felt tempo are now measured (`05-measurement-method.md`). Not measured: {{ UNMEASURED() }}. Line-level lyric timing and 30-second clips cannot show them.
- **A clip is one section and a lyric record is one transcription.** Each measured number has a basis code in `04-reference-list.md`, table 4b. Lean on the medians, not on any single track.
