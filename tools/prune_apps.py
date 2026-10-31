#!/usr/bin/env python3
"""
Keep only the Neon Calculator app on the website.

Everything else is withdrawn until it is ready for review: the other seven app
pages, their icons, their social images, their catalogue entries, their cards on
the homepage and the apps index, and their rows in the sitemap. The app privacy
policy is reduced to the one app that remains.

The Neon Calculator page gets its own details block (version, size, package,
Android version, release date, permissions, policy links), read from the facts
below.

Idempotent: running it again changes nothing.

Usage:  python3 tools/prune_apps.py [repo_root]
"""
import json
import os
import re
import shutil
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

KEEP = "neon-calculator"
REMOVE = ["car-simulator", "grabit", "neon-piano", "pulsechat", "soulstream", "twinspace", "voltaura"]

# verified facts: neon-calculator/app/build.gradle + GitHub release "latest"
KEEP_FACTS = {
    "slug": KEEP,
    "name": "Neon Calculator",
    "tagline": "A colourful, kid-friendly calculator with glowing neon buttons.",
    "category": "Tools",
    "price": "Free",
    "platform": "Android",
    "version": "1.3",
    "version_code": 4,
    "size": "7.2 MB",
    "min_android": "Android 8.0 (API 26) or newer",
    "package": "com.neon.calc",
    "updated": "10 October 2026",
    "icon": "/apps/icons/neon-calculator.svg",
    "apk": "https://github.com/shopshphereofficial-dev/neon-calculator/releases/latest/download/app.apk",
    "repo": "https://github.com/shopshphereofficial-dev/neon-calculator",
    "permissions": "Internet and network state only. The app works fully offline.",
    "privacy_url": "/app-privacy-policy.html",
    "deletion_url": "/account-deletion.html",
    "page": "/apps/neon-calculator/",
}

FOOTER = (
    '<footer><div class="footer-links"><a href="/">Home</a><a href="/products/">Products</a>'
    '<a href="/apps/">Apps</a><a href="/blog/">Blog</a><a href="/privacy-policy.html">Privacy Policy</a>'
    '<a href="/refund-policy.html">Refund Policy</a><a href="/terms.html">Terms &amp; Conditions</a>'
    '<a href="/sitemap.html">Site Map</a><a href="/about.html">About</a></div>'
    '<p><strong>Digitalaikart</strong> &mdash; Premium AI Digital Products</p>'
    '<p>Feedback &amp; Inquiries: <a href="mailto:lonefaisal977@gmail.com">lonefaisal977@gmail.com</a> '
    '| WhatsApp: <a href="https://wa.me/919682600301">+91 96826 00301</a>, '
    '<a href="https://wa.me/918492020923">+91 84920 20923</a></p>'
    '<p class="entity"><strong>Digitalaikart</strong> is a brand of <strong>UTILITYNEST</strong> '
    '\u2014 a registered MSME (Udyam, Govt. of India), Qazibagh, Ichgam, Budgam, '
    'Jammu &amp; Kashmir 191111 \u00b7 <a href="/about.html">About &amp; Contact</a></p>'
    '<p style="margin-top:0.5rem;color:#64748b">&copy; 2026 Digitalaikart, a brand of UTILITYNEST. '
    'All rights reserved.</p></footer>'
)

NAV = (
    '<nav class="nav"><div class="nav-inner"><a href="/" class="nav-logo">Digitalaikart</a>'
    '<div class="nav-links"><a href="/">Home</a><a href="/products/">Products</a>'
    '<a href="/apps/" class="active">Apps</a><a href="/ai/">Astral AI</a><a href="/blog/">Blog</a>'
    '<a href="/about.html">About</a></div></div></nav>'
)

PRIVACY_BLOCK = (
    '<h2 class="section-title">Apps, data and privacy</h2><div class="gold-divider"></div>'
    '<p>This app is published by <strong>UTILITYNEST</strong> (registered MSME / Udyam, Govt. of '
    'India), the company behind Digitalaikart. It needs no account, shows no advertising, and '
    'does not send your personal data to our servers.</p>'
    '<p><a href="/app-privacy-policy.html">App privacy policy</a> \u00b7 '
    '<a href="/account-deletion.html">Delete your data</a> \u00b7 '
    '<a href="/about.html">About &amp; Contact</a></p>'
)


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def card(f):
    return (
        '<div class="app-card-wrap" data-name="' + f["name"] + '" data-cat="' + f["category"] + '">'
        '<div class="app-card"><div class="app-card-top">'
        '<div class="app-icon"><img src="' + f["icon"] + '" alt="' + f["name"] + ' icon"></div>'
        '<div><div class="app-name">' + f["name"] + '</div>'
        '<div class="app-cat">' + f["category"] + '</div></div></div>'
        '<div class="app-card-body"><p class="app-desc">' + f["tagline"] + '</p>'
        '<div class="app-tags"><span class="app-tag">v' + f["version"] + '</span>'
        '<span class="app-tag">' + f["size"] + '</span>'
        '<span class="app-tag">offline</span><span class="app-tag">ad-free</span></div>'
        '<div class="app-foot"><span class="app-price free">Free</span>'
        '<span style="font-size:.7rem;color:var(--text-muted)">' + f["platform"] + '</span></div>'
        '<a href="' + f["page"] + '" class="btn btn-gold">View app &rarr;</a></div></div></div>'
    )


def build_apps_index(f):
    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<link rel="icon" href="/favicon.ico" sizes="48x48">'
        '<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">'
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">'
        '<title>Apps for Android \u2014 Digitalaikart</title>'
        '<meta name="description" content="Android apps built by UTILITYNEST under the Digitalaikart '
        'brand \u2014 starting with Neon Calculator, a free offline calculator. Permissions, privacy '
        'policy and download details.">'
        '<meta property="og:title" content="Apps for Android \u2014 Digitalaikart">'
        '<meta property="og:description" content="Android apps built by UTILITYNEST under the '
        'Digitalaikart brand \u2014 starting with Neon Calculator.">'
        '<meta property="og:type" content="website">'
        '<meta property="og:url" content="https://digitalkartai.shop/apps/">'
        '<meta property="og:site_name" content="Digitalaikart">'
        '<meta property="og:locale" content="en_IN">'
        '<meta property="og:image" content="https://digitalkartai.shop/assets/og-default.png">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="Apps for Android \u2014 Digitalaikart">'
        '<meta name="twitter:description" content="Android apps built by UTILITYNEST under the '
        'Digitalaikart brand.">'
        '<meta name="twitter:image" content="https://digitalkartai.shop/assets/og-default.png">'
        '<link rel="canonical" href="https://digitalkartai.shop/apps/">'
        '<link rel="stylesheet" href="/assets/style.css">'
        '<link rel="stylesheet" href="/assets/apps.css"></head><body>'
    )
    body = (
        NAV
        + '<header class="page-header"><h1>Apps</h1>'
        '<p>Our own Android app, built and published by UTILITYNEST under the Digitalaikart brand.</p>'
        '</header><div class="app-grid" style="max-width:1000px;margin:0 auto;padding:0 1.5rem 2rem">'
        + card(f)
        + '</div><section class="section"><div style="max-width:720px;margin:0 auto;'
        'color:var(--text-secondary);font-size:.85rem">'
        + PRIVACY_BLOCK
        + '</div></section>'
        + FOOTER
        + '<script src="/assets/effects.js"></script></body></html>\n'
    )
    return head + body


def homepage_apps_section(f):
    return (
        '<section class="section" id="apps">\n'
        '  <h2 class="section-title">Our Apps</h2>\n'
        '  <div class="gold-divider"></div>\n'
        '  <p class="section-sub">Our own Android app \u2014 built and published by UTILITYNEST '
        'under the Digitalaikart brand.</p>\n'
        '  <div class="app-grid">' + card(f) + '</div>\n'
        '</section>'
    )


def details_section(f):
    rows = [
        ("Version", f["version"] + " (build " + str(f["version_code"]) + ")"),
        ("Size", f["size"]),
        ("Requires", f["min_android"]),
        ("Package", f["package"]),
        ("Last updated", f["updated"]),
        ("Price", "Free \u2014 no ads, no in-app purchases"),
        ("Publisher", "UTILITYNEST (Digitalaikart)"),
        ("Permissions", f["permissions"]),
    ]
    tr = "".join(
        '<tr><th style="text-align:left;padding:.45rem .8rem .45rem 0;color:var(--text-primary);'
        'font-weight:600;white-space:nowrap">' + k + '</th>'
        '<td style="padding:.45rem 0">' + v + '</td></tr>'
        for k, v in rows
    )
    return (
        '<section class="section"><h2 class="section-title">App details</h2>'
        '<div class="gold-divider"></div>'
        '<div style="max-width:720px;margin:0 auto;color:var(--text-secondary);font-size:.85rem">'
        '<table style="width:100%;border-collapse:collapse">' + tr + '</table>'
        '<p style="margin-top:1rem"><strong>Published by UTILITYNEST</strong> (registered MSME / '
        'Udyam, Govt. of India). <a href="' + f["privacy_url"] + '">App privacy policy</a> \u00b7 '
        '<a href="' + f["deletion_url"] + '">Delete your data</a> \u00b7 '
        '<a href="/about.html">About &amp; Contact</a></p></div></section>'
    )


def prune_files():
    removed = []
    for slug in REMOVE:
        d = os.path.join(ROOT, "apps", slug)
        if os.path.isdir(d):
            shutil.rmtree(d)
            removed.append("apps/%s/" % slug)
        for p in (os.path.join(ROOT, "apps", "icons", slug + ".svg"),
                  os.path.join(ROOT, "assets", "apps", "og", slug + ".png")):
            if os.path.isfile(p):
                os.remove(p)
                removed.append(os.path.relpath(p, ROOT))
    return removed


def prune_catalogue():
    path = os.path.join(ROOT, "apps.json")
    try:
        data = json.loads(read(path))
    except ValueError:
        return False
    apps = [a for a in data.get("apps", []) if a.get("slug") == KEEP]
    if apps:
        apps[0].update(KEEP_FACTS)
        apps[0]["downloads"] = [{"label": "Download APK", "url": KEEP_FACTS["apk"]},
                                {"label": "Source on GitHub", "url": KEEP_FACTS["repo"]}]
    new = {"updated": data.get("updated", ""),
           "note": "Only apps that are ready for release are listed here.",
           "apps": apps}
    write(path, json.dumps(new, indent=1, ensure_ascii=False) + "\n")
    return True


def rewrite_apps_index():
    write(os.path.join(ROOT, "apps", "index.html"), build_apps_index(KEEP_FACTS))


def rewrite_homepage():
    path = os.path.join(ROOT, "index.html")
    t = read(path)
    if not t:
        return False
    m = re.search(r'<section class="section" id="apps">.*?</section>', t, re.S)
    if not m:
        return False
    new = homepage_apps_section(KEEP_FACTS)
    if m.group(0).strip() == new.strip():
        return False
    write(path, t[:m.start()] + new + t[m.end():])
    return True


def rewrite_app_page():
    path = os.path.join(ROOT, "apps", KEEP, "index.html")
    t = read(path)
    if not t:
        return False
    changed = False
    # drop the "More apps" section entirely
    m = re.search(r'<section class="section"><h2 class="section-title">More apps</h2>.*?</section>', t, re.S)
    if m:
        t = t[:m.start()] + t[m.end():]
        changed = True
    # add the details block once
    if "App details" not in t:
        anchor = "<footer"
        i = t.find(anchor)
        if i > 0:
            t = t[:i] + details_section(KEEP_FACTS) + t[i:]
            changed = True
    if changed:
        write(path, t)
    return changed


def prune_sitemap():
    path = os.path.join(ROOT, "sitemap.xml")
    t = read(path)
    if not t:
        return False
    before = t
    for slug in REMOVE:
        t = re.sub(r"\s*<url>(?:(?!</url>).)*?/apps/" + re.escape(slug) + r"/(?:(?!</url>).)*?</url>",
                   "", t, flags=re.S)
    if t != before:
        write(path, t)
        return True
    return False


def prune_app_privacy():
    path = os.path.join(ROOT, "app-privacy-policy.html")
    t = read(path)
    if not t:
        return False
    changed = False

    # permissions list: keep only the calculator block, drop the withdrawn apps
    calc = re.search(r'<h3>Neon Calculator</h3>.*?(?=<h3>|<h2>)', t, re.S)
    end_h2 = t.find("<h2>Data we collect</h2>")
    if calc and end_h2 > calc.end() and "<h3>" in t[calc.end():end_h2]:
        t = t[:calc.start()] + calc.group(0).rstrip() + "\n\n  " + t[end_h2:]
        changed = True

    # the policy is about one app now, so speak about it in the singular
    singular = (
        '<p>Neon Calculator is a general-audience app, made with children in mind. It does not\n'
        '  collect personal information, does not show advertising and has no in-app purchases,\n'
        '  so it is safe for children to use. If you believe a child has sent us personal\n'
        '  information by email or WhatsApp, contact us and we will delete it.</p>'
    )
    m = re.search(r"<p>Our apps are general-audience apps.*?</p>", t, re.S)
    if m:
        t = t[:m.start()] + singular + t[m.end():]
        changed = True

    if changed:
        write(path, t)
    return changed


def main():
    removed = prune_files()
    prune_catalogue()
    rewrite_apps_index()
    home = rewrite_homepage()
    page = rewrite_app_page()
    sm = prune_sitemap()
    pol = prune_app_privacy()
    print("deleted: %d file(s)/folder(s)" % len(removed))
    for r in removed:
        print("   -", r)
    print("homepage apps section rewritten:", home)
    print("neon page updated:", page)
    print("sitemap pruned:", sm)
    print("app privacy policy pruned:", pol)


if __name__ == "__main__":
    main()
