#!/usr/bin/env python3
"""Digitalaikart — AI news blog agent.

Fetches the latest AI news, writes a blog post in the site's own format,
generates a natural, story-specific cover image with Gemini, and updates the
blog index and the RSS feed. Runs daily from GitHub Actions.

Environment:
    GEMINI_API_KEY   required (set as a GitHub Actions secret — never committed)
    FORCE_TODAY      optional; "1" re-generates today's post from scratch
"""
import os
import re
import json
import base64
import html
import datetime
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, 'blog')
OG = os.path.join(ROOT, 'assets', 'og')
INDEX = os.path.join(BLOG, 'index.html')
FEED = os.path.join(ROOT, 'feed.xml')
USED = os.path.join(BLOG, 'agent-used.json')
BASE = 'https://digitalkartai.shop'
AUTHOR = 'Digitalaikart Editorial'
SIGNATURE = 'Digitalaikart Editorial'

KEY = os.environ.get('GEMINI_API_KEY', '').strip()
FORCE = os.environ.get('FORCE_TODAY', '').strip().lower() in ('1', 'true', 'yes')
# Newest first; older ones are kept as fallbacks because Google retires models.
TEXT_MODELS = ['gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-flash-latest', 'gemini-2.5-flash']
IMAGE_MODELS = ['gemini-3.1-flash-image', 'gemini-3-pro-image', 'gemini-2.5-flash-image']
API = 'https://generativelanguage.googleapis.com/v1beta/models/'

FEEDS = [
    'https://news.google.com/rss/search?q=artificial+intelligence+India+when:3d&hl=en-IN&gl=IN&ceid=IN:en',
    'https://news.google.com/rss/search?q=%22artificial+intelligence%22+when:2d&hl=en-IN&gl=IN&ceid=IN:en',
    'https://techcrunch.com/category/artificial-intelligence/feed/',
]

UA = 'Mozilla/5.0 (compatible; DigitalaikartBlogBot/1.0)'


# ---------------------------------------------------------------- helpers
def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def slugify(s, maxlen=60):
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s[:maxlen].strip('-')


def png_size(data):
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        w = int.from_bytes(data[16:20], 'big')
        h = int.from_bytes(data[20:24], 'big')
        return w, h
    return 1200, 630


def strip_tags(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


# ---------------------------------------------------------------- gemini
def gemini_text(prompt):
    body = json.dumps({
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'responseMimeType': 'application/json', 'temperature': 0.8},
    }).encode()
    last = None
    for model in TEXT_MODELS:
        try:
            req = urllib.request.Request(API + model + ':generateContent?key=' + KEY,
                                         data=body, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.loads(r.read())
            txt = d['candidates'][0]['content']['parts'][0]['text']
            print('text model:', model)
            return json.loads(txt)
        except Exception as e:
            last = e
            print('text model failed:', model, str(e)[:90])
    raise SystemExit('no working text model: %s' % last)


def gemini_image(prompt):
    body = json.dumps({'contents': [{'parts': [{'text': prompt}]}]}).encode()
    for model in IMAGE_MODELS:
        try:
            req = urllib.request.Request(API + model + ':generateContent?key=' + KEY,
                                         data=body, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.loads(r.read())
            for part in d['candidates'][0]['content']['parts']:
                if 'inlineData' in part:
                    print('image model:', model)
                    return base64.b64decode(part['inlineData']['data'])
        except Exception as e:
            print('image model failed:', model, str(e)[:90])
    return None


# ---------------------------------------------------------------- news
def fetch_news():
    items = []
    for feed in FEEDS:
        try:
            root = ET.fromstring(http_get(feed))
        except Exception as e:
            print('feed failed:', feed, e)
            continue
        for it in root.iter('item'):
            title = (it.findtext('title') or '').strip()
            link = (it.findtext('link') or '').strip()
            desc = strip_tags(it.findtext('description') or '')[:600]
            src = ''
            m = re.search(r'-\s*([^-]+)$', title)
            if m:
                src = m.group(1).strip()
                title = title[:m.start()].strip()
            if not title or not link:
                continue
            items.append({'title': title, 'link': link, 'desc': desc, 'source': src or 'News'})
    return items


def already_used(link, title):
    used = []
    if os.path.exists(USED):
        try:
            used = json.load(open(USED, encoding='utf-8'))
        except Exception:
            used = []
    if link in used:
        return True
    slug = slugify(title, 80)
    for f in os.listdir(BLOG):
        if f.endswith('.html') and slug[:38] and slug[:38] in f:
            return True
    return False


def pick_item(items):
    for it in items:
        if not already_used(it['link'], it['title']):
            return it
    return None


def article_text(url, limit=5000):
    """Best-effort fetch of the source page for grounding. Never fatal."""
    try:
        raw = http_get(url, timeout=25).decode('utf-8', 'ignore')
        return strip_tags(raw)[:limit]
    except Exception:
        return ''


def recent_posts(exclude_slug, n=3):
    """Newest existing posts, for the 'related' block (internal linking)."""
    out = []
    files = sorted([f for f in os.listdir(BLOG) if f.endswith('.html') and f != 'index.html'], reverse=True)
    for f in files:
        if exclude_slug in f:
            continue
        try:
            s = open(os.path.join(BLOG, f), encoding='utf-8').read()
        except Exception:
            continue
        m = re.search(r'<title>(.*?)</title>', s, re.S)
        if not m:
            continue
        title = re.sub(r'\s*[—\-]\s*Digitalaikart\s*$', '', m.group(1)).strip()
        out.append((title, '/blog/' + f))
        if len(out) >= n:
            break
    return out


# ---------------------------------------------------------------- prompt
IMAGE_STYLE = (
    "a striking, natural editorial image for this specific story. Make it look REAL and different every time: "
    "a photorealistic scene (or a realistic photographic-style rendering) with people, places or objects that suit "
    "THIS story, natural lighting and believable colour. Do NOT use a flat corporate vector look and do NOT force any "
    "fixed brand palette or the website's colours. Wide 16:9 landscape composition, one clear subject, no text, "
    "no letters, no logos, no watermarks, no UI screenshots."
)


def build_prompt(item, body_text):
    today = datetime.date.today().strftime('%B %d, %Y')
    return """You are the editor of Digitalaikart, an India-focused AI news blog (audience: Indian students, professionals, entrepreneurs). Write ONE news-explainer blog post about the story below.

STORY
Headline: %s
Source: %s
Link: %s
Feed summary: %s
Article text (may be empty or partial): %s

RULES
- Write in clear, plain English. India-first framing: what it means for Indian users, students, professionals or businesses.
- FACTUAL: only use facts present in the material above. Never invent quotes, numbers, dates or names. If a detail is missing, stay general instead of guessing.
- No emojis inside the article text. Do not use markdown.
- Today's date is %s.

Return ONLY JSON, exactly this shape:
{
 "title": "headline, <=70 chars, no clickbait",
 "slug": "kebab-case, <=55 chars",
 "category": "one of: AI Business, AI Policy, AI Products, AI Hardware, AI Jobs, AI Safety, AI Research, AI India",
 "description": "meta description, 140-160 chars, ends with a full stop",
 "emoji": "one emoji that fits the story",
 "keywords": ["5 short keywords"],
 "tags": ["#Tag1","#Tag2","#Tag3","#Tag4"],
 "tldr": ["3-4 one-line takeaways"],
 "sections": [{"heading": "short heading without numbering", "paragraphs": ["paragraph", "paragraph"]}],
 "faq": [{"q": "question", "a": "2-line answer"}],
 "image_prompt": "%s"
}
Provide 4-5 sections with 1-2 paragraphs each (aim 700-900 words total) and 3 FAQ items.""" % (
        item['title'], item['source'], item['link'], item['desc'][:600], body_text[:3500], today, IMAGE_STYLE)


# ---------------------------------------------------------------- render
def post_css():
    """Reuse the styling of an existing post so new posts match the site."""
    for f in sorted(os.listdir(BLOG), reverse=True):
        if f.endswith('.html') and f != 'index.html':
            s = open(os.path.join(BLOG, f), encoding='utf-8').read()
            m = re.search(r'<style>(.*?)</style>', s, re.S)
            if m:
                return m.group(1)
    return ''


EXTRA_CSS = (
    '.post-cover{width:100%;height:auto;border-radius:14px;border:1px solid var(--border);display:block;aspect-ratio:16/9;object-fit:cover}'
)


def render_post(p, item, img_name, img_w, img_h, pubdate):
    slug = '%s-%s' % (pubdate.isoformat(), p['slug'])
    url = '%s/blog/%s.html' % (BASE, slug)
    img = '%s/assets/og/%s' % (BASE, img_name)
    words = sum(len(s.get('paragraphs', [])) * 60 for s in p['sections']) + 120
    mins = max(3, round(words / 200))
    date_h = pubdate.strftime('%B %d, %Y')
    iso = pubdate.isoformat()

    sections = []
    for i, s in enumerate(p['sections'], 1):
        paras = ''.join('<p>%s</p>' % html.escape(x) for x in s.get('paragraphs', []))
        sections.append('<h2><span class="num">%02d.</span>%s</h2>%s' % (i, html.escape(s['heading']), paras))
    faq = ''.join('<p><strong>%s</strong><br>%s</p>' % (html.escape(f['q']), html.escape(f['a'])) for f in p.get('faq', []))
    tldr = ''.join('<li>%s</li>' % html.escape(x) for x in p.get('tldr', []))
    tags = ''.join('<span>%s</span>' % html.escape(t) for t in p.get('tags', []))
    keywords = ', '.join(p.get('keywords', []))
    kw_meta = ''.join('<meta property="article:tag" content="%s">' % html.escape(k) for k in p.get('keywords', []))
    share_t = urllib.parse.quote(p['title'])
    share_u = urllib.parse.quote(url)

    rel = recent_posts(slug, 4)
    if rel:
        rel_html = '\n'.join('      <li><a href="%s">%s</a></li>' % (r[1], html.escape(r[0])) for r in rel)
    else:
        rel_html = '      <li><a href="/blog/">All AI news &amp; explainers →</a></li>'

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>%(title)s — Digitalaikart</title>
<meta name="description" content="%(desc)s">
<meta name="news_keywords" content="%(keywords)s">
<link rel="alternate" type="application/rss+xml" title="Digitalaikart Blog — AI News RSS Feed" href="https://digitalkartai.shop/feed.xml">
<link rel="canonical" href="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="article">
<meta property="article:section" content="%(category)s">
<meta property="article:published_time" content="%(iso)s">
<meta property="og:url" content="%(url)s">
<meta property="og:site_name" content="Digitalaikart">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta property="og:image" content="%(img)s">
<meta property="og:image:width" content="%(iw)d">
<meta property="og:image:height" content="%(ih)d">
<meta property="og:image:alt" content="%(title)s — Digitalaikart blog cover">
<meta name="twitter:image" content="%(img)s">
%(kwmeta)s
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "articleSection": "%(category)s",
  "headline": %(title_json)s,
  "description": %(desc_json)s,
  "image": ["%(img)s"],
  "datePublished": "%(iso)s",
  "publisher": {"@type": "Organization", "name": "Digitalaikart", "url": "https://digitalkartai.shop", "logo": {"@type": "ImageObject", "url": "https://digitalkartai.shop/assets/og-default.png", "width": 1200, "height": 630}},
  "author": {"@type": "Organization", "name": "Digitalaikart"},
  "mainEntityOfPage": "%(url)s",
  "keywords": %(keywords_json)s
}
</script>
<style>%(css)s%(extra)s</style>
</head>
<body>
<nav class="nav"><div class="nav-inner"><a href="/" class="nav-logo">Digitalaikart</a><div class="nav-links"><a href="/">Home</a><a href="/products/">Products</a><a href="/ai/">AI Assistant</a><a href="/blog/" class="active">Blog</a></div></div></nav>

<div class="post-wrap">
  <img class="post-cover" src="/assets/og/%(imgsrc)s" alt="%(title)s" width="%(iw)d" height="%(ih)d">

  <div class="post-meta"><span class="cat">%(category)s</span><span>%(date_h)s</span><span>%(mins)d min read</span><span>By %(author)s</span></div>
  <h1 class="post-title">%(title)s</h1>
  <div class="tag-pills" aria-label="Topics">%(tags)s</div>

  <div class="tldr">
    <h4>TL;DR</h4>
    <ul>%(tldr)s</ul>
  </div>

  <div class="post-body">
%(sections)s
    <div class="faq">
      <h2>Frequently asked questions</h2>
%(faq)s
    </div>
  </div>

  <div class="engage">
    <h4>Found this useful? Share it</h4>
    <div class="engage-row">
      <a class="engage-btn" href="https://wa.me/?text=%(share_t)s%%20%(share_u)s" target="_blank" rel="noopener">WhatsApp</a>
      <a class="engage-btn" href="https://twitter.com/intent/tweet?text=%(share_t)s&url=%(share_u)s" target="_blank" rel="noopener">X / Twitter</a>
      <a class="engage-btn" href="/products/">Explore AI guides</a>
    </div>
  </div>

  <div class="sources">
    <h4>Source</h4>
    <ul>
      <li><strong>%(source)s</strong> — <a href="%(link)s" target="_blank" rel="noopener nofollow">original report</a></li>
      <li>Published: %(date_h)s · Compiled by Digitalaikart</li>
    </ul>
  </div>

  <div class="related">
    <h4>More AI news</h4>
    <ul>
%(related)s
    </ul>
  </div>
</div>

<footer><div class="footer-links"><a href="/">Home</a><a href="/products/">Products</a><a href="/blog/">Blog</a><a href="/privacy-policy.html">Privacy Policy</a><a href="/refund-policy.html">Refund Policy</a><a href="/terms.html">Terms &amp; Conditions</a></div><p><strong>Digitalaikart</strong> — Premium AI Digital Products</p><p style="margin-top:0.5rem;color:#334155">&copy; %(year)d Digitalaikart. All rights reserved.</p></footer>
<script src="/assets/effects.js"></script>
</body>
</html>
""" % dict(
        title=html.escape(p['title']), desc=html.escape(p['description']), keywords=html.escape(keywords),
        kwmeta=kw_meta, url=url, img=img, imgsrc=img_name, iw=img_w, ih=img_h,
        category=html.escape(p['category']), iso=iso, date_h=date_h, mins=mins,
        author=AUTHOR, tags=tags, tldr=tldr, sections='\n'.join(sections), faq=faq,
        share_t=share_t, share_u=share_u, source=html.escape(item['source']), link=html.escape(item['link']),
        css=post_css(), extra=EXTRA_CSS, year=pubdate.year, related=rel_html,
        title_json=json.dumps(p['title']), desc_json=json.dumps(p['description']),
        keywords_json=json.dumps(keywords),
    )


# ---------------------------------------------------------------- index + feed
CARD_CSS = '<style id="dak-card-img">.blog-card-img img{width:100%;height:100%;object-fit:cover;display:block}</style>'


def ensure_card_css(s):
    if 'dak-card-img' in s:
        return s
    return s.replace('</head>', CARD_CSS + '\n</head>', 1)


def update_index(p, slug, img_name, pubdate):
    s = open(INDEX, encoding='utf-8').read()
    s = ensure_card_css(s)
    anchor = '<!-- NEW POSTS: insert new blog post cards directly below this line, above existing cards -->'
    if anchor not in s:
        print('index anchor missing; skipping index update')
        open(INDEX, 'w', encoding='utf-8').write(s)
        return
    if img_name:
        img_html = '<img src="/assets/og/%s" alt="%s" loading="lazy">' % (img_name, html.escape(p['title']))
    else:
        img_html = '<span>%s</span>' % p.get('emoji', '🤖')
    card = ('\n  <a class="blog-card" href="/blog/%s.html">\n'
            '    <div class="blog-card-img">%s</div>\n'
            '    <div class="blog-card-body">\n'
            '      <h3>%s</h3>\n'
            '      <p>%s</p>\n'
            '      <div class="date">%s · %s min read</div>\n'
            '    </div>\n'
            '  </a>') % (slug, img_html, html.escape(p['title']),
                          html.escape(p['description']), pubdate.strftime('%B %d, %Y'),
                          max(3, round(900 / 200)))
    s = s.replace(anchor, anchor + card, 1)
    open(INDEX, 'w', encoding='utf-8').write(s)


def update_feed(p, slug, pubdate):
    s = open(FEED, encoding='utf-8').read()
    item = ('\n    <item>\n'
            '      <title>%s</title>\n'
            '      <link>%s/blog/%s.html</link>\n'
            '      <guid isPermaLink="true">%s/blog/%s.html</guid>\n'
            '      <description>%s</description>\n'
            '      <pubDate>%s</pubDate>\n'
            '      <category>%s</category>\n'
            '    </item>') % (html.escape(p['title']), BASE, slug, BASE, slug,
                              html.escape(p['description']),
                              pubdate.strftime('%a, %d %b %Y 09:00:00 +0530'),
                              html.escape(p['category']))
    i = s.find('<item>')
    if i == -1:
        s = s.replace('</channel>', item + '\n  </channel>')
    else:
        s = s[:i] + item.strip() + '\n    ' + s[i:]
    open(FEED, 'w', encoding='utf-8').write(s)


def mark_used(link):
    used = []
    if os.path.exists(USED):
        try:
            used = json.load(open(USED, encoding='utf-8'))
        except Exception:
            used = []
    used.append(link)
    json.dump(used[-200:], open(USED, 'w', encoding='utf-8'), indent=1)


def cleanup_today():
    """Remove today's agent post so it can be regenerated (FORCE_TODAY=1)."""
    today = datetime.date.today().isoformat()
    for f in list(os.listdir(BLOG)):
        if not (f.startswith(today + '-') and f.endswith('.html')):
            continue
        path = os.path.join(BLOG, f)
        try:
            body = open(path, encoding='utf-8').read()
        except Exception:
            continue
        if SIGNATURE not in body:
            continue
        slug = f[:-5]
        s = open(INDEX, encoding='utf-8').read()
        s = re.sub(r'\s*<a class="blog-card" href="/blog/%s\.html">.*?</a>' % re.escape(slug), '', s, flags=re.S)
        open(INDEX, 'w', encoding='utf-8').write(s)
        fd = open(FEED, encoding='utf-8').read()
        fd = re.sub(r'\s*<item>(?:(?!</item>).)*?</item>',
                    lambda m: '' if slug in m.group(0) else m.group(0), fd, flags=re.S)
        open(FEED, 'w', encoding='utf-8').write(fd)
        os.remove(path)
        img = os.path.join(OG, slug + '.png')
        if os.path.exists(img):
            os.remove(img)
        print('force: removed', f)


# ---------------------------------------------------------------- main
def main():
    if not KEY:
        raise SystemExit('GEMINI_API_KEY is not set')

    if FORCE:
        cleanup_today()

    items = fetch_news()
    print('news items found:', len(items))
    item = pick_item(items)
    if not item:
        print('no fresh story — nothing to do')
        return
    print('chosen:', item['title'], '|', item['source'])

    body_text = article_text(item['link'])
    post = gemini_text(build_prompt(item, body_text))

    slug = slugify(post.get('slug') or post['title'], 55)
    pubdate = datetime.date.today()
    fname = '%s-%s.html' % (pubdate.isoformat(), slug)
    if os.path.exists(os.path.join(BLOG, fname)):
        print('post already exists:', fname)
        return

    img_name = '%s-%s.png' % (pubdate.isoformat(), slug)
    img_w, img_h = 1200, 630
    try:
        data = gemini_image(post.get('image_prompt') or (
            'a natural, photorealistic editorial image for a news story about: ' + post['title'] +
            '. Wide 16:9, no text.'))
        if data:
            img_w, img_h = png_size(data)
            open(os.path.join(OG, img_name), 'wb').write(data)
            print('image written:', img_name, img_w, 'x', img_h)
        else:
            img_name = ''
    except Exception as e:
        print('image generation failed (post still published):', e)
        img_name = ''

    html_doc = render_post(post, item, img_name, img_w, img_h, pubdate)
    open(os.path.join(BLOG, fname), 'w', encoding='utf-8').write(html_doc)
    print('post written:', fname)

    update_index(post, '%s-%s' % (pubdate.isoformat(), slug), img_name, pubdate)
    update_feed(post, '%s-%s' % (pubdate.isoformat(), slug), pubdate)
    mark_used(item['link'])
    print('done')


if __name__ == '__main__':
    main()
