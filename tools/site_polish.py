#!/usr/bin/env python3
"""Digitalaikart - site polish (idempotent).

Three independent fixes:

1. NAV: replaces the top-nav links on every content page with one canonical set
   - Home, Products, Apps, AI Assistant, Blog - and marks the current section
   active. Previously the /products/ section (81 pages) was missing the
   "AI Assistant" link entirely, so an option vanished as you navigated.

2. PRODUCT CARDS: adds each product's existing cover image
   (/assets/products/<slug>.jpg - the same one its detail page shows) to its
   card on /products/ and to the card templates used by the publish workflows.
   The listing previously showed only an "AI" placeholder.

3. HELP WIDGET: restyles assets/helpbot.js to the light theme and swaps its
   mark for a drawn robot help-desk head (no emoji). The API key and all logic
   are left byte-for-byte untouched.

Safe to re-run: every step checks before it changes anything.
"""
import argparse
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------- #
# 1. NAV
# --------------------------------------------------------------------------- #
NAV_ITEMS = [('/', 'Home'), ('/products/', 'Products'), ('/apps/', 'Apps'),
             ('/ai/', 'AI Assistant'), ('/blog/', 'Blog')]
NAV_RE = re.compile(r'<div class="nav-links">.*?</div>', re.S)


def nav_block(active):
    out = ['<div class="nav-links">']
    for href, label in NAV_ITEMS:
        cls = ' class="active"' if label == active else ''
        out.append('<a href="%s"%s>%s</a>' % (href, cls, label))
    out.append('</div>')
    return ''.join(out)


def active_for(rel):
    rel = rel.replace('\\', '/')
    if rel == 'index.html':
        return 'Home'
    return {'products': 'Products', 'apps': 'Apps',
            'ai': 'AI Assistant', 'blog': 'Blog'}.get(rel.split('/')[0])


def nav_pages():
    out = [f for f in sorted(os.listdir(ROOT)) if f.endswith('.html')]
    for sub in ('products', 'blog', 'ai', 'apps'):
        d = os.path.join(ROOT, sub)
        if not os.path.isdir(d):
            continue
        for base, _dirs, files in os.walk(d):
            for f in sorted(files):
                if f.endswith('.html'):
                    out.append(os.path.relpath(os.path.join(base, f), ROOT))
    return [p for p in out if p.split('/')[0] not in ('admin', 'ads')]


def step_nav(dry):
    n = 0
    for rel in nav_pages():
        p = os.path.join(ROOT, rel)
        s = open(p, encoding='utf-8').read()
        m = NAV_RE.search(s)
        if not m:
            continue
        want = nav_block(active_for(rel))
        if m.group(0) == want:
            continue
        if not dry:
            open(p, 'w', encoding='utf-8').write(s[:m.start()] + want + s[m.end():])
        n += 1
    print('nav: %s %d page(s)' % ('would update' if dry else 'updated', n))


# --------------------------------------------------------------------------- #
# 2. PRODUCT CARD IMAGES
# --------------------------------------------------------------------------- #
CARD_RE = re.compile(
    r'<div class="card-img"><span class="card-badge">(?P<badge>[^<]*)</span></div>'
    r'(?P<mid>.*?)<h3 class="card-title">(?P<title>.*?)</h3>'
    r'(?P<rest>.*?)<a href="/products/(?P<slug>[a-z0-9\-]+)/" class="btn btn-gold">',
    re.S)


def add_images(text):
    def repl(m):
        slug = m.group('slug')
        if not os.path.isfile(os.path.join(ROOT, 'assets', 'products', slug + '.jpg')):
            return m.group(0)
        alt = m.group('title').replace('"', '&quot;')   # already HTML-encoded text
        img = ('<a class="card-img-link" href="/products/%s/">'
               '<img src="/assets/products/%s.jpg" alt="%s" loading="lazy" '
               'width="1200" height="630"></a>'
               % (slug, slug, alt))
        return ('<div class="card-img">' + img
                + '<span class="card-badge">' + m.group('badge') + '</span></div>'
                + m.group('mid') + '<h3 class="card-title">' + m.group('title') + '</h3>'
                + m.group('rest') + '<a href="/products/%s/" class="btn btn-gold">' % slug)
    return CARD_RE.sub(repl, text)


def card_files():
    files = ['products/index.html']
    updir = os.path.join(ROOT, '.github', 'site-updates')
    if os.path.isdir(updir):
        for f in sorted(os.listdir(updir)):
            if f.endswith('.html'):
                files.append(os.path.join('.github', 'site-updates', f))
    return files


def step_cards(dry):
    n = 0
    for rel in card_files():
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        s = open(p, encoding='utf-8').read()
        s2 = add_images(s)
        if s2 != s:
            if not dry:
                open(p, 'w', encoding='utf-8').write(s2)
            n += 1
            print('cards: %s updated' % rel)
    print('cards: %s %d file(s)' % ('would update' if dry else 'updated', n))


# --------------------------------------------------------------------------- #
# 3. HELP WIDGET (assets/helpbot.js) - light theme + robot mark
# --------------------------------------------------------------------------- #
HELPBOT = os.path.join(ROOT, 'assets', 'helpbot.js')

NEW_ICON = """/* robot help-desk mark (drawn, not an emoji) */
  function icon(size) {
    return '<svg width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
      + '<path d="M12 3.6v2.3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
      + '<circle cx="12" cy="2.5" r="1.25" fill="currentColor"/>'
      + '<rect x="4.1" y="5.9" width="15.8" height="11.4" rx="3.3" stroke="currentColor" stroke-width="1.7"/>'
      + '<circle cx="9.1" cy="10.9" r="1.35" fill="currentColor"/>'
      + '<circle cx="14.9" cy="10.9" r="1.35" fill="currentColor"/>'
      + '<path d="M9.4 14.1h5.2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
      + '<path d="M4.1 11.3H2.3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
      + '<path d="M19.9 11.3h1.8" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
      + '</svg>';
  }
"""

NEW_CSS = """  var css = ''
    + '.hb-fab{position:fixed;right:22px;bottom:104px;z-index:900;width:50px;height:50px;border-radius:50%;border:none;color:#ffffff;background:linear-gradient(135deg,#1d4ed8,#1e40af);cursor:pointer;box-shadow:0 10px 24px rgba(29,78,216,.35);display:flex;align-items:center;justify-content:center;transition:transform .15s,box-shadow .15s}'
    + '.hb-fab:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(29,78,216,.45)}'
    + '.hb-panel{position:fixed;right:22px;bottom:164px;z-index:901;width:334px;max-width:calc(100vw - 44px);height:440px;max-height:62vh;background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;display:none;flex-direction:column;overflow:hidden;box-shadow:0 24px 60px rgba(15,23,42,.18)}'
    + '.hb-panel.on{display:flex}'
    + '.hb-hd{padding:.75rem 1rem;border-bottom:1px solid #e2e8f0;display:flex;align-items:center;gap:.6rem;background:#f8fafc}'
    + '.hb-hi{display:flex;align-items:center;flex:0 0 auto;color:#1d4ed8}'
    + '.hb-t{flex:1;min-width:0}'
    + '.hb-hd b{color:#0f172a;font-size:.85rem}'
    + '.hb-hd small{display:block;color:#64748b;font-size:.62rem;font-weight:400}'
    + '.hb-x{background:none;border:none;color:#94a3b8;cursor:pointer;font-size:1rem;flex:0 0 auto}'
    + '.hb-msgs{flex:1;overflow-y:auto;padding:.8rem;display:flex;flex-direction:column;gap:.55rem;background:#ffffff}'
    + '.hb-m{max-width:88%;padding:.55rem .75rem;border-radius:11px;font-size:.8rem;line-height:1.5;white-space:pre-wrap}'
    + '.hb-m.u{align-self:flex-end;background:linear-gradient(135deg,#1d4ed8,#1e40af);color:#ffffff;font-weight:500}'
    + '.hb-m.a{align-self:flex-start;background:#f1f5f9;border:1px solid #e2e8f0;color:#0f172a}'
    + '.hb-m.a a{color:#1d4ed8}'
    + '.hb-links{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.55rem}'
    + '.hb-btn{display:inline-flex;align-items:center;gap:.3rem;background:linear-gradient(135deg,#1d4ed8,#1e40af);color:#ffffff !important;font-weight:700;font-size:.72rem;line-height:1.1;padding:.4rem .65rem;border-radius:8px;text-decoration:none;white-space:nowrap}'
    + '.hb-btn:hover{filter:brightness(1.06)}'
    + '.hb-btn svg{width:12px;height:12px}'
    + '.hb-chips{display:flex;gap:.4rem;flex-wrap:wrap;padding:0 .8rem .5rem}'
    + '.hb-chips button{background:#ffffff;border:1px solid #cbd5e1;color:#1d4ed8;border-radius:99px;padding:.24rem .65rem;font-size:.66rem;cursor:pointer;font-family:inherit}'
    + '.hb-chips button:hover{background:#f1f5f9}'
    + '.hb-in{display:flex;gap:.45rem;padding:.65rem;border-top:1px solid #e2e8f0}'
    + '.hb-in input{flex:1;background:#ffffff;border:1px solid #cbd5e1;border-radius:9px;padding:.55rem .7rem;color:#0f172a;font-size:.8rem;outline:none;font-family:inherit}'
    + '.hb-in input:focus{border-color:#1d4ed8}'
    + '.hb-in button{background:linear-gradient(135deg,#1d4ed8,#1e40af);border:none;border-radius:9px;padding:0 .9rem;color:#ffffff;font-weight:800;cursor:pointer;font-size:.8rem;font-family:inherit}';
"""


def step_helpbot(dry):
    if not os.path.isfile(HELPBOT):
        print('helpbot: not found')
        return
    s = open(HELPBOT, encoding='utf-8').read()
    orig = s
    i = s.find('/* unique help-bot mark:')
    if i != -1:
        j = s.find('\n  }\n', i)
        if j != -1:
            s = s[:i] + NEW_ICON + s[j + len('\n  }\n'):]
    i = s.find("  var css = ''")
    if i != -1:
        j = s.find("';\n", i)
        if j != -1:
            s = s[:i] + NEW_CSS + s[j + 3:]
    s = s.replace('stroke="#0a1628"', 'stroke="currentColor"')
    if s != orig:
        if not dry:
            open(HELPBOT, 'w', encoding='utf-8').write(s)
        print('helpbot: %s' % ('would update' if dry else 'updated'))
    else:
        print('helpbot: already current')


# --------------------------------------------------------------------------- #
# 4. STYLESHEET (nav stays visible on small screens; product card covers)
# --------------------------------------------------------------------------- #
NAV_CSS_OLD = (
    '.nav-links{display:flex;gap:1.5rem;align-items:center}\n'
    '.nav-links a{font-size:0.85rem;color:var(--text-secondary);transition:color 0.2s;white-space:nowrap}\n'
    '.nav-links a:hover{color:var(--gold)}\n'
    '.nav-links a.active{color:var(--gold)}\n'
    '@media(max-width:600px){.nav-links{gap:0.8rem}.nav-links a{font-size:0.75rem}.nav-logo{font-size:1.1rem}}')
NAV_CSS_NEW = (
    '.nav-links{display:flex;gap:0.35rem;align-items:center;overflow-x:auto;scrollbar-width:none;'
    '-ms-overflow-style:none;-webkit-overflow-scrolling:touch;min-width:0}\n'
    '.nav-links::-webkit-scrollbar{display:none}\n'
    '.nav-links a{font-size:0.85rem;color:var(--text-secondary);transition:color 0.2s,background 0.2s;'
    'white-space:nowrap;padding:0.3rem 0.55rem;border-radius:8px}\n'
    '.nav-links a:hover{color:var(--gold);background:rgba(29,78,216,0.08)}\n'
    '.nav-links a.active{color:var(--gold);background:rgba(29,78,216,0.12);font-weight:700}\n'
    '.nav-logo{flex:0 0 auto}\n'
    '@media(max-width:640px){.nav{padding:0.7rem 0.9rem}.nav-links{gap:0.1rem}'
    '.nav-links a{font-size:0.76rem;padding:0.28rem 0.42rem}.nav-logo{font-size:1.02rem}}\n'
    '@media(max-width:430px){.nav-inner{flex-wrap:wrap;row-gap:0.3rem}'
    '.nav-links{width:100%;order:2}.nav-links a{font-size:0.74rem}}')
CARD_CSS_OLD = (
    '.card-img{height:170px;background:linear-gradient(135deg,var(--navy-card) 0%,#e2e8f0 100%);'
    'display:flex;align-items:center;justify-content:center;position:relative}\n'
    ".card-img::after{content:'AI';font-size:2.5rem;font-weight:900;color:rgba(245,197,66,0.12)}")
CARD_CSS_NEW = (
    '.card-img{height:170px;background:linear-gradient(135deg,var(--navy-card) 0%,#e2e8f0 100%);'
    'display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}\n'
    '.card-img img{width:100%;height:100%;object-fit:cover;display:block}\n'
    '.card-img a{display:block;width:100%;height:100%}')


def step_css(dry):
    p = os.path.join(ROOT, 'assets', 'style.css')
    s = open(p, encoding='utf-8').read()
    orig = s
    if NAV_CSS_OLD in s:
        s = s.replace(NAV_CSS_OLD, NAV_CSS_NEW, 1)
    if CARD_CSS_OLD in s:
        s = s.replace(CARD_CSS_OLD, CARD_CSS_NEW, 1)
    if s != orig:
        if not dry:
            open(p, 'w', encoding='utf-8').write(s)
        print('css: %s' % ('would update' if dry else 'updated'))
    else:
        print('css: already current')


# --------------------------------------------------------------------------- #
# 5. GENERATOR TEMPLATE (so newly generated blog posts keep the full nav)
# --------------------------------------------------------------------------- #
def step_template(dry):
    p = os.path.join(ROOT, 'tools', 'blog_agent.py')
    if not os.path.isfile(p):
        return
    s = open(p, encoding='utf-8').read()
    old = ('<div class="nav-links"><a href="/">Home</a><a href="/products/">Products</a>'
           '<a href="/ai/">AI Assistant</a><a href="/blog/" class="active">Blog</a></div>')
    new = ('<div class="nav-links"><a href="/">Home</a><a href="/products/">Products</a>'
           '<a href="/apps/">Apps</a><a href="/ai/">AI Assistant</a>'
           '<a href="/blog/" class="active">Blog</a></div>')
    if old in s:
        if not dry:
            open(p, 'w', encoding='utf-8').write(s.replace(old, new))
        print('template: blog_agent.py nav %s' % ('would update' if dry else 'updated'))
    else:
        print('template: blog_agent.py nav already ok')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    step_nav(args.dry_run)
    step_cards(args.dry_run)
    step_helpbot(args.dry_run)
    step_css(args.dry_run)
    step_template(args.dry_run)
    print('done')


if __name__ == '__main__':
    main()
