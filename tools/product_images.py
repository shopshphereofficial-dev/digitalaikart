#!/usr/bin/env python3
"""Digitalaikart — give every product page a natural cover image.

For each product page on disk it:
  * generates a natural, topic-specific image with Gemini (image model only —
    no Gemini text call),
  * saves it as a compressed 1200x630 JPEG at assets/products/<slug>.jpg,
  * inserts <img class="product-cover"> as the first child of .product-hero,
  * points the Product schema, og:image and twitter:image at it.

Idempotent: a product that already has its .jpg and references it is skipped, so
re-running resumes where it stopped.

Environment:
    GEMINI_API_KEY   required (GitHub Actions secret)
    PRODUCT_LIMIT    optional, how many to process this run (0 = all)
    PRODUCT_OFFSET   optional, start index (for batching)
"""
import os
import sys
import re
import json
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import blog_agent as ba  # noqa: E402

PRODUCTS = os.path.join(ROOT, 'products.json')
PDIR = os.path.join(ROOT, 'products')
OUT = os.path.join(ROOT, 'assets', 'products')
SITE = 'https://digitalkartai.shop'


def load_products():
    """Every product page on disk, enriched from products.json where available."""
    meta = {}
    try:
        d = json.load(open(PRODUCTS, encoding='utf-8'))
        items = d if isinstance(d, list) else d.get('products', [])
        for it in items:
            slug = (it.get('slug') or '').strip()
            if slug:
                meta[slug] = it
    except Exception as e:
        print('products.json unreadable:', str(e)[:80])

    out = []
    for slug in sorted(os.listdir(PDIR)):
        page = os.path.join(PDIR, slug, 'index.html')
        if not os.path.isfile(page):
            continue
        it = dict(meta.get(slug) or {})
        it['slug'] = slug
        html = open(page, encoding='utf-8', errors='ignore').read()
        if not it.get('name'):
            m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
            it['name'] = re.sub(r'\s+', ' ', m.group(1)).strip() if m else slug.replace('-', ' ').title()
        if not it.get('tagline'):
            m = re.search(r'class="tagline"[^>]*>(.*?)</p>', html, re.S)
            it['tagline'] = re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''
        out.append(it)
    return out


def process(it):
    slug = it['slug']
    page = os.path.join(PDIR, slug, 'index.html')
    s = open(page, encoding='utf-8').read()
    rel = '/assets/products/%s.jpg' % slug
    fname = os.path.join(OUT, slug + '.jpg')

    if os.path.exists(fname) and rel in s:
        print('SKIP (done):', slug)
        return False

    name = (it.get('name') or slug).replace('\u2014', '-')
    tagline = (it.get('tagline') or '').strip()
    print('-> %s | %s' % (slug, name[:60]))

    prompt = (
        'A natural, photorealistic editorial photograph that suits this Indian digital guide: '
        '"%s". %s Real scene with real people or objects, natural lighting, believable colour. '
        'No text, no letters, no logos, no watermarks, no book covers, no screens with writing. '
        'Wide 16:9 landscape composition.' % (name, tagline[:200]))

    try:
        raw = ba.gemini_image(prompt)
    except Exception as e:
        print('   image failed:', str(e)[:90])
        return False
    if not raw:
        print('   no image returned')
        return False

    os.makedirs(OUT, exist_ok=True)
    w, h = ba.save_cover(raw, fname)
    print('   saved %s.jpg (%d KB, %dx%d)' % (slug, os.path.getsize(fname) // 1024, w, h))

    alt = name.replace('"', '&quot;')
    img = ('<img class="product-cover" src="%s" alt="%s" width="%d" height="%d">'
           % (rel, alt, w, h))

    if '<img class="product-cover"' in s:
        s = re.sub(r'<img class="product-cover"[^>]*>', img, s, count=1)
    else:
        s = s.replace('<section class="product-hero">',
                      '<section class="product-hero">\n  ' + img, 1)

    url = SITE + rel
    s = re.sub(r'("image"\s*:\s*")[^"]*(")', r'\g<1>' + url + r'\g<2>', s, count=1)
    s = re.sub(r'(<meta property="og:image" content=")[^"]*(")', r'\g<1>' + url + r'\g<2>', s, count=1)
    s = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")', r'\g<1>' + url + r'\g<2>', s, count=1)
    s = re.sub(r'(<meta property="og:image:width" content=")[^"]*(")', r'\g<1>%d\g<2>' % w, s, count=1)
    s = re.sub(r'(<meta property="og:image:height" content=")[^"]*(")', r'\g<1>%d\g<2>' % h, s, count=1)
    open(page, 'w', encoding='utf-8').write(s)
    print('   page wired')
    time.sleep(1)
    return True


def main():
    if not ba.KEY:
        raise SystemExit('GEMINI_API_KEY is not set')
    items = load_products()
    limit = int(os.environ.get('PRODUCT_LIMIT') or 0)
    offset = int(os.environ.get('PRODUCT_OFFSET') or 0)
    batch = items[offset:offset + limit] if limit else items[offset:]
    print('products total=%d, this run=%d (offset %d)' % (len(items), len(batch), offset))
    done = 0
    for it in batch:
        if process(it):
            done += 1
    print('images created this run:', done)


if __name__ == '__main__':
    main()
