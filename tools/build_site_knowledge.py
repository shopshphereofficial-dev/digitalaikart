#!/usr/bin/env python3
"""
Digitalaikart — site knowledge builder.

Scans the repository and writes site-knowledge.json, a single machine-readable
file describing EVERYTHING currently on digitalkartai.shop: products (from
products.json AND the /products/ pages), blog posts, downloadable playbooks,
and site pages (policies, AI page, etc.).

Run automatically by .github/workflows/build-site-knowledge.yml on every push,
so the website help bot always has up-to-date knowledge.

Usage:  python3 tools/build_site_knowledge.py [repo_root]
"""
import os, re, json, sys, html, datetime

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
SITE = "https://digitalkartai.shop"


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def meta(html_text, attr, name):
    """<meta name="description" content="..."> or <meta property="og:title" ...>"""
    pat = r'<meta\s+%s=["\']%s["\']\s+content=["\'](.*?)["\']' % (attr, re.escape(name))
    m = re.search(pat, html_text, re.I | re.S)
    if not m:
        pat = r'<meta\s+content=["\'](.*?)["\']\s+%s=["\']%s["\']' % (attr, re.escape(name))
        m = re.search(pat, html_text, re.I | re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def title_of(html_text):
    m = re.search(r"<title>(.*?)</title>", html_text, re.I | re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def all_meta(html_text, attr, name):
    pat = r'<meta\s+%s=["\']%s["\']\s+content=["\'](.*?)["\']' % (attr, re.escape(name))
    return [html.unescape(x).strip() for x in re.findall(pat, html_text, re.I | re.S)]


# ---------------------------------------------------------------- products ---
def load_products():
    raw = read(os.path.join(ROOT, "products.json"))
    by_slug = {}
    meta_note = ""
    if raw:
        try:
            data = json.loads(raw)
            meta_note = data.get("note", "")
            for p in data.get("products", []):
                slug = (p.get("slug") or "").strip()
                if not slug:
                    continue
                by_slug[slug] = {
                    "slug": slug,
                    "name": p.get("name", "").strip(),
                    "tagline": strip_tags(p.get("tagline", "")),
                    "price": str(p.get("price", "")).strip(),
                    "mrp": str(p.get("mrp", "")).strip(),
                    "url": p.get("url") or ("/products/%s/" % slug),
                    "also": strip_tags(p.get("also_available", "")),
                    "topics": p.get("topics", []) or [],
                    "source": "products.json",
                }
        except json.JSONDecodeError as e:
            print("WARN: products.json invalid JSON:", e, file=sys.stderr)

    # every product page on disk (some are not (yet) listed in products.json)
    pdir = os.path.join(ROOT, "products")
    if os.path.isdir(pdir):
        for slug in sorted(os.listdir(pdir)):
            page = os.path.join(pdir, slug, "index.html")
            if not os.path.isfile(page):
                continue
            h = read(page)
            desc = meta(h, "name", "description") or meta(h, "property", "og:description")
            t = title_of(h)
            t = re.sub(r"\s*[|\-—]\s*Digitalaikart.*$", "", t).strip() or slug
            price = ""
            m = re.search(r'class=["\']price["\'][^>]*>\s*([^<]+)', h)
            if m:
                price = strip_tags(m.group(1))
            if slug in by_slug:
                by_slug[slug]["title"] = t
                by_slug[slug]["summary"] = desc
                if not by_slug[slug]["price"] and price:
                    by_slug[slug]["price"] = price
            else:
                by_slug[slug] = {
                    "slug": slug,
                    "name": t,
                    "tagline": desc,
                    "summary": desc,
                    "price": price,
                    "mrp": "",
                    "url": "/products/%s/" % slug,
                    "also": "",
                    "topics": [],
                    "source": "product page",
                }
    return list(by_slug.values()), meta_note


# ------------------------------------------------------------------- blogs ---
def load_blogs():
    out = []
    bdir = os.path.join(ROOT, "blog")
    if not os.path.isdir(bdir):
        return out
    for fn in sorted(os.listdir(bdir)):
        if not fn.endswith(".html") or fn == "index.html":
            continue
        h = read(os.path.join(bdir, fn))
        if not h:
            continue
        title = meta(h, "property", "og:title") or title_of(h)
        summary = meta(h, "name", "description") or meta(h, "property", "og:description")
        date = meta(h, "property", "article:published_time") or meta(h, "property", "article:modified_time")
        if not date:
            m = re.match(r"(\d{4}-\d{2}-\d{2})", fn)
            date = m.group(1) if m else ""
        section = meta(h, "property", "article:section")
        tags = all_meta(h, "property", "article:tag")
        out.append({
            "title": title,
            "url": "/blog/%s" % fn,
            "date": date,
            "section": section,
            "tags": tags,
            "summary": summary,
        })
    # newest first
    out.sort(key=lambda b: b.get("date") or "", reverse=True)
    return out


# --------------------------------------------------------------- downloads ---
def load_downloads():
    out = []
    ddir = os.path.join(ROOT, "downloads")
    if not os.path.isdir(ddir):
        return out
    for fn in sorted(os.listdir(ddir)):
        if not fn.lower().endswith(".pdf"):
            continue
        title = re.sub(r"[-_]+", " ", fn[:-4]).strip()
        title = re.sub(r"\s+", " ", title).title()
        out.append({"title": title, "url": "/downloads/%s" % fn})
    return out


# ------------------------------------------------------------------- pages ---
def load_pages():
    pages = [
        ("/", "index.html"),
        ("/ai/", "ai/index.html"),
        ("/ai/plans.html", "ai/plans.html"),
        ("/privacy-policy.html", "privacy-policy.html"),
        ("/refund-policy.html", "refund-policy.html"),
        ("/terms.html", "terms.html"),
        ("/thank-you.html", "thank-you.html"),
        ("/sitemap.html", "sitemap.html"),
    ]
    out = []
    for url, rel in pages:
        h = read(os.path.join(ROOT, rel))
        if not h:
            continue
        out.append({
            "url": url,
            "title": title_of(h),
            "summary": meta(h, "name", "description") or meta(h, "property", "og:description"),
        })
    return out


# -------------------------------------------------------------------- apps ---
def load_apps():
    raw = read(os.path.join(ROOT, "apps.json"))
    out = []
    if raw:
        try:
            data = json.loads(raw)
            for a in data.get("apps", []):
                slug = (a.get("slug") or "").strip()
                if not slug:
                    continue
                out.append({
                    "slug": slug,
                    "name": a.get("name", "").strip(),
                    "tagline": a.get("tagline", "").strip(),
                    "category": a.get("category", "").strip(),
                    "price": str(a.get("price", "Free")).strip(),
                    "platform": a.get("platform", "Android"),
                    "tags": a.get("tags", []) or [],
                    "features": a.get("features", []) or [],
                    "url": "/apps/%s/" % slug,
                    "downloads": [d.get("url") for d in (a.get("downloads") or []) if d.get("url")],
                })
        except json.JSONDecodeError as e:
            print("WARN: apps.json invalid JSON:", e, file=sys.stderr)
    return out


# -------------------------------------------------------------------- site ---
SITE_FACTS = {
    "name": "Digitalaikart",
    "domain": "digitalkartai.shop",
    "what": ("Digitalaikart is an Indian digital-products store selling instant-download "
             "AI guides, career/study playbooks and ebooks. Payment is via UPI/secure "
             "checkout. Digital products are delivered by instant download; a printed "
             "combo is available for the GPT-6 Astra Guide."),
    "contact": {
        "whatsapp": "+91 96826 00301",
        "email": "lonefaisal977@gmail.com",
    },
    "how_to_buy": ("Open a product page, tap Buy, pay via the secure UPI checkout, then "
                   "you land on the thank-you page where your download link appears."),
    "how_to_download": ("After a successful purchase you are taken to /thank-you.html, "
                        "which contains the download link(s). Links also reach you by "
                        "email/WhatsApp if you share contact details at checkout."),
    "refund": ("Digital products are generally non-refundable once downloaded. If a file "
               "is broken or the wrong item was delivered, contact us on WhatsApp "
               "+91 96826 00301 or email lonefaisal977@gmail.com and it is fixed or refunded."),
    "shipping": ("Most products are digital (no shipping). The GPT-6 Astra Guide also has a "
                 "Digital + Printed combo at Rs 1,999; printed copies are shipped within India "
                 "and take a few working days."),
    "payment": "Secure UPI / online checkout in Indian Rupees (INR).",
    "paid_ai": {
        "name": "Digitalaikart AI",
        "url": "/ai/",
        "plans_url": "/ai/plans.html",
        "desc": ("Digitalaikart AI is the store's own Gemini-powered chat assistant for "
                 "general questions (AI, tech, career, study, business). It has a free tier "
                 "and paid plans; see /ai/plans.html for current plans and pricing."),
    },
    "free_help_bot": ("This help bot answers questions about the website itself: products, "
                      "prices, downloads, policies, blog articles and our own Android apps. For "
                      "anything else, it points you to Digitalaikart AI at /ai/."),
    "apps": ("Digitalaikart also publishes its own Android apps (free and premium) at /apps/ — "
             "games, tools, media apps and AI utilities. Each app has its own page with details, "
             "screenshots and a download link."),
}


def main():
    products, note = load_products()
    blogs = load_blogs()
    downloads = load_downloads()
    pages = load_pages()
    apps = load_apps()

    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    doc = {
        "generated": now,
        "generated_note": ("Auto-generated by tools/build_site_knowledge.py — do not edit by "
                           "hand. Regenerated on every push to main."),
        "site": SITE_FACTS,
        "counts": {
            "products": len(products),
            "blogs": len(blogs),
            "downloads": len(downloads),
            "pages": len(pages),
            "apps": len(apps),
        },
        "products": products,
        "blogs": blogs,
        "downloads": downloads,
        "pages": pages,
        "apps": apps,
    }
    out = os.path.join(ROOT, "site-knowledge.json")

    # Idempotent: if nothing but the "generated" timestamp would change, leave the
    # file untouched so the CI job does not create an empty commit on every run.
    if os.path.exists(out):
        try:
            with open(out, "r", encoding="utf-8") as f:
                old = json.load(f)
            old_body = {k: v for k, v in old.items() if k != "generated"}
            new_body = {k: v for k, v in doc.items() if k != "generated"}
            if old_body == new_body:
                print("site-knowledge.json unchanged — not rewritten "
                      "(products=%d blogs=%d downloads=%d pages=%d apps=%d)"
                      % (len(products), len(blogs), len(downloads), len(pages), len(apps)))
                return
        except (OSError, ValueError):
            pass

    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    size = os.path.getsize(out)
    print("wrote %s (%.1f KB) — products=%d blogs=%d downloads=%d pages=%d"
          % (out, size / 1024, len(products), len(blogs), len(downloads), len(pages)))


if __name__ == "__main__":
    main()
