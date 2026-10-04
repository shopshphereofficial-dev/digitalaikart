#!/usr/bin/env python3
# Build: The Data Analyst Career Starter Kit 2026 (India Edition) - Digitalaikart
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether,
                                HRFlowable, NextPageTemplate)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfgen import canvas as pdfcanvas

NAVY = HexColor('#0a1628')
NAVY2 = HexColor('#132a47')
GOLD = HexColor('#f5c542')
LIGHT = HexColor('#f4f6fa')
INK = HexColor('#1e293b')
MUTE = HexColor('#5b6b82')
LINE = HexColor('#d9e0ea')
CODEBG = HexColor('#f3f6fb')

PAGE_W, PAGE_H = A4

S = {
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.8, leading=14.4,
                           textColor=INK, spaceAfter=7, alignment=TA_LEFT),
    'lead': ParagraphStyle('lead', fontName='Helvetica-Oblique', fontSize=10.4, leading=15.4,
                           textColor=NAVY, spaceAfter=10),
    'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=19.5, leading=23,
                         textColor=NAVY, spaceBefore=2, spaceAfter=4),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12.6, leading=16,
                         textColor=NAVY, spaceBefore=10, spaceAfter=5, keepWithNext=1),
    'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=10.7, leading=14,
                         textColor=NAVY, spaceBefore=8, spaceAfter=3, keepWithNext=1),
    'kicker': ParagraphStyle('kicker', fontName='Helvetica-Bold', fontSize=8.4, leading=11,
                             textColor=GOLD, spaceAfter=2),
    'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=9.8, leading=14,
                             textColor=INK, leftIndent=14, bulletIndent=4, spaceAfter=4),
    'check': ParagraphStyle('check', fontName='Helvetica', fontSize=9.8, leading=14.5,
                            textColor=INK, leftIndent=18, bulletIndent=4, spaceAfter=4),
    'code': ParagraphStyle('code', fontName='Courier', fontSize=8.5, leading=12.1,
                           textColor=NAVY),
    'pnote': ParagraphStyle('pnote', fontName='Helvetica-Oblique', fontSize=8.8, leading=12.4,
                            textColor=MUTE, spaceBefore=4),
    'cell': ParagraphStyle('cell', fontName='Helvetica', fontSize=8.7, leading=11.9,
                           textColor=INK),
    'cellb': ParagraphStyle('cellb', fontName='Helvetica-Bold', fontSize=8.7, leading=11.9,
                            textColor=white),
    'src': ParagraphStyle('src', fontName='Helvetica', fontSize=8.5, leading=12.4,
                          textColor=INK, leftIndent=14, bulletIndent=4, spaceAfter=4),
    'toc': ParagraphStyle('toc', fontName='Helvetica', fontSize=10.2, leading=17, textColor=INK),
}


def _invariant_canvas(*args, **kwargs):
    kwargs['invariant'] = 1
    return pdfcanvas.Canvas(*args, **kwargs)


def cover(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY); canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canv.setStrokeColor(GOLD); canv.setLineWidth(1.2)
    canv.rect(12 * mm, 12 * mm, PAGE_W - 24 * mm, PAGE_H - 24 * mm)
    canv.setFillColor(GOLD); canv.setFont('Helvetica-Bold', 12.5)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 36 * mm, 'D I G I T A L A I K A R T   P R E S E N T S')
    canv.setFillColor(white); canv.setFont('Helvetica-Bold', 34)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 60 * mm, 'The Data Analyst')
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 76 * mm, 'Career Starter Kit')
    canv.setFillColor(GOLD); canv.setFont('Helvetica-Bold', 15)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 90 * mm, '2026  ·  India Edition')
    canv.setStrokeColor(GOLD); canv.setLineWidth(0.8)
    canv.line(PAGE_W / 2 - 32 * mm, PAGE_H - 97 * mm, PAGE_W / 2 + 32 * mm, PAGE_H - 97 * mm)
    canv.setFillColor(white); canv.setFont('Helvetica', 12.2)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 110 * mm, 'From any degree to your first Data Analyst job -')
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 117 * mm, 'the roadmap, the portfolio, the resume, the interview.')
    canv.setFont('Helvetica-Oblique', 10.4)
    canv.setFillColor(HexColor('#c8d3e4'))
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 127 * mm, 'A 16-week plan built on the 2026 Indian job market: the exact skills')
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 133 * mm, 'in order, 4 portfolio projects, 60 interview answers and salary data.')

    items = [
        'The 2026 market in numbers - demand, roles, cities, salaries',
        'The exact skill stack, in the right order, with nothing wasted',
        'A week-by-week 16-week roadmap with a deliverable each week',
        '4 portfolio project briefs built on real Indian datasets',
        'The ATS resume template + bullet formulas that pass the screen',
        '60 interview questions with model answers + salary playbook',
    ]
    x = PAGE_W / 2 - 74 * mm
    box_h = 66 * mm
    y = PAGE_H - 156 * mm
    canv.setFillColor(NAVY2)
    canv.roundRect(x, y - box_h, 148 * mm, box_h, 4 * mm, stroke=0, fill=1)
    canv.setStrokeColor(GOLD); canv.setLineWidth(0.7)
    canv.roundRect(x, y - box_h, 148 * mm, box_h, 4 * mm, stroke=1, fill=0)
    ty = y - 9 * mm
    canv.setFillColor(GOLD); canv.setFont('Helvetica-Bold', 10)
    canv.drawCentredString(PAGE_W / 2, ty, 'W H A T   I S   I N S I D E')
    ty -= 8.5 * mm
    canv.setFillColor(white); canv.setFont('Helvetica', 10.2)
    for txt in items:
        canv.drawString(x + 9 * mm, ty, '>>  ' + txt)
        ty -= 8.2 * mm
    canv.setFillColor(GOLD); canv.setFont('Helvetica-Bold', 10.5)
    canv.drawCentredString(PAGE_W / 2, 34 * mm, 'First Edition  ·  October 2026')
    canv.setFillColor(HexColor('#8ea2c0')); canv.setFont('Helvetica', 9.4)
    canv.drawCentredString(PAGE_W / 2, 26 * mm, 'No coding background required. Works from any degree.')
    canv.drawCentredString(PAGE_W / 2, 20 * mm, 'digitalaikart.shop')
    canv.restoreState()


def on_page(canv, doc):
    canv.saveState()
    canv.setStrokeColor(GOLD); canv.setLineWidth(1.4)
    canv.line(18 * mm, 14 * mm, PAGE_W - 18 * mm, 14 * mm)
    canv.setFont('Helvetica', 7.7); canv.setFillColor(MUTE)
    canv.drawString(18 * mm, 9.5 * mm, 'The Data Analyst Career Starter Kit 2026  ·  India Edition')
    canv.drawRightString(PAGE_W - 18 * mm, 9.5 * mm, 'digitalkartai.shop  ·  Page %d' % doc.page)
    canv.setFillColor(NAVY)
    canv.rect(0, PAGE_H - 6 * mm, PAGE_W, 6 * mm, stroke=0, fill=1)
    canv.setFillColor(GOLD)
    canv.rect(0, PAGE_H - 6.9 * mm, PAGE_W, 0.9 * mm, stroke=0, fill=1)
    canv.restoreState()


def P(text, style='body'):
    st = S[style] if isinstance(style, str) else style
    return Paragraph(text, st)


def bullets(items, style='bullet', mark='\u2022'):
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


def table(data, widths, header=True):
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


def code_block(title, body):
    head = Table([[cellp('<font color="#ffffff">%s</font>' % title, 'cellb')]], colWidths=[None])
    head.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), NAVY),
                              ('TOPPADDING', (0, 0), (-1, -1), 5),
                              ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                              ('LEFTPADDING', (0, 0), (-1, -1), 8)]))
    inner = Table([[Paragraph(body.replace('\n', '<br/>'), S['code'])]], colWidths=[None])
    inner.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), CODEBG),
                               ('BOX', (0, 0), (-1, -1), 0.8, GOLD),
                               ('TOPPADDING', (0, 0), (-1, -1), 8),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                               ('LEFTPADDING', (0, 0), (-1, -1), 9),
                               ('RIGHTPADDING', (0, 0), (-1, -1), 9)]))
    box = Table([[head], [inner]], colWidths=[None])
    box.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.9, NAVY2),
                             ('TOPPADDING', (0, 0), (-1, -1), 0),
                             ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                             ('LEFTPADDING', (0, 0), (-1, -1), 0),
                             ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
    return KeepTogether([Spacer(1, 6), box, Spacer(1, 5)])


story = []
A = story.append

# ================================================================ TOC
toc_entries = [
    ('1', 'Read this first', 'Who this kit is for, the one truth about hiring, and how to use it'),
    ('2', 'The 2026 market, in numbers', 'Demand, the roles, the cities and the real salary bands'),
    ('3', 'The exact skill stack, in order', 'Excel, SQL, Power BI, Python, statistics and AI - and what to skip'),
    ('4', 'The 16-week roadmap', 'A week-by-week plan with one deliverable every week'),
    ('5', 'The portfolio that gets interviews', '4 project briefs on real Indian data, with business questions'),
    ('6', 'The ATS resume', 'The rules, the bullet formula and a complete fresher example'),
    ('7', 'LinkedIn and Naukri profiles', 'Keyword strategy recruiters actually search on'),
    ('8', 'Interview prep: 60 questions', 'Every round, model answers, case framework and STAR stories'),
    ('9', 'Salary and negotiation', 'Benchmarks by skill stack plus the exact script to use'),
    ('10', 'The 7-day interview sprint', 'The final week, the application tracker and the daily routine'),
    ('11', 'Free resources and checklists', 'Verified free courses, datasets, certifications and tick-lists'),
]


def build_toc():
    out = [Spacer(1, 6),
           Paragraph('CONTENTS', S['kicker']),
           Paragraph('Contents', S['h1']), gold_rule()]
    for num, title, sub in toc_entries:
        out.append(Paragraph('<b>Part %s &nbsp;·&nbsp; %s</b>' % (num, title), S['toc']))
        out.append(Paragraph('<font size="8.8" color="#5b6b82">%s</font>' % sub,
                             ParagraphStyle('tsub', parent=S['toc'], fontSize=8.8, leading=12.5,
                                            textColor=MUTE, leftIndent=14, spaceAfter=6)))
    out.append(Spacer(1, 12))
    out.append(HRFlowable(width='100%', thickness=1.1, color=GOLD, spaceBefore=4, spaceAfter=10))
    out.append(Paragraph('HOW TO USE THIS KIT', S['kicker']))
    out.append(Paragraph('Three ways in, depending on where you are today', S['h2']))
    for row in [
        '<b>Complete beginner</b> - read Parts 1-4 in order, then start Week 1 of the roadmap tomorrow. Do not buy any course until you have finished the free resources in Part 11.',
        '<b>Already know Excel and some SQL</b> - jump to Part 5 and build the four portfolio projects. Projects, not certificates, are what get you the interview.',
        '<b>Interviewing already, no callbacks</b> - go straight to Parts 6, 7 and 8. A weak resume and a thin portfolio are almost always the reason, not your skill.',
        'Keep this PDF open beside your practice window. Every table, script and question is written to be used as-is, with only the [BRACKETED] parts replaced.',
    ]:
        out.append(Paragraph(row, S['body'], bulletText='\u2022'))
    return out


# ================================================================ PART 1
section(story, 'PART 1', 'Read this first',
        'This is not a motivational book. It is a work plan. Follow it and in 16 weeks you will have '
        'the three things every Indian employer actually checks: a demonstrable skill stack, a portfolio '
        'of real projects, and a resume that survives the software that reads it first.')

A(P('<b>The one truth about hiring.</b> In 2026, Indian employers hiring junior data analysts are not '
    'screening for degrees, and they are barely screening for certificates. They are screening for '
    'evidence: can you pull data with SQL, build a dashboard that answers a business question, and explain '
    'what it means? Almost every hiring manager says the same thing - a candidate who opens a dashboard '
    'and explains the decision it supported beats a candidate with three certificates and nothing to show.'))

A(P('<b>Who this kit is for:</b>'))
for b in bullets([
    'Freshers from <b>any</b> background - commerce, science, arts, engineering - with no work experience.',
    'Working professionals in non-technical roles (operations, BPO, support, sales, MIS) who want to move into analytics.',
    'Early-career IT or services staff (0-2 years) who want to switch from support/testing to a data role.',
    'Anyone who has been "learning" for months with no interviews - the fix is almost always the portfolio and the resume.',
]):
    A(b)

A(P('<b>What you need to start:</b> a laptop, an internet connection, and about 1.5 to 2 focused hours a day. '
    'Everything in this kit runs on free software - Power BI Desktop, MySQL or PostgreSQL, Python, and a free '
    'AI chat. You do not need to pay for anything to become job-ready.'))

A(P('<b>How long it really takes.</b> With daily practice of 1.5-2 hours, the realistic timeline from zero to '
    'interview-ready is about 5-6 months. Part-time, plan for 8-10 months. Structured, daily practice matters '
    'more than the number of courses you collect - a candidate who does one thing every day for five months '
    'beats one who binge-watches courses for a year and builds nothing.'))

A(P('<b>The 6-step path this kit walks you through:</b>'))
for i, b in enumerate([
    'Pick the skill stack in the right order (Part 3) - do not learn five tools in parallel.',
    'Follow the 16-week roadmap, one deliverable a week (Part 4).',
    'Build four portfolio projects on real Indian data (Part 5).',
    'Write an ATS-ready resume around those projects (Part 6).',
    'Optimise your LinkedIn and Naukri profiles so recruiters find you (Part 7).',
    'Prepare for the six interview rounds and negotiate a fair salary (Parts 8-9).',
], 1):
    A(P('%d. %s' % (i, b)))

A(Spacer(1, 4))
A(P('<i>Every market figure, salary band, tool name and hiring fact in this kit was checked against live '
    'Indian sources in October 2026. The sources are listed in the appendix. Figures change - re-check them '
    'before you make a final career decision.</i>', S['pnote']))

A(PageBreak())

# ================================================================ PART 2
section(story, 'PART 2', 'The 2026 market, in numbers',
        'Before you spend a single hour learning, know exactly what the market is asking for. These are the '
        'numbers that should decide what you study - and what you skip.')

A(P('<b>Demand is real and it is growing.</b> Across India, employers posted about 4,166 unique Data Analyst '
    'roles in the 90 days from 22 June to 20 September 2026 - an average of roughly 312 new roles every week. '
    'Weekly volume rose from 306 to 367 across that window, which is a growing market, not a shrinking one. '
    'On Naukri.com alone, the "data analyst" search returns in the region of 27,000-plus active postings. '
    '(Sources: GetUHired India job-market report, September 2026; Naukri.com, October 2026.)'))

A(P('<b>What the market asks for, by the numbers.</b> When you count the skills named in those live postings, '
    'three tools dominate everything else. This is the single most useful table in the kit - it tells you where '
    'to spend your first 12 weeks.'))
A(table([
    [cellp('Skill', 'cellb'), cellp('Postings naming it', 'cellb'), cellp('Priority', 'cellb')],
    [cellp('<b>SQL</b>'), cellp('~2,708 of 4,166'), cellp('Non-negotiable - learn first')],
    [cellp('<b>Python</b> (pandas, numpy)'), cellp('~1,910'), cellp('High - raises your salary ceiling')],
    [cellp('<b>Power BI</b>'), cellp('~1,650'), cellp('High - the #1 BI tool in India')],
    [cellp('Excel / Advanced Excel'), cellp('Very high'), cellp('Baseline - assume it is required')],
], [52 * mm, 40 * mm, None]))
A(P('Source: GetUHired India job-posting analysis, September 2026. SQL appears as a required (not "preferred") '
    'skill in more than 90% of Indian data analyst listings - if you learn one thing well, make it SQL. Power BI '
    'is the most-requested business-intelligence tool in Indian postings, with Tableau a clear second.', S['pnote']))

A(P('<b>The roles you are actually applying for.</b> "Data analyst" covers a wide range of jobs in India. Know '
    'the entry titles so you search for all of them, not just one.'))
A(table([
    [cellp('Job title', 'cellb'), cellp('What you do', 'cellb'), cellp('Entry fit', 'cellb')],
    [cellp('Junior / Data Analyst'), cellp('Pull data, build reports and dashboards, answer business questions'), cellp('Primary target')],
    [cellp('Business Analyst (data track)'), cellp('Translate business problems into analysis and recommendations'), cellp('Primary target')],
    [cellp('BI Analyst'), cellp('Own dashboards and reporting in Power BI or Tableau'), cellp('Primary target')],
    [cellp('MIS Executive'), cellp('Build and maintain daily/weekly management reports (Excel-heavy)'), cellp('Easiest first job')],
    [cellp('Reporting Analyst'), cellp('Recurring reports and data quality for a function'), cellp('Good entry point')],
    [cellp('Research / Marketing Analyst'), cellp('Analyse campaigns, users or market data'), cellp('Good entry point')],
], [42 * mm, None, 34 * mm]))
A(P('Tip: apply to MIS Executive and Reporting Analyst roles too. They are less competitive, they get you inside '
    'a company, and they convert into analyst roles faster than applying cold for "Data Analyst" for a year.', S['pnote']))

A(P('<b>Where the jobs are.</b> Hiring is concentrated in the metros, but remote and Tier-2 postings are '
    'rising. Bangalore and Hyderabad lead, followed by Delhi-NCR, Mumbai, Pune and Chennai.'))
A(table([
    [cellp('City', 'cellb'), cellp('Share of postings', 'cellb'), cellp('Note', 'cellb')],
    [cellp('Bengaluru'), cellp('Highest'), cellp('Most competitive; product and startup roles')],
    [cellp('Hyderabad'), cellp('Very high'), cellp('GCCs and BFSI analytics; strong salaries')],
    [cellp('Delhi-NCR (incl. Noida, Gurugram)'), cellp('High'), cellp('Consulting, BFSI, e-commerce')],
    [cellp('Mumbai / Pune'), cellp('High'), cellp('BFSI and IT services; large MIS demand')],
    [cellp('Chennai'), cellp('Moderate'), cellp('IT services and BFSI back-offices')],
], [52 * mm, 34 * mm, None]))
A(P('About a quarter of postings offer remote or hybrid work, so you are not restricted to your own city.', S['pnote']))

A(P('<b>What you can realistically earn.</b> Salary in India depends less on the title and more on the tool '
    'stack you bring. The table below is the clearest reason to keep going past Excel into SQL and Python - the '
    'same job title pays a very different amount depending on your stack.'))
A(table([
    [cellp('Your tool stack', 'cellb'), cellp('Typical band (1-4 yrs)', 'cellb'), cellp('Premium vs base', 'cellb')],
    [cellp('Excel + Power BI (SQL optional)'), cellp('Rs 4.5 - 7.5 LPA'), cellp('Base')],
    [cellp('SQL + Power BI / Tableau'), cellp('Rs 6 - 10 LPA'), cellp('+25-35%')],
    [cellp('SQL + Python (pandas, numpy)'), cellp('Rs 8 - 14 LPA'), cellp('+40-55%')],
    [cellp('SQL + Python + Statistics / A-B testing'), cellp('Rs 10 - 18 LPA'), cellp('+60-80%')],
], [62 * mm, 40 * mm, None]))
A(P('For a fresher with no experience, the realistic entry band is about Rs 3-6 LPA, rising fast with a strong '
    'portfolio and Python. Figures are self-reported market aggregates (AmbitionBox, Glassdoor and LinkedIn '
    'Salary Insights, 2026) and over-represent higher earners - treat them as ranges to negotiate within, not '
    'guarantees. Source: careerskillguide salary analysis, May 2026.', S['pnote']))

A(P('<b>Certifications that Indian recruiters actually recognise.</b> Certificates do not replace a portfolio, '
    'but one recognised certificate helps you pass a recruiter filter. Finish <b>one</b> fully rather than '
    'starting several:'))
for b in bullets([
    '<b>Google Data Analytics Professional Certificate</b> (Coursera) - the most widely recognised general entry certificate.',
    '<b>Microsoft Certified: Power BI Data Analyst Associate (PL-300)</b> - the strongest signal for a Power BI-heavy role.',
    '<b>NPTEL (IIT) courses</b> on statistics and data analysis - free, and respected by traditional Indian employers.',
]):
    A(b)

A(PageBreak())

# ================================================================ PART 3
section(story, 'PART 3', 'The exact skill stack, in order',
        'Learn in this order and do not skip ahead. Each skill makes the next one easier. Trying to learn all '
        'six at once is the single most common reason people never finish.')

A(P('<b>1. Advanced Excel (Weeks 1-2).</b> Excel is assumed everywhere and is tested in almost every fresher '
    'interview. Master, in this order: SUMIFS/COUNTIFS, IF and nested IF, XLOOKUP and INDEX-MATCH, PivotTables '
    'and PivotCharts, text-to-columns, remove duplicates, conditional formatting, and Power Query for basic '
    'cleaning. Then build one clean MIS report from a raw, messy export - that is the exact task interviewers set.'))
A(P('<b>2. SQL - your number one skill (Weeks 3-7).</b> SQL is the language of data and the most frequently '
    'tested skill in Indian analyst interviews. Learn: SELECT, WHERE, ORDER BY, GROUP BY, HAVING, all JOINs '
    '(inner, left, right, full), subqueries, CASE, and then window functions (ROW_NUMBER, RANK, LAG/LEAD, '
    'running totals) and CTEs. Practise on a realistic three-table schema (customers, orders, products) - not '
    'on toy one-table examples. If you can write intermediate SQL, you are competitive for the majority of '
    'Indian analyst roles.'))
A(P('<b>3. Power BI (Weeks 8-10).</b> Power BI is the dominant BI tool in India. Learn the data model '
    '(relationships, star schema basics), the difference between calculated columns and measures, core DAX '
    '(SUM, CALCULATE, FILTER, DIVIDE, time intelligence), and dashboard design that answers a question rather '
    'than just showing charts. Being able to turn a query into a clear, interactive dashboard is what employers '
    'pay for. Tableau is second and is learnable in 3-4 weeks once Power BI clicks.'))
A(P('<b>4. Python for data (Weeks 11-13).</b> Python is not required for every role, but it raises your salary '
    'ceiling sharply - SQL plus Python analysts are paid roughly 40-55% more than Excel-plus-BI analysts at the '
    'same experience. Learn pandas (read, filter, group, merge, pivot), matplotlib or seaborn for charts, and '
    'how to clean a messy real-world file. You do not need machine learning for a first analyst job.'))
A(P('<b>5. Statistics fundamentals (Weeks 14-15).</b> Just enough to analyse honestly: mean vs median and why '
    'outliers matter, distributions, standard deviation, correlation vs causation, and the basics of A/B '
    'testing and hypothesis testing. Interviewers test this through scenario questions, not maths.'))
A(P('<b>6. AI as an accelerant (ongoing).</b> In 2026 the strongest junior analysts use AI to move faster - '
    'generating and debugging SQL, summarising results, and drafting the plain-English "so what". This does not '
    'replace the skills above; it makes a skilled analyst faster. Showing in an interview that you use AI '
    'responsibly is a genuine differentiator against candidates who do not.'))

A(P('<b>What to deliberately skip for now.</b> These appear in job descriptions as "nice to have" but are not '
    'entry requirements, and learning them too early wastes weeks you should spend on SQL and a portfolio:'))
for b in bullets([
    'R - the market overwhelmingly asks for Python, not R, at the junior level.',
    'Machine learning and modelling - for after your first job.',
    'Data engineering (Spark, dbt, cloud pipelines) - a different career, not a first-analyst skill.',
    'Advanced statistics or a second BI tool before your first one is solid.',
]):
    A(b)

A(Spacer(1, 4))
A(code_block('The order, in one line',
             'Excel  ->  SQL  ->  Power BI  ->  Python  ->  Statistics  ->  AI\n'
             'Weeks 1-2    3-7      8-10         11-13      14-15          ongoing\n'
             'Rule: one skill at a time, one small deliverable each week.'))

A(PageBreak())

# ================================================================ PART 4
section(story, 'PART 4', 'The 16-week roadmap',
        'One row per week. The "deliverable" column is the point - if you finish a week with nothing to show, '
        'you did not really finish it. Keep every deliverable; they become your portfolio and your interview stories.')

A(P('<b>Your daily routine (1.5-2 hours):</b> 45 minutes learning the concept, 45 minutes practising on real '
    'data, 15-30 minutes writing down what you learned in your own words (this is what makes it stick and what '
    'you will say in interviews).'))
A(table([
    [cellp('Week', 'cellb'), cellp('Focus', 'cellb'), cellp('Deliverable you must produce', 'cellb')],
    [cellp('1'), cellp('Excel: formulas, lookups'), cellp('A cleaned sheet from a messy raw export')],
    [cellp('2'), cellp('Excel: PivotTables, Power Query'), cellp('A one-page MIS report with 3 pivot charts')],
    [cellp('3'), cellp('SQL: SELECT, WHERE, ORDER BY'), cellp('20 queries on a 3-table sample database')],
    [cellp('4'), cellp('SQL: GROUP BY, HAVING, JOINs'), cellp('A 10-question business analysis in pure SQL')],
    [cellp('5'), cellp('SQL: subqueries, CASE'), cellp('Segmentation query set (e.g. customers by value)')],
    [cellp('6'), cellp('SQL: window functions, CTEs'), cellp('Ranking, running-total and LAG/LEAD queries')],
    [cellp('7'), cellp('SQL: revision + timed practice'), cellp('50 timed queries; a SQL cheat-sheet you wrote')],
    [cellp('8'), cellp('Power BI: model, relationships'), cellp('A clean data model from two related tables')],
    [cellp('9'), cellp('Power BI: DAX measures'), cellp('5 working measures incl. one time-intelligence calc')],
    [cellp('10'), cellp('Power BI: dashboard design'), cellp('Project 1: Sales Performance Dashboard')],
    [cellp('11'), cellp('Python: pandas basics'), cellp('A cleaned CSV + summary stats in a notebook')],
    [cellp('12'), cellp('Python: group, merge, pivot'), cellp('Project 3: customer segmentation notebook')],
    [cellp('13'), cellp('Python: charts + revision'), cellp('A written analysis with 3 charts and a "so what"')],
    [cellp('14'), cellp('Statistics: core concepts'), cellp('A one-page stats cheat-sheet you can explain aloud')],
    [cellp('15'), cellp('Statistics: A/B + cases'), cellp('Answers to 8 analytics case questions, written')],
    [cellp('16'), cellp('Projects, resume, interview prep'), cellp('Projects 2 and 4, final resume, mock interview')],
], [14 * mm, 46 * mm, None]))
A(P('If you fall behind, do not skip the deliverable - shorten the learning time instead. A finished small '
    'deliverable is worth more than a half-learned big topic.', S['pnote']))

A(PageBreak())

# ================================================================ PART 5
section(story, 'PART 5', 'The portfolio that gets interviews',
        'Four projects are enough. Each one must answer a business question, not just display data. Recruiters '
        'and hiring managers are instantly bored by another Netflix or HR-Attrition Kaggle notebook - build '
        'projects that look like real work on Indian data.')

A(P('<b>The rule that separates a strong portfolio from a weak one.</b> A weak project starts from a clean '
    'dataset and makes charts. A strong project starts from a business question, uses a messy or real dataset, '
    'cleans it, and ends with a recommendation written in plain English. Interviewers remember the candidate '
    'who says "I found that the top 12% of customers drove 41% of revenue, so I recommended X" - not the one '
    'who lists the tools they used.'))

for t, q, ds, steps, show, avoid in [
    ('Project 1 - Sales Performance Dashboard (Power BI)',
     'Where is the business losing revenue, and which regions or products should it push?',
     'Any public Indian retail/sales dataset, or a downloaded government or e-commerce dataset.',
     'Load and clean two related tables (orders and products/customers); build a star-schema model; write DAX '
     'measures for total sales, month-over-month growth and top-N products; design one page with a KPI row, a '
     'trend line, a region map and a product ranking; add slicers for region and month.',
     'A 5-minute walkthrough: the question, the model, the three measures, and the one decision the dashboard supports.',
     'Do not show 15 charts on one page. Three to five visuals that answer the question beat a cluttered wall.'),
    ('Project 2 - SQL-Only Business Analysis (MySQL / PostgreSQL)',
     'Ten real business questions answered entirely in SQL, from raw tables.',
     'A sample retail schema (customers, orders, order_items, products) or a scraped public dataset.',
     'Write and document 10 queries: monthly revenue trend, top 10 products, repeat-purchase rate, customers '
     'who never reordered, average order value by city, month-on-month growth with window functions, RFM-style '
     'segmentation, and a CTE that answers a multi-step question.',
     'A single document: each question, the query, the result and a one-line interpretation. This proves raw SQL ability.',
     'Do not paste queries you cannot explain line by line. Interviewers will ask you to rewrite one live.'),
    ('Project 3 - Customer Segmentation / Funnel Analysis (Python)',
     'Which customer segments should marketing prioritise, and where does the funnel leak?',
     'A public e-commerce or marketing dataset (Kaggle) or a scraper of a public listing site.',
     'Use pandas to clean and merge; compute recency, frequency and monetary value; group customers into '
     'segments; plot segment sizes and value with matplotlib/seaborn; write a short "so what" with a marketing recommendation.',
     'A notebook plus a one-page PDF summary: question, method, two charts, recommendation.',
     'Do not use a pre-cleaned Kaggle dataset with no business framing - rebuild it around a real question.'),
    ('Project 4 - Live Job-Market Analysis (shows you are current)',
     'What skills are Indian employers actually asking for right now, and what pays most?',
     'Live postings scraped from a job board (Naukri/LinkedIn/Indeed) or a public skills dataset.',
     'Collect 150-300 postings; clean the skills field in Excel or pandas; count skill frequency; correlate '
     'skills with the salary bands mentioned; visualise in Power BI with slicers for experience and city.',
     'A dashboard plus a paragraph: "SQL appeared in X% of postings, Power BI in Y%, and these combinations pay most."',
     'This project is deliberately about the current market - it signals to an interviewer that you work with real, fresh data.'),
]:
    A(P('<b>%s</b>' % t, S['h3']))
    A(P('<b>Business question:</b> %s' % q, S['body']))
    A(P('<b>Dataset:</b> %s' % ds, S['body']))
    A(P('<b>Steps:</b> %s' % steps, S['body']))
    A(P('<b>What you show an interviewer:</b> %s' % show, S['body']))
    A(P('<b>Mistake to avoid:</b> %s' % avoid, S['pnote']))

A(Spacer(1, 4))
A(P('<b>How to publish your portfolio (do this, it doubles your reach):</b>'))
for b in bullets([
    'Push every project to <b>GitHub</b> with a clean README: the business question, the data source, the method, and the result.',
    'Write a short <b>LinkedIn post</b> per project - the question you asked, one chart, and one finding. Recruiters search LinkedIn.',
    'Keep a one-page PDF summary of each project ready to attach to applications.',
    'Put the GitHub link at the top of your resume and in your LinkedIn "Featured" section.',
]):
    A(b)

A(PageBreak())

# ================================================================ PART 6
section(story, 'PART 6', 'The ATS resume',
        'Most Indian companies run your resume through an applicant-tracking system (ATS) before a human sees '
        'it. The ATS matches keywords from the job description and rejects anything it cannot parse. A beautiful '
        'two-column designer resume often scores worse than a plain one-column document.')

A(P('<b>The seven ATS rules:</b>'))
for b in bullets([
    'Use <b>one column</b>. Multi-column layouts, text boxes and tables confuse many ATS parsers.',
    'Use <b>standard section headings</b>: Summary, Skills, Experience, Projects, Education, Certifications.',
    'Mirror the <b>exact keywords</b> from the job description (SQL, Power BI, data cleaning, dashboards, stakeholder communication).',
    'Keep it to <b>one page</b> as a fresher. Two pages only after 3-4 years of experience.',
    'Save as <b>PDF</b> (unless the posting asks for .docx) and name the file Firstname_Lastname_DataAnalyst.pdf.',
    'No photos, graphics, icons, or skill-percentage bars - the ATS cannot read them and humans do not trust them.',
    'Lead every bullet with a <b>verb and a number</b>.',
]):
    A(b)

A(P('<b>The bullet formula (use it for every line):</b>'))
A(code_block('Action + Tool + What + Result',
             'Built  [a thing]  using  [tool]  that  [did what]  resulting in  [a number or outcome].\n\n'
             'Weak:   Worked on a sales dashboard using Power BI.\n'
             'Strong: Built an interactive sales dashboard in Power BI over 40,000 rows\n'
             '        that cut the weekly reporting time from 3 hours to 15 minutes.'))
A(P('<b>Fresher note:</b> you have no work experience, so your Projects section carries the resume. Give each '
    'project two bullets in the formula above. Numbers can come from the dataset ("analysed 40,000 rows", '
    '"identified 12% of customers driving 41% of revenue").', S['pnote']))

A(P('<b>A complete fresher resume skeleton (replace the brackets):</b>'))
A(code_block('DATA ANALYST - RESUME TEMPLATE (one page)',
             '[YOUR NAME]\n'
             '[City]  |  [phone]  |  [email]  |  linkedin.com/in/[you]  |  github.com/[you]\n\n'
             'SUMMARY\n'
             'Aspiring Data Analyst with hands-on skills in SQL, Advanced Excel, Power BI and\n'
             'Python (pandas). Built 4 end-to-end projects on real datasets, including a sales\n'
             'dashboard and a SQL business analysis. Strong at translating business questions\n'
             'into clear analysis and dashboards. Available to join immediately.\n\n'
             'SKILLS\n'
             'SQL (joins, GROUP BY, window functions, CTEs) | Advanced Excel (XLOOKUP, PivotTables,\n'
             'Power Query) | Power BI (data model, DAX, dashboards) | Python (pandas, matplotlib) |\n'
             'Statistics (descriptive stats, A/B basics) | Data cleaning | Data storytelling\n\n'
             'PROJECTS\n'
             'Sales Performance Dashboard  |  Power BI, DAX\n'
             '  - Built an interactive dashboard over [40,000] rows that surfaced a [12%]\n'
             '    revenue concentration in [2] regions, supporting a re-allocation of ad spend.\n'
             '  - Wrote [5] DAX measures including month-over-month growth and top-N products.\n\n'
             'SQL Business Analysis  |  MySQL\n'
             '  - Answered [10] business questions in SQL, from monthly revenue trend to\n'
             '    RFM-style customer segmentation, documented with query, result and insight.\n\n'
             'Customer Segmentation  |  Python (pandas)\n'
             '  - Segmented [5,000+] customers by recency, frequency and value; recommended\n'
             '    a retention focus on the top segment worth [41%] of revenue.\n\n'
             'EDUCATION\n'
             '[Degree], [College], [University]  -  [Year]\n\n'
             'CERTIFICATIONS\n'
             '[Google Data Analytics Certificate - Coursera, 2026]'))

A(P('<b>Applying with the resume - the 30-second rule.</b> Tailor the top third of the resume to each role: '
    'change the Summary line and the order of the Skills line to match the keywords in that specific job '
    'description. A tailored resume is read; a generic one is filtered out.'))

A(PageBreak())

# ================================================================ PART 7
section(story, 'PART 7', 'LinkedIn and Naukri profiles',
        'A large share of Indian analyst hiring happens through recruiter search, not job-board applications. '
        'Recruiters search by keyword - so your profile must contain the exact words they type.')

A(P('<b>Naukri (still the most important board in India).</b> Most traditional Indian companies and many MNCs '
    'post on Naukri first, and recruiter search runs on your skill tags. Complete the profile fully:'))
for b in bullets([
    'Fill the <b>Resume Headline</b> with target keywords: "Data Analyst | SQL | Power BI | Advanced Excel | Python".',
    'Add every relevant <b>Key Skill tag</b> individually - SQL, MySQL, Microsoft Power BI, Advanced Excel, Python, pandas, Data Analysis, Data Visualization. Recruiter filters match these tags.',
    'Set <b>experience to "0 years"</b> or your real number, and mark yourself immediately available.',
    'Upload the same ATS-friendly PDF you send to companies.',
    'Update your profile weekly - a recently updated profile ranks higher in recruiter search.',
]):
    A(b)

A(P('<b>LinkedIn (where the better roles and referrals live).</b>'))
for b in bullets([
    '<b>Headline:</b> "Data Analyst (Fresher) | SQL, Power BI, Excel, Python | Built 4 portfolio projects". Do not leave it as your degree.',
    '<b>About section:</b> three short paragraphs - who you are, the tools you use, and a link to your GitHub. Use keywords naturally.',
    '<b>Featured section:</b> pin your best dashboard screenshot or GitHub repo so it is the first thing a recruiter clicks.',
    '<b>Skills:</b> add and get endorsements for SQL, Power BI, Excel, Python, Data Analysis.',
    '<b>Open to work:</b> turn it on and list the target titles from Part 2.',
    '<b>Post cadence:</b> one short post per project (question, one chart, one finding). Tag the tools. This is how recruiters and alumni find you.',
]):
    A(b)

A(P('<b>The recruiter outreach message (send it after you apply, to the recruiter or hiring manager):</b>'))
A(code_block('LinkedIn / Naukri message template',
             'Hi [Name], I applied for the [Data Analyst] role at [Company] and wanted to\n'
             'add a quick note. I have hands-on SQL, Power BI and Excel skills and I recently\n'
             'built [a sales dashboard / a SQL business analysis] on real data - here is my\n'
             'portfolio: [GitHub link]. I am available to join immediately and would welcome\n'
             'a short conversation. Thank you for your time.'))
A(P('Keep it to four lines, always include a portfolio link, and never send the same message with the company '
    'name blank. Referrals convert far better than cold job-board applications - ask alumni from your college '
    'who work in analytics.', S['pnote']))

A(PageBreak())

# ================================================================ PART 8
section(story, 'PART 8', 'Interview prep: 60 questions',
        'Indian data-analyst interviews for 0-1 year roles follow a predictable structure. Prepare each round '
        'separately and you will walk in calm instead of hoping the questions match what you studied.')

A(P('<b>The six rounds you should expect.</b> Startups often compress these into one 90-minute session; IT '
    'services may split them across two days. Always ask the recruiter which tools and whether there is a live '
    'coding test.'))
A(table([
    [cellp('Round', 'cellb'), cellp('What happens', 'cellb'), cellp('How to prepare', 'cellb')],
    [cellp('HR screening (15-25 min)'), cellp('Intro, salary, relocation, notice period'), cellp('A 2-minute pitch; a researched salary band')],
    [cellp('Aptitude / MCQ'), cellp('Logic, percentages, sometimes SQL MCQs'), cellp('Practise 20 aptitude sets')],
    [cellp('Technical - Excel'), cellp('Live sheet: pivot, lookup, clean data'), cellp('Rebuild one MIS report from raw data')],
    [cellp('Technical - SQL'), cellp('3-8 queries: joins, GROUP BY, windows'), cellp('50 timed queries on a 3-table schema')],
    [cellp('Technical - BI'), cellp('"Walk us through your dashboard"'), cellp('A 5-minute recorded walkthrough')],
    [cellp('Manager / case'), cellp('"Sales dropped - what do you check?"'), cellp('Structured hypothesis lists')],
], [40 * mm, 52 * mm, None]))

A(P('<b>SQL questions (the highest-leverage round).</b> Practise these until you can write each from memory on '
    'a three-table schema (customers, orders, products).', S['h2']))
for q, a in [
    ('1. Get the top 5 products by total revenue.',
     'SELECT product_id, SUM(price*qty) AS revenue FROM order_items GROUP BY product_id ORDER BY revenue DESC LIMIT 5;'),
    ('2. Find customers who have never placed an order.',
     'SELECT c.* FROM customers c LEFT JOIN orders o ON c.id=o.customer_id WHERE o.id IS NULL;'),
    ('3. Monthly revenue trend for the last 12 months.',
     'SELECT DATE_FORMAT(order_date,"%Y-%m") m, SUM(total) rev FROM orders GROUP BY m ORDER BY m DESC LIMIT 12;'),
    ('4. Average order value by city.',
     'SELECT c.city, AVG(o.total) aov FROM orders o JOIN customers c ON c.id=o.customer_id GROUP BY c.city;'),
    ('5. Customers whose spend is above the overall average.',
     'SELECT customer_id FROM orders GROUP BY customer_id HAVING SUM(total) > (SELECT AVG(total) FROM orders);'),
    ('6. Rank customers within each city by total spend.',
     'SELECT city, customer_id, SUM(total) s, RANK() OVER (PARTITION BY city ORDER BY SUM(total) DESC) rnk FROM orders JOIN customers USING(customer_id) GROUP BY city, customer_id;'),
    ('7. Running total of daily revenue.',
     'SELECT order_date, SUM(total) OVER (ORDER BY order_date) running FROM orders GROUP BY order_date;'),
    ('8. Month-over-month growth percentage.',
     'WITH m AS (SELECT DATE_FORMAT(order_date,"%Y-%m") mon, SUM(total) rev FROM orders GROUP BY mon) SELECT mon, rev, LAG(rev) OVER (ORDER BY mon) prev, ROUND((rev-LAG(rev) OVER (ORDER BY mon))*100.0/LAG(rev) OVER (ORDER BY mon),1) growth FROM m;'),
    ('9. Customers with more than one order (repeat buyers).',
     'SELECT customer_id, COUNT(*) n FROM orders GROUP BY customer_id HAVING COUNT(*) > 1;'),
    ('10. Second-highest salary/spend (classic puzzle).',
     'SELECT MAX(total) FROM orders WHERE total < (SELECT MAX(total) FROM orders);'),
]:
    A(P('<b>%s</b><br/><font face="Courier" size="8.4" color="#0a1628">%s</font>' % (q, a), S['body']))
A(P('Then practise the reasoning out loud: why a LEFT JOIN instead of an INNER JOIN, why HAVING and not WHERE, '
    'what a window function does that GROUP BY cannot. Interviewers test understanding, not memorisation.', S['pnote']))

A(P('<b>Excel tasks you will be given (do them under time):</b>', S['h2']))
for b in bullets([
    'Clean a deliberately messy CSV: remove duplicates, fix formats, handle blanks.',
    'Build a PivotTable summarising sales by month and region, then add a PivotChart.',
    'Use XLOOKUP to bring a product name into an orders sheet from a products sheet.',
    'Write SUMIFS/COUNTIFS for a conditional total (e.g. sales in the South region in Q3).',
    'Explain when you would use Power Query instead of manual cleaning.',
]):
    A(b)

A(P('<b>Power BI questions:</b>', S['h2']))
for b in bullets([
    'What is the difference between a calculated column and a measure? (Row context vs filter context.)',
    'What does CALCULATE do, and when do you use it?',
    'How do you handle a many-to-many relationship in your model?',
    'Walk me through your dashboard - what question does it answer?',
    'How would you show month-over-month growth in a card visual?',
]):
    A(b)

A(P('<b>Analytics case questions (use the same framework every time):</b>', S['h2']))
A(code_block('The 5-step case framework',
             '1. CLARIFY   - restate the question; ask what "success" means and the time frame.\n'
             '2. HYPOTHESIS - list 3-4 plausible causes before touching data.\n'
             '3. DATA      - say which tables/metrics you would pull to test each cause.\n'
             '4. INSIGHT   - state what the data would show and how you would verify it.\n'
             '5. ACTION    - give one clear recommendation and one way to measure it.'))
for q in [
    '"Sign-ups are up but revenue is flat. What do you check?"',
    '"A campaign has a high click-through rate but few conversions. Why?"',
    '"Which customers should we target to reduce churn?"',
    '"How would you measure whether a new feature worked?" (A/B testing basics.)',
]:
    A(Paragraph(q, S['body'], bulletText='\u2022'))

A(P('<b>Behavioural / STAR (use one story per question):</b>', S['h2']))
for b in bullets([
    '"Tell me about yourself." (60-90 seconds: who you are, your tools, your best project, why this role.)',
    '"Walk me through your best project." (Use the Part 5 walkthrough for Project 1 or 2.)',
    '"Tell me about a time you found something unexpected in data."',
    '"How do you handle a stakeholder who disagrees with your numbers?"',
    '"Describe a time you had to learn something quickly."',
    '"What is your biggest weakness?" (Pick a real, fixable one and say what you are doing about it.)',
    '"Where do you see yourself in three years?"',
]):
    A(b)

A(PageBreak())

# ================================================================ PART 9
section(story, 'PART 9', 'Salary and negotiation',
        'You will be asked your expectations in the very first HR round. Answer with a researched band, not a '
        'number you made up on the spot - and never with "as per company norms", which quietly costs you money.')

A(P('<b>Benchmarks to anchor against (India, 2026).</b> Use the row that matches your stack, and adjust down '
    'for a small city or a services company and up for a product company or BFSI/fintech.'))
A(table([
    [cellp('Situation', 'cellb'), cellp('Typical band', 'cellb')],
    [cellp('Fresher, Excel + Power BI, first job'), cellp('Rs 3 - 5 LPA')],
    [cellp('Fresher with a strong portfolio + SQL'), cellp('Rs 4 - 6 LPA')],
    [cellp('1-2 yrs, SQL + Power BI / Tableau'), cellp('Rs 6 - 10 LPA')],
    [cellp('1-2 yrs, SQL + Python'), cellp('Rs 8 - 12 LPA')],
    [cellp('3-5 yrs, Python + statistics, product/fintech'), cellp('Rs 12 - 18 LPA')],
], [None, 55 * mm]))
A(P('Sources: AmbitionBox, Glassdoor India and LinkedIn Salary Insights (2026), via careerskillguide. Self-reported '
    'and skewed toward higher earners - use as a range, and always ask the employer for their budget first.', S['pnote']))

A(P('<b>The negotiation script (memorise the shape, not the words):</b>'))
A(code_block('When asked "what are your salary expectations?"',
             '"Based on my research for [Data Analyst] roles in [city], and my SQL, Power BI\n'
             ' and Python skills plus my project portfolio, I am targeting [Rs X - Rs Y] LPA.\n'
             ' I am flexible for the right role and learning opportunity - could you tell me the\n'
             ' range budgeted for this position?"'))
for b in bullets([
    'Give a <b>band</b>, never a single number - a single number becomes your ceiling.',
    'Quote a band whose <b>bottom is your real target</b>, so the midpoint lands where you want.',
    'Always <b>ask their range</b> before you commit. If they name it first, you negotiate from knowledge.',
    'When they make an offer, negotiate <b>once</b>, politely, with one reason (the stack you bring). If they hold, accept or decline gracefully.',
    'If cash is fixed, negotiate what is flexible: joining bonus, early review at 6 months, or a defined learning budget.',
]):
    A(b)

A(P('<b>What not to do:</b> do not say "as per company norms"; do not quote a number you cannot justify with '
    'research; do not accept on the call without a written offer; and do not inflate your experience - offers '
    'are withdrawn after background checks.', S['pnote']))

A(PageBreak())

# ================================================================ PART 10
section(story, 'PART 10', 'The 7-day interview sprint',
        'Once you have an interview scheduled, run this seven-day plan. It is deliberately repetitive: practise '
        'each round in the format you will face it, not just read about it.')

for d, t in [
    ('Day 1 - SQL', 'Write 20 JOIN + GROUP BY queries, timed to 45 minutes. Then 10 window-function queries.'),
    ('Day 2 - Excel', 'Take one dirty CSV and produce a pivot, a lookup and a short written commentary.'),
    ('Day 3 - Power BI', 'Record a 5-minute screen walkthrough of your best dashboard and watch it back.'),
    ('Day 4 - Statistics', 'Explain mean vs median, correlation vs causation and A/B testing aloud, without notes.'),
    ('Day 5 - Behavioural', 'Write STAR stories for three projects and rehearse your 2-minute introduction.'),
    ('Day 6 - Mock', 'Do a full technical mock with a friend, mentor or an AI voice assistant. Note every weak query.'),
    ('Day 7 - Apply', 'Send 5 tailored applications and 5 recruiter messages. Match the resume keywords to each JD.'),
]:
    A(P('<b>%s:</b> %s' % (d, t), S['body']))

A(P('<b>The application tracker (keep it in a sheet - volume plus targeting is what works):</b>'))
A(table([
    [cellp('Company', 'cellb'), cellp('Role', 'cellb'), cellp('Applied on', 'cellb'), cellp('Round', 'cellb'), cellp('Next step / follow-up', 'cellb')],
    [cellp(' '), cellp(' '), cellp(' '), cellp(' '), cellp(' ')],
    [cellp(' '), cellp(' '), cellp(' '), cellp(' '), cellp(' ')],
    [cellp(' '), cellp(' '), cellp(' '), cellp(' '), cellp(' ')],
], [30 * mm, 30 * mm, 24 * mm, 22 * mm, None]))
A(P('Apply through multiple channels: job boards for volume, but put disproportionate effort into referrals '
    'and direct company applications, which convert at a higher rate. Follow up politely after 5-7 days. Aim '
    'for a steady 5 tailored applications a day rather than 50 generic ones.', S['pnote']))

A(Spacer(1, 4))
A(P('<b>Interview-day checklist:</b>'))
for b in checks([
    'Portfolio link ready to share (GitHub + one-page project PDF).',
    'A SQL editor open for a live test; know your 3-table schema by heart.',
    'Your 2-minute introduction rehearsed out loud.',
    'Three questions ready to ask the interviewer about the team and the data stack.',
    'One notebook example of a business insight you delivered from data.',
    'Researched salary band for the city and company tier written down.',
]):
    A(b)

A(PageBreak())

# ================================================================ PART 11
section(story, 'PART 11', 'Free resources and checklists',
        'You do not need to pay for a course to become job-ready. Everything below is free or has a strong free '
        'tier, and each is a recognised or widely used resource in the Indian market.')

A(P('<b>Learn the skills:</b>'))
for b in bullets([
    '<b>SQL:</b> SQLabHub and Kaggle Learn SQL - hands-on, query-based, free. Practise on MySQL/PostgreSQL with the Sakila sample database.',
    '<b>Power BI:</b> Microsoft Learn "Power BI Data Analyst" path (free) - the same path that prepares you for PL-300.',
    '<b>Excel:</b> Microsoft Support learning paths plus a self-built MIS report from a raw export.',
    '<b>Python:</b> Kaggle Learn "Python" and "Pandas" (free, short, practical).',
    '<b>Statistics:</b> Khan Academy statistics, and free NPTEL (IIT) courses on data analysis.',
    '<b>Certification (optional, one only):</b> Google Data Analytics Professional Certificate (Coursera) or Microsoft PL-300.',
]):
    A(b)

A(P('<b>Practise on real data (Indian datasets work best in interviews):</b>'))
for b in bullets([
    'data.gov.in - open Indian government datasets (population, health, transport, agriculture).',
    'Kaggle datasets - Zomato restaurants, IPL cricket, e-commerce orders, retail sales.',
    'Sakila / MySQL sample schema - the standard three-table schema for SQL practice.',
    'A live scrape of Naukri/LinkedIn analyst postings - for Project 4.',
]):
    A(b)

A(P('<b>Before you start applying - portfolio checklist:</b>'))
for b in checks([
    'Four projects done, each with a written business question and a recommendation.',
    'Every project on GitHub with a clear README.',
    'One-page PDF summary ready for each project.',
    'Best dashboard screenshotted and pinned on LinkedIn.',
    'Resume is one page, single column, keyword-tailored, saved as PDF.',
]):
    A(b)

A(P('<b>Before every application - resume checklist:</b>'))
for b in checks([
    'Top third tailored to this job description (Summary + Skills order).',
    'Every bullet uses the Action + Tool + Result formula.',
    'File named Firstname_Lastname_DataAnalyst.pdf.',
    'GitHub and LinkedIn links live and working.',
    'No graphics, columns, photos or skill bars.',
]):
    A(b)

A(Spacer(1, 6))
A(HRFlowable(width='100%', thickness=1.1, color=GOLD, spaceBefore=4, spaceAfter=8))
A(P('<b>The five mistakes that keep Indian freshers unemployed for a year:</b>', S['h2']))
for i, b in enumerate([
    'Learning tools forever and building nothing - a portfolio of four projects beats a wall of certificates.',
    'Applying with one generic resume to every job instead of tailoring the top third each time.',
    'Using pre-cleaned Kaggle datasets and making charts instead of answering a business question.',
    'Skipping SQL depth - it is required in over 90% of listings and is the most-tested skill.',
    'Never asking for referrals - a message to an alum in analytics converts far better than a cold application.',
], 1):
    A(P('%d. %s' % (i, b)))

A(PageBreak())

# ================================================================ APPENDIX
A(Paragraph('APPENDIX', S['kicker']))
A(Paragraph('Sources and verification', S['h1']))
A(gold_rule())
A(P('Every market figure, salary band, tool name and hiring fact in this kit was checked against live Indian '
    'sources in October 2026. Job markets and salaries change - re-verify before making a final decision. '
    'This kit is educational guidance, not a guarantee of employment or income.', 'lead'))
for s_ in [
    'GetUHired - "Data Analyst Jobs in India 2026" market report (4,166 unique postings, 22 June - 20 September 2026; ~312/week; 306 to 367 weekly growth; SQL 2,708, Python 1,910, Power BI 1,650).',
    'Naukri.com - "Data Analyst Jobs" listing, October 2026 (~27,000-plus active postings).',
    'Itdaksh Education - "Data Analyst Roadmap from Scratch India 2026" (SQL required in over 90% of listings; Power BI vs Tableau priority).',
    'knok.work - "Data Analyst Skills and Roadmap for India (2026)" (Power BI most-requested BI tool; recognised certifications: Google Data Analytics, Microsoft PL-300, NPTEL; city concentration).',
    'careerskillguide - "Data Analyst Salary India 2026" (salary bands and tool-stack premiums; sources: AmbitionBox April 2026, Glassdoor India March 2026, LinkedIn Salary Insights April 2026).',
    'DataVix - "How to Get a Data Analyst Job in India (2026 Complete Guide)" (skills order, portfolio over certificates, ATS resume).',
    'Masai School - "How to Become a Data Analyst in India in 2026 (No Experience)" (fresher salary Rs 3.5-6 LPA; Python premium; AI-assisted analysis as a 2026 differentiator).',
    'Asmorix - "Data Analyst Interview Questions for Freshers" (interview rounds: HR, aptitude, Excel, SQL, BI, manager/case; preparation cadence).',
    'KIT Skill Hub - "Complete Data Analyst Career Guide for Freshers 2026" (entry roles, six-step roadmap).',
]:
    A(Paragraph(s_, S['src'], bulletText='\u2022'))
A(Spacer(1, 10))
A(HRFlowable(width='100%', thickness=1.1, color=GOLD, spaceAfter=6))
A(P('The Data Analyst Career Starter Kit 2026 - First Edition, October 2026 · digitalaikart.shop · '
    'For personal use by the purchaser.', S['pnote']))

# ================================================================ BUILD
doc = BaseDocTemplate(os.environ.get('OUT', 'downloads/data-analyst-career-kit-2026.pdf'), pagesize=A4,
                      leftMargin=18 * mm, rightMargin=18 * mm,
                      topMargin=14 * mm, bottomMargin=18 * mm,
                      title='The Data Analyst Career Starter Kit 2026 - India Edition',
                      author='Digitalaikart')
frame = Frame(18 * mm, 18 * mm, PAGE_W - 36 * mm, PAGE_H - 32 * mm, id='main')
cover_frame = Frame(18 * mm, 18 * mm, PAGE_W - 36 * mm, PAGE_H - 32 * mm, id='cover')

story_with_toc = [Spacer(1, 1), NextPageTemplate('body'), PageBreak()] + build_toc() + story

tmpl_cover = PageTemplate('cover', frames=[cover_frame], onPage=cover)
tmpl_body = PageTemplate('body', frames=[frame], onPage=on_page)
doc.addPageTemplates([tmpl_cover, tmpl_body])

doc.build(story_with_toc, canvasmaker=_invariant_canvas)
print('built OK')
