# 3 — Findings behind the process

These findings describe what the 100 most recent rap Hot 100 top-10 songs have in common. None of them claims that a technique *causes* chart success.

**How to read the counts:**
- Every count is **k / n assessed**. *n* leaves out tracks where the fact could not be measured or is unknown. Unknown never counts as "no".
- **Measured** findings (M-1 to M-6, M-9, M-10, and the timing rows of M-8) come from three sources read directly on 2026-11-25: Apple catalog durations, Apple's 30-second preview clips, and time-synced lyric records from LRCLIB. Nobody listened to the recordings; the numbers come from signal analysis of the clips and from reading the lyric records. `05-measurement-method.md` gives the method, the checks and the limits.
- **Documented** findings (M-7, M-11, M-12, and parts of M-8) come from what published pages say. A claim counts only when page text supports it (**P**) or a cited source was not rejected by the verifier (**S**). Claims that could not be confirmed (**U**) and recollection (**R**) are never counted.
- **Production judgment is labeled [J]:** every "Try it" block and the final section.

**What was assessed:**
- **Runtime:** {{ g('all','runtime')['n'] }} of 100 ({{ top('runtime_basis')['catalog'] }} from the Apple catalog, {{ top('runtime_basis').get('cited', 0) }} from cited sources).
- **Felt tempo:** {{ g('all','n_clip') }} preview clips. {{ g('all','feel_basis')['M'] }} show a clear backbeat; {{ g('all','feel_basis').get('L',0) + g('all','feel_basis').get('I',0) }} more are resolved with a stated caveat; {{ g('all','feel_basis').get('?',0) }} stay open. {{ cnt('clip_missing') }} tracks had no clip.
- **Lyric timing and structure:** {{ g('all','n_lyric') }} tracks have a time-synced lyric record whose length matches the track within 3 seconds. {{ 'Each record was' if not detector_only() else str(read_twice()) + ' of them were' }} read twice, by a repetition detector and by an independent AI reader; where the two disagreed, a second AI reader ruled. No person read them. Timing basis: {{ sm('all','lyric_basis','A') }} agreed (A), {{ sm('all','lyric_basis','J') }} ruled (J){{ ', ' + str(detector_only()) + ' detector only (G)' if detector_only() else '' }}. {{ cnt('lyric_missing') }} tracks had no matching record ({{ lst('lyric_missing', None, ' and ') }}){{ ' and ' + str(cnt('lyric_unusable')) + ' could not be resolved' if cnt('lyric_unusable') else '' }}.
- **Timestamps** are crowd-synced line times. Where two or more matching records exist ({{ ra('tracks_with_2plus_records') }} tracks), their first-line times agree within one second for {{ ra('first_line_within_1s') }}. Treat every timestamp below as good to about a second, not to the frame.
- **Not measured:** the silence after a punchline, where ad-libs sit inside a bar, and what the drums and 808 do when a section returns. Line-level lyric timing and a 30-second clip cannot show them. They stay unknown.

## Measured counts at a glance

{{ open_table('measured_table.md') }}

*Album-bomb* = a song that first entered the top 10 in the same chart week as at least two other songs by the same lead artist (an album-release week). *Climbed* = the song charted below the top 10 before first entering it. *Felt bars* are bars of four felt beats; on a doubled DAW grid (your 144 grid for a 72 feel) the bar count doubles. Style tags come from source descriptions, not from Billboard.

---

## Ranked patterns

Ranked by how directly each one changes a writing, arrangement or delivery decision, weighted by how many songs back it.

### M-1. The pocket is a slow backbeat: felt {{ q('all','felt_clear','q1','{:.0f}') }}–{{ q('all','felt_clear','q3','{:.0f}') }} BPM in the middle half, whatever the published BPM says

- **Effect:** delivery and writing. The felt pulse sets how long a bar lasts and where the snare answers you. Ranked first because it is the first decision in the session and the best-covered measurement.
- **Count:**
  - Of {{ g('all','n_clip') }} preview clips, **{{ g('all','feel_basis')['M'] }}** show a clear backbeat (a snare or clap on felt beats 2 and 4).
  - Of those {{ g('all','feel_basis')['M'] }}: **{{ cls('all','feel_class_clear','slow') }} are slow** (felt under 90), **{{ cls('all','feel_class_clear','mid') }} are mid-tempo** (felt {{ fr('mid') }}) and **{{ cls('all','feel_class_clear','fast') }} are fast** (felt {{ fr('fast') }}). Median felt tempo **{{ q('all','felt_clear','median','{:g}') }} BPM**, middle half {{ q('all','felt_clear','q1','{:.0f}') }}–{{ q('all','felt_clear','q3','{:.0f}') }}.
  - Adding the {{ g('all','feel_basis').get('L',0) + g('all','feel_basis').get('I',0) }} readings resolved with a caveat gives {{ cls('all','feel_class_all_resolved','slow') }} slow / {{ cls('all','feel_class_all_resolved','mid') }} mid / {{ cls('all','feel_class_all_resolved','fast') }} fast of {{ g('all','felt_all_resolved')['n'] }}.
  - **Published BPMs mostly show the doubled number.** Among clear clips with an earlier BPM listing, the listing sits at double the felt tempo for {{ top('listing_vs_felt').get('listed at double the felt tempo', 0) }}, at the felt tempo for {{ top('listing_vs_felt').get('listed at the felt tempo', 0) }}, at both for {{ top('listing_vs_felt').get('listed at double the felt tempo and listed at the felt tempo', 0) }}, and matches neither for {{ top('listing_vs_felt').get('listing matches neither', 0) }}. That is the "144 on the grid, 72 in the pocket" convention you already use.
- **Examples (pulse/felt from the clip):**
  - *Slow:* "Like That" {{ pf('Like That') }}, "Luther" {{ pf('Luther') }}, "Cinderella" {{ pf('Cinderella') }}, "Pushin P" {{ pf('Pushin P') }}, "Carnival" {{ pf('Carnival') }}, "Wait For U" {{ pf('Wait For U') }}.
  - *Mid:* "Paint The Town Red" {{ pf('Paint The Town Red') }}, "Hey Now" {{ pf('Hey Now') }}, "Squabble Up" {{ pf('Squabble Up') }}, "Circo Loco" {{ pf('Circo Loco') }}, "2 Hard 4 The Radio" {{ pf('2 Hard 4 The Radio') }}, "First Class" {{ pf('First Class') }}.
  - *Fast:* "Houdini" {{ pf('Houdini') }}, "Super Freaky Girl" {{ pf('Super Freaky Girl') }}, "Noid" {{ pf('Noid') }}.
- **Not resolved ({{ cnt('feel_unresolved') }}):** {{ lst('feel_unresolved', None, ', ') }}. Both readings fit the clip.
- **Resolved by range only ({{ cnt('feel_range_rule') }}):** the clip did not separate the two readings, and one of them falls outside 55–150 BPM: {{ lst('feel_range_rule', None, ', ') }}.
- **Try it [J]:**
  - Before you write, clap 2 and 4 against the loop at the felt tempo and say your central phrase over it. If the clap feels rushed, you are counting the doubled grid.
  - In a slow pocket, aim rhymes at the snare (felt beats 2 and 4) and leave the back half of beat 4 open. That is the room your last word or ad-lib needs.
- **Exception:** the {{ cls('all','feel_class_clear','fast') }} fast records keep a full snare on 2 and 4 at {{ fr('fast') }}. A fast, fully felt pulse leaves less room per syllable (see M-2): good for a chant, hard on dense bars. [J]
- **Flags:**
  - Drake-credited songs supply **{{ top('slow_by_artist').get('Drake', 0) }} of the {{ cls('all','feel_class_clear','slow') }}** clear slow readings.
  - A 30-second clip is one section. A beat switch elsewhere in the track is not seen, so a song with two beats has one of them measured.
  - **Drill:** only two list songs carry a drill tag ("Barbie World" and "Princess Diana"). Nothing about drill can be generalized from two songs.

### M-2. Mouth speed holds near four syllables a second; the beat decides how that feels

- **Effect:** writing (how many syllables a bar can hold) and delivery (pocket). Ranked second because it converts directly into a syllable budget.
- **Count:**
  - Across verse sections, the median track delivers **{{ q('all','verse_sylls_per_s','median','{:.1f}') }} syllables per second** (middle half {{ q('all','verse_sylls_per_s','q1','{:.1f}') }}–{{ q('all','verse_sylls_per_s','q3','{:.1f}') }}; n={{ g('all','verse_sylls_per_s')['n'] }}), or {{ q('all','verse_words_per_s','median','{:.1f}') }} words per second.
  - The rate barely moves with tempo: {{ '%.1f' % g('all','ride_slow')['sylls_per_s'] }} per second on slow beats (n={{ g('all','ride_slow')['n'] }}), {{ '%.1f' % g('all','ride_mid')['sylls_per_s'] }} on mid-tempo beats (n={{ g('all','ride_mid')['n'] }}), {{ '%.1f' % g('all','ride_fast')['sylls_per_s'] }} on the {{ g('all','ride_fast')['n'] }} fast ones.
  - So the **syllables per felt beat** change instead: about **{{ '%.1f' % g('all','ride_slow')['sylls_per_beat'] }}** on slow beats, **{{ '%.1f' % g('all','ride_mid')['sylls_per_beat'] }}** on mid-tempo beats and {{ '%.1f' % g('all','ride_fast')['sylls_per_beat'] }} on fast ones. A slow pocket fills most of the four sixteenth-note slots in a beat; at 100 BPM the same mouth speed sits between eighth notes and triplets.
  - A lyric line lasts **{{ q('all','verse_line_gap_s','median','{:.1f}') }} seconds** at the median (middle half {{ q('all','verse_line_gap_s','q1','{:.1f}') }}–{{ q('all','verse_line_gap_s','q3','{:.1f}') }}). In felt beats that is about four beats for {{ sm('all','verse_line_beats_bands','3.5-4.5 (about 4)') }} tracks and about two for {{ sm('all','verse_line_beats_bands','1.5-2.5 (about 2)') }} (of {{ g('all','verse_line_beats')['n'] }}).
  - Verses are denser than hooks in **{{ g('all','verse_denser_than_hook') }}** tracks: {{ q('all','verse_words_per_s','median','{:.1f}') }} words a second against {{ q('all','hook_words_per_s','median','{:.1f}') }}.
- **Examples:**
  - *Densest verses (words per second):* {{ lst('dense_verses', 5, ', ') }}.
  - *Sparsest:* {{ lst('sparse_verses', 5, ', ') }}.
- **Try it [J]:**
  - At a 72 feel, one felt beat is 0.83 seconds, so the median rate gives you about 3.4 syllables a beat and 13 to 14 a felt bar. Write the dense bar to that budget, then cut two syllables from the bar that carries the punchline so the last word has air.
  - Count one line you already like. At 72, 16 syllables a felt bar is 4.8 a second: only {{ top('verse_sylls_share')['above_4_8'] }} of {{ top('verse_sylls_share')['n'] }} verses in this set run faster. Ten a bar is 3.0 a second, which is about where hooks sit (median {{ '%.1f' % top('hook_sylls_per_s')['median'] }}).
- **Exception:** "All The Way" runs far above the rest and "K-POP" far below; both reached the top 10.{{ isfirst('dense_verses','All The Way') }}{{ isfirst('sparse_verses','K-POP') }} Density is a choice, not a requirement. [J]
- **Flags:**
  - Syllables are estimated from spelling, and section boundaries come from the repetition detector, so individual figures can be off by 10% or so. The medians are steadier than any single track.
  - Line timing cannot show where inside the bar a syllable falls, or the gap after a last word.

### M-3. Getting to the hook: two shapes, and the songs that climbed use the fast one

- **Effect:** arrangement (what comes first) and writing (how long the first verse can run). Ranked third: it is the hook-first or verse-first decision, now measured.
- **Count:**
  - **{{ g('all','has_hook') }}** assessed tracks have a main section that recurs. **{{ g('all','no_hook') }}** have none (see M-9).
  - The first hook starts at a median **{{ q('all','first_hook','median') }}** (middle half {{ q('all','first_hook','q1') }}–{{ q('all','first_hook','q3') }}). It has arrived by 0:30 in {{ g('all','first_hook_le_30s') }} tracks, by 1:00 in {{ g('all','first_hook_le_60s') }}, and comes after 1:30 in {{ g('all','first_hook_gt_90s') }}.
  - The hook comes **before the first verse** in **{{ g('all','hook_before_first_verse') }}** tracks with a section map. Within the first three lyric lines: {{ g('all','hook_first') }}.
  - **The first return anchor** (the earliest line of any block that comes back, hook or not) lands at a median {{ q('all','first_anchor','median') }}. In {{ num(g('all','anchor_is_hook')) }} of {{ den(g('all','anchor_is_hook')) }} tracks that anchor is the hook itself; in the rest an intro chant, tag or pre-hook returns first.
  - **By chart path:** songs that **climbed** into the top 10 reach the hook at a median **{{ q('climbers','first_hook','median') }}** (n={{ g('climbers','first_hook')['n'] }}) and put it before the first verse in {{ g('climbers','hook_before_first_verse') }}. Songs that **debuted** there: **{{ q('debuts','first_hook','median') }}** and {{ g('debuts','hook_before_first_verse') }}. Album-bomb cuts: {{ q('album_bomb','first_hook','median') }}; other songs: {{ q('not_bomb','first_hook','median') }}.
- **Examples with timestamps:**
  - *Hook first:* "First Class" (hook at {{ hook('First Class') }} after {{ lbh('First Class') }} line), "Type Shit" ({{ hook('Type Shit') }}), "BackOutsideBoyz" ({{ hook('BackOutsideBoyz') }}), "Barbie World" ({{ hook('Barbie World') }}), "Rather Lie" ({{ hook('Rather Lie') }}), "Pussy & Millions" ({{ hook('Pussy & Millions') }}), "Carnival" ({{ hook('Carnival') }}), "Players" ({{ hook('Players') }}, the first line of the record).
  - *Verse first, long wait:* "Not Like Us" (hook at {{ hook('Not Like Us') }} after {{ lbh('Not Like Us') }} lines), "Like That" ({{ hook('Like That') }} after {{ lbh('Like That') }}), "On BS" ({{ hook('On BS') }} after {{ lbh('On BS') }}), "National Treasures" ({{ hook('National Treasures') }} after {{ lbh('National Treasures') }}), "K-POP" ({{ hook('K-POP') }} after {{ lbh('K-POP') }}), "Houdini" ({{ hook('Houdini') }} after {{ lbh('Houdini') }}).
- **Try it [J]:**
  - Single or short-form: put a line that will come back inside the first 15 seconds. {{ num(g('climbers','first_anchor_le_15s')) }} of the {{ den(g('climbers','first_anchor_le_15s')) }} climbers have a returning line by then, and the hook itself has started by 0:15 in {{ num(g('climbers','first_hook_le_15s')) }} and by 0:30 in {{ num(g('climbers','first_hook_le_30s')) }}.
  - Statement record: you can hold the hook past a minute, as "Not Like Us" and "Like That" do{{ hook_after('Not Like Us', 60) }}{{ hook_after('Like That', 60) }}, but give the listener a return anchor earlier: a tag, a chant or a refrain line that will come back.
- **Exception:** "Not Like Us" spent {{ wk10('Not Like Us') }} weeks in the top 10 with its hook at {{ hook('Not Like Us') }}. A late hook did not stop it. [J]
- **Flags:**
  - "Which block is the hook" is a judgment when two blocks recur. The two readings disagreed on whether there is a hook or when it starts for {{ top('review_summary')['hook_time_disputed'] }} of {{ top('review_summary')['reviewed'] }} tracks before the ruling; those are marked J in table 4b.
  - Drake-credited songs put the hook before the first verse in {{ g('drake_credit','hook_before_first_verse') }}; the rest in {{ g('no_drake','hook_before_first_verse') }}. Album-bomb weeks pull the whole set toward later hooks.
  - Only {{ g('climbers','n_songs') }} songs climbed. The gap is large, but the group is small and not controlled.

### M-4. The first voice is rarely a rap line, and the intro is four or eight felt bars

- **Effect:** arrangement (the opening) and delivery (how you enter). Ranked fourth: it governs the first seconds, which is where your A/B test lives.
- **Count:**
  - The first lyric line starts at a median **{{ q('all','first_line','median','{:.1f}') }} seconds**: within 5 seconds in {{ g('all','first_line_le_5s') }} tracks and after 15 seconds in {{ g('all','first_line_gt_15s') }}.
  - **What that first line is** (the AI reader's call, from the text alone): an ad-lib or vocalization in {{ sm('all','first_line_kind','adlib_or_vocalization') }}, a sample or another voice in {{ sm('all','first_line_kind','sample_or_other_voice') }}, spoken in {{ sm('all','first_line_kind','spoken') }}, sung in {{ sm('all','first_line_kind','sung') }}, a rap line in {{ sm('all','first_line_kind','rap') }}, unclear in {{ sm('all','first_line_kind','unclear') }}.
  - The record opens on an intro in {{ sm('all','first_section','intro') }} of {{ g('all','n_section_map') }} section maps, on the hook in {{ sm('all','first_section','hook') }} and straight into a verse in {{ sm('all','first_section','verse') }}.
  - **Intro length** (the time before the first hook or verse): median {{ q('all','intro_len_s','median','{:.0f}') }} seconds, or **{{ q('all','intro_len_bars','median','{:.1f}') }} felt bars** (middle half {{ q('all','intro_len_bars','q1','{:.1f}') }}–{{ q('all','intro_len_bars','q3','{:.1f}') }}).
- **Examples:** "Evil J0rdan" waits until {{ fl('Evil J0rdan') }} for its first line; "Real Spill" until {{ fl('Real Spill') }}; "Redrum" until {{ fl('Redrum') }}. "Not Like Us", "Houdini" and "Carnival" have a voice inside the first second.{{ fl_under('Not Like Us', 1) }}{{ fl_under('Houdini', 1) }}{{ fl_under('Carnival', 1) }}
- **Try it [J]:** treat the intro as four felt bars (eight on your 144 grid) with one identity sound in it: a tag, an ad-lib, a chopped phrase. Enter with the lead on bar five. If the record needs more runway, take eight and nothing in between.
- **Exception:** {{ sm('all','first_section','verse') }} records start on the verse with no intro at all ({{ lst('verse_first_section_list', None, ', ') }}), and {{ sm('all','first_section','hook') }} start on the hook. [J]
- **Flags:** the lyric record shows the first *transcribed* line. A wordless intro, a beat tag or an instrumental sample before it is invisible here. The kind of line is the weakest label in this study: the reader judged it from text, which often cannot tell a sample from the artist, and may have recognized a well-known borrowed lyric. Treat that split as a rough guide (see `05-measurement-method.md`).

### M-5. Section sizes: hooks of four or eight felt bars, first verses of eight, twelve or sixteen

- **Effect:** writing and arrangement. Ranked fifth: it sizes every block in the session plan.
- **Count (one reader's section map, {{ g('all','n_section_map') }} tracks; bars need a resolved felt tempo):**
  - **First hook:** median {{ q('all','hook1_len_s_map','median','{:.0f}') }} seconds, **{{ q('all','hook1_len_bars_map','median','{:.1f}') }} felt bars**. About four bars in {{ sm('all','hook1_len_bar_bands_map','3-5 (about 4)') }} tracks and about eight in {{ sm('all','hook1_len_bar_bands_map','7-9 (about 8)') }} (of {{ g('all','hook1_len_bars_map')['n'] }}).
  - **First verse:** median {{ q('all','verse1_len_s_map','median','{:.0f}') }} seconds, **{{ q('all','first_verse_len_bars','median','{:.0f}') }} felt bars**. About eight bars in {{ sm('all','verse_len_bar_bands','6-10 (about 8)') }}, about twelve in {{ sm('all','verse_len_bar_bands','10-14 (about 12)') }}, about sixteen in {{ sm('all','verse_len_bar_bands','14-18 (about 16)') }}, longer in {{ sm('all','verse_len_bar_bands','18-26') + sm('all','verse_len_bar_bands','26+') }} (of {{ g('all','first_verse_len_bars')['n'] }}).
  - **Verses per song:** two in {{ sm('all','n_verses','2') }}, three in {{ sm('all','n_verses','3') }}, four or more in {{ sm('all','n_verses','4') }}, one in {{ sm('all','n_verses','1') }}.
  - **Hook occurrences:** two in {{ g('all','hook_count').get('2',0) }} tracks, three in {{ g('all','hook_count').get('3',0) }}, four or more in {{ g('all','hook_count').get('4',0) + g('all','hook_count').get('5+',0) }}.
  - A bridge appears in {{ g('all','has_bridge') }}, a pre-hook in {{ g('all','has_pre_hook') }} and a post-hook in {{ g('all','has_post_hook') }}. The record ends on an outro in {{ sm('all','ends_on','outro') }} maps, on the hook or post-hook in {{ sm('all','ends_on','hook') + sm('all','ends_on','post_hook') }} and on a verse in {{ sm('all','ends_on','verse') }}.
- **Try it [J]:** plan the demo as intro 4, hook 8, verse 12 or 16, hook 8, verse 8 to 16, hook 8 in felt bars. Double each number on the 144 grid. That is the commonest skeleton in the set, not a rule.
- **Exception:** "Rich Flex", "Family Matters" and "Meltdown" are built in parts, each with a documented beat switch (M-11), and do not fit the skeleton. [J]{{ needswitch('Rich Flex') }}{{ needswitch('Family Matters') }}{{ needswitch('Meltdown') }}
- **Flags:** section labels are one reader's call, and a hook sung twice in a row is counted as one long hook. Trap-tagged songs run shorter first verses (median {{ q('style_trap','first_verse_len_bars','median','{:.0f}') }} felt bars) than the set as a whole.

### M-6. When the hook comes back it is nearly the same words; change shows up around it

- **Effect:** arrangement (transitions) and delivery. Ranked sixth: it says where to spend your variation.
- **Count:**
  - The hook returns with **identical words in {{ sm('all','hook_return','identical') }}** tracks and with **minor variation in {{ sm('all','hook_return','minor_variation') }}** (a few words or ad-libs). It comes back extended in {{ sm('all','hook_return','extended') }}, shortened in {{ sm('all','hook_return','shortened') }} and with new lyrics in {{ sm('all','hook_return','new_lyrics') }}.
  - The last hook is at least a quarter longer than the first in {{ g('all','last_hook_longer') }} tracks and shorter in {{ g('all','last_hook_shorter') }}.
  - **Verse 2 against verse 1:** shorter in {{ num(g('all','verse2_shorter')) }}, about the same in {{ num(g('all','verse2_similar')) }}, longer in {{ g('all','verse2_longer') }}. There is no "short second verse" rule in this set.
  - A stretch of 12 seconds or more between transcribed lines appears in {{ g('all','gap_ge_12s') }} tracks. It can be a break, a beat change or a sample interlude, but also a passage the transcriber left out, so it is a hint and not a count of breaks.
  - What lyric timing cannot show: drums, 808 and doubles. Documented changes between sections are in M-11.
- **Examples:**
  - *Same words every time:* {{ sub('hook_return_lists', 'identical', 6) }}.
  - *Longer on return:* {{ sub('hook_return_lists', 'extended', 5) }}.
  - *Shorter on return:* {{ sub('hook_return_lists', 'shortened', 5) }}.
- **Try it [J]:** keep the hook's words fixed so it reads as the anchor, and move the change to its edges: drop the drums for the last felt bar before it, or add the stack and ad-libs only on the final pass. Give verse 2 the same length as verse 1 unless the song is short of ideas.
- **Exception:** the hook comes back with new lyrics on {{ sub('hook_return_lists', 'new_lyrics', None, ' and ') }}. [J]
- **Flags:** word-level sameness says nothing about the mix. A hook can keep its words and still gain doubles, harmonies or a new bed that this method cannot hear.

{{ open_template('03-documented.part.md') }}
