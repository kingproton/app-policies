# Bar-map timestamp calculator: 144 BPM grid, 4/4, 72 BPM felt (half-time).
GRID_BPM = 144.0
BEAT = 60.0 / GRID_BPM          # 0.416667 s per grid beat
BAR = 4 * BEAT                  # 1.666667 s per grid bar
def t(bar, beat=1, sub=0.0):
    """start time of grid bar `bar` (1-indexed), grid beat `beat` (1-4), plus fractional beat `sub`"""
    return (bar - 1) * BAR + (beat - 1 + sub) * BEAT
def mmss(s):
    m = int(s // 60); r = s - 60 * m
    return f"{m}:{r:04.1f}"
def felt(bar):  # felt bar number (72 BPM) containing grid bar
    return (bar + 1) // 2
blocks = [  # name, first grid bar, last grid bar
    ("Intro (beat only, 808 filtered)", 1, 4),
    ("Block 1 — Opening A: HOOK 1 | Opening B: VERSE 1a (cold image)", 5, 20),
    ("Block 2 — Opening A: VERSE 1a | Opening B: HOOK 1", 21, 36),
    ("Verse 1b — pocket change (double-time run)", 37, 44),
    ("Verse 1c — back to home pocket; ends in silence", 45, 52),
    ("Hook 2 (+ doubles on the title phrase)", 53, 68),
    ("Verse 2 (8 felt bars)", 69, 84),
    ("Drop: full-mix mute, one felt bar", 85, 86),
    ("Hook 3 (full stack + ad-lib answers)", 87, 102),
    ("Outro (beat rides out, tag)", 103, 106),
]
print("| Block | Grid bars (144) | Felt bars (72) | Start | End | Length |")
print("|---|---|---|---|---|---|")
for name, a, b in blocks:
    start, end = t(a), t(b + 1)
    print(f"| {name} | {a}–{b} ({b-a+1}) | {felt(a)}–{felt(b)} ({(b-a+1)//2 if (b-a+1)%2==0 else (b-a+1)/2}) | {mmss(start)} | {mmss(end)} | {end-start:.1f} s |")
print()
events = [
    ("Opening A first vocal: hook pickup (title phrase starts on the 'and' of grid beat 4)", 4, 4, 0.5),
    ("Opening A hook downbeat / title phrase lands", 5, 1, 0),
    ("Opening B first vocal: verse pickup", 4, 4, 0.5),
    ("Opening B first title phrase (last word of the cold verse, on the snare)", 19, 3, 0),
    ("Opening B hook downbeat", 21, 1, 0),
    ("Punch point P1 (Block 1) — pre-roll from grid bar 3", 5, 1, 0),
    ("Punch point P2 (Block 2) — pre-roll from grid bar 19", 21, 1, 0),
    ("Breath B1 (end of felt bar 12)", 24, 4, 0),
    ("Breath B2 (end of felt bar 14)", 28, 4, 0),
    ("Breath B3 (end of felt bar 16)", 32, 4, 0),
    ("Breath B4 — big breath before the run", 36, 3, 0.5),
    ("POCKET CHANGE: double-time run starts (punch point P3)", 37, 1, 0),
    ("Pocket returns home (punch point P4)", 45, 1, 0),
    ("Verse-ending punchline's last word on the snare", 51, 3, 0),
    ("SILENCE: no vocal, 808 muted (hats keep time) — 2.1 s", 51, 3, 0.5),
    ("Hook 2 downbeat (punch point P5)", 53, 1, 0),
    ("Verse 2 start (punch point P6)", 69, 1, 0),
    ("Verse 2 mid-point breath / punch point P7", 77, 1, 0),
    ("Drop: full-mix mute", 85, 1, 0),
    ("Hook 3 downbeat (punch point P8)", 87, 1, 0),
    ("Outro / end", 107, 1, 0),
]
print("| Event | Grid bar.beat | Felt bar | Time |")
print("|---|---|---|---|")
for name, bar, beat, sub in events:
    print(f"| {name} | {bar}.{beat}{'+' if sub else ''} | {felt(bar)} | {mmss(t(bar, beat, sub))} |")
