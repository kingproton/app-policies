"""Paths for the measurement scripts.
SP  working directory: downloads (chart pages, article text, lyric records, preview audio) go here and are never
    committed; only the derived numbers in data/measured/ are. Set MEASURE_WORK to move it (default: <repo>/work/).
IN  the study's own inputs (final_rows.json, tracks_merged.json, to_verify.json, classification_status.json, and all.json /
    arrivals.json once fetch_charts.py and top10.py have run). Default: <repo>/data/raw/. Set MEASURE_INPUTS to move it."""
import os
_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SP = os.environ.get('MEASURE_WORK', os.path.join(_REPO, 'work')).rstrip('/') + '/'
IN = os.environ.get('MEASURE_INPUTS', os.path.join(_REPO, 'data', 'raw')).rstrip('/') + '/'
os.makedirs(SP + 'net', exist_ok=True)
