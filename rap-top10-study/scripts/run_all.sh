#!/usr/bin/env bash
# Re-run the analysis from the frozen research data (data/raw/) and regenerate every derived file.
# collect.py is not re-run: it read this session's workflow journals; data/raw/collected.json is its frozen output.
# top10.py / candidates.py / chartmetrics.py rebuild the chart data and need data/raw/all.json (run fetch_charts.py first).
set -euo pipefail
cd "$(dirname "$0")"
python3 classify_merge.py > /dev/null
python3 track_merge.py
python3 aggregate.py > /dev/null
python3 findings_stats.py > /dev/null
python3 render_counts.py > /dev/null
python3 render_reference.py
python3 barmap.py > "${STUDY_WORK:-../data/raw/}barmap_tables.md"
echo "done: 04-reference-list.md, data/*.csv, data/raw/*.json, counts table and bar-map tables regenerated"
