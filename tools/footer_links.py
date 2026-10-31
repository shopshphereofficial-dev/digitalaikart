#!/usr/bin/env python3
"""
Make the footer navigation consistent on every page.

Every page's footer should offer the same top-level links, including the Apps
section, so a visitor (or a crawler) landing on any page can reach /apps/ and
the legal pages in one tap.

Adds a missing "Apps" link after "Products" and a missing "About" link at the
end of <div class="footer-links">. Leaves everything else untouched.

Idempotent: a footer that already has the link is skipped.

Usage:  python3 tools/footer_links.py [repo_root]
"""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
LINKS_RE = re.compile(r'(<div class="footer-links">)(.*?)(</div>)', re.S)

APPS_LINK = '<a href="/apps/">Apps</a>'
ABOUT_LINK = '<a href="/about.html">About</a>'
PRODUCTS_LINK = '<a href="/products/">Products</a>'


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def fix_footer(foot):
    m = LINKS_RE.search(foot)
    if not m:
        return foot, False
    inner = m.group(2)
    changed = False
    if 'href="/apps/"' not in inner:
        if PRODUCTS_LINK in inner:
            inner = inner.replace(PRODUCTS_LINK, PRODUCTS_LINK + APPS_LINK, 1)
        else:
            inner = inner + APPS_LINK
        changed = True
    if 'href="/about.html"' not in inner:
        inner = inner + ABOUT_LINK
        changed = True
    if not changed:
        return foot, False
    return foot[:m.start()] + m.group(1) + inner + m.group(3) + foot[m.end():], True


def fix_ai_footer(path, text):
    """The /ai/ page uses its own footer without a footer-links block."""
    if os.path.relpath(path, ROOT) != os.path.join("ai", "index.html"):
        return text, False
    i = text.rfind("<footer")
    if i < 0:
        return text, False
    head, foot = text[:i], text[i:]
    if 'href="/apps/"' in foot:
        return text, False
    anchor = '<a href="/about.html">About &amp; Contact</a>'
    if anchor not in foot:
        return text, False
    foot = foot.replace(anchor, '<a href="/apps/">Apps</a> \u00b7 ' + anchor, 1)
    return head + foot, True


def main():
    touched, skipped = 0, 0
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in (".git", ".github", "node_modules")]
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            path = os.path.join(d, f)
            text = read(path)
            if not text:
                continue
            i = text.rfind("<footer")
            if i < 0:
                skipped += 1
                continue
            head, foot = text[:i], text[i:]
            new_foot, changed = fix_footer(foot)
            if not changed:
                new_foot, changed = fix_ai_footer(path, text)
                if changed:
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(new_foot)
                    touched += 1
                    continue
            if changed:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(head + new_foot)
                touched += 1
            else:
                skipped += 1
    print("footers updated: %d, already fine / no footer: %d" % (touched, skipped))


if __name__ == "__main__":
    main()
