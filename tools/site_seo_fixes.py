#!/usr/bin/env python3
"""Digitalaikart — one-off, idempotent SEO fixes across the static site.

Does five things and reports each one:

  1. loads /assets/analytics.js on every page (via assets/effects.js where that is
     already present, otherwise a direct one-line loader),
  2. makes the homepage H1 describe what the site sells,
  3. adds the small CSS rules the homepage H1 and product covers need,
  4. shortens every <title> longer than 65 characters,
  5. normalises "Rs. 149" / "Rs 149" to the rupee sign on product pages.

Safe to re-run: every step checks before it changes anything.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYTICS_LOADER = (
    "\n/* ---------- 8. GOOGLE ANALYTICS 4 (site-wide) ---------- */\n"
    "(function () {\n"
    "  if (window.__dakGAloader) return; window.__dakGAloader = true;\n"
    "  var s = document.createElement('script');\n"
    "  s.src = '/assets/analytics.js?v=1';\n"
    "  s.defer = true;\n"
    "  document.head.appendChild(s);\n"
    "})();\n"
)
DIRECT_LOADER = '<script defer src="/assets/analytics.js?v=1"></script>'

CSS_ADD = """
/* --- added: homepage H1 descriptor + product covers --- */
.hero-brand-sub{display:block;font-size:0.34em;font-weight:600;letter-spacing:0;margin-top:0.45rem;background:none;-webkit-text-fill-color:var(--text-secondary);color:var(--text-secondary)}
.product-cover{width:100%;height:auto;border-radius:16px;border:1px solid var(--border);display:block;aspect-ratio:16/9;object-fit:cover;box-shadow:0 18px 50px rgba(0,0,0,0.35)}
"""


def pages():
    """(dir, filename) for every real content page."""
    out = [('', f) for f in sorted(os.listdir(ROOT)) if f.endswith('.html')]
    for d in sorted(os.listdir(os.path.join(ROOT, 'products'))):
        if os.path.isfile(os.path.join(ROOT, 'products', d, 'index.html')):
            out.append(('products', os.path.join(d, 'index.html')))
    for f in sorted(os.listdir(os.path.join(ROOT, 'blog'))):
        if f.endswith('.html') and f != 'index.html':
            out.append(('blog', f))
    return out


def read(p):
    return open(p, encoding='utf-8').read()


def write(p, s):
    open(p, 'w', encoding='utf-8').write(s)


def step1_analytics():
    n_effects = n_direct = 0
    fx = os.path.join(ROOT, 'assets', 'effects.js')
    if os.path.isfile(fx):
        s = read(fx)
        if 'analytics.js' not in s:
            write(fx, s + ANALYTICS_LOADER)
            n_effects += 1
    for d, f in pages():
        p = os.path.join(ROOT, d, f)
        s = read(p)
        if 'analytics.js' in s or '/assets/effects.js' in s:
            continue
        if '</head>' in s:
            write(p, s.replace('</head>', DIRECT_LOADER + '\n</head>', 1))
            n_direct += 1
    print('1. analytics: effects.js loader added=%d, direct loader added=%d' % (n_effects, n_direct))


def step2_home_h1():
    p = os.path.join(ROOT, 'index.html')
    s = read(p)
    old = '<h1 class="hero-brand">Digitalaikart</h1>'
    new = ('<h1 class="hero-brand">Digitalaikart'
           '<span class="hero-brand-sub">AI digital products, guides &amp; tools for India</span></h1>')
    if old in s:
        write(p, s.replace(old, new, 1))
        print('2. homepage H1: updated')
    elif 'hero-brand-sub' in s:
        print('2. homepage H1: already updated')
    else:
        print('2. homepage H1: pattern not found — left unchanged')


def step3_css():
    p = os.path.join(ROOT, 'assets', 'style.css')
    s = read(p)
    if 'hero-brand-sub' in s:
        print('3. css: already present')
        return
    write(p, s + CSS_ADD)
    print('3. css: added')


def shorten(title):
    t = title.strip()
    if len(t) <= 65:
        return t
    for suf in (' | Digitalaikart', ' &mdash; Digitalaikart', ' — Digitalaikart',
                ' - Digitalaikart', 'Digitalaikart'):
        if t.endswith(suf):
            head = t[:-len(suf)].rstrip(' -—|&mdash;')
            if len(head) >= 25:
                t = head
            break
    if len(t) > 65:
        t = t[:62].rsplit(' ', 1)[0].rstrip(' -—|,&;')
    return t


def step4_titles():
    n = 0
    for d, f in pages():
        p = os.path.join(ROOT, d, f)
        s = read(p)
        m = re.search(r'<title>(.*?)</title>', s, re.S)
        if not m or len(m.group(1)) <= 65:
            continue
        new = shorten(m.group(1))
        if new and new != m.group(1):
            write(p, s[:m.start(1)] + new + s[m.end(1):])
            n += 1
            print('   %-52s -> %s' % (f[:52], new[:60]))
    print('4. titles: shortened %d' % n)


def step5_currency():
    n = 0
    pdir = os.path.join(ROOT, 'products')
    for d in sorted(os.listdir(pdir)):
        p = os.path.join(pdir, d, 'index.html')
        if not os.path.isfile(p):
            continue
        s = read(p)
        if '₹' in s:
            continue
        new = re.sub(r'\bRs\.?\s?(\d[\d,]*)', r'₹\1', s)
        if new != s:
            write(p, new)
            n += 1
            print('   currency applied:', d)
    print('5. currency: normalised on %d product pages' % n)


def main():
    step1_analytics()
    step2_home_h1()
    step3_css()
    step4_titles()
    step5_currency()
    print('done')


if __name__ == '__main__':
    main()
