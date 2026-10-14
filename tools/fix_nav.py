"""Rename the nav link 'AI Assistant' to 'Astral AI' across the site."""
import os, re

ROOT = os.getcwd()
changed = 0
files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules', 'ads')]
    for fn in filenames:
        if fn.endswith('.html'):
            files.append(os.path.join(dirpath, fn))

for p in files:
    s = open(p, encoding='utf-8').read()
    orig = s
    # nav link, keep whatever class it already has
    s = re.sub(r'(<a href="/ai/"[^>]*>)\s*AI Assistant\s*(</a>)', r'\1Astral AI\2', s)
    # footer link, if it says AI Assistant
    s = re.sub(r'(<a href="/ai/plans\.html"[^>]*>)\s*AI Assistant\s*(</a>)', r'\1Astral AI Plans\2', s)
    if s != orig:
        open(p, 'w', encoding='utf-8').write(s)
        changed += 1

print("html files scanned:", len(files))
print("files changed:", changed)
