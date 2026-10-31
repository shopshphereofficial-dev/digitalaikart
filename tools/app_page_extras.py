#!/usr/bin/env python3
"""
Post-process the generated /apps/ pages.

tools/build_apps.py rebuilds the app pages from apps.json on every change, and
its template is deliberately plain. This script adds the things Google Play
review and visitors need, and is safe to run after every rebuild:

  * a "Permissions & data" section — what the app can access and why, plus
    links to the app privacy policy and the data-deletion page
  * an "App details" table — version, size, required Android version, package
    name, release date, price and publisher
  * the legal-entity footer line (UTILITYNEST), both support numbers, and the
    Apps/About links

Idempotent: pages that already carry these blocks are left alone.

Usage:  python3 tools/app_page_extras.py [repo_root]
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

ENTITY_P = (
    '<p class="entity"><strong>Digitalaikart</strong> is a brand of '
    '<strong>UTILITYNEST</strong> \u2014 a registered MSME (Udyam, Govt. of India), '
    'Qazibagh, Ichgam, Budgam, Jammu &amp; Kashmir 191111 \u00b7 '
    '<a href="/about.html">About &amp; Contact</a></p>'
)
SECOND_NUMBER = ', <a href="https://wa.me/918492020923">+91 84920 20923</a>'
COPY_RE = re.compile(r"&copy;\s*(\d{4})\s*Digitalaikart\.\s*All rights reserved\.")
LINKS_RE = re.compile(r'(<div class="footer-links">)(.*?)(</div>)', re.S)

DEFAULTS = {
    "min_android": "Android 8.0 (API 26) or newer",
    "permissions": "No special permissions.",
    "privacy_url": "/app-privacy-policy.html",
    "deletion_url": "/account-deletion.html",
}


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def fix_footer(text):
    i = text.rfind("<footer")
    if i < 0:
        return text, False
    head, foot = text[:i], text[i:]
    if "UTILITYNEST" in foot:
        return text, False

    if "wa.me/919682600301" in foot and "84920" not in foot:
        foot = foot.replace('>+91 96826 00301</a>', '>+91 96826 00301</a>' + SECOND_NUMBER, 1)

    m = LINKS_RE.search(foot)
    if m:
        inner = m.group(2)
        if 'href="/apps/"' not in inner:
            inner += '<a href="/apps/">Apps</a>'
        if 'href="/about.html"' not in inner:
            inner += '<a href="/about.html">About</a>'
        foot = foot[:m.start()] + m.group(1) + inner + m.group(3) + foot[m.end():]

    foot = COPY_RE.sub(r"&copy; \1 Digitalaikart, a brand of UTILITYNEST. All rights reserved.", foot)
    c = re.search(r'<p[^>]*>&copy;', foot)
    if c:
        foot = foot[:c.start()] + ENTITY_P + foot[c.start():]
    else:
        j = foot.find("</footer>")
        foot = foot[:j] + ENTITY_P + foot[j:] if j >= 0 else foot + ENTITY_P
    return head + foot, True


def details_block(app):
    rows = [
        ("Version", str(app.get("version") or "")),
        ("Size", str(app.get("size") or "")),
        ("Requires", app.get("min_android") or DEFAULTS["min_android"]),
        ("Package", str(app.get("package") or "")),
        ("Last updated", str(app.get("updated") or "")),
        ("Price", "Free \u2014 no ads, no in-app purchases"),
        ("Publisher", "UTILITYNEST (Digitalaikart)"),
        ("Permissions", app.get("permissions") or DEFAULTS["permissions"]),
    ]
    tr = "".join(
        '<tr><th style="text-align:left;padding:.45rem .8rem .45rem 0;color:var(--text-primary);'
        'font-weight:600;white-space:nowrap">' + k + '</th>'
        '<td style="padding:.45rem 0">' + v + '</td></tr>'
        for k, v in rows if v
    )
    return (
        '<section class="section"><h2 class="section-title">App details</h2>'
        '<div class="gold-divider"></div>'
        '<div style="max-width:720px;margin:0 auto;color:var(--text-secondary);font-size:.85rem">'
        '<table style="width:100%;border-collapse:collapse">' + tr + '</table></div></section>'
    )


def permissions_block(app):
    priv = app.get("privacy_url") or DEFAULTS["privacy_url"]
    dele = app.get("deletion_url") or DEFAULTS["deletion_url"]
    perms = app.get("permissions") or DEFAULTS["permissions"]
    return (
        '<section class="section"><h2 class="section-title">Permissions &amp; data</h2>'
        '<div class="gold-divider"></div>'
        '<div style="max-width:720px;margin:0 auto;color:var(--text-secondary);font-size:.85rem">'
        '<p>This app does not create an account for you, does not include advertising or analytics '
        'SDKs, and does not send your personal data to our servers. Every permission is optional and '
        'can be revoked in Android Settings at any time.</p>'
        '<ul><li>' + perms + '</li></ul>'
        '<p><strong>Published by UTILITYNEST</strong> (registered MSME / Udyam, Govt. of India), the '
        'company behind Digitalaikart. <a href="' + priv + '">App privacy policy</a> \u00b7 '
        '<a href="' + dele + '">Delete your data</a> \u00b7 '
        '<a href="/about.html">About &amp; Contact</a></p></div></section>'
    )


def main():
    try:
        data = json.loads(read(os.path.join(ROOT, "apps.json")))
    except ValueError:
        data = {}
    apps = {a.get("slug"): a for a in data.get("apps", [])}

    touched = 0
    for slug, app in apps.items():
        path = os.path.join(ROOT, "apps", slug, "index.html")
        t = read(path)
        if not t:
            continue
        changed = False
        if "App details" not in t and "<footer" in t:
            i = t.rfind("<footer")
            t = t[:i] + details_block(app) + permissions_block(app) + t[i:]
            changed = True
        new, foot_changed = fix_footer(t)
        if foot_changed:
            t, changed = new, True
        if changed:
            write(path, t)
            touched += 1

    # the /apps/ listing page also needs the entity footer
    listing = os.path.join(ROOT, "apps", "index.html")
    t = read(listing)
    if t:
        new, changed = fix_footer(t)
        if changed:
            write(listing, new)
            touched += 1

    print("app pages updated: %d" % touched)


if __name__ == "__main__":
    main()
