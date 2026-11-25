"""Download Apple 30-second previews and measure tempo / felt pulse. Audio stays in the working directory only and is never committed."""
import sys, os, json, subprocess, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from netlib import fetch
from mpaths import SP
PV = SP + 'net/previews/'
M = json.load(open(SP + 'net/itunes_matches.json'))
def work(item):
    cid, v = item
    from audio_feel import analyze
    wav = PV + f'{cid}.wav'
    try:
        r = analyze(wav)
    except Exception as e:
        r = dict(error=f'{type(e).__name__}: {e}')
    return cid, r
if __name__ == '__main__':
    items = []
    for cid, v in M.items():
        m = v.get('match')
        if not m or not m.get('previewUrl'): continue
        m4a = PV + f'{cid}.m4a'; wav = PV + f'{cid}.wav'
        if not os.path.exists(wav):
            st, _ = fetch(m['previewUrl'], m4a, binary=True)
            if st != 200: print('download failed', cid, st, flush=True); continue
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', m4a, '-ac', '1', '-ar', '22050', wav], check=False)
        if os.path.exists(wav): items.append((cid, v))
    print('clips ready:', len(items), flush=True)
    out = {}
    with mp.Pool(3) as pool:
        for cid, r in pool.imap_unordered(work, items):
            out[cid] = r
            v = M[cid]
            print(v['n'], cid, v['title'][:26], '->', (r.get('felt_bpm'), r.get('pulse_bpm'), r.get('score'), r.get('margin')) if r and 'error' not in r else r, flush=True)
            json.dump(out, open(SP + 'net/audio_feel.json', 'w'), indent=1)
    print('analysed', len(out))
