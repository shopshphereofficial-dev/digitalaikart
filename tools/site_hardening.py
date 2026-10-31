#!/usr/bin/env python3
"""
Security and hygiene pass over the static site.

Fixes, all idempotent:

  * escapes the label the help bot prints into a link button (the label comes
    from the model, so it must never be treated as HTML)
  * rebuilds the paid assistant's linkify() so a URL from the model can neither
    break out of the href attribute nor inject markup
  * adds rel="noopener noreferrer" to every target="_blank" link that lacks it
  * adds <meta name="referrer" content="strict-origin-when-cross-origin"> to
    pages that lack it, so tokens never leak through the Referer header
  * marks the admin panel, the ad creatives and the utility pages
    (404, thank-you) noindex so they stay out of Google

Usage:  python3 tools/site_hardening.py [repo_root]
"""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

NOINDEX_PATHS = ("admin/index.html", "404.html", "thank-you.html",
                 "ads/banner.html", "ads/native.html", "ads/test.html")
NOINDEX_META = '<meta name="robots" content="noindex, nofollow">'
REFERRER_META = '<meta name="referrer" content="strict-origin-when-cross-origin">'

ESC_FN = (
    "  function esc(s) {\n"
    "    return String(s == null ? '' : s)\n"
    "      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')\n"
    "      .replace(/\"/g, '&quot;').replace(/'/g, '&#39;');\n"
    "  }\n\n"
)

NEW_LINKIFY = """  function linkify(m) {
    var raw = m.textContent, out = '', last = 0, x;
    var re = /(https?:\\/\\/[^\\s)<>"']+)/g;
    function esc(s) {
      return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
              .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }
    while ((x = re.exec(raw))) {
      out += esc(raw.slice(last, x.index));
      var u = esc(x[1]);
      out += '<a href="' + u + '" target="_blank" rel="noopener noreferrer">' + u + '</a>';
      last = x.index + x[1].length;
    }
    out += esc(raw.slice(last));
    m.innerHTML = out;
  }"""


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def fix_helpbot():
    path = os.path.join(ROOT, "assets", "helpbot.js")
    t = read(path)
    if not t or "function esc(s)" in t:
        return False
    changed = False
    anchor = "  function el(t, c, txt) {"
    if anchor in t:
        t = t.replace(anchor, ESC_FN + anchor, 1)
        changed = True
    old = "      a.innerHTML = '<span>' + (l.label || labelFor(l.url)) + '</span>' + arrow();"
    new = "      a.innerHTML = '<span>' + esc(l.label || labelFor(l.url)) + '</span>' + arrow();"
    if old in t:
        t = t.replace(old, new, 1)
        changed = True
    if changed:
        write(path, t)
    return changed


def fix_chat_linkify():
    path = os.path.join(ROOT, "ai", "chat.js")
    t = read(path)
    if not t:
        return False
    m = re.search(r"  function linkify\(m\) \{.*?\n  \}", t, re.S)
    if not m:
        return False
    if 'rel="noopener noreferrer"' in m.group(0) and "function esc(s)" in m.group(0):
        return False
    t = t[:m.start()] + NEW_LINKIFY + t[m.end():]
    write(path, t)
    return True


BLANK_RE = re.compile(r"<a\b[^>]*target=\"_blank\"[^>]*>")


def fix_blank_links(path, text):
    changed = False

    def repl(m):
        nonlocal changed
        tag = m.group(0)
        if "noopener" in tag or "noreferrer" in tag:
            return tag
        changed = True
        if re.search(r'\brel="[^"]*"', tag):
            return re.sub(r'\brel="([^"]*)"', lambda x: 'rel="%s noopener noreferrer"' % x.group(1), tag, count=1)
        return tag[:-1] + ' rel="noopener noreferrer">'

    new = BLANK_RE.sub(repl, text)
    return new, changed


def main():
    js_help = fix_helpbot()
    js_chat = fix_chat_linkify()

    pages = 0
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in (".git", ".github", "node_modules")]
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            path = os.path.join(d, f)
            rel = os.path.relpath(path, ROOT)
            t = read(path)
            if not t:
                continue
            original = t
            t, changed = fix_blank_links(path, t)

            if REFERRER_META not in t and "<head" in t:
                t = t.replace("<head>", "<head>" + REFERRER_META, 1) if "<head>" in t else t
                t = t.replace("<head ", "<head " + REFERRER_META + " ", 1) if REFERRER_META not in t else t

            if rel in NOINDEX_PATHS and NOINDEX_META not in t and "<head" in t:
                if "<head>" in t:
                    t = t.replace("<head>", "<head>" + NOINDEX_META, 1)
                else:
                    t = t.replace("<head ", "<head " + NOINDEX_META + " ", 1)

            if t != original:
                write(path, t)
                pages += 1

    print("helpbot.js hardened:", js_help)
    print("chat.js linkify hardened:", js_chat)
    print("pages updated:", pages)


if __name__ == "__main__":
    main()
