#!/usr/bin/env python3
"""Digitalaikart — add the Tally newsletter signup to the site.

Inserts a signup section before the footer on the homepage, every product page and
every blog post, appends the CSS it needs, and adds a small fallback to
assets/effects.js so any future page (e.g. a freshly generated blog post) also
gets the form without touching the blog template.

Idempotent: pages that already contain id="newsletter" are skipped.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORM_ID = 'rjNXyX'

SECTION = '''
<section class="newsletter" id="newsletter">
  <div class="newsletter-inner">
    <h2>Get new AI guides &amp; tips first</h2>
    <p>One short email whenever we publish something genuinely useful &mdash; new AI guides, tools and India-specific playbooks. No spam, unsubscribe anytime.</p>
    <iframe data-tally-src="https://tally.so/embed/{fid}?alignLeft=1&amp;hideTitle=1&amp;transparentBackground=1&amp;dynamicHeight=1"
            loading="lazy" width="100%" height="230" frameborder="0" marginheight="0" marginwidth="0"
            title="Digitalaikart newsletter signup"></iframe>
  </div>
</section>
<script async src="https://tally.so/widgets/embed.js"></script>
'''.replace('{fid}', FORM_ID)

CSS = '''
/* --- added: newsletter signup --- */
.newsletter{padding:3.5rem 1.5rem}
.newsletter-inner{max-width:640px;margin:0 auto;border:1px solid var(--border,rgba(255,255,255,0.12));border-radius:18px;padding:2rem 1.5rem;text-align:center;background:rgba(255,255,255,0.03)}
.newsletter-inner h2{font-size:1.4rem;font-weight:800;color:#f1f5f9;margin-bottom:0.6rem}
.newsletter-inner p{color:var(--text-secondary,#94a3b8);font-size:0.9rem;margin-bottom:1.2rem;max-width:520px;margin-left:auto;margin-right:auto}
'''

FALLBACK = '''
/* ---------- 9. NEWSLETTER SIGNUP (fallback for pages without it) ---------- */
(function () {
  function build() {
    if (document.getElementById('newsletter')) return;
    var footer = document.querySelector('footer');
    if (!footer || !footer.parentNode) return;
    var s = document.createElement('section');
    s.className = 'newsletter';
    s.id = 'newsletter';
    s.innerHTML = '<div class="newsletter-inner">' +
      '<h2>Get new AI guides &amp; tips first</h2>' +
      '<p>One short email whenever we publish something genuinely useful &mdash; new AI guides, tools and India-specific playbooks. No spam, unsubscribe anytime.</p>' +
      '<iframe data-tally-src="https://tally.so/embed/{fid}?alignLeft=1&amp;hideTitle=1&amp;transparentBackground=1&amp;dynamicHeight=1" loading="lazy" width="100%" height="230" frameborder="0" marginheight="0" marginwidth="0" title="Digitalaikart newsletter signup"></iframe>' +
      '</div>';
    footer.parentNode.insertBefore(s, footer);
    if (!document.querySelector('script[src*="tally.so/widgets"]')) {
      var t = document.createElement('script');
      t.async = true;
      t.src = 'https://tally.so/widgets/embed.js';
      document.head.appendChild(t);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
  else build();
})();
'''.replace('{fid}', FORM_ID)


def pages():
    out = [('', f) for f in sorted(os.listdir(ROOT)) if f.endswith('.html')
           and f not in ('404.html', 'thank-you.html')]
    for d in sorted(os.listdir(os.path.join(ROOT, 'products'))):
        if os.path.isfile(os.path.join(ROOT, 'products', d, 'index.html')):
            out.append(('products', os.path.join(d, 'index.html')))
    for f in sorted(os.listdir(os.path.join(ROOT, 'blog'))):
        if f.endswith('.html') and f != 'index.html':
            out.append(('blog', f))
    return out


def insert_section():
    n = 0
    for d, f in pages():
        p = os.path.join(ROOT, d, f)
        s = open(p, encoding='utf-8').read()
        if 'id="newsletter"' in s:
            continue
        if '<footer' not in s:
            continue
        i = s.index('<footer')
        s = s[:i] + SECTION + s[i:]
        open(p, 'w', encoding='utf-8').write(s)
        n += 1
    print('pages given the signup section:', n)


def add_css():
    p = os.path.join(ROOT, 'assets', 'style.css')
    s = open(p, encoding='utf-8').read()
    if '.newsletter-inner' in s:
        print('css: already present')
        return
    open(p, 'w', encoding='utf-8').write(s + CSS)
    print('css: added')


def add_fallback():
    p = os.path.join(ROOT, 'assets', 'effects.js')
    s = open(p, encoding='utf-8').read()
    if 'NEWSLETTER SIGNUP' in s:
        print('effects.js fallback: already present')
        return
    open(p, 'w', encoding='utf-8').write(s + FALLBACK)
    print('effects.js fallback: added')


def main():
    insert_section()
    add_css()
    add_fallback()
    print('done')


if __name__ == '__main__':
    main()
