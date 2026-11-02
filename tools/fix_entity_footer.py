#!/usr/bin/env python3
"""Digitalaikart - restore the UTILITYNEST entity footer on blog posts.

Why this exists
---------------
`tools/blog_agent.py` used to emit a footer that named the parent company:

    Digitalaikart is a brand of UTILITYNEST - a registered MSME (Udyam,
    Govt. of India), Qazibagh, Ichgam, Budgam, Jammu & Kashmir 191111

At some point the template was shortened to a bare three-line footer. Every
post published after that - 11 of them, 31 Oct to 2 Nov 2026 - shipped without
the entity line, the contact details, and the Apps / About / Site Map links.

That matters for two reasons: Google Play organisation verification looks for
the legal entity on the site, and an inconsistent footer weakens the
entity association the Organization schema is trying to build.

What this script does (idempotent, safe to re-run)
--------------------------------------------------
1. Restores the full footer in any blog post that is missing the entity line.
2. Fixes the template in `tools/blog_agent.py` so future posts include it.
3. Adds `parentOrganization` (UTILITYNEST) to the Organization JSON-LD on
   index.html and about.html, if it is not already there.
4. Removes `netlify.toml` and `_headers` - leftovers from the abandoned
   Netlify setup. GitHub Pages ignores both, so they only mislead.

It touches nothing else. It never rewrites page content, titles or URLs.
"""

import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FULL_FOOTER = (
    '<footer><div class="footer-links"><a href="/">Home</a><a href="/products/">Products</a>'
    '<a href="/apps/">Apps</a><a href="/blog/">Blog</a><a href="/privacy-policy.html">Privacy Policy</a>'
    '<a href="/refund-policy.html">Refund Policy</a><a href="/terms.html">Terms &amp; Conditions</a>'
    '<a href="/sitemap.html">Site Map</a><a href="/about.html">About</a></div>'
    '<p><strong>Digitalaikart</strong> \u2014 Premium AI Digital Products</p>'
    '<p>Feedback &amp; Inquiries: <a href="mailto:lonefaisal977@gmail.com">lonefaisal977@gmail.com</a> | '
    'WhatsApp: <a href="https://wa.me/919682600301">+91 96826 00301</a>, '
    '<a href="https://wa.me/918492020923">+91 84920 20923</a></p>'
    '<p class="entity"><strong>Digitalaikart</strong> is a brand of <strong>UTILITYNEST</strong> \u2014 '
    'a registered MSME (Udyam, Govt. of India), Qazibagh, Ichgam, Budgam, Jammu &amp; Kashmir 191111 \u00b7 '
    '<a href="/about.html">About &amp; Contact</a></p>'
    '<p style="margin-top:0.5rem;color:#64748b">&copy; {year} Digitalaikart, a brand of UTILITYNEST. '
    'All rights reserved.</p></footer>'
)

FOOTER_RE = re.compile(r'<footer><div class="footer-links">.*?</footer>', re.S)

PARENT_ORG = (
    '    "parentOrganization": {\n'
    '      "@type": "Organization",\n'
    '      "name": "UTILITYNEST",\n'
    '      "description": "UTILITYNEST is a registered micro enterprise (MSME / Udyam, Government of '
    'India) and the parent entity of the Digitalaikart brand.",\n'
    '      "address": {\n'
    '        "@type": "PostalAddress",\n'
    '        "streetAddress": "Qazibagh, Ichgam",\n'
    '        "addressLocality": "Budgam",\n'
    '        "addressRegion": "Jammu & Kashmir",\n'
    '        "postalCode": "191111",\n'
    '        "addressCountry": "IN"\n'
    '      },\n'
    '      "telephone": "+91-96826-00301",\n'
    '      "email": "lonefaisal977@gmail.com"\n'
    '    },\n'
)

ORG_ANCHOR = re.compile(
    r'("@type":\s*"Organization",\s*\n\s*"@id":\s*"https://digitalkartai\.shop/#organization",\s*\n'
    r'\s*"name":\s*"Digitalaikart",\s*\n)'
)


def fix_posts():
    fixed = []
    for path in sorted(glob.glob(os.path.join(ROOT, 'blog', '*.html'))):
        text = open(path, encoding='utf-8').read()
        if 'utilitynest' in text.lower():
            continue
        m = FOOTER_RE.search(text)
        if not m:
            print('  skip (no footer):', os.path.relpath(path, ROOT))
            continue
        year = re.search(r'(\d{4})-\d{2}-\d{2}', os.path.basename(path))
        footer = FULL_FOOTER.replace('{year}', year.group(1) if year else '2026')
        open(path, 'w', encoding='utf-8').write(text[:m.start()] + footer + text[m.end():])
        fixed.append(os.path.relpath(path, ROOT))
    return fixed


def fix_template():
    path = os.path.join(ROOT, 'tools', 'blog_agent.py')
    if not os.path.isfile(path):
        return False
    text = open(path, encoding='utf-8').read()
    if 'utilitynest' in text.lower():
        return False
    m = FOOTER_RE.search(text)
    if not m:
        return False
    open(path, 'w', encoding='utf-8').write(
        text[:m.start()] + FULL_FOOTER.replace('{year}', '%(year)d') + text[m.end():]
    )
    return True


def fix_schema():
    changed = []
    for name in ('index.html', 'about.html'):
        path = os.path.join(ROOT, name)
        if not os.path.isfile(path):
            continue
        text = open(path, encoding='utf-8').read()
        if 'parentOrganization' in text:
            continue
        m = ORG_ANCHOR.search(text)
        if not m:
            print('  skip (no Organization block):', name)
            continue
        new = text[:m.end()] + PARENT_ORG + text[m.end():]
        for block in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
            json.loads(block.group(1))  # fail loudly rather than ship broken JSON-LD
        open(path, 'w', encoding='utf-8').write(new)
        changed.append(name)
    return changed


def drop_dead_netlify():
    dropped = []
    for name in ('netlify.toml', '_headers'):
        path = os.path.join(ROOT, name)
        if os.path.isfile(path):
            os.remove(path)
            dropped.append(name)
    return dropped


def main():
    print('blog posts fixed   :', len(fix_posts()))
    print('generator template :', 'updated' if fix_template() else 'already correct')
    print('schema updated     :', ', '.join(fix_schema()) or 'already correct')
    print('dead netlify files :', ', '.join(drop_dead_netlify()) or 'none')


if __name__ == '__main__':
    main()
