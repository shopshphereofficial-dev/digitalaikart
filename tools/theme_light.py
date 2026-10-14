#!/usr/bin/env python3
"""Digitalaikart - one-off, idempotent dark-navy/gold -> light/blue theme pass.

Changes COLOUR VALUES ONLY. No layout, spacing, font, size, wording, markup
structure or file name is touched.

What it does
------------
1. Rewrites the `:root` palette in `assets/style.css` to the light palette and
   replaces every hardcoded hex from the dark palette with its light equivalent,
   in `assets/style.css` AND in every page's inline `<style>` block and inline
   `style="..."` attributes. The replacement is a single simultaneous pass, so
   chained/overlapping values (e.g. `#1e3a5f`->`#e2e8f0` while `#e2e8f0`->
   `#0f172a`) resolve correctly and are never applied twice.
2. Applies one targeted contrast fix so the page is actually readable on the new
   light background: the fixed top nav used a hardcoded dark translucent
   `rgba(10,22,40,0.72)` which would have left dark link text on a dark bar.
   It becomes `rgba(255,255,255,0.72)`. This is the only non-hex colour changed
   by default (disable with `--no-contrast-fix`).

Idempotency
-----------
Every converted file gets a tiny `theme:light` marker comment. A file that
already carries the marker is skipped, so the script is safe to re-run and a
narrow `--scope test` run followed by a full run will not double-convert the
staging pages. (A plain value substitution is NOT idempotent here because
several target values - #e2e8f0, #334155, #94a3b8 - are also source values.)

Usage
-----
    python3 tools/theme_light.py                 # whole site
    python3 tools/theme_light.py --scope test    # 3 staging pages + style.css
    python3 tools/theme_light.py --dry-run       # report only, change nothing
    python3 tools/theme_light.py --rgba          # ALSO recolour rgba() tints
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dark palette value -> light palette value (exactly as specified).
HEX_MAP = {
    '#0a1628': '#ffffff',   # page background      -> white
    '#0f1e36': '#ffffff',   # card                 -> white
    '#081120': '#f8fafc',   # deep panel           -> very light grey
    '#1e3a5f': '#e2e8f0',   # border               -> light grey
    '#1a2f50': '#e2e8f0',
    '#f5c542': '#1d4ed8',   # gold accent          -> deep blue
    '#e8a82c': '#1e40af',
    '#e2e8f0': '#0f172a',   # light text           -> dark text
    '#f1f5f9': '#0f172a',
    '#cbd5e1': '#334155',
    '#94a3b8': '#475569',
    '#334155': '#64748b',
    '#475569': '#94a3b8',
    '#22c55e': '#16a34a',   # --green in :root (per the specified :root block)
}

# Optional rgba() tint recolour (off by default): rgb triple -> rgb triple.
RGBA_MAP = {
    '245,197,66': '29,78,216',    # gold   -> #1d4ed8
    '232,168,44': '30,64,175',    # gold-d -> #1e40af
    '148,163,184': '71,85,105',   # slate  -> #475569
}

HEX_RE = re.compile(r'#([0-9a-fA-F]{6})(?![0-9a-fA-F])')
CSS_MARKER = '/* theme:light */'
HTML_MARKER = '<!-- theme:light -->'

# Files never touched (generated / explicitly excluded by the brief).
EXCLUDE = {'blog/index.html'}

TEST_FILES = [
    'assets/style.css',
    'index.html',
    'products/8th-pay-commission-handbook/index.html',
    'blog/2026-09-16-activate-105-million-ai-fund.html',
]


def all_pages():
    out = ['assets/style.css']
    for f in sorted(os.listdir(ROOT)):
        if f.endswith('.html'):
            out.append(f)
    pdir = os.path.join(ROOT, 'products')
    for d in sorted(os.listdir(pdir)):
        p = os.path.join(pdir, d, 'index.html')
        if os.path.isfile(p):
            out.append(os.path.join('products', d, 'index.html'))
    bdir = os.path.join(ROOT, 'blog')
    for f in sorted(os.listdir(bdir)):
        if f.endswith('.html'):
            out.append(os.path.join('blog', f))
    return [p for p in out if p not in EXCLUDE]


def convert_hex(text):
    def repl(m):
        key = '#' + m.group(1).lower()
        return HEX_MAP.get(key, m.group(0))
    return HEX_RE.sub(repl, text)


def convert_rgba(text):
    def repl(m):
        triple = re.sub(r'\s+', '', m.group(1))
        return 'rgba(%s,%s)' % (RGBA_MAP.get(triple, m.group(1)), m.group(2))
    return re.sub(r'rgba\(\s*([0-9]{1,3}\s*,\s*[0-9]{1,3}\s*,\s*[0-9]{1,3})\s*,\s*([^)]+)\)', repl, text)


def fix_nav(text):
    """Light nav bar so dark link text stays readable (the one contrast fix)."""
    return text.replace('background:rgba(10,22,40,0.72)', 'background:rgba(255,255,255,0.72)')


def process(path, dry, use_rgba, contrast_fix):
    full = os.path.join(ROOT, path)
    src = open(full, encoding='utf-8').read()
    if CSS_MARKER in src or HTML_MARKER in src:
        return ('skip', path)
    out = convert_hex(src)
    if use_rgba:
        out = convert_rgba(out)
    if contrast_fix and path == 'assets/style.css':
        out = fix_nav(out)
    if out == src:
        return ('unchanged', path)
    if not dry:
        if path.endswith('.css'):
            out = out.rstrip('\n') + '\n' + CSS_MARKER + '\n'
        else:
            if re.search(r'<head[^>]*>', out, re.I):
                out = re.sub(r'(<head[^>]*>)', r'\1' + HTML_MARKER, out, count=1, flags=re.I)
            else:
                out = HTML_MARKER + '\n' + out
        open(full, 'w', encoding='utf-8').write(out)
    return ('changed', path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scope', choices=['test', 'all'], default='all')
    ap.add_argument('--files', default='', help='comma-separated explicit file list')
    ap.add_argument('--rgba', action='store_true', help='also recolour rgba() gold/slate tints')
    ap.add_argument('--no-contrast-fix', action='store_true', help='skip the nav contrast fix')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    if args.files:
        files = [f.strip() for f in args.files.split(',') if f.strip()]
    elif args.scope == 'test':
        files = TEST_FILES
    else:
        files = all_pages()

    changed = skipped = unchanged = 0
    for p in files:
        status, _ = process(p, args.dry_run, args.rgba, not args.no_contrast_fix)
        if status == 'changed':
            changed += 1
            print('   changed: %s' % p)
        elif status == 'skip':
            skipped += 1
        else:
            unchanged += 1
    verb = 'would change' if args.dry_run else 'changed'
    print('theme_light: scope=%s rgba=%s contrast_fix=%s' %
          (args.scope, args.rgba, not args.no_contrast_fix))
    print('%s %d file(s); skipped %d (already converted); %d had nothing to do' %
          (verb, changed, skipped, unchanged))


if __name__ == '__main__':
    main()
