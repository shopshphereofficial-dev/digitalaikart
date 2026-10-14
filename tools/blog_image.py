#!/usr/bin/env python3
"""Digitalaikart — publish step for agent-written posts.

The article text is written by the blog agent (not by Gemini). Each finished
post arrives as a JSON spec in blog/pending/. This script asks Gemini for the
cover image ONLY, then renders the post HTML and updates the blog index and the
RSS feed. Runs from GitHub Actions (which holds the GEMINI_API_KEY secret), or
by hand after dropping a spec.

Spec shape — blog/pending/<date>-<slug>.json:
{
  "date": "2026-10-14",
  "title": "...", "slug": "...", "category": "...",
  "description": "...", "emoji": "...",
  "keywords": ["..."], "tags": ["#A", "#B"],
  "tldr": ["..."],
  "sections": [{"heading": "...", "paragraphs": ["..."]}],
  "faq": [{"q": "...", "a": "..."}],
  "image_prompt": "...",
  "source_name": "...", "source_link": "https://..."
}

Environment:
    GEMINI_API_KEY   required — used only for the cover image
"""
import os
import glob
import json
import datetime

import blog_agent as B

PENDING = os.path.join(B.BLOG, 'pending')


def process(spec_path):
    spec = json.load(open(spec_path, encoding='utf-8'))
    slug = B.slugify(spec.get('slug') or spec['title'], 55)
    try:
        pubdate = datetime.date.fromisoformat(spec['date'])
    except Exception:
        pubdate = datetime.date.today()

    fname = '%s-%s.html' % (pubdate.isoformat(), slug)
    if os.path.exists(os.path.join(B.BLOG, fname)):
        print('post already exists, skipping:', fname)
        os.remove(spec_path)
        return

    img_name = '%s-%s.png' % (pubdate.isoformat(), slug)
    img_w, img_h = 1200, 630
    prompt = spec.get('image_prompt') or (
        'a natural, photorealistic editorial image for a story about: ' +
        spec['title'] + '. Wide 16:9, no text.')
    try:
        data = B.gemini_image(prompt)
    except Exception as e:
        print('image generation failed (post still published):', e)
        data = None
    if data:
        img_w, img_h = B.png_size(data)
        open(os.path.join(B.OG, img_name), 'wb').write(data)
        print('image written:', img_name, img_w, 'x', img_h)
    else:
        print('no image — publishing text only')
        img_name = ''

    item = {'source': spec.get('source_name', 'News'),
            'link': spec.get('source_link', '')}
    doc = B.render_post(spec, item, img_name, img_w, img_h, pubdate)
    open(os.path.join(B.BLOG, fname), 'w', encoding='utf-8').write(doc)
    print('post written:', fname)

    slug_full = '%s-%s' % (pubdate.isoformat(), slug)
    B.update_index(spec, slug_full, img_name, pubdate)
    B.update_feed(spec, slug_full, pubdate)
    if spec.get('source_link'):
        B.mark_used(spec['source_link'])
    os.remove(spec_path)


def main():
    if not B.KEY:
        raise SystemExit('GEMINI_API_KEY is not set')
    specs = sorted(glob.glob(os.path.join(PENDING, '*.json')))
    if not specs:
        print('nothing pending — no agent-written post waiting')
        return
    for s in specs:
        try:
            process(s)
        except Exception as e:
            print('failed:', os.path.basename(s), '->', e)


if __name__ == '__main__':
    main()
