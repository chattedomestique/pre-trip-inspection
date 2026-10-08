"""Builds pre-trip-inspection.html from src/ and vendor/. Run: python3 build.py"""
import re, base64, pathlib, json, html, sys
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
import diagrams as dia
SG = ROOT / 'vendor' / 'styleguide'
B = ROOT / 'src'

core = (SG/'core.min.css').read_text()
faces = re.findall(r'@font-face\{[^}]*\}', core)
latin = [f for f in faces if 'archivo-latin-var' in f][0]
b64 = base64.b64encode((SG/'fonts'/'archivo-latin-var.woff2').read_bytes()).decode()
latin = latin.replace('url("fonts/archivo-latin-var.woff2")', 'url("data:font/woff2;base64,%s")' % b64)
for f in faces: core = core.replace(f, '')
core = latin + core
els = ''.join((SG/('elements/%s.min.css' % n)).read_text() for n in ['button','appbar','list','progress','tag'])
icons_css = (SG/'icons.css').read_text()
need = ['arrow-right','arrow-left','rotate-ccw','chevron-right','chevron-left','circle-check','flag','check']
rules = []
for n in need:
    m = re.search(r'\.ic--%s\{[^\n]*\}' % re.escape(n), icons_css)
    if m: rules.append(m.group(0))
icons = '@layer sg.base{' + ''.join(rules) + '}'
css = core + els + icons + (B/'diagrams.css').read_text() + (B/'page.css').read_text()

# ---------- content ----------
def md(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*(.+?)\*(?!\*)', r'<em>\1</em>', t)
    return t

secs = []; cur = None
for raw in (B/'content.txt').read_text().splitlines():
    if not raw.strip() or raw.startswith('#  ') or raw.startswith('# '): continue
    if raw.startswith('## '):
        sid, title, pg, d, lab, sub = [x.strip() for x in raw[3:].split('|')]
        assert d in dia.DIA, d
        cur = {'id': sid, 'title': title, 'pg': pg, 'dia': d, 'lab': lab, 'sub': sub, 'items': []}
        secs.append(cur); continue
    idx, name, opts, text = [x.strip() for x in raw.split('|', 3)]
    it = {'i': '•' if idx in ('!', '0', '0b') else idx, 'n': name, 't': md(text), 'p': []}
    for tok in opts.split():
        k, v = tok.split('=', 1)
        if k == 'p': it['p'] = [x for x in v.split(',') if x]
        elif k == 'dia': assert v in dia.DIA, v; it['d'] = v
        elif k == 'lab': it['l'] = v
    cur['items'].append(it)

# every part id a line names must exist in its diagram
bad = []
for s in secs:
    for it in s['items']:
        d = it.get('d', s['dia'])
        have = set(re.findall(r'data-id="([^"]+)"', dia.DIA[d]))
        for p in it['p']:
            if p != '*' and p not in have: bad.append((s['id'], it['i'], d, p))
if bad: print('MISSING PARTS', bad); sys.exit(1)

labels = {'say': 'You must say', 'point': 'Point and say', 'do': 'Do', 'ind': 'Indicate', 'tell': 'Tell the tester', 'note': 'Remember'}
used = sorted({d for s in secs for d in [s['dia']] + [it['d'] for it in s['items'] if 'd' in it]})
data = {'secs': secs, 'dias': {k: dia.DIA[k] for k in used}, 'labels': labels}
data_js = 'var DATA=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';'

PAGE = lambda extra='': '<div class="page"><header class="appbar" id="bar"></header>' + extra + '<div class="view" id="home"></div><div class="view" id="run" hidden></div></div>'
JS = (B/'app.js').read_text()
shell_head = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="color-scheme" content="light dark">\n'

# 1. the single file: opens from anywhere, no install
out = f'<title>Pre-Trip Inspection</title>\n<style>{css}</style>\n{PAGE()}\n<script>var PWA=false;{data_js}\n{JS}</script>\n'
(ROOT/'pre-trip-inspection.html').write_text(shell_head + '</head>\n<body>\n' + out + '</body>\n</html>\n')

# 2. the installable app, in docs/ so GitHub Pages can serve it
import hashlib
DOCS = ROOT / 'docs'; (DOCS/'icons').mkdir(parents=True, exist_ok=True)
head = (shell_head +
  '<meta name="theme-color" content="#f5f5f5" media="(prefers-color-scheme: light)">\n<meta name="theme-color" content="#0e0e0e" media="(prefers-color-scheme: dark)">\n'
  '<title>Pre-Trip Inspection</title>\n<link rel="manifest" href="manifest.webmanifest">\n'
  '<link rel="icon" href="icons/icon-192.png" type="image/png">\n<link rel="apple-touch-icon" href="icons/apple-touch-icon-180.png">\n'
  '<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-capable" content="yes">\n'
  '<meta name="apple-mobile-web-app-title" content="Pre-Trip">\n<meta name="apple-mobile-web-app-status-bar-style" content="default">\n')
update = '<div class="update" id="update" role="status" hidden><p>A new version is ready.</p><button class="btn" data-size="sm" data-variant="primary" type="button" id="update-go">Reload</button></div>'
pwa_css = (B/'pwa.css').read_text()
index = (head + f'<style>{css}{pwa_css}</style>\n</head>\n<body>\n{PAGE(update)}\n<script>var PWA=true;{data_js}\n{JS}</script>\n<script>{(B/"pwa.js").read_text()}</script>\n</body>\n</html>\n')
(DOCS/'index.html').write_text(index)
(DOCS/'manifest.webmanifest').write_text((B/'manifest.webmanifest').read_text())
(DOCS/'.nojekyll').write_text('')
h = hashlib.sha1()
for p in [DOCS/'index.html', DOCS/'manifest.webmanifest'] + sorted((DOCS/'icons').glob('*.png')): h.update(p.read_bytes())
(DOCS/'sw.js').write_text((B/'sw.js').read_text().replace('__VERSION__', h.hexdigest()[:10]))
print('pre-trip-inspection.html and docs/ written; app version', h.hexdigest()[:10])
