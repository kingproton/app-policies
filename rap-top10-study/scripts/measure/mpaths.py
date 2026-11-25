"""Working directory for the measurement scripts. Downloads (chart pages, article text, lyric records, preview audio)
go here and are never committed; only the derived numbers in data/measured/ are. Set MEASURE_WORK to move it."""
import os
SP = os.environ.get('MEASURE_WORK', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'work')).rstrip('/') + '/'
