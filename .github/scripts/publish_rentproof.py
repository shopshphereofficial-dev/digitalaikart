#!/usr/bin/env python3
"""Publish the RentProof catalogue entries.

Idempotent: run it as many times as you like. It appends the product to
products.json and product-history.json, adds the download mapping to
thank-you.html, the URL to sitemap.xml and the card to products/index.html —
but only where the slug is not already present.
"""
import json
import pathlib
import re
import sys

SLUG = "rentproof-rent-receipt-hra-india"
DATE = "2026-11-02"

ENTRY = {
    "slug": SLUG,
    "name": "RentProof — Rent Receipt & HRA Exemption Kit (Offline Web App)",
    "tagline": (
        "A working rent-receipt and HRA tool in a single HTML file. Enter the year, the rent, "
        "the city and the landlord once, and it prints twelve rent receipts — April to March, "
        "numbered consecutively, two to an A4 page — each with the landlord's PAN, the full "
        "property address, the period, the amount in figures and in words using Indian numbering, "
        "the payment mode and bank or UPI reference, the date of receipt, a signature block and a "
        "Re 1 revenue-stamp box only where cash rent exceeds Rs 5,000 a month. Change any month's "
        "amount for a mid-year hike, or set a month to zero for a month the flat was empty, and the "
        "annual total follows. Then the HRA exemption under Section 10(13A) as the least of three "
        "amounts — actual HRA received, rent paid less one-tenth of salary, and 50% or 40% of "
        "salary — with each limit shown, the deciding one marked and the taxable balance given. "
        "The 50% limit follows Rule 279 of the Income-tax Rules 2026 from tax year 2026-27, so it "
        "covers Mumbai, Kolkata, Delhi, Chennai, Hyderabad, Pune, Ahmedabad and Bengaluru, and "
        "falls back to the four old metros under Rule 2A for 2025-26 and earlier. Section 80GG is "
        "computed the same way for salaries with no HRA, with the Rs 60,000 cap and the ownership "
        "check. It also prints a rent summary sheet and an HRA working sheet, generates a landlord "
        "no-PAN declaration for the Rs 1,00,000 threshold, keeps a ten-item document checklist, and "
        "exports everything to one JSON file. No sign-up, no subscription, no internet needed, and "
        "your salary and the landlord's PAN never leave the browser. It is a calculator and a "
        "document generator: it does not file anything, does not verify that rent was paid, and is "
        "not tax advice."
    ),
    "price": "₹199",
    "mrp": "₹699",
    "url": f"/products/{SLUG}/",
    "also_available": [
        "payslip-pro-india",
        "income-tax-act-2025-playbook-2026-27",
        "staffkit-hr-letters-india",
    ],
    "topics": [
        "rent receipt", "rent receipt generator", "HRA", "HRA exemption", "house rent allowance",
        "Section 10(13A)", "Rule 279", "Rule 2A", "HRA calculator", "HRA calculation",
        "rent receipt for HRA", "landlord PAN", "landlord PAN required", "rent above 1 lakh",
        "Form 12BB", "Form 124", "Form 10BA", "Section 80GG", "80GG deduction", "revenue stamp",
        "rent agreement", "rent paid proof", "investment proof", "tax saving", "salary tax",
        "old tax regime", "metro city HRA", "50% HRA", "40% HRA", "Bengaluru HRA",
        "Hyderabad HRA", "Pune HRA", "Ahmedabad HRA", "Mumbai HRA", "Delhi HRA", "Chennai HRA",
        "Kolkata HRA", "Gurugram HRA", "Noida HRA", "ITR HRA", "income tax India",
        "salaried employee", "tenant", "rented flat", "printable receipt", "offline tool",
        "rent proof", "India",
    ],
}

FEATURES = [
    "Single self-contained HTML file (66 KB) — opens in any modern browser, works fully offline, no install and no account",
    "Twelve rent receipts for the financial year, April to March, numbered consecutively from a prefix and starting number you choose",
    "Two receipts per A4 page with a print stylesheet that forces a clean light layout; twelve months come to six pages",
    "Each receipt carries tenant, tenant PAN, landlord, landlord PAN, full property address, period, amount in figures and in words, mode, optional bank/UPI reference, date of receipt and a signature block",
    "Amounts in words in Indian numbering (lakh, crore, paise) — Twenty Two Thousand Rupees Only, not a Western grouping",
    "Per-month amounts: a mid-year hike is edited in place, and a month set to zero drops out of the annual total",
    "Landlord PAN watch: the annual total is tracked as you type and the PAN is flagged as required the moment it crosses ₹1,00,000, with a format check (ABCDE1234F)",
    "Revenue-stamp box printed only when the mode is cash and the month exceeds ₹5,000 — no box for bank transfer, UPI or cheque",
    "HRA exemption under Section 10(13A) as the least of three amounts, with each limit shown, the deciding limit marked and the taxable balance given",
    "Rule 279 of the Income-tax Rules 2026 from tax year 2026-27: 50% for Mumbai, Kolkata, Delhi, Chennai, Hyderabad, Pune, Ahmedabad and Bengaluru, 40% elsewhere",
    "Rule 2A for tax year 2025-26 and earlier: 50% for the four old metros only; the app switches with the financial year you select",
    "City aliases handled (Bangalore/Bengaluru, Bombay/Mumbai, Calcutta/Kolkata, Madras/Chennai, New Delhi/Delhi); Gurugram, Noida and Kochi stay at 40%",
    "Salary base is basic + DA only, never gross salary or CTC, with that point made on the screen and in the print sheet",
    "Section 80GG for salaries with no HRA: ₹5,000-a-month cap, 25% of adjusted total income, rent less 10% of income, with an explicit refusal if you own a house where you work",
    "Indicative tax saved at a chosen marginal rate, labelled as indicative and old-regime only",
    "Printable rent summary sheet with the month-by-month table, annual total and the HRA working on one page",
    "Printable HRA working sheet with the inputs, the three limits, the exempt and taxable figures and the rule cited",
    "Landlord no-PAN declaration generator for the ₹1,00,000 threshold, ready to sign, with the reason and Aadhaar line",
    "Ten-item document checklist with saved progress and the three patterns that get an HRA claim reopened (relative landlord without a real tenancy, cash with no trail, gross salary as the base)",
    "JSON export and import of everything entered, plus a labelled sample data file and a reset",
    "Responsive layout with tabs that scroll on phones; no external fonts, scripts, trackers or network calls",
    "Pack: RentProof.html, 11-section USER-GUIDE.html, START-HERE.txt, sample-data.json and a 12-clause LICENSE.txt",
    "133 automated checks passed before publication: 78 on the calculation core (amount in words, city percentages, the three HRA limits, 80GG, receipt generation, PAN validation) and 55 on the interface in a DOM",
    "Razorpay payment link wired to the thank-you page download for this slug",
]

HISTORY = {
    "date": DATE,
    "name": ENTRY["name"],
    "slug": SLUG,
    "category": "Offline Web App / Rent Receipts, HRA & 80GG Calculation",
    "type": "webapp",
    "price": "₹199",
    "mrp": "₹699",
    "url": f"https://digitalkartai.shop/products/{SLUG}/",
    "download": f"https://digitalkartai.shop/downloads/{SLUG}.zip",
    "payment_link": "https://rzp.io/rzp/rE1WwqJ",
    "status": "published",
    "features": FEATURES,
}

CARD = """<div class="card">
    <div class="card-img" style="background:linear-gradient(135deg,#0a1628 0%,#16273f 100%);display:flex;align-items:center;justify-content:center"><span class="card-badge">72% OFF</span><span style="color:#c9a227;font-weight:700;font-size:1rem;line-height:1.35;text-align:center;padding:1.6rem;letter-spacing:0.01em">RENTPROOF<br>12 RENT RECEIPTS<br>+ HRA WORKING</span></div>
    <div class="card-body">
      <h3 class="card-title">RentProof &mdash; Rent Receipt &amp; HRA Exemption Kit</h3>
      <p class="card-desc">Twelve print-ready rent receipts for the financial year and the HRA exemption worked out to the rupee, in one offline HTML file. April to March, numbered, two to an A4 page, each with the landlord PAN, the full property address, the amount in words and a revenue stamp box only where cash rent needs one. The exemption follows Rule 279 for 2026-27 &mdash; 50% for Mumbai, Kolkata, Delhi, Chennai, Hyderabad, Pune, Ahmedabad and Bengaluru &mdash; with Section 80GG, a no-PAN declaration and a ten-item document checklist.</p>
      <ul class="card-features">
        <li>12 receipts, two per A4 page</li>
        <li>HRA: least of three, binding limit marked</li>
        <li>Eight-city 50% rule for 2026-27</li>
        <li>80GG, no-PAN declaration, checklist</li>
        <li>Offline HTML app &middot; no sign-up</li>
      </ul>
      <div class="price-row"><span class="price">&#8377;199</span><span class="price-old">&#8377;699</span><span class="price-label">one-time</span></div>
      <a href="/products/__SLUG__/" class="btn btn-gold">View Details &rarr;</a>
    </div>
  </div>
""".replace("__SLUG__", SLUG)


def read(path):
    return pathlib.Path(path).read_text(encoding="utf-8")


def write(path, text):
    pathlib.Path(path).write_text(text, encoding="utf-8")


def main():
    changed = []

    # 1. products.json
    data = json.loads(read("products.json"))
    if any(p.get("slug") == SLUG for p in data["products"]):
        print("products.json: already present")
    else:
        data["products"].append(ENTRY)
        data["updated"] = DATE
        write("products.json", json.dumps(data, ensure_ascii=False, indent=1) + "\n")
        changed.append("products.json")
        print("products.json: appended (%d products)" % len(data["products"]))

    # 2. product-history.json
    hist = json.loads(read("product-history.json"))
    if any(h.get("slug") == SLUG for h in hist["history"]):
        print("product-history.json: already present")
    else:
        hist["history"].append(HISTORY)
        hist["updated"] = DATE
        write("product-history.json", json.dumps(hist, ensure_ascii=False, indent=1) + "\n")
        changed.append("product-history.json")
        print("product-history.json: appended (%d entries)" % len(hist["history"]))

    # 3. thank-you.html download map
    ty = read("thank-you.html")
    if SLUG in ty:
        print("thank-you.html: already mapped")
    else:
        anchor = "'staffkit-hr-letters-india':'/downloads/staffkit-hr-letters-india.zip'}"
        if anchor not in ty:
            sys.exit("thank-you.html: download map anchor not found — refusing to guess")
        ty = ty.replace(
            anchor,
            "'staffkit-hr-letters-india':'/downloads/staffkit-hr-letters-india.zip',"
            "'%s':'/downloads/%s.zip'}" % (SLUG, SLUG),
            1,
        )
        write("thank-you.html", ty)
        changed.append("thank-you.html")
        print("thank-you.html: download mapping added")

    # 4. sitemap.xml
    sm = read("sitemap.xml")
    if f"products/{SLUG}/" in sm:
        print("sitemap.xml: already listed")
    else:
        m = re.search(
            r"<url><loc>https://digitalkartai\.shop/products/staffkit-hr-letters-india/</loc>"
            r"<lastmod>[^<]*</lastmod><changefreq>[^<]*</changefreq><priority>[^<]*</priority></url>",
            sm,
        )
        if not m:
            sys.exit("sitemap.xml: staffkit entry not found — refusing to guess")
        line = (
            "<url><loc>https://digitalkartai.shop/products/%s/</loc><lastmod>%s</lastmod>"
            "<changefreq>weekly</changefreq><priority>0.9</priority></url>" % (SLUG, DATE)
        )
        sm = sm[: m.end()] + "\n" + line + sm[m.end():]
        write("sitemap.xml", sm)
        changed.append("sitemap.xml")
        print("sitemap.xml: entry added")

    # 5. products/index.html card
    idx = read("products/index.html")
    if f"/products/{SLUG}/" in idx:
        print("products/index.html: card already present")
    else:
        grid = '<div class="product-grid">'
        if idx.count(grid) != 1:
            sys.exit("products/index.html: product grid not found exactly once — refusing to guess")
        idx = idx.replace(grid, grid + "\n  " + CARD, 1)
        write("products/index.html", idx)
        changed.append("products/index.html")
        print("products/index.html: card added")

    # verify
    json.loads(read("products.json"))
    json.loads(read("product-history.json"))
    assert f"/products/{SLUG}/" in read("products/index.html")
    assert SLUG in read("thank-you.html")
    print("CHANGED:", ", ".join(changed) if changed else "(nothing — already published)")


if __name__ == "__main__":
    main()
