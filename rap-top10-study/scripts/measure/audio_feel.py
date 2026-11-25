"""Estimate tempo and the felt pulse (backbeat spacing) of a short audio clip.

Idea: the felt pulse of a rap beat is set by the backbeat. The snare or clap lands on felt beats 2 and 4, so
the backbeat spacing P is two felt beats and felt BPM = 120 / P. Published BPM listings cannot tell 72 from 144;
the backbeat can.

Steps
 1. Percussive spectrogram (HPSS) and band-limited onset envelopes: low (kick/808) and a snare/clap "body"
    envelope (geometric mean of mid and high percussive flux, so hats alone and kicks alone score low).
    The body envelope is NOT suppressed where a kick coincides: four-on-the-floor and bounce beats put a kick
    or bass note under the clap, and suppressing those hid the backbeat.
 2. Tempo family: the strongest harmonic-sum peak of the onset-envelope spectrum gives a precise pulse rate T*
    (commercial rap is grid-locked, so one constant tempo per clip is assumed).
 3. Every candidate is scored at its own best bar phase (all phases over one bar, in steps of one analysis frame,
    11.6 ms). A shared phase-locked grid was tried and dropped: claps often sit 20 to 40 ms off the kick grid.
 4. For each felt-tempo candidate in the octave family of T* and each grid shift (triplet-related tempi are
    scored too, but only as a diagnostic), fold the envelopes into one bar of 16 steps and score the backbeat template:
        back2 = body on beat 2;  back4 = body on beat 4, or on the "and" of 4 (displaced drill backbeat)
        on    = body on beats 1 and 3
        score = min(back2, back4) * balance - max(on) + 0.3 * (kick on 1 - kick on the backbeats, floored at -1)
    A candidate that is too slow puts real backbeats on its beats 1 and 3 (score near 0); one that is too fast
    cannot have backbeats on both its 2 and 4 unless the kick is as loud in the snare band as the snare, and
    then the kick term and the balance factor count against it.
 5. The winner is the felt tempo; the margin over the best candidate in a different octave is the confidence.
"""
import numpy as np, librosa

HOP = 256; NFFT = 2048; SR = 22050
LO_BPM, HI_BPM = 46.0, 185.0


def envelopes(y, sr=SR):
    S = np.abs(librosa.stft(y, n_fft=NFFT, hop_length=HOP))
    _, P = librosa.decompose.hpss(S, margin=(1.0, 3.0))
    f = librosa.fft_frequencies(sr=sr, n_fft=NFFT)

    def flux(lo, hi, M):
        B = np.log1p(20.0 * M[(f >= lo) & (f < hi)])
        return np.concatenate([[0.0], np.maximum(0.0, np.diff(B, axis=1)).sum(axis=0)])

    def nrm(x):
        m = np.percentile(x, 99) or 1.0
        return np.clip(x / m, 0, 1.5)
    low = nrm(flux(30, 140, S)); mid = nrm(flux(180, 1800, P)); high = nrm(flux(1800, 6000, P)); full = nrm(flux(30, 11000, P))
    body = np.sqrt(np.maximum(mid, 1e-9) * np.maximum(high, 1e-9))
    return dict(full=full, body=body, low=low)


def pulse_rate(env, sr=SR, lo=55.0, hi=190.0):
    """Precise pulse tempo T* (BPM) from a harmonic sum over the zero-padded envelope spectrum."""
    x = env - env.mean()
    n = int(2 ** np.ceil(np.log2(len(x) * 32)))
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x)), n))
    df = (sr / HOP) / n                                   # Hz per bin
    grid = np.arange(lo, hi, 0.02)
    def mag(freq_hz):
        idx = freq_hz / df; i0 = np.floor(idx).astype(int); fr = idx - i0
        i0 = np.clip(i0, 0, len(spec) - 2)
        return spec[i0] * (1 - fr) + spec[i0 + 1] * fr
    hs = sum(w * mag(grid / 60.0 * h) for h, w in ((1, 1.0), (2, 1.0), (4, 1.0), (8, 0.5)))
    return float(grid[np.argmax(hs)]), hs, grid


def maxfilt(x, k=2):
    return np.maximum.reduce([np.roll(x, s) for s in range(-k, k + 1)])


def robust_mean(a):
    """Trimmed mean down the bar axis (drops the top and bottom bar when there are 5 or more)."""
    nb = a.shape[0]
    if nb < 5: return a.mean(axis=0)
    t = max(1, int(0.12 * nb))
    return np.sort(a, axis=0)[t:nb - t].mean(axis=0)


def fold(env, felt, phase_frames, sr=SR):
    """Bar-folded 16-step profile of an envelope for one felt tempo and one phase (in frames)."""
    fps = sr / HOP
    step = 60.0 / felt * fps / 4.0
    bar = 16 * step
    nb = int((len(env) - phase_frames - bar) // bar)
    if nb < 3: return None, 0
    pos = phase_frames + np.arange(nb)[:, None] * bar + np.arange(16)[None, :] * step
    return robust_mean(np.interp(pos, np.arange(len(env)), env)), nb


def score_profile(b, lo):
    """Backbeat-template score of one folded bar (b: body, lo: low band; 16 steps each)."""
    back2 = b[4]; back4 = max(b[12], b[14])
    k4 = lo[12] if b[12] >= b[14] else lo[14]
    hi_, lo_ = max(back2, back4), min(back2, back4)
    balance = (lo_ / hi_) ** 0.5 if hi_ > 1e-6 else 0.0
    on = max(b[0], b[8])
    kick = max(-1.0, min(1.0, lo[0] - max(lo[4], k4)))
    return float(lo_ * balance - on + 0.3 * kick), float(lo_), float(on)


def fold_all(env, felt, sr=SR):
    """Bar-folded 16-step profiles for every phase (1-frame steps over one bar): array [n_phase, 16], and bar count."""
    fps = sr / HOP
    step = 60.0 / felt * fps / 4.0
    bar = 16 * step
    n_ph = int(np.ceil(bar))
    nb = int((len(env) - n_ph - bar) // bar)
    if nb < 3: return None, 0
    pos = np.arange(n_ph)[:, None, None] + np.arange(nb)[None, :, None] * bar + np.arange(16)[None, None, :] * step
    v = np.interp(pos, np.arange(len(env)), env)                      # [n_ph, nb, 16]
    if nb >= 5:
        t = max(1, int(0.12 * nb)); v = np.sort(v, axis=1)[:, t:nb - t]
    return v.mean(axis=1), nb


def analyze(path, keep_profiles=True):
    y, sr = librosa.load(path, sr=SR, mono=True)
    if len(y) < sr * 10: return None
    E = envelopes(y, sr)
    t_star, hs, grid = pulse_rate(E['full'], sr)
    body = maxfilt(E['body'], 2); low = maxfilt(E['low'], 2)
    ratios = {1.0: 'octave', 0.5: 'octave', 0.25: 'octave', 2.0: 'octave', 4.0: 'octave',
              2 / 3: 'triplet-related', 4 / 3: 'triplet-related', 1.5: 'triplet-related', 0.75: 'triplet-related'}
    fps = sr / HOP
    scored = []
    for r, fam in ratios.items():
        f = round(t_star * r, 3)
        if not (LO_BPM <= f <= HI_BPM): continue
        B, nb = fold_all(body, f, sr)
        if B is None: continue
        L, _ = fold_all(low, f, sr)
        best = None
        for k in range(B.shape[0]):
            sc, back, on = score_profile(B[k], L[k])
            if best is None or sc > best['score']:
                best = dict(felt=f, score=round(sc, 3), back=round(back, 3), on=round(on, 3), bars=nb, phase_s=round(k / fps, 3), family=fam,
                            body16=[round(float(x), 2) for x in B[k]], low16=[round(float(x), 2) for x in L[k]])
        scored.append(best)
    if not scored: return None
    scored.sort(key=lambda d: -d['score'])
    octs = [d for d in scored if d['family'] == 'octave']
    # Only the octave family decides. Triplet-related tempi are kept as a diagnostic: an event on every pulse beat
    # lands exactly on steps 4 and 12 of a six-beat fold and fakes a backbeat at two-thirds of the pulse.
    best = octs[0] if octs else scored[0]
    same = [d for d in scored if d['family'] == best['family'] and d is not best]
    second = same[0] if same else dict(felt=None, score=0.0)
    cross = [d for d in scored if d['family'] != best['family']]
    out = dict(pulse_bpm=round(t_star, 2), felt_bpm=round(best['felt'], 2), score=best['score'], back=best['back'], on=best['on'],
               runner_up=second['felt'], runner_up_score=second['score'], margin=round(best['score'] - second['score'], 3),
               first_downbeat_s=best['phase_s'], bars_used=best['bars'], family=best['family'], duration_s=round(len(y) / sr, 1),
               displaced_backbeat=bool(best['body16'][14] > best['body16'][12]),
               other_family_best=(cross[0]['felt'], cross[0]['score']) if cross else None,
               candidates=[(d['felt'], d['score'], d['family']) for d in sorted(scored, key=lambda d: d['felt'])])
    if keep_profiles:
        out['body16'] = best['body16']; out['low16'] = best['low16']
        if second.get('felt'): out['runner_up_body16'] = second['body16']
    return out
