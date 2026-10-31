#!/usr/bin/env python3
"""
Repair broken card wrappers on the listing pages.

Ninety-five cards on products/index.html had lost their wrapping
`<div class="card">`, so the page carried 90 stray `</div>` tags and those cards
were rendered without the .card wrapper — no border, shadow or spacing. That is
both a visible layout bug and invalid markup.

The repair is line based and conservative: it only inserts a `<div class="card">`
line in front of a `<div class="card-img">` that does not already have one, then
re-parses the whole page and refuses to save unless the markup is balanced.

Idempotent: a page whose cards are already wrapped is left alone.

Usage:  python3 tools/fix_product_cards.py [repo_root]
"""
import os
import sys
from html.parser import HTMLParser

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
TARGETS = ["products/index.html", "blog/index.html", "apps/index.html"]

VOID = {"img", "br", "meta", "link", "input", "hr", "source", "area", "base", "col", "embed"}


class Balance(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.stray = 0

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.stack.pop()
            if self.stack:
                self.stack.pop()
        else:
            self.stray += 1


def balance(text):
    p = Balance()
    p.feed(text)
    return p.stray, len(p.stack)


def repair(text):
    lines = text.split("\n")
    starts = {i for i, l in enumerate(lines) if l.strip().startswith('<div class="card-img"')}
    out = []
    inserted = 0
    for i, line in enumerate(lines):
        if i in starts and '<div class="card">' not in "\n".join(out[-4:]):
            indent = line[: len(line) - len(line.lstrip())]
            out.append((indent[:-2] if len(indent) >= 2 else "") + '<div class="card">')
            inserted += 1
        out.append(line)
    return "\n".join(out), inserted


def main():
    total = 0
    for rel in TARGETS:
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        stray, unclosed = balance(text)
        if stray == 0 and unclosed == 0:
            continue
        fixed, inserted = repair(text)
        stray2, unclosed2 = balance(fixed)
        if stray2 or unclosed2:
            print("%s: still unbalanced (stray %d, unclosed %d) — left untouched"
                  % (rel, stray2, unclosed2))
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(fixed)
        total += inserted
        print("%s: re-inserted %d card wrappers (page had %d stray closers)"
              % (rel, inserted, stray))
    print("cards repaired:", total)


if __name__ == "__main__":
    main()
