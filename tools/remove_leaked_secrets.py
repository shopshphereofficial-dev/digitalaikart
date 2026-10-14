#!/usr/bin/env python3
"""Digitalaikart — emergency: strip the leaked secrets out of the public files.

The AI section (ai/auth.js) and the help bot (assets/helpbot.js) shipped with a
GitHub personal access token and a Gemini API key written straight into the
JavaScript, obfuscated only by splitting them into arrays and joining them. The
files are public, so anyone could read those values.

This script replaces any such array-joined secret with an empty string, so the
live files stop handing the secrets to every visitor.

IMPORTANT: this does NOT undo the leak — the values remain in the git history and
stay valid until the token is revoked and the key rotated. It only stops the
ongoing exposure. The real fix is the Edge Function rewrite.

Idempotent.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = [
    os.path.join(ROOT, 'ai', 'auth.js'),
    os.path.join(ROOT, 'assets', 'helpbot.js'),
]

# a secret hidden as ['ab','cd',...].join('')
SECRET_ARRAY = re.compile(
    r"\[\s*'(?:github_pat|ghp_|AQ\.|AIza)[^']*'\s*(?:,\s*'[^']*'\s*)*\]\.join\(''\)"
)


def scrub(path):
    if not os.path.isfile(path):
        print('skip (missing):', os.path.relpath(path, ROOT))
        return 0
    s = open(path, encoding='utf-8').read()
    hits = len(SECRET_ARRAY.findall(s))
    if not hits:
        print('clean already:', os.path.relpath(path, ROOT))
        return 0
    s = SECRET_ARRAY.sub("''", s)
    s = s.replace(
        "/* users-repo token — filled in after owner creates the fine-grained PAT */",
        "/* SECRET REMOVED — this file must never contain credentials again. */"
    )
    open(path, 'w', encoding='utf-8').write(s)
    print('scrubbed %d secret(s) from %s' % (hits, os.path.relpath(path, ROOT)))
    return hits


def main():
    total = 0
    for t in TARGETS:
        total += scrub(t)
    print('total secrets removed:', total)
    if total == 0:
        print('nothing to do')


if __name__ == '__main__':
    main()
