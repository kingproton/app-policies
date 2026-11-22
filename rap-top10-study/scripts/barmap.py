"""Bar-map and event-map generator for 02-worked-session.md (144 BPM grid, 4/4, 72 BPM felt).

Run it to print both markdown tables exactly as they appear in 02. Times round half up to 0.1 s.
Formula: start of grid bar n, beat b (+ fraction f of a beat) = (n - 1) * 1.6667 + (b - 1 + f) * 0.4167 s.
"""
from decimal import Decimal, ROUND_HALF_UP

GRID_BPM = 144
BEAT = Decimal(60) / Decimal(GRID_BPM)       # 0.41667 s per grid beat
BAR = 4 * BEAT                               # 1.66667 s per grid bar


def t(bar, beat=1, frac=0):
    return (bar - 1) * BAR + (Decimal(beat) - 1 + Decimal(str(frac))) * BEAT


def mmss(s):
    s = s.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    m = int(s // 60)
    return f"{m}:{s - 60 * m:04.1f}"


def felt(bar):
    return (bar + 1) // 2


def pos(bar, beat, frac):
    return f"{bar}.{beat}{'½' if frac else ''}"


BLOCKS = [  # name, first grid bar, last grid bar
    ("Intro — beat with the 808 filtered out (A: title tag at 3.1 · B: pickup at 4.4½)", 1, 4),
    ("Block 1 — **A:** Hook 1 · **B:** Verse 1a (cold image)", 5, 20),
    ("Block 2 — **A:** Verse 1a · **B:** Hook 1", 21, 36),
    ("Verse 1b — pocket change 1 (triplet run)", 37, 44),
    ("Verse 1c — home pocket; ends on silence", 45, 52),
    ("Hook 2 — title phrase doubled", 53, 68),
    ("Verse 2 — home pocket, pocket change 2 at felt bars 39–40", 69, 84),
    ("Drop — full mix out", 85, 86),
    ("Hook 3 — full stack, ad-lib answers", 87, 102),
    ("Outro — beat rides out", 103, 106),
]

EVENTS = [  # opening, label, grid bar, beat, fraction of a beat
    ("A", "FIRST VOCAL — title phrase spoken dry, once", 3, 1, 0),
    ("A", "HOOK 1 downbeat (808 enters)", 5, 1, 0),
    ("B", "FIRST VOCAL — verse pickup on the last 8th of the intro · punch P1 drops in at 4.4 (pre-roll from 3.1)", 4, 4, 0.5),
    ("both", "Breath — end of felt bar 4", 8, 4, 0),
    ("B", "Punch P1b — second half of the cold verse (pre-roll from 11.1, 0:16.7)", 13, 1, 0),
    ("both", "Breath — end of felt bar 6", 12, 4, 0),
    ("both", "Breath — end of felt bar 8", 16, 4, 0),
    ("B", "Title phrase first heard — last word of the cold verse, on the snare", 19, 3, 0),
    ("both", "Breath — end of felt bar 10", 20, 4, 0),
    ("B", "HOOK 1 downbeat", 21, 1, 0),
    ("A", "Verse 1a · punch P2 (pre-roll from 19.1)", 21, 1, 0),
    ("both", "Breath B1", 24, 4, 0),
    ("both", "Breath B2", 28, 4, 0),
    ("A", "Punch P2b — second half of Verse 1a (pre-roll from 27.1, 0:43.3)", 29, 1, 0),
    ("both", "Breath B3", 32, 4, 0),
    ("both", "Breath B4 — full breath before the run", 36, 3, 0.5),
    ("both", "**POCKET CHANGE 1** — triplet run starts · punch P3", 37, 1, 0),
    ("both", "Breath B5 — catch breath inside the run", 40, 4, 0),
    ("both", "Breath B6 — before the return", 44, 4, 0),
    ("both", "Pocket returns home · punch P4", 45, 1, 0),
    ("both", "Breath — end of felt bar 24", 48, 4, 0),
    ("both", "Verse 1 punchline — last word on the snare", 51, 3, 0),
    ("both", "**SILENCE** — vocal and 808 out, hats keep time (≈2.3 s, to 1:26.7)", 51, 3, 0.5),
    ("both", "HOOK 2 downbeat · paste point P5 (the comped Hook 1)", 53, 1, 0),
    ("both", "Breath — hook answer bar", 56, 4, 0),
    ("both", "Breath — hook answer bar", 60, 4, 0),
    ("both", "Breath — hook answer bar", 64, 4, 0),
    ("both", "Breath — before Verse 2", 68, 4, 0),
    ("both", "Verse 2 · punch P6", 69, 1, 0),
    ("both", "Breath", 72, 4, 0),
    ("both", "Breath", 76, 4, 0),
    ("both", "**POCKET CHANGE 2** — half-density 8ths, rhymes on the snare only · punch P7", 77, 1, 0),
    ("both", "Breath", 80, 4, 0),
    ("both", "Pocket returns home", 81, 1, 0),
    ("both", "Breath — before the drop", 84, 4, 0),
    ("both", "Drop — full mix out for one felt bar", 85, 1, 0),
    ("both", "HOOK 3 downbeat · paste point P8 (comp + full stack)", 87, 1, 0),
    ("both", "Breath — hook answer bar", 90, 4, 0),
    ("both", "Breath — hook answer bar", 94, 4, 0),
    ("both", "Breath — hook answer bar", 98, 4, 0),
    ("both", "End of song (end of felt bar 53)", 107, 1, 0),
]


def bar_table():
    out = ["| Block | Grid bars (144) | Grid count | Felt bars (72) | Felt count | Start | End |", "|---|---|---|---|---|---|---|"]
    for name, a, b in BLOCKS:
        n = b - a + 1
        out.append(f"| {name} | {a}–{b} | {n} | {felt(a)}–{felt(b)}" if felt(a) != felt(b) else f"| {name} | {a}–{b} | {n} | {felt(a)}")
        out[-1] += f" | {n // 2} | {mmss(t(a))} | {mmss(t(b + 1))} |"
    return out


def event_table():
    out = ["| Opening | Event | Grid bar.beat | Felt bar | Time |", "|---|---|---|---|---|"]
    for op, label, bar, beat, frac in sorted(EVENTS, key=lambda e: (t(e[2], e[3], e[4]), e[0] != 'both')):
        where = "106 end" if bar == 107 else pos(bar, beat, frac)
        out.append(f"| {op} | {label} | {where} | {felt(bar if bar < 107 else 106)} | {mmss(t(bar, beat, frac))} |")
    return out


if __name__ == '__main__':
    print('\n'.join(bar_table()))
    print()
    print('\n'.join(event_table()))
