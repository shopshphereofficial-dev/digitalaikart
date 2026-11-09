#!/usr/bin/env python3
"""Keep sitemap.xml limited to real, indexable HTML pages.

Adds missing public pages and removes pages whose HTML explicitly declares
noindex. This prevents checkout/thank-you pages from being re-added by CI.
"""
import os
import re
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, 'sitemap.xml')
BASE = 'https://digitalkartai.shop'
SKIP_DIRS = ('/.git', '/.github', '/admin', '/ads', '/node_modules')
SKIP_FILES = ('/404.html', '/thank-you.html')


def has_noindex(html):
    """Recognise robots meta tags regardless of attribute order."""
    for tag in re.findall(r'<meta\b[^>]*>', html, flags=re.I | re.S):
        name = re.search(r'\bname\s*=\s*["\']robots["\']', tag, flags=re.I)
        content = re.search(r'\bcontent\s*=\s*["\']([^"\']*)["\']', tag, flags=re.I)
        if name and content and re.search(r'\bnoindex\b', content.group(1), flags=re.I):
            return True
    return False


def page_paths():
    out = []
    for root, dirs, files in os.walk(ROOT):
        rel_root = root[len(ROOT):].replace(os.sep, '/')
        if any(rel_root == s or rel_root.startswith(s + '/') for s in SKIP_DIRS):
            dirs[:] = []
            continue
        for filename in files:
            if not filename.lower().endswith('.html'):
                continue
            full_path = os.path.join(root, filename)
            path = (rel_root + '/' + filename) if rel_root else ('/' + filename)
            if path.endswith('/index.html'):
                path = path[:-len('index.html')]
            if path in SKIP_FILES:
                continue
            try:
                with open(full_path, encoding='utf-8', errors='replace') as handle:
                    if has_noindex(handle.read()):
                        continue
            except OSError:
                continue
            out.append(path)
    return sorted(set(out))


def main():
    today = datetime.date.today().isoformat()
    with open(SITEMAP, encoding='utf-8') as handle:
        xml = handle.read()

    allowed = set(page_paths())
    removed = []

    def keep_indexable_url(match):
        block = match.group(0)
        loc = re.search(r'<loc>\s*' + re.escape(BASE) + r'([^<]*)</loc>', block)
        if loc and loc.group(1) not in allowed:
            removed.append(loc.group(1))
            return ''
        return block

    # Remove stale, missing and noindex URLs before adding the current page set.
    xml = re.sub(r'<url\b[^>]*>.*?</url>', keep_indexable_url, xml, flags=re.S)
    existing = set(re.findall(r'<loc>' + re.escape(BASE) + r'([^<]*)</loc>', xml))
    missing = [path for path in sorted(allowed) if path not in existing]

    add = []
    for path in missing:
        if path.startswith('/products/'):
            priority, changefreq = '0.9', '<changefreq>weekly</changefreq>'
        elif path.startswith('/blog/'):
            priority, changefreq = '0.8', ''
        elif path.startswith('/apps/'):
            priority, changefreq = '0.7', ''
        else:
            priority, changefreq = '0.6', ''
        add.append(
            '<url><loc>%s%s</loc><lastmod>%s</lastmod>%s<priority>%s</priority></url>'
            % (BASE, path, today, changefreq, priority)
        )

    if add:
        xml = xml.replace('</urlset>', '\n'.join(add) + '\n</urlset>')

    with open(SITEMAP, 'w', encoding='utf-8') as handle:
        handle.write(xml)

    print('removed %d non-indexable/stale page URLs; added %d indexable pages' % (len(removed), len(add)))
    if removed:
        for path in removed:
            print('  removed:', path)
    if not removed and not add:
        print('sitemap already complete and indexable')


if __name__ == '__main__':
    main()
