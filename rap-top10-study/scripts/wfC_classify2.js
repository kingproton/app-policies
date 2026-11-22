export const meta = {
  name: 'rap-top10-classify-v2',
  description: 'Budget-capped classification: year-end chart lists, same-week rap/R&B component charts, exclusion audit',
  phases: [
    { title: 'Lists', detail: 'year-end Hot Rap Songs / Hot R&B Songs lists' },
    { title: 'Classify', detail: 'week-cluster agents with hard search budgets' },
    { title: 'Audit', detail: 'exclusion audit of songs pre-tagged non-rap' },
  ],
}

const BUDGET_RULE = (n) => `HARD SEARCH BUDGET: you may make at most ${n} WebSearch calls in total for this job. The whole session shares a cap of 200 searches per turn, so overspending starves other agents. Plan your searches before you start. If any WebSearch call returns a notice that the search budget is used up, STOP searching immediately and finish with what you already have, marking anything unproven "unverified" (never guess).`

const COMMON = `Context: today is 2026-11-22. You are verifying a research reference set: the most recent rap songs to reach the top 10 of the U.S. Billboard Hot 100 (research cutoff 2026-11-22, starting chart 2026-11-21).
Tools: use WebSearch (load it with ToolSearch query "select:WebSearch" if it is not loaded). Direct fetching of billboard.com, wikipedia.org etc. is BLOCKED (curl/WebFetch fail) — do not try. WebSearch runs server-side and summarizes pages; mode "standard" unless results are thin.
GENRE RULE: a song counts as RAP if Billboard classified it as rap — it appeared on Hot Rap Songs (billboard.com/charts/rap-song/), or on a rap-only component chart (Rap Streaming Songs: /charts/rap-streaming-songs/; Rap Airplay: /charts/hot-rap-tracks/ — NOTE that slug is Rap Airplay, not Hot Rap Songs; Rap Digital Song Sales), or Billboard text says it charted on Hot Rap Songs. Billboard splits Hot R&B/Hip-Hop Songs into two MUTUALLY EXCLUSIVE subsets, Hot R&B Songs and Hot Rap Songs: a song on Hot R&B Songs (/charts/r-and-b-songs/) or R&B Streaming Songs is NOT rap for this study. Songs on neither (pop, country, Latin, rock, Afrobeats-only) are not rap.
MOST EFFICIENT EVIDENCE: one search for a same-week component chart page (e.g. "billboard rap streaming songs chart 2022-11-19" or "billboard hot r&b songs 2022-11-19") can classify every album track that week at once. Billboard chart-beat articles about album debuts often list which tracks debuted on Hot Rap Songs vs Hot R&B Songs. Wikipedia "Billboard Year-End Hot Rap Songs of YYYY" lists are definitive for songs that charted long enough to rank.
Model memory alone is not evidence: if you only remember it, use evidence_type "model_knowledge_only" with confidence "low".
Also confirm the stated Hot 100 rank from Billboard or press reporting when the same search shows it (do not spend extra searches only for rank). Do not reproduce lyrics.`

const SONG_SCHEMA = {
  type: 'object',
  properties: {
    cid: { type: 'integer' },
    title: { type: 'string' },
    hot_rap_songs: { type: 'string', enum: ['charted', 'not_charted', 'unverified'] },
    hot_rap_peak: { type: ['integer', 'null'] },
    same_week_on_hot_rap: { type: 'string', enum: ['yes', 'no', 'unknown'] },
    evidence_type: { type: 'string', enum: ['billboard_chart_page', 'billboard_article', 'wikipedia_chart_table', 'other_press', 'model_knowledge_only', 'none'] },
    evidence_summary: { type: 'string' },
    source_urls: { type: 'array', items: { type: 'string' } },
    other_genre_charts: { type: 'array', items: { type: 'string' } },
    crossover_note: { type: 'string' },
    hot100_rank_reported: { type: ['integer', 'null'] },
    rank_discrepancy: { type: 'string' },
    confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
  },
  required: ['cid', 'title', 'hot_rap_songs', 'evidence_type', 'evidence_summary', 'source_urls', 'confidence', 'same_week_on_hot_rap'],
}
const BATCH_SCHEMA = { type: 'object', properties: { songs: { type: 'array', items: SONG_SCHEMA }, searches_used: { type: 'integer' } }, required: ['songs'] }
const LISTS_SCHEMA = {
  type: 'object',
  properties: {
    lists: { type: 'array', items: { type: 'object', properties: {
      chart: { type: 'string' }, year: { type: 'integer' }, completeness: { type: 'string', enum: ['full', 'partial'] },
      source_url: { type: 'string' },
      entries: { type: 'array', items: { type: 'object', properties: { rank: { type: ['integer', 'null'] }, title: { type: 'string' }, artist: { type: 'string' } }, required: ['title'] } } },
      required: ['chart', 'year', 'completeness', 'entries'] } },
    searches_used: { type: 'integer' },
    notes: { type: 'string' },
  },
  required: ['lists'],
}
const AUDIT_SCHEMA = {
  type: 'object',
  properties: {
    flagged: { type: 'array', items: { type: 'object', properties: {
      entry: { type: 'string' }, reason: { type: 'string' }, hot_rap_songs: { type: 'string', enum: ['charted', 'not_charted', 'unverified'] }, source_urls: { type: 'array', items: { type: 'string' } } },
      required: ['entry', 'reason', 'hot_rap_songs', 'source_urls'] } },
    checked_clean: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['flagged', 'notes'],
}

const fmt = s => `cid=${s[0]} | first Hot 100 top-10 chart date ${s[1]} | rank that week #${s[2]} | "${s[3]}" — ${s[4]}`
const jobs = []
if (args.yearend) {
  jobs.push(() => agent(`${COMMON}\n\n${BUDGET_RULE(args.yearend.budget)}\n\nTASK: Retrieve Billboard year-end genre lists to classify songs in bulk. For each year ${args.yearend.years.join(', ')}: (1) "Billboard Year-End Hot Rap Songs of <year>" (Wikipedia list page or billboard.com/charts/year-end/<year>/hot-rap-songs) and (2) the year-end Hot R&B Songs list (billboard.com/charts/year-end/<year>/hot-r-and-b-songs or Wikipedia). Return every (rank, title, artist) row the search results show; mark completeness "partial" if you could not see the whole list. Prioritize the Hot Rap Songs lists.`,
    { label: 'yearend-lists', phase: 'Lists', schema: LISTS_SCHEMA }))
}
for (const g of (args.groups || [])) {
  jobs.push(() => agent(`${COMMON}\n\n${BUDGET_RULE(g.budget)}\n\nHINT: ${g.hint}\n\nVerify each of these ${g.songs.length} songs; return one entry per song (same cid), and report searches_used.\n${g.songs.map(fmt).join('\n')}`,
    { label: `classify:${g.label}`, phase: 'Classify', schema: BATCH_SCHEMA }))
}
if (args.audit) {
  jobs.push(() => agent(`${COMMON}\n\n${BUDGET_RULE(args.audit.budget)}\n\nEXCLUSION AUDIT. These songs reached the Hot 100 top 10 (first top-10 week shown) and were PRE-TAGGED NON-RAP without verification. Find any that Billboard actually classified as rap (Hot Rap Songs or a rap-only component chart); they would then belong in the reference set. Most are plainly pop/country/rock/Latin/R&B — do not spend searches on those. Spend your few searches only on entries with a rapper credited, trap/hip-hop production, or real doubt. Report flagged songs with evidence (or "unverified" if suspicious but unproven), and list in checked_clean the ones you specifically checked and found not rap.\n${args.audit.list.join('\n')}`,
    { label: 'exclusion-audit', phase: 'Audit', schema: AUDIT_SCHEMA }))
}
const out = await parallel(jobs)
return { results: out }
