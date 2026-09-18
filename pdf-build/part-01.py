#!/usr/bin/env python3
# Builds: The Festive Seller Playbook 2026 (digitalkartai.shop)
import os
import reportlab.rl_config
reportlab.rl_config.invariant = 1
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, NextPageTemplate,
                                ListFlowable, ListItem, KeepTogether, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents

NAVY = colors.HexColor("#0a1628")
NAVY2 = colors.HexColor("#13294b")
GOLD = colors.HexColor("#c9962e")
CREAM = colors.HexColor("#faf5e9")
LIGHT = colors.HexColor("#eef1f6")
INK = colors.HexColor("#1a2330")
GREY = colors.HexColor("#5a6472")

PAGE_W, PAGE_H = A4
M_L, M_R, M_T, M_B = 0.9*inch, 0.9*inch, 0.85*inch, 0.8*inch

styles = getSampleStyleSheet()

body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=10.5, leading=15, textColor=INK, spaceAfter=9,
                      alignment=TA_JUSTIFY)
lead = ParagraphStyle("lead", parent=body, fontSize=11.5, leading=17,
                      textColor=NAVY, spaceAfter=10)
H1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=17, leading=21,
                    textColor=NAVY, spaceBefore=16, spaceAfter=8, keepWithNext=1)
H2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=12.5, leading=16,
                    textColor=NAVY2, spaceBefore=12, spaceAfter=8, keepWithNext=1)
kicker = ParagraphStyle("kicker", fontName="Helvetica-Bold", fontSize=9, leading=12,
                        textColor=GOLD, spaceBefore=0, spaceAfter=2)
cell = ParagraphStyle("cell", parent=body, fontSize=9, leading=11.5, spaceAfter=0,
                      alignment=TA_LEFT)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
cellhead = ParagraphStyle("cellhead", parent=cell, fontName="Helvetica-Bold",
                          textColor=colors.white)
boxbody = ParagraphStyle("boxbody", parent=body, fontSize=10, leading=14, spaceAfter=0)
boxtitle = ParagraphStyle("boxtitle", fontName="Helvetica-Bold", fontSize=10.5,
                          leading=14, textColor=NAVY, spaceAfter=4)
quote = ParagraphStyle("quote", parent=body, fontName="Helvetica-Oblique",
                      fontSize=10.5, leading=15, textColor=NAVY2, alignment=TA_LEFT)

def P(t, s=body): return Paragraph(t, s)

def bullets(items, style=body):
    return ListFlowable([ListItem(Paragraph(t, style)) for t in items],
                        bulletType="bullet", leftIndent=14)

def numbered(items, style=body):
    return ListFlowable([ListItem(Paragraph(t, style)) for t in items],
                        bulletType="1", leftIndent=16)

def table(data, fracs, header=True, lightfill=LIGHT):
    cw = [f * (PAGE_W - M_L - M_R) for f in fracs]
    rows = []
    for i, r in enumerate(data):
        rows.append([Paragraph(c, cellhead if (header and i == 0) else cell) for c in r])
    t = Table(rows, colWidths=cw, repeatRows=1 if header else 0, hAlign="CENTER")
    st = [("VALIGN", (0,0), (-1,-1), "TOP"),
          ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
          ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
          ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#b8c0cc"))]
    if header:
        st += [("BACKGROUND", (0,0), (-1,0), NAVY),
               ("TEXTCOLOR", (0,0), (-1,0), colors.white)]
        for i in range(1, len(rows)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0,i), (-1,i), lightfill))
    t.setStyle(TableStyle(st))
    return t

def callout(title, text):
    inner = [Paragraph(title, boxtitle), Paragraph(text, boxbody)]
    t = Table([[inner]], colWidths=[(PAGE_W - M_L - M_R)])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CREAM),
        ("BOX", (0,0), (-1,-1), 0.8, GOLD),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("VALIGN", (0,0), (-1,-1), "TOP")]))
    return t

def goldline():
    t = Table([[""]], colWidths=[(PAGE_W - M_L - M_R)], rowHeights=[2])
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), GOLD),
                           ("TOPPADDING", (0,0), (-1,-1), 0),
                           ("BOTTOMPADDING", (0,0), (-1,-1), 0)]))
    return t

class PlaybookDoc(BaseDocTemplate):
    def afterFlowable(self, fl):
        if isinstance(fl, Paragraph):
            if fl.style.name == "H1":
                text = fl.getPlainText()
                self.notify("TOCEntry", (0, text, self.page))
                key = "h1-%d" % self.page
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=0, closed=False)

def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#13294b"))
    canvas.rect(0, 0, PAGE_W, 0.28*inch, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0.28*inch, PAGE_W, 0.045*inch, stroke=0, fill=1)
    # ornament band top
    canvas.setFillColor(colors.HexColor("#13294b"))
    canvas.rect(0, PAGE_H - 2.05*inch, PAGE_W, 1.9*inch, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE_H - 2.05*inch, PAGE_W, 0.045*inch, stroke=0, fill=1)
    cx = PAGE_W / 2
    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawCentredString(cx, PAGE_H - 1.35*inch, "DIGITALKARTAI  PRESENTS")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 33)
    canvas.drawCentredString(cx, PAGE_H - 2.85*inch, "The Festive Seller")
    canvas.drawCentredString(cx, PAGE_H - 3.42*inch, "Playbook 2026")
    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(cx, PAGE_H - 4.15*inch, "Big Billion Days. Great Indian Festival. Navratri to Diwali.")
    canvas.setFillColor(colors.HexColor("#c7d0dd"))
    canvas.setFont("Helvetica", 11.5)
    canvas.drawCentredString(cx, PAGE_H - 4.62*inch, "The complete small-seller playbook for India's biggest shopping season -")
    canvas.drawCentredString(cx, PAGE_H - 4.98*inch, "channels, pricing math, deals, ads, GST 2.0 and cash flow, verified for 2026.")
    # feature box
    bw, bh = 5.6*inch, 2.35*inch
    bx, by = cx - bw/2, PAGE_H - 8.0*inch
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(1)
    canvas.setFillColor(colors.HexColor("#0e1e38"))
    canvas.roundRect(bx, by, bw, bh, 10, stroke=1, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(cx, by + bh - 0.42*inch, "WHAT'S INSIDE")
    canvas.setFillColor(colors.HexColor("#c7d0dd"))
    canvas.setFont("Helvetica", 10.5)
    lines = [
        "The 2026 festive calendar with every date that matters",
        "Where the money is going: category-by-category growth",
        "A pricing worksheet that protects your margin",
        "The T-14 sprint checklist before the sales open",
        "GST 2.0 and cash-flow rules for marketplace sellers",
        "The Diwali second wave most sellers plan to miss",
    ]
    y = by + bh - 0.85*inch
    for ln in lines:
        canvas.setFillColor(GOLD); canvas.drawString(bx + 0.42*inch, y, ">>")
        canvas.setFillColor(colors.HexColor("#dfe6ef"))
        canvas.drawString(bx + 0.72*inch, y, ln)
        y -= 0.29*inch
    canvas.setFillColor(colors.HexColor("#8b98ab"))
    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(cx, 0.95*inch, "Digital Edition")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(cx, 0.62*inch, "digitalkartai.shop")
    canvas.restoreState()

def on_inner(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE_H - 0.16*inch, PAGE_W, 0.16*inch, stroke=0, fill=1)
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 8.5)
    canvas.drawString(M_L, PAGE_H - 0.42*inch, "THE FESTIVE SELLER PLAYBOOK 2026")
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawRightString(PAGE_W - M_R, PAGE_H - 0.42*inch, "digitalkartai.shop")
    canvas.setStrokeColor(colors.HexColor("#d5dae2"))
    canvas.setLineWidth(0.5)
    canvas.line(M_L, PAGE_H - 0.5*inch, PAGE_W - M_R, PAGE_H - 0.5*inch)
    canvas.line(M_L, 0.55*inch, PAGE_W - M_R, 0.55*inch)
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(M_L, 0.36*inch, "The Festive Seller Playbook 2026 - Digital Edition")
    canvas.drawRightString(PAGE_W - M_R, 0.36*inch, "Page %d" % canvas.getPageNumber())
    canvas.restoreState()

doc = PlaybookDoc("festive-seller-playbook-2026.pdf", pagesize=A4,
                  leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B,
                  title="The Festive Seller Playbook 2026",
                  author="digitalkartai.shop")
frame_cover = Frame(M_L, M_B, PAGE_W - M_L - M_R, PAGE_H - M_T - M_B, id="coverf")
frame_inner = Frame(M_L, M_B, PAGE_W - M_L - M_R, PAGE_H - M_T - M_B, id="innerf")
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[frame_cover], onPage=on_cover),
    PageTemplate(id="inner", frames=[frame_inner], onPage=on_inner),
])

story = []
story.append(NextPageTemplate("inner"))
story.append(Spacer(1, 1))
story.append(PageBreak())

# ---------- TOC ----------
story.append(Paragraph("Contents", ParagraphStyle("TOCHead", fontName="Helvetica-Bold",
             fontSize=17, leading=21, textColor=NAVY, spaceBefore=16, spaceAfter=8)))
story.append(goldline())
story.append(Spacer(1, 8))
toc = TableOfContents()
toc.levelStyles = [ParagraphStyle("toc1", fontName="Helvetica", fontSize=10.5,
                                  leading=17, textColor=INK, leftIndent=6)]
story.append(toc)
story.append(PageBreak())

# ================= 1 =================
story.append(P("1. The five-week window that pays for the whole year", H1))
story.append(P("Every September and October, Indian online retail compresses a quarter's worth of demand into about five weeks. In 2025 those weeks crossed Rs 1.15 lakh crore in gross sales for e-commerce platforms, growing 20 to 25 percent over the previous year. For 2026, Redseer Strategy Consultants - the Bengaluru firm whose festive estimates the industry treats as the reference - expects the festive window to grow about 25 percent again, to roughly USD 15-16 billion, with 180 to 185 million shoppers participating. India's full-year online retail is on track to cross USD 90 billion, the fastest growth in five years.", lead))
story.append(P("Two marketplace events anchor the season. Flipkart's Big Billion Days 2026 was announced on 16 September 2026: early access opens on 8 October for Flipkart Plus, Flipkart Black and Flipkart credit card members, and the public sale runs from 9 October. Amazon's Great Indian Festival had not announced official dates as this playbook went to press on 18 September 2026; reports tracking Amazon's own assistant point to a start between 27 September and 7 October, and the last three editions have all opened in the last week of September with roughly 24 hours of early access for Prime members. Treat that as the planning window, and watch Seller Central for the confirmed date."))
story.append(P("If you sell online in India - on Amazon, Flipkart, Meesho, ONDC, quick commerce apps, WhatsApp or Instagram - this is the one stretch of the year when buyers arrive without you having to pay full price to find them. It is also the stretch where an unprepared seller loses money faster than any other: fees, ad spend, stockouts and returns all scale with volume.", body))
story.append(P("This playbook is written for the small seller: the person running a catalogue of 5 to 500 products, often alone or with a tiny team, who cannot afford agencies or a ₹50,000-a-month ad budget. Everything here is something you can do yourself, starting this week.", body))
story.append(callout("How to use this playbook",
    "If you are already selling, start with Chapter 6 (the T-14 sprint) and Chapter 7 (pricing) - those are the chapters that decide whether this festive season makes you money. If you are starting from zero, read Chapters 4 and 5 first to pick your channel honestly, then aim at the Diwali wave rather than panic-registering this week. Chapters 10 and 11 (GST and cash flow) apply to everyone; they are where festive-season profits usually go to die."))
story.append(Spacer(1, 6))
story.append(P("A note on honesty: nothing in these pages guarantees sales. What it does guarantee is that you will avoid the predictable, boring mistakes - mispriced deals, GST surprises, cash stuck in settlements, dead stock in November - that separate the sellers who profit from the sellers who merely post big revenue numbers.", body))

story.append(P("Three sellers, three seasons", H2))
story.append(P("Where you start from decides which chapters are really for you, so place yourself honestly in one of these three seats.", body))
story.append(bullets([
