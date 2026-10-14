#!/usr/bin/env python3
"""Digitalaikart — publish a queued blog post written by an agent.

An agent (on its own schedule) drops one JSON file into `blog/incoming/` with the
finished article. This script turns that JSON into a real blog post:

  * picks the oldest queued JSON (so nothing gets stranded),
  * generates ONLY the cover image with Gemini (no Gemini text call),
  * renders the post HTML with the site's own renderer,
  * updates blog/index.html and feed.xml,
  * deletes the JSON it consumed.

It never writes article text itself — that is the agent's job. If nothing is
queued it exits quietly with success, so the schedule simply does nothing.

Environment:
    GEMINI_API_KEY   required (GitHub Actions secret) — used for the image only.
"""
import os
import sys
import json
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import blog_agent as ba  # noqa: E402  (reuse the renderer + Gemini image helper)

BLOG = os.path.join(ROOT, 'blog')
OG = os.path.join(ROOT, 'assets', 'og')
INCOMING = os.path.join(BLOG, 'incoming')

REQUIRED = ('title', 'slug', 'category', 'description', 'sections')


def pick_queued():
    """Oldest queued JSON first."""
    if not os.path.isdir(INCOMING):
        return None
    files = sorted(f for f in os.listdir(INCOMING) if f.endswith('.json'))
    return os.path.join(INCOMING, files[0]) if files else None


def main():
    path = pick_queued()
    if not path:
        print('no queued post — nothing to do')
        return

    name = os.path.basename(path)
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        raise SystemExit('queued file %s is not valid JSON: %s' % (name, e))

    missing = [k for k in REQUIRED if not data.get(k)]
    if missing:
        raise SystemExit('queued file %s is missing: %s' % (name, ', '.join(missing)))
    if not isinstance(data.get('sections'), list) or not data['sections']:
        raise SystemExit('queued file %s has no sections' % name)
    print('publishing queued post:', name, '|', data['title'][:60])

    post = data
    item = {
        'title': data.get('source_title') or data['title'],
        'link': data.get('source_url', ''),
        'source': data.get('source_name', 'News'),
        'desc': '',
    }

    slug = ba.slugify(post.get('slug') or post['title'], 55)
    pubdate = datetime.date.today()
    fname = '%s-%s.html' % (pubdate.isoformat(), slug)
    if os.path.exists(os.path.join(BLOG, fname)):
        print('post already exists, dropping queued file:', fname)
        os.remove(path)
        return

    # ---- cover image: the ONLY Gemini call in this whole script ----
    img_name = '%s-%s.jpg' % (pubdate.isoformat(), slug)
    img_w, img_h = 1200, 630
    prompt = post.get('image_prompt') or (
        'A natural, photorealistic editorial photo for this news story: "%s". '
        'Real scene, real people or objects, natural lighting. No text, no letters, '
        'no logos, no watermarks. Wide 16:9 landscape.' % post['title'])
    try:
        raw = ba.gemini_image(prompt)
        if raw:
            img_w, img_h = ba.save_cover(raw, os.path.join(OG, img_name))
            print('image written:', img_name, img_w, 'x', img_h)
        else:
            img_name = ''
            print('image generation failed — publishing without a cover')
    except Exception as e:
        img_name = ''
        print('image generation failed (%s) — publishing without a cover' % str(e)[:80])

    html_doc = ba.render_post(post, item, img_name, img_w, img_h, pubdate)
    open(os.path.join(BLOG, fname), 'w', encoding='utf-8').write(html_doc)
    print('post written:', fname)

    key = '%s-%s' % (pubdate.isoformat(), slug)
    ba.update_index(post, key, img_name, pubdate)
    ba.update_feed(post, key, pubdate)
    if item['link']:
        ba.mark_used(item['link'])
    os.remove(path)
    print('done — queued file removed')


if __name__ == '__main__':
    main()
