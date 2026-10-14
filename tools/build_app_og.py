#!/usr/bin/env python3
"""Render a 1200x630 share/preview image per app from its real logo + metadata.

Runs in CI (GitHub Actions runner has Google Chrome). Falls back through a few
headless-browser binaries; if none is found it exits non-zero so the failure is
visible rather than silently shipping broken images.

Usage: python3 tools/build_app_og.py [repo_root]
"""
import json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = os.path.join(ROOT, "assets", "apps", "og")

BRAND = {
    'neon-calculator': ('#B537F2', '#7A1FB0'),
    'neon-piano':      ('#12071F', '#3B1060'),
    'car-simulator':   ('#0B1020', '#123A63'),
    'grabit':          ('#0B0620', '#2A0B4A'),
    'soulstream':      ('#0B0620', '#3A0B52'),
    'pulsechat':       ('#070B16', '#122B5A'),
    'twinspace':       ('#4F46E5', '#1E1B6B'),
    'voltaura':        ('#0B1020', '#2B0B4A'),
}

HTML = """<!doctype html><html><head><meta charset=utf-8><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;font-family:'DejaVu Sans',Arial,sans-serif;
  background:radial-gradient(1100px 700px at 82% 8%, {c2} 0%, {c1} 62%);color:#fff;
  display:flex;flex-direction:column;justify-content:center;padding:74px 84px;position:relative}}
body::after{{content:'';position:absolute;inset:0;
  background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);
  background-size:60px 60px;-webkit-mask-image:linear-gradient(120deg,#000 20%,transparent 75%)}}
.row{{display:flex;align-items:center;gap:44px;position:relative;z-index:2}}
.tile{{width:190px;height:190px;border-radius:44px;overflow:hidden;flex:none;
  box-shadow:0 26px 60px rgba(0,0,0,.5);border:1px solid rgba(255,255,255,.14)}}
.tile svg{{width:190px;height:190px;display:block}}
.eyebrow{{font-size:20px;letter-spacing:.24em;text-transform:uppercase;color:#9FE8FF;font-weight:700;margin-bottom:14px}}
h1{{font-size:74px;line-height:1.02;font-weight:800;letter-spacing:-.5px}}
.tag{{font-size:27px;color:rgba(255,255,255,.82);margin-top:18px;max-width:760px;line-height:1.35}}
.chips{{display:flex;gap:12px;margin-top:30px;flex-wrap:wrap;position:relative;z-index:2}}
.chip{{font-size:20px;padding:11px 20px;border-radius:999px;background:rgba(255,255,255,.12);
  border:1px solid rgba(255,255,255,.22);color:#fff}}
.foot{{position:absolute;left:84px;bottom:46px;display:flex;align-items:center;gap:14px;z-index:2}}
.dot{{width:11px;height:11px;border-radius:50%;background:#37E6A0}}
.foot span{{font-size:21px;color:rgba(255,255,255,.9);font-weight:600}}
</style></head><body>
<div class="row">
  <div class="tile">{logo}</div>
  <div>
    <div class="eyebrow">{cat} &middot; Android</div>
    <h1>{name}</h1>
    <div class="tag">{tagline}</div>
  </div>
</div>
<div class="chips">{chips}</div>
<div class="foot"><span class="dot"></span><span>digitalkartai.shop/apps &nbsp;&middot;&nbsp; Free download</span></div>
</body></html>"""


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def optimize(path):
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(path).convert('RGB')
    im.quantize(colors=192, method=Image.MEDIANCUT, dither=Image.NONE).save(path, optimize=True)


def find_browser():
    for c in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chromium-headless-shell'):
        if shutil.which(c):
            return c
    return None


def main():
    browser = find_browser()
    if not browser:
        sys.exit('No headless browser found (looked for google-chrome / chromium).')
    apps = json.load(open(os.path.join(ROOT, 'apps.json'), encoding='utf-8'))['apps']
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp()
    for a in apps:
        slug = a['slug']
        c1, c2 = BRAND.get(slug, ('#0B1020', '#123A63'))
        icon = a.get('icon') or ''
        logo = open(os.path.join(ROOT, icon.lstrip('/')), encoding='utf-8').read()
        chips = ''.join('<div class="chip">%s</div>' % esc(f) for f in (a.get('features') or [])[:3])
        html = HTML.format(c1=c1, c2=c2, logo=logo, cat=esc(a.get('category', 'App')),
                           name=esc(a['name']), tagline=esc(a.get('tagline', '')), chips=chips)
        page = os.path.join(tmp, slug + '.html')
        open(page, 'w', encoding='utf-8').write(html)
        out = os.path.join(OUT, slug + '.png')
        subprocess.run([browser, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                        '--force-device-scale-factor=1', '--window-size=1200,630',
                        '--screenshot=' + out, 'file://' + page],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
        optimize(out)
        print('rendered', slug, os.path.getsize(out), 'bytes')


if __name__ == '__main__':
    main()
