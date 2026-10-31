#!/usr/bin/env python3
"""
Site fixes for digitalkartai.shop.

1. Legal entity — makes UTILITYNEST (the registered MSME / Udyam entity) the
   clearly stated operating entity everywhere:
     * a legal-entity line in the footer of every page
     * both official support WhatsApp numbers
     * an About link in the footer navigation
     * "a brand of UTILITYNEST" in the copyright line
     * an operator paragraph on the three policy pages
     * a footer for /ai/ (which had none) and both numbers on /thank-you.html

2. Bug fixes:
     * blog posts that pointed their cover/og:image at an empty
       "https://digitalkartai.shop/assets/og/" URL now use a real image
     * three product pages whose cover.jpg was never uploaded now use the
       brand image instead of a broken thumbnail
     * the GCC fresher playbook linked to /privacy.html, /refund.html and
       /contact.html, none of which exist — now the real policy pages
     * /about.html added to the help bot's page list

Idempotent: safe to run repeatedly.

Usage:  python3 tools/site_fixes.py [repo_root]
"""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

ENTITY_P = (
    '<p class="entity"><strong>Digitalaikart</strong> is a brand of '
    '<strong>UTILITYNEST</strong> \u2014 a registered MSME (Udyam, Govt. of India), '
    'Qazibagh, Ichgam, Budgam, Jammu &amp; Kashmir 191111 \u00b7 '
    '<a href="/about.html">About &amp; Contact</a></p>'
)

SUPPORT_P = (
    '<p class="entity-contact">Support: '
    '<a href="mailto:lonefaisal977@gmail.com">lonefaisal977@gmail.com</a> \u00b7 '
    'WhatsApp: <a href="https://wa.me/919682600301">+91 96826 00301</a>, '
    '<a href="https://wa.me/918492020923">+91 84920 20923</a></p>'
)

OPERATOR_P = (
    '<p class="updated"><strong>Operated by:</strong> UTILITYNEST, a registered micro '
    'enterprise (MSME / Udyam, Govt. of India), Qazibagh, Ichgam, Budgam, '
    'Jammu &amp; Kashmir 191111, India. <strong>Digitalaikart</strong> is the brand name '
    'under which UTILITYNEST sells its digital products. Founder / authorised '
    'representative: Faisal Fayaz Lone. Support: '
    '<a href="mailto:lonefaisal977@gmail.com">lonefaisal977@gmail.com</a>, WhatsApp '
    '<a href="https://wa.me/919682600301">+91 96826 00301</a> or '
    '<a href="https://wa.me/918492020923">+91 84920 20923</a>, '
    'Monday to Saturday, 9:30 AM to 6:30 PM IST.</p>'
)

AI_FOOTER = (
    '<footer style="max-width:900px;margin:2.5rem auto 1.5rem;padding:1rem 1.25rem;'
    'border-top:1px solid #e2e8f0;font-size:.82rem;line-height:1.7;color:#475569;text-align:center">'
    '<p><strong>Digitalaikart</strong> is a brand of <strong>UTILITYNEST</strong> \u2014 a registered '
    'MSME (Udyam, Govt. of India), Qazibagh, Ichgam, Budgam, Jammu &amp; Kashmir 191111.</p>'
    '<p>Support: <a href="mailto:lonefaisal977@gmail.com">lonefaisal977@gmail.com</a> \u00b7 WhatsApp '
    '<a href="https://wa.me/919682600301">+91 96826 00301</a>, '
    '<a href="https://wa.me/918492020923">+91 84920 20923</a> \u00b7 Mon\u2013Sat, 9:30 AM\u20136:30 PM IST</p>'
    '<p><a href="/about.html">About &amp; Contact</a> \u00b7 '
    '<a href="/privacy-policy.html">Privacy</a> \u00b7 '
    '<a href="/terms.html">Terms</a> \u00b7 '
    '<a href="/refund-policy.html">Refunds</a></p>'
    '<p>&copy; 2026 Digitalaikart, a brand of UTILITYNEST. All rights reserved.</p></footer>'
)

COPY_RE = re.compile(r"&copy;\s*(\d{4})\s*Digitalaikart\.\s*All rights reserved\.")
SECOND_NUMBER = ', <a href="https://wa.me/918492020923">+91 84920 20923</a>'
THANK_YOU_OLD = '<strong>+91 96826 00301</strong> on WhatsApp or email'
THANK_YOU_NEW = ('<strong>+91 96826 00301</strong> or <strong>+91 84920 20923</strong> '
                 'on WhatsApp or email')

BRAND_IMAGE = "/assets/og-default.png"
BROKEN_COVERS = {
    "/products/ai-prompt-pack-indian-travel-agents-2026-27/cover.jpg": BRAND_IMAGE,
    "/products/ai-prompt-pack-indian-interior-designers-2026-27/cover.jpg": BRAND_IMAGE,
    "/products/ai-safe-kids-playbook-india-2026-27/cover.jpg": BRAND_IMAGE,
    "/assets/products/ai-safe-kids-playbook-india-2026-27.jpg": BRAND_IMAGE,
}
GCC_PAGE = os.path.join("products", "gcc-fresher-playbook-2026-27", "index.html")
GCC_LINKS = {
    'href="/privacy.html"': 'href="/privacy-policy.html"',
    'href="/refund.html"': 'href="/refund-policy.html"',
    'href="/contact.html"': 'href="/about.html"',
}


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def html_files():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in (".git", ".github", "node_modules")]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(d, f)


def patch_footer(text):
    i = text.rfind("<footer")
    if i < 0:
        return text, False
    head, foot = text[:i], text[i:]
    if "UTILITYNEST" in foot:
        return text, False

    if "wa.me/919682600301" in foot and "84920" not in foot:
        foot = foot.replace('>+91 96826 00301</a>', '>+91 96826 00301</a>' + SECOND_NUMBER, 1)

    if "/about.html" not in foot:
        foot = re.sub(
            r'(<div class="footer-links">)(.*?)(</div>)',
            lambda m: m.group(1) + m.group(2) + '<a href="/about.html">About</a>' + m.group(3),
            foot, count=1, flags=re.S,
        )

    foot = COPY_RE.sub(
        r"&copy; \1 Digitalaikart, a brand of UTILITYNEST. All rights reserved.", foot)

    block = ENTITY_P if "lonefaisal977@gmail.com" in foot else ENTITY_P + SUPPORT_P
    m = re.search(r'<p[^>]*>&copy;', foot)
    if m:
        foot = foot[:m.start()] + block + foot[m.start():]
    else:
        j = foot.find("</footer>")
        foot = foot[:j] + block + foot[j:] if j >= 0 else foot + block
    return head + foot, True


def patch_policies(path, text):
    name = os.path.basename(path)
    if name not in ("privacy-policy.html", "terms.html", "refund-policy.html"):
        return text, False
    if "Operated by:" in text:
        return text, False
    changed = False

    if name == "terms.html":
        old = "refers to Digitalaikart, operated by Faisal Fayaz Lone."
        new = ("refers to Digitalaikart, the brand of UTILITYNEST, a registered micro "
               "enterprise (MSME / Udyam, Govt. of India), Qazibagh, Ichgam, Budgam, "
               "Jammu &amp; Kashmir 191111, India, represented by its founder Faisal Fayaz Lone.")
        if old in text:
            text = text.replace(old, new, 1)
            changed = True

    if 'class="updated"' in text:
        text = re.sub(r'(<p class="updated">.*?</p>)',
                      lambda m: m.group(1) + "\n  " + OPERATOR_P,
                      text, count=1, flags=re.S)
        changed = True
    else:
        m = re.search(r"<h1>.*?</h1>", text, re.S)
        if m:
            text = text[:m.end()] + "\n  " + OPERATOR_P + text[m.end():]
            changed = True

    if "84920" not in text:
        text = text.replace("WhatsApp at +91 96826 00301",
                            "WhatsApp at +91 96826 00301 or +91 84920 20923")
        text = text.replace("+91 96826 00301</a>", "+91 96826 00301</a>" + SECOND_NUMBER)
        changed = True
    return text, changed


def patch_specials():
    """Pages that have no standard footer, plus the knowledge builder's page list."""
    done = []

    ai_page = os.path.join(ROOT, "ai", "index.html")
    t = read(ai_page)
    if t and "UTILITYNEST" not in t and "</body>" in t:
        write(ai_page, t.replace("</body>", AI_FOOTER + "\n</body>", 1))
        done.append("ai/index.html")

    ty = os.path.join(ROOT, "thank-you.html")
    t = read(ty)
    if t and THANK_YOU_NEW not in t and THANK_YOU_OLD in t:
        write(ty, t.replace(THANK_YOU_OLD, THANK_YOU_NEW, 1))
        done.append("thank-you.html")

    kb = os.path.join(ROOT, "tools", "build_site_knowledge.py")
    t = read(kb)
    if t and '"about.html"' not in t and '("/sitemap.html", "sitemap.html"),' in t:
        write(kb, t.replace('("/sitemap.html", "sitemap.html"),',
                            '("/about.html", "about.html"),\n        ("/sitemap.html", "sitemap.html"),', 1))
        done.append("tools/build_site_knowledge.py")

    return done


def patch_broken_images(path, text):
    """Empty /assets/og/ covers and product covers that were never uploaded."""
    if 'assets/og/"' in text:
        text = text.replace('https://digitalkartai.shop/assets/og/"',
                            'https://digitalkartai.shop' + BRAND_IMAGE + '"')
        text = text.replace('"/assets/og/"', '"' + BRAND_IMAGE + '"')
    for bad, good in BROKEN_COVERS.items():
        if bad in text:
            text = text.replace("https://digitalkartai.shop" + bad,
                                "https://digitalkartai.shop" + good)
            text = text.replace('"' + bad + '"', '"' + good + '"')
    return text


def main():
    touched, skipped = 0, 0
    for path in sorted(html_files()):
        text = read(path)
        if not text:
            continue
        new, changed = patch_policies(path, text)
        new, changed2 = patch_footer(new)
        new2 = patch_broken_images(path, new)
        changed3 = new2 != new
        if os.path.relpath(path, ROOT) == GCC_PAGE:
            for bad, good in GCC_LINKS.items():
                if bad in new2:
                    new2 = new2.replace(bad, good)
                    changed3 = True
        if changed or changed2 or changed3:
            write(path, new2)
            touched += 1
        else:
            skipped += 1

    specials = patch_specials()
    print("pages updated: %d, already fine / no footer: %d" % (touched, skipped))
    if specials:
        print("also patched:", ", ".join(specials))


if __name__ == "__main__":
    main()
