#!/usr/bin/env python3
"""
Small SEO and rendering touch-ups that need no judgement call.

1. The three policy pages had stub meta descriptions ("Privacy Policy for
   Digitalaikart") — replaced with real ones.
2. Blog and product descriptions longer than ~165 characters are cut at a word
   boundary to ~155, so Google shows the whole snippet instead of truncating it.
3. The listing pages carry 137–281 cards each; `.card` and `.blog-card` get
   content-visibility:auto so the browser skips rendering the off-screen ones
   (a straight render-cost win on a 240 KB page).
4. The admin setup screen gains a one-line warning about using a short-lived,
   single-repo GitHub token.

Idempotent: each step checks before it writes.

Usage:  python3 tools/seo_touchups.py [repo_root]
"""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

DESCRIPTIONS = {
    "privacy-policy.html": ("How UTILITYNEST (Digitalaikart) handles your data: what Razorpay "
                            "processes, what Google Analytics sees, cookies, retention and deletion."),
    "refund-policy.html": ("Digitalaikart refunds: instant-download guides are non-refundable once "
                           "downloaded, with replacements for duplicate charges or corrupted files."),
    "terms.html": ("Terms & Conditions for buying from Digitalaikart (UTILITYNEST): licence, "
                   "permitted use, INR pricing, delivery and liability."),
}

CSS_ADDITION = """
/* Listing performance: skip rendering cards that are far off-screen. */
.card,.blog-card{content-visibility:auto;contain-intrinsic-size:auto 360px}
"""

ADMIN_NOTE = (
    '<p style="background:#fef3c7;border:1px solid #fcd34d;border-radius:8px;'
    'padding:.6rem .8rem;font-size:.75rem;color:#78350f;margin:.6rem 0">'
    'Security: use a <b>fine-grained</b> token limited to this one repository, '
    'Contents = Read and write, and set a <b>7-day expiry</b>. Never paste a token '
    'on a shared phone, and use &ldquo;Forget everything&rdquo; when you finish.</p>'
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


def trim(desc, limit=155):
    desc = desc.strip()
    if len(desc) <= 165:
        return desc
    cut = desc[:limit]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip(" ,.;:—-.") + "…"


def fix_descriptions():
    pages = 0
    for rel, new in DESCRIPTIONS.items():
        path = os.path.join(ROOT, rel)
        t = read(path)
        if not t:
            continue
        m = re.search(r'<meta name="description" content="([^"]*)"', t)
        if not m or m.group(1) == new:
            continue
        t = t[:m.start(1)] + new + t[m.end(1):]
        write(path, t)
        pages += 1

    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in (".git", ".github", "node_modules")]
        for f in files:
            if not f.endswith(".html"):
                continue
            path = os.path.join(d, f)
            t = read(path)
            if not t:
                continue
            changed = False
            for m in list(re.finditer(r'<meta name="description" content="([^"]*)"', t)):
                old = m.group(1)
                if len(old) <= 165:
                    continue
                new = trim(old)
                if new != old:
                    t = t[:m.start(1)] + new + t[m.end(1):]
                    changed = True
            if changed:
                write(path, t)
                pages += 1
    return pages


def fix_css():
    path = os.path.join(ROOT, "assets", "style.css")
    t = read(path)
    if not t or "content-visibility:auto" in t:
        return False
    write(path, t.rstrip() + "\n" + CSS_ADDITION)
    return True


def fix_admin_note():
    path = os.path.join(ROOT, "admin", "index.html")
    t = read(path)
    if not t or "fine-grained" in t:
        return False
    anchor = "GitHub Token paste karo"
    i = t.find(anchor)
    if i < 0:
        return False
    j = t.find("</p>", i)
    if j < 0:
        return False
    t = t[: j + 4] + ADMIN_NOTE + t[j + 4:]
    write(path, t)
    return True


def main():
    print("pages with better descriptions:", fix_descriptions())
    print("css content-visibility added:", fix_css())
    print("admin security note added:", fix_admin_note())


if __name__ == "__main__":
    main()
