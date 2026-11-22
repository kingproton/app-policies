"""Shared paths. Defaults point at the repository copy (rap-top10-study/data/raw/);
set STUDY_WORK / STUDY_REPO to run against another working directory."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get('STUDY_REPO', os.path.abspath(os.path.join(HERE, '..')) + '/')
WORK = os.environ.get('STUDY_WORK', os.path.join(REPO, 'data', 'raw') + '/')
