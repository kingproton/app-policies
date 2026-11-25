{{ open_template('03-m7-borrowing.part.md') }}

### M-8. The {{ g('climbers','n_songs') }} songs that *climbed* into the top 10 look different from the {{ g('debuts','n_songs') }} that debuted there

- **Effect:** arrangement (how soon the hook comes, solo vs guests) and which patterns to weight. Ranked eighth only because the group is small. [J] I treat the climbers as the nearest comparison for a single released on its own, because they rose over weeks and did not debut in an album week; nothing in the data records label or release type, so that reading is not tested.
- **Count:** {{ g('climbers','n_songs') }}/100 climbed in; {{ g('debuts','n_songs') }} debuted directly. Compared with the debuts:
  - **First hook:** median **{{ q('climbers','first_hook','median') }}** vs **{{ q('debuts','first_hook','median') }}**; by 0:30 in {{ g('climbers','first_hook_le_30s') }} vs {{ g('debuts','first_hook_le_30s') }}.
  - **Hook before the first verse:** {{ g('climbers','hook_before_first_verse') }} vs {{ g('debuts','hook_before_first_verse') }}.
  - **A second credited vocalist:** **{{ fs('climbers','second_vocalist_credit') }}** vs **{{ fs('debuts','second_vocalist_credit') }}**.
  - **Documented borrowing:** **{{ fs('climbers','borrow_documented') }}** vs **{{ fs('debuts','borrow_documented') }}**. These are floors, not rates: a song with nothing documented is unknown, not "no" (see M-7).
  - **Runtime:** median {{ q('climbers','runtime','median') }} vs {{ q('debuts','runtime','median') }}.
  - **Chart run:** median weeks in the top 10 **{{ ST_climb_weeks() }}** vs **{{ ST_debut_weeks() }}**.
- **Examples:** {{ climber_examples(6) }}.
- **Try it [J]:** if you want a comparison group for your demo, use these {{ g('climbers','n_songs') }} rather than the {{ g('debuts','n_songs') }} direct debuts ({{ g('album_bomb','n_songs') }} of the 100 are album-bomb cuts): mostly solo ({{ den(fs('climbers','second_vocalist_credit')) - num(fs('climbers','second_vocalist_credit')) }} of {{ den(fs('climbers','second_vocalist_credit')) }}), with the hook started by 0:30 in {{ g('climbers','first_hook_le_30s') }}. That describes {{ g('climbers','n_songs') }} songs; it is not a way to climb.
- **Exception:** "Euphoria" climbed with no recurring hook at {{ rt('Euphoria') }}{{ nohook('Euphoria') }}{{ climber('Euphoria') }}, and "Noid"{{ climber('Noid') }}{{ same_week('Noid', 'St. Chroma') }} entered the top 10 in the week its album-mate "St. Chroma" debuted there. Both climbs coincided with outside events, a public feud and an album release; the study can't say what drove them.
- **Flags:**
  - **Small sample ({{ g('climbers','n_songs') }}).**
  - Doja Cat has {{ climbers_by('Doja Cat') }} of the climbers ("Agora Hills", "Paint The Town Red", "Vegas"){{ climber('Agora Hills') }}{{ climber('Paint The Town Red') }}{{ climber('Vegas') }} and Tyler, The Creator {{ climbers_by('Tyler') }}.
  - Comparing climbers with debuts shows correlation inside this set, not a recipe.

### M-9. {{ num(g('all','no_hook')) }} of {{ den(g('all','no_hook')) }} assessed records have no recurring hook

- **Effect:** writing, i.e. whether to build a chorus at all. Ranked ninth: few songs, but a clear alternative shape.
- **Count:** in **{{ g('all','no_hook') }}** tracks no block of lyric comes back as a hook: {{ titles('no_hook_list') }}.
  - {{ num(g('style_verse_led','no_hook')) }} of the {{ num(g('all','no_hook')) }} carry the verse-led tag, and {{ num(g('drake_credit','no_hook')) }} are Drake-credited.
  - Their runtimes run from {{ no_hook_rt_min() }} to {{ no_hook_rt_max() }}.
- **What comes back instead, song by song** (the lyric-record column is the AI reader's description of the record; the page column is page text, basis P):

| Song | In the lyric record | On the pages |
|---|---|---|
| "Make Them Cry"{{ nohook('Make Them Cry') }} | One continuous rap; only short ad-lib tags repeat, at both ends{{ rnote('Make Them Cry','ad-lib tags at both ends') }} | One word is repeated in the intro and again in the outro, bookending the song{{ need('Make Them Cry','opening','repeated in the intro') }} |
| "Evil J0rdan"{{ nohook('Evil J0rdan') }} | One verse after a {{ fl('Evil J0rdan') }} wait; nothing returns{{ rnote('Evil J0rdan','one continuous rap verse') }} | A long intro built on a sample links it to the album track before it{{ need('Evil J0rdan','structure','Popular') }} |
| "Reincarnated"{{ nohook('Reincarnated') }} | Three verses; verses 1 and 2 end on the title word{{ rnote('Reincarnated','end on the title word') }} | Three verses and no chorus; a sung Spanish intro by another singer; the third verse changes speaker{{ need('Reincarnated','structure','no chorus') }}{{ needv('Reincarnated','opening','Spanish') }}{{ needv('Reincarnated','return_1','third verse') }} |
| "Euphoria"{{ nohook('Euphoria') }} | Three verse parts; one line recurs once{{ rnote('Euphoria','a single line recurs') }} | The beat is the landmark: a soft start, then it picks up, and the instrumental grows more aggressive{{ needv('Euphoria','return_1','picks up') }}{{ needv('Euphoria','return_2','aggressive') }} |
| "Hiss"{{ nohook('Hiss') }} | Three verses separated by ad-lib breaks{{ rnote('Hiss','ad-lib breaks') }} | A spoken-word intro, and a second spoken break between the first and second verse{{ needv('Hiss','return_1','spoken word') }} |
| "Calling For You"{{ nohook('Calling For You') }} | No section returns; a one-off refrain passage, a sung title chant and a long skit{{ rnote('Calling For You','No section returns') }}{{ rnote('Calling For You','skit') }} | A sample "anchors the song"; a skit of about 90 seconds sits halfway through{{ needv('Calling For You','hook_description','anchors') }}{{ need('Calling For You','structure','skit') }} |
| "Papi's Home"{{ nohook("Papi's Home") }} | One verse framed by a sampled intro and outro{{ rnote("Papi's Home",'framed by a sampled intro and outro') }} | The sample is used in the intro and again in the outro; one verse only{{ need("Papi's Home",'structure','outro as well as the intro') }}{{ need("Papi's Home",'structure','only one verse') }} |

- **Try it [J]:**
  - If you go hookless, build a **return anchor**: a spoken frame that comes back, a beat change, or one line repeated as a refrain.
  - Make the record's context obvious: the target, the occasion, the stakes.
- **Exception:** "Man At The Garden" sits between the two shapes: one short line recurs through the verses as a litany before a chant block arrives at {{ hook('Man At The Garden') }}.{{ rnote('Man At The Garden','refrain line') }} [J]
- **Flags:** "no hook" here means no *lyric* block returns. A wordless or instrumental refrain would not show in a lyric record. Two of these are diss records ("Euphoria", "Hiss"){{ nohook('Euphoria') }}{{ nohook('Hiss') }}, so part of this shape belongs to one kind of record.

### M-10. Runtime: album-bomb cuts run long; other songs sit nearer 3:15–3:20

- **Effect:** arrangement, i.e. how many sections to build. Ranked tenth.
- **Count:**
  - Median **{{ q('all','runtime','median') }}** (middle half {{ q('all','runtime','q1') }}–{{ q('all','runtime','q3') }}; n={{ g('all','runtime')['n'] }}).
  - **{{ g('all','runtime_le_3min') }}** are 3:00 or under; **{{ g('all','runtime_ge_4min') }}** are 4:00 or over.
  - Source: the Apple catalog duration for {{ top('runtime_basis')['catalog'] }} tracks, a cited runtime for {{ top('runtime_basis').get('cited',0) }} ({{ lst('runtime_cited_only', None, ', ') }}).
- **By group:**
  - Album-bomb cuts: median **{{ q('album_bomb','runtime','median') }}**; other songs: **{{ q('not_bomb','runtime','median') }}**.
  - Climbers: **{{ q('climbers','runtime','median') }}** (n={{ g('climbers','runtime')['n'] }}).
  - Drake-credited: **{{ q('drake_credit','runtime','median') }}**, vs **{{ q('no_drake','runtime','median') }}** for everything else.
- **Examples:**
  - *Shortest:* {{ lst('shortest', 5, ', ') }}.
  - *Longest:* {{ lst('longest', None, ', ') }}.
- **Try it [J]:**
  - Build the demo between about 2:45 and 3:30.
  - Add a section only if it brings a new bed, a new voice or a new device (M-6, M-11).
- **Exception:** "Family Matters" ({{ rt('Family Matters') }}) and "Euphoria" ({{ rt('Euphoria') }}) are long feud records built in several distinct parts (M-11).
- **Flags:** the long tail is mostly Drake album cuts and feud records.

{{ open_template('03-m11-m12.part.md') }}

---

## Concentration and sample-size flags (read before generalizing)

- **Chart pattern:**
  - **{{ ST['debuts'] }}/100** debuted in the top 10.
  - **{{ ST['one_week_top10'] }}/100** spent exactly one week there.
  - **{{ ST['album_bomb_songs'] }}/100** are album-bomb cuts.
- **Artist concentration:**
  - **Drake** is lead artist on **{{ ST['lead_artists'][0][1] }}** and credited on {{ ST['drake_any_credit'] }}.
  - {{ ST['lead_artists'][1][0] }} leads **{{ ST['lead_artists'][1][1] }}**; {{ ST['lead_artists'][2][0] }} **{{ ST['lead_artists'][2][1] }}**.
  - Wherever a count above splits by Drake credit, the split is shown, because one artist's habits can pass for a pattern.
- **Drill:** only **2** tracks are tagged drill, "Barbie World" and "Princess Diana", both with Ice Spice. Every drill-specific recommendation in the process is therefore **judgment [J]**, not a finding.
- **Verse-led:** only {{ g('style_verse_led','n_songs') }} tracks carry the tag, and {{ num(g('style_verse_led','no_hook')) }} of them have no recurring hook. Their medians are shown for orientation, not as rules.
- **The rap top-10 drought:** Billboard and the press reported no rap song in the top 10 from "What Did I Miss?" (July 2025) until spring 2026, and no rap song in the top 40 on the charts dated 2025-10-25 and 2025-11-01, a first since 1990 (both known through web-search summaries from the earlier pass; the articles were not opened in this study). That gap is why the 100 reach back to September 2021.

---

## What could and could not be measured

| Question asked | Status | Basis |
|---|---|---|
| Runtime | **Measured** for {{ top('runtime_basis')['catalog'] }}, cited for {{ top('runtime_basis').get('cited',0) }} | Apple catalog duration |
| Tempo and felt pulse, half and double time normalized | **Measured**: {{ g('all','feel_basis')['M'] }} clear, {{ g('all','feel_basis').get('L',0) + g('all','feel_basis').get('I',0) }} with a caveat, {{ g('all','feel_basis').get('?',0) }} open, {{ cnt('clip_missing') }} no clip | Backbeat in a 30-second preview clip |
| First lead-vocal entrance | **Proxy only.** The first transcribed lyric line is measured for {{ g('all','n_lyric') }}, to about a second. Whether that line is the lead artist is a text-only label: a rap or sung line in {{ sm('all','first_line_kind','rap') + sm('all','first_line_kind','sung') }}, an ad-lib or spoken line in {{ sm('all','first_line_kind','adlib_or_vocalization') + sm('all','first_line_kind','spoken') }}, a sample or another voice in {{ sm('all','first_line_kind','sample_or_other_voice') }}, unclear in {{ sm('all','first_line_kind','unclear') }}. The lead-vocal entrance itself was not measured | Time-synced lyric record |
| First hook or return anchor | **Measured** for {{ g('all','n_lyric') }}; no hook found in {{ num(g('all','no_hook')) }} | Two readings of the same record, ruled where they differed |
| Section order and lengths | **Measured**: section order and lengths in seconds for {{ g('all','n_section_map') }} (one reader's map, table 4b-2); lengths in felt bars for the {{ min(g('all','hook1_len_bars_map')['n'], g('all','first_verse_len_bars')['n'], g('all','intro_len_bars')['n']) }} to {{ max(g('all','hook1_len_bars_map')['n'], g('all','first_verse_len_bars')['n'], g('all','intro_len_bars')['n']) }} that also have a resolved felt tempo | Same record plus the felt tempo |
| How densely the rapper rides the beat | **Measured** as syllables per second for {{ g('all','verse_sylls_per_s')['n'] }} and per felt beat for {{ g('all','verse_sylls_per_beat')['n'] }} | Same record; syllables estimated from spelling |
| Vocal density between sections | **Measured by section type**: verse against hook, words per second, for {{ den(g('all','verse_denser_than_hook')) }} (M-2). Not computed for each return of a section | Same record |
| How the performance changes between sections | **Documented only**: cited delivery observations on {{ fsx('tracks_with_sourced_delivery') }} songs and page statements on {{ pagefacts('delivery') }} (M-12); return codes in table 4c. Not measured | Page text and cited sources |
| Where phrases start and stop against the drums; where rhymes land | **Unknown** | Needs word-level timing against the audio |
| Silence after punchlines | **Unknown for 100/100** | Line-level timing cannot show a gap inside or after a line |
| Changes in drums, 808, melody, doubles and ad-libs when a section returns | **Unknown** at the layer level. Documented instead (M-11): a beat switch on {{ bs_n() }} songs, and, in the earlier pass's coding of what changes between sections, a beat or bed change on {{ fs('all','return_beat') }} of {{ fs('all','return_sourced_tracks') - fs('all','return_none') }} coded songs | Needs the full recording or stems |
| Which change is audible enough to matter | **Unknown for 100/100** as a listening judgment, because nobody listened. What sources single out is coded for {{ fs('all','return_sourced_tracks') - fs('all','return_none') }} tracks in table 4c (M-11), and {{ fs('all','return_none') }} more is coded as naming no specific change | — |
| A hook that is absent vs one that is unverified | **Separated**: "none" in table 4b means the record was read and no returning block was accepted ({{ nohook_basis('A') }} where both readings agree, {{ nohook_basis('J') }} where a second reader ruled); "no matching record" means there was no usable record | — |

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
  - **P**: after the skeptic's check, the saved Wikipedia or Songfacts page text states the fact or names the work, and the quoted words were found in the saved page. A P can rest on a supported verdict, on a partly supported one (the page states the core; the detail it does not state is not counted; this includes verdicts the skeptic downgraded from supported), on a new page statement, or on a claim recoded to what the page states ({{ po('opening','recoded') }} opening). `05-measurement-method.md` gives the split.
  - **S**: a cited source supports the claim and the earlier verifier did not reject it. These were read through web-search summaries.
  - **U**: cited but not confirmed, or contradicted by page text. Kept for transparency, never counted.
  - **R**: unverified recollection. Never counted.
  - **?**: unknown.
- **Grid BPM:** the fastest steady pulse that carries the beat, which is what a DAW project would be set to. **Felt BPM:** the backbeat tempo, with the snare or clap on beats 2 and 4. On a slow pocket the grid is double the felt tempo.
- **Felt bar:** four felt beats. Bar counts in this file are felt bars; double them for a doubled DAW grid.
- **Hook:** the main block of lyric that comes back in substantially the same words. **Return anchor:** the first line of *any* block that comes back. **Hook before the first verse:** no verse section starts before the first hook; a short intro, tag or sample may come before it.
- **Borrowings** are typed as sample, interpolation, dialogue clip or self-reuse. Page-supported credits count, as do the {{ len(MS_ALL['page_origins']['borrowings_search_summary_only']) }} credits the earlier verifier added from search summaries and credits cited by research that were not flagged; unconfirmed and rejected credits do not.
- **Return-change coding** (M-11) is mine, from the cited descriptions. Each song's code is in `scripts/corrections.py` (`RETURN_TYPES`, `RETURNING`).
- **Second credited vocalist** = the Billboard credit names at least two vocalists. Producer-only credits such as Metro Boomin don't count.
- **Style tags** (trap, West Coast bounce, boom-bap/verse-led, pop-rap, R&B-rap, drill, Jersey club, rage) were assigned by the research agents from source descriptions and credits. They're descriptive, not Billboard categories.
- **Earlier re-check reports** from the search-based pass are kept in `data/raw/` (`recheck_sweep_claims.md`, `recheck_classification.md`). They predate the page-level check and are superseded by it where the two differ.
