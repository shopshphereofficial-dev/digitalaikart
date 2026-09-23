#!/usr/bin/env python3
# Build: The AI Listing Playbook (Meesho, Amazon, Flipkart) - Digitalaikart
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether,
                                HRFlowable, NextPageTemplate)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas as pdfcanvas

NAVY = HexColor('#0a1628')
NAVY2 = HexColor('#132a47')
GOLD = HexColor('#f5c542')
LIGHT = HexColor('#f4f6fa')
INK = HexColor('#1e293b')
MUTE = HexColor('#5b6b82')
LINE = HexColor('#d9e0ea')
PROMPTBG = HexColor('#fbf7e8')

PAGE_W, PAGE_H = A4

S = {
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.8, leading=14.5,
                           textColor=INK, spaceAfter=7, alignment=TA_LEFT),
    'lead': ParagraphStyle('lead', fontName='Helvetica-Oblique', fontSize=10.5, leading=15.5,
                           textColor=NAVY, spaceAfter=10),
    'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=20, leading=24,
                         textColor=NAVY, spaceBefore=2, spaceAfter=4),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=13, leading=16,
                         textColor=NAVY, spaceBefore=10, spaceAfter=5, keepWithNext=1),
    'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=10.8, leading=14,
                         textColor=NAVY, spaceBefore=8, spaceAfter=3, keepWithNext=1),
    'kicker': ParagraphStyle('kicker', fontName='Helvetica-Bold', fontSize=8.5, leading=11,
                              textColor=GOLD, spaceAfter=2),
    'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=9.8, leading=14,
                             textColor=INK, leftIndent=14, bulletIndent=4, spaceAfter=4),
    'check': ParagraphStyle('check', fontName='Helvetica', fontSize=9.8, leading=14.5,
                            textColor=INK, leftIndent=18, bulletIndent=4, spaceAfter=4),
    'prompt': ParagraphStyle('prompt', fontName='Courier', fontSize=8.6, leading=12.2,
                             textColor=NAVY),
    'pnote': ParagraphStyle('pnote', fontName='Helvetica-Oblique', fontSize=8.8, leading=12.5,
                            textColor=MUTE, spaceBefore=4),
    'cell': ParagraphStyle('cell', fontName='Helvetica', fontSize=8.8, leading=12,
                           textColor=INK),
    'cellb': ParagraphStyle('cellb', fontName='Helvetica-Bold', fontSize=8.8, leading=12,
                           textColor=white),
    'cellh': ParagraphStyle('cellh', fontName='Helvetica-Bold', fontSize=8.8, leading=12,
                            textColor=NAVY),
    'src': ParagraphStyle('src', fontName='Helvetica', fontSize=8.6, leading=12.5,
                          textColor=INK, leftIndent=14, bulletIndent=4, spaceAfter=4),
    'toc': ParagraphStyle('toc', fontName='Helvetica', fontSize=10.2, leading=17, textColor=INK),
}


class CoverCanvas(pdfcanvas.Canvas):
    pass


def _invariant_canvas(*args, **kwargs):
    kwargs['invariant'] = 1
    return pdfcanvas.Canvas(*args, **kwargs)


def on_page(canv, doc):
    canv.saveState()
    # footer
    canv.setStrokeColor(GOLD); canv.setLineWidth(1.4)
    canv.line(18 * mm, 14 * mm, PAGE_W - 18 * mm, 14 * mm)
    canv.setFont('Helvetica', 7.8); canv.setFillColor(MUTE)
    canv.drawString(18 * mm, 9.5 * mm, 'The AI Listing Playbook  ·  Meesho · Amazon · Flipkart')
    canv.drawRightString(PAGE_W - 18 * mm, 9.5 * mm, 'digitalkartai.shop  ·  Page %d' % doc.page)
    # header strip
    canv.setFillColor(NAVY)
    canv.rect(0, PAGE_H - 6 * mm, PAGE_W, 6 * mm, stroke=0, fill=1)
    canv.setFillColor(GOLD)
    canv.rect(0, PAGE_H - 6.9 * mm, PAGE_W, 0.9 * mm, stroke=0, fill=1)
    canv.restoreState()


def cover(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY); canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # gold frame
    canv.setStrokeColor(GOLD); canv.setLineWidth(1.2)
    canv.rect(12 * mm, 12 * mm, PAGE_W - 24 * mm, PAGE_H - 24 * mm)
    # brand
    canv.setFillColor(GOLD); canv.setFont('Helvetica-Bold', 12.5)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 38 * mm, 'D I G I T A L A I K A R T   P R E S E N T S')
    # title
    canv.setFillColor(white); canv.setFont('Helvetica-Bold', 39)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 62 * mm, 'The AI Listing')
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 78 * mm, 'Playbook')
    canv.setFillColor(GOLD); canv.setFont('Helvetica-Bold', 15)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 92 * mm, 'Meesho  ·  Amazon  ·  Flipkart')
    canv.setStrokeColor(GOLD); canv.setLineWidth(0.8)
    canv.line(PAGE_W / 2 - 30 * mm, PAGE_H - 99 * mm, PAGE_W / 2 + 30 * mm, PAGE_H - 99 * mm)
    canv.setFillColor(white); canv.setFont('Helvetica', 12.3)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 112 * mm, 'Write marketplace listings that pass QC and sell -')
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 119 * mm, 'with AI doing the writing, verified for 2026.')
    canv.setFont('Helvetica-Oblique', 10.5)
    canv.setFillColor(HexColor('#c8d3e4'))
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 129 * mm, 'A practical playbook for Indian online sellers: the new 2026 rules,')
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 135 * mm, 'the 15-minute workflow, 25 copy-paste prompts, and QC checklists.')

    # what's inside box
    items = [
        ('WHAT IS INSIDE', None),
        ('Amazon\'s 75-character title rule (July 2026) and how to pass it', None),
        ('The 2026 listing rules for all three marketplaces, in plain numbers', None),
        ('The 15-minute listing workflow, minute by minute', None),
        ('25 copy-paste AI prompts - titles, keywords, images, prices, replies', None),
        ('Pre-publish QC checklists + the 7-day listing revival plan', None),
    ]
    y = PAGE_H - 158 * mm
    x = PAGE_W / 2 - 72 * mm
    canv.setFillColor(NAVY2)
    canv.roundRect(x, y - 60 * mm, 144 * mm, 58 * mm, 4 * mm, stroke=0, fill=1)
    canv.setStrokeColor(GOLD); canv.setLineWidth(0.7)
    canv.roundRect(x, y - 60 * mm, 144 * mm, 58 * mm, 4 * mm, stroke=1, fill=0)
    ty = y - 8 * mm
    canv.setFillColor(GOLD); canv.setFont('Helvetica-Bold', 10)
    canv.drawCentredString(PAGE_W / 2, ty, 'W H A T   I S   I N S I D E')
    ty -= 8.5 * mm
    canv.setFillColor(white); canv.setFont('Helvetica', 10.6)
    for txt, _ in items[1:]:
        canv.drawString(x + 10 * mm, ty, '>>  ' + txt)
        ty -= 8.3 * mm
    # bottom
    canv.setFillColor(GOLD); canv.setFont('Helvetica-Bold', 10.5)
    canv.drawCentredString(PAGE_W / 2, 34 * mm, 'First Edition  ·  September 2026')
    canv.setFillColor(HexColor('#8ea2c0')); canv.setFont('Helvetica', 9.5)
    canv.drawCentredString(PAGE_W / 2, 26 * mm, 'Works with ChatGPT, Claude, Gemini and Meta AI - free plans are enough')
    canv.drawCentredString(PAGE_W / 2, 20 * mm, 'digitalaikart.shop')
    canv.restoreState()


def P(text, style='body'):
    return Paragraph(text, S[style])


def bullets(items, style='bullet', mark='•'):
    return [Paragraph(t, S[style], bulletText=mark) for t in items]


def checks(items):
    return [Paragraph(t, S['check'], bulletText='[  ]') for t in items]


def gold_rule():
    return HRFlowable(width='100%', thickness=1.1, color=GOLD, spaceBefore=0, spaceAfter=8)


def section(doc, kicker, title, lead=None):
    doc.append(Spacer(1, 2))
    doc.append(Paragraph(kicker, S['kicker']))
    doc.append(Paragraph(title, S['h1']))
    doc.append(gold_rule())
    if lead:
        doc.append(Paragraph(lead, S['lead']))


def table(data, widths, header=True, fontsize=8.8):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ('GRID', (0, 0), (-1, -1), 0.6, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    if header:
        style += [('BACKGROUND', (0, 0), (-1, 0), NAVY)]
        for row in data[1:]:
            pass
        # zebra
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.append(('BACKGROUND', (0, i), (-1, i), LIGHT))
    else:
        for i in range(0, len(data)):
            if i % 2 == 1:
                style.append(('BACKGROUND', (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(style))
    return t


def cellp(txt, style='cell'):
    return Paragraph(txt, S[style])


def prompt_block(pid, title, when, body, note):
    head = Table([[cellp(pid, 'cellb'), cellp('<font color="#ffffff">%s</font>' % title, 'cellb')]],
                 colWidths=[16 * mm, None])
    head.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), GOLD),
        ('BACKGROUND', (1, 0), (1, 0), NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('SPAN', (1, 0), (1, 0)),
    ]))
    inner = Table([[Paragraph(body, S['prompt'])]], colWidths=[None])
    inner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PROMPTBG),
        ('BOX', (0, 0), (-1, -1), 0.8, GOLD),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 9), ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    parts = [head,
             Paragraph(when, S['pnote']),
             inner]
    if note:
        parts.append(Paragraph('<b>Check before you use the output:</b> ' + note, S['pnote']))
    box = Table([[p] for p in parts], colWidths=[None])
    box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.9, NAVY2),
        ('BACKGROUND', (0, 0), (-1, -1), white),
        ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    return KeepTogether([Spacer(1, 6), box, Spacer(1, 4)])


story = []
doc_append = story.append

# ---------------------------------------------------------------- COVER + TOC
# (cover drawn via onPage of first template)

toc_entries = [
    ('1', 'Read this first', 'What this playbook is, who it is for, and the one rule that makes AI work'),
    ('2', 'What changed in 2026', 'The rules and AI shift most sellers have not noticed yet'),
    ('3', 'The rules that decide if your listing lives', 'Amazon.in, Flipkart and Meesho rule cards + side-by-side table'),
    ('4', 'The 15-minute listing workflow', 'Step by step with time budgets, plus the Product Fact Sheet'),
    ('5', 'The prompt library - 25 prompts', 'Foundations, per-platform prompts, and prompts beyond the listing'),
    ('6', 'Get found by AI shopping assistants', 'The 8-point machine-readability audit'),
    ('7', 'Pre-publish QC checklists', 'One checklist per platform - tick before you submit'),
    ('8', 'The 7-day listing revival plan', 'Fix your existing catalog one focused day at a time'),
    ('9', 'Prices, sales dates and honesty', 'The 2026 sale calendar, fake-MRP traps, and what not to do'),
]

# We add the TOC after cover via explicit flow.
def build_toc():
    out = [Spacer(1, 6),
           Paragraph('CONTENTS', S['kicker']),
           Paragraph('Contents', S['h1']), gold_rule()]
    for num, title, sub in toc_entries:
        out.append(Paragraph(
            '<b>Part %s &nbsp;·&nbsp; %s</b>' % (num, title), S['toc']))
        out.append(Paragraph(
            '<font size="8.8" color="#5b6b82">%s</font>' % sub,
            ParagraphStyle('tsub', parent=S['toc'], fontSize=8.8, leading=12.5,
                           textColor=MUTE, leftIndent=14, spaceAfter=6)))
    out.append(Spacer(1, 14))
    out.append(HRFlowable(width='100%', thickness=1.1, color=GOLD, spaceBefore=4, spaceAfter=10))
    out.append(Paragraph('HOW TO USE THIS PLAYBOOK', S['kicker']))
    out.append(Paragraph('Three ways in, depending on where you are today', S['h2']))
    for row in [
        ('<b>Brand new seller</b> - read Parts 1-4 in order tonight, fill one Product Fact Sheet, and publish your first listing with prompts A1, A2 and D1/B1/C1. Expect your first Meesho catalog to go live about 72 hours after QC.'),
        ('<b>Existing catalog, no time</b> - jump straight to Part 8, the 7-day revival plan. One focused task a day; by Sunday every listing obeys the 2026 rules.'),
        ('<b>Want the edge</b> - run prompt F2 on your best listing and fix what it flags. The AI shopping-assistant audit in Part 6 is where your competitors are weakest.'),
        ('Keep this PDF open beside your AI chat window while you work. Every prompt in Part 5 is written to be pasted whole, with only the [BRACKETED] parts replaced.'),
    ]:
        out.append(Paragraph(row, S['body'], bulletText='•'))
    return out

# ---------------------------------------------------------------- PART 1

p1 = []
section = lambda *a: None  # placeholder (we use explicit code below)

doc_append(PageBreak())
doc_append(Paragraph('PART 1', S['kicker']))
doc_append(Paragraph('Read this first', S['h1']))
doc_append(gold_rule())
doc_append(P('You sell on Meesho, Amazon or Flipkart (or plan to). You know your product. '
             'But every listing takes an hour, the words come out clumsy, and the platforms '
             'keep changing rules you only discover when a listing gets rejected.', 'lead'))
doc_append(P('This playbook fixes exactly that. It gives you (1) the current 2026 listing '
             'rules for all three marketplaces in plain numbers, (2) a 15-minute workflow that '
             'turns your product facts into a finished, compliant listing, and (3) 25 '
             'copy-paste prompts that make any AI tool - ChatGPT, Claude, Gemini or Meta AI - '
             'do the writing for you, safely.'))
doc_append(Paragraph('Who this is for', S['h2']))
for b in bullets([
    'New sellers setting up their first catalogs and tired of rejections and silent low visibility.',
    'Existing sellers whose listings were written years ago and now fail the new 2026 rules.',
    'Resellers and small brands who want Hinglish and English listings without hiring a copywriter.',
    'Anyone who has tried asking AI "write my product description" and got generic, risky output.']):
    doc_append(b)
doc_append(Paragraph('What you need before starting', S['h2']))
for b in bullets([
    'Any AI chat tool on your phone or laptop. Free plans of ChatGPT, Claude, Gemini or Meta AI are enough.',
    'Your product facts: material, size, colour, what is in the box, price. (Part 4 gives you a fact sheet to fill.)',
    'Product photos: one clean white-background shot plus a few angle shots. The prompts help you plan the rest.',
    '15 minutes per listing. That is the honest budget this workflow is built around.']):
    doc_append(b)
doc_append(Paragraph('The one rule that makes AI work for sellers', S['h2']))
doc_append(P('<b>Facts from you, words from the AI.</b> AI tools are excellent writers and '
             'confident liars. They do not know your kurti is rayon or your earbuds have a '
             '38-hour battery - and they will happily invent a spec that gets you bad reviews '
             'and returns. Every prompt in this book contains a guard: <i>use only the facts I '
             'give you; if something is missing, ask me</i>. Keep that guard in every prompt '
             'you ever write for your business.'))
doc_append(Paragraph('What this playbook is not', S['h2']))
for b in bullets([
    'Not a "get rich on Meesho" course. Listing quality is one lever; margins and stock are yours to manage.',
    'Not a rulebook replacement. Platforms update rules often - always confirm current limits inside Seller Central, Seller Hub or the Meesho Supplier Panel before bulk edits.',
    'Not a promise of ranking. No honest guide can guarantee position in search; these are the inputs the platforms reward.']):
    doc_append(b)
doc_append(P('Every platform rule, date and number in this playbook was verified on 23 September '
             '2026 from official seller documentation and current reporting; the full source list '
             'is on the last page.', 'pnote'))

# ---------------------------------------------------------------- PART 2

doc_append(PageBreak())
doc_append(Paragraph('PART 2', S['kicker']))
doc_append(Paragraph('What changed in 2026', S['h1']))
doc_append(gold_rule())
doc_append(P('Three things changed this year that most sellers have not fully absorbed yet. '
             'Each one is an opening for the sellers who act.', 'lead'))

doc_append(Paragraph('1. Amazon cut titles to 75 characters - and its AI now rewrites yours', S['h2']))
doc_append(P('From 27 July 2026, product titles on Amazon must be <b>75 characters or less, '
             'including spaces</b>, in every category except media (books, music, video, DVD keep '
             '200). Amazon announced this in June 2026 and enforces it now. Titles still '
             'over the limit are being gradually replaced by Amazon\'s own AI recommendation - '
             'so the rewrite happens either on your terms or on Amazon\'s.'))
doc_append(P('Two things come with the change:'))
for b in bullets([
    'A new <b>Item Highlights</b> field: up to 125 extra characters for materials, use cases or '
    'compatibility. It is searchable and shows below the title - but generally only when your '
    'title is inside the 75-character limit. Together you get a 200-character searchable budget.',
    'Backend search terms in India are limited to <b>200 bytes</b> - bytes, not characters. Go '
    'one byte over and the entire field can be de-indexed. Hindi words in Devanagari use 3 bytes '
    'per character, so transliterated spellings ("chikankari" not the Devanagari spelling) save space.']):
    doc_append(b)
doc_append(P('If you sell on Amazon, this alone is worth an afternoon: shorten every title to 75 '
             'characters and move the overflow into Item Highlights before Amazon\'s AI does it for you.'))

doc_append(Paragraph('2. The marketplaces moved their AI budgets to the seller side', S['h2']))
doc_append(P('According to Inc42 reporting (18 August 2026), Amazon, Flipkart and Meesho have '
             'shifted their AI investment from shopper-facing features to seller-side tools:'))
for b in bullets([
    '<b>Amazon</b> launched an AI seller assistant for its 1.7 million Indian sellers, built on '
    'Amazon Bedrock, answering in plain English or Hinglish for onboarding, catalogue, inventory '
    'and insights. Amazon reports sellers using it cut listing errors by about 10% and routine '
    'operational work by nearly 70%.',
    '<b>Meesho</b> is extending its Chorus AI platform to guide sellers on pricing, catalogue '
    'quality, advertising and sale participation - with a voice AI system reported to handle up '
    'to 3,00,000 seller calls a day. Meesho\'s annual transacting sellers reached 1.04 million, '
    'up 81% year on year.',
    '<b>Flipkart</b> reports that simplified AI dashboards helped new-seller onboarding from '
    'Tier-3 and Tier-4 towns grow 80-85% this year.']):
    doc_append(b)
doc_append(P('Translation: the platforms will happily draft your listing and set your price '
             'bands. Use their tools for speed - but keep your own numbers outside the platform, '
             'because a marketplace tool optimises for the marketplace\'s metric, which is rarely '
             'your profit per unit.'))

doc_append(Paragraph('3. Nearly half of sellers still use no AI at all', S['h2']))
doc_append(P('Snapdeal\'s Bharat Seller Report 2026 found <b>44% of surveyed e-commerce sellers '
             'use no AI tools</b> - even though 46% now get more than three-quarters of their '
             'business online. That gap is your opening: sellers who simply write better listings '
             'with AI - compliant, keyword-honest, complete - stand out in search while '
             'competitors keep hand-typing weak titles.'))
doc_append(Paragraph('And a quiet fourth shift: AI shopping assistants', S['h2']))
doc_append(P('Buyers increasingly ask AI to shop - "find me a durable trekking bag under '
             'Rs 3,000 with a laptop compartment." Your listing only enters that answer if it is '
             'structured, specific and complete. Part 6 of this playbook is a dedicated audit for '
             'that. It is the newest edge in Indian e-commerce, and almost nobody optimises for it yet.'))

# ---------------------------------------------------------------- PART 3

doc_append(PageBreak())
doc_append(Paragraph('PART 3', S['kicker']))
doc_append(Paragraph('The rules that decide if your listing lives', S['h1']))
doc_append(gold_rule())
doc_append(P('Every marketplace runs a quality gate between your upload and the buyer. Learn '
             'each platform\'s rules once, and your listings stop bouncing.', 'lead'))

doc_append(Paragraph('Amazon.in rule card', S['h2']))
doc_append(table([
    [cellp('Field', 'cellb'), cellp('Rule (verified Sept 2026)', 'cellb')],
    [cellp('Title', 'cellh'), cellp('Max 75 characters including spaces (all categories except media, since 27 July 2026). Structure: brand + product noun + 1-2 key attributes. No word repeated more than twice. Banned characters: !, $, ?, _, {, }, ^, ¬, ¦. No promotional words like "free shipping" or "100% guaranteed".')],
    [cellp('Item Highlights', 'cellh'), cellp('Up to 125 characters, searchable, shown below the title when the title is under 75. Use for materials, use cases, compatibility. Content that repeated the old 200-character titles goes here now.')],
    [cellp('Bullets', 'cellh'), cellp('5 recommended. Each 10-255 characters; only the first 1,000 bytes across all five are indexed - front-load.')],
    [cellp('Description', 'cellh'), cellp('Max 2,000 characters, plain text only (HTML was removed in July 2021). Use A+ Content for richer formatting - text inside images is NOT indexed.')],
    [cellp('Backend search terms', 'cellh'), cellp('200 bytes in India. Measured in bytes, not characters. Exceeding the limit can de-index all your terms. No repeats of title words.')],
    [cellp('Images', 'cellh'), cellp('Main image: pure white background (RGB 255,255,255), product fills 85% of frame, no text, logos, watermarks or props. 500-10,000 px longest side; 1,000 px+ enables zoom. JPEG, TIFF, PNG or non-animated GIF. 6 images + 1 video recommended.')],
    [cellp('Most common killers', 'cellh'), cellp('Over-length titles (now AI-rewritten), empty attribute fields, sparse backend terms, main images with text or coloured backgrounds.')],
], [30 * mm, None]))
doc_append(Spacer(1, 8))

doc_append(Paragraph('Flipkart rule card', S['h2']))
doc_append(table([
    [cellp('Field', 'cellb'), cellp('Rule (verified Sept 2026)', 'cellb')],
    [cellp('Title', 'cellh'), cellp('No single published limit - the working rules are: brand name first, the product noun (what buyers type) within the first five words, only 2-3 defining attributes, no promotional language (fails QC), no ALL CAPS, no keyword stuffing. Flipkart penalises spammy titles.')],
    [cellp('Attributes', 'cellh'), cellp('Fill every applicable attribute. Flipkart search filters run on structured attributes - a blank field removes you from filtered results. Category taxonomy differs from Amazon; an Amazon bulk template silently drops Flipkart fields.')],
    [cellp('Images', 'cellh'), cellp('Main image: white background, product fills roughly 85% of the frame, no watermarks, no text overlays, no visible MRP stickers, no props. Minimum 500x500 px; 1000x1000 px or higher recommended (Big Billion Days audits expect 1000x1000). JPEG, RGB. Minimum 2 images; most categories allow up to 8.')],
    [cellp('Description', 'cellh'), cellp('Cover benefits, use cases, materials, care and warranty in natural language. Wrong or exaggerated claims fail QC.')],
    [cellp('Most common killers', 'cellh'), cellp('Image QC rejections with generic error messages, missing mandatory attributes, wrong category, duplicate listings, fake MRP.')],
], [30 * mm, None]))
doc_append(Spacer(1, 8))

doc_append(Paragraph('Meesho rule card', S['h2']))
doc_append(table([
    [cellp('Field', 'cellb'), cellp('Rule (verified Sept 2026)', 'cellb')],
    [cellp('Title', 'cellh'), cellp('Target 50-120 characters. Structure: product type first (the exact word buyers type - "kurti", "bedsheet", "earrings"), then style, then material, then ONE main feature. No ALL CAPS, no symbols, no repeated keywords. (Confirm current field limits in your Supplier Panel before bulk edits.)')],
    [cellp('Catalogs', 'cellh'), cellp('A catalog holds 1-9 products of the same category. Meesho recommends 3-4 products per catalog and uploading 5-7 catalogs in your first days for visibility. Catalogs go live roughly 72 hours after passing QC.')],
    [cellp('Images', 'cellh'), cellp('Square 1:1 images, recommended 1000x1000 px (minimum 500x500), JPEG or PNG. Clean white or light background, no collage, no watermark, no price or contact text. The first image carries almost all the click weight. Detailed image guidelines live inside the Supplier Panel.')],
    [cellp('Compliance', 'cellh'), cellp('Correct GST details and HSN code required at upload (a wrong HSN surfaces later as settlement issues). Size chart mandatory for fashion. Fake MRP or misleading discounts are penalised.')],
    [cellp('Most common killers', 'cellh'), cellp('Image policy breaks (collage, watermark, text, blurry), title that does not match the image, wrong category, wrong HSN, duplicate detection.')],
], [30 * mm, None]))
doc_append(Spacer(1, 8))

doc_append(Paragraph('Side by side: the three platforms at a glance', S['h2']))
doc_append(table([
    [cellp('Rule', 'cellb'), cellp('Amazon.in', 'cellb'), cellp('Flipkart', 'cellb'), cellp('Meesho', 'cellb')],
    [cellp('Title target', 'cellh'), cellp('75 chars max + 125 Item Highlights'), cellp('Brand first, noun in first 5 words'), cellp('50-120 chars, product type first')],
    [cellp('Main image', 'cellh'), cellp('Pure white, 85% fill, 1000px+'), cellp('White, ~85% fill, 1000x1000'), cellp('Square 1000x1000, white/light')],
    [cellp('Go-live time', 'cellh'), cellp('Usually same day'), cellp('After QC'), cellp('~72 hours after QC')],
    [cellp('Biggest listing killer', 'cellh'), cellp('Over-length titles, empty attributes'), cellp('Image QC + attribute gaps'), cellp('Image policy breaks')],
    [cellp('Seller scale (2026)', 'cellh'), cellp('1.7 million sellers'), cellp('1.4 million+ sellers'), cellp('1.04 million transacting (+81% YoY)')],
], [24 * mm, 50 * mm, 52 * mm, 48 * mm]))
doc_append(Spacer(1, 4))
doc_append(P('One habit covers all three: <b>one product, one fact sheet, three tailored '
             'listings.</b> Never paste the same title across platforms - the rules and the '
             'buyer language differ.', 'body'))

# ---------------------------------------------------------------- PART 4

doc_append(PageBreak())
doc_append(Paragraph('PART 4', S['kicker']))
doc_append(Paragraph('The 15-minute listing workflow', S['h1']))
doc_append(gold_rule())
doc_append(P('This is the whole method on one page. Each step uses one prompt from Part 5.', 'lead'))
doc_append(table([
    [cellp('Min', 'cellb'), cellp('Step', 'cellb'), cellp('Prompt', 'cellb')],
    [cellp('0-2', 'cellh'), cellp('Fill the Product Fact Sheet below. Rough notes are fine - the AI structures them.'), cellp('A1')],
    [cellp('2-5', 'cellh'), cellp('Mine keywords. Then type your top 5 phrases into the platform search bar and confirm real results appear.'), cellp('A2')],
    [cellp('5-8', 'cellh'), cellp('Generate the title for your platform and stress-test it (character count, noun position, banned words).'), cellp('B1 / C1 / D1 + A4')],
    [cellp('8-11', 'cellh'), cellp('Generate bullets and the description. Read every line - delete anything not in your fact sheet.'), cellp('B3 / C3 / D2')],
    [cellp('11-12', 'cellh'), cellp('Amazon only: backend search terms under 200 bytes.'), cellp('B4')],
    [cellp('12-13', 'cellh'), cellp('Plan the image set before you shoot: main white shot + lifestyle + spec + scale + in-box.'), cellp('C4')],
    [cellp('13-14', 'cellh'), cellp('Run the platform QC checklist (Part 7). Fix anything flagged.'), cellp('-')],
    [cellp('14-15', 'cellh'), cellp('Submit. Meesho: check back after ~72 hours. Amazon/Flipkart: check next morning for QC messages.'), cellp('-')],
], [16 * mm, None, 30 * mm]))
doc_append(Spacer(1, 8))

doc_append(Paragraph('The Product Fact Sheet (fill this once per product)', S['h2']))
doc_append(P('This is the single most valuable page in the playbook. Every prompt reads from it, '
             'which is why the same AI that invents specs for other sellers stays honest for you.'))
doc_append(KeepTogether(table([
    [cellp('Product type (exact buyer word)', 'cellh'), cellp('_______________________')],
    [cellp('Brand / model / design name', 'cellh'), cellp('_______________________')],
    [cellp('Material / fabric', 'cellh'), cellp('_______________________')],
    [cellp('Colour', 'cellh'), cellp('_______________________')],
    [cellp('Sizes / dimensions / weight', 'cellh'), cellp('_______________________')],
    [cellp('What is in the box', 'cellh'), cellp('_______________________')],
    [cellp('Key features (max 5, in your own words)', 'cellh'), cellp('_______________________')],
    [cellp('Who buys it + occasion', 'cellh'), cellp('_______________________')],
    [cellp('Care / warranty / shelf life', 'cellh'), cellp('_______________________')],
    [cellp('HSN code + GST rate', 'cellh'), cellp('_______________________')],
    [cellp('Cost price / planned price / MRP', 'cellh'), cellp('_______________________')],
    [cellp('Photos ready? (white main + 3-5 secondary)', 'cellh'), cellp('Yes / No')],
], [70 * mm, 40 * mm], header=False)))
doc_append(Spacer(1, 6))
doc_append(P('Tip: save each product\'s fact sheet in one spreadsheet. When a platform changes '
             'rules again - and it will - you regenerate every listing in an afternoon instead '
             'of rewriting from memory.', 'pnote'))

# ---------------------------------------------------------------- PART 5

doc_append(PageBreak())
doc_append(Paragraph('PART 5', S['kicker']))
doc_append(Paragraph('The prompt library - 25 copy-paste prompts', S['h1']))
doc_append(gold_rule())
doc_append(P('Paste any of these straight into ChatGPT, Claude, Gemini or Meta AI. Replace every '
             '[BRACKETED] part. The "check" note after each prompt tells you what a good output '
             'looks like - and the traps to catch.', 'lead'))
doc_append(P('Every prompt already includes the anti-hallucination guard. Do not remove the '
             'line "use only the facts I give you" from any prompt you edit.', 'pnote'))

doc_append(Paragraph('Group A · Foundations (4 prompts)', S['h2']))

doc_append(prompt_block('A1', 'The Product Fact Sheet Builder',
    'Use: once per product, before everything else.',
    'You are my e-commerce listing assistant. Convert my rough notes below into a structured\n'
    'fact sheet with these fields: product type, brand, material, colour, sizes, dimensions,\n'
    'weight, what is in the box, key features (max 5), target buyer, occasion, care,\n'
    'warranty. RULES: use ONLY facts from my notes. If a field is missing from my notes,\n'
    'write [ASK SELLER] - never guess, never invent. My notes:\n'
    '[PASTE YOUR ROUGH NOTES]',
    'Every line must be traceable to your notes. Fill every [ASK SELLER] gap yourself before using the sheet.'))

doc_append(prompt_block('A2', 'The Keyword Miner',
    'Use: after the fact sheet, before any title.',
    'You are an e-commerce keyword researcher for [PLATFORM: Amazon.in / Flipkart / Meesho].\n'
    'Product: [PRODUCT TYPE + ONE-LINE DESCRIPTION]. Generate:\n'
    '1) 15 search phrases an Indian buyer would actually type for this product. Include 2-3\n'
    '   Hinglish or transliterated variants if common for this category.\n'
    '2) For each, a competition guess marked clearly as a GUESS (High/Medium/Low).\n'
    '3) 5 long-tail phrases (3+ words) showing clearer buying intent.\n'
    '4) 8 backend search terms: synonyms, alternate names, common Indian misspellings -\n'
    '   not words that will already be in my title. Present everything as one table.',
    'AI cannot see real search volumes. Treat all competition ratings as guesses and verify your top 5 phrases by typing them into the platform search bar before trusting them.'))

doc_append(prompt_block('A3', 'The Competitor Teardown',
    'Use: when entering a crowded category.',
    'I will paste the titles of 3 competitor listings for [PRODUCT TYPE]. For each one:\n'
    '1) List the keywords it targets.\n'
    '2) One thing its title does well.\n'
    '3) One gap I can exploit (missing attribute, vague claim, no size info, no occasion\n'
    '   hook, no material named).\n'
    'Then suggest a different angle for MY listing - not a copy of any of them.\n'
    'Competitor 1: [PASTE]  Competitor 2: [PASTE]  Competitor 3: [PASTE]',
    'Copy structures and angles, never wording or images. And remember your facts may differ - keep the gap-honest angle.'))

doc_append(prompt_block('A4', 'The Title Stress Test',
    'Use: on every title before you submit it, any platform.',
    'Here is my draft title for [PLATFORM]: "[TITLE]". Check and report:\n'
    '1) Exact character count including spaces - state the number.\n'
    '2) Is the product noun (the word buyers type, like "kurti" or "earbuds") within the\n'
    '   first 4 words?  3) Any word repeated more than twice?\n'
    '4) Any banned or promotional words (best, free, guaranteed, 100%)?\n'
    '5) Would the first 30 characters alone tell a buyer what the product is?\n'
    'Then give one improved version, with its new character count.',
    'The character count must match the platform\'s own field counter. If the AI counts differently, trust the platform field.'))

doc_append(Paragraph('Group B · Amazon.in (5 prompts)', S['h2']))

doc_append(prompt_block('B1', 'The 75-Character Title',
    'Use: every Amazon listing, new or old.',
    'Write an Amazon.in product title for this product.\n'
    'HARD RULES: maximum 75 characters INCLUDING spaces - count and show the count.\n'
    'Structure: Brand + product noun + 1-2 key attributes. No promotional words. No special\n'
    'characters like !, $, ?, _ or ^. No word repeated more than twice.\n'
    'Give 3 ranked options, each with its exact character count.\n'
    'Product fact sheet: [PASTE FACT SHEET]',
    'If every option is near exactly 75 characters, the AI is front-loading. Pick the option that survives being cut to 30 characters in mobile search.'))

doc_append(prompt_block('B2', 'Item Highlights',
    'Use: for details that no longer fit the 75-character title.',
    'For this Amazon listing, write the Item Highlights field: max 125 characters,\n'
    'searchable, for materials / use cases / compatibility that did not fit the title.\n'
    'Show the character count. Give 3 options.\n'
    'Product facts: [PASTE FACT SHEET]. My final title: [PASTE TITLE]',
    'Item Highlights generally only displays when the title is under 75 characters - so this pair only pays off together.'))

doc_append(prompt_block('B3', 'Five Bullet Points',
    'Use: after the title.',
    'Write 5 Amazon bullet points for this product. Each bullet 80-150 characters.\n'
    'Cover in order: main benefit, material/quality, size or dimensions, use case or\n'
    'occasion, care or warranty. Use ONLY facts from the fact sheet - if a fact is\n'
    'missing, write [CONFIRM] instead of inventing it. No emojis, no hype words.\n'
    'Fact sheet: [PASTE]',
    'Only the first 1,000 bytes across all five bullets are indexed - if the AI writes long, cut from the fifth bullet first, not the first.'))

doc_append(prompt_block('B4', 'Backend Search Terms (under 200 bytes)',
    'Use: Amazon only, once per listing.',
    'Generate Amazon.in backend search terms for this product.\n'
    'HARD LIMIT: the total field must stay under 200 BYTES including spaces - bytes, not\n'
    'characters (Devanagari words cost 3 bytes per character, so prefer transliterated\n'
    'spellings). Include: synonyms, alternate names, common Indian misspellings, Hinglish\n'
    'variants. Do NOT repeat any word already in my title: [PASTE TITLE].\n'
    'Output: the final space-separated list on one line, then the exact byte count.',
    'Going over the byte limit can de-index every term in the field. Count bytes, paste into Seller Central, and let the platform counter confirm.'))

doc_append(prompt_block('B5', 'Plain-Text Description',
    'Use: when the description field is the only content you have.',
    'Write an Amazon product description, max 2,000 characters, PLAIN TEXT only - no HTML,\n'
    'no markdown, no emoji. Structure: 2-sentence opener on who it is for; a spec list one\n'
    'per line (material, size, weight, colour); care instructions; closing line on what is\n'
    'in the box. Use only facts from the fact sheet - flag gaps with [CONFIRM].\n'
    'Fact sheet: [PASTE]',
    'Text inside images is not indexed - if a spec matters for search, it must exist as text here or in attributes.'))

doc_append(Paragraph('Group C · Flipkart (4 prompts)', S['h2']))

doc_append(prompt_block('C1', 'The Brand-First Title',
    'Use: every Flipkart listing.',
    'Write a Flipkart product title for this product. RULES: brand name first; the\n'
    'product noun (what buyers type) within the first five words; only 2-3 defining\n'
    'attributes (colour, size, material or pack quantity); no promotional language - it\n'
    'fails Flipkart QC; no ALL CAPS; readable, not stuffed. 3 ranked options with\n'
    'character counts, none over 100 characters.\n'
    'Fact sheet: [PASTE]',
    'Flipkart heavily truncates titles on mobile and sometimes reformats them. If the first five words alone would still sell the click, the title works.'))

doc_append(prompt_block('C2', 'The Attribute Sweep',
    'Use: after choosing the category, before submitting.',
    'Here are the attribute fields Flipkart asks for in my category: [PASTE FIELD LIST,\n'
    'or write "standard apparel fields"]. Using my fact sheet, give the value I should\n'
    'enter for each field. For any field where you do not know my answer, write [ASK] -\n'
    'never guess. Then mark the 5 fields that most affect filtered-search visibility.\n'
    'Fact sheet: [PASTE]',
    'A blank attribute removes you from that filter\'s results entirely. This is the cheapest visibility win on Flipkart.'))

doc_append(prompt_block('C3', 'QC-Safe Description',
    'Use: after the title.',
    'Write a Flipkart product description. Structure: first line = what it is and who it\n'
    'is for; then a Specifications block (one line per attribute); then In the box;\n'
    'then a 2-line care note. Under 1,200 characters. No superlatives, no unverifiable\n'
    'claims - Flipkart QC rejects exaggerated wording. Facts only from: [PASTE FACT SHEET]',
    'Flipkart rejection messages rarely name the rule that failed. Keep claims boring and factual, and you stop feeding that loop.'))

doc_append(prompt_block('C4', 'The Image Set Planner',
    'Use: before your photo shoot - any platform.',
    'Plan my Flipkart image set (main + secondary images) for this product. The main\n'
    'image must be white-background, product-only, filling ~85% of the frame. For the\n'
    'other slots give a shot list: lifestyle in an Indian context, a spec infographic\n'
    '(list exactly which specs to display), a scale/dimension reference, a what-is-in-\n'
    'the-box shot, a close-up, and a trust panel (warranty/care). For each: what to\n'
    'show and the single text line to put on the image (secondary images may carry text).\n'
    'Product: [PASTE FACT SHEET]',
    'Do not shoot a single extra photo before this list exists - most sellers shoot first and discover later they missed the spec or scale shot.'))

doc_append(Paragraph('Group D · Meesho (4 prompts)', S['h2']))

doc_append(prompt_block('D1', 'The 50-120 Character Title',
    'Use: every Meesho catalog.',
    'Write a Meesho product title. Structure: product type first (the exact word buyers\n'
    'type - "kurti", "bedsheet", "earrings"), then style, then material, then ONE main\n'
    'feature. Target 50-120 characters total. No ALL CAPS, no symbols, no repeated\n'
    'keywords, natural and honest. 3 options with character counts.\n'
    'Fact sheet: [PASTE]',
    'A title under 50 characters usually means missed keywords; over 120 starts to look like spam and gets truncated in the grid.'))

doc_append(prompt_block('D2', 'The Value-First Description',
    'Use: after the Meesho title.',
    'Write a Meesho product description. Meesho buyers are value-first and many are\n'
    'first-time online shoppers: lead with what the product is and its material, then 5\n'
    'short "why you will like it" lines, then care, then a one-line size-chart reminder\n'
    'for apparel. Under 800 characters, simple English. Facts only from:\n'
    '[PASTE FACT SHEET]',
    'Read it once aloud. If a sentence needs re-reading, it is too complex for the audience that converts best here.'))

doc_append(prompt_block('D3', 'The Hinglish Version',
    'Use: categories where buyers search and read in Hindi.',
    'Rewrite this product description in natural Hinglish - Hindi in Devanagari script,\n'
    'keeping common English e-commerce words in English (fabric, size, pack, delivery).\n'
    'Keep every fact identical. Do not translate size codes (M, XL) or units (cm, kg).\n'
    'Description: [PASTE DESCRIPTION]',
    'Run one read-through for tone: Hinglish should sound like a helpful shopkeeper, not a textbook translation.'))

doc_append(prompt_block('D4', 'The Catalog Grouper',
    'Use: when uploading multiple Meesho catalogs.',
    'My products: [LIST YOUR PRODUCT TYPES]. Group them into Meesho catalogs.\n'
    'RULES: a catalog holds products of the same category; 3-4 products per catalog\n'
    'works best for orders. Output: catalog name, products in it, and a one-line title\n'
    'pattern to keep titles consistent within the catalog. Flag any product that\n'
    'belongs in a different category than the one I put it in.',
    'Meesho recommends 5-7 catalogs in your first days. Same-category grouping and consistent titles help the algorithm place each catalog.'))

doc_append(Paragraph('Group E · Beyond the listing (4 prompts)', S['h2']))

doc_append(prompt_block('E1', 'Buyer Question Replies',
    'Use: on listing Q&A - fast, honest replies convert.',
    'A buyer asked on my listing: "[BUYER QUESTION]". Product facts: [PASTE FACT SHEET].\n'
    'Write a public reply under 60 words: warm and simple, answers exactly the question\n'
    'with facts only, plus one helpful extra (a size tip or care note). If the answer\n'
    'needs information I do not have, write a reply asking one specific clarification\n'
    'instead. Never invent specs.',
    'A wrong answer here becomes a return later. If the fact is not in your sheet, ask, do not answer.'))

doc_append(prompt_block('E2', 'Negative Review Response',
    'Use: within 24 hours of any bad review.',
    'I received this negative review: "[REVIEW]". Write a calm, professional public\n'
    'response under 70 words: acknowledge the specific issue, no excuses, state one\n'
    'concrete fix or next step, invite them to contact me on [WHATSAPP/EMAIL].\n'
    'No blaming the customer. No discounts promised in public.',
    'Future buyers read this more than the review. Steady, specific and solved beats defensive every time.'))

doc_append(prompt_block('E3', 'The Price Sanity Check',
    'Use: before setting or changing any price.',
    'My numbers: cost price Rs [X] per unit, estimated platform fees + shipping Rs [Y]\n'
    'per unit, planned selling price Rs [Z], listed MRP Rs [M]. Calculate: (1) margin\n'
    'per unit after fees; (2) my break-even price; (3) the discount percentage the MRP\n'
    'displays - and warn me if that discount looks unrealistic enough to count as a\n'
    'fake-MRP pattern. Then list 3 questions that would test my cost assumptions.\n'
    'Use ONLY the numbers I gave - do not estimate fees for me.',
    'Fill the fee number from your own settlement report, not the AI - fee estimates are the one place the AI must stay silent.'))

doc_append(prompt_block('E4', 'The Sale-Season Refresh',
    'Use: 2-3 weeks before big sale events.',
    'Sale season is coming: [PLATFORM]\'s sale opens [DATE], and Diwali is 8 November\n'
    '2026. My top listing: [PASTE TITLE + BULLETS]. Suggest: (1) two keywords to add\n'
    'for the festive or gifting angle in this category; (2) one line about delivery\n'
    'timing to add to the description; (3) what NOT to change - the parts already\n'
    'converting. Do not suggest price changes - those are mine to decide.',
    'Keyword performance shifts before every sale event. Refresh, but never rebuild a listing that is already selling.'))

doc_append(Paragraph('Group F · Growing (4 prompts)', S['h2']))

doc_append(prompt_block('F1', 'One Fact Sheet, Three Listings',
    'Use: any product you list on more than one platform.',
    'Using ONLY this fact sheet, produce for the same product: (1) an Amazon.in title of\n'
    'max 75 characters (count it) plus Item Highlights of max 125 characters; (2) a\n'
    'Flipkart title with brand first and the product noun in the first five words;\n'
    '(3) a Meesho title of 50-120 characters with the product type first. Keep every\n'
    'fact identical across all three. Show each with its character count.\n'
    'Fact sheet: [PASTE]',
    'Three tailored listings from one source of truth - this is how a catalog survives the next rule change too.'))

doc_append(prompt_block('F2', 'The AI Shopping-Assistant Audit',
    'Use: once per listing, after it is live.',
    'Buyers now ask AI shopping assistants things like "find me a [PRODUCT CATEGORY]\n'
    'under Rs [PRICE] for [USE CASE]". Audit my listing for machine-readability:\n'
    '[PASTE TITLE + DESCRIPTION + ATTRIBUTES]. Score 0-5 on: specific specs present\n'
    '(dimensions, material, weight), structured attribute completeness, exact product\n'
    'noun in the title, honest claims, size/compatibility clarity. For each score\n'
    'below 5, write the exact line to add. Facts only from my listing.',
    'AI assistants skip listings whose specs live only inside images or vague prose. Every "add this line" suggestion should be a fact you confirm first.'))

doc_append(prompt_block('F3', 'The WhatsApp Broadcast',
    'Use: when driving repeat buyers to a listing.',
    'Write a WhatsApp broadcast message for my existing customers about this product:\n'
    '[FACTS + LINK]. Under 400 characters, 1 emoji max, no ALL CAPS, one clear next\n'
    'step, mention price only if I included it. Two versions: English and Hinglish.\n'
    'Facts only from what I gave you.',
    'Send it to yourself first. Check the link, the price and that it reads like a person, not a poster.'))

doc_append(prompt_block('F4', 'The Weekly 30-Minute Audit',
    'Use: every week, same slot - this is the compounding habit.',
    'Act as my listing auditor. I will paste my listings (title + price + platform).\n'
    'Flag and priority-rank: (1) any Amazon title over 75 characters - at risk of an\n'
    'AI rewrite; (2) any title where the product noun is not in the first 4 words;\n'
    '(3) any listing missing Item Highlights or backend terms; (4) any title with\n'
    'promotional words that fail QC. Output a fix list, biggest risk first.\n'
    'My listings: [PASTE LIST]',
    'Thirty minutes a week catches a broken title before it costs a week of sales - and before Amazon\'s AI rewrites it for you.'))

# ---------------------------------------------------------------- PART 6

doc_append(PageBreak())
doc_append(Paragraph('PART 6', S['kicker']))
doc_append(Paragraph('Get found by AI shopping assistants', S['h1']))
doc_append(gold_rule())
doc_append(P('The newest frontier: buyers ask AI to shop, and marketplaces run their own AI '
             'search and assistants. A listing built only for human eyes is becoming invisible '
             'to machines. The fix is not tricks - it is structure.', 'lead'))
doc_append(P('When a shopper asks for "a durable trekking bag under Rs 3,000 with a laptop '
             'compartment", an AI assistant needs to find those three facts in your listing as '
             'clean, separate data - not as a sentence buried in paragraph four. The 8-point '
             'audit below (built into prompt F2) is what machine-readable looks like:'))
for b in bullets([
    '<b>Exact product noun in the title.</b> "Kurti", not "ethnic wear combo". The machine matches the word the buyer said.',
    '<b>Every attribute field filled.</b> Filterable data is speakable data for an assistant.',
    '<b>Specific numbers, not adjectives.</b> "38 cm x 24 cm, 480 g, 100% cotton" beats "compact and lightweight".',
    '<b>Complete size chart.</b> Fashion without a size chart is unanswerable for fit questions.',
    '<b>Honest, checkable claims.</b> Assistants trained on catalogues penalise exaggerated language.',
    '<b>Specs as text, not as image text.</b> Text inside infographic images is invisible to search and assistants.',
    '<b>FAQ-style bullets.</b> Answer the top 5 buyer questions directly in the listing.',
    '<b>A short, compliant title.</b> On Amazon, the 75-character limit means the machine reads your whole title - and Item Highlights add another 125 searchable characters.',
]):
    doc_append(b)
doc_append(Spacer(1, 4))
doc_append(P('Do this audit once per listing, live. It is the cheapest long-term visibility '
             'work you will do this year - and almost none of your competitors are doing it.', 'pnote'))

# ---------------------------------------------------------------- PART 7

doc_append(PageBreak())
doc_append(Paragraph('PART 7', S['kicker']))
doc_append(Paragraph('Pre-publish QC checklists', S['h1']))
doc_append(gold_rule())
doc_append(P('Print this page or keep it open. Tick every box before you press submit - a '
             'rejection costs days; a fix costs seconds.', 'lead'))

doc_append(Paragraph('Amazon.in', S['h2']))
for c in checks([
    'Title is 75 characters or less including spaces (count it, do not eyeball it)',
    'Item Highlights filled (up to 125 characters) with material / use case / compatibility',
    'No banned characters (!, $, ?, _, {, }, ^) and no word repeated more than twice',
    '5 bullet points, each 80-150 characters, facts only',
    'Description under 2,000 characters, plain text, no HTML',
    'Backend search terms under 200 bytes, no title words repeated',
    'Main image: pure white background, product fills 85%, no text or logos, 1,000 px+',
    'All attribute fields complete; HSN and GST set',
]):
    doc_append(c)
doc_append(Spacer(1, 6))

doc_append(Paragraph('Flipkart', S['h2']))
for c in checks([
    'Brand name first in the title; product noun in the first five words',
    'No promotional language, no ALL CAPS, no keyword stuffing',
    'Every mandatory attribute filled (blank fields remove you from filtered search)',
    'Main image: white background, ~85% fill, no watermark, text, props or visible MRP stickers',
    'Images 1000x1000 px or larger, JPEG; at least 2 uploaded (aim for 5-8)',
    'Correct category and subcategory; no duplicate listing',
    'Fashion categories: accurate size chart attached',
]):
    doc_append(c)
doc_append(Spacer(1, 6))

doc_append(Paragraph('Meesho', S['h2']))
for c in checks([
    'Title is 50-120 characters, product type first, no symbols or repeated keywords',
    'Images square (1:1), 1000x1000 recommended, clean background',
    'No collage, watermark, price text or contact details on any image',
    'Catalog groups 3-4 products of the same category',
    'Correct HSN code and GST rate entered (wrong HSN = settlement pain later)',
    'Fashion: size chart attached and matches the sizes you entered',
    'Price covers product cost + fees + shipping (run prompt E3 first)',
    'You know catalogs go live ~72 hours after QC - plan sale events backwards from that',
]):
    doc_append(c)

# ---------------------------------------------------------------- PART 8

doc_append(PageBreak())
doc_append(Paragraph('PART 8', S['kicker']))
doc_append(Paragraph('The 7-day listing revival plan', S['h1']))
doc_append(gold_rule())
doc_append(P('For sellers with an existing catalog. One focused task per day - by Sunday your '
             'listings obey the 2026 rules and read like they were written by a professional.', 'lead'))
doc_append(table([
    [cellp('Day', 'cellb'), cellp('Task (30-60 minutes)', 'cellb'), cellp('Prompts', 'cellb')],
    [cellp('1', 'cellh'), cellp('Inventory: paste all your titles into the weekly audit. Count how many Amazon titles exceed 75 characters.'), cellp('F4')],
    [cellp('2', 'cellh'), cellp('Amazon: shorten every over-length title to 75 characters and add Item Highlights. Brand owners: review AI recommendations in Review Listing Changes within 14 days.'), cellp('B1, B2')],
    [cellp('3', 'cellh'), cellp('Flipkart: run the attribute sweep on your 5 best listings; fix every blank field. Re-shoot or clean any main image with stickers or text.'), cellp('C2, C4')],
    [cellp('4', 'cellh'), cellp('Meesho: check catalogs group same-category products, 3-4 each. Verify HSN codes and size charts.'), cellp('D4')],
    [cellp('5', 'cellh'), cellp('Rewrite the worst 5 descriptions with AI - one fact sheet per product first. Delete every claim you cannot prove.'), cellp('A1, B5 / C3 / D2')],
    [cellp('6', 'cellh'), cellp('Seasonal refresh: add festive keywords to your top listings ahead of the sale events (Amazon Great Indian Festival opens 8 Oct, Flipkart BBD 9 Oct, Diwali 8 Nov 2026).'), cellp('E4')],
    [cellp('7', 'cellh'), cellp('Lock the habit: book a weekly 30-minute audit slot. Run it, fix the top flag, close the laptop.'), cellp('F4')],
], [12 * mm, None, 24 * mm]))
doc_append(Spacer(1, 6))
doc_append(P('After the first full run, this collapses into the weekly 30-minute audit - the '
             'difference between sellers who react to rule changes and sellers who read about '
             'them later.', 'pnote'))

# ---------------------------------------------------------------- PART 9

doc_append(PageBreak())
doc_append(Paragraph('PART 9', S['kicker']))
doc_append(Paragraph('Prices, sales dates and honesty', S['h1']))
doc_append(gold_rule())
doc_append(Paragraph('The 2026 dates that matter (verified September 2026)', S['h2']))
doc_append(table([
    [cellp('Event', 'cellb'), cellp('2026 date', 'cellb')],
    [cellp('Amazon Great Indian Festival opens (Prime early access 7 Oct)', 'cellh'), cellp('8 October')],
    [cellp('Flipkart Big Billion Days opens (Plus/Black early access 8 Oct)', 'cellh'), cellp('9 October')],
    [cellp('Navratri begins', 'cellh'), cellp('11 October')],
    [cellp('Dhanteras', 'cellh'), cellp('6 November')],
    [cellp('Diwali (Lakshmi Puja)', 'cellh'), cellp('8 November')],
    [cellp('Bhai Dooj', 'cellh'), cellp('11 November')],
], [None, 40 * mm]))
doc_append(Spacer(1, 6))
doc_append(P('Work backwards from these dates: listings should be refreshed 2-3 weeks ahead, '
             'and Meesho catalogs need their ~72-hour QC window plus buffer.', 'body'))

doc_append(Paragraph('The honesty rules that protect your account', S['h2']))
for b in bullets([
    '<b>Fake MRP is a penalty, not a tactic.</b> Meesho and Flipkart both penalise inflated MRPs and misleading discount displays. Prompt E3 flags the pattern before the platform does.',
    '<b>Never let AI invent specs.</b> One invented "waterproof" or wrong fabric percentage becomes returns, one-star reviews, and account flags. Facts from you, words from the AI.',
    '<b>Keyword stuffing backfires on every platform.</b> QC suppresses it, buyers distrust it, and AI search assistants skip it.',
    '<b>Keep your own scorecard.</b> Use the marketplaces\' AI tools for speed - but judge results on your own margin per unit, tracked outside the platform dashboard.',
]):
    doc_append(b)
doc_append(Spacer(1, 8))
doc_append(Paragraph('A final word', S['h2']))
doc_append(P('None of this needs talent. It needs one fact sheet per product, one workflow, and '
             'one weekly audit slot. The 44% of sellers using no AI are not your competition - '
             'they are your opportunity. Start with your best-selling listing, tonight, with '
             'prompt A1.'))

# ---------------------------------------------------------------- SOURCES

doc_append(PageBreak())
doc_append(Paragraph('APPENDIX', S['kicker']))
doc_append(Paragraph('Sources and verification', S['h1']))
doc_append(gold_rule())
doc_append(P('Every platform rule, statistic and date in this playbook was verified on '
             '23 September 2026 from the sources below. Rules change - always confirm current '
             'field limits inside Seller Central, Seller Hub or the Meesho Supplier Panel '
             'before bulk edits.', 'lead'))
for s_ in [
    'Amazon Seller Central (India) - "Updates to improve your product titles begin on July 27, 2026" seller forum announcement, June 2026',
    'Amazon Seller Central - Product Title Requirements and Guidelines; Product Image guide (500-10,000 px, white background RGB 255,255,255, 85% frame)',
    'Amazon Seller Central (India) - title policy of January 2025 (banned characters, word repetition)',
    'Keywords.am - "Amazon Character Limits 2026: The Complete Technical Reference" (India backend search terms: 200 bytes; bullets 10-255 chars, first 1,000 bytes indexed)',
    'supplier.meesho.com - How to Sell on Meesho (catalogs of 1-9 products, 3-4 per catalog recommended, 5-7 catalogs to start, ~72-hour go-live)',
    'Robnu and Lohar Studio - Meesho listing and title guidelines 2026 (50-120 character titles; 1000x1000 px square images; size-chart and HSN requirements)',
    'Inc42 - "Amazon, Flipkart & Meesho\'s AI Focus Shifts To Seller-Side Stacks", 18 August 2026 (1.7 Mn Amazon sellers; AI seller assistant on Bedrock; -10% listing errors, ~70% less routine work; Meesho 1.04 Mn transacting sellers, +81% YoY; Snapdeal Bharat Seller Report 2026: 44% no AI use, 46% derive 75%+ of business online; Flipkart Tier-3/4 onboarding +80-85%)',
    'The Hindu BusinessLine - "Meesho bets on agentic AI to become a business assistant for sellers", 23 July 2026 (Chorus platform extension to sellers)',
    'Base.com - "Top 20 Checks to Audit Your Flipkart Catalog Before Big Billion Days", August 2026 (Flipkart image QC, 1000x1000 px, title structure rules)',
    'Fynd Commerce docs - Flipkart Listing Management API image guidelines (JPEG, white background, minimum image count)',
    'Hindustan Times and Latestly, 20 September 2026 - Amazon Great Indian Festival 2026 opens 8 October (Prime early access 7 October)',
    'Zoutons - "India Festive Season Sales Statistics 2026", verified 22 September 2026 (Flipkart Big Billion Days 9 October, Plus/Black early access 8 October; Navratri 11 October; Dhanteras 6 November; Diwali 8 November; Bhai Dooj 11 November)',
    'ListingRVA AI - Flipkart product listing guide 2026 (1.4 Mn+ seller base; image and title standards)',
]:
    doc_append(Paragraph(s_, S['src'], bulletText='•'))
doc_append(Spacer(1, 10))
doc_append(HRFlowable(width='100%', thickness=1.1, color=GOLD, spaceAfter=6))
doc_append(Paragraph('The AI Listing Playbook - First Edition, September 2026 · '
                     'digitalaikart.shop · For personal use by the purchaser.', S['pnote']))

# ---------------------------------------------------------------- BUILD

doc = BaseDocTemplate(os.environ.get('OUT', 'downloads/ai-listing-playbook.pdf'), pagesize=A4,
                      leftMargin=18 * mm, rightMargin=18 * mm,
                      topMargin=14 * mm, bottomMargin=18 * mm,
                      title='The AI Listing Playbook - Meesho, Amazon, Flipkart',
                      author='Digitalaikart')
frame = Frame(18 * mm, 18 * mm, PAGE_W - 36 * mm, PAGE_H - 32 * mm, id='main')

cover_frame = Frame(18 * mm, 18 * mm, PAGE_W - 36 * mm, PAGE_H - 32 * mm, id='cover')

# First page uses cover painter; subsequent pages use on_page.
# We insert the TOC right after the cover page's frame content.
class _DocHack(BaseDocTemplate):
    pass

# Simplest: draw cover fully via onPage of a dedicated template, put TOC in frame 1.
story_with_toc = [Spacer(1, 1), NextPageTemplate('body'), PageBreak()] + build_toc() + story

tmpl_cover = PageTemplate('cover', frames=[cover_frame], onPage=cover)
tmpl_body = PageTemplate('body', frames=[frame], onPage=on_page)
doc.addPageTemplates([tmpl_cover, tmpl_body])

doc.build(story_with_toc, canvasmaker=_invariant_canvas)
print('built OK')
