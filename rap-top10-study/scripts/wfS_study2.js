export const meta = {
  name: 'rap-top10-group-study',
  description: 'Budget-capped album/group study of rap Hot 100 top-10 songs: sourced observations, then independent verification',
  phases: [
    { title: 'Research', detail: 'one agent per album or single group' },
    { title: 'Verify', detail: 'independent check of numeric and structural claims per group' },
  ],
}

const COMMON = `Context: today is 2026-11-22. You are one of many agents studying the musical decisions in the most recent rap songs to reach the top 10 of the U.S. Billboard Hot 100. The end user is an independent rapper who wants studio-usable findings; accuracy and honest labeling matter more than coverage.
TOOLS: Use WebSearch (load it with ToolSearch query "select:WebSearch" if it is not already loaded). Direct fetching (curl/WebFetch) of billboard.com, wikipedia.org, genius.com, lrclib, musicbrainz, deezer, tunebat, songbpm etc. is BLOCKED by this environment's network policy — do not attempt it. WebSearch runs server-side and summarizes those pages. Use mode "standard"; use "extended" only when standard results are thin. Follow the HARD SEARCH BUDGET stated below.
NOBODY CAN LISTEN TO THE AUDIO in this environment. Therefore:
- Only record a timestamp (m:ss) if a cited source states it (e.g. a review saying "the beat switches at 2:10"). Never estimate or invent timestamps.
- Every observation carries a basis: "source" (you found it in a cited page — give the URL), "unverified_recollection" (you believe it from prior knowledge of the record but found no source — allowed ONLY for coarse facts such as whether the song opens with its hook, whether a chorus exists, or whether a beat switch exists; it will be reported separately as unverified), or the field is "unknown".
- Distinguish an ABSENT hook (a source says there is no chorus/hook) from an UNVERIFIED one.
- Do not reproduce lyrics. Quote at most 5 words of a lyric (e.g. a hook title phrase) when needed to identify a section.
TEMPO: Aggregator BPMs (tunebat, songbpm, musicstax, Melodics, Klang.io, Hooktheory, Musicnotes via Wikipedia, karaoke-version) often disagree by a factor of 2. Record each listed value with its source. Then give grid_bpm = the DAW/session tempo convention (for trap/drill/rage this is normally the faster value, typically 120-180, where the snare lands once per bar on beat 3 = half-time feel) and felt_bpm = the rap-bar pulse (backbeat on 2 and 4 of the felt bar; for half-time trap felt = grid/2; for boom-bap/West Coast bounce at ~85-110 felt = grid). Mark feel_basis "source" only if a source describes the feel; otherwise "genre_convention_inference".
VERSION: Identify the recording version you are describing (default: the original explicit album or single version on streaming services) and its runtime.`

const TRACK_SCHEMA = {
  type: 'object',
  properties: {
    cid: { type: 'integer' },
    title: { type: 'string' },
    artists: { type: 'string' },
    album: { type: 'string' },
    release_date: { type: 'string' },
    version_used: { type: 'string' },
    producers: { type: 'array', items: { type: 'string' } },
    runtime_mmss: { type: ['string', 'null'] },
    runtime_seconds: { type: ['number', 'null'] },
    runtime_sources: { type: 'array', items: { type: 'string' } },
    tempo_listed: { type: 'array', items: { type: 'object', properties: { bpm: { type: 'number' }, source: { type: 'string' } }, required: ['bpm', 'source'] } },
    grid_bpm: { type: ['number', 'null'] },
    felt_bpm: { type: ['number', 'null'] },
    feel_basis: { type: 'string', enum: ['source', 'genre_convention_inference', 'unknown'] },
    key: { type: ['string', 'null'] },
    style_tag: { type: 'string', enum: ['trap', 'melodic_trap', 'drill', 'rage', 'plugg_or_pluggnb', 'west_coast_bounce', 'boom_bap_or_verse_led', 'jersey_club', 'pop_rap', 'rnb_rap', 'dance_or_house_rap', 'country_rap', 'afro_or_latin_rap', 'other'] },
    style_basis: { type: 'string' },
    opening_element: { type: 'string', enum: ['producer_tag', 'sample_or_interpolation', 'ad_lib_or_spoken_intro', 'sung_intro', 'hook_or_chorus', 'rap_verse', 'instrumental', 'unknown'] },
    opening_basis: { type: 'string', enum: ['source', 'unverified_recollection', 'unknown'] },
    opening_detail: { type: 'string' },
    producer_tag_present: { type: 'string', enum: ['yes', 'no', 'unknown'] },
    producer_tag_detail: { type: 'string' },
    first_lead_vocal_time: { type: ['string', 'null'] },
    hook_status: { type: 'string', enum: ['present_verified', 'present_unverified', 'absent_verified', 'absent_unverified', 'unknown'] },
    hook_first: { type: 'string', enum: ['yes', 'no', 'unknown'] },
    hook_first_basis: { type: 'string', enum: ['source', 'unverified_recollection', 'unknown'] },
    first_hook_time: { type: ['string', 'null'] },
    hook_description: { type: 'string' },
    return_anchor: { type: 'string' },
    hook_devices: { type: 'array', items: { type: 'string', enum: ['sample_or_interpolation', 'title_chant_or_repetition', 'producer_tag', 'call_and_response', 'sung_melody', 'catchphrase_or_slogan', 'beat_switch_moment', 'feature_hook', 'other'] } },
    delivery_observations: { type: 'array', items: { type: 'object', properties: {
      aspect: { type: 'string', enum: ['phrase_placement', 'rhyme_landing', 'silence_or_space', 'flow_switch', 'density_or_speed', 'melodic_or_sung', 'ad_libs', 'doubles_or_stacks', 'conversational_or_spoken', 'other'] },
      observation: { type: 'string' }, basis: { type: 'string', enum: ['source', 'unverified_recollection'] }, source: { type: ['string', 'null'] }, timestamp: { type: ['string', 'null'] } },
      required: ['aspect', 'observation', 'basis'] } },
    section_order: { type: ['array', 'null'], items: { type: 'string' } },
    section_order_basis: { type: 'string', enum: ['source', 'unverified_recollection', 'unknown'] },
    beat_switch: { type: 'string', enum: ['yes', 'no', 'unknown'] },
    beat_switch_basis: { type: 'string', enum: ['source', 'unverified_recollection', 'unknown'] },
    beat_switch_detail: { type: 'string' },
    beat_switch_time: { type: ['string', 'null'] },
    features: { type: 'array', items: { type: 'object', properties: { artist: { type: 'string' }, role: { type: 'string' }, position: { type: 'string' } }, required: ['artist', 'role'] } },
    section_return_changes: { type: 'array', items: { type: 'object', properties: {
      element: { type: 'string', enum: ['drums', 'bass_808', 'melody_or_sample', 'vocal_density', 'doubles', 'ad_libs', 'arrangement_dropout', 'other'] },
      change: { type: 'string' }, basis: { type: 'string', enum: ['source', 'unverified_recollection'] }, source: { type: ['string', 'null'] }, timestamp: { type: ['string', 'null'] } },
      required: ['element', 'change', 'basis'] } },
    most_audible_change: { type: 'string' },
    samples: { type: 'array', items: { type: 'object', properties: { work: { type: 'string' }, how_used: { type: 'string' }, source: { type: ['string', 'null'] } }, required: ['work', 'how_used'] } },
    context_note: { type: 'string' },
    unknowns: { type: 'array', items: { type: 'string' } },
    sources: { type: 'array', items: { type: 'object', properties: { url: { type: 'string' }, supports: { type: 'string' } }, required: ['url', 'supports'] } },
  },
  required: ['cid', 'title', 'version_used', 'runtime_mmss', 'tempo_listed', 'grid_bpm', 'felt_bpm', 'feel_basis', 'style_tag', 'opening_element', 'opening_basis', 'hook_status', 'hook_first', 'hook_first_basis', 'beat_switch', 'beat_switch_basis', 'delivery_observations', 'section_return_changes', 'samples', 'unknowns', 'sources'],
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    cid: { type: 'integer' },
    runtime_status: { type: 'string', enum: ['confirmed', 'corrected', 'unverifiable'] },
    runtime_mmss: { type: ['string', 'null'] },
    runtime_note: { type: 'string' },
    tempo_status: { type: 'string', enum: ['confirmed', 'corrected', 'conflict', 'unverifiable'] },
    grid_bpm: { type: ['number', 'null'] },
    felt_bpm: { type: ['number', 'null'] },
    tempo_values_found: { type: 'array', items: { type: 'object', properties: { bpm: { type: 'number' }, source: { type: 'string' } }, required: ['bpm', 'source'] } },
    tempo_note: { type: 'string' },
    opening_status: { type: 'string', enum: ['confirmed', 'corrected', 'unverifiable'] },
    opening_element: { type: 'string', enum: ['producer_tag', 'sample_or_interpolation', 'ad_lib_or_spoken_intro', 'sung_intro', 'hook_or_chorus', 'rap_verse', 'instrumental', 'unknown'] },
    hook_first: { type: 'string', enum: ['yes', 'no', 'unknown'] },
    hook_first_basis: { type: 'string', enum: ['source', 'unverified_recollection', 'unknown'] },
    hook_status: { type: 'string', enum: ['present_verified', 'present_unverified', 'absent_verified', 'absent_unverified', 'unknown'] },
    beat_switch_status: { type: 'string', enum: ['confirmed', 'corrected', 'unverifiable'] },
    beat_switch: { type: 'string', enum: ['yes', 'no', 'unknown'] },
    beat_switch_basis: { type: 'string', enum: ['source', 'unverified_recollection', 'unknown'] },
    samples_status: { type: 'string', enum: ['confirmed', 'corrected', 'unverifiable', 'none_claimed'] },
    samples_note: { type: 'string' },
    flagged_claims: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, problem: { type: 'string' } }, required: ['claim', 'problem'] } },
    upgraded_to_source: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, source: { type: 'string' } }, required: ['claim', 'source'] } },
    overall_confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
  },
  required: ['cid', 'runtime_status', 'tempo_status', 'opening_status', 'hook_first', 'hook_status', 'beat_switch_status', 'beat_switch', 'flagged_claims', 'overall_confidence'],
}


const BUDGET_RULE = (n) => `HARD SEARCH BUDGET: at most ${n} WebSearch calls for this whole job. The session shares a cap of 200 searches per turn across all agents, so overspending starves others. Plan first. Prefer sources that cover several tracks at once: the Wikipedia ALBUM page (track listing with lengths, producers, sample credits; composition notes), album-level BPM/key listings (tunebat, songbpm, musicstax album pages), and track-by-track reviews (e.g. Billboard "every song ranked", Complex, Pitchfork, Rolling Stone, HipHopDX, Uproxx, The Ringer). If any WebSearch returns a notice that the budget is used up, STOP searching and finish with what you have, marking unproven fields unknown.`
const GROUP_SCHEMA = { type: 'object', properties: { tracks: { type: 'array', items: TRACK_SCHEMA }, searches_used: { type: 'integer' } }, required: ['tracks'] }
const GVERIFY_SCHEMA = { type: 'object', properties: { checks: { type: 'array', items: VERIFY_SCHEMA }, searches_used: { type: 'integer' } }, required: ['checks'] }
const G = args.groups || []
if (!G.length) throw new Error('no groups passed')
const fmt = t => `cid=${t[0]} | "${t[3]}" — ${t[4]} | first reached the Hot 100 top 10 on the chart dated ${t[1]} at #${t[2]}`
const out = await pipeline(
  G,
  g => agent(`${COMMON}\n\n${BUDGET_RULE(g.rb)}\n\nGROUP: ${g.label}. ${g.album || ''}\nTRACKS (return one entry per track, same cid):\n${g.tracks.map(fmt).join('\n')}\n\nFor every track answer the study's three questions wherever a reliable source supports it: (1) what the listener recognizes first (runtime, tempo and felt pulse, first lead-vocal entrance, first recognizable hook/refrain, or the return anchor if there is no chorus); (2) how the rapper rides the beat (phrase placement vs drums, rhyme landing, space after punchlines, changes between sections); (3) what changes when a section returns (section order, beat switches, drums/808/melody/vocal density/doubles/ad-libs, feature placement) and which change is audible enough to matter. Fill unknowns honestly; never invent timestamps.`,
    { label: `research:${g.label}`, phase: 'Research', schema: GROUP_SCHEMA }),
  (r, g) => {
    if (!r || !r.tracks) return { group: g, research: r, verify: null }
    const claims = r.tracks.map(x => ({ cid: x.cid, title: x.title, version_used: x.version_used, runtime_mmss: x.runtime_mmss, tempo_listed: x.tempo_listed, grid_bpm: x.grid_bpm, felt_bpm: x.felt_bpm, opening_element: x.opening_element, opening_basis: x.opening_basis, hook_status: x.hook_status, hook_first: x.hook_first, hook_first_basis: x.hook_first_basis, first_hook_time: x.first_hook_time, beat_switch: x.beat_switch, beat_switch_basis: x.beat_switch_basis, beat_switch_time: x.beat_switch_time, samples: (x.samples || []).map(s => s.work) }))
    return agent(`${COMMON}\n\n${BUDGET_RULE(g.vb)}\n\nYou are an independent fact-checker for GROUP: ${g.label}. A research agent produced these per-track claims:\n${JSON.stringify(claims)}\nRe-check with your OWN searches (do not trust the claims). Priorities, in order: (a) runtimes against an album track listing; (b) tempo against an album-level BPM listing from a DIFFERENT site than the researcher used, resolving half/double-time; (c) for tracks whose opening/hook/beat-switch claims are marked "source", confirm a real page supports them, and list unsupported ones in flagged_claims; list any "unverified_recollection" claim you confirmed from a real page in upgraded_to_source. Return one check per track (same cid). If evidence is missing, mark unverifiable — do not guess.`,
      { label: `verify:${g.label}`, phase: 'Verify', schema: GVERIFY_SCHEMA })
      .then(v => ({ group: g, research: r, verify: v }))
  },
)
return { results: out.filter(Boolean) }
