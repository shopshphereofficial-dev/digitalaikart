# -*- coding: utf-8 -*-
"""Build the UK Study & Graduate Route Playbook PDF."""

import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable, KeepTogether,
                                ListFlowable, ListItem, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

import content1
import content2
import content3

NAVY = colors.HexColor("#0a1628")
NAVY_LIGHT = colors.HexColor("#16294a")
GOLD = colors.HexColor("#c9a227")
INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#5a6270")
PAPER = colors.HexColor("#fbf9f4")
RULE = colors.HexColor("#d8d2c4")

TITLE = "The UK Study Visa & Graduate Route Playbook 2027"
SUBTITLE = "Indian Student Edition  -  the money rules, the application, and what to do after you land"
EDITION = "Updated 18 November 2026"

ss = getSampleStyleSheet()

BODY = ParagraphStyle("Body", parent=ss["Normal"], fontName="Helvetica", fontSize=10,
                      leading=14.5, textColor=INK, spaceAfter=7, alignment=TA_LEFT)
H1 = ParagraphStyle("H1", parent=BODY, fontName="Helvetica-Bold", fontSize=18,
                    leading=22, textColor=NAVY, spaceBefore=0, spaceAfter=2)
H2 = ParagraphStyle("H2", parent=BODY, fontName="Helvetica-Bold", fontSize=11.5,
                    leading=15, textColor=NAVY_LIGHT, spaceBefore=11, spaceAfter=4)
CELL = ParagraphStyle("Cell", parent=BODY, fontSize=8.6, leading=11.2, spaceAfter=0)
CELL_HEAD = ParagraphStyle("CellHead", parent=CELL, fontName="Helvetica-Bold",
                           textColor=colors.white)
CELL_B = ParagraphStyle("CellB", parent=CELL, fontName="Helvetica-Bold")
CALLOUT_T = ParagraphStyle("CalloutT", parent=BODY, fontName="Helvetica-Bold",
                           fontSize=9.6, leading=12.5, textColor=NAVY, spaceAfter=3)
CALLOUT_B = ParagraphStyle("CalloutB", parent=BODY, fontSize=9.4, leading=13, spaceAfter=0)
COVER_T = ParagraphStyle("CoverT", parent=BODY, fontName="Helvetica-Bold", fontSize=34,
                         leading=38, textColor=colors.white, alignment=TA_LEFT)
TOC_HEAD = ParagraphStyle("TocHead", parent=H1, spaceAfter=14)


class Doc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ("H1", "H2"):
            text = flowable.getPlainText()
            level = 0 if flowable.style.name == "H1" else 1
            key = "s%s" % self.seq.nextf("outline")
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text[:90], key, level=level, closed=(level > 0))
            self.notify("TOCEntry", (level, text, self.page, key))


def cover(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, h, stroke=0, fill=1)
    canvas.setFillColor(NAVY_LIGHT)
    canvas.rect(0, h - 3.05 * inch, w, 3.05 * inch, stroke=0, fill=1)

    canvas.setFillColor(GOLD)
    canvas.rect(0, h - 3.11 * inch, w, 0.06 * inch, stroke=0, fill=1)

    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(0.95 * inch, h - 1.05 * inch, "DIGITALKARTAI.SHOP  |  DIGITAL EDITION")
    canvas.setFillColor(colors.HexColor("#9fb0c9"))
    canvas.setFont("Helvetica", 10)
    canvas.drawString(0.95 * inch, h - 1.32 * inch, "Study  |  Student visa  |  Graduate Route  |  Skilled Worker")

    y = h - 2.05 * inch
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 33)
    for line in ["The UK Study Visa &", "Graduate Route", "Playbook 2027"]:
        canvas.drawString(0.95 * inch, y, line)
        y -= 0.52 * inch

    canvas.setFillColor(GOLD)
    canvas.rect(0.95 * inch, h - 4.05 * inch, 1.5 * inch, 0.035 * inch, stroke=0, fill=1)

    canvas.setFillColor(colors.HexColor("#d5dbe6"))
    canvas.setFont("Helvetica", 13.5)
    canvas.drawString(0.95 * inch, h - 4.42 * inch, "Indian Student Edition")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(0.95 * inch, h - 4.72 * inch,
                      "The money rules, the application, and what to do after you land")

    box_top = h - 5.55 * inch
    canvas.setFillColor(NAVY_LIGHT)
    canvas.rect(0.95 * inch, box_top - 2.35 * inch, w - 1.9 * inch, 2.35 * inch, stroke=0, fill=1)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.8)
    canvas.rect(0.95 * inch, box_top - 2.35 * inch, w - 1.9 * inch, 2.35 * inch, stroke=1, fill=0)

    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 9.5)
    canvas.drawString(1.2 * inch, box_top - 0.36 * inch, "WHAT CHANGED FOR THE 2027 CYCLE")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 10)
    lines = [
        "Funds you must show rise on 30 November 2026 to GBP 1,570 a month in London",
        "and GBP 1,203 outside London - with the exact bank-balance arithmetic worked",
        "for four real cases, including the 28-day and 31-day clocks.",
        "",
        "The Graduate Route drops to 18 months for applications made on or after",
        "1 January 2027, with a two-year exception announced but not yet defined.",
        "31 chapters, worked cost tables, 7 printable worksheets, 4 negotiation letters.",
    ]
    yy = box_top - 0.66 * inch
    for line in lines:
        canvas.drawString(1.2 * inch, yy, line)
        yy -= 0.185 * inch

    canvas.setFillColor(colors.HexColor("#8fa1bb"))
    canvas.setFont("Helvetica", 9)
    canvas.drawString(0.95 * inch, 1.35 * inch, EDITION)
    canvas.drawString(0.95 * inch, 1.15 * inch,
                      "Figures checked against GOV.UK, the Home Office fee tables and the September 2026 statement of changes.")
    canvas.setFillColor(GOLD)
    canvas.rect(0.95 * inch, 0.95 * inch, w - 1.9 * inch, 0.02 * inch, stroke=0, fill=1)
    canvas.restoreState()


def footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.6)
    canvas.drawString(doc.leftMargin, 0.62 * inch, "The UK Study Visa & Graduate Route Playbook 2027")
    canvas.drawRightString(w - doc.rightMargin, 0.62 * inch, str(canvas.getPageNumber()))
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 0.78 * inch, w - doc.rightMargin, 0.78 * inch)
    canvas.restoreState()


def table_from(spec, doc_width):
    headers, rows, fracs = spec
    assert abs(sum(fracs) - 1.0) < 1e-6, fracs
    data = [[Paragraph(h, CELL_HEAD) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), CELL if i == 0 else CELL) for i, c in enumerate(r)])
    t = Table(data, colWidths=[f * doc_width for f in fracs], repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), PAPER))
    t.setStyle(TableStyle(style))
    return t


def callout(title, text, doc_width):
    inner = [Paragraph(title, CALLOUT_T), Paragraph(text, CALLOUT_B)]
    t = Table([[inner]], colWidths=[doc_width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fdf6e3")),
        ("LINEBEFORE", (0, 0), (0, -1), 3, GOLD),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def build(path):
    doc = Doc(path, pagesize=A4, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
              topMargin=0.95 * inch, bottomMargin=1.0 * inch,
              title=TITLE, author="DigitalKartAI", subject=SUBTITLE,
              creator="digitalkartai.shop")

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[Frame(0, 0, A4[0], A4[1], id="c")], onPage=cover),
        PageTemplate(id="Body", frames=[frame], onPage=footer),
    ])

    story = [Spacer(1, 1), NextPageTemplate("Body"), PageBreak()]

    # TOC
    story.append(Paragraph("Contents", TOC_HEAD))
    story.append(HRFlowable(width="100%", thickness=1.1, color=GOLD, spaceBefore=0, spaceAfter=12))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("toc0", fontName="Helvetica-Bold", fontSize=10.2, leading=15,
                       textColor=NAVY, leftIndent=0, firstLineIndent=0, spaceBefore=3),
        ParagraphStyle("toc1", fontName="Helvetica", fontSize=9, leading=12.5,
                       textColor=MUTED, leftIndent=16, firstLineIndent=0),
    ]
    toc.dotsMinLevel = 0
    story.append(toc)
    story.append(PageBreak())

    blocks = content1.BLOCKS + content2.BLOCKS + content3.BLOCKS
    for kind, val in blocks:
        if kind == "h1":
            story.append(Paragraph(val, H1))
            story.append(HRFlowable(width="100%", thickness=1.0, color=GOLD,
                                    spaceBefore=3, spaceAfter=10))
        elif kind == "h2":
            story.append(Paragraph(val, H2))
        elif kind == "p":
            story.append(Paragraph(val, BODY))
        elif kind == "b":
            story.append(ListFlowable(
                [ListItem(Paragraph(x, BODY), leftIndent=14) for x in val],
                bulletType="bullet", start="square", leftIndent=14,
                bulletFontSize=7, bulletColor=GOLD, spaceAfter=8))
        elif kind == "n":
            story.append(ListFlowable(
                [ListItem(Paragraph(x, BODY), leftIndent=18) for x in val],
                bulletType="1", leftIndent=18, bulletFontSize=9,
                bulletColor=NAVY, spaceAfter=8))
        elif kind == "t":
            story.append(Spacer(1, 3))
            story.append(table_from(val, doc.width))
            story.append(Spacer(1, 9))
        elif kind == "call":
            story.append(Spacer(1, 4))
            story.append(callout(val[0], val[1], doc.width))
            story.append(Spacer(1, 9))
        elif kind == "pb":
            story.append(PageBreak())

    doc.multiBuild(story)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "uk-playbook.pdf"
    print(build(out))
