# 5 — Handoff: measure the listening-dependent fields (Codex, local agent, or you)

**Status of this study:** Claude could not listen to any recording. The cloud environment had no audio access, and its network policy blocked the lyric-timing and audio-preview hosts. The fields below are therefore **unknown** for most of the 100 tracks in `data/track_measurements.csv`. This brief lets another system fill them **from the actual recordings** with an auditable method.

## Objective

For each of the 100 tracks in `data/reference_100.csv`, measure the following from the audio. Write results to `data/listening_measurements.csv`, keyed by `n` (the list position), and keep every method auditable.

1. First lead-vocal entrance (s).
2. First hook/refrain entrance (s), and whether the track opens with it.
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
first_hook_s,opens_with_hook,section_labels,section_starts_s,section_bars_on_grid,median_punch_gap_ms,max_punch_gap_ms,
return_changes,method_notes,checked_by_hand
```

## Constraints

- Never write lyric text into any file; timestamps only.
- Never overwrite `track_measurements.csv`; write a new file and a diff report.
- Mark any value derived from a preview or a different edit; give the edit's duration.

## Acceptance criteria

- ≥90 of the 100 tracks have tempo, first vocal, first hook (or "no hook"), and section starts.
- The 10-track hand-check passes the tolerances above.
- A short `listening_findings.md` re-computes the counts in `03-findings.md` that depended on these fields. Flag any finding that flips.

## Known risks / questions to resolve rather than assume

- **Album vs single edits:** "Not Like Us" and several Drake tracks have video or clean edits with different intros. Use the version named in `version_used`.
- **Beat switches:** section segmentation will over-split songs with beat switches ("Rich Flex", "First Person Shooter", "Family Matters", "Meltdown"). Label each switch explicitly.
- **Half-time ambiguity:** jersey-club and bounce tracks ("Just Wanna Rock", "Not Like Us") may not follow the snare-on-3 rule. Resolve these by hand.
