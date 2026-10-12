# -*- coding: utf-8 -*-
"""Deterministic premium PDF builder for The AI Prompt Pack for Indian Real Estate Agents.
Navy #0a1628 / gold #f5c542. Built with reportlab in invariant mode so the byte
output is reproducible on CI."""
import os, sys

os.environ.setdefault("SOURCE_DATE_EPOCH", "1760000000")
import reportlab.rl_config as rl_config
rl_config.invariant = 1
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether,
                                Flowable, NextPageTemplate)

NAVY = colors.HexColor("#0a1628")
NAVY2 = colors.HexColor("#12233d")
GOLD = colors.HexColor("#f5c542")
GOLD_D = colors.HexColor("#c99a1e")
INK = colors.HexColor("#1b2436")
GREY = colors.HexColor("#5b6678")
LIGHT = colors.HexColor("#f4f6fa")
LIGHT2 = colors.HexColor("#eef2f9")
LINEC = colors.HexColor("#d8dee9")
WHITE = colors.white

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

S = {}
S['h1'] = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=23, leading=27, textColor=NAVY, spaceAfter=4)
S['lead'] = ParagraphStyle('lead', fontName='Helvetica', fontSize=11, leading=16, textColor=GREY, spaceAfter=10)
S['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=10.2, leading=15.4, textColor=INK, spaceAfter=7, alignment=TA_JUSTIFY)
S['bodyc'] = ParagraphStyle('bodyc', parent=S['body'], alignment=TA_LEFT)
S['sechead'] = ParagraphStyle('sechead', fontName='Helvetica-Bold', fontSize=15.5, leading=19, textColor=WHITE)
S['secsub'] = ParagraphStyle('secsub', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor("#cdd7e6"))
S['ptitle'] = ParagraphStyle('ptitle', fontName='Helvetica-Bold', fontSize=10.6, leading=14, textColor=NAVY, spaceAfter=2)
S['ptext'] = ParagraphStyle('ptext', fontName='Helvetica', fontSize=9.2, leading=13.2, textColor=INK)
S['note'] = ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=9, leading=13, textColor=GREY)
S['bullet'] = ParagraphStyle('bullet', fontName='Helvetica', fontSize=10, leading=14.6, textColor=INK, leftIndent=12, bulletIndent=2, spaceAfter=3)
S['cellh'] = ParagraphStyle('cellh', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=WHITE)
S['cell'] = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.8, leading=12, textColor=INK)
S['cellb'] = ParagraphStyle('cellb', fontName='Helvetica-Bold', fontSize=8.8, leading=12, textColor=NAVY)
S['quote'] = ParagraphStyle('quote', fontName='Helvetica-Oblique', fontSize=10.5, leading=15, textColor=NAVY, alignment=TA_CENTER)

def esc(t):
    return t

def P(t, st='body'):
    return Paragraph(t, S[st])

class GoldRule(Flowable):
    def __init__(self, width=40, thickness=3, color=GOLD):
        Flowable.__init__(self)
        self.width = width; self.thickness = thickness; self.color = color
    def wrap(self, aw, ah):
        self._w = self.width if self.width else aw
        return (self._w, self.thickness + 2)
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self._w, self.thickness, stroke=0, fill=1)

def section_banner(num, title, sub):
    t = Table([[Paragraph(f"{num} &nbsp;·&nbsp; {title}", S['sechead'])],
               [Paragraph(sub, S['secsub'])]],
              colWidths=[PAGE_W - 2*MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (0,0), 11),
        ('BOTTOMPADDING', (0,0), (0,0), 0),
        ('TOPPADDING', (0,1), (0,1), 1),
        ('BOTTOMPADDING', (0,1), (0,1), 11),
        ('LINEBEFORE', (0,0), (0,-1), 4, GOLD),
    ]))
    return t

def prompt_box(name, text):
    inner = [Paragraph(name, S['ptitle']), Paragraph(text, S['ptext'])]
    t = Table([['', inner]], colWidths=[3.2, (PAGE_W - 2*MARGIN) - 3.2])
    t.setStyle(TableStyle([
        ('BACKGROUND', (1,0), (1,0), LIGHT),
        ('BACKGROUND', (0,0), (0,0), GOLD),
        ('LEFTPADDING', (0,0), (0,0), 0), ('RIGHTPADDING', (0,0), (0,0), 0),
        ('TOPPADDING', (0,0), (0,0), 0), ('BOTTOMPADDING', (0,0), (0,0), 0),
        ('LEFTPADDING', (1,0), (1,0), 10), ('RIGHTPADDING', (1,0), (1,0), 10),
        ('TOPPADDING', (1,0), (1,0), 8), ('BOTTOMPADDING', (1,0), (1,0), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return KeepTogether([t, Spacer(1, 6)])

def bullets(items):
    return [Paragraph(i, S['bullet'], bulletText='•') for i in items]

def callout(title, text, bg=LIGHT2, bar=GOLD_D):
    inner = [Paragraph(title, ParagraphStyle('ct', fontName='Helvetica-Bold', fontSize=10.4, leading=14, textColor=NAVY, spaceAfter=3)),
             Paragraph(text, S['ptext'])]
    t = Table([['', inner]], colWidths=[3.2, (PAGE_W - 2*MARGIN) - 3.2])
    t.setStyle(TableStyle([
        ('BACKGROUND', (1,0), (1,0), bg),
        ('BACKGROUND', (0,0), (0,0), bar),
        ('LEFTPADDING', (0,0), (0,0), 0), ('RIGHTPADDING', (0,0), (0,0), 0),
        ('TOPPADDING', (0,0), (0,0), 0), ('BOTTOMPADDING', (0,0), (0,0), 0),
        ('LEFTPADDING', (1,0), (1,0), 10), ('RIGHTPADDING', (1,0), (1,0), 10),
        ('TOPPADDING', (1,0), (1,0), 9), ('BOTTOMPADDING', (1,0), (1,0), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return KeepTogether([t, Spacer(1, 8)])

def data_table(header, rows, widths):
    data = [[Paragraph(h, S['cellh']) for h in header]]
    for r in rows:
        data.append([Paragraph(str(c), S['cell'] if i == 0 else S['cell']) for i, c in enumerate(r)])
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.4, LINEC),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LINEBEFORE', (0,0), (0,-1), 3, GOLD),
    ]
    t.setStyle(TableStyle(style))
    return t

# ---------------- CONTENT ----------------
SECTIONS = []

def add(num, title, sub, intro, prompts):
    SECTIONS.append(dict(num=num, title=title, sub=sub, intro=intro, prompts=prompts))

add("Section 1", "Property Listing Descriptions",
    "Portals: 99acres, MagicBricks, Housing.com, NoBroker, Square Yards",
    "A buyer scans a listing in about six seconds. Weak copy gets scrolled past; a clear, specific listing gets the enquiry. These prompts turn a few facts about a property into copy that reads like a human wrote it — and that stays on the right side of RERA's 'no misleading representation' rule. Always paste the real facts; the AI only writes, you verify.",
    [
    ("1. The 150-word portal listing (sale)",
     "You are a top Indian real estate copywriter. Write a 150-word listing description for a [3BHK] apartment in [society/locality], [city]. Facts: [carpet area sq ft], [floor/total floors], [facing], [age], [parking], [amenities], [possession status: ready/under construction], [price], [RERA registered: yes/no]. Rules: open with the single strongest fact, not 'This beautiful property'. Write for a [family/end-user] buyer. Plain, warm English. No exclamation marks. Do not use the words stunning, cozy, dream home, or entertainer's dream. End with a one-line call to action for a site visit."),
    ("2. The premium listing (understated, no hype)",
     "Act as a luxury real estate copywriter for India's HNI market. Write a 130-word description for a [4BHK] in [locality], [city], priced [₹X crore]. Include: [carpet area], [floor], [view/private lift/podium], [interiors by X], [amenities]. Tone: calm and factual, like a private-client brochure. Absolutely no hype words (no 'magnificent', 'opulent', 'dream'). Mention the neighbourhood's real draw — [schools/club/connectivity] — in one line. Close with a discreet invitation to a private viewing."),
    ("3. The rental listing (tenant-first, short)",
     "Write a 90-word rental listing for a [2BHK] in [locality], [city]. Facts: [furnishing], [carpet area], [floor], [parking], [water/power backup], [deposit], [monthly rent], [available from]. Write for [working professionals / families / students]. Lead with what a tenant cares about first: furnishing, connectivity, and the deposit. Keep it honest — if there is no lift or the flat is a [4th] floor walk-up, say so. End with 'Message on WhatsApp to schedule a visit.'"),
    ("4. The plot / land listing",
     "You are a real estate writer specialising in land. Write a 110-word listing for a [dimension, e.g. 30x40] plot in [layout/locality], [city]. Facts: [total area sq ft / sq yd], [facing], [road width], [approvals: DTCP/BDA/gram panchayat], [khata/patta status], [corner plot: yes/no], [price per sq ft], [water/electricity nearby]. State clearly what is approved and what is not — buyers of land check this first. Avoid any promise of appreciation or guaranteed returns."),
    ("5. The commercial listing (shop / office)",
     "Write a 110-word listing for a [shop/office] space in [area], [city]. Facts: [carpet area], [frontage], [floor], [footfall/landmark], [rent/sale price], [parking], [power load], [suitable for: retail/clinic/office]. Write for a business owner who cares about footfall, access and rent-vs-revenue. Mention GST applicability on under-construction commercial space in one line if relevant. End with a call to schedule a walkthrough."),
    ("6. Turn my rough notes into a clean listing",
     "Rewrite the following rough notes into a polished 140-word property listing. Keep every fact exactly as given — do not invent amenities, measurements or approvals. Notes: [paste your raw notes]. Format: one strong opening line, a short paragraph of facts, a bulleted 'Highlights' list of 4 items, and a closing call to action. Fix grammar and repetition. Keep it simple enough for a first-time buyer to understand."),
    ("7. The compliance-safe listing (no misleading claims)",
     "Review my draft listing below and make it compliant and honest. Remove any claim that could be read as misleading or a guaranteed return, any promise of appreciation, any 'best project' or superlative without proof, and any implied approval the property does not have. Keep the selling points that are factual. Return the cleaned listing plus a short list of the specific phrases you removed and why. Draft: [paste your listing]."),
    ("8. Three variants for A/B testing",
     "Write three different 120-word listing descriptions for the same property, each using a different lead angle: (a) the investment/financial angle, (b) the lifestyle/family angle, (c) the location/connectivity angle. Property facts: [paste facts]. Keep all three honest and free of hype. Label them Variant A, B and C so I can post each on a different portal or ad and see which gets more enquiries."),
    ])

add("Section 2", "WhatsApp Lead Follow-up",
    "Speed wins deals — most buyers message several agents at once",
    "In Indian real estate the deal is often decided in the first few minutes. Buyers usually enquire with three or four agents at the same time, so the first useful reply often wins the site visit. These prompts help you reply fast, qualify without interrogating, and follow up for weeks without sounding like spam. Send from your WhatsApp Business number and always read before you send.",
    [
    ("9. The instant first reply (under 60 seconds)",
     "Write a short, warm WhatsApp reply to a new property enquiry. Enquiry was about: [3BHK in Whitefield under ₹1.5 crore]. Reply must: greet, confirm we have [X] options, ask one qualifying question (budget confirmation or preferred visit day), and end with a question so the conversation keeps going. Under 45 words. Friendly, no emojis spam (maximum one). Do not send a wall of text. Also give me a 20-word version I can send at 11pm when I am busy."),
    ("10. Qualification questions that don't feel like a form",
     "Give me a natural WhatsApp flow of 4 short messages that qualify a property buyer. I need to learn: budget range, preferred locality/configuration, ready-to-move vs under-construction, and purchase timeline. Each message must ask only ONE question and sound like a person, not a form. After the 4 questions, suggest how to tag the lead as Hot / Warm / Cold. Context: I am a broker in [city]."),
    ("11. Hinglish version for local buyers",
     "Rewrite this WhatsApp message in friendly Hinglish (Hindi written in English letters) the way a broker in [city] actually talks to local buyers. Keep it respectful and professional — no slang that could offend. Keep all facts exactly as given. Message: [paste your English message]."),
    ("12. The 7-touch follow-up sequence (30 days)",
     "Create a 7-message WhatsApp follow-up sequence spread over 30 days for a warm property lead who has gone quiet. Lead context: [interested in 3BHK, saw one flat, said 'will get back']. Each message must give a reason to reply (a new listing, a price update, a question, a useful tip) and never just say 'following up'. Number them with the day to send. Keep each under 40 words. Stop-the-sequence rule: if the lead replies, I continue the conversation normally."),
    ("13. Site-visit booking and reminder",
     "Write three WhatsApp messages: (1) offering two specific site-visit slots for [Saturday 4pm or Sunday 11am], (2) a confirmation with the location pin request and what to bring, (3) a reminder for the morning of the visit. Property: [3BHK, Prestige Lakeside, ₹1.4 crore]. Friendly, short, and clear. The reminder should reduce no-shows without sounding pushy."),
    ("14. Revive a dead lead (30+ days silent)",
     "Write a 2-message WhatsApp sequence to re-open a conversation with a buyer who went silent over a month ago. Do not guilt them or ask 'are you still interested?'. Instead, lead with something genuinely new and useful — [a similar flat that just came up / a price correction / a new RERA-registered project in their area]. Lead context: [paste]. Under 45 words each. Give a soft, easy exit if they are no longer looking."),
    ("15. New-listing / price-drop broadcast",
     "Write a WhatsApp broadcast announcing [a new listing / a price drop] to my list of [buyers looking in Whitefield]. Include: the one-line headline, 3 key facts, price, and a clear 'reply YES for photos and details'. Keep it under 60 words, no misleading urgency, and make it easy to opt out. Do not claim it is a limited-time offer unless that is actually true."),
    ("16. Post-site-visit thank you and next step",
     "Write a WhatsApp message to send within two hours of a site visit. Property: [X]. Buyer's likely concern: [price / vastu / floor]. Message must: thank them, address that one concern with a factual point, and suggest the next concrete step (second visit, loan pre-approval, comparing one other option). Under 55 words, warm and confident, never desperate."),
    ])

add("Section 3", "Instagram, Reels & Story Content",
    "Listings sell faster when your feed proves you know the area",
    "Most agents post the same flat photos with no hook. These prompts give you a reason for buyers to follow you: sharp Reel scripts, area-expert posts, and captions that actually get saved and shared. Post 4-5 times a week, mix listing posts with genuinely useful local content, and always add your WhatsApp number in the caption.",
    [
    ("17. 30-second Reel script for a listing",
     "Write a 30-second Instagram Reel script for a property. Structure: a 3-second hook (a question or a surprising fact about [locality]), 3 quick value points about the flat, one honest limitation, and a closing line with a call to action to DM 'VISIT'. Property: [3BHK, 1450 sq ft, Whitefield, ₹1.4 crore, ready to move]. Give shot suggestions in brackets. Spoken tone: confident, conversational, like a local expert."),
    ("18. Carousel: '5 things to check before buying in [area]'",
     "Create a 6-slide Instagram carousel titled '5 things to check before buying a flat in [locality], [city]'. Slide 1 is the cover with the title. Slides 2-6 each cover one check (for example: [RERA registration, builder's OC/CC status, carpet vs super built-up, water source, circle rate vs asking price]). For each slide give a short headline and 1-2 lines of plain explanation. Slide 6 ends with a soft call to action. Accurate and practical, no fluff."),
    ("19. Listing caption with hashtags",
     "Write an Instagram caption for a property listing post. Property: [paste facts]. Caption must: open with a hook, give the 4 most important facts, invite a DM, and end with 20 relevant hashtags mixing city, locality, property type and intent tags (for example #BangaloreRealEstate #WhitefieldFlats #3BHKForSale). Keep the caption under 120 words and genuinely useful, not just salesy."),
    ("20. Story sequence for a new launch",
     "Design a 5-frame Instagram Story sequence to tease a new listing before I post it. Frame 1: a mystery/teaser. Frame 2: a location hint. Frame 3: one standout feature. Frame 4: price range and configuration. Frame 5: swipe-up/DM call to action. For each frame give the on-screen text (max 12 words) and the visual idea. Property: [paste facts]. Keep it honest — no fake scarcity."),
    ("21. 'Myth vs fact' Reel on a rule buyers get wrong",
     "Write a 30-second Reel script debunking one common myth Indian homebuyers believe. Choose the myth: [e.g. 'you can avoid TDS by paying in cash' or 'ready-to-move flats also attract GST' or 'stamp duty is only on what you paid']. Give: the myth, why it is wrong, the correct rule with the real number or section, and a one-line takeaway. Make me sound like a trustworthy local expert, not a tax professor. Add shot notes in brackets."),
    ("22. 'Area guide' post that positions you as the expert",
     "Write an Instagram post that positions me as the go-to broker for [locality], [city]. Content: what kind of buyers the area suits, average price band per sq ft, top 3 real draws (schools, metro, tech park), one honest drawback, and what is coming up in the next 2 years. Keep it factual and balanced. End with 'DM me the word AREA for a free locality report.' Under 150 words."),
    ])

add("Section 4", "Objection Handling & Negotiation",
    "The three objections that kill most deals — and what to say",
    "Most deals are lost to the same handful of objections: it is too expensive, I will think about it, or another agent showed something cheaper. These prompts help you prepare calm, factual responses you can use on a call or a WhatsApp message. Never argue, never pressure — answer the real worry behind the words.",
    [
    ("23. 'It's too expensive'",
     "Act as an experienced Indian real estate negotiator. A buyer says the [₹1.4 crore] price for a [3BHK in Whitefield] is too high. Give me 4 responses, each under 50 words: (a) reframe to price-per-sq-ft and compare with the area average, (b) break the price into EMI so it feels real, (c) compare with two genuinely comparable recent transactions, (d) offer a middle path (a slightly different unit or floor). Tone: calm, factual, never pushy. Do not invent comparable sales — I will fill those in."),
    ("24. 'I'll think about it / will get back'",
     "A buyer is stalling with 'I'll think about it'. Give me 3 short WhatsApp responses that gently move things forward without pressure. Each must ask one useful question that reveals the real hesitation (price, family approval, loan, vastu, another option). Provide a version for a first-time buyer and a version for an investor. Under 45 words each."),
    ("25. 'Another agent showed me a cheaper flat'",
     "A buyer says another broker showed a similar flat for [₹15 lakh] less. Write a response that stays professional and never bad-mouths the other agent. It should: thank them for comparing, ask two clarifying questions (is it the same carpet area and the same approval status?), and explain the three real reasons prices differ (carpet vs super built-up, floor/facing, approvals and OC status). Under 70 words. End by offering to do an honest side-by-side."),
    ("26. Price negotiation practice (buyer side)",
     "Roleplay as a tough but fair Indian property seller's agent. I am the buyer's agent trying to negotiate a [₹1.4 crore] flat down. Respond realistically to each of my offers, using Indian market logic (circle rate, demand in the area, comparable sales). Start by asking me for my best offer. After 4 rounds, break character and tell me which of my arguments were strong and which were weak."),
    ("27. Coaching the owner on price expectations",
     "Write a WhatsApp message to a flat owner whose asking price of [₹1.5 crore] is above what the market is paying in [locality]. Message must: respect their expectation, show the evidence (current asking vs actual closed prices per sq ft in the area), explain the cost of sitting unsold, and propose a realistic price band. Under 90 words. Never insult their property or their judgement."),
    ("28. Home-loan and EMI reassurance",
     "A buyer is worried about affording the EMI. Write a short, reassuring WhatsApp message that explains the home-loan basics in plain English: indicative EMI for [₹1.1 crore loan] over [20 years] at [current rate], what documents the bank needs, and that pre-approval is free and takes a few days. Include a one-line note that rates vary by bank and profile. Under 80 words, no jargon."),
    ])

add("Section 5", "Winning New Listings (Seller / Owner Side)",
    "Your income depends on sellers trusting you — not just buyers",
    "Half of an agent's job is finding owners who want to sell. These prompts help you reach owners honestly and get the mandate. Never claim you already have a buyer if you do not — it damages trust and can breach RERA's rules against false representation. Build a genuine buyer list first, then these messages land far better.",
    [
    ("29. Outreach to an owner listed elsewhere",
     "Write a short WhatsApp message to a flat owner whose property has been listed on a portal for [90 days] without selling. Do not criticise the other agent. Explain in 3 lines: what I do differently (a qualified buyer list, weekly feedback, honest pricing advice), and ask for a 10-minute call. Under 60 words, respectful, no spammy claims. Context: property is a [3BHK in Whitefield]."),
    ("30. The 'sell faster' pitch",
     "Write a 70-word message to a society owner who is thinking of selling. Lead with one concrete, honest benefit (access to my active buyer list, professional photos, portal + WhatsApp marketing). Include a soft proof point placeholder like [sold X flats in this society in the last year]. End with a low-commitment ask: a free 10-minute valuation. No fake urgency."),
    ("31. Society / door-to-door outreach script",
     "Give me a 45-second door-to-door script for meeting owners in [society name]. It should: introduce me as the local specialist for the area, ask a soft opening question (are you or anyone you know planning to sell?), hand over a card, and leave without pressure. Also give a shorter version for the building security or the secretary, and one polite line to use if the owner is busy."),
    ("32. Referral request message",
     "Write a WhatsApp message asking a past client for a referral. Client bought/sold: [3BHK in Whitefield, closed in March]. Message must: thank them, remind them briefly of the good outcome, and ask if they know anyone planning to buy or sell in the area. Offer to handle it personally. Under 55 words, warm, no pressure, no generic 'Dear valued client' tone."),
    ("33. Owner onboarding checklist message",
     "Write a WhatsApp message that onboards a new seller after they agree to list with me. It should confirm: the agreed asking price, what I will do in the first 7 days (photos, portal upload, WhatsApp broadcast to my buyers), what I need from them (documents list), and when they will hear from me (weekly update). Under 90 words, structured and reassuring. Include a line that I will always share honest buyer feedback."),
    ])

add("Section 6", "Rentals & Commercial Spaces",
    "Rentals close fast — reply speed and clarity decide it",
    "Rental and commercial deals move quickly and often hinge on a few practical details: deposit, furnishing, and whether the space suits the tenant's business. These prompts help you write clear listings, screen tenants fairly, and handle the deposit conversation. Keep screening lawful — never screen or refuse on the basis of religion, caste, region, gender, marital status or dietary preference.",
    [
    ("34. Rental listing for students / working bachelors",
     "Write a 90-word rental listing for a [2BHK] in [locality], [city] aimed at [working professionals / students]. Facts: [furnishing], [rent], [deposit], [water/power backup], [distance to metro/college/tech park], [house rules if any]. Be upfront about any restriction (for example, no smoking, or owners' society rules) so I get genuine enquiries only. End with a WhatsApp call to action. Fair and inclusive language only."),
    ("35. Commercial space listing (shop / office)",
     "Write a 100-word listing for a [shop/office] on rent in [area], [city]. Facts: [carpet area], [frontage], [floor], [footfall], [rent], [deposit], [fit-out status], [suitable businesses]. Write for a business owner comparing 3 spaces. Lead with footfall and access. Mention GST on commercial rent for a registered tenant in one line. End with a call to schedule a viewing."),
    ("36. Rent and deposit negotiation message",
     "Write a WhatsApp message to a prospective tenant who is negotiating the rent and deposit for [2BHK, ₹35,000/month, 3-month deposit]. Message must: acknowledge their point, explain what the deposit covers, offer one fair option (for example, [2-month deposit for a longer lease] if the owner agrees), and keep the door open. Under 70 words. Do not promise anything the owner has not approved — leave a [confirm with owner] note."),
    ("37. Landlord onboarding message",
     "Write a WhatsApp message to onboard a landlord who wants to rent out a [2BHK in Whitefield]. It should confirm: the agreed monthly rent, my process (photos, portal listing, tenant screening, agreement and police verification help), my fee, and what I need from them. Under 90 words, clear and reassuring. Include a line on how I screen tenants fairly and lawfully."),
    ("38. Fair tenant screening questions",
     "Give me a short, lawful set of tenant-screening questions for renting out a [2BHK] in [city]. I need to confirm: number of occupants, employment/income stability, intended lease length, and whether they will keep a pet. Explain in one line why I must NOT ask about religion, caste, region, marital status, gender or food habits, and how to phrase each question politely over WhatsApp."),
    ])

add("Section 7", "NRI & HNI Clients",
    "NRIs buy remotely — trust and clarity do the selling",
    "NRI and high-net-worth buyers need a different style: they are often in a different time zone, they worry about compliance, and they value discretion. These prompts help you communicate clearly across time zones, explain the tax rules accurately, and run smooth virtual site visits. Always confirm current tax rules with a CA before advising a client.",
    [
    ("39. NRI welcome message (time-zone aware)",
     "Write a warm WhatsApp message to an NRI buyer in [Dubai] enquiring about a [3BHK in Bengaluru] for investment. Message must: acknowledge the time difference and offer to call at a time that suits them, confirm I will send a full pack (photos, floor plan, price sheet, locality report), and ask what matters most to them (rental yield, capital growth, or family use). Under 70 words, professional and reassuring."),
    ("40. Explaining TDS to an NRI seller (accurate)",
     "Write a clear, accurate WhatsApp explanation for an NRI client selling a property in India. Cover: when the buyer must deduct tax, that there is NO ₹50 lakh threshold for NRI sellers, the typical rate for long-term gains (about 12.5% plus surcharge and cess, which works out to roughly 15% in many cases), and that a lower-deduction certificate can reduce it. Add a line recommending they confirm with their CA. Under 110 words, no jargon."),
    ("41. Virtual site-visit / video walkthrough message",
     "Write a WhatsApp message proposing a live video walkthrough for an overseas buyer. Include: what I will show (entrance, living area, kitchen, bedrooms, balcony view, common areas), that I will walk through the flat live so they can ask questions, the time in their local time zone, and what I will send after (recording + floor plan + locality photos). Under 80 words."),
    ("42. HNI concierge follow-up",
     "Write a discreet follow-up WhatsApp message for a high-net-worth client who viewed a [₹5 crore] property. Tone: understated, respectful of their time, no pressure. Summarise the 2-3 facts they cared about, offer to arrange anything else they need (a second viewing, an interior designer, a loan discussion), and let them set the pace. Under 70 words."),
    ])

add("Section 8", "Builder Projects & Channel Partners",
    "Channel partners earn on relationships and clear information",
    "If you sell for builders as a channel partner, your value is fast, accurate information and good follow-up. These prompts help you announce launches, pitch builders for tie-ups, and run site-visit events. Only claim a price increase, a launch or a limited offer if it is genuinely true — false urgency is the fastest way to lose a builder's trust.",
    [
    ("43. Project launch announcement broadcast",
     "Write a WhatsApp broadcast announcing the launch of [project name], [locality], [city]. Include: configuration and carpet area, starting price, possession timeline, RERA registration number, and a 'reply YES for the price sheet and floor plan'. Keep it under 80 words. Only include urgency if the builder has genuinely confirmed it. End with an opt-out line."),
    ("44. Channel-partner pitch to a builder",
     "Write a short, professional email to a builder's sales head proposing a channel-partner tie-up. Include: who I am, my buyer base in [area], what I can deliver (qualified site visits per month), my channel-partner code/registration, and a request for the current price sheet and commission terms. Under 150 words. Confident and specific, no fluff."),
    ("45. Site-visit event invitation",
     "Write a WhatsApp invite for a site-visit event at [project name] on [date], with [free cab / refreshments / a launch offer]. Include: what buyers will see (sample flat, amenities, master plan), why now, and a clear 'reply YES to book a slot'. Under 70 words. Keep any offer factual — describe exactly what is included, nothing more."),
    ("46. Price-increase notice (only if genuine)",
     "The builder has genuinely confirmed a price increase effective [date]. Write a factual WhatsApp message to my interested buyers: state the current price, the confirmed new price and effective date, and invite them to book at the current price before the change. No exaggeration, no fake scarcity. Under 70 words. If any detail is not confirmed, leave a [confirm] placeholder."),
    ])

add("Section 9", "Property Ads That Generate Leads",
    "Click-to-WhatsApp ads work best when the ad does the qualifying",
    "Paid ads are the fastest way to get leads — but a bad ad wastes money. These prompts write the primary text, headlines and creative briefs for Meta and Google campaigns, and set up a clean A/B test. Point every ad at WhatsApp, not a form, so the buyer can talk to you in one tap.",
    [
    ("47. Meta click-to-WhatsApp ad",
     "Write a Facebook/Instagram click-to-WhatsApp ad for a [3BHK in Whitefield, ₹1.4 crore]. Give me: 3 primary text options (each under 90 words), 3 headlines (max 40 characters), and a one-line description. Each ad must lead with a real benefit or a question, include the key facts, and end with 'Tap to chat on WhatsApp'. Target audience suggestion: [buyers in Bengaluru aged 30-45]. No misleading claims."),
    ("48. Google Search ad for a locality + configuration",
     "Write Google Search ads for the keyword '[3BHK for sale in Whitefield]'. Give me 3 headlines (max 30 characters each), 2 descriptions (max 90 characters each), and 5 negative keywords to avoid junk clicks. Include the real selling points (carpet area, price band, RERA registration). Keep it factual and relevant to the search intent."),
    ("49. Creative brief for a designer (Canva)",
     "Write a one-page creative brief for a designer making Instagram ad creatives for a property. Include: the property, the target buyer, the single message, the exact text to appear on the creative, the colour/mood direction, the format (1080x1350 feed + 1080x1920 story), and 3 layout ideas. Also list what must NOT appear (for example, misleading price claims or watermarks on photos)."),
    ("50. Five ad angles to A/B test",
     "Give me 5 different ad angles to test for the same property: (a) price/EMI angle, (b) locality/connectivity angle, (c) family lifestyle angle, (d) investment/rental-yield angle, (e) urgency/new-listing angle. For each, write one 60-word primary text and one headline. Property facts: [paste]. Keep every angle honest — the urgency angle must use only a genuine reason. Tell me how to compare results after 7 days."),
    ])

add("Section 10", "Admin, Paperwork & Follow-up Systems",
    "The unglamorous work that actually closes deals",
    "Deals are won in the follow-up and lost in the paperwork. These prompts turn messy notes and transcripts into clean records, build your document checklists, and draft the polite messages that keep a transaction moving. Use them to save hours every week — and to make sure nothing slips.",
    [
    ("51. Document checklist for a resale purchase",
     "Create a clear document checklist for a resale flat purchase in [city], written for a first-time buyer. Group the documents into: seller's ownership documents, approvals and society documents, and buyer-side items. Include the key ones like sale deed/chain of title, latest tax receipts, OC/CC, RERA registration where applicable, NOCs, and the TDS and registration paperwork. Add a one-line note on what each document proves. Plain English."),
    ("52. Weekly site-visit route and schedule",
     "I have these site visits this week: [list of properties with areas and preferred times]. Build me an efficient day-by-day route that groups properties by locality to cut travel, leaves buffer time between visits, and flags any that are far apart. Output as a simple table: Day, Time, Property, Area, Travel note. Also suggest which buyer to pair with which property."),
    ("53. Turn a call transcript into CRM notes",
     "Turn this call transcript with a buyer into structured CRM notes. Output: Buyer name, Budget, Configuration, Preferred locality, Timeline, Home-loan status, Main concern, Next action and date. Keep it factual — do not add anything that was not said. If something is unclear, write 'not stated' rather than guessing. Transcript: [paste transcript]."),
    ("54. Weekly pipeline review summary",
     "Summarise my week's pipeline into a short report I can send myself or my team. Input: [list of leads with their stage and last contact date]. Output: total active leads, hot/warm/cold split, leads with no contact in 7+ days (flag these), deals likely to close this week, and my top 3 priorities for next week. Keep it under 150 words."),
    ("55. Google review request message",
     "Write a short WhatsApp message asking a happy client for a Google review after a deal closes. Make it easy: include where to click, why it helps me (trust for other buyers), and a line that they can be as brief or as detailed as they like. Under 45 words, warm and genuine. Add a polite line so they do not feel obliged."),
    ])

add("Section 11", "Personal Branding & Market Updates",
    "The agent buyers remember is the one who is useful before the sale",
    "The agents who win long-term are the ones who share useful market information, not just listings. These prompts build your profile, your monthly market update, and social proof. Post consistently — two useful posts a week beats ten listing dumps a month.",
    [
    ("56. Monthly market update for your area",
     "Write a monthly market-update post for [locality], [city], for my Instagram and WhatsApp status. Include: average asking price per sq ft now vs last quarter, whether it is a buyer's or seller's market, one thing that changed (a new metro line, a price correction, new supply), and one practical tip for buyers or sellers this month. Keep it factual and balanced, under 150 words. End with a soft call to action to DM for a full report."),
    ("57. Profile and bio for portals and social",
     "Write my professional bio in three lengths: (a) a 40-word portal profile, (b) a 150-character Instagram bio, (c) a 120-word LinkedIn 'About' section. Details: [name], RERA-registered agent in [city], specialises in [locality/residential], [X] years' experience, [X] families helped. Tone: trustworthy, specific, human. Avoid cliches like 'passionate about real estate'."),
    ("58. Client testimonial post",
     "Turn this client feedback into a clean Instagram testimonial post. Feedback: [paste what the client said]. Output: a short caption that tells the mini-story (what they wanted, what we did, the result), a headline, and 8 hashtags. Keep the client's privacy — use [First name, locality] only unless they agreed to more. Under 120 words."),
    ])

# ---------------- DOC BUILD ----------------
def cover(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # gold frame
    canv.setStrokeColor(GOLD)
    canv.setLineWidth(2)
    canv.rect(14*mm, 14*mm, PAGE_W-28*mm, PAGE_H-28*mm, stroke=1, fill=0)
    # top brand
    canv.setFillColor(GOLD)
    canv.setFont('Helvetica-Bold', 15)
    canv.drawCentredString(PAGE_W/2, PAGE_H-32*mm, "DIGITALAIKART")
    canv.setFillColor(colors.HexColor("#9fb0c9"))
    canv.setFont('Helvetica', 9.5)
    canv.drawCentredString(PAGE_W/2, PAGE_H-39*mm, "PREMIUM AI DIGITAL PRODUCTS  ·  MADE FOR INDIA")
    # title block
    canv.setFillColor(WHITE)
    canv.setFont('Helvetica-Bold', 30)
    canv.drawCentredString(PAGE_W/2, PAGE_H-92*mm, "THE AI PROMPT PACK")
    canv.setFont('Helvetica-Bold', 30)
    canv.drawCentredString(PAGE_W/2, PAGE_H-105*mm, "FOR INDIAN REAL")
    canv.drawCentredString(PAGE_W/2, PAGE_H-118*mm, "ESTATE AGENTS")
    canv.setFillColor(GOLD)
    canv.rect(PAGE_W/2-30*mm, PAGE_H-127*mm, 60*mm, 2.4, stroke=0, fill=1)
    canv.setFillColor(colors.HexColor("#cdd7e6"))
    canv.setFont('Helvetica', 13)
    canv.drawCentredString(PAGE_W/2, PAGE_H-140*mm, "58 copy-paste prompts for listings, WhatsApp leads,")
    canv.drawCentredString(PAGE_W/2, PAGE_H-147*mm, "objections, ads and follow-up that wins deals")
    # feature chips
    canv.setFont('Helvetica-Bold', 11)
    chips = ["58 PROMPTS", "11 SECTIONS", "INDIA 2026 EDITION", "RERA-AWARE"]
    y = PAGE_H-172*mm
    canv.setFillColor(GOLD)
    canv.drawCentredString(PAGE_W/2, y, "   ".join(chips))
    # footer
    canv.setFillColor(colors.HexColor("#8b9bb4"))
    canv.setFont('Helvetica', 9)
    canv.drawCentredString(PAGE_W/2, 24*mm, "digitalkartai.shop")
    canv.setFont('Helvetica-Oblique', 8.5)
    canv.drawCentredString(PAGE_W/2, 18.5*mm, "Verify every fact, rule and figure before you send or publish. This pack is a drafting tool, not legal or tax advice.")
    canv.restoreState()

def later_pages(canv, doc):
    canv.saveState()
    # top hairline
    canv.setStrokeColor(LINEC); canv.setLineWidth(0.5)
    canv.line(MARGIN, PAGE_H-13*mm, PAGE_W-MARGIN, PAGE_H-13*mm)
    canv.setFillColor(NAVY); canv.setFont('Helvetica-Bold', 8)
    canv.drawString(MARGIN, PAGE_H-11*mm, "THE AI PROMPT PACK FOR INDIAN REAL ESTATE AGENTS")
    canv.setFillColor(GOLD_D); canv.setFont('Helvetica-Bold', 8)
    canv.drawRightString(PAGE_W-MARGIN, PAGE_H-11*mm, "DIGITALAIKART")
    # footer
    canv.setStrokeColor(LINEC)
    canv.line(MARGIN, 14*mm, PAGE_W-MARGIN, 14*mm)
    canv.setFillColor(GREY); canv.setFont('Helvetica', 8)
    canv.drawString(MARGIN, 10*mm, "digitalkartai.shop")
    canv.drawRightString(PAGE_W-MARGIN, 10*mm, "Page %d" % (doc.page-1))
    canv.restoreState()

def build():
    out = sys.argv[1] if len(sys.argv) > 1 else "ai-prompts-real-estate-agents-india.pdf"
    doc = BaseDocTemplate(out, pagesize=A4,
                          leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=20*mm, bottomMargin=20*mm,
                          title="The AI Prompt Pack for Indian Real Estate Agents",
                          author="Digitalaikart")
    frame = Frame(MARGIN, 20*mm, PAGE_W-2*MARGIN, PAGE_H-40*mm, id='n',
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id='cover', frames=[frame], onPage=cover),
        PageTemplate(id='body', frames=[frame], onPage=later_pages),
    ])
    story = []
    story.append(NextPageTemplate('body'))
    story.append(PageBreak())  # cover is drawn by onPage; content starts p2

    # --- Welcome ---
    story.append(Paragraph("Welcome — read this first", S['h1']))
    story.append(GoldRule(60))
    story.append(Spacer(1, 8))
    story.append(P("You are holding the prompt pack I wish existed when I started selling property. Every prompt here is written for one job: to turn the blank page — a listing, a WhatsApp reply, a Reel script, an ad — into a first draft in seconds, so you can spend your time on the part that closes deals: talking to people.", 'body'))
    story.append(P("This is not a theory book. It is a working toolkit. Each of the 58 prompts is ready to copy, paste into ChatGPT, Gemini, Claude or any AI assistant, and fill in the [brackets] with your real property details. The AI writes the first draft; you add the facts, check the numbers, and send it in your own voice.", 'body'))
    story.append(callout("The one rule that keeps you safe",
        "AI drafts, you verify, you send — in that order. AI assistants sometimes get a rule, a figure or an approval status wrong. Never publish a listing, an ad, a tax figure or a client message without reading it first. Where this pack states a legal or tax rule, confirm the current position on the official portal or with a CA before you rely on it."))
    story.append(Paragraph("How this pack is organised", ParagraphStyle('x', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=NAVY, spaceBefore=6, spaceAfter=5)))
    story += bullets([
        "<b>Section 1-2:</b> Listings and WhatsApp follow-up — the two things you do every single day.",
        "<b>Section 3-4:</b> Social content and objection handling — how you get and keep attention.",
        "<b>Section 5-8:</b> Winning sellers, rentals, NRI clients and builder projects.",
        "<b>Section 9-11:</b> Paid ads, admin systems and personal branding.",
        "<b>The Toolbox (after Section 11):</b> the 5-part prompt formula, an India rules cheat-sheet, a fill-in property brief, the 10 phrases to avoid, and a 30-day plan.",
    ])
    story.append(Spacer(1, 6))
    story.append(callout("How to get a great answer every time",
        "Give the AI three things: your role, your real facts, and your rules. Instead of 'write a listing', say 'You are an Indian real estate copywriter. Write a 150-word listing for a 3BHK in Whitefield, ₹1.4 crore, carpet 1450 sq ft, ready to move. No hype words. End with a call to action.' The more real detail you paste, the less the AI has to invent — and the safer your output.", bg=colors.HexColor("#fff8e6"), bar=GOLD))
    story.append(PageBreak())

    # --- Contents ---
    story.append(Paragraph("What's inside", S['h1']))
    story.append(GoldRule(60))
    story.append(Spacer(1, 8))
    story.append(P("58 prompts across 11 sections, plus a Toolbox that teaches you the formula and keeps your facts straight.", 'lead'))
    rows = []
    for sec in SECTIONS:
        first = sec['prompts'][0][0].split('.')[0]
        last = sec['prompts'][-1][0].split('.')[0]
        rows.append([sec['title'], f"{len(sec['prompts'])} prompts", f"Prompts {first}-{last}"])
    rows.append(["The Toolbox: formula, India rules cheat-sheet, property brief, phrases to avoid, 30-day plan, FAQs", "6 tools", "After Section 11"])
    story.append(data_table(["Section", "Size", "Prompts"], rows, [250, 75, 110]))
    story.append(Spacer(1, 14))
    story.append(callout("Start with the section you need today",
        "You do not have to read this front to back. If a listing is due this morning, go to Section 1. If a lead has gone cold, go to Section 2. If you are about to spend money on ads, go to Section 9. The Toolbox at the back is worth reading once, properly.",
        bg=colors.HexColor("#fff8e6"), bar=GOLD))
    story.append(PageBreak())

    # --- Sections ---
    for sec in SECTIONS:
        story.append(section_banner(sec['num'], sec['title'], sec['sub']))
        story.append(Spacer(1, 10))
        story.append(P(sec['intro'], 'body'))
        story.append(Spacer(1, 4))
        for name, text in sec['prompts']:
            story.append(prompt_box(name, text))
        story.append(Spacer(1, 8))
        story.append(GoldRule(PAGE_W-2*MARGIN, 1, LINEC))
        story.append(Spacer(1, 10))

    # --- Toolbox divider ---
    story.append(PageBreak())
    story.append(Paragraph("THE TOOLBOX", ParagraphStyle('tb', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=GOLD_D, spaceAfter=2)))
    story.append(Paragraph("Everything you need to use the prompts well", S['h1']))
    story.append(GoldRule(60))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. The 5-part prompt formula", ParagraphStyle('x', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=NAVY, spaceBefore=2, spaceAfter=5)))
    story.append(P("Every strong prompt in this pack is built from the same five parts. Learn the shape once and you can write your own for any situation.", 'body'))
    story.append(data_table(
        ["Part", "What it does", "Example"],
        [["Role", "Tells the AI who to be", "'You are a real estate copywriter for India.'"],
         ["Context", "Gives the real facts", "'3BHK, Whitefield, 1450 sq ft, ready to move.'"],
         ["Constraints", "Sets the rules and the tone", "'150 words, no hype words, honest.'"],
         ["Format", "Says what the output looks like", "'One hook, facts, 4 bullets, CTA.'"],
         ["Example", "Shows the AI a model to copy", "'Here is a listing I like: …'"]],
        [70, 165, 200]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("2. India rules & numbers you must never get wrong", ParagraphStyle('x', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=NAVY, spaceBefore=2, spaceAfter=5)))
    story.append(P("Buyers and sellers ask about these constantly. Keep them right, and always confirm the current position on the official portal or with a CA before you advise a client.", 'body'))
    story.append(data_table(
        ["Topic", "What to know (verify current position)"],
        [["RERA registration",
          "Under Section 9 of the RERA Act, 2016, an agent must be registered with the state RERA authority before facilitating sale/purchase in a registered project. Registration is state-wise, commonly valid 5 years, renewable. Quote your registration number in every sale you facilitate."],
         ["RERA penalties",
          "Operating without registration: penalty of ₹10,000 per day of default, up to 5% of the property cost (Section 62). Contravening RERA orders can extend to the same ceiling; breaching Tribunal orders can mean up to 1 year imprisonment, a fine up to 10% of the property cost, or both (Section 66)."],
         ["TDS on purchase",
          "The buyer deducts TDS at 1% where the consideration OR the stamp duty value is ₹50 lakh or more (Section 194-IA; from 1 April 2026, Section 393(1) of the Income-tax Act, 2025). Form 26QB (now renumbered Form 141) within 30 days. For an NRI seller there is NO ₹50 lakh threshold — tax is withheld at non-resident rates."],
         ["GST on property",
          "Under-construction residential: 5% (1% for affordable housing up to ₹45 lakh and 60 sqm carpet in metros / 90 sqm elsewhere), without input tax credit. Ready-to-move with OC/CC: no GST. Under-construction commercial: 12%. Land/plots: no GST. These rates were not changed by the GST 2.0 reform of 22 September 2025."],
         ["Stamp duty & registration",
          "A state tax on the sale deed, roughly 4-8%, charged on the higher of the agreement value or the state's circle / ready-reckoner / guidance value. Registration is usually about 1%, often capped. All-in, budget 5-11% over the price. Several states give a 1-2% concession for a woman buyer. Rates change — verify on your state's registration portal."],
         ["False representation",
          "RERA bars unfair trade practices, including false or misleading statements about a property, its approvals or your services. Never claim a buyer you do not have, an approval the property lacks, or a return you cannot support."]],
        [95, 340]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("3. Fill-in property brief (keep one per listing)", ParagraphStyle('x', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=NAVY, spaceBefore=2, spaceAfter=5)))
    story.append(P("Fill this once, then paste it into any prompt. Complete briefs produce far better listings and ads than half-remembered facts.", 'body'))
    story.append(data_table(
        ["Field", "Your details"],
        [["Property type & configuration", ""],
         ["Locality / society / city", ""],
         ["Carpet area (sq ft) and floor", ""],
         ["Facing, age, possession status", ""],
         ["Parking, amenities, water/power", ""],
         ["Price / rent and deposit", ""],
         ["RERA registration no. (if applicable)", ""],
         ["Approvals (OC/CC, DTCP, khata/patta)", ""],
         ["Target buyer and one main benefit", ""],
         ["One honest limitation to mention", ""]],
        [200, 235]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("4. The 10 phrases to strike from your listings", ParagraphStyle('x', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=NAVY, spaceBefore=2, spaceAfter=5)))
    story.append(P("These are the cliches and risky claims that make a listing look fake — or breach RERA's rules against misleading representation. Delete them and replace with a fact.", 'body'))
    story += bullets([
        "<b>\"Dream home\"</b> — say what the home actually offers.",
        "<b>\"Stunning / magnificent / opulent\"</b> — describe the view, the light, the layout instead.",
        "<b>\"Best investment / guaranteed returns\"</b> — you cannot promise appreciation. Remove it.",
        "<b>\"RERA approved\"</b> when the project is not actually registered — verify and quote the number.",
        "<b>\"Fully approved\"</b> with no mention of which approval — name the OC/CC or layout approval.",
        "<b>\"Prime location\"</b> — give the distance to the metro, school or tech park.",
        "<b>\"Hurry, last unit\"</b> unless it is genuinely true.",
        "<b>\"Peaceful / vastu-compliant\"</b> as a bare claim — state the facing or the layout fact.",
        "<b>\"No brokerage\"</b> if you are the broker — be honest about your fee.",
        "<b>\"Semi-furnished\"</b> without listing what is included — list the items.",
    ])
    story.append(Spacer(1, 12))

    story.append(Paragraph("5. Your 30-day AI action plan", ParagraphStyle('x', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=NAVY, spaceBefore=2, spaceAfter=5)))
    story.append(data_table(
        ["Week", "Focus", "What to do"],
        [["Week 1", "Listings",
          "Rewrite your 3 current listings with Prompts 1-6. Fill one property brief per listing. Post each on 99acres, MagicBricks and Housing.com."],
         ["Week 2", "WhatsApp",
          "Set up the instant first-reply (Prompt 9) and the 7-touch follow-up (Prompt 12). Clear every unanswered lead older than 3 days using Prompt 14."],
         ["Week 3", "Content & ads",
          "Post 3 Reels (Prompts 17, 21) and run one small click-to-WhatsApp ad with Prompt 47. Set up the A/B test from Prompt 50."],
         ["Week 4", "Systems & sellers",
          "Build your document checklist (Prompt 51), start the weekly pipeline review (Prompt 54), and send 20 seller outreach messages (Prompt 29)."]],
        [55, 80, 300]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("6. Frequently asked questions", ParagraphStyle('x', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=NAVY, spaceBefore=2, spaceAfter=5)))
    faqs = [
        ("Which AI tool should I use?", "ChatGPT, Gemini, Claude or any good assistant will run these prompts. Use whichever you already have. For long listings and negotiation scripts, assistants that handle long text well tend to give the most natural results."),
        ("Will the output sound like AI wrote it?", "Not if you paste real facts and edit the draft in your own words before sending. The prompts are written to sound like a person; your final read-through is what removes any remaining stiffness."),
        ("Can I use these for rentals and commercial too?", "Yes. Sections 1, 2, 6 and 9 work for residential, rental and commercial with a small change of facts. The formula is the same."),
        ("Do I need to know prompt engineering?", "No. Copy the prompt, replace the [brackets] with your details, and send. The 5-part formula in the Toolbox shows you how to adapt them yourself once you are comfortable."),
        ("Is the legal and tax information in this pack current?", "It reflects the position verified in October 2026. Rules and rates change, and they vary by state. Always confirm on the official portal or with a CA before you advise a client — this pack is a drafting tool, not legal or tax advice."),
    ]
    for q, a in faqs:
        story.append(Paragraph(q, ParagraphStyle('q', fontName='Helvetica-Bold', fontSize=10.2, leading=14, textColor=NAVY, spaceBefore=5, spaceAfter=2)))
        story.append(Paragraph(a, S['body']))

    story.append(Spacer(1, 14))
    story.append(callout("You now have the toolkit — the next step is one prompt",
        "Open your AI assistant, pick the prompt for the job in front of you, and fill in the brackets. Do that once today and you will not go back to a blank page again. For more India-first AI tools and guides, visit digitalkartai.shop.",
        bg=NAVY, bar=GOLD))
    story.append(Spacer(1, 8))
    story.append(Paragraph("© 2026 Digitalaikart · digitalkartai.shop · This pack is a drafting tool, not legal or tax advice.",
                           ParagraphStyle('f', fontName='Helvetica', fontSize=8.5, leading=12, textColor=GREY, alignment=TA_CENTER)))

    doc.build(story)
    print("BUILT", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    build()
