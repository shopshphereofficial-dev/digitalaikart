# -*- coding: utf-8 -*-
"""Build the premium PDF for: The Smart Credit Card Playbook 2026 - India Edition."""
import os
import reportlab.rl_config as _rlc
_rlc.invariant = 1  # reproducible bytes (fixed timestamps) for CI builds
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether, PageBreak,
                                Flowable)
from reportlab.pdfgen import canvas as canvasmod

NAVY = colors.HexColor("#0a1628")
NAVY2 = colors.HexColor("#13233d")
GOLD = colors.HexColor("#f5c542")
GOLD_D = colors.HexColor("#c99a1e")
INK = colors.HexColor("#1b2432")
GREY = colors.HexColor("#5b6577")
LIGHT = colors.HexColor("#f4f6fa")
LINE = colors.HexColor("#d9dee8")
RED = colors.HexColor("#b3261e")
GREEN = colors.HexColor("#1f7a4d")

def _font_dir():
    import glob
    for d in ("/usr/share/fonts/truetype/dejavu/",
              "/usr/share/fonts/dejavu/",
              "/usr/share/fonts/TTF/",
              "/usr/share/fonts/truetype/"):
        if os.path.exists(d + "DejaVuSans.ttf"):
            return d
    hits = glob.glob("/usr/share/fonts/**/DejaVuSans.ttf", recursive=True)
    if hits:
        return os.path.dirname(hits[0]) + "/"
    raise SystemExit("DejaVu fonts not found; install fonts-dejavu-core")


FDIR = _font_dir()
pdfmetrics.registerFont(TTFont("DJS", FDIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DJS-B", FDIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DJS-O", FDIR + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DJSerif", FDIR + "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DJSerif-B", FDIR + "DejaVuSerif-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DJS", normal="DJS", bold="DJS-B", italic="DJS-O", boldItalic="DJS-B")

S = {}
S["body"] = ParagraphStyle("body", fontName="DJS", fontSize=10.2, leading=15.4,
                           textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7)
S["bodyc"] = ParagraphStyle("bodyc", parent=S["body"], alignment=TA_LEFT)
S["lead"] = ParagraphStyle("lead", parent=S["body"], fontSize=11.2, leading=17,
                           textColor=NAVY2)
S["h1"] = ParagraphStyle("h1", fontName="DJS-B", fontSize=19, leading=23,
                         textColor=NAVY, spaceBefore=2, spaceAfter=2)
S["h1n"] = ParagraphStyle("h1n", fontName="DJS-B", fontSize=10, leading=12,
                          textColor=GOLD_D, spaceAfter=1)
S["h2"] = ParagraphStyle("h2", fontName="DJS-B", fontSize=12.4, leading=16,
                         textColor=NAVY2, spaceBefore=10, spaceAfter=4)
S["h3"] = ParagraphStyle("h3", fontName="DJS-B", fontSize=10.8, leading=14,
                         textColor=GOLD_D, spaceBefore=7, spaceAfter=2)
S["bullet"] = ParagraphStyle("bullet", parent=S["body"], leftIndent=14,
                             bulletIndent=3, spaceAfter=3.5, alignment=TA_LEFT)
S["callout"] = ParagraphStyle("callout", fontName="DJS", fontSize=10, leading=14.6,
                              textColor=INK, alignment=TA_LEFT)
S["calloutt"] = ParagraphStyle("calloutt", fontName="DJS-B", fontSize=10.4,
                               leading=14, textColor=NAVY, spaceAfter=2)
S["cell"] = ParagraphStyle("cell", fontName="DJS", fontSize=8.3, leading=11,
                           textColor=INK)
S["cellb"] = ParagraphStyle("cellb", fontName="DJS-B", fontSize=8.3, leading=11,
                            textColor=colors.white)
S["toc"] = ParagraphStyle("toc", fontName="DJS", fontSize=10.4, leading=17,
                          textColor=INK)
S["small"] = ParagraphStyle("small", fontName="DJS", fontSize=8.4, leading=12,
                            textColor=GREY, alignment=TA_LEFT)
S["cover_t"] = ParagraphStyle("cover_t", fontName="DJS-B", fontSize=33, leading=37,
                              textColor=colors.white, alignment=TA_LEFT)
S["cover_s"] = ParagraphStyle("cover_s", fontName="DJS", fontSize=14, leading=20,
                              textColor=GOLD, alignment=TA_LEFT)
S["cover_m"] = ParagraphStyle("cover_m", fontName="DJS", fontSize=10.5, leading=15,
                              textColor=colors.HexColor("#c7d0e0"), alignment=TA_LEFT)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def P(t, st="body"):
    return Paragraph(esc(t), S[st])


def PR(t, st="body"):
    """Raw paragraph - caller supplies safe inline markup."""
    return Paragraph(t, S[st])


def H1(num, title):
    return [Spacer(1, 2), Paragraph(esc(num), S["h1n"]),
            Paragraph(esc(title), S["h1"]), GoldRule()]


def H2(t):
    return Paragraph(esc(t), S["h2"])


def H3(t):
    return Paragraph(esc(t), S["h3"])


def bullets(items):
    return [Paragraph(esc(i), S["bullet"], bulletText="\u2022") for i in items]


def numbered(items):
    out = []
    for i, it in enumerate(items, 1):
        out.append(Paragraph(esc(it), S["bullet"], bulletText=str(i) + "."))
    return out


class GoldRule(Flowable):
    def __init__(self, w=None, color=GOLD, th=2.2):
        Flowable.__init__(self)
        self.w = w
        self.color = color
        self.th = th

    def wrap(self, aw, ah):
        self.width = aw
        self.height = self.th + 6
        return (aw, self.th + 6)

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setLineWidth(self.th)
        c.line(0, 4, 64, 4)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.8)
        c.line(64, 4, self.width, 4)


class Callout(Flowable):
    """A boxed callout with a coloured left bar and optional title."""
    def __init__(self, title, text, bg=LIGHT, bar=GOLD):
        Flowable.__init__(self)
        self.title = title
        self.text = text
        self.bg = bg
        self.bar = bar

    def wrap(self, aw, ah):
        self.width = aw
        self._inner = aw - 20
        tstyle = S["calloutt"]
        bstyle = S["callout"]
        self._tpara = Paragraph(esc(self.title), tstyle) if self.title else None
        self._bpara = Paragraph(esc(self.text), bstyle)
        th = self._tpara.wrap(self._inner, 1000)[1] if self._tpara else 0
        bh = self._bpara.wrap(self._inner, 1000)[1]
        self.height = th + bh + 18
        return (aw, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.roundRect(0, 0, self.width, self.height, 5, stroke=1, fill=1)
        c.setFillColor(self.bar)
        c.roundRect(0, 0, 5, self.height, 2, stroke=0, fill=1)
        y = self.height - 10
        if self._tpara:
            th = self._tpara.wrap(self._inner, 1000)[1]
            self._tpara.drawOn(c, 14, y - th)
            y -= th
        bh = self._bpara.wrap(self._inner, 1000)[1]
        self._bpara.drawOn(c, 14, y - bh - 1)


def mktable(header, rows, widths, zebra=True):
    data = [[Paragraph(esc(h), S["cellb"]) for h in header]]
    for r in rows:
        data.append([Paragraph(esc(c), S["cell"]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, GOLD_D),
        ("GRID", (0, 1), (-1, -1), 0.4, LINE),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
    ]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(st))
    return t


# ----------------------------------------------------------------------------
# Canvas with cover + running header/footer
# ----------------------------------------------------------------------------
class BookCanvas(canvasmod.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._saved)
        for st in self._saved:
            self.__dict__.update(st)
            self._decorate(n)
            super().showPage()
        super().save()

    def _decorate(self, n):
        p = self._pageNumber
        if p == 1:
            self._cover()
        else:
            self._chrome(p, n)

    def _cover(self):
        c = self
        W, H = A4
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        # subtle gold corner motif
        c.setFillColor(NAVY2)
        c.rect(0, H - 150, W, 150, stroke=0, fill=1)
        c.setStrokeColor(GOLD)
        c.setLineWidth(3)
        c.line(48, H - 96, 48, H - 40)
        c.setFillColor(GOLD)
        c.setFont("DJS-B", 11)
        c.drawString(60, H - 74, "DIGITALAIKART  \u00b7  PREMIUM INDIA EDITION")
        # title block
        c.setFillColor(GOLD)
        c.setFont("DJS-B", 12)
        c.drawString(48, H - 250, "THE 2026 MONEY PLAYBOOK SERIES")
        c.setFillColor(colors.white)
        c.setFont("DJS-B", 40)
        c.drawString(46, H - 300, "The Smart")
        c.drawString(46, H - 348, "Credit Card")
        c.setFillColor(GOLD)
        c.drawString(46, H - 396, "Playbook 2026")
        c.setFillColor(colors.HexColor("#c7d0e0"))
        c.setFont("DJS", 14)
        c.drawString(48, H - 440, "India Edition \u00b7 Earn maximum rewards, stack")
        c.drawString(48, H - 462, "festive offers, and never fall into the minimum-due trap")
        # gold divider
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.line(48, H - 495, 210, H - 495)
        # feature strip
        feats = ["Card-by-card 2026 rewards map", "Festive-sale bank offers decoded",
                 "The minimum-due trap maths", "Your RBI rights, in plain English"]
        c.setFont("DJS", 11)
        c.setFillColor(colors.white)
        yy = H - 540
        for f in feats:
            c.setFillColor(GOLD)
            c.circle(52, yy + 3.5, 2.4, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.drawString(64, yy, f)
            yy -= 26
        # bottom band
        c.setFillColor(NAVY2)
        c.rect(0, 0, W, 96, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.setFont("DJS-B", 12)
        c.drawString(48, 58, "Verified against official sources \u00b7 October 2026")
        c.setFillColor(colors.HexColor("#c7d0e0"))
        c.setFont("DJS", 9.5)
        c.drawString(48, 36, "digitalkartai.shop  \u00b7  First Edition 2026  \u00b7  Digitalaikart Original")

    def _chrome(self, p, n):
        c = self
        W, H = A4
        # top rule + running head
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.line(48, H - 44, 92, H - 44)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.line(92, H - 44, W - 48, H - 44)
        c.setFillColor(GREY)
        c.setFont("DJS", 8)
        c.drawString(48, H - 58, "The Smart Credit Card Playbook 2026 \u2014 India Edition")
        c.drawRightString(W - 48, H - 58, "DIGITALAIKART")
        # footer
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.line(48, 46, W - 48, 46)
        c.setFillColor(GREY)
        c.setFont("DJS", 8)
        c.drawString(48, 33, "digitalkartai.shop  \u00b7  Educational guide, not financial advice")
        c.setFillColor(NAVY)
        c.setFont("DJS-B", 8)
        c.drawRightString(W - 48, 33, "Page %d of %d" % (p - 1, n - 1))


# ----------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------
story = []
story.append(Spacer(1, 4))
story.append(PageBreak())  # page 1 = cover (drawn by canvas)

# ---- Read this first ----
story += H1("Before you start", "Read This First")
story.append(P("This playbook is written for one person: an Indian cardholder who wants the rewards and the "
               "festive-sale discounts without ever paying 40% interest. It is deliberately short on theory and "
               "long on numbers you can act on today. Every card rate, cap, rule and offer below was checked "
               "against official issuer terms, RBI directions and platform offer pages in October 2026."))
story.append(P("Two honest warnings before you spend a rupee. First, credit cards reward discipline, not "
               "spending \u2014 the entire reward on a typical card is worth 1% to 5%, while the interest on an unpaid "
               "balance runs at 39% to 50% a year. Rewards are the small print; interest is the big print. Second, "
               "card terms change constantly, so treat every number here as a verified snapshot and confirm the "
               "current terms in your card's Most Important Terms and Conditions (MITC) before you apply or spend."))
story.append(Callout("This is education, not advice",
                     "Nothing here is personalised financial advice and no card is recommended for you personally. "
                     "Use the method, check your own MITC, and decide what fits your spending. For a decision this "
                     "personal, a licensed adviser can help.",
                     bg=colors.HexColor("#fff8e1"), bar=GOLD_D))
story.append(Spacer(1, 6))
story.append(H2("What is inside"))
toc = [
    "1.  The one rule that decides everything",
    "2.  How to choose the right card (the net-value method)",
    "3.  The 2026 card landscape, category by category",
    "4.  Squeezing maximum rewards \u2014 caps, exclusions, redemption",
    "5.  RuPay credit cards on UPI: earning on everyday scans",
    "6.  Stacking the October 2026 festive-sale offers",
    "7.  The minimum-due trap \u2014 the exact maths",
    "8.  If you are already in the trap: the escape plan",
    "9.  Your rights under RBI's 2026 rules",
    "10. Safety and fraud: the 10-minute checklist",
    "11. Build credit safely, and raise your limit the smart way",
    "12. Your 30-day action plan",
    "Appendix A \u2014 AI prompt pack   \u00b7   Appendix B \u2014 Cheat sheet and glossary   \u00b7   FAQ",
]
story += [Paragraph(esc(t), S["toc"]) for t in toc]
story.append(PageBreak())

# ---- Chapter 1 ----
story += H1("Chapter 1", "The One Rule That Decides Everything")
story.append(P("Almost everything you have heard about credit cards \u2014 the cashback, the reward points, the "
               "lounge access, the 10% festive discounts \u2014 sits on top of a single number: whether you pay the "
               "full statement amount by the due date. Do that, and your card is the cheapest short-term credit you "
               "will ever get, plus free rewards. Miss it, and the same card becomes one of the most expensive loans "
               "in Indian personal finance."))
story.append(H2("Why paying in full is the whole game"))
story.append(P("A credit card gives you an interest-free period \u2014 a window in which you are using the bank's "
               "money for free. The window runs from the day you make a purchase to the payment due date of the "
               "statement that carries it. Understanding that window is the difference between a free 45-day float "
               "and a 50% annual interest bill."))
story += bullets([
    "The billing cycle is the gap between two statement dates, usually about 30 days; each purchase lands on "
    "one statement, due 15 to 20 days after it closes.",
    "A purchase made just after your statement closes gets almost the full cycle plus the grace period \u2014 up to "
    "about 45 to 50 interest-free days; one made just before it closes gets only 15 to 20 days.",
    "The lever: time large purchases to the start of the billing cycle to stretch the free credit the longest.",
])
story.append(Callout("Your one-line rule",
                     "Set auto-pay for the total amount due \u2014 never the minimum due. If you cannot clear the full "
                     "statement this month, that purchase did not belong on a credit card.",
                     bg=colors.HexColor("#eaf5ee"), bar=GREEN))
story.append(H2("What happens the moment you pay less than the full amount"))
story.append(P("The instant you leave a balance outstanding, three things happen at once \u2014 and they are why the "
               "interest cost is so much worse than it looks:"))
story += numbered([
    "The interest-free period is suspended. Interest is charged on the unpaid balance from each transaction "
    "date \u2014 retroactively, not from the due date.",
    "Every new purchase also loses its grace period and starts earning interest from day one, until you clear "
    "the full balance.",
    "The interest compounds monthly, and 18% GST is added on top of every finance charge \u2014 so the number on "
    "the card is not the number you pay.",
])
story.append(P("RBI now forces issuers to print a warning on every statement that making only the minimum payment "
               "will stretch your repayment over months or years with compounded interest. That warning is the most "
               "important sentence on your bill."))
story.append(P("One free fix: RBI's card directions let you change your card's billing cycle at least once, to any "
               "date. If your due date falls before your salary, move it to just after your payday \u2014 that alone "
               "removes the most common reason people miss a payment."))
story.append(PageBreak())

# ---- Chapter 2 ----
story += H1("Chapter 2", "How to Choose the Right Card")
story.append(P("There is no single best credit card in India \u2014 only the best card for your spending. The card "
               "that pays 10% on food delivery earns nothing extra when you fill petrol; the card that slashes fuel "
               "surcharge does nothing for your electricity bill. So do not choose by the biggest number in the "
               "advertisement. Choose by net annual value for your actual spend."))
story.append(H2("The net-annual-value method"))
story += numbered([
    "Map your real monthly spend by category: online shopping, groceries, food delivery, dining out, fuel, "
    "utility bills, travel, and UPI scan-and-pay.",
    "For each shortlisted card, read its earn rate in your top two or three categories, and note the monthly "
    "or quarterly cap and the exclusions.",
    "Value the rewards at their realistic redemption value \u2014 not the headline point value the bank quotes.",
    "Subtract the annual fee, and check the spend at which it is waived.",
    "Pick the card with the highest net value. Two to three cards is the sweet spot: one all-rounder, one "
    "category specialist, and optionally one platform or fuel card. More than three becomes hard to track.",
])
story.append(H2("Read the MITC \u2014 it is the real contract"))
story.append(P("The Most Important Terms and Conditions (MITC) is the authority for everything that matters: earn "
               "rates, caps, excluded categories, annual and late fees, interest rate, and how long reward points "
               "last. RBI requires issuers to publish it and give you a copy. Before you apply, search the MITC "
               "for the words \u2018cap\u2019, \u2018exclude\u2019 and \u2018UPI\u2019 \u2014 those three words decide most of your "
               "real reward."))
story.append(H2("Eligibility and the score that matters"))
story += bullets([
    "Most issuers look for a CIBIL score of 750 or above for a clean, document-light approval; entry cards "
    "often start around 700\u2013720.",
    "Salaried applicants usually prove income with salary slips; self-employed applicants with an ITR and "
    "bank statements.",
    "If your profile is thin or new to credit, a secured card against a fixed deposit builds history with "
    "almost no risk \u2014 the limit is tied to your deposit.",
    "Do not apply to several issuers in a short window: each application is a hard enquiry on your report.",
])
story.append(Callout("Fee versus cap: the trap in the headline rate",
                     "A 10% rate that stops at a small monthly cap can pay less than a flat 2% with no cap once "
                     "you spend normally. Always compare cards after applying the caps, not before.",
                     bg=colors.HexColor("#fff8e1"), bar=GOLD_D))
story.append(PageBreak())

# ---- Chapter 3 ----
story += H1("Chapter 3", "The 2026 Card Landscape")
story.append(P("The tables below summarise the strongest cards in each spending category, verified against issuer "
               "terms in October 2026. Rates and caps change often \u2014 confirm the current figures in the MITC "
               "before you apply or spend. The aim is to show the shape of the market, not to name a winner."))
story.append(H2("Online shopping"))
story.append(mktable(
    ["Card", "Earn rate", "Cap / key condition"],
    [
        ["Amazon Pay ICICI", "5% on Amazon for Prime, 3% non-Prime; 1% other", "Lifetime free; rewards as Amazon Pay balance; fuel, rent, EMI, precious metals excluded"],
        ["SBI Cashback", "5% on all online spends", "\u20b92,000 per statement cycle (halved from \u20b95,000 on 1 Apr 2026); excludes utilities, insurance, fuel, rent, wallets, education, jewellery, gaming, FASTag, govt"],
        ["Flipkart Axis", "7.5% Myntra; 5% Flipkart and Cleartrip; 1% other", "\u20b94,000 per quarter per merchant; rules updated 28 Aug 2026"],
        ["HDFC Millennia", "5% on listed partner brands; 1% other", "\u20b91,000 per month cap; \u20b9999 fee waived at \u20b91L spend"],
        ["HDFC Swiggy", "10% on Swiggy app; 5% online; 1% other", "10%: \u20b91,500/mo (min \u20b9249); 5%: \u20b91,500/mo; 1%: \u20b9500/mo"],
        ["Jupiter Edge+ (CSB RuPay)", "10% on Amazon, Flipkart, Myntra wishlist brands", "\u20b92,000/mo with \u20b9600 per merchant; lifetime free"],
    ],
    [88, 210, 210]))
story.append(Spacer(1, 6))
story.append(H2("Food, dining and groceries"))
story.append(mktable(
    ["Card", "Best for", "Earn rate and cap"],
    [
        ["HDFC Swiggy", "Swiggy, Instamart, Dineout", "10% (\u20b91,500/mo)"],
        ["Zomato RBL", "Zomato", "10% (\u20b91,000/mo)"],
        ["Axis ACE", "All-round dining and bills", "4% Swiggy/Zomato; 5% utility via Google Pay; 2% other; \u20b9499 fee"],
        ["HSBC Live+", "Dining, food delivery, groceries combined", "10% combined (\u20b91,200/mo); 1.5% other"],
        ["Tata Neu Infinity HDFC", "BigBasket, bbnow", "5% NeuCoins on the Tata ecosystem"],
    ],
    [120, 175, 213]))
story.append(Spacer(1, 6))
story.append(H2("Fuel, travel and utilities"))
story.append(mktable(
    ["Need", "Strong cards", "Earn rate and cap"],
    [
        ["Fuel", "IndianOil RBL XTRA; BPCL SBI Octane; HDFC IndianOil", "Up to 8.5%; 7.25%; 5% + 1% waiver (surcharge-waiver caps apply)"],
        ["Travel and miles", "ICICI MakeMyTrip; Axis Atlas; HDFC Infinia", "Co-brand rewards; EDGE Miles; ~3.33% base, up to 10x via SmartBuy (invite-only)"],
        ["Utility bills", "Axis ACE; Axis Airtel", "5% via Google Pay; 25% on Airtel bills (capped), 10% other utilities"],
        ["UPI scan-and-pay", "Kiwi Axis RuPay; Tata Neu Infinity RuPay", "1.5% uncapped, lifetime free; 5% Tata UPI, 1.5% other"],
    ],
    [82, 190, 236]))
story.append(Spacer(1, 6))
story.append(Callout("A practical 3-card wallet",
                     "Most readers are best served by: (1) one all-rounder that covers bills and dining \u2014 Axis ACE "
                     "or HDFC Millennia; (2) one category specialist for your biggest spend \u2014 a fuel card or a "
                     "grocery card; and (3) one platform or UPI card if you shop or scan heavily. Keep it to three.",
                     bg=LIGHT, bar=NAVY))
story.append(PageBreak())

# ---- Chapter 4 ----
story += H1("Chapter 4", "Squeezing Maximum Rewards")
story.append(P("A reward programme is a set of rules with three moving parts: the rate, the cap, and the "
               "exclusions. Miss any one of them and your effective reward can fall to near zero. Here is how to "
               "extract the most from any card without overthinking it."))
story.append(H2("Caps first, rate second"))
story.append(P("The cap decides everything above a modest spend. A card that pays 10% but stops at \u20b91,500 a "
               "month pays exactly \u20b918,000 a year and nothing more, however much you spend. Once your monthly "
               "spend in the bonus category passes the cap, the remaining spend drops to the base rate \u2014 so plan "
               "which card to use once each card's cap is exhausted."))
story.append(H2("The exclusions that quietly erase rewards"))
story.append(P("Most Indian cards exclude the same categories from earning: fuel, rent, wallet loads, EMI "
               "conversions, government and tax payments, jewellery, insurance premiums, education fees, and "
               "cash-like or person-to-person transfers. Two cards can look identical on the front page and differ "
               "completely once these are applied."))
story.append(H2("Merchant category codes: why the same shop can earn or not"))
story.append(P("Rewards are calculated on the merchant category code (MCC) the terminal sends, not on what you "
               "bought. A kirana QR may post as retail (earns) or as something else (does not). After you pay a new "
               "kind of merchant for the first time, check your statement preview to see whether the transaction "
               "earned \u2014 one check beats a dozen assumptions."))
story.append(H2("Redemption: value points honestly, and redeem before a devaluation"))
story += bullets([
    "Value points at what you will actually redeem them for \u2014 often a fraction of the marketing figure.",
    "SBI Card, from 1 April 2026, capped statement-credit redemption at 60,000 points per card per calendar "
    "month and allows redemption only in multiples of 4,000 points (exceptions: Air India SBI Signature, "
    "PhonePe SBI PURPLE and SELECT BLACK). Check your own issuer's redemption multiples and caps.",
    "Points can expire, and programmes get devalued. RBI gives at least 30 days' notice of adverse changes "
    "\u2014 so when a devaluation is announced, redeem first and decide about the card second.",
])
story.append(Callout("The devaluation window is an action window",
                     "Banks almost never reverse an announced devaluation, and they cluster their notice at the "
                     "regulatory floor of 30 days. Treat that notice as your cue to redeem the balance before the "
                     "cut lands \u2014 or to exit the card without a closure charge if the change is against you.",
                     bg=colors.HexColor("#fff8e1"), bar=GOLD_D))
story.append(PageBreak())

# ---- Chapter 5 ----
story += H1("Chapter 5", "RuPay Credit Cards on UPI")
story.append(P("UPI-on-credit lets you pay a merchant QR code from your credit limit instead of your bank balance. "
               "For everyday kirana and supermarket spending that used to go through debit UPI, this turns "
               "previously unrewarded payments into earning ones \u2014 if you set it up correctly and pay the bill in "
               "full."))
story.append(H2("How it actually works"))
story += numbered([
    "Only RuPay credit cards can be linked to UPI. Visa and Mastercard credit cards cannot be used on standard "
    "UPI credit rails as of October 2026.",
    "Link the card inside PhonePe, Google Pay, Paytm, BHIM or your bank's own UPI app, and set a separate UPI "
    "PIN for the credit account.",
    "At checkout, choose the RuPay credit account before scanning. The payment draws on your credit limit and "
    "appears on your card statement like any swipe, with the usual grace period if you pay in full.",
])
story.append(H2("The rules that catch people out"))
story += bullets([
    "Merchant payments only. Credit cards on UPI are blocked from person-to-person transfers by design.",
    "NPCI allows up to \u20b91 lakh per transaction, but your bank may set a lower credit-UPI sub-limit for new "
    "linkages.",
    "Rewards are set by the issuer's MITC \u2014 not by NPCI and not by the app. Some cards pay full rates on UPI; "
    "others exclude it or pay a reduced rate.",
    "Your monthly cashback cap is shared across UPI and swipe spend. UPI moves everyday spending onto the card "
    "and can push you past the cap faster.",
    "It is still a credit card: it reports to the credit bureaus, and if you revolve the balance, interest and "
    "GST apply exactly as on a swipe.",
])
story.append(Callout("Verify before you migrate your spending",
                     "Search your MITC for the word UPI before you move daily spends onto the card, then check the "
                     "first statement after linking to confirm the transactions actually earned. Assuming parity "
                     "with swipes is the most common and most avoidable disappointment.",
                     bg=LIGHT, bar=NAVY))
story.append(P("One discipline point: because a credit-UPI payment feels identical to a debit-UPI payment, it is "
               "easy to stop noticing how much you are spending. Set a monthly credit-UPI cap in the app, or move "
               "discretionary spending back to debit once you hit your limit."))
story.append(PageBreak())

# ---- Chapter 6 ----
story += H1("Chapter 6", "Stacking the October 2026 Festive-Sale Offers")
story.append(P("The festive sales are the single biggest discount window of the Indian year, and the headline "
               "\u201810% off with the right bank card' is real \u2014 but it is capped, has exclusions, and is not always "
               "the best card to use. Here is the honest version, verified from the offer terms in October 2026."))
story.append(H2("The two sales and their bank partners"))
story.append(mktable(
    ["Sale", "Runs", "Bank partner", "Base cap per order"],
    [
        ["Amazon Great Indian Festival", "8 to 20 Oct 2026", "SBI credit / debit cards", "\u20b91,500, then \u20b91,250 from 12 Oct; min \u20b92,490 (\u20b94,990 mobiles)"],
        ["Flipkart Big Billion Days", "9 to 18 Oct 2026 (early access 8 Oct)", "Axis Bank and ICICI Bank cards", "Axis base \u20b91,500, then \u20b91,250 from 11 Oct; min \u20b94,990"],
    ],
    [110, 120, 118, 160]))
story.append(Spacer(1, 6))
story.append(H2("The exclusions decide whether you actually get it"))
story += bullets([
    "On Amazon, the SBI offer excludes corporate cards, the Paytm SBI, Flipkart SBI and Cashback SBI cards, and "
    "RuPay credit cards used through UPI.",
    "On Amazon, SBI also reclaims the reward points on discounted transactions \u2014 so you may trade card rewards "
    "for the instant discount.",
    "On Flipkart, the Flipkart Axis card is excluded from the general offer (it gets a separate EMI-only offer), "
    "and Axis excludes UPI and net-banking payments.",
    "The base discount can be availed a limited number of times, and it resets on set days \u2014 Amazon resets on "
    "9, 10, 11, 13, 15, 17 and 19 October; Flipkart resets on 11 and 16 October.",
])
story.append(H2("The crossover: when the 10% offer loses to your own card"))
story.append(P("The SBI base cap of \u20b91,500 equals 5% of \u20b930,000. Below \u20b930,000, the SBI 10% (capped) wins. "
               "Above \u20b930,000, a 5%-back card \u2014 like Amazon Pay ICICI for Prime members \u2014 often beats it, unless "
               "the bonus offers close the gap. From 12 October, when the SBI cap drops to \u20b91,250, the crossover "
               "falls to \u20b925,000."))
story.append(Callout("The 30-second decision rule",
                     "Compare the final price, not the sticker: sale price minus the bank discount, against the "
                     "rewards your own card would earn. Split a large cart into orders across reset days so the cap "
                     "applies more than once. And do not accept an EMI offer that forfeits a higher cashback.",
                     bg=colors.HexColor("#eaf5ee"), bar=GREEN))
story.append(P("Finally, the sale discount is worth chasing only on things you were going to buy anyway. A \u20b91,500 "
               "discount on a \u20b930,000 phone you did not need is not a saving \u2014 it is \u20b928,500 you just spent."))
story.append(PageBreak())

# ---- Chapter 7 ----
story += H1("Chapter 7", "The Minimum-Due Trap")
story.append(P("Banks print the minimum amount due in a large, friendly font. It feels responsible to pay it. It is "
               "the most expensive decision in Indian personal finance, and the maths below shows exactly why."))
story.append(H2("What the minimum due actually is"))
story.append(P("It is typically the higher of 5% of your outstanding balance or \u20b9200\u2013250, plus any EMI "
               "instalments due, past-due amounts, overlimit charges and the interest and fees charged that cycle. "
               "It is the smallest payment that keeps your account \u2018current'. It is not a payment plan."))
story.append(H2("Why the cost explodes"))
story += numbered([
    "Interest is charged on the full outstanding balance from each transaction date \u2014 not from the due date.",
    "You lose the interest-free period on every new purchase until the full balance is cleared.",
    "The rate compounds monthly, and 18% GST is added on top of every finance charge.",
    "Most mainstream cards charge 3.25% to 3.75% a month \u2014 roughly 39% to 45% a year \u2014 which becomes about "
    "48% to 50% once GST is added.",
])
story.append(H2("Bank-wise revolving rates (2026)"))
story.append(mktable(
    ["Issuer / card type", "Monthly rate", "Approx. APR (with GST)"],
    [
        ["Premium cards (e.g. HDFC Infinia, SBI Prime Advantage)", "1.99%", "~28%"],
        ["ICICI Instant Platinum", "2.49%", "~35%"],
        ["SBI Card (standard variants)", "3.50%", "~49.6%"],
        ["HDFC (Regalia, Diners)", "3.60%", "~50%"],
        ["ICICI (Amazon Pay, Coral)", "3.67%", "~51%"],
        ["Axis Bank (Ace, Flipkart, Magnus)", "3.60%", "~50%"],
        ["Kotak Mahindra (revised 2025)", "3.75%", "~53%"],
    ],
    [230, 90, 188]))
story.append(Spacer(1, 6))
story.append(H2("The worked example that should end the debate"))
story.append(P("Take a \u20b950,000 balance on a card charging 3.5% a month, and pay only the minimum each month, "
               "with no new spending. Because interest keeps compounding on a balance that barely moves, you would "
               "pay roughly \u20b91.7 to \u20b91.9 lakh in total and take about 8 to 10 years to clear it \u2014 of which "
               "\u20b91.2 to \u20b91.4 lakh is pure interest, two to three times the original amount. Every month, most of "
               "your minimum payment goes to interest and only a small slice touches the principal."))
story.append(Callout("The one comparison to remember",
                     "Converting that same \u20b950,000 to a 12-month EMI at around 15% costs roughly \u20b954,200 in total "
                     "\u2014 a saving of about \u20b91.17 lakh versus paying the minimum. The difference between a minimum-due "
                     "habit and an EMI is not a few hundred rupees. It is over a lakh.",
                     bg=colors.HexColor("#fdecea"), bar=RED))
story.append(PageBreak())

# ---- Chapter 8 ----
story += H1("Chapter 8", "If You Are Already in the Trap")
story.append(P("If you are revolving a balance, do not panic and do not keep paying the minimum. There is a clear "
               "order of operations that cuts the cost dramatically, and it works whether your balance is \u20b920,000 "
               "or \u20b92 lakh."))
story += numbered([
    "Stop new spending on the card. Move to debit or bank-UPI until the balance is clear, so the balance can "
    "actually fall.",
    "Convert the balance to EMI immediately. Most banks offer conversion at 12\u201318% a year \u2014 HDFC SmartEMI, SBI "
    "Flexi Pay, ICICI EMI on Call. On \u20b950,000 over 12 months at 15% you pay about \u20b954,200 total, versus roughly "
    "\u20b91.7 lakh if you keep paying the minimum.",
    "Or take a personal loan at 11\u201316% and clear the card outright. It sounds odd to borrow to repay borrowing, "
    "but the maths is unambiguous: 12% beats 45%.",
    "Or balance-transfer to a cheaper card if one offers a low introductory rate \u2014 read the transfer fee and "
    "the rate that applies after the intro period.",
    "Negotiate a temporary rate reduction with the issuer's retention team. It works some of the time, and is "
    "most likely if you have a long, clean history.",
    "Once clear, set auto-pay for the total amount due, not the minimum, so it never happens again.",
])
story.append(Callout("A note on tax",
                     "Interest paid on a credit card is generally not tax-deductible, while interest on certain "
                     "personal or business loans can be. That is one more reason a lower-rate loan often beats "
                     "revolving a card.",
                     bg=LIGHT, bar=NAVY))
story.append(H2("Do not close the card in a hurry"))
story.append(P("Clearing the balance and then closing the card can hurt your credit score, because it removes "
               "available credit (raising your utilisation ratio) and shortens your credit history. Keep the card "
               "open, use it lightly \u2014 20% to 30% of the limit \u2014 and pay in full every cycle. If the annual fee is "
               "the problem, ask for a fee waiver or downgrade rather than closing."))
story.append(PageBreak())

# ---- Chapter 9 ----
story += H1("Chapter 9", "Your Rights Under RBI's 2026 Rules")
story.append(P("RBI's directions on credit cards give you more protection than most cardholders realise. These are "
               "the rights worth knowing, and using."))
story.append(mktable(
    ["Your right", "What it means in practice"],
    [
        ["Change your billing cycle", "You can change the cycle at least once, to any start or closing date, to match your salary and cash flow."],
        ["Choose your card network", "At a new issue, and at renewal, covered issuers must offer a choice among available card networks. This is not instant mid-term switching."],
        ["A minimum-due warning", "Statements must warn that paying only the minimum stretches repayment with compounded interest; the MITC must explain that the interest-free period is suspended if a previous balance is outstanding."],
        ["No negative amortisation", "The minimum due must cover the full interest plus some principal \u2014 your balance cannot grow while you pay on time."],
        ["Transparent rewards", "All cashbacks, points and benefits must be disclosed and verifiable, with details on the issuer's website."],
        ["30 days' notice of adverse changes", "If a change is to your disadvantage, you get at least 30 days' notice and may surrender the card with no closure charge, subject to clearing dues."],
        ["No unilateral limit increase", "Issuers cannot raise your credit limit without your explicit consent (OTP or written)."],
        ["Fairer late-payment rules (from 1 Apr 2027)", "A card can be reported past due, or penal charges levied, only if it stays past due for more than 3 days; late charges apply only to the outstanding amount, not the total due."],
        ["No capitalising charges", "Issuers cannot levy interest on unpaid taxes, levies or charges."],
    ],
    [150, 358]))
story.append(Spacer(1, 6))
story.append(P("Practical use: if your issuer announces a fee hike or a reward cut you dislike, that 30-day notice is "
               "your exit window \u2014 redeem your points, then decide whether the card still earns its fee, and if not, "
               "surrender it without a closure charge."))
story.append(PageBreak())

# ---- Chapter 10 ----
story += H1("Chapter 10", "Safety and Fraud: The 10-Minute Checklist")
story.append(P("A credit card is only as safe as your habits. Fraud on Indian cards is overwhelmingly the result of "
               "a shared secret or a rushed click, not a broken system."))
story += bullets([
    "Never share your OTP, CVV, PIN or full card number with anyone \u2014 no bank, no RBI official, no \u2018courier', "
    "and no one who calls about a \u2018refund' or a \u2018KYC update'.",
    "Use only your card app or the number printed on the back of your card. Fake customer-care numbers on "
    "search results are a leading fraud channel.",
    "Turn on transaction alerts by SMS and email, and review your statement every cycle \u2014 you are the first line "
    "of detection.",
    "If your card is lost or you spot an unauthorised transaction, block the card and report it immediately "
    "through the app or the issuer's helpline.",
    "RBI's limited-liability framework means your share of the loss on an unauthorised transaction depends "
    "heavily on how fast you report \u2014 report at once and liability is typically nil; delay and your share grows.",
    "Prefer tokenised cards in wallets and merchant apps over entering your raw card number, and use the app's "
    "lock/unlock and spend-limit controls for online transactions.",
    "Pay dues only through the issuer's authorised channels \u2014 RBI advises against paying through unauthorised "
    "modes.",
    "Be wary of any \u2018digital arrest', \u2018loan approved \u2014 pay a fee' or \u2018card upgrade \u2014 confirm the OTP' call. "
    "None are real.",
])
story.append(Callout("The 3-step drill if something goes wrong",
                     "1. Block the card in the app. 2. Report the unauthorised transaction in writing and keep the "
                     "reference number. 3. If the issuer does not resolve it, escalate to the RBI's Integrated "
                     "Ombudsman Scheme \u2014 it is free and built for exactly this.",
                     bg=colors.HexColor("#fdecea"), bar=RED))
story.append(PageBreak())

# ---- Chapter 11 ----
story += H1("Chapter 11", "Build Credit Safely, Raise Your Limit the Smart Way")
story.append(P("A well-used card is one of the fastest ways to build a strong credit profile \u2014 and a badly used "
               "one is the fastest way to wreck it. The habits are simple and the rewards compound."))
story.append(H2("The habits that build your score"))
story += bullets([
    "Pay the full statement, on time, every cycle \u2014 the single biggest factor in your score.",
    "Keep total utilisation under 30% across all cards; under 10% is excellent. High utilisation can cost "
    "30\u201380 points over six months.",
    "Do not close your oldest card; the length of your credit history matters.",
    "Avoid several new applications at once \u2014 each is a hard enquiry.",
])
story.append(H2("How to raise your credit limit without a needless score hit"))
story.append(P("There are two routes. A bank-initiated, pre-approved increase is usually a soft enquiry and does "
               "not touch your score \u2014 accept it in the app. A formal, out-of-cycle request through the app can "
               "trigger a hard enquiry that costs about 5\u201310 points and stays on your report, so time it well."))
story += bullets([
    "Let the bank's periodic review do the work: use 20\u201330% of your limit and pay in full for at least six "
    "consecutive months.",
    "Update your income with the bank after a raise \u2014 banks rarely refresh it on their own, and a higher "
    "documented income lifts your ceiling.",
    "Ask only once every 6\u201312 months, and only after a full cycle of low utilisation. Requesting while "
    "utilisation is high, or right after a missed payment, usually backfires.",
    "Documents usually asked for: last 2\u20133 months' salary slips (salaried), or the latest ITR plus 3\u20136 months' "
    "bank statements (self-employed).",
])
story.append(Callout("The 30-30 rule",
                     "Before requesting a limit increase: bring utilisation below 30% for one full billing cycle, "
                     "document a 30%+ jump in income, and wait 30+ days after any major positive credit event. Hit "
                     "all three and your odds improve sharply.",
                     bg=colors.HexColor("#eaf5ee"), bar=GREEN))
story.append(PageBreak())

# ---- Chapter 12 ----
story += H1("Chapter 12", "Your 30-Day Action Plan")
story.append(H2("Week 1 \u2014 Audit"))
story += bullets([
    "List every card: network, annual fee and its waiver threshold, interest rate, statement date, due date.",
    "For each card, note the earn rate in your top two categories, the cap, and the exclusions from the MITC.",
    "Total your reward points and check for any expiry dates this quarter.",
])
story.append(H2("Week 2 \u2014 Fix"))
story += bullets([
    "Set auto-pay for the total amount due on every card. Not the minimum.",
    "If a balance is revolving, start the escape plan: EMI conversion, personal loan, or balance transfer.",
    "Ask your main issuer to move your billing cycle so the due date falls just after your salary.",
])
story.append(H2("Week 3 \u2014 Optimise"))
story += bullets([
    "Assign each spending category to the card that wins there, and stop using the wrong card by habit.",
    "Link a RuPay credit card to UPI if it earns on UPI spends \u2014 verify in the MITC first.",
    "Before your next big purchase, compare the festive bank offer against your own card's earn using the "
    "crossover rule.",
])
story.append(H2("Week 4 \u2014 Automate and protect"))
story += bullets([
    "Turn on transaction alerts and app lock/unlock; set online spend limits.",
    "Redeem expiring points; if a devaluation was announced, redeem before it lands.",
    "If your income rose, update it with the bank; if utilisation is under 30%, request a limit increase the "
    "smart way.",
])
story.append(Callout("Printable: your monthly card health-check",
                     "\u25a1 Paid every card in full by the due date   \u25a1 Utilisation under 30%   \u25a1 Points checked for "
                     "expiry   \u25a1 No category spends above their cap   \u25a1 Statements reviewed for errors   "
                     "\u25a1 Alerts on   \u25a1 No new balance revolving",
                     bg=LIGHT, bar=NAVY))
story.append(PageBreak())

# ---- Appendix A ----
story += H1("Appendix A", "AI Prompt Pack")
story.append(P("Copy these into any AI assistant (ChatGPT, Gemini, Claude) to turn the method into a personal plan. "
               "Replace the brackets with your own numbers. Do not enter your card number, CVV, OTP or PIN into any "
               "AI tool."))
prompts = [
    ("Pick my best card",
     "I spend about \u20b9[amount] a month, split roughly: online shopping [%], groceries [%], food delivery [%], "
     "dining [%], fuel [%], utilities [%], UPI scans [%]. I want to maximise rewards without an annual fee over "
     "\u20b9[amount]. Compare the cards that fit and show me the net annual value after caps and exclusions."),
    ("Decode a card's MITC",
     "Here is the rewards section of a card's MITC: [paste text]. Summarise in a table: the earn rate per "
     "category, the monthly or quarterly cap, the excluded categories, and anything that applies specifically to "
     "UPI spends."),
    ("Festive-sale decision",
     "I am buying a [product] for \u20b9[amount] on [Amazon/Flipkart] during the festive sale. I hold [card A] and "
     "[card B]. Work out the final price with the bank offer versus the rewards my own card would earn, and tell "
     "me which is cheaper and why."),
    ("Minimum-due escape plan",
     "I have a \u20b9[amount] balance revolving at [rate]% a month on a card. Compare paying the minimum versus "
     "converting to a 12-month EMI at [rate]% versus a personal loan at [rate]%, and give me the total cost and "
     "the cheapest realistic path."),
    ("Statement audit",
     "Here is my card statement summary for the month: [paste the category totals]. Identify where my rewards are "
     "below what my cards should pay, and which spends hit a cap or an exclusion."),
    ("Billing-cycle timing",
     "My statement closes on the [date] and the due date is the [date]. My salary arrives on the [date]. Suggest "
     "the best billing-cycle change under RBI rules and when I should time large purchases for the longest "
     "interest-free period."),
    ("Reward-point value",
     "I have [number] points on [card]. I can redeem them for statement credit, vouchers or air miles. Compare the "
     "real value of each option per point and tell me the best use."),
    ("Limit-increase script",
     "Write me a short, polite request to my bank's app chat asking for a credit-limit increase, given that I have "
     "paid in full for [months] months, my utilisation is [%], and my income rose to \u20b9[amount] a month."),
]
for t, b in prompts:
    story.append(H3(t))
    story.append(P(b))
story.append(PageBreak())

# ---- Appendix B ----
story += H1("Appendix B", "Cheat Sheet and Glossary")
story.append(H2("The one-page cheat sheet"))
story.append(mktable(
    ["Situation", "What to do"],
    [
        ["Normal month", "Pay the full statement by the due date. Set auto-pay for the total, not the minimum."],
        ["Want the longest free credit", "Buy at the start of the billing cycle; change the cycle to sit after your salary."],
        ["Big purchase in a festive sale", "Compare bank discount (after its cap) against your own card's earn; split across reset days."],
        ["Balance you cannot clear this month", "Convert to EMI immediately; do not let it revolve at 40%+."],
        ["Already revolving", "Stop new spending, convert to EMI or a personal loan, then set auto-pay for the full amount."],
        ["Choosing a card", "Compare after caps and exclusions, not the headline rate. Keep to 2\u20133 cards."],
        ["An adverse change is announced", "Redeem points before it lands; exit the card with no closure charge if it no longer earns its fee."],
        ["Lost card or fraud", "Block in the app, report immediately, keep the reference, escalate to the RBI Ombudsman if unresolved."],
    ],
    [175, 333]))
story.append(Spacer(1, 8))
story.append(H2("Glossary"))
gloss = [
    ("APR", "Annual Percentage Rate \u2014 the yearly cost of borrowing, including the effect of monthly compounding."),
    ("Billing cycle", "The period between two statement dates, usually about 30 days."),
    ("Cap", "The maximum reward or discount a card pays in a period; beyond it, the base rate or zero applies."),
    ("CIBIL", "India's main credit bureau; your score (300\u2013900) summarises your repayment behaviour."),
    ("Grace period", "The interest-free window on a card, provided the previous balance is fully cleared."),
    ("MCC", "Merchant Category Code \u2014 the code a terminal sends, which decides whether a spend earns."),
    ("Minimum amount due", "The smallest payment that keeps the account current; not a repayment plan."),
    ("MITC", "Most Important Terms and Conditions \u2014 the authoritative document for a card's rates, caps and fees."),
    ("Revolving credit", "Carrying a balance month to month; the most expensive way to use a card."),
    ("Utilisation ratio", "Outstanding balance as a percentage of your total limit; keep it under 30%."),
]
for k, v in gloss:
    story.append(PR("<b>%s</b> \u2014 %s" % (esc(k), esc(v)), "bullet"))
story.append(Spacer(1, 6))
story.append(H2("Frequently asked questions"))
faqs = [
    ("Will paying only the minimum due hurt my credit score?",
     "Not immediately \u2014 it keeps the account current and avoids a late fee. But it pushes utilisation high, which "
     "can drag your score down over months, and it is by far the most expensive way to borrow."),
    ("Is the 10% festive-sale discount always the best option?",
     "No. It is capped per order, has exclusions, and on Amazon SBI reclaims your reward points. Above roughly "
     "\u20b930,000 a 5%-back card often beats it. Compare the final price."),
    ("Can I use any credit card on UPI?",
     "Only RuPay credit cards can be linked to UPI as of October 2026. Visa and Mastercard credit cards cannot."),
    ("Should I close a card I no longer use?",
     "Usually no. Closing it removes available credit and shortens your history. Keep it open with light use and "
     "ask for a fee waiver if the fee is the issue."),
    ("Are reward points guaranteed to keep their value?",
     "No. Programmes get devalued, though RBI requires at least 30 days' notice of adverse changes. Redeem "
     "regularly and watch for devaluation notices."),
]
for q, a in faqs:
    story.append(H3(q))
    story.append(P(a))
story.append(Spacer(1, 10))
story.append(GoldRule())
story.append(P("The Smart Credit Card Playbook 2026 \u2014 India Edition. Published by Digitalaikart. Every card "
               "rate, cap, rule and offer was verified against official issuer terms, RBI directions and platform "
               "offer pages in October 2026. Credit card terms change frequently \u2014 confirm the current terms in "
               "your card's MITC before you apply or spend. This guide is educational and is not personalised "
               "financial advice.", "small"))


def build(path):
    doc = BaseDocTemplate(path, pagesize=A4,
                          leftMargin=48, rightMargin=48, topMargin=64, bottomMargin=58,
                          title="The Smart Credit Card Playbook 2026 - India Edition",
                          author="Digitalaikart")
    frame = Frame(48, 58, A4[0] - 96, A4[1] - 64 - 58, id="main",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame])])
    doc.build(story, canvasmaker=BookCanvas)
    print("built", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    out = os.environ.get("PDF_OUT",
                         os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "smart-credit-card-playbook-2026.pdf"))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    build(out)
