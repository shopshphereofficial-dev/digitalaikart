#!/usr/bin/env python3
"""
Give every image its real width and height (and lazy-load the ones below the
fold), so the browser reserves space before the picture arrives.

That is the single cheapest Core Web Vitals win on this site: the blog and
product listings carry dozens of cover images each, and without intrinsic
dimensions every one of them shifts the layout as it loads (CLS), which Google
counts in page experience.

The site's CSS already has `img{max-width:100%;height:auto}` and the card styles
set their own height, so adding the attributes cannot distort anything.

Idempotent: images that already carry width and height are skipped.

Usage:  python3 tools/img_dimensions.py [repo_root]
"""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
SRC_RE = re.compile(r'src="([^"]+)"', re.I)


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def size_of(path):
    """Return (w, h) for a local image file, or None."""
    if not os.path.isfile(path):
        return None
    if path.lower().endswith(".svg"):
        try:
            head = open(path, "r", encoding="utf-8", errors="replace").read(600)
            w = re.search(r'width="(\d+(?:\.\d+)?)', head)
            h = re.search(r'height="(\d+(?:\.\d+)?)', head)
            if w and h:
                return int(float(w.group(1))), int(float(h.group(1)))
            vb = re.search(r'viewBox="[\d.\-]+\s+[\d.\-]+\s+([\d.]+)\s+([\d.]+)"', head)
            if vb:
                return int(float(vb.group(1))), int(float(vb.group(2)))
        except OSError:
            pass
        return None
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def main():
    pages = 0
    imgs = 0
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in (".git", ".github", "node_modules")]
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            page = os.path.join(d, f)
            t = read(page)
            if not t:
                continue
            original = t
            seen_first = [False]

            def repl(m):
                tag = m.group(0)
                # collapse any duplicated lazy/decoding attributes from earlier runs
                tag = re.sub(r'(\sloading="lazy")(?=\s[^>]*\sloading="lazy")', '', tag)
                tag = re.sub(r'(\sdecoding="async")(?=\s[^>]*\sdecoding="async")', '', tag)
                if re.search(r"\bwidth=", tag) and re.search(r"\bheight=", tag):
                    seen_first[0] = True
                    return tag
                src = SRC_RE.search(tag)
                if not src or not src.group(1).startswith("/"):
                    return tag
                local = os.path.join(ROOT, src.group(1).lstrip("/").split("?")[0])
                wh = size_of(local)
                if not wh:
                    return tag
                w, h = wh
                extra = ' width="%d" height="%d"' % (w, h)
                if not re.search(r"\bdecoding=", tag):
                    extra += ' decoding="async"'
                if not seen_first[0]:
                    # first image on the page is likely the LCP candidate: load it eagerly
                    seen_first[0] = True
                elif not re.search(r"\bloading=", tag):
                    extra += ' loading="lazy"'
                return tag[:-1] + extra + ">"

            t = IMG_RE.sub(repl, t)
            if t != original:
                write(page, t)
                pages += 1
                imgs += t.count(' loading="lazy"') - original.count(' loading="lazy"')

    print("pages updated: %d, images given dimensions: %d" % (pages, max(imgs, 0)))


if __name__ == "__main__":
    main()
