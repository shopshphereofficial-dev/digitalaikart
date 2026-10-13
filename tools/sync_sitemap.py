#!/usr/bin/env python3
"""Keep sitemap.xml in sync with the pages actually on the site.

Adds any real page (blog post, product, app, policy, ...) that is missing from
sitemap.xml. Skips /admin, /ads and the noindex pages. Idempotent.
"""
import os
import re
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, 'sitemap.xml')
BASE = 'https://digitalkartai.shop'
SKIP_DIRS = ('/.git', '/.github', '/admin', '/ads', '/node_modules')
SKIP_FILES = ('/404.html', '/thank-you.html')


def page_paths():
    out = []
    for root, dirs, files in os.walk(ROOT):
        rel_root = root[len(ROOT):]
        if any(s in rel_root for s in SKIP_DIRS):
            continue
        for f in files:
            if not f.endswith('.html'):
                continue
            p = (rel_root + '/' + f) if rel_root else ('/' + f)
            if p.endswith('/index.html'):
                p = p[:-len('index.html')]
            if p in SKIP_FILES:
                continue
            out.append(p)
    return sorted(set(out))


def main():
    today = datetime.date.today().isoformat()
    xml = open(SITEMAP, encoding='utf-8').read()
    existing = set(re.findall(r'<loc>' + re.escape(BASE) + r'([^<]*)</loc>', xml))

    missing = [p for p in page_paths() if p not in existing]
    if not missing:
        print('sitemap already complete')
        return

    add = []
    for p in missing:
        if p.startswith('/products/'):
            pri, cf = '0.9', '<changefreq>weekly</changefreq>'
        elif p.startswith('/blog/'):
            pri, cf = '0.8', ''
        elif p.startswith('/apps/'):
            pri, cf = '0.7', ''
        else:
            pri, cf = '0.6', ''
        add.append('<url><loc>%s%s</loc><lastmod>%s</lastmod>%s<priority>%s</priority></url>'
                   % (BASE, p, today, cf, pri))

    xml = xml.replace('</urlset>', '\n'.join(add) + '\n</urlset>')
    open(SITEMAP, 'w', encoding='utf-8').write(xml)
    print('added %d urls:' % len(add))
    for p in missing:
        print('  ', p)


if __name__ == '__main__':
    main()
