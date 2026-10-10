#!/usr/bin/env python3
"""
Digitalaikart — Apps store builder.

Reads apps.json and generates:
  /apps/index.html          the app-store listing (search + category filter)
  /apps/<slug>/index.html   one page per app

Uses the site's existing stylesheet (assets/style.css) and markup patterns so
the store matches the rest of digitalkartai.shop. Run by the GitHub Action
.github/workflows/build-apps.yml on every push that touches apps.json.

Usage: python3 tools/build_apps.py [repo_root]
"""
import os, re, json, sys, html, datetime

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
SITE = "https://digitalkartai.shop"

NAV = ('<nav class="nav"><div class="nav-inner"><a href="/" class="nav-logo">Digitalaikart</a>'
       '<div class="nav-links"><a href="/">Home</a><a href="/products/">Products</a>'
       '<a href="/apps/" class="active">Apps</a><a href="/ai/">AI Assistant</a><a href="/blog/">Blog</a>'
       '</div></div></nav>')

WA = ('<a href="https://wa.me/919682600301" class="whatsapp-float" target="_blank" rel="noopener" '
      'aria-label="Chat on WhatsApp"><svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967'
      '-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475'
      '-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.608.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497'
      '.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01'
      '-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487'
      '.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413'
      '-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374'
      'a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994'
      'c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945'
      'L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.488"/></svg></a>')

FOOTER = ('<footer><div class="footer-links"><a href="/">Home</a><a href="/products/">Products</a>'
          '<a href="/apps/">Apps</a><a href="/blog/">Blog</a><a href="/privacy-policy.html">Privacy Policy</a>'
          '<a href="/refund-policy.html">Refund Policy</a><a href="/terms.html">Terms &amp; Conditions</a>'
          '<a href="/sitemap.html">Site Map</a></div><p><strong>Digitalaikart</strong> &mdash; Premium AI Digital Products</p>'
          '<p>Feedback &amp; Inquiries: <a href="mailto:lonefaisal977@gmail.com">lonefaisal977@gmail.com</a> | '
          'WhatsApp: <a href="https://wa.me/919682600301">+91 96826 00301</a></p>'
          '<p style="margin-top:0.5rem;color:#334155">&copy; 2026 Digitalaikart. All rights reserved.</p></footer>'
          '<script src="/assets/effects.js"></script>')

FONTS = ('<link rel="icon" href="/favicon.ico" sizes="48x48">'
         '<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">'
         '<link rel="apple-touch-icon" href="/apple-touch-icon.png">')


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def initials(name):
    parts = re.findall(r"[A-Za-z0-9]+", name or "App")
    return (parts[0][:1] + (parts[1][:1] if len(parts) > 1 else "")).upper() or "A"


def icon_html(app, cls):
    if app.get("icon"):
        return '<div class="%s"><img src="%s" alt="%s icon"></div>' % (cls, esc(app["icon"]), esc(app["name"]))
    return '<div class="%s">%s</div>' % (cls, esc(initials(app.get("name", ""))))


def price_html(app):
    price = (app.get("price") or "Free").strip()
    if price.lower() in ("free", "0", ""):
        return '<span class="app-price free">Free</span>'
    return '<span class="app-price">%s</span>' % esc(price)


def head(title, desc, url, ld=None):
    og_img = SITE + "/assets/og-default.png"
    parts = [
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        FONTS,
        '<title>%s</title>' % esc(title),
        '<meta name="description" content="%s">' % esc(desc),
        '<meta property="og:title" content="%s">' % esc(title),
        '<meta property="og:description" content="%s">' % esc(desc),
        '<meta property="og:type" content="website">',
        '<meta property="og:url" content="%s">' % esc(url),
        '<meta property="og:site_name" content="Digitalaikart">',
        '<meta property="og:locale" content="en_IN">',
        '<meta property="og:image" content="%s">' % og_img,
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % esc(title),
        '<meta name="twitter:description" content="%s">' % esc(desc),
        '<meta name="twitter:image" content="%s">' % og_img,
        '<link rel="canonical" href="%s">' % esc(url),
        '<link rel="stylesheet" href="/assets/style.css">',
    ]
    if ld:
        parts.append('<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False))
    parts.append('</head><body>')
    return "".join(parts)


# ------------------------------------------------------------------ listing ---
def card(app):
    tags = "".join('<span class="app-tag">%s</span>' % esc(t) for t in (app.get("tags") or [])[:4])
    badge = ('<span class="app-badge">%s</span>' % esc(app["badge"])) if app.get("badge") else ""
    hay = (app.get("name", "") + " " + " ".join(app.get("tags") or []) + " " + app.get("category", "")).lower()
    return (
        '<div class="app-card-wrap" data-name="%s" data-cat="%s" data-hay="%s">%s'
        '<div class="app-card">'
        '<div class="app-card-top">%s<div><div class="app-name">%s</div><div class="app-cat">%s</div></div></div>'
        '<div class="app-card-body"><p class="app-desc">%s</p><div class="app-tags">%s</div>'
        '<div class="app-foot">%s<span style="font-size:.7rem;color:var(--text-muted)">%s</span></div>'
        '<a href="/apps/%s/" class="btn btn-gold">View app &rarr;</a>'
        '</div></div></div>'
    ) % (
        esc(app["name"]), esc(app.get("category", "")), esc(hay), badge,
        icon_html(app, "app-icon"), esc(app["name"]), esc(app.get("category", "")),
        esc(app.get("tagline", "")), tags, price_html(app), esc(app.get("platform", "Android")),
        esc(app["slug"]),
    )


def listing(apps):
    cats = []
    for a in apps:
        c = a.get("category")
        if c and c not in cats:
            cats.append(c)
    chips = '<button class="chip on" data-cat="">All</button>' + "".join(
        '<button class="chip" data-cat="%s">%s</button>' % (esc(c), esc(c)) for c in cats)
    cards = "".join(card(a) for a in apps)
    ld = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": "Digitalaikart Apps", "url": SITE + "/apps/",
        "description": "Free and premium Android apps by Digitalaikart — games, tools, media apps and AI utilities.",
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": "%s/apps/%s/" % (SITE, a["slug"]), "name": a["name"]}
            for i, a in enumerate(apps)]},
    }
    body = (
        head("Apps for Android — Digitalaikart",
             "Download our Android apps — games, tools, media apps and AI utilities. Free and premium, made by Digitalaikart.",
             SITE + "/apps/", ld)
        + NAV
        + '<header class="page-header"><h1>Apps</h1>'
          '<p>Our own Android apps &mdash; games, tools, media apps and AI utilities. Free and premium.</p></header>'
        + '<div class="app-filters">'
          '<input id="appSearch" class="app-search" type="search" placeholder="Search apps..." aria-label="Search apps">'
          + chips + '</div>'
        + '<div class="app-grid" id="appGrid">' + cards + '</div>'
        + '<div class="coming-soon" id="appEmpty" style="display:none">No apps match your search. <span>Try another word.</span></div>'
        + '<section class="final-cta"><h2>Want an app made for you?</h2>'
          '<p>We build custom Android apps. Tell us your idea and we&rsquo;ll make it.</p>'
          '<a href="https://wa.me/919682600301" class="btn btn-gold" target="_blank" rel="noopener">Ask on WhatsApp</a></section>'
        + WA + FOOTER
        + '<script>(function(){var s=document.getElementById("appSearch"),g=document.getElementById("appGrid"),'
          'cards=[].slice.call(g.querySelectorAll(".app-card-wrap")),chips=[].slice.call(document.querySelectorAll(".chip")),'
          'empty=document.getElementById("appEmpty"),cat="";'
          'function apply(){var q=(s.value||"").toLowerCase().trim(),n=0;cards.forEach(function(c){'
          'var ok=(!cat||c.getAttribute("data-cat")===cat)&&(!q||c.getAttribute("data-hay").indexOf(q)>-1);'
          'c.style.display=ok?"":"none";if(ok)n++;});empty.style.display=n?"none":"block";}'
          's.addEventListener("input",apply);chips.forEach(function(b){b.addEventListener("click",function(){'
          'chips.forEach(function(x){x.classList.remove("on")});b.classList.add("on");cat=b.getAttribute("data-cat");apply();});});'
          '})();</script>'
        + '</body></html>'
    )
    return body


# ------------------------------------------------------------------- detail ---
def download_buttons(app):
    dls = app.get("downloads") or []
    if not dls:
        return ('<div class="coming-soon" style="border:1px dashed var(--border);border-radius:12px;padding:1.1rem">'
                'Direct download is <span>coming soon</span> &mdash; message us on WhatsApp to get it early.</div>')
    out = []
    for d in dls:
        cls = "btn btn-gold" if d.get("style") != "outline" else "btn btn-outline"
        ext = ' target="_blank" rel="noopener"' if str(d.get("url", "")).startswith("http") else ""
        out.append('<a href="%s" class="%s"%s>%s</a>' % (esc(d["url"]), cls, ext, esc(d.get("label", "Download"))))
    return "".join(out)


def detail(app, all_apps):
    shots = app.get("screenshots") or []
    if shots:
        shot_html = '<div class="shot-strip">' + "".join(
            '<img src="%s" alt="%s screenshot">' % (esc(s), esc(app["name"])) for s in shots) + '</div>'
    else:
        shot_html = ('<div class="shot-strip">' + "".join(
            '<div class="shot-ph">Screenshot %d</div>' % (i + 1) for i in range(3)) + '</div>')

    video = app.get("video") or ""
    vid_html = ""
    m = re.search(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|shorts/))([A-Za-z0-9_-]{6,})", video)
    if m:
        vid_html = ('<section class="section"><h2 class="section-title">Preview</h2><div class="gold-divider"></div>'
                     '<div class="video-wrap"><iframe src="https://www.youtube.com/embed/%s" title="%s preview" '
                     'allowfullscreen loading="lazy"></iframe></div></section>') % (esc(m.group(1)), esc(app["name"]))

    feats = "".join('<div class="feature-card"><h4>%s</h4></div>' % esc(f) for f in (app.get("features") or []))
    feats_html = ('<section class="section"><h2 class="section-title">What you get</h2><div class="gold-divider"></div>'
                  '<div class="feature-grid">' + feats + '</div></section>') if feats else ""

    paras = "".join('<p>%s</p>' % esc(p) for p in (app.get("description") or "").split("\n\n") if p.strip())
    tags = "".join('<span class="app-tag">%s</span>' % esc(t) for t in (app.get("tags") or []))

    rel = [a for a in all_apps if a.get("category") == app.get("category") and a["slug"] != app["slug"]][:3]
    if len(rel) < 3:
        rel += [a for a in all_apps if a["slug"] != app["slug"] and a not in rel][:3 - len(rel)]
    rel_html = ""
    if rel:
        rel_html = ('<section class="section"><h2 class="section-title">More apps</h2><div class="gold-divider"></div>'
                    '<div class="app-grid">' + "".join(card(a) for a in rel) + '</div></section>')

    meta_bits = ['<div><b>%s</b>Platform</div>' % esc(app.get("platform", "Android"))]
    if app.get("version"):
        meta_bits.append('<div><b>%s</b>Version</div>' % esc(app["version"]))
    if app.get("size"):
        meta_bits.append('<div><b>%s</b>Size</div>' % esc(app["size"]))
    meta_bits.append('<div><b>%s</b>Price</div>' % esc(app.get("price", "Free")))

    ld = {
        "@context": "https://schema.org", "@type": "SoftwareApplication",
        "name": app["name"], "operatingSystem": "Android",
        "applicationCategory": app.get("category", "Utilities"),
        "description": (app.get("description") or app.get("tagline", "")).split("\n\n")[0],
        "url": "%s/apps/%s/" % (SITE, app["slug"]),
        "offers": {"@type": "Offer", "price": "0" if (app.get("price", "Free").lower() == "free") else re.sub(r"[^0-9.]", "", app.get("price", "")),
                   "priceCurrency": "INR"},
        "publisher": {"@type": "Organization", "name": "Digitalaikart", "url": SITE},
    }

    return (
        head("%s — Android app by Digitalaikart" % app["name"],
             (app.get("tagline") or "").strip(), "%s/apps/%s/" % (SITE, app["slug"]), ld)
        + NAV
        + '<div style="max-width:1000px;margin:0 auto;padding:6.5rem 1.5rem 0"><a href="/apps/" '
          'style="color:var(--gold);font-size:.8rem">&larr; All apps</a></div>'
        + '<section class="app-hero">'
          + icon_html(app, "app-hero-icon")
          + '<div class="app-info"><span class="eyebrow">' + esc(app.get("category", "App")) + '</span>'
          + '<h1>' + esc(app["name"]) + '</h1>'
          + '<p class="tagline">' + esc(app.get("tagline", "")) + '</p>'
          + '<div class="app-meta">' + "".join(meta_bits) + '</div>'
          + download_buttons(app)
          + '<div class="app-tags" style="margin-top:1rem">' + tags + '</div></div>'
        + '</section>'
        + '<section class="section"><h2 class="section-title">Screenshots</h2><div class="gold-divider"></div>'
          '<p class="section-sub">A look at the app</p>' + shot_html + '</section>'
        + vid_html
        + feats_html
        + '<section class="section"><h2 class="section-title">About this app</h2><div class="gold-divider"></div>'
          '<div style="max-width:720px;margin:0 auto;color:var(--text-secondary);font-size:.85rem">' + paras + '</div></section>'
        + rel_html
        + WA + FOOTER + '</body></html>'
    )


def update_sitemap(slugs):
    path = os.path.join(ROOT, "sitemap.xml")
    try:
        with open(path, "r", encoding="utf-8") as f:
            xml = f.read()
    except OSError:
        return
    add = []
    if SITE + "/apps/" not in xml:
        add.append(SITE + "/apps/")
    for s in slugs:
        u = "%s/apps/%s/" % (SITE, s)
        if u not in xml:
            add.append(u)
    if not add:
        return
    today = datetime.date.today().isoformat()
    block = "".join('<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq>'
                    '<priority>0.8</priority></url>' % (u, today) for u in add)
    xml = xml.replace("</urlset>", block + "</urlset>") if "</urlset>" in xml else xml + block
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)


def main():
    with open(os.path.join(ROOT, "apps.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    apps = [a for a in data.get("apps", []) if a.get("slug")]

    os.makedirs(os.path.join(ROOT, "apps"), exist_ok=True)
    with open(os.path.join(ROOT, "apps", "index.html"), "w", encoding="utf-8") as f:
        f.write(listing(apps))

    for a in apps:
        d = os.path.join(ROOT, "apps", a["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(detail(a, apps))

    update_sitemap([a["slug"] for a in apps])
    print("built apps store: %d apps -> /apps/ + %d detail pages" % (len(apps), len(apps)))


if __name__ == "__main__":
    main()
