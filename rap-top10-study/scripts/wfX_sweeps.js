export const meta = {
  name: 'rap-top10-gap-sweeps',
  description: 'Budget-capped gap sweeps: tempo values for tracks missing BPM, sourced structure for chart climbers, completeness critic',
  phases: [
    { title: 'Sweeps', detail: 'tempo sweep and structure sweep' },
    { title: 'Critic', detail: 'completeness and consistency review with spot checks' },
  ],
}

const BASE = `Context: today is 2026-11-22. You support a study of the most recent rap songs to reach the U.S. Billboard Hot 100 top 10. Use WebSearch (load it with ToolSearch query "select:WebSearch" if needed). Direct fetching of billboard.com / wikipedia.org / tunebat / songbpm / genius is BLOCKED; WebSearch runs server-side and summarizes pages. Nobody can listen to audio here: record a timestamp only if a cited page states it. Never reproduce lyrics (max 5-word quotes).`
const BUDGET = n => `HARD SEARCH BUDGET: at most ${n} WebSearch calls for this whole job (the session shares a 200-per-turn cap). If a search returns a budget-exhausted notice, stop and return what you have.`

const TEMPO_SCHEMA = { type: 'object', properties: { tracks: { type: 'array', items: { type: 'object', properties: {
  cid: { type: 'integer' }, title: { type: 'string' },
  values: { type: 'array', items: { type: 'object', properties: { bpm: { type: 'number' }, source: { type: 'string' } }, required: ['bpm', 'source'] } },
  grid_bpm: { type: ['number', 'null'] }, felt_bpm: { type: ['number', 'null'] }, key: { type: ['string', 'null'] }, runtime_mmss: { type: ['string', 'null'] }, runtime_source: { type: ['string', 'null'] }, note: { type: 'string' } },
  required: ['cid', 'values', 'grid_bpm', 'felt_bpm'] } }, searches_used: { type: 'integer' } }, required: ['tracks'] }
const STRUCT_SCHEMA = { type: 'object', properties: { tracks: { type: 'array', items: { type: 'object', properties: {
  cid: { type: 'integer' }, title: { type: 'string' },
  opening_element: { type: 'string', enum: ['producer_tag', 'sample_or_interpolation', 'ad_lib_or_spoken_intro', 'sung_intro', 'hook_or_chorus', 'rap_verse', 'instrumental', 'unknown'] },
  opening_basis: { type: 'string', enum: ['source', 'unverified_recollection', 'unknown'] }, opening_source: { type: ['string', 'null'] },
  hook_status: { type: 'string', enum: ['present_verified', 'present_unverified', 'absent_verified', 'absent_unverified', 'unknown'] },
  hook_first: { type: 'string', enum: ['yes', 'no', 'unknown'] }, hook_first_basis: { type: 'string', enum: ['source', 'unverified_recollection', 'unknown'] },
  first_hook_time: { type: ['string', 'null'] }, hook_device: { type: 'string' }, return_anchor: { type: 'string' },
  section_order: { type: ['array', 'null'], items: { type: 'string' } }, section_order_basis: { type: 'string', enum: ['source', 'unverified_recollection', 'unknown'] },
  beat_switch: { type: 'string', enum: ['yes', 'no', 'unknown'] }, beat_switch_basis: { type: 'string', enum: ['source', 'unverified_recollection', 'unknown'] },
  notable: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, source: { type: ['string', 'null'] }, timestamp: { type: ['string', 'null'] } }, required: ['claim'] } } },
  required: ['cid', 'opening_element', 'opening_basis', 'hook_status', 'hook_first', 'hook_first_basis', 'beat_switch', 'beat_switch_basis'] } }, searches_used: { type: 'integer' } }, required: ['tracks'] }
const CRITIC_SCHEMA = { type: 'object', properties: {
  issues: { type: 'array', items: { type: 'object', properties: { cid: { type: ['integer', 'null'] }, field: { type: 'string' }, problem: { type: 'string' }, suggested_fix: { type: 'string' } }, required: ['field', 'problem'] } },
  spot_checks: { type: 'array', items: { type: 'object', properties: { cid: { type: 'integer' }, claim: { type: 'string' }, verdict: { type: 'string', enum: ['supported', 'contradicted', 'unverifiable'] }, source: { type: ['string', 'null'] }, note: { type: 'string' } }, required: ['cid', 'claim', 'verdict'] } },
  overall: { type: 'string' } }, required: ['issues', 'spot_checks', 'overall'] }

const fmt = t => `cid=${t[0]} | "${t[1]}" — ${t[2]}${t[3] ? ' | ' + t[3] : ''}`
const jobs = []
if (args.tempo) jobs.push(() => agent(`${BASE}\n\n${BUDGET(args.tempo.budget)}\n\nTEMPO SWEEP. These tracks still lack a published tempo. For each, find listed BPM values (tunebat, songbpm, musicstax, getsongbpm, Melodics, Klang.io, Hooktheory, karaoke-version, Musicnotes via Wikipedia). Album-level pages (e.g. a musicstax or tunebat album page) list every track at once, so use them first. Record each value with its source. Then give grid_bpm (DAW convention; trap/drill/rage normally 120-180 with snare once per bar = half-time feel) and felt_bpm (rap-bar pulse: grid/2 for half-time trap; equal to grid for bounce/boom-bap/pop-rap at ~85-115). Leave null if nothing is found. Tracks marked NEEDS RUNTIME also lack a runtime: give runtime_mmss of the original album/single version with its source (album track listings give every length at once).\n${args.tempo.tracks.map(fmt).join('\n')}`,
  { label: 'tempo-sweep', phase: 'Sweeps', schema: TEMPO_SCHEMA }))
if (args.structure) jobs.push(() => agent(`${BASE}\n\n${BUDGET(args.structure.budget)}\n\nSTRUCTURE SWEEP for ${args.structure.purpose || 'songs that CLIMBED into the top 10 (they did not debut there), the most relevant subgroup for an independent artist.'} For each, establish from real pages: what the listener hears first (opening element); whether the song opens with its hook/chorus; whether a chorus exists (distinguish absent from unverified); the hook device (sample/interpolation, chant, sung melody, catchphrase, producer tag, call-and-response); the return anchor if there is no chorus; section order if a source describes it; beat switch yes/no; and any documented timestamps. Good sources: Wikipedia composition sections, Billboard/Complex/Pitchfork/Rolling Stone/Stereogum/Genius song-fact pages, producer interviews, Songfacts, Hooktheory. Use basis "unverified_recollection" only for coarse facts you could not source.\n${args.structure.tracks.map(fmt).join('\n')}`,
  { label: 'structure-sweep', phase: 'Sweeps', schema: STRUCT_SCHEMA }))
const first = await parallel(jobs)
let critic = null
if (args.critic) {
  phase('Critic')
  critic = await agent(`${BASE}\n\n${BUDGET(args.critic.budget)}\n\nCOMPLETENESS CRITIC. Below is a compact digest of the study's per-track measurements (one line per track: n | title | runtime | grid/felt BPM | opening (basis) | hook-first (basis) | hook status | beat switch (basis) | samples). Review it for: implausible values (e.g. runtimes, BPMs outside 55-200, half/double-time inconsistency with the style), internal contradictions, claims marked 'source' that look doubtful, and the most important gaps. Then spend your searches spot-checking ${args.critic.budget} of the most consequential or suspicious claims (prefer runtime/BPM/sample/beat-switch claims you can verify). Report issues and spot checks.\n${args.critic.digest}`,
    { label: 'completeness-critic', phase: 'Critic', schema: CRITIC_SCHEMA })
}
return { sweeps: first, critic }
