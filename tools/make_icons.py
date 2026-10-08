"""Exports the app icons from src/mark.svg into docs/icons/. Run: python3 tools/make_icons.py
Maskable icons carry an opaque background and a smaller mark so a launcher can crop them to any shape."""
import base64, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'docs' / 'icons'
OUT.mkdir(parents=True, exist_ok=True)
mark = 'data:image/svg+xml;base64,' + base64.b64encode((ROOT / 'src' / 'mark.svg').read_bytes()).decode()
PAPER = '#f5f5f5'
ICONS = {
    'icon-192.png': (192, 1, None),
    'icon-512.png': (512, 1, None),
    'icon-maskable-192.png': (192, 0.56, PAPER),
    'icon-maskable-512.png': (512, 0.56, PAPER),
    'apple-touch-icon-180.png': (180, 0.78, PAPER),
}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    for name, (size, fill, bg) in ICONS.items():
        pg.set_viewport_size({'width': size, 'height': size})
        pg.set_content(f'<body style="margin:0;display:grid;place-items:center;block-size:100vh;background:{bg or "transparent"}"><img src="{mark}" style="inline-size:{fill*100}%;block-size:{fill*100}%"></body>')
        pg.screenshot(path=str(OUT / name), omit_background=bg is None)
        print(OUT / name)
    b.close()
