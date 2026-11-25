#!/usr/bin/env bash
# Re-run the analysis from the frozen research data (data/raw/) and the derived measurements (data/measured/),
# and regenerate every derived file.
# collect.py is not re-run: it read this session's workflow journals; data/raw/collected.json is its frozen output.
# top10.py / candidates.py / chartmetrics.py rebuild the chart data and need data/raw/all.json (run fetch_charts.py first).
set -euo pipefail
cd "$(dirname "$0")"
python3 classify_merge.py > /dev/null
python3 track_merge.py
python3 measure_merge.py
python3 aggregate.py > /dev/null
python3 exclusion_grades.py > /dev/null
python3 chart_check.py > /dev/null
python3 findings_stats.py > /dev/null
python3 measured_stats.py > /dev/null
python3 render_counts.py > /dev/null
python3 barmap.py > "${STUDY_WORK:-../data/raw/}barmap_tables.md"
python3 render_docs.py --check > /dev/null      # stop here, before any document is written, if a template cannot fill
python3 render_reference.py
python3 render_docs.py > /dev/null
echo "done: documents 01, 02, 03, 04, 05 and README, data/*.csv, data/raw/*.json, counts tables and bar-map tables regenerated"
