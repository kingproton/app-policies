"""Polite cached HTTP fetcher for the verification pass. Honest client id, per-host spacing, on-disk cache."""
import os, time, urllib.request, urllib.parse, urllib.error, ssl, json
UA = "chart-research-script/1.0 (python; non-commercial research)"
_last = {}
SPACING = {'en.wikipedia.org': 1.6, 'ca.billboard.com': 1.0, 'itunes.apple.com': 3.2, 'lrclib.net': 0.6,
           'audio-ssl.itunes.apple.com': 0.3, 'www.songfacts.com': 2.0, 'songbpm.com': 1.5}
CTX = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE') or os.environ.get('REQUESTS_CA_BUNDLE') or '/root/.ccr/ca-bundle.crt')
PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
_opener = urllib.request.build_opener(urllib.request.ProxyHandler({'https': PROXY, 'http': PROXY} if PROXY else {}), urllib.request.HTTPSHandler(context=CTX))


def fetch(url, cache_path=None, retries=3, binary=False, timeout=45):
    """Return (status, body). Uses the cache when present. Never raises on HTTP errors."""
    if cache_path and os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
        data = open(cache_path, 'rb').read()
        return 200, (data if binary else data.decode('utf-8', 'replace'))
    host = urllib.parse.urlparse(url).netloc
    for attempt in range(retries):
        wait = SPACING.get(host, 1.5) - (time.time() - _last.get(host, 0))
        if wait > 0: time.sleep(wait)
        _last[host] = time.time()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
            with _opener.open(req, timeout=timeout) as r:
                data = r.read(); status = r.status
            if cache_path:
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                open(cache_path, 'wb').write(data)
            return status, (data if binary else data.decode('utf-8', 'replace'))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(8 * (attempt + 1)); continue
            return e.code, ''
        except Exception as e:
            if attempt < retries - 1: time.sleep(4 * (attempt + 1)); continue
            return 0, f'ERR {type(e).__name__}: {e}'
    return 0, ''


def wiki_raw(title, outdir):
    """Wikitext of an article through the crawl-permitted /wiki/ path."""
    safe = urllib.parse.quote(title.replace(' ', '_'), safe="()_,'!.-:")
    path = os.path.join(outdir, urllib.parse.quote(title.replace(' ', '_'), safe='') + '.wiki')
    return fetch(f"https://en.wikipedia.org/wiki/{safe}?action=raw", path)
