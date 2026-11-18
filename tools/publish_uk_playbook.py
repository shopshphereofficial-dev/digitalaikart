#!/usr/bin/env python3
"""Publish the UK Study Visa & Graduate Route Playbook 2027 to the site.

Idempotent: re-running changes nothing if the entry already exists.
- inserts the product card at the top of products/index.html
- appends the entry to products.json (never touches existing entries)
- appends the product URL to sitemap.xml (never touches existing entries)
"""
import json
import os
import sys

SLUG = "uk-student-visa-graduate-route-playbook-2027"
URL = "/products/%s/" % SLUG
ABS = "https://digitalkartai.shop/products/%s/" % SLUG

CARD = """<div class="card">
    <div class="card-img" style="background:linear-gradient(135deg,#0a1628 0%,#16273f 100%);display:flex;align-items:center;justify-content:center"><span class="card-badge">NEW</span><span style="color:#c9a227;font-weight:700;font-size:1rem;line-height:1.35;text-align:center;padding:1.6rem;letter-spacing:0.01em">UK STUDY VISA<br>&amp; GRADUATE<br>ROUTE 2027</span></div>
    <div class="card-body">
      <h3 class="card-title">The UK Study Visa &amp; Graduate Route Playbook 2027 &mdash; Indian Student Edition</h3>
      <p class="card-desc">A 50-page working playbook on the UK Student visa as it stands in November 2026. It opens with the two changes most applicants have not caught up with: from 30 November 2026 the money you must show rises to GBP 1,570 a month in London and GBP 1,203 outside London, and from 1 January 2027 the Graduate Route drops from two years to 18 months, with a two-year exception for &ldquo;high compliance&rdquo; universities that the Autumn Budget announced but has not defined. Then the arithmetic, worked four ways with the 28-day and 31-day clocks mapped onto a calendar, in rupees at Rs 123.5 to the pound. Then the application: the document set, ATAS, the TB certificate, the B2 English rule, the IHS calculation, the credibility interview and the ten refusal reasons with the fix for each. Then what happens after you land &mdash; the eVisa, the 20-hour work condition and its self-employment trap, the Graduate Route timing that buys six months, the GBP 33,400 new entrant route to Skilled Worker, and four letters that ask a university for money.</p>
      <ul class="card-features">
        <li>The 30 November 2026 funds rise, before and after, in pounds and rupees</li>
        <li>Four worked fund calculations, with the nine-month cap and deposit offset</li>
        <li>The 28-day clock mapped onto five real application dates</li>
        <li>The credibility interview questions and the answers that work</li>
        <li>Graduate Route 18 months vs 2 years, and the Skilled Worker switch</li>
        <li>Seven printable worksheets and four scholarship negotiation letters</li>
      </ul>
      <div class="price-row"><span class="price">&#8377;199</span><span class="price-old">&#8377;1,199</span><span class="price-label">one-time</span></div>
      <a href="{{URL}}" class="btn btn-gold">View Details &rarr;</a>
    </div>
  </div>
""".replace("{{URL}}", URL)

ENTRY = {
    "slug": SLUG,
    "name": "The UK Study Visa & Graduate Route Playbook 2027 \u2014 Indian Student Edition",
    "tagline": (
        "The complete 50-page playbook for Indian students going to the UK in 2027, written after the rules "
        "changed twice. The money first: from 30 November 2026 a Student visa applicant must show GBP 1,570 a "
        "month in London and GBP 1,203 outside London, up from GBP 1,529 and GBP 1,171 under statement of "
        "changes HC 584, with the accommodation deposit offset capped at GBP 1,570, the nine-month maximum at "
        "GBP 14,130 and GBP 10,827, and the whole stack in rupees at Rs 123.5 to the pound including the GBP 558 "
        "visa fee and the GBP 776 student Immigration Health Surcharge. Then the clock: the 28 days the money "
        "must sit still, counted backwards from the closing balance, ending no more than 31 days before you "
        "apply, mapped onto five real application dates, with the four ways people break the window, what counts "
        "as acceptable funds and what does not, the parent consent letter, the loan conditions that decide "
        "whether an education loan is usable, and four worked fund calculations. Then the application: the "
        "document set, ATAS for sensitive postgraduate subjects, the TB certificate from a Home Office approved "
        "clinic valid six months from the x-ray, the B2 English rule in all four components, the IHS calculation, "
        "biometrics and the eVisa, the credibility interview questions and the answers that work, the ten refusal "
        "reasons with the fix for each, and how to classify a refusal before you act on it. Then the part that "
        "decides whether the degree pays: the Graduate Route at two years for applications made on or before "
        "31 December 2026 and 18 months from 1 January 2027, three years for PhD graduates, the GBP 937 fee and "
        "the IHS on that route, the two-year exception for high compliance universities announced in the 2026 "
        "Autumn Budget and still undefined, the 20-hour term-time work condition and its self-employment trap, "
        "the GBP 33,400 new entrant floor and GBP 41,700 general threshold for Skilled Worker with the four-year "
        "discount clock, and an honest chapter on settlement. Then the money back: Chevening's 2027-28 timeline, "
        "GREAT Scholarships at GBP 10,000 to GBP 13,000 with their March and May 2027 deadlines, the automatic "
        "university awards worth GBP 8,000 at Newcastle, Bath, Regent's and Dundee, and four letters that ask a "
        "university for a fee reduction. Seven printable worksheets, a 16-term glossary, and every source named "
        "and dated. Facts traced to GOV.UK, the Home Office fee tables of 8 October 2026, statement of changes "
        "HC 584 of 3 September 2026, the Graduate visa pages, the Skilled Worker guidance and the RBI reference "
        "rate of 17 November 2026."
    ),
    "price": "\u20b9199",
    "mrp": "\u20b91,199",
    "url": URL,
    "topics": [
        "study in UK 2027",
        "UK student visa",
        "student visa requirements India",
        "UK study visa funds",
        "28 day rule student visa",
        "maintenance funds UK visa",
        "GBP 1570 London maintenance",
        "student visa 30 November 2026",
        "HC 584 immigration rules",
        "Graduate Route 2027",
        "graduate visa 18 months",
        "post study work UK",
        "high compliance universities graduate route",
        "UK student visa fee",
        "immigration health surcharge students",
        "IHS calculation",
        "CAS confirmation of acceptance for studies",
        "credibility interview UK visa",
        "UK visa refusal reasons",
        "ATAS certificate",
        "TB test UK visa India",
        "B2 English requirement student visa",
        "eVisa UKVI account",
        "20 hours work student visa",
        "Skilled Worker visa new entrant",
        "GBP 33400 salary threshold",
        "switch student to skilled worker",
        "UK scholarships Indian students",
        "GREAT scholarships 2027",
        "Chevening 2027",
        "UK tuition discount negotiation",
        "study abroad playbook PDF",
        "UK study checklist",
    ],
}


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def add_card(root):
    path = os.path.join(root, "products", "index.html")
    html = read(path)
    if URL in html:
        print("card: already present")
        return False
    marker = '<div class="product-grid">'
    if marker not in html:
        raise SystemExit("card: product-grid marker not found")
    html = html.replace(marker, marker + "\n" + CARD, 1)
    write(path, html)
    print("card: inserted at top of product grid")
    return True


def add_json(root):
    path = os.path.join(root, "products.json")
    raw = read(path)
    data = json.loads(raw)
    slugs = [p.get("slug") for p in data.get("products", [])]
    if SLUG in slugs:
        print("products.json: already present")
        return False
    idx = raw.rindex("\n ]\n}")
    block = json.dumps(ENTRY, indent=1, ensure_ascii=True)
    block = "\n".join("  " + line for line in block.split("\n"))
    new = raw[:idx] + ",\n" + block + raw[idx:]
    check = json.loads(new)
    if check["products"][-1]["slug"] != SLUG or len(check["products"]) != len(slugs) + 1:
        raise SystemExit("products.json: append validation failed")
    write(path, new)
    print("products.json: appended entry, %d products" % len(check["products"]))
    return True


def add_sitemap(root):
    path = os.path.join(root, "sitemap.xml")
    xml = read(path)
    if ABS in xml:
        print("sitemap: already present")
        return False
    line = ('<url><loc>%s</loc><lastmod>2026-11-18</lastmod>'
            '<changefreq>weekly</changefreq><priority>0.9</priority></url>\n' % ABS)
    if "</urlset>" not in xml:
        raise SystemExit("sitemap: urlset not found")
    xml = xml.replace("</urlset>", line + "</urlset>", 1)
    write(path, xml)
    print("sitemap: appended product URL")
    return True


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    changed = [add_card(root), add_json(root), add_sitemap(root)]
    print("changed:", any(changed))
