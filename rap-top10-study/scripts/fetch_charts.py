"""Download every weekly Hot 100 chart (the public mhollingshead/billboard-hot-100 mirror of billboard.com)
into WORK/all.json (about 44 MB; not committed). Needed only to re-run top10.py and chartmetrics.py."""
import os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
URL = 'https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/all.json'
dest = WORK + 'all.json'
if os.path.exists(dest):
    print('already present:', dest)
else:
    urllib.request.urlretrieve(URL, dest)
    print('saved', dest, os.path.getsize(dest), 'bytes')
