# JEE Main 2027 Starter Handbook — resume notes (2026-09-20)

This product launch is ~90% complete but NOT published. The self-review gate passed; the blocker is only the binary PDF upload (see below). Live state: product page is a placeholder redirect to /products/, payment link plink_TeCJv6HvzqvxwT is CANCELLED, no card in products/index.html, no products.json entry, no sitemap entry. downloads/jee-main-2027-starter-handbook.pdf on main is a CORRUPT 30,000-byte placeholder and must be replaced.

## What is ready
- Deterministic build script (invariant CreationDate/ModDate, output MD5 321ad7ad6176704450bc207a3fc513cd, 90,983 bytes): agent workspace notes `jee-main-2027-starter-handbook-build.py` (re-run twice to confirm identical MD5).
- Final page HTML, card HTML, products.json entry, sitemap URL: committed under `.github/site-updates/` (jee-card.html, jee-products-entry.json, jee-sitemap-url.txt).
- Assembly workflow: `.github/workflows/assemble-jee-pdf.yml` — triggered by pushing `.github/pdf-parts/jee-main-2027-starter-handbook.READY`. It concatenates `.github/pdf-parts/jee-main-2027-starter-handbook.partNN.txt` (NN=01..12, 10,110 chars of base64 each, except part12=10,102), applies each part's `.fix.json` (position->char substitutions), decodes, asserts MD5 321ad7ad6176704450bc207a3fc513cd, writes downloads/jee-main-2027-starter-handbook.pdf, inserts the card/entry/sitemap, and pushes.
- Verified correct on GitHub: part01 (byte-perfect), part02 + part02.fix.json, part03 + part03.fix.json, part04 + part04.fix.json.
- part05.txt is currently garbage (repeated failed transcription attempts) — must be replaced.
- parts 06-12 not yet uploaded.

## How to finish
1. Rebuild the PDF with the deterministic script; verify MD5 321ad7ad6176704450bc207a3fc513cd.
2. base64 it (121,312 chars). Split: parts 01-04 as 10,110-char chunks (already uploaded + fix files), remaining 80,872 chars from offset 40440 into 8 chunks of 10,110 (last is 10,102) for parts 05-12.
3. Commit each part file, fetch it back, diff vs local truth, commit a `.fix.json` with substitution fixes until the assembled result matches the MD5. (Transcription through the commit API introduces ~1-14 single-char errors per 10k chars; the fix-file mechanism handles them. Beware mid-stream truncation — verify lengths after every commit.)
4. After all 12 parts + fixes verify locally (simulate the workflow's assembly in Python and check the MD5), commit an empty `.github/pdf-parts/jee-main-2027-starter-handbook.READY` — the workflow assembles, verifies, publishes card/entry/sitemap, and pushes.
5. Create a NEW Razorpay payment link: ₹99 (9900 paise), description 'The JEE Main 2027 Starter Handbook — Digital Edition (33-page PDF)', callback https://digitalkartai.shop/thank-you.html?product=jee-main-2027-starter-handbook, reference_id jee-main-2027-starter-handbook. The old link is cancelled.
6. Update the product page's buy button with the new link (restore the full page from git history commit 0a7f56ee or rebuild) and remove this redirect placeholder.

Product: 33-page JEE Main 2027 starter guide, ₹99 (MRP ₹499). All research, writing, and QA are done.
