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
ALBUM_MATE_INFERRED = {32: 'Reincarnated'}   # Fair Trade, Champagne Poetry, In The Bible now have direct listings (overrides below)
# Version notes surfaced under table 4b (abridged from track_measurements.csv version_used).
VERSION_NOTES = {
    'Evil J0rdan': "album version (MUSIC track 4); a review says it has a new synthesized intro versus the earlier-circulated 'EvilJ0rdan'.",
    'Noid': 'album version (4:44), not the music-video edit, which drops the vocal intro and final verses.',
    'Carnival': "current explicit streaming version (4:24). The live 'Iron Man' sample is documented only for an earlier version, so it is not counted.",
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
    # Searched (4 searches each), still only indirect evidence.
    47: dict(status='unverified', evidence_type='wikipedia_chart_table', confidence='low', source_url='https://en.wikipedia.org/wiki/Cinderella_(Future,_Metro_Boomin_and_Travis_Scott_song)',
             summary="Searched: only a Hot R&B/Hip-Hop Songs peak (No. 3) was found, which does not separate rap from R&B; album-mate 'Like That' was No. 1 on Hot Rap Songs."),
    48: dict(status='unverified', evidence_type='wikipedia_chart_table', confidence='low', source_url="https://en.wikipedia.org/wiki/We_Don%27t_Trust_You_(song)",
             summary="Searched: Hot R&B/Hip-Hop Songs peak No. 5 and No. 79 on that chart's 2024 year-end list; no rap-chart row seen."),
    55: dict(status='unverified', evidence_type='wikipedia_chart_table', confidence='low', source_url='https://www.billboard.com/charts/rap-streaming-songs/2024-02-17/',
             summary="Searched: Hot R&B/Hip-Hop Songs peak No. 5 and Rhythmic No. 9; album-mate 'Redrum' was on Rap Streaming Songs (2024-02-17)."),
    69: dict(status='unverified', evidence_type='billboard_chart_page', confidence='low', source_url='https://www.billboard.com/charts/rap-streaming-songs/2023-08-12/',
             summary="Searched: Rap Streaming Songs pages from Aug-Sep 2023 show other Utopia songs, but FE!N itself never appeared in a result."),
    65: dict(status='unverified', evidence_type='other_press', confidence='low', source_url='https://currently.att.yahoo.com/att/doja-cat-paint-town-red-171023820.html',
             summary="Searched: Hot 100 No. 5, Global 200 No. 1 and Digital Song Sales No. 1 found, but no genre-chart placement. A summary that put it on Hot Rap Songs was about 'Paint The Town Red' and was discarded."),
    99: dict(status='unverified', evidence_type='wikipedia_chart_table', confidence='low', source_url='https://en.wikipedia.org/wiki/Bad_Decisions_(Benny_Blanco,_BTS_and_Snoop_Dogg_song)',
             summary="Searched: Wikipedia's chart table lists only Hot 100 (No. 10) and Pop Airplay (No. 26) for 2022; no genre-chart rows."),
    22: dict(status='not_rap', evidence_type='wikipedia_chart_table', confidence='medium', source_url='https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_Rap_Songs_of_2025',
             summary=("Inferred: absent from the 2025 year-end Hot Rap Songs list, which ranks Doechii's smaller 'Denial Is a River' at No. 10, while 'Anxiety' was No. 39 on the "
                      "2025 year-end Hot 100. A targeted re-check (4 searches) found no direct Hot R&B Songs or Hot Rap Songs row; chart-history rows on unnamed charts conflict "
                      "and may mix in the 2023 Sleepy Hallow track 'A N X I E T Y'.")),
}

# ---- 7. Independent re-check of the gap sweep's structure claims --------------------------
# cid -> {field: verdict}; verdict 'confirmed' keeps S; anything else drops a sweep-sourced value to U
# (hooks: present_verified -> present_unverified). Fields: opening_element, hook_before_first_verse,
# has_hook_or_chorus, beat_switch. 'partly' entries are resolved by hand to confirmed / not_supported.
SWEEP_VERDICTS = {
    8:   {'hook_before_first_verse': 'partly'},     # Shabang: opener is the line later used as the hook; order vs verse 1 not shown
    27:  {'opening_element': 'partly'},             # Squabble Up: Debbie Deb sample "near the beginning", not shown as first sound
    29:  {'hook_before_first_verse': 'partly'},     # Luther: sampled chorus first; the song's own hook vs verse 1 not placed
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
