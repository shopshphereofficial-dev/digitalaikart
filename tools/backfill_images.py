#!/usr/bin/env python3
"""Digitalaikart — backfill natural cover images for existing blog posts.

For each slug listed in BACKFILL_SLUGS it:
  1. writes a short, story-specific image prompt (Gemini text, with a fallback),
  2. generates a natural, photorealistic cover image (Gemini image),
  3. centre-crops it to a real 1200x630 JPEG,
  4. swaps the post's inline SVG / old cover for a real <img class="post-cover">,
  5. points og:image / twitter:image at the new file,
  6. puts the same image on the blog index card.

Idempotent: re-running only touches posts that still lack a .jpg cover.

Environment:
    GEMINI_API_KEY    required (GitHub Actions secret)
    BACKFILL_SLUGS    comma-separated post slugs (filename without .html)
"""
import os
import re
import sys
import io
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import blog_agent as ba  # noqa: E402  (reuse Gemini helpers + retry logic)

from PIL import Image  # noqa: E402

BLOG = os.path.join(ROOT, 'blog')
OG = os.path.join(ROOT, 'assets', 'og')
INDEX = os.path.join(BLOG, 'index.html')
SITE = 'https://digitalkartai.shop'
W, H = 1200, 630

COVER_CSS = ('.post-cover{width:100%;height:auto;border-radius:14px;border:1px solid var(--border);'
             'display:block;aspect-ratio:16/9;object-fit:cover}')


def field(s, pattern, default=''):
    m = re.search(pattern, s, re.S)
    return m.group(1).strip() if m else default


def to_cover_jpeg(raw, out_path):
    """Centre-crop to 16:9 and save a real, optimised 1200x630 JPEG."""
    im = Image.open(io.BytesIO(raw)).convert('RGB')
    w, h = im.size
    target = W / H
    if w / h > target:
        nw = int(round(h * target))
        left = (w - nw) // 2
        im = im.crop((left, 0, left + nw, h))
    else:
        nh = int(round(w / target))
        top = (h - nh) // 2
        im = im.crop((0, top, w, top + nh))
    im = im.resize((W, H), Image.LANCZOS)
    im.save(out_path, 'JPEG', quality=82, optimize=True, progressive=True)
    return os.path.getsize(out_path)


def image_prompt(title, desc):
    """Ask the text model for a bespoke prompt; fall back to a direct one."""
    try:
        out = ba.gemini_text(
            'Write ONE short image-generation prompt (max 60 words) for a photorealistic editorial '
            'photo that illustrates this news story. Describe a concrete, natural scene with real '
            'people, places or objects. No text, no logos, no brand colours. Wide 16:9 landscape.\n\n'
            'Headline: %s\nSummary: %s\n\nReturn ONLY JSON: {"image_prompt": "..."}' % (title, desc))
        p = (out or {}).get('image_prompt', '').strip()
        if p:
            return p + ' Photorealistic, natural lighting, no text, no letters, no logos, wide 16:9.'
    except Exception as e:
        print('  prompt model unavailable (%s) — using direct prompt' % str(e)[:60])
    return ('A natural, photorealistic editorial photo for this news story: "%s". %s '
            'Real scene, real people or objects, natural lighting, believable colour. '
            'No text, no letters, no logos, no watermarks. Wide 16:9 landscape.' % (title, desc))


def process(slug, idx):
    fname = slug + '.html'
    path = os.path.join(BLOG, fname)
    if not os.path.exists(path):
        print('SKIP (no file):', fname)
        return idx
    post = open(path, encoding='utf-8').read()

    base = field(post, r'og:image"\s+content="https://digitalkartai\.shop/assets/og/([^"]+?)\.(?:png|jpe?g)"') or slug
    new_name = base + '.jpg'
    new_path = os.path.join(OG, new_name)

    if os.path.exists(new_path) and '/assets/og/%s' % new_name in post:
        print('SKIP (already has jpg cover):', fname)
        return idx

    title = field(post, r'<title>(.*?)</title>')
    title = re.sub(r'\s*[—\-]\s*Digitalaikart\s*$', '', title).strip()
    desc = field(post, r'<meta name="description" content="([^"]*)"')
    print('-> %s | %s' % (slug, title[:60]))

    raw = ba.gemini_image(image_prompt(title, desc))
    if not raw:
        print('  image generation failed — left unchanged')
        return idx
    size = to_cover_jpeg(raw, new_path)
    print('  image written: %s (%d KB)' % (new_name, size // 1024))

    img_url = '%s/assets/og/%s' % (SITE, new_name)
    alt = title.replace('"', '&quot;')
    img_tag = ('<img class="post-cover" src="/assets/og/%s" alt="%s" width="%d" height="%d">'
               % (new_name, alt, W, H))

    # 1. cover inside the post
    if re.search(r'<img class="post-cover"', post):
        post = re.sub(r'<img class="post-cover"[^>]*>', img_tag, post, count=1)
    elif re.search(r'<svg class="post-svg".*?</svg>', post, re.S):
        post = re.sub(r'<svg class="post-svg".*?</svg>', img_tag, post, count=1, flags=re.S)
    else:
        post = post.replace('<div class="post-wrap">', '<div class="post-wrap">\n  ' + img_tag, 1)

    # 2. cover styling
    if '.post-cover' not in post:
        post = post.replace('</style>', COVER_CSS + '</style>', 1)

    # 3. social / preview meta
    post = re.sub(r'(<meta property="og:image" content=")[^"]*(")', r'\g<1>' + img_url + r'\g<2>', post, count=1)
    post = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")', r'\g<1>' + img_url + r'\g<2>', post, count=1)
    post = re.sub(r'(<meta property="og:image:width" content=")[^"]*(")', r'\g<1>%d\g<2>' % W, post, count=1)
    post = re.sub(r'(<meta property="og:image:height" content=")[^"]*(")', r'\g<1>%d\g<2>' % H, post, count=1)

    # 3b. sweep up any remaining references (JSON-LD "image", etc.) in the post
    #     and in the blog index, so nothing points at the file we are replacing.
    for old_ext in ('.png', '.jpeg'):
        old_ref = '/assets/og/%s%s' % (base, old_ext)
        post = post.replace(old_ref, '/assets/og/%s' % new_name)
        idx = idx.replace(old_ref, '/assets/og/%s' % new_name)
    open(path, 'w', encoding='utf-8').write(post)

    # 4. index card
    card = ('<a class="blog-card" href="/blog/%s">' % fname)
    i = idx.find(card)
    if i >= 0:
        j = idx.find('<div class="blog-card-img">', i)
        k = idx.find('</div>', j)
        if j >= 0 and k > j:
            idx = idx[:j] + '<div class="blog-card-img"><img src="/assets/og/%s" alt="%s" loading="lazy">' % (new_name, alt) + idx[k:]
            print('  index card updated')
    else:
        print('  card not found in index')

    # 5. drop the stale old image
    old = os.path.join(OG, base + '.png')
    if base + '.png' != new_name and os.path.exists(old):
        os.remove(old)
        print('  removed stale', base + '.png')
    return idx


def main():
    if not ba.KEY:
        raise SystemExit('GEMINI_API_KEY is not set')
    slugs = [s.strip() for s in os.environ.get('BACKFILL_SLUGS', '').split(',') if s.strip()]
    if not slugs:
        raise SystemExit('BACKFILL_SLUGS is empty — nothing to do')
    print('backfilling %d post(s) on %s' % (len(slugs), datetime.date.today().isoformat()))
    idx = open(INDEX, encoding='utf-8').read()
    for slug in slugs:
        idx = process(slug, idx)
    open(INDEX, 'w', encoding='utf-8').write(idx)
    print('done')


if __name__ == '__main__':
    main()
