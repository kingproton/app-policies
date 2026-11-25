"""Hand-coded corrections applied after the independent verifier pass.

Every entry traces to a verifier flag (data/raw/tracks_merged.json -> 'flagged') or to the
3-lens document review. Keys are candidate ids (cid). Nothing here comes from memory.

Basis ladder used everywhere (strongest first):
  source            a cited page supports the claim and the verifier did not reject it,
                    or a later gap sweep supplied its own citation
  unconfirmed       the researcher claimed a source, but the verifier could not find support
                    (kept for transparency, never counted as sourced)
  unverified_recollection
  unknown
"""

# ---- 1. Structural claims the verifier could not support ------------------------------
# field -> 'unconfirmed' keeps the value but drops it from sourced counts;
# 'unknown' clears it (used only where the verifier explicitly reset the field to unknown).
VERIFIER_DOWNGRADES = {
    5:   {'hook_status': 'present_unverified'},                      # Janice STFU
    21:  {'hook_status': 'present_unverified'},                      # Rather Lie
    31:  {'hook_status': 'present_unverified'},                      # Hey Now
    34:  {'hook_status': 'present_unverified'},                      # Sticky (Tyler)
    50:  {'hook_status': 'present_unverified'},                      # Enough (Miami)
    56:  {'hook_status': 'present_unverified'},                      # Agora Hills
    67:  {'hook_status': 'present_unverified'},                      # Paint The Town Red
    69:  {'hook_status': 'present_unverified'},                      # FE!N
    74:  {'hook_status': 'present_unverified'},                      # All My Life
    76:  {'hook_status': 'present_unverified'},                      # Princess Diana
    87:  {'hook_status': 'present_unverified'},                      # Spin Bout U
    88:  {'hook_status': 'present_unverified'},                      # Pussy & Millions
    93:  {'hook_status': 'present_unverified'},                      # Forever
    113: {'hook_status': 'present_unverified'},                      # First Class
    119: {'hook_status': 'present_unverified'},                      # Super Gremlin
    17:  {'beat_switch': 'unconfirmed'},                             # What Did I Miss?
    20:  {'opening': 'unconfirmed'},                                 # Evil J0rdan: research cites album reviews; verifier found a promo-version intro note
    23:  {'opening': 'unconfirmed', 'beat_switch': 'unconfirmed'},   # Gimme A Hug
    32:  {'opening': 'unconfirmed'},                                 # Reincarnated
    35:  {'opening': 'unconfirmed', 'hook_first': 'unconfirmed'},    # St. Chroma
    36:  {'opening': 'unconfirmed'},                                 # Noid
    41:  {'opening': 'unconfirmed', 'hook_first': 'unconfirmed',     # Family Matters
          'hook_status': 'unknown', 'beat_switch_time': None},
    28:  {'beat_switch_time': None},                                 # TV Off: '~2:00' not re-found (switch itself confirmed)
    44:  {'beat_switch': 'unconfirmed'},                             # 7 Minute Drill
    53:  {'opening': 'unconfirmed', 'hook_first': 'unconfirmed'},    # Hiss
    55:  {'opening': 'unconfirmed', 'hook_first': 'unconfirmed'},    # Nee-nah
    59:  {'beat_switch': 'unconfirmed'},                             # First Person Shooter
    60:  {'opening': 'unconfirmed'},                                 # IDGAF
    63:  {'opening': 'unconfirmed'},                                 # Daylight
    96:  {'opening': 'unconfirmed'},                                 # Tomorrow 2
    98:  {'opening': 'unconfirmed', 'hook_first': 'unconfirmed'},    # Staying Alive
    101: {'opening': 'unconfirmed', 'beat_switch': 'unconfirmed'},   # Jimmy Cooks (sweep re-sources the switch)
    118: {'opening': 'unconfirmed', 'hook_first': 'unconfirmed'},    # Pushin P
    124: {'opening': 'unconfirmed', 'hook_status': 'present_unverified'},  # Way 2 Sexy
    126: {'opening': 'unconfirmed'},                                 # Fair Trade
    127: {'opening': 'unconfirmed', 'beat_switch': 'unconfirmed'},   # Champagne Poetry
    130: {'opening': 'unconfirmed'},                                 # Papi's Home
}

# Return-change records that describe a claim the verifier rejected (same switch / same intro).
RETURNS_UNCONFIRMED = {17, 20, 23, 44, 59, 127}

# ---- 2. Sample / interpolation credits ------------------------------------------------
# status: confirmed (verifier confirmed or found it) | cited (research URL, not flagged)
#         not_reconfirmed (research URL, verifier could not re-find it) | rejected | uncited
SAMPLE_STATUS = {   # (cid, substring of 'work') -> status
    (20, 'Popular'): 'rejected',              # fan wiki only
    (52, 'Iron Man'): 'rejected',             # not confirmed in the streaming version used
    (45, 'Everlasting Bass'): 'not_reconfirmed',
    (45, 'Eazy-Duz-It'): 'not_reconfirmed',
    (54, 'Serenata'): 'confirmed',
    (54, 'Shining'): 'not_reconfirmed',
    (56, 'Troop'): 'not_reconfirmed',          # verifier got no results for this title
    (60, 'Tunnel'): 'cited',                  # verifier could not re-find it; the gap sweep cites Urban Islandz for the intro sample
    (62, 'Shake It'): 'not_reconfirmed',
    (102, 'RY X'): 'not_reconfirmed',
}
SAMPLE_REPLACE = {  # cid -> (substring to drop, [new entries])
    23: ('Unidentified gospel', [
        dict(work="Aaron Hall - 'I Miss You' (1993)", how_used='Credited sample (Wikipedia, per the verifier; replaces an unnamed gospel-style sample).', source='Wikipedia, per verifier', status='confirmed'),
        dict(work="Terrell Grice - 'Sing'", how_used='Credited sample (Wikipedia, per the verifier).', source='Wikipedia, per verifier', status='confirmed')]),
}
SAMPLE_ADD = {
    24: [dict(work='The Nokia ringtone (in the synths)', how_used='Wikipedia says the synths sample the Nokia ringtone (per the verifier).', source='Wikipedia, per verifier', status='confirmed')],
    55: [dict(work="Lenny Williams - ''Cause I Love You'", how_used='Credited on the Wikipedia album page (search summary, per the verifier).', source='Wikipedia, per verifier', status='confirmed')],
    85: [dict(work="Elijah Fox - 'East Village'", how_used="Credited in Wikipedia's Her Loss notes (per the verifier).", source='https://en.wikipedia.org/wiki/Her_Loss', status='confirmed')],
    89: [dict(work="The Isley Brothers - 'Ballad for the Fallen Soldier'", how_used="Credited in Wikipedia's Her Loss notes (per the verifier).", source='https://en.wikipedia.org/wiki/Her_Loss', status='confirmed')],
    131: [dict(work="Justin Timberlake - 'Until the End of Time'", how_used='Credited on Wikipedia (per the verifier); the Half on a Baby material comes via OG Ron C\'s remix.', source='Wikipedia, per verifier', status='confirmed')],
}
SAMPLE_RENAME = {   # (cid, substring) -> new work text
    (92, 'Gwen'): "An unnamed sample (named as Coco O.'s 'Gwen' in research; the name is unconfirmed)",
    (109, 'Higher'): "'Higher' by Tems",
}
SAMPLE_FORCE = {    # (cid, substring) -> field overrides
    (92, 'Gwen'): {'status': 'confirmed'},     # sample use confirmed; only the name is not
    (41, 'Push Ups'): {'credited': False, 'borrow_type': 'self-reuse', 'status': 'cited'},
}

# ---- 3. Tempo ----------------------------------------------------------------------------
TEMPO_OUTLIERS = {  # cid -> [(bpm, site substring)] removed from tempo evidence
    49: [(128, 'SFR'), (147, 'Songdata')],
    67: [(165, 'songdata'), (140, 'songdata')],
    68: [(112, 'beatport')],
    69: [(179, 'shazam')],
    81: [(122, 'mixgraph')],
    83: [(117, 'Beatport')],
    108: [(101, 'Songdata'), (130, 'Chordify')],
    111: [(172, 'Songdata')],
    112: [(182, 'Songdata')],
}
# The verifier called these feels unresolved (half vs full cannot be settled from listings).
FEEL_UNRESOLVED_VERIFIER = {
    9: 'Only listing is 193 (two aggregators that may share data); the song has two parts, so one value may cover one part.',
    49: 'Listings agree on 112; felt 56 or 112 cannot be settled without listening.',
    70: 'Listed 122; nothing describes a half-time beat, and 122 is just as plausible as the felt pulse.',
}
# Songs that are interpolations in Wikipedia but typed otherwise by the keyword rule.
FORCE_INTERPOLATION = {(5, 'I Follow Rivers')}
# Wikipedia calls this a sample of Dukureh's recording (some outlets say interpolation).
FORCE_SAMPLE = {(95, 'Hound Dog')}

# ---- 4. Return-change coding (coded from the cited descriptions; my coding, see 03) --------
# beat = the instrumental bed or drums change (switch, new sample, drums enter);
# voice = a different person takes the section; register = same rapper changes voice/character;
# delivery = spoken break or interlude; none = sources say nothing specific changes.
RETURN_TYPES = {
    9: 'beat', 11: 'beat', 17: 'beat', 20: 'beat', 21: 'register', 23: 'beat', 28: 'beat', 30: 'beat',
    32: 'register', 34: 'none', 35: 'voice', 36: 'beat', 40: 'beat', 41: 'beat', 44: 'beat', 45: 'voice',
    47: 'voice', 53: 'delivery', 55: 'voice', 56: 'delivery', 59: 'beat', 60: 'beat', 68: 'beat', 69: 'voice',
    75: 'beat', 76: 'voice', 83: 'beat+voice', 84: 'beat', 101: 'beat', 118: 'voice', 124: 'voice', 126: 'beat', 127: 'beat',
}

# ---- 5. Reference-list marks ------------------------------------------------------------
# Included as rap on album-mate inference only (no page showing this title on a rap chart).
ALBUM_MATE_INFERRED = {}   # Reincarnated is on the 2025 year-end Hot Rap Songs list (No. 32), read directly   # Fair Trade, Champagne Poetry, In The Bible now have direct listings (overrides below)
# Version notes surfaced under table 4b (abridged from track_measurements.csv version_used).
VERSION_NOTES = {
    'Evil J0rdan': "album version (MUSIC track 4); a review says it has a new synthesized intro versus the earlier-circulated 'EvilJ0rdan'.",
    'Noid': 'album version (4:44), not the music-video edit, which drops the vocal intro and final verses.',
    'Carnival': "current explicit streaming version (4:24). The live 'Iron Man' sample is documented only for an earlier version, so it is not counted. Table 4b measures the catalog track on the CARNIVAL PACK EP (4:23, not flagged explicit), one second shorter.",
    'Agora Hills': 'album version (4:25); a 3:39 radio edit exists.',
    'FE!N': 'album version (3:11), not the Chase B remix.',
    'Princess Diana': 'the Nicki Minaj remix, which is the version credited on the chart (2:52); the original solo version is 2:35.',
    'Spin Bout U': 'album version, not the music-video edit.',
    'Super Freaky Girl': "solo single (2:50), not the 3:55 'Queen Mix'.",
    'Big Energy': 'solo version (2:54), not the Mariah Carey/DJ Khaled remix.',
    'Players': 'original single, not the Busta Rhymes or Jersey club remixes.',
}

# ---- 6. Classification overrides from the targeted re-check (filled from the agent report) --
# cid -> dict(status='rap'|'not_rap'|'unverified', evidence_type, confidence, summary, source_url)
CLASSIFICATION_OVERRIDES = {
    # Direct: a search-result summary named the song, the chart and a position (pages could not be opened).
    36: dict(status='rap', evidence_type='other_press', confidence='medium', source_url='https://radiox.cms.socastsrm.com/?p=252637',
             summary="A Billboard syndication says 'Noid' began at No. 6 on Hot Rap Songs and No. 43 on the Hot 100 (search-result summary)."),
    44: dict(status='rap', evidence_type='billboard_chart_page', confidence='medium', source_url='https://www.billboard.com/charts/rap-streaming-songs/2024-04-20/',
             summary="Billboard's Rap Streaming Songs chart dated 2024-04-20 lists it as a new entry (peak 2, 1 week) (search-result summary)."),
    89: dict(status='rap', evidence_type='billboard_chart_page', confidence='medium', source_url='https://www.billboard.com/charts/rap-streaming-songs/2022-11-19/',
             summary="Rap Streaming Songs dated 2022-11-19: new entry at No. 6; No. 7 on 2022-11-26 (search-result summaries)."),
    91: dict(status='rap', evidence_type='billboard_chart_page', confidence='medium', source_url='https://www.billboard.com/charts/rap-streaming-songs/2022-11-19/',
             summary="Rap Streaming Songs dated 2022-11-19: new entry at No. 7 (search-result summary, which called the page text jumbled)."),
    126: dict(status='rap', evidence_type='billboard_chart_page', confidence='medium', source_url='https://www.billboard.com/charts/rap-song/2021-12-04/',
              summary="Hot Rap Songs dated 2021-12-04: No. 13, peak No. 3 (search-result summary)."),
    127: dict(status='rap', evidence_type='billboard_chart_page', confidence='medium', source_url='https://www.billboard.com/charts/rap-streaming-songs/2021-09-18/',
              summary="Rap Streaming Songs dated 2021-09-18: new entry at No. 4; No. 15 (peak 4, 5 weeks) on 2021-10-16 (search-result summaries)."),
    129: dict(status='rap', evidence_type='billboard_chart_page', confidence='medium', source_url='https://www.billboard.com/charts/rap-song/2021-10-23/',
              summary="Hot Rap Songs dated 2021-10-23: re-entry, peak 6, 4 weeks; Rap Streaming Songs peak 6 on 2021-09-18 (search-result summaries)."),
    14: dict(status='not_rap', evidence_type='other_press', confidence='medium',
             source_url='https://www.rttnews.com/3661276/pinkpantheress-zara-larsson-s-stateside-climbs-to-no-1-on-billboard-s-pop-airplay-chart.aspx',
             summary="RTTNews (June 2026) reports it topped Billboard's Hot Dance/Pop Songs for 16 weeks; no sign of Hot Rap Songs (search-result summary)."),
    79: dict(status='not_rap', evidence_type='billboard_chart_page', confidence='medium', source_url='https://www.billboard.com/artist/Rema/chart-history/AFB',
             summary="No. 1 on Billboard's U.S. Afrobeats Songs for a record 58 weeks (Wikipedia; Rema's Afrobeats chart history); no sign of Hot Rap Songs (search-result summaries)."),
    116: dict(status='not_rap', evidence_type='billboard_article', confidence='medium',
              source_url='https://www.billboard.com/pro/imagine-dragons-j-i-d-s-enemy-crowns-rock-streaming-songs-chart/',
              summary="Billboard reported it topped Rock Streaming Songs (Jan. 15, 2022 chart); Hot Rock & Alternative Songs peak 2 (Wikipedia); no sign of Hot Rap Songs."),
    # Decided from tables read directly on Wikipedia (2026-11-25); see data/measured/genre_tables.json.
    65: dict(status='not_rap', evidence_type='wikipedia_chart_table', confidence='medium', source_url='https://en.wikipedia.org/wiki/Jack_Harlow_discography',
             summary="Jack Harlow's discography table gives '3D' a Hot 100 peak of 5 and a dash in both the Hot R&B/Hip-Hop Songs and Hot Rap Songs columns (table read directly). A dash alone can be an editor's omission, so this is indirect; no rap-chart listing was found by eight searches either."),
    99: dict(status='not_rap', evidence_type='wikipedia_chart_table', confidence='medium', source_url='https://en.wikipedia.org/wiki/Snoop_Dogg_singles_discography',
             summary="Snoop Dogg's singles discography gives 'Bad Decisions' a Hot 100 peak of 10 and a dash in the Hot R&B/Hip-Hop Songs column (table read directly). Search summaries of Billboard's Hot Rap Songs chart dated 2022-08-20 show a top five without it, though every title in that top five ranked below it on the Hot 100 that week."),
    3: dict(status='not_rap', evidence_type='billboard_article', confidence='low', source_url='https://www.billboard.com/music/chart-beat/adela-nicole-kidman-pop-hit-trending-up-1236346540/',
            summary="Indirect: a Billboard Chart Beat headline calls it one of the year's fastest-rising pop hits (headline seen in search results; the article was not opened). Seven searches found no text placing it on Hot Rap Songs, Rap Streaming Songs, Rap Airplay or Hot R&B/Hip-Hop Songs, and its Wikipedia chart table lists no genre chart."),
    1: dict(status='not_rap', evidence_type='wikipedia_chart_table', confidence='medium', source_url='https://en.wikipedia.org/wiki/Babydoll_(Dominic_Fike_song)',
            summary="The song's Wikipedia chart table lists Hot Rock & Alternative Songs (peak No. 2) and no rap or R&B/hip-hop chart (table read directly); search summaries of Billboard's weekly Hot Rock & Alternative Songs pages agree."),
    22: dict(status='not_rap', evidence_type='wikipedia_chart_table', confidence='medium', source_url='https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_Rap_Songs_of_2025',
             summary=("Year-end deduction from lists read directly: 'Anxiety' is No. 13 on the 2025 year-end Hot R&B/Hip-Hop Songs list and No. 39 on the 2025 year-end Hot 100, "
                      "but is not among the 50 titles on the 2025 year-end Hot Rap Songs list, where a rap title of that size would rank near the top ten. "
                      "Doechii's discography table has no rap column. No weekly Hot R&B Songs or Hot Rap Songs row was read.")),
}

# ---- 7. Independent re-check of the gap sweep's structure claims --------------------------
# cid -> {field: verdict}; verdict 'confirmed' keeps S; anything else drops a sweep-sourced value to U
# (hooks: present_verified -> present_unverified). Fields: opening_element, hook_before_first_verse,
# has_hook_or_chorus, beat_switch. 'partly' entries are resolved by hand to confirmed / not_supported.
SWEEP_VERDICTS = {
    8:   {'hook_before_first_verse': 'partly'},     # Shabang: opener is the line later used as the hook; order vs verse 1 not shown
    27:  {'opening_element': 'partly'},             # Squabble Up: Debbie Deb sample "near the beginning", not shown as first sound
    29:  {'hook_before_first_verse': 'partly'},     # Luther: sampled chorus first; the song's own hook vs verse 1 not placed
    39:  {'beat_switch': 'not_settled'},            # Not Like Us: one search summary (The Root) mentions a switch; the research record
                                                    # for the same song says no source settles whether the late breakdown is a switch,
                                                    # and neither saved page mentions one. Two passes disagree, so it is not counted.
    34:  {'opening_element': 'not_found', 'hook_before_first_verse': 'not_found'},  # Sticky: lyric sites conflict
    45:  {'opening_element': 'partly'},             # Like That: the Songfacts intro line describes 'Eazy-Duz-It', not this song
    52:  {'hook_before_first_verse': 'partly'},     # Carnival: no source gives the chorus vs first-verse order
    109: {'hook_before_first_verse': 'partly'},     # Wait For U: Tems refrain precedes verse 1, but a lyric page labels it intro
    113: {'opening_element': 'partly'},             # First Class: a brief sung "Mm" or the chorus; nothing supports "spoken"
    119: {'hook_before_first_verse': 'partly'},     # Super Gremlin: sampled vocal first; no chorus shown before verse 1
}
# Recodes where the re-check's own sources support a different value (kept as sourced, with the note).
SWEEP_RECODE = {
    38: ('opening_element', 'ad_lib_or_spoken_intro', "Re-check: a Paul Rosenberg voicemail skit opens the song, then the sung 'Without Me' callback (Songfacts, Yahoo, HotNewHipHop via search summaries)."),
    52: ('opening_element', 'chant', "Re-check: the song opens with a crowd chant by Inter Milan's Curva Nord ultras, recorded in the studio for the track (not a sample) and repeated throughout."),
}

# ---- 8. Final-review corrections -------------------------------------------------------------
# Delivery notes describing the same intro the verifier tied to a different version.
DELIVERY_UNCONFIRMED = {20}                      # Evil J0rdan
# Delivery items recoded: (cid, aspect) -> aspect
DELIVERY_RECODE = {(84, 'flow_switch'): 'other'}  # Rich Flex: the "flow switch" note describes the beat switch
# Return-change records: True = the change sits in a section or element that comes back
# (a verse slot, a returning chorus, a returning sample); False = a one-way switch or an
# intro/outro hand-off; None = a spoken insert between sections.
RETURNING = {9: False, 11: False, 28: False, 30: False, 40: False, 60: False, 68: False, 83: False, 84: False, 101: False,
             36: True, 41: True, 75: True, 126: True,
             35: True, 45: True, 47: True, 55: True, 69: True, 76: True, 118: True, 124: True,
             21: True, 32: True, 34: True, 53: None, 56: None}
# Exclusions above the cut that rest on inference rather than a direct non-rap listing.
GENRE_INFERENCE_EXCLUSIONS = {3: 'Nicole Kidman'}
# Exclusions backed by a non-rap chart row or a rap-column dash read directly in a Wikipedia table.
# Evidence grade for these exclusions, set by hand: direct = a non-rap genre-chart row; yearend = deduced from year-end
# lists; indirect = neither (a dash in a table's rap column can be an unfilled cell).
NONRAP_GRADE = {1: 'indirect', 22: 'yearend', 65: 'indirect', 99: 'indirect'}   # 1 Babydoll: a rock-chart listing alone does not rule out rap
NONRAP_TABLE_EVIDENCE = {1: "Hot Rock & Alternative Songs peak No. 2 (the song's Wikipedia chart table)", 22: 'year-end lists', 65: 'discography table', 99: 'discography table'}
YEAREND_ABSENCE_EXCLUSIONS = {71: 'Seven', 80: "Boy's A Liar, Pt. 2", 104: 'I Like You (A Happier Song)',
                              120: 'One Right Now', 121: 'Need To Know', 123: 'Thats What I Want'}


# ---- 9. Coding of documented "how it was made" statements (page facts kept by the skeptic) -------------
# Each kept recording-process statement is coded by the first matching rule below; PROCESS_OVERRIDES fixes single
# statements by (cid, leading words). Codes:
#   beat_sent        the finished beat was sent or handed over; the producer was not present for the vocal
#   beat_preexisting the beat existed long before, was made for someone else, or was passed on by others
#   hook_first       the hook, melody or title phrase came first, or was taken from an existing snippet
#   fast_or_freestyle freestyled, one take, written or made in minutes, made on the spot
#   guest_later      a guest verse was added, swapped or recorded separately after the song existed
#   late_session     recorded in the last day or two before release
#   sample_first     the track was built from or around a sample that came first
#   snippet_first    previewed, teased, leaked or performed before release (release strategy, outside the studio)
#   studio_info      only where or when it was recorded
PROCESS_RULES = [
    ('late_session', r'day before (?:the album|release|it came out)|last song recorded'),
    ('fast_or_freestyle', r'freestyl|one take|on the spot|in four minutes|seven-minute|spontaneous|within a seven'),
    ('guest_later', r'(?:verse|part|section) (?:was )?(?:added|replaced)|added later|later addition|recorded (?:his|her) (?:part|vocal|verse) (?:separately|afterwards)|earlier version had|recruited|decided to add|existed before the guest|texted him a demo|then sent her verses'),
    ('hook_first', r'hook first|came up with the hook|hummed|hook line came out|made the hook|took the chorus|title phrase is a group shout|one specific .* melody'),
    ('sample_first', r'built around the sample|beat around the|edited version of|shopped .* samples|from the sampled hook|chopping the sample|held the sample'),
    ('beat_sent', r'sent (?:the|it|a|to)|beat pack|in a batch|not in the (?:room|studio)|first heard the (?:final|finished)|exchanging files|sent it back|handed them|picked the beat from|texted'),
    ('beat_preexisting', r'made the (?:instrumental|beat) in (?:his bedroom in )?(?:19|20)\d\d|turned it down|originally made for|beat existed before|first intended for|first planned for|began as a|was not ready for his album|recorded for a .* compilation|had circulated online since'),
    ('snippet_first', r'preview|teased|snippet|leaked|premiered|performed live|circulated|played publicly'),
    ('studio_info', r'infobox|recorded (?:in|at|during|across|on) |studios?\b|mixed by'),
]
# Single statements the rules place wrongly: (cid, first words of the statement) -> code
PROCESS_OVERRIDES = {
    (5, 'The instrumental came from'): 'other',                 # Janice STFU: where the beat came from, not a preview
    (105, 'Boi-1da says the beat ideas'): 'other',              # N95: ideas made together in a session, then finished by Lamar alone
    (117, 'Minaj decided to add Lil Baby'): 'other',            # Do We Have A Problem?: the guest was chosen at the beat stage, not added later
    (13, 'The song was first previewed'): 'snippet_first',      # Make Them Pay: a preview the day before release, not a tracking date
    (45, 'An earlier version of the song had only Future'): 'guest_later',   # Like That: Lamar's verse came after the version sent for clearance
    (101, 'Recorded in 2022. Wikipedia also says'): 'other',    # Jimmy Cooks: the page's "planned for Her Loss" line is odd (that album came later); not counted
    (113, 'Chahayed (keys) and Lopez'): 'other',                # First Class: producers present through the sessions
    (97, 'The rights holder Hipgnosis'): 'sample_first',        # Super Freaky Girl: the sample came first, from the publisher
    (102, 'Gordo came up with the beat'): 'beat_sent',          # Sticky (Drake): beat made elsewhere, then brought to him
}



# ---- 10. Page-level coding (2026-11-25): what the saved Wikipedia / Songfacts text supports -------------
# Hand-coded from the page check's verdict notes and new statements. measure_merge applies an entry ONLY when the
# matching verdict or statement survived the skeptic and the mechanical quote check; otherwise it is skipped.
# (a) A "partly supported" verdict whose core yes the page does state (details on file go beyond the page).
PAGE_CORE = {
    'beat_switch': {9, 11, 23, 28, 40, 41, 44, 59, 68, 84, 101, 127},
    # 9 National Treasures, 11 Dust (softer opening, then harder trap production), 23 Gimme A Hug (two switches),
    # 28 TV Off, 40 Euphoria, 41 Family Matters, 44 7 Minute Drill (a second producer's beat takes over),
    # 59 First Person Shooter (a different sample bed in the second half), 68 Meltdown, 84 Rich Flex,
    # 101 Jimmy Cooks (the page says the track "then switches to an instrumental" built on a second sample; the
    # skeptic cut the verdict to partly supported only because two off-page details were part of the claim), 127 Champagne Poetry.
    # Not included: 62 Calling For You (the page describes a skit or interlude, not a change of beat).
}
# (b) The page supports a different value from the one on file: cid -> (field, new value)
PAGE_RECODE = {
    41: ('opening_element', 'ad_lib_or_spoken_intro'),    # Family Matters: a voice clip of Drake's mother opens it
    101: ('opening_element', 'sample_or_interpolation'),  # Jimmy Cooks: the Playa Fly sample starts the record
}
# (c) A new page statement sets a field that was unknown: (cid, statement category, words in the statement, field, value)
PAGE_FACT_SET = [
    (6, 'beat_switch', 'beat switch before Future', 'beat_switch', 'yes'),          # Ran To Atlanta
    (24, 'beat_switch', 'second half the beat changes', 'beat_switch', 'yes'),       # Nokia
    (63, 'beat_switch', 'beat switches two minutes', 'beat_switch', 'yes'),          # Daylight
    (85, 'beat_switch', 'has a beat switch', 'beat_switch', 'yes'),                  # Major Distribution
    (10, 'opening', 'repeated in the intro', 'opening_element', 'ad_lib_or_spoken_intro'),   # Make Them Cry
    (11, 'opening', 'spoken intro', 'opening_element', 'ad_lib_or_spoken_intro'),            # Dust
    (13, 'opening', 'sampled refrain', 'opening_element', 'sample_or_interpolation'),        # Make Them Pay
    (19, 'opening', 'acoustic guitar', 'opening_element', 'instrumental'),                   # All The Way
    (26, 'opening', 'opens with the chorus', 'opening_element', 'hook_or_chorus'),           # 4X4
    (64, 'opening', 'starts with Drake singing', 'opening_element', 'sung_intro'),           # Fear Of Heights
    (68, 'opening', 'whispering', 'opening_element', 'ad_lib_or_spoken_intro'),              # Meltdown
    (69, 'opening', 'alarm-like synth', 'opening_element', 'instrumental'),                  # FE!N
    (91, 'opening', 'opens with the chorus', 'opening_element', 'hook_or_chorus'),           # BackOutsideBoyz
    (92, 'opening', 'begins with Lil Baby rapping', 'opening_element', 'rap_verse'),         # California Breeze
    (94, 'opening', 'at the beginning', 'opening_element', 'sample_or_interpolation'),       # Real Spill
    (128, 'opening', 'intro by Project Pat', 'opening_element', 'sample_or_interpolation'),  # Knife Talk
]
# (d) A borrowing stated on a page and not on file: cid -> [(words in the statement, work, type, credited or None)]
PAGE_SAMPLE_ADD = {
    52: [('Hell of a Life', "Kanye West - 'Hell of a Life' (2010), which itself samples Black Sabbath's 'Iron Man'", 'sample', True)],
    64: [('Cramps', "The Cramps - 'Can Your Pussy Do the Dog?'", 'interpolation', None)],
    94: [('Sade', "Sade - 'The Big Unknown' (2018)", 'sample', None)],
    96: [('Munch', "Ice Spice - 'Munch (Feelin' U)' (interpolated in Cardi B's verse)", 'interpolation', None)],
    102: [('Virgil Abloh', "Virgil Abloh - spoken clip from his 2017 Columbia lecture (closes the song)", 'audio clip', None)],
    111: [('Data 2.0', "Aura Qualic - 'Data 2.0'", 'sample', None)],
    112: [('Young Thug', "Young Thug - 'Hot' (2019), interpolated in the chorus", 'interpolation', None)],
    125: [('Time Flies', "Drake - 'Time Flies' (2020), his own earlier song", 'interpolation', None)],
    128: [('Feed the Streets', "Juicy J, Project Pat & A$AP Rocky - 'Feed the Streets' (Project Pat's verse)", 'sample', True)],
    40: [("Get 'Em High", "Kanye West - 'Get 'Em High' (2004), a line interpolated at the end", 'interpolation', None)],
    93: [('God Did', "DJ Khaled - 'God Did' and Drake - 'Chicago Freestyle'", 'interpolation', None)],
}

# ---- 12. Display-only evidence text for table 4d: cid -> text shown in the evidence cell -----------------------
# Used where the automatically shortened research text cut off the deciding words or carried a premise the header
# corrects. The status and the basis on file are not changed.
EVIDENCE_DISPLAY = {
    2: "Billboard's 'Chart Highlights for Oct. 17, 2026' and a chart-beat story (also on Yahoo) say 'Solar Eclipse' debuted at No. 1 on "
       "Hot R&B/Hip-Hop Songs and at No. 1 on Hot R&B Songs (search-result summaries; the Hot Rap Songs page for that week was not seen).",
    123: "Absent from Billboard's 2022 year-end Hot Rap Songs (top 49 in the summary), Hot R&B/Hip-Hop Songs (through No. 99) and Hot R&B Songs "
         "(through No. 49), per search summaries of those pages; most of its top-10 run, fall 2021 into early 2022, falls in that chart year. "
         "Lil Nas X's 'Industry Baby' is No. 5 on the same rap list.",
}

# ---- 11. Lyric records the AI reader flagged as incomplete: cid -> note shown under table 4b ------------------
LYRIC_RECORD_NOTES = {
    52: "the record transcribes only the hook; the rap verses are missing, so the verse columns show a dash and the gaps in it are not breaks",   # Carnival
}
