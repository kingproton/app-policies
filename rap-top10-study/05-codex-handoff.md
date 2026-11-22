# 5 — Handoff: measure the listening-dependent fields (Codex, local agent, or you)

**Status of this study:** Claude could not listen to any recording. The cloud environment had no audio access, and its network policy blocked the lyric-timing and audio-preview hosts. As a result:
- fields 1 and 5, the hook timestamp in field 2 and the section times in field 3 are **unknown for all 100 tracks** (hook order in field 2 is sourced for only 7: 3 yes, 4 no);
- tempo has a published listing for 85 tracks, and 71 have a resolved grid/felt reading, but **every felt value is a genre-convention inference** (no source describes the feel);
- section-return changes (field 6) are described in text for 27 tracks (6 more were not re-confirmed by the verifier).

This brief lets another system fill them **from the actual recordings** with an auditable method.

## Objective

For each of the 100 tracks in `data/reference_100.csv`, measure the following from the audio. Write results to `data/listening_measurements.csv`, keyed by `n` (the list position), and keep every method auditable.

1. First lead-vocal entrance (s).
2. First hook/refrain entrance (s); whether the hook arrives before the first rap verse (the study's `hook_before_first_verse`); and whether it is literally the first sound (`opens_with_hook`).
3. Section boundaries (s) with labels.
4. Tempo, and the beat grid with half/double-time resolved.
5. Silence after the last word of each verse-ending line (ms).
6. Per-section changes in drums / 808 / melody / vocal density / doubles / ad-libs.

## Inputs

- `data/reference_100.csv`: title, artists, first top-10 date, plus the `version_used` column in `data/track_measurements.csv` (default: the original explicit album or single version).
- **Audio you are licensed to use.** Use the user's own purchased files, or 30-second previews only for the tempo cross-check. Do **not** download full tracks from unlicensed sources.
- Optional timing aid: time-synced lyrics from LRCLIB (`https://lrclib.net/api/get?artist_name=…&track_name=…&duration=…`), used **only for timestamps**. Never reproduce lyric text in any output.

## Method (required)

| Field | Method | Acceptance check |
|---|---|---|
| Tempo / grid | `librosa.beat.beat_track` plus a second estimator (e.g. `essentia` RhythmExtractor2013). Report both. If they differ by ×2 or ×0.5, resolve by snare position: snare on beat 3 of the bar means half-time feel, so grid = faster value and felt = grid ÷ 2. | Agrees with ≥1 published BPM in `track_measurements.csv` within ±2 BPM, after octave folding |
| First lead vocal | Separate vocals (Demucs `htdemucs`). The first vocal onset is where vocal-stem RMS stays above −35 dBFS for ≥250 ms. Classify it as ad-lib/tag vs lead line by duration (lead line ≥1.5 s). | Hand-spot-check 10 random tracks; error ≤0.3 s |
| Hook / sections | Self-similarity matrix on chroma + MFCC (e.g. `librosa.segment.agglomerative` or `msaf`), snapped to the nearest bar line of the resolved grid. The hook is the most-repeated vocal section; cross-check with LRCLIB timestamps where available. | Section count within ±1 of a manual label on 10 tracks |
| Silence after punchlines | On the vocal stem: gap (ms) between the last word offset of each section-ending line and the next vocal onset. | Report median and max per track |
| Section-return changes | Compare stem energy per section on first vs later occurrence: drums, bass (808), other, vocals. Flag changes > 3 dB, plus doubles (vocal-stem stereo width / correlation) and ad-lib density (short vocal events per bar). | Each flagged change listed with timestamp |

## Output schema (`data/listening_measurements.csv`)

```
n,title,audio_version,duration_s,bpm_est_1,bpm_est_2,grid_bpm,felt_bpm,feel_rule,first_vocal_s,first_vocal_type,
first_hook_s,hook_before_first_verse,opens_with_hook,opening_element,section_labels,section_starts_s,section_bars_on_grid,median_punch_gap_ms,max_punch_gap_ms,
return_changes,method_notes,checked_by_hand
```

## Constraints

- Never write lyric text into any file; timestamps only.
- Never overwrite `track_measurements.csv`; write a new file and a diff report.
- Mark any value derived from a preview or a different edit; give the edit's duration.

## Acceptance criteria

- ≥90 of the 100 tracks have tempo, first vocal, first hook (or "no hook"), and section starts.
- The 10-track hand-check passes the tolerances above.
- A short `listening_findings.md` re-computes the counts in `03-findings.md` that depended on these fields. Compare like with like: `hook_before_first_verse` against the study's `hook_before_first_verse` column, `opening_element` against `opening`, and the measured feel against the inferred `grid_bpm`/`felt_bpm`. Flag any finding that flips.

## Priority: the claims that would most change the findings

Measure these first. Each one is a place where the text-based study had to infer or could not confirm.

1. **Half- vs full-time feel (M-1).** Every felt value is inferred. Settle the 8 half-time readings at grid 112–126 first ("Janice STFU", "We Don't Trust You", "Agora Hills", "Virginia Beach", "Calling For You", "Meltdown", "Pussy & Millions", "Puffin On Zootiez"). Then settle the tracks marked `feel_unresolved` ("Shabang", "National Treasures", "Houdini", "Young Metro", "K-POP", "Just Wanna Rock").
2. **Openings and hook order (M-5).** Only 14 openings and 7 hook-order answers are sourced; 20 openings and 12 hook-order answers are marked **U** (cited, but a verifier could not confirm them).
3. **Beat switches (M-7).** Confirm or reject the 5 **U** switches ("What Did I Miss?", "Gimme A Hug", "7 Minute Drill", "First Person Shooter", "Champagne Poetry") and the 3 recollection-only ones ("Calling For You", "United In Grief", "Fair Trade"). All 18 "no switch" answers are recollection.
4. **Hooks (M-4).** 32 "hook present" answers and all 6 "no hook" answers are unverified.

## Known risks / questions to resolve rather than assume

- **Album vs single edits:** "Not Like Us" and several Drake tracks have video or clean edits with different intros. Use the version named in `version_used`; the version notes under table 4b list the ones most likely to be confused ("Princess Diana" is the chart-credited Nicki Minaj remix; "Carnival" is the current streaming version).
- **Beat switches:** section segmentation will over-split songs with beat switches ("Rich Flex", "First Person Shooter", "Family Matters", "Meltdown"). Label each switch explicitly.
- **Half-time ambiguity:** jersey-club and bounce tracks ("Just Wanna Rock", "Not Like Us") may not follow the snare-on-3 rule. Resolve these by hand.
