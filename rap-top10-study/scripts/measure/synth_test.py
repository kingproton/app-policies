"""Synthetic check of audio_feel: known patterns in, felt BPM out."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpaths import SP
import numpy as np, soundfile as sf, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio_feel import analyze
SR = 22050; rng = np.random.default_rng(7)
def burst(n, lo, hi, dec):
    x = rng.standard_normal(n); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, n) * np.exp(-np.arange(n) / (dec * SR))
def kick():
    n = int(0.25 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (45 + 80 * np.exp(-t * 30)) * t) * np.exp(-t * 14) * 1.2
def sub(dur):
    n = int(dur * SR); t = np.arange(n) / SR; return 0.6 * np.sin(2 * np.pi * 46 * t) * np.exp(-t * 1.5)
def clap(): return 0.9 * burst(int(0.12 * SR), 900, 6000, 0.03)
def ckick():   # kick with a beater click (broadband transient)
    k = kick(); c = 0.55 * burst(int(0.03 * SR), 600, 5000, 0.006); k[:len(c)] += c; return k
def snare():
    n = int(0.15 * SR); t = np.arange(n) / SR; return 0.8 * burst(n, 400, 7000, 0.04) + 0.3 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25)
def hat(): return 0.25 * burst(int(0.03 * SR), 7500, 11000, 0.008)
def vocal(dur):
    n = int(dur * SR); t = np.arange(n) / SR; f0 = rng.uniform(110, 220)
    v = sum(np.sin(2 * np.pi * f0 * h * t) / h for h in range(1, 12)) * np.hanning(n) * 0.25
    return v + 0.15 * burst(n, 2000, 6000, 0.02)
def render(felt, style, dur=30.0, vocals=True):
    y = np.zeros(int(dur * SR) + SR); fb = 60.0 / felt
    def put(sig, t):
        i = int(t * SR)
        if i < len(y) - len(sig): y[i:i + len(sig)] += sig
    nb = int(dur / (4 * fb))
    for b in range(nb + 1):
        t0 = b * 4 * fb + 0.37
        if style == 'trap':        # hats on felt 16ths with rolls; kicks syncopated; clap on 2 and 4
            for k in range(16): put(hat(), t0 + k * fb / 4)
            for k in (12, 12.5, 13, 13.5) if b % 2 else (): put(hat(), t0 + k * fb / 4 + fb / 8)
            for k in ((0, 2.75, 3.5) if b % 2 == 0 else (0, 1.5, 2.5)): put(kick(), t0 + k * fb); put(sub(fb), t0 + k * fb)
            put(clap(), t0 + fb); put(clap(), t0 + 3 * fb)
        elif style == 'boombap':   # hats on 8ths; kick 1, 2.5, 3; snare 2 and 4
            for k in range(8): put(hat(), t0 + k * fb / 2)
            for k in (0, 1.5, 2): put(kick(), t0 + k * fb)
            put(snare(), t0 + fb); put(snare(), t0 + 3 * fb)
        elif style == 'bounce':    # hats 16ths; kick 1, 1.75, 3; clap 2 and 4
            for k in range(16): put(hat(), t0 + k * fb / 4)
            for k in (0, 0.75, 2, 2.75): put(kick(), t0 + k * fb); put(sub(fb / 2), t0 + k * fb)
            put(clap(), t0 + fb); put(clap(), t0 + 3 * fb)
        elif style == 'drill':     # hats in triplet-ish 8ths; snare on 2 and the 8th before 4.5 (displaced)
            for k in range(8): put(hat(), t0 + k * fb / 2)
            for k in (0, 0.75, 2.5): put(kick(), t0 + k * fb); put(sub(fb), t0 + k * fb)
            put(snare(), t0 + fb); put(snare(), t0 + (3 if b % 2 == 0 else 3.5) * fb)
        elif style == 'fourfloor':  # clicky kick on every beat; clap on 2 and 4 over the kick; off-beat hats
            for k in range(4): put(ckick(), t0 + k * fb); put(hat(), t0 + (k + 0.5) * fb)
            put(clap(), t0 + fb); put(clap(), t0 + 3 * fb)
        elif style == 'westbounce':  # clap on 2 and 4 with a bass note under each clap; kick 1, 2.5, 3.5
            for k in range(8): put(hat(), t0 + k * fb / 2)
            for k in (0, 1.5, 2.5): put(kick(), t0 + k * fb)
            for k in (1, 3): put(clap(), t0 + k * fb); put(sub(fb / 2), t0 + k * fb); put(kick(), t0 + k * fb)
        elif style == 'clickboombap':  # clicky kick on 1 and 3 (plus 2.5); snare on 2 and 4
            for k in range(8): put(hat(), t0 + k * fb / 2)
            for k in (0, 1.5, 2): put(ckick(), t0 + k * fb)
            put(snare(), t0 + fb); put(snare(), t0 + 3 * fb)
        elif style == 'clicktrap':   # clicky kick on 1 and 3; clap on 2 and 4; hats on 16ths
            for k in range(16): put(hat(), t0 + k * fb / 4)
            for k in (0, 2): put(ckick(), t0 + k * fb); put(sub(fb), t0 + k * fb)
            put(clap(), t0 + fb); put(clap(), t0 + 3 * fb)
        elif style == 'drill2':      # snare on 2 and on the and-of-4 in every bar
            for k in range(8): put(hat(), t0 + k * fb / 2)
            for k in (0, 0.75, 2.5): put(kick(), t0 + k * fb); put(sub(fb), t0 + k * fb)
            put(snare(), t0 + fb); put(snare(), t0 + 3.5 * fb)
        elif style == 'club':        # five-kick club pattern (1, 2, 3, 3.75, 4.5) with a clap on 2 and 4
            for k in (0, 1, 2, 2.75, 3.5): put(ckick(), t0 + k * fb)
            for k in range(8): put(hat(), t0 + k * fb / 2)
            put(clap(), t0 + fb); put(clap(), t0 + 3 * fb)
        if vocals:
            for k in range(16):
                if rng.random() < 0.62: put(vocal(fb / 4 * rng.uniform(0.6, 1.0)), t0 + k * fb / 4 + rng.normal(0, 0.012))
    y = y[:int(dur * SR)]; return (y / np.abs(y).max() * 0.8).astype(np.float32)
OUT = SP + 'net/synth/'
os.makedirs(OUT, exist_ok=True)
results = []
ok = 0; tests = [(72, 'trap'), (81, 'trap'), (65, 'trap'), (60.5, 'trap'), (87, 'trap'), (90, 'boombap'), (86, 'boombap'), (100, 'bounce'), (105, 'bounce'), (133, 'bounce'), (72, 'drill'), (74, 'drill'),
    (127, 'fourfloor'), (120, 'fourfloor'), (101, 'westbounce'), (96, 'westbounce'), (90, 'clickboombap'), (84, 'clickboombap'),
    (70, 'clicktrap'), (77, 'clicktrap'), (71, 'drill2'), (72.5, 'drill2'), (140, 'club'), (72, 'club')]
for felt, style in tests:
    p = OUT + f'{style}_{felt}.wav'; sf.write(p, render(felt, style), SR)
    r = analyze(p)
    good = abs(r['felt_bpm'] - felt) / felt < 0.03; ok += good
    results.append(dict(pattern=style, true_felt_bpm=felt, estimated_felt_bpm=r['felt_bpm'], pulse_bpm=r['pulse_bpm'], score=r['score'], margin=r['margin'], correct=bool(good)))
    print(f"{style:8} true felt {felt:6} -> est {r['felt_bpm']:7} (pulse {r['pulse_bpm']}, score {r['score']}, margin {r['margin']}, runner-up {r['runner_up']}) {'OK' if good else 'MISS'}  {r['candidates']}")
print(ok, 'of', len(tests), 'correct')
# optional argument: a folder to write the result to (data/measured/ in the repository)
if len(sys.argv) > 1:
    import json
    json.dump(dict(note='Felt-tempo estimator run on synthetic drum patterns with a known felt tempo; correct = within 3%.', correct=int(ok), patterns=len(tests), results=results),
              open(sys.argv[1].rstrip('/') + '/synthetic_feel_test.json', 'w'), indent=0)
