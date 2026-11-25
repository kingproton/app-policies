"""Derive timing and structure from time-synced lyrics (LRC) without keeping any lyric text.

Input: LRCLIB search results (working-directory cache). Output per track: timestamps, repetition ids, section map and
summary metrics. Lyric text is used in memory only (to detect repeated lines and count words) and is never written.

Method
 1. Parse LRC lines -> (time, text). Blank lines are kept as gap markers.
 2. Normalise each line (lowercase, drop bracketed ad-libs and punctuation) and give repeated lines the same id
    (exact match, or a close fuzzy match for lines of 3+ words).
 3. A line is "repeated material" when it sits in a run of >= 2 consecutive lines that occurs again elsewhere,
    or when the same line occurs >= 4 times. Runs of repeated material are hook-like sections (H); runs of
    unrepeated lines are verse-like sections (V). Short stray runs are folded into their neighbours.
 4. H sections are clustered by shared line ids. The cluster with the most total lines that occurs at least
    twice is the song's hook. Everything is reported with the first-line time of each section.
"""
import re, json, difflib, statistics, unicodedata


def parse_lrc(s):
    out = []
    for raw in (s or '').splitlines():
        m = re.match(r'\s*\[(\d+):(\d+(?:[.:]\d+)?)\]\s*(.*)$', raw)
        if not m: continue
        t = int(m.group(1)) * 60 + float(m.group(2).replace(':', '.'))
        out.append((t, m.group(3).strip()))
    out.sort(key=lambda x: x[0])
    return out


def norm_line(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    t = re.sub(r'\([^)]*\)|\[[^\]]*\]', ' ', t)
    t = re.sub(r"[^a-z0-9' ]+", ' ', t).replace("'", '')
    return re.sub(r'\s+', ' ', t).strip()


def syllables(word):
    w = re.sub(r'[^a-z]', '', word.lower())
    if not w: return 0
    n = len(re.findall(r'[aeiouy]+', w))
    if w.endswith('e') and not w.endswith(('le', 'ee')) and n > 1: n -= 1
    return max(1, n)


def assign_ids(norms):
    ids, reps = [], []
    for s in norms:
        hit = None
        for k, r in enumerate(reps):
            if s == r or (len(s.split()) >= 3 and len(r.split()) >= 3 and abs(len(s) - len(r)) <= 0.35 * max(len(s), len(r))
                          and difflib.SequenceMatcher(None, s, r).ratio() >= 0.84):
                hit = k; break
        if hit is None: reps.append(s); hit = len(reps) - 1
        ids.append(hit)
    return ids


def analyze(lrc_text, duration=None):
    raw = parse_lrc(lrc_text)
    lines = [(t, x) for t, x in raw if norm_line(x)]
    blanks = [t for t, x in raw if not x.strip()]
    if len(lines) < 8: return None
    times = [t for t, _ in lines]
    norms = [norm_line(x) for _, x in lines]
    words = [len(n.split()) for n in norms]
    sylls = [sum(syllables(w) for w in n.split()) for n in norms]
    ids = assign_ids(norms)
    n = len(ids)
    count = {}
    for i in ids: count[i] = count.get(i, 0) + 1
    rep = [False] * n
    # runs of >= 2 lines that recur (non-overlapping)
    for i in range(n):
        for j in range(i + 1, n):
            if ids[i] != ids[j]: continue
            k = 0
            while j + k < n and i + k < j and ids[i + k] == ids[j + k]: k += 1
            if k >= 2:
                for q in range(k): rep[i + q] = rep[j + q] = True
    for i in range(n):
        if count[ids[i]] >= 4 and words[i] >= 2: rep[i] = True
    # smooth: single unrepeated line inside repeated material, and single repeated line inside a verse
    for i in range(1, n - 1):
        if not rep[i] and rep[i - 1] and rep[i + 1]: rep[i] = True
    for i in range(1, n - 1):
        if rep[i] and not rep[i - 1] and not rep[i + 1]: rep[i] = False
    # segments, split also at long silences (blank marker or gap > 3x median spacing)
    gaps = [times[i + 1] - times[i] for i in range(n - 1)]
    med = statistics.median(gaps) if gaps else 3.0
    segs = []; start = 0
    for i in range(1, n + 1):
        brk = i == n or rep[i] != rep[i - 1] or (times[i] - times[i - 1]) > max(3.2 * med, 8.0)
        if brk:
            segs.append(dict(kind='H' if rep[start] else 'V', i0=start, i1=i - 1)); start = i
    # fold tiny segments into neighbours
    changed = True
    while changed and len(segs) > 1:
        changed = False
        for k, s in enumerate(segs):
            ln = s['i1'] - s['i0'] + 1
            if (s['kind'] == 'H' and ln < 2) or (s['kind'] == 'V' and ln < 2 and 0 < k < len(segs) - 1):
                nb = k - 1 if k > 0 else k + 1
                if times[min(s['i0'], segs[nb]['i0'])] is not None and abs(times[s['i0']] - times[segs[nb]['i1'] if nb < k else segs[nb]['i0']]) <= max(3.2 * med, 8.0):
                    a, b = min(k, nb), max(k, nb)
                    segs[a] = dict(kind=segs[nb]['kind'], i0=segs[a]['i0'], i1=segs[b]['i1']); del segs[b]; changed = True; break
        # merge adjacent same-kind segments that are not separated by a long silence
        k = 0
        while k < len(segs) - 1:
            if segs[k]['kind'] == segs[k + 1]['kind'] and times[segs[k + 1]['i0']] - times[segs[k]['i1']] <= max(3.2 * med, 8.0):
                segs[k] = dict(kind=segs[k]['kind'], i0=segs[k]['i0'], i1=segs[k + 1]['i1']); del segs[k + 1]; changed = True
            else: k += 1
    end_time = max(duration or 0, times[-1] + med)        # some records carry a wrong duration field
    for k, s in enumerate(segs):
        s['start'] = round(times[s['i0']], 2)
        s['end'] = round(times[segs[k + 1]['i0']] if k + 1 < len(segs) else min(end_time, times[s['i1']] + 2 * med), 2)
        s['last_line_start'] = round(times[s['i1']], 2)
        s['n_lines'] = s['i1'] - s['i0'] + 1
        s['words'] = sum(words[s['i0']:s['i1'] + 1]); s['sylls'] = sum(sylls[s['i0']:s['i1'] + 1])
        s['idset'] = sorted(set(ids[s['i0']:s['i1'] + 1]))
    # cluster hook-like sections
    H = [s for s in segs if s['kind'] == 'H']
    clusters = []
    for s in H:
        for c in clusters:
            a, b = set(s['idset']), set(c['ids'])
            if len(a & b) / max(1, min(len(a), len(b))) >= 0.5:
                c['members'].append(s); c['ids'] = sorted(a | b); break
        else: clusters.append(dict(ids=list(s['idset']), members=[s]))
    for ci, c in enumerate(clusters):
        for s in c['members']: s['cluster'] = ci
    multi = [c for c in clusters if len(c['members']) >= 2]
    hook = max(multi, key=lambda c: sum(m['n_lines'] for m in c['members'])) if multi else None
    hook_id = clusters.index(hook) if hook else None
    # a single hook-like block made of an internally repeated chant also counts as a refrain, but not as a returning hook
    labels = []
    for s in segs:
        if s['kind'] == 'H': labels.append('HOOK' if s.get('cluster') == hook_id and hook else 'REFRAIN')
        else: labels.append('VERSE' if s['n_lines'] >= 4 else 'BRIDGE_OR_INTRO')
    for s, lab in zip(segs, labels): s['label'] = lab
    verses = [s for s in segs if s['label'] == 'VERSE']
    hooks = [s for s in segs if s['label'] == 'HOOK']
    first_verse = verses[0]['start'] if verses else None
    first_hook = hooks[0]['start'] if hooks else None
    def dens(ss, key):
        d = sum(max(0.1, min(s['end'], s['last_line_start'] + 1.5 * med) - s['start']) for s in ss)
        return round(sum(s[key] for s in ss) / d, 2) if ss and d > 0 else None
    def line_gaps(ss):
        g = []
        for s in ss: g += [times[i + 1] - times[i] for i in range(s['i0'], s['i1'])]
        return g
    vg = line_gaps(verses); hg = line_gaps(hooks)
    # similarity of the hook's later occurrences to its first (ids only)
    hook_var = None
    if hooks and len(hooks) >= 2:
        base = ids[hooks[0]['i0']:hooks[0]['i1'] + 1]
        hook_var = [round(difflib.SequenceMatcher(None, base, ids[h['i0']:h['i1'] + 1]).ratio(), 2) for h in hooks[1:]]
    out = dict(
        n_lines=n, first_line_s=round(times[0], 2), last_line_s=round(times[-1], 2), median_line_gap_s=round(med, 3),
        opening_section=labels[0], opening_section_lines=segs[0]['n_lines'],
        has_returning_hook=bool(hook), hook_occurrences=len(hooks), first_hook_s=first_hook, first_verse_s=first_verse,
        hook_before_first_verse=(None if not hook else (True if first_verse is None else first_hook < first_verse)),
        lines_before_first_hook=(None if not hooks else hooks[0]['i0']),
        first_sustained_section_s=next((s['start'] for s in segs if s['n_lines'] >= 4), None),
        hook_durations_s=[round(h['end'] - h['start'], 1) for h in hooks], hook_lines=[h['n_lines'] for h in hooks],
        verse_durations_s=[round(v['end'] - v['start'], 1) for v in verses], verse_lines=[v['n_lines'] for v in verses],
        hook_return_similarity=hook_var,
        verse_median_line_gap_s=round(statistics.median(vg), 3) if vg else None,
        hook_median_line_gap_s=round(statistics.median(hg), 3) if hg else None,
        verse_words_per_s=dens(verses, 'words'), hook_words_per_s=dens(hooks, 'words'),
        verse_sylls_per_s=dens(verses, 'sylls'), hook_sylls_per_s=dens(hooks, 'sylls'),
        longest_gap_s=round(max(gaps), 2) if gaps else None, longest_gap_at_s=round(times[gaps.index(max(gaps))], 2) if gaps else None,
        repeated_line_share=round(sum(rep) / n, 2), blank_markers=len(blanks),
        sections=[dict(label=s['label'], start=s['start'], end=s['end'], lines=s['n_lines'], cluster=s.get('cluster')) for s in segs],
        order=' '.join({'HOOK': 'H', 'VERSE': 'V', 'REFRAIN': 'r', 'BRIDGE_OR_INTRO': 'b'}[s['label']] for s in segs),
        line_times=[round(t, 2) for t in times], line_ids=ids, line_words=words,
    )
    return out
