#!/usr/bin/env python3
# Premium PDF builder for "The Dhanteras & Diwali 2026 Gold Buying Playbook".
# Navy #0a1628 / gold #f5c542. Built with reportlab. DejaVu fonts used so the
# rupee sign and tick/arrow glyphs render correctly.
import os, sys

os.environ.setdefault("SOURCE_DATE_EPOCH", "1760000000")
import reportlab.rl_config as rl_config
rl_config.invariant = 1

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

FDIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DJV", os.path.join(FDIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJVB", os.path.join(FDIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DJVI", os.path.join(FDIR, "DejaVuSans-Oblique.ttf")))

OUT = sys.argv[1] if len(sys.argv) > 1 else "dhanteras-diwali-2026-gold-buying-playbook.pdf"

W, H = A4
M = 56
CW = W - 2 * M
NAVY = HexColor("#0a1628")
NAVY_DEEP = HexColor("#060f1d")
CARD = HexColor("#122238")
CARD2 = HexColor("#16293f")
GOLD = HexColor("#f5c542")
GOLD_DIM = HexColor("#b9902f")
TEXT = HexColor("#dbe4f0")
MUTED = HexColor("#8fa3bf")
WHITE = HexColor("#ffffff")

F = "DJV"
FB = "DJVB"
FI = "DJVI"

TITLE = "THE DHANTERAS & DIWALI 2026 GOLD BUYING PLAYBOOK"
RS = "\u20b9"


def wrap(text, font, size, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Doc:
    def __init__(self, path):
        self.c = rl_canvas.Canvas(path, pagesize=A4)
        self.c.setTitle("The Dhanteras & Diwali 2026 Gold Buying Playbook — India Edition")
        self.c.setAuthor("Faisal Fayaz Lone")
        self.c.setSubject("How to buy gold in India this festive season without overpaying or getting cheated")
        self.c.setCreator("Digitalaikart")
        self.page = 0
        self.y = 0
        self.chapter = ""
        self._first = True
        self.toc = []

    def bg(self):
        c = self.c
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, H - 6, W, 6, stroke=0, fill=1)
        c.setFillColor(NAVY_DEEP)
        c.rect(0, 0, W, 34, stroke=0, fill=1)
        c.setFillColor(GOLD_DIM)
        c.rect(0, 34, W, 0.7, stroke=0, fill=1)

    def footer(self):
        c = self.c
        c.setFillColor(MUTED)
        c.setFont(F, 7.6)
        c.drawString(M, 14, "Digitalaikart  \u00b7  Gold Buying Playbook 2026")
        c.drawRightString(W - M, 14, "Page %d" % self.page)

    def new_page(self):
        if not self._first:
            self.footer()
            self.c.showPage()
        self._first = False
        self.page += 1
        self.bg()
        self.y = H - 74

    def need(self, h):
        if self.y - h < 66:
            self.new_page()

    # ---------- blocks ----------
    def cover(self):
        self.new_page()
        c = self.c
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.4)
        c.rect(38, 38, W - 76, H - 76, stroke=1, fill=0)
        c.setStrokeColor(GOLD_DIM)
        c.setLineWidth(0.6)
        c.rect(46, 46, W - 92, H - 92, stroke=1, fill=0)
        c.setFillColor(GOLD)
        c.setFont(FB, 10.5)
        c.drawCentredString(W / 2, H - 116, "D I G I T A L A I K A R T   O R I G I N A L")
        c.setFillColor(WHITE)
        c.setFont(FB, 33)
        c.drawCentredString(W / 2, H - 232, "THE DHANTERAS &")
        c.setFillColor(GOLD)
        c.setFont(FB, 40)
        c.drawCentredString(W / 2, H - 282, "DIWALI 2026")
        c.setFillColor(WHITE)
        c.setFont(FB, 26)
        c.drawCentredString(W / 2, H - 322, "GOLD BUYING PLAYBOOK")
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.line(W / 2 - 80, H - 350, W / 2 + 80, H - 350)
        c.setFillColor(TEXT)
        c.setFont(FB, 13)
        c.drawCentredString(W / 2, H - 388, "Buy gold this festive season without overpaying,")
        c.drawCentredString(W / 2, H - 408, "getting cheated, or choosing the wrong form.")
        c.setFillColor(MUTED)
        c.setFont(F, 11)
        c.drawCentredString(W / 2, H - 452, "India Edition  \u00b7  Verified October 2026")
        c.drawCentredString(W / 2, H - 474, "Prices  \u00b7  Hallmarking  \u00b7  Muhurat  \u00b7  GST  \u00b7  Capital-gains tax  \u00b7  ETF vs digital vs physical")
        c.setFillColor(WHITE)
        c.setFont(FB, 12)
        c.drawCentredString(W / 2, 196, "FAISAL FAYAZ LONE")
        c.setFillColor(MUTED)
        c.setFont(F, 10)
        c.drawCentredString(W / 2, 178, "First Edition \u00b7 October 2026")
        c.setFont(F, 8.4)
        c.drawCentredString(W / 2, 122, "Verified against IBJA/All India Bullion rates, the Ministry of Finance customs")
        c.drawCentredString(W / 2, 109, "notifications of 12 May 2026, the Income-tax Act 2025, BIS hallmarking rules")
        c.drawCentredString(W / 2, 96, "and Budget 2026 SGB changes.")
        c.setFillColor(GOLD)
        c.setFont(FB, 9)
        c.drawCentredString(W / 2, 68, "digitalkartai.shop")

    def h1(self, text):
        self.need(74)
        self.chapter = text
        self.toc.append((text, self.page))
        self.c.bookmarkPage("ch%d" % len(self.toc))
        self.c.addOutlineEntry(text, "ch%d" % len(self.toc), level=0)
        self.y -= 8
        self.c.setFillColor(GOLD)
        self.c.setFont(FB, 19)
        for ln in wrap(text, FB, 19, CW):
            self.c.drawString(M, self.y, ln)
            self.y -= 23
        self.y += 6
        self.c.setStrokeColor(GOLD)
        self.c.setLineWidth(1.6)
        self.c.line(M, self.y, M + 62, self.y)
        self.y -= 20

    def h2(self, text):
        self.need(46)
        self.y -= 6
        self.c.setFillColor(GOLD)
        self.c.setFont(FB, 13)
        for ln in wrap(text, FB, 13, CW):
            self.c.drawString(M, self.y, ln)
            self.y -= 17
        self.y -= 4

    def h3(self, text):
        self.need(34)
        self.c.setFillColor(WHITE)
        self.c.setFont(FB, 10.8)
        for ln in wrap(text, FB, 10.8, CW):
            self.c.drawString(M, self.y, ln)
            self.y -= 15
        self.y -= 3

    def p(self, text, color=None, size=10.2, font=F, lead=14.8):
        color = color or TEXT
        for ln in wrap(text, font, size, CW):
            self.need(lead)
            self.c.setFillColor(color)
            self.c.setFont(font, size)
            self.c.drawString(M, self.y, ln)
            self.y -= lead
        self.y -= 5

    def bullet(self, text, size=10.0):
        for i, ln in enumerate(wrap(text, F, size, CW - 16)):
            self.need(14.2)
            self.c.setFillColor(GOLD if i == 0 else TEXT)
            self.c.setFont(F, size)
            if i == 0:
                self.c.drawString(M + 2, self.y, "\u2022")
            self.c.drawString(M + 16, self.y, ln)
            self.y -= 14.2
        self.y -= 2

    def numbered(self, n, text, size=10.0):
        for i, ln in enumerate(wrap(text, F, size, CW - 22)):
            self.need(14.2)
            self.c.setFillColor(GOLD if i == 0 else TEXT)
            self.c.setFont(FB if i == 0 else F, size)
            if i == 0:
                self.c.drawString(M + 2, self.y, "%d." % n)
            self.c.drawString(M + 22, self.y, ln)
            self.y -= 14.2
        self.y -= 2

    def callout(self, title, text, fill=None):
        inner = CW - 30
        tlines = wrap(title, FB, 10.2, inner)
        blines = wrap(text, F, 9.6, inner)
        h = 14 + len(tlines) * 14 + len(blines) * 12.9 + 12
        self.need(h + 6)
        c = self.c
        top = self.y + 6
        c.setFillColor(fill or CARD2)
        c.rect(M, top - h, CW, h, stroke=0, fill=1)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1)
        c.rect(M, top - h, CW, h, stroke=1, fill=0)
        yy = top - 17
        c.setFillColor(GOLD)
        c.setFont(FB, 10.2)
        for ln in tlines:
            c.drawString(M + 15, yy, ln)
            yy -= 14
        c.setFillColor(TEXT)
        c.setFont(F, 9.6)
        for ln in blines:
            c.drawString(M + 15, yy, ln)
            yy -= 12.9
        self.y = top - h - 8

    def table(self, headers, rows, widths=None, size=8.8):
        n = len(headers)
        if not widths:
            widths = [CW / n] * n
        total = sum(widths)
        widths = [w / total * CW for w in widths]
        hh = 22
        self.need(hh + 20)
        c = self.c
        c.setFillColor(GOLD)
        c.rect(M, self.y - hh + 12, CW, hh, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont(FB, size)
        x = M
        for i, hd in enumerate(headers):
            c.drawString(x + 6, self.y - hh + 18, hd)
            x += widths[i]
        self.y -= hh - 12
        for ri, row in enumerate(rows):
            cells = [wrap(str(cell), F, size, widths[i] - 12) for i, cell in enumerate(row)]
            rh = max(len(c) for c in cells) * 11.9 + 9
            self.need(rh)
            c.setFillColor(CARD if ri % 2 == 0 else NAVY_DEEP)
            c.rect(M, self.y - rh, CW, rh, stroke=0, fill=1)
            c.setFillColor(TEXT)
            c.setFont(F, size)
            x = M
            for i, cell in enumerate(cells):
                yy = self.y - 13
                for ln in cell:
                    c.drawString(x + 6, yy, ln)
                    yy -= 11.9
                x += widths[i]
            self.y -= rh
        self.y -= 8

    def spacer(self, h=8):
        self.y -= h

    def finish(self):
        self.footer()
        self.c.showPage()
        self.c.save()


d = Doc(OUT)

# ======================= COVER =======================
d.cover()

# ======================= HOW TO USE =======================
d.new_page()
d.h1("How to Use This Playbook")
d.p("India buys more gold than any country on earth, and almost all of it is bought in the "
    "few weeks between Dhanteras and the wedding season. This year that buying happens at "
    "record prices. On 7 October 2026, 24K gold was around " + RS + "14,957 a gram \u2014 about " +
    RS + "1.50 lakh for 10 grams, and roughly 22% higher than a year earlier. Silver was near " +
    RS + "2.28 lakh a kilo.")
d.p("At those numbers, the small decisions matter more than they ever did. The difference between "
    "a well-bought purchase and a badly-bought one is not the day you choose. It is the form you "
    "buy, the making charge you agree to, and whether the piece is genuinely hallmarked. On a " +
    RS + "1.5 lakh purchase those three things can swing your outcome by " + RS + "30,000 or more.")
d.p("This playbook is written to be used, not read once. It is organised so you can go straight "
    "to the part you need:")
d.bullet("Part 1 \u2014 what gold costs right now and why 2026 is different (the price, the import-duty shock, the September correction).")
d.bullet("Part 2 \u2014 the exact 2026 dates, the Dhanteras puja window city by city, and the truth about the \u201cbuying muhurat\u201d.")
d.bullet("Part 3 \u2014 the form decision: jewellery, coins, ETF, gold fund, digital gold or SGB \u2014 and the maths that shows which one costs you least.")
d.bullet("Part 4 \u2014 how to buy physical gold without getting cheated: hallmarking, HUID, the invoice, making charges, buyback.")
d.bullet("Part 5 \u2014 the investment forms decoded, including the Budget 2026 change that killed the Sovereign Gold Bond's tax edge for secondary buyers.")
d.bullet("Part 6 \u2014 capital-gains tax on gold in FY 2026-27, in one table.")
d.bullet("Part 7 \u2014 storage, safety, and the scams that spike every festive season.")
d.bullet("Part 8 \u2014 a printable Dhanteras buying checklist.")
d.bullet("Part 9 \u2014 a budget-to-form plan for " + RS + "25,000, " + RS + "50,000 and " + RS + "1 lakh.")
d.bullet("Part 10 \u2014 the honest price outlook, and why you should stop trying to time the market.")
d.callout("A word on accuracy",
          "Every price, tax rate, fee and rule here was checked in October 2026 against official or "
          "primary sources \u2014 IBJA/All India Bullion reference rates, the Ministry of Finance customs "
          "notifications dated 12 May 2026, BIS hallmarking rules, the Income-tax Act 2025 and Budget "
          "2026. Gold moves daily; treat the price figures as the level at the time of writing and "
          "always confirm today's rate before you buy.")

# ======================= PART 1 =======================
d.new_page()
d.h1("Part 1 \u00b7 The 2026 Price Reality")
d.h2("Where gold stands today")
d.p("Gold in India is quoted per 10 grams for 24K (999 purity). On 7 October 2026 the India-wide "
    "reference was about " + RS + "1,49,570 to " + RS + "1,49,987 per 10 grams, or roughly " +
    RS + "14,957 a gram. That is about 22% higher than a year earlier. Jewellery is usually 22K "
    "(91.6% purity), which is priced lower than 24K.")
d.table(
    ["Purity", "Per gram", "Per 10 g", "Typical use"],
    [["24K (999)", RS + "14,957\u201315,006", RS + "1,49,570\u20131,50,060", "Coins, bars, investment"],
     ["22K (916)", RS + "13,710", RS + "1,37,100", "Most jewellery"],
     ["18K (750)", RS + "11,218", RS + "1,12,180", "Studded / light jewellery"],
     ["Silver (999)", RS + "228\u2013229", RS + "2,28,000/kg", "Coins, utensils, gifting"]],
    widths=[2, 2.4, 2.6, 3])
d.p("These are bullion-level reference rates. A jeweller's invoice adds making charges, sometimes "
    "wastage, and GST on top \u2014 none of which the published rate carries. Part 4 shows you exactly "
    "how to read that invoice.", color=MUTED, size=9.6)
d.h2("Why 2026 is different from every previous Dhanteras")
d.h3("1. Import duty jumped from 6% to 15% in May")
d.p("On 13 May 2026 the government raised the effective import duty on gold and silver to 15% \u2014 "
    "a 10% basic customs duty plus a 5% Agriculture Infrastructure and Development Cess \u2014 up from "
    "6%. The move came days after the Prime Minister publicly urged Indians to pause gold buying for "
    "a year, as record imports pressured the rupee. This duty is already baked into the domestic "
    "price you see; you do not pay it separately at the counter, but it is one reason the local "
    "price sits where it does.")
d.h3("2. Gold corrected hard in September, then steadied")
d.p("After a record run, gold fell about 6.5% during September 2026 \u2014 its worst month since June \u2014 "
    "as US bond yields hit multi-year highs and the dollar firmed. It stabilised in early October. "
    "That single month shows how fast this market can move, in both directions.")
d.h3("3. Indians are shifting from jewellery to investment gold")
d.p("Under record prices, Indian buyers have not stopped buying gold \u2014 they have changed what they "
    "buy. In the first quarter of 2026, bars and coins made up 52% of India's total domestic gold "
    "demand, the highest share on record since 2013, up from 42% a year earlier, even as jewellery "
    "volumes softened. That shift is the single most useful thing to understand before Dhanteras: "
    "the metal is the investment; the jewellery is the occasion.")
d.callout("The takeaway",
          "You are buying in a high-price, high-volatility year. That is not a reason to skip the "
          "purchase \u2014 festive buying is a tradition and, done sensibly, a sensible long-term asset. "
          "It is a reason to get the form, the charge and the hallmark right.")

# ======================= PART 2 =======================
d.new_page()
d.h1("Part 2 \u00b7 The Dates and the Muhurat Truth")
d.h2("The five days of Diwali 2026")
d.p("Diwali 2026 runs across five days. The day that matters for gold is the first one.")
d.table(
    ["Day", "Date (2026)", "What it is"],
    [["Dhanteras", "Fri, 6 November", "First day \u2014 the traditional gold, silver and utensil buying day"],
     ["Naraka Chaturdasi", "Sat, 7 November", "Choti Diwali \u2014 the ritual oil bath"],
     ["Diwali / Lakshmi Puja", "Sun, 8 November", "Main day \u2014 evening Lakshmi\u2013Ganesh puja"],
     ["Govardhan Puja", "Mon, 9 November", "Annakut"],
     ["Bhai Dooj", "Tue, 10 November", "Final day"]],
    widths=[2.6, 2.6, 6])
d.p("Dhanteras 2026 is Friday, 6 November. Note that some calendars print 7 November. The reason is "
    "a genuine calendrical subtlety: the Trayodashi tithi that names the festival begins only at "
    "about 10:31 AM on the 6th and ends around 10:49 AM on the 7th, so a calendar that assigns the "
    "day by whichever tithi is running at sunrise lands on the 7th. But Dhanteras is an evening "
    "festival \u2014 the puja and the buying belong to the twilight after sunset \u2014 and that evening on "
    "the 6th falls squarely inside Trayodashi, while by sunset on the 7th the tithi has already "
    "moved on. The correct date is 6 November.", color=TEXT, size=9.9)
d.h2("The puja window (pradosh kaal), city by city")
d.p("The Lakshmi\u2013Kubera\u2013Dhanvantari puja is kept in the pradosh kaal \u2014 the roughly two-and-a-half "
    "hours after sunset. Because sunset is a local event, the window shifts from city to city. "
    "Approximate 6 November 2026 windows:")
d.table(
    ["City", "Pradosh window", "City", "Pradosh window"],
    [["Delhi", "5:31 \u2013 8:09 PM", "Hyderabad", "5:41 \u2013 8:12 PM"],
     ["Mumbai", "6:01 \u2013 8:34 PM", "Pune", "5:58 \u2013 8:30 PM"],
     ["Kolkata", "4:55 \u2013 7:29 PM", "Ahmedabad", "5:57 \u2013 8:32 PM"],
     ["Chennai", "5:39 \u2013 8:08 PM", "Jaipur", "5:39 \u2013 8:16 PM"],
     ["Bengaluru", "5:50 \u2013 8:19 PM", "Lucknow", "5:19 \u2013 7:55 PM"]],
    widths=[2.2, 3.2, 2.2, 3.2])
d.p("These are for the puja. Confirm your own city's exact sunset on a live panchang before you sit "
    "for it \u2014 the window moves with your longitude.", color=MUTED, size=9.5)
d.h2("The muhurat truth: what is real and what is marketing")
d.callout("The buying muhurat is a myth you are sold every year",
          "Published guides tell you a purchase must happen inside the pradosh window \u201cor the benefit "
          "is lost.\u201d That is retail messaging, not shastra. Classical sources fix the puja to the "
          "pradosh window; they do not fix the purchase to it. Buying metal is auspicious through the "
          "whole of Trayodashi \u2014 effectively all of 6 November and into the morning of the 7th. "
          "Jewellers compress a full day of buying into a tight evening slot because a customer who "
          "believes the window is closing buys faster and asks fewer questions about price. Buy when "
          "the shop is calm and the piece is right.")
d.h2("A calmer alternative: Pushya Nakshatra")
d.p("Pushya is traditionally regarded as at least as auspicious as Dhanteras for buying gold, and in "
    "2026 it falls on 31 October and 1 November \u2014 five days before Dhanteras. Shops are far less "
    "crowded, which means more time and, often, more room to negotiate the making charge. If your "
    "family is flexible on the date, this is worth considering.")
d.h2("What people actually buy on Dhanteras")
d.bullet("Metal \u2014 gold or silver coins, bars, or a piece of jewellery. Gold if the household can; silver or a steel/brass utensil otherwise.")
d.bullet("A new broom (jhadu), treated as a form of Lakshmi that sweeps out want, and often worshipped before first use.")
d.bullet("Utensils, coriander seeds, and \u2014 since Dhanteras honours Dhanvantari, the physician-god \u2014 sometimes a token of ayurveda or medicine.")
d.bullet("The classic token: a small metal coin kept in the puja and never spent.")

# ======================= PART 3 =======================
d.new_page()
d.h1("Part 3 \u00b7 The Form Decision \u2014 Where Your Money Goes")
d.p("This is the most important decision you will make this Dhanteras, and the one most buyers get "
    "wrong. The price of gold is the same whichever form you buy. What differs is cost, storage, "
    "liquidity, purity certainty and tax. For an asset you intend to sell later, those five things "
    "decide your outcome as much as the metal's price does.")
d.h2("The six ways Indians own gold")
d.table(
    ["Form", "Entry cost", "Storage", "Liquidity", "Purity"],
    [["Jewellery", "High: 8\u201325% making + 3% GST + 5% GST on making", "Yours (locker/home)", "Sell to jeweller, at a haircut", "Check hallmark"],
     ["Coins / bars", "Low: ~2\u20135% premium + 3% GST", "Yours", "Sell to dealer", "Stamped, usually 24K"],
     ["Gold ETF", "Low: ~0.5\u20131% a year", "None (demat)", "Sells on the exchange in seconds", "Standardised, vaulted"],
     ["Gold fund-of-funds", "Low + double layer of fees", "None", "NAV, no intraday", "Standardised"],
     ["Digital gold", "3% GST + 3\u20135% platform spread", "Provider vaults it", "Sell back on the platform", "Provider-certified"],
     ["Existing SGB", "Bought on the exchange", "None (demat)", "Thin exchange volumes", "Government-backed"]],
    widths=[1.9, 3.4, 2.1, 2.5, 2.0])
d.h2("The maths: " + RS + "1.5 lakh of gold, three ways")
d.p("Take a purchase with a gold value of about " + RS + "1,37,100 (10 grams of 22K at " +
    RS + "13,710 a gram), and follow it through three forms.")
d.h3("As a 22K chain (consumption)")
d.p("Gold value " + RS + "1,37,100. Add 12% making charge " + RS + "16,452. Add GST: 3% on the gold "
    "(" + RS + "4,113) plus 5% on the making charge (" + RS + "823). You pay roughly " + RS + "1,58,488 "
    "at the counter. On resale you would typically recover only the gold value minus a jeweller's "
    "deduction \u2014 say " + RS + "1,25,000 to " + RS + "1,30,000. The immediate gap is " +
    RS + "28,000 to " + RS + "33,000, or 18\u201322%. The making charge and GST are pure, unrecoverable "
    "cost.")
d.h3("As a gold ETF (investment)")
d.p("You buy units tracking the gold price. No making charge, no GST, no locker. You pay a small "
    "brokerage and an annual expense ratio of about 0.5\u20131%. On " + RS + "1.5 lakh that is roughly " +
    RS + "750\u20131,500 a year. You can sell in seconds on the exchange.")
d.h3("As digital gold (convenience)")
d.p("You pay the live rate plus a platform spread of about 3\u20135%, and 3% GST. There is no demat and "
    "you can start from " + RS + "1, but the round-trip cost (buy spread plus sell spread) typically "
    "runs to several thousand rupees on a " + RS + "1.5 lakh holding, and the product is not regulated "
    "the way a listed fund is.")
d.callout("The rule that saves you the most money",
          "Decide the purpose first, then pick the form. If the gold is for wearing or gifting, buy "
          "the piece \u2014 that is what jewellery is for, and the making charge is the price of the "
          "occasion. If the gold is to save and later sell, buy the metal: coins or bars if you want "
          "something in your hand, a gold ETF if you have a demat account and want the lowest cost and "
          "best liquidity. Do not buy a high-making-charge ornament as an \u201cinvestment\u201d and then "
          "resent the loss on resale. Purpose first, form second.")

# ======================= PART 4 =======================
d.new_page()
d.h1("Part 4 \u00b7 Buying Physical Gold Without Getting Cheated")
d.p("Physical gold is the form most families buy, and the form with the most room for sharp practice. "
    "Almost all of it is preventable with five checks.")
d.h2("Check 1 \u2014 Hallmarking: the three marks and the HUID")
d.p("Since 2021, every piece of gold jewellery legally sold in India must carry a BIS hallmark with "
    "three things:")
d.bullet("The BIS logo \u2014 the triangular Bureau of Indian Standards mark.")
d.bullet("A purity / fineness stamp: 22K916 for 22 carat (91.6%), 18K750 for 18 carat (75%), 14K585 for 14 carat.")
d.bullet("A six-digit alphanumeric HUID \u2014 the Hallmark Unique Identification code, laser-etched on the piece.")
d.p("The HUID is your proof. Open the BIS Care app, use \u201cVerify HUID\u201d, and enter the six-digit code. "
    "It will show the jeweller's registration, the hallmarking date, the purity, the article type and "
    "the hallmarking centre. If it returns \u201cNo record found\u201d, treat the piece as unverified and walk "
    "away. This takes thirty seconds and is the single best fraud check you have.")
d.h2("Check 2 \u2014 The invoice is your legal safeguard")
d.p("A proper invoice must show the HUID, the weight, the gold rate applied, and the making charges "
    "separately. Without it you cannot complain effectively through the BIS Care app, and many "
    "jewellers will not give full buyback value. Never accept a handwritten slip that just says "
    "\u201cgold chain \u2014 8g\u201d.")
d.h2("Check 3 \u2014 Making charges: negotiate them as a percentage")
d.p("Making charges on jewellery run from about 8% to 25% of the gold value; machine-made and light "
    "pieces sit at the low end, heavy hand-crafted sets at the high end. Coins and bars carry only a "
    "small premium of about 2\u20135%. Two practical rules:")
d.numbered(1, "Always ask for the making charge as a percentage, not a lump sum. A percentage is comparable across shops; a lump sum is not.")
d.numbered(2, "Ask separately about \u201cwastage\u201d. Some jewellers fold a wastage charge into the price. If it is not on the invoice, it should not be in the price.")
d.p("On a " + RS + "1.5 lakh purchase, moving the making charge from 18% to 10% saves roughly " +
    RS + "11,000. That is more than the entire price difference between two Dhanteras dates. Spend "
    "your energy on the charge, not the day.", color=TEXT)
d.h2("Check 4 \u2014 Don't pay a 24K rate for 22K gold")
d.p("Most jewellery is 22K, which is 91.6% pure and therefore cheaper per gram than 24K. Confirm "
    "which rate the shop is applying, and that it matches the purity stamp. A shop that quotes the "
    "24K rate and sells you 22K has overcharged you by about 8\u20139%.")
d.h2("Check 5 \u2014 Ask the buyback terms before you pay")
d.p("Buyback policy varies hugely. Ask, in writing on the invoice if possible: what deduction will "
    "the shop apply if you sell this piece back, and will it buy back at all? Jewellery loses the "
    "making charge on resale; coins and bars recover far better because they carry only a small "
    "premium. If the answer is vague, that is your answer.")
d.callout("Old-gold exchange and \u201cgold savings schemes\u201d",
          "Two festive-season traps. First, old-gold exchange: the shop values your old gold at a "
          "deduction (often 10\u201320%) and then sells you new gold at full making charges \u2014 you can lose "
          "on both ends. Get the old gold valued independently first. Second, monthly gold savings "
          "schemes: read the fine print on the making-charge waiver, the exit rules and what happens "
          "if gold prices fall. A scheme that locks you into buying jewellery at the end is a "
          "jewellery purchase, not an investment.")

# ======================= PART 5 =======================
d.new_page()
d.h1("Part 5 \u00b7 The Investment Forms, Decoded")
d.h2("Gold ETFs")
d.p("A gold ETF is a fund listed on NSE/BSE whose units track the domestic gold price, usually one "
    "unit to about one gram. You need a demat and trading account. It is SEBI-regulated, has no "
    "making charges, no locker and no purity doubt, and sells on the exchange in seconds.")
d.bullet("Cost: an annual expense ratio of about 0.5\u20131%, plus small brokerage.")
d.bullet("Check the portfolio: SEBI requires at least 95% in gold and related instruments, but that can include derivatives. Prefer ETFs with higher physical backing and lower derivative exposure.")
d.bullet("Compare the market price with the iNAV (indicative net asset value) so you do not buy at an inflated premium.")
d.h2("Gold fund-of-funds")
d.p("These invest in gold ETFs but are bought and sold like any mutual fund, so no demat account is "
    "needed and you can run a SIP. The trade-off: you bear both the fund's expenses and the "
    "underlying ETF's, redemptions happen only at NAV (no intraday liquidity), and there can be "
    "tracking error. Convenient, slightly more expensive.")
d.h2("Digital gold")
d.p("Digital gold lets you buy tiny amounts online, with the provider vaulting the equivalent "
    "physical metal. You can start from about " + RS + "1, there is no demat, and you can sell back "
    "on the platform or, on some platforms, take physical delivery once your holding crosses a "
    "threshold. The catch: digital gold is not regulated by the RBI or SEBI the way a listed fund "
    "is, and buy\u2013sell spreads and fees vary by platform. Read the terms before you start. It is a "
    "reasonable tool for very small, regular saving; it is not the cheapest way to hold a large "
    "investment.")
d.h2("Sovereign Gold Bonds \u2014 and what Budget 2026 changed")
d.callout("The SGB tax edge is now only for original subscribers",
          "SGBs are no longer issued in fresh tranches, but existing ones still trade. Until Budget "
          "2026, capital gains on any SGB redeemed at maturity were fully exempt \u2014 however you bought "
          "it. From 1 April 2026 that changed. The exemption now applies only to the original "
          "subscriber who bought in the RBI issue and holds the bond continuously to its 8-year "
          "maturity. If you buy an SGB on the secondary market, the exemption is gone: you pay capital "
          "gains tax even if you hold to maturity. Premature redemption through RBI windows after "
          "five years also lost its exemption. The 2.5% annual interest continues, taxed at your slab "
          "rate. The change triggered a sharp fall in secondary-market SGB prices, because buyers had "
          "been paying a 10\u201315% premium purely for the tax-free redemption.")
d.p("The practical reading: unless you can still subscribe at original issue and hold to maturity, "
    "do not pay a premium for an SGB on the exchange. A plain gold ETF now does the same job more "
    "cheaply and far more liquidly.")

# ======================= PART 6 =======================
d.new_page()
d.h1("Part 6 \u00b7 Tax on Gold in FY 2026-27")
d.p("How your gold is taxed depends entirely on the form you hold and how long you hold it. The "
    "rules below apply from 1 April 2026 (tax year 2026-27).")
d.table(
    ["Form", "Long-term after", "LTCG rate", "If sold earlier"],
    [["Physical gold / jewellery / coins", "24 months", "12.5% (no indexation)", "Taxed at your income-tax slab"],
     ["Digital gold", "24 months", "12.5% (no indexation)", "Taxed at your slab"],
     ["Gold ETF (listed)", "12 months", "12.5% (no indexation)", "Taxed at your slab"],
     ["Gold fund-of-funds", "24 months", "12.5% (no indexation)", "Taxed at your slab"],
     ["SGB (original subscriber, to maturity)", "\u2014", "Exempt", "\u2014"],
     ["SGB (all other exits from Apr 2026)", "12 months", "12.5% (no indexation)", "Taxed at your slab"]],
    widths=[3.2, 1.9, 2.4, 2.5])
d.h2("The details that catch people out")
d.bullet("Indexation is gone. Since 23 July 2024 there is no indexation benefit on gold; the flat rate is 12.5% on long-term gains. The 20%-with-indexation option survives only for land and buildings.")
d.bullet("The " + RS + "1.25 lakh exemption does not apply to gold ETFs. That exemption is for listed equity. Gold ETF long-term gains are taxed at 12.5% from the first rupee.")
d.bullet("Gold ETFs are the most tax-efficient form for a medium-term hold: you cross into long-term after just 12 months, versus 24 months for physical, digital and gold funds.")
d.bullet("3% GST on the gold value and 5% GST on the making charge can be added to your cost of acquisition when you compute the gain \u2014 keep the invoice.")
d.bullet("Inherited or gifted gold: tax depends on how and when you eventually sell, and on the previous owner's cost. Keep the original purchase records if you can.")
d.callout("One extra month can cut your tax from 30% to 12.5%",
          "Say you hold a gold ETF worth " + RS + "10 lakh that rises to " + RS + "13 lakh. Sell at 11 "
          "months and the " + RS + "3 lakh gain is short-term, taxed at your slab \u2014 about " + RS + "90,000 "
          "in the top bracket. Wait past 12 months and it becomes long-term at 12.5% \u2014 about " +
          RS + "37,500. Tax is not the only consideration (the price could fall while you wait), but "
          "for a medium-term gold holding, the 12-month line is worth planning around.")

# ======================= PART 7 =======================
d.new_page()
d.h1("Part 7 \u00b7 Storage, Safety and the Festive Scams")
d.h2("Where to keep physical gold")
d.bullet("Bank locker: safest for large holdings. Cost varies by bank and locker size, typically a few thousand rupees a year plus GST; banks now also require a locker agreement under RBI rules. Insure high-value contents separately.")
d.bullet("Home: fine for small holdings, but the real risk is not theft alone \u2014 it is that people talk. Keep the purchase invoice safe; it is your proof of ownership and your cost basis for tax.")
d.bullet("For ETF, fund and digital gold, \u201cstorage\u201d is not your problem \u2014 the vaulting is handled, which is exactly why those forms are cheaper to own.")
d.h2("Scams that spike every festive season")
d.bullet("Fake or missing hallmark: a piece with no HUID, or a HUID that returns \u201cNo record found\u201d in the BIS Care app. Always verify.")
d.bullet("\u201cGold at a discount\u201d online: if the price is below the live rate plus reasonable cost, the metal is not what it claims to be.")
d.bullet("Gold investment MLMs: schemes promising fixed monthly \u201creturns\u201d from gold. There is no such thing; these are usually Ponzi structures.")
d.bullet("Unverifiable digital-gold apps: stick to platforms backed by audited vaulting partners (for example refiners such as MMTC-PAMP or Augmont), and read the spread and exit terms.")
d.bullet("Fake buyback promises: a verbal promise of \u201cfull value buyback\u201d that vanishes when you return. Get the terms in writing.")
d.callout("The one habit that prevents most losses",
          "Before you pay, do three things on your phone: confirm today's 24K and 22K rate, verify the "
          "HUID in the BIS Care app, and photograph the itemised invoice. Ten minutes, and you have "
          "removed almost every way a festive gold purchase goes wrong.")

# ======================= PART 8 =======================
d.new_page()
d.h1("Part 8 \u00b7 The Dhanteras 2026 Buying Checklist")
d.p("Print this or keep it on your phone. Work top to bottom.")
d.h2("Before you leave home")
d.bullet("Set your budget in rupees, and decide the purpose: wear/gift (jewellery) or save (coins, bars, ETF).")
d.bullet("Check today's 24K and 22K rate on a reliable source so you know what a fair quote looks like.")
d.bullet("Note your city's Dhanteras puja window \u2014 and remember the buying itself is fine all day.")
d.bullet("If investing, decide the form in advance: coins/bars, gold ETF (demat), gold fund (SIP), or digital gold.")
d.h2("At the counter \u2014 eight checks")
d.numbered(1, "Hallmark present: BIS logo + purity stamp (22K916 / 18K750) + six-digit HUID.")
d.numbered(2, "HUID verified in the BIS Care app \u2014 \u201cNo record found\u201d means walk away.")
d.numbered(3, "Purity matches the rate you are being charged (do not pay 24K rates for 22K gold).")
d.numbered(4, "Making charge quoted as a percentage, and agreed before the piece is finalised.")
d.numbered(5, "Wastage charge \u2014 asked about and, if any, itemised.")
d.numbered(6, "Buyback and exchange terms \u2014 asked, and written on the invoice.")
d.numbered(7, "Invoice shows HUID, weight, gold rate, making charge and GST separately.")
d.numbered(8, "GST correct: 3% on gold value, 5% on making charges.")
d.h2("After you buy")
d.bullet("Photograph and file the invoice \u2014 it is your proof of ownership and your tax cost basis.")
d.bullet("Insure or store safely; do not announce the purchase publicly.")
d.bullet("Record the purchase (date, form, grams, cost) so your future capital-gains calculation is easy.")

# ======================= PART 9 =======================
d.new_page()
d.h1("Part 9 \u00b7 Your Budget-to-Form Plan")
d.p("How to split a festive gold budget so it does what you want it to do. Adjust the split to your "
    "own purpose \u2014 the point is to separate the occasion from the investment.")
d.h2("If your budget is " + RS + "25,000")
d.bullet(RS + "10,000\u2013" + RS + "15,000 in a small jewellery piece or silver, for the occasion and gifting.")
d.bullet(RS + "10,000\u2013" + RS + "15,000 in a gold ETF or a 1\u20132 gram 24K coin, for saving. At today's rate that is a little under a gram of 24K per " + RS + "15,000.")
d.h2("If your budget is " + RS + "50,000")
d.bullet(RS + "20,000 for the occasion \u2014 a wearable piece with the making charge negotiated down.")
d.bullet(RS + "30,000 into a gold ETF, bought in one go or split into three monthly purchases to average the price.")
d.h2("If your budget is " + RS + "1,00,000")
d.bullet(RS + "30,000\u2013" + RS + "40,000 for jewellery or gifting.")
d.bullet(RS + "60,000\u2013" + RS + "70,000 into an ETF or gold fund. Consider staggering it across two or three months rather than buying all at once at a record price.")
d.callout("Why stagger?",
          "Gold swung by more than 20% twice in 2026 and fell 6.5% in a single month. No one, "
          "including the banks, can call the next three months. Buying in two or three tranches "
          "instead of one removes the pressure to guess the bottom and gives you an average price "
          "rather than a single bet.")

# ======================= PART 10 =======================
d.new_page()
d.h1("Part 10 \u00b7 The Outlook and the Honest Verdict")
d.h2("What the forecasters actually say")
d.p("After the September correction, the big banks split sharply, and it is worth seeing the spread "
    "because it shows how little certainty there is.")
d.bullet("HSBC lowered its average 2026 forecast to about $4,490 an ounce, from $4,560, seeing possible short-term pressure.")
d.bullet("J.P. Morgan cut its own Q4 2026 target by roughly a quarter, to about $4,500, citing softer demand and sensitivity to real interest rates.")
d.bullet("More bullish houses (Deutsche Bank, Wells Fargo) still carry targets up to $6,000\u2013$6,300, which would imply " + RS + "2 lakh-plus per 10 grams.")
d.p("Translated to rupees, the consensus cluster points to something like " + RS + "1.6 lakh to " +
    RS + "1.9 lakh per 10 grams around Dhanteras \u2014 expensive by history, but not necessarily a fresh "
    "record over the January 2026 peak. The dramatic " + RS + "2 lakh-plus headline comes from bullish "
    "calls that the banks making them have largely walked back.", color=TEXT)
d.h2("The honest verdict")
d.p("Do not try to time this market. Over ten years, the evidence that Dhanteras month reliably beats "
    "an ordinary month is weak \u2014 it went both ways, and the recent five-year run coincides with a "
    "broad gold rally that has nothing to do with Diwali. The date is worth a point or two, in a "
    "direction nobody can call. The making charge is worth several times that, and it is knowable "
    "before you walk into the shop.")
d.p("So optimise the right variable. Decide the form by purpose. Negotiate the making charge. Verify "
    "the hallmark. Keep the invoice. Buy on the day that means something to your family, and let the "
    "metal do its slow work over the years.")
d.callout("If you remember one thing",
          "You are not buying a price. You are buying grams. The price will move after you buy \u2014 up or "
          "down \u2014 and there is nothing you can do about that. What you can control is how many grams "
          "your money actually buys once making charges, GST and spreads are stripped out. Get that "
          "right and you have bought well, whatever the market does next.")

# ======================= APPENDIX A =======================
d.new_page()
d.h1("Appendix A \u00b7 24-Term Glossary")
terms = [
    ("24K / 22K / 18K", "Gold purity by carat: 24K is 99.9% (999), 22K is 91.6% (916), 18K is 75% (750)."),
    ("BIS", "Bureau of Indian Standards, which runs the hallmarking scheme."),
    ("Hallmark", "The official purity mark on gold jewellery: BIS logo + fineness stamp + HUID."),
    ("HUID", "Hallmark Unique Identification \u2014 a six-digit code laser-etched on each piece, verifiable in the BIS Care app."),
    ("Making charge", "The jeweller's labour charge, usually 8\u201325% of the gold value on jewellery."),
    ("Wastage", "A charge some jewellers add for metal lost in crafting; should be itemised."),
    ("GST on gold", "3% on the gold value; 5% on the making charge."),
    ("Import duty", "Tax on imported bullion; raised to an effective 15% (10% BCD + 5% AIDC) on 13 May 2026."),
    ("BCD", "Basic Customs Duty \u2014 the main component of the import duty."),
    ("AIDC", "Agriculture Infrastructure and Development Cess \u2014 a 5% cess on gold and silver imports."),
    ("IBJA", "India Bullion and Jewellers Association, whose reference rate is a common daily benchmark."),
    ("Spot / reference rate", "The bullion-level price of pure metal, before any retail add-ons."),
    ("Pradosh kaal", "The roughly two-and-a-half-hour window after sunset, when the Dhanteras puja is kept."),
    ("Trayodashi", "The thirteenth lunar tithi, which gives Dhanteras its name and runs across 6\u20137 November 2026."),
    ("Pushya", "A nakshatra traditionally considered auspicious for buying gold; 31 Oct\u20131 Nov 2026."),
    ("Gold ETF", "A SEBI-regulated, exchange-listed fund tracking the gold price; needs a demat account."),
    ("iNAV", "Indicative net asset value \u2014 the fair value of an ETF unit at a given moment."),
    ("Expense ratio", "The annual fee an ETF or fund charges; about 0.5\u20131% for gold ETFs."),
    ("Gold fund-of-funds", "A mutual fund that invests in gold ETFs; no demat needed, SIP-able."),
    ("Digital gold", "Gold bought online and vaulted by a provider; not RBI/SEBI-regulated like a listed fund."),
    ("SGB", "Sovereign Gold Bond \u2014 a government gold-linked bond; no fresh issues, and its tax edge narrowed in Budget 2026."),
    ("LTCG / STCG", "Long-term / short-term capital gains; gold LTCG is 12.5% with no indexation."),
    ("Indexation", "Adjusting cost for inflation; no longer available on gold since 23 July 2024."),
    ("Buyback", "The price at which a jeweller will repurchase your gold; always ask before buying."),
]
for t, s in terms:
    d.h3(t)
    d.p(s, color=MUTED, size=9.6, lead=13.6)

# ======================= APPENDIX B =======================
d.new_page()
d.h1("Appendix B \u00b7 One-Page Quick Reference")
d.h2("Key numbers, October 2026")
d.table(
    ["Item", "Value"],
    [["24K gold (per 10 g)", RS + "1,49,570 \u2013 1,50,060"],
     ["24K gold (per gram)", RS + "14,957 \u2013 15,006"],
     ["22K gold (per 10 g)", RS + "1,37,100"],
     ["Silver (per kg)", RS + "2,28,000 \u2013 2,29,000"],
     ["Gold, year-on-year", "About +22%"],
     ["Import duty (effective)", "15% (10% BCD + 5% AIDC), since 13 May 2026"],
     ["GST", "3% on gold, 5% on making charge"],
     ["Making charge, jewellery", "8\u201325% of gold value"],
     ["Making charge, coins/bars", "About 2\u20135% premium"]],
    widths=[4, 5])
d.h2("Key dates")
d.table(
    ["Event", "Date"],
    [["Pushya (alternate auspicious day)", "31 Oct \u2013 1 Nov 2026"],
     ["Dhanteras", "Fri, 6 Nov 2026"],
     ["Diwali / Lakshmi Puja", "Sun, 8 Nov 2026"],
     ["Bhai Dooj", "Tue, 10 Nov 2026"]],
    widths=[4, 4])
d.h2("Tax at a glance (FY 2026-27)")
d.table(
    ["Form", "LTCG after", "Rate"],
    [["Physical / digital gold", "24 months", "12.5%"],
     ["Gold ETF", "12 months", "12.5%"],
     ["Gold fund-of-funds", "24 months", "12.5%"],
     ["SGB (original subscriber, to maturity)", "\u2014", "Exempt"]],
    widths=[4, 2.6, 2.2])
d.spacer(6)
d.callout("Keep learning",
          "This playbook is a Digitalaikart original, built to be current for the 2026 festive season. "
          "Gold moves daily, so confirm today's rate and the latest tax rules before you act. For "
          "anything specific to your situation, speak to a qualified financial adviser.")
d.spacer(4)
d.p("Digitalaikart \u00b7 Premium AI and money guides for India \u00b7 digitalkartai.shop",
    color=GOLD, size=10, font=FB)

d.finish()
print("Built:", OUT)
