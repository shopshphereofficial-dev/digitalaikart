#!/usr/bin/env python3
# Deterministic premium PDF builder for the AI Teacher Toolkit 2026.
# Navy #0a1628 / gold #f5c542. Built with reportlab in invariant mode so the
# byte output is reproducible on CI.
import os, sys

os.environ.setdefault("SOURCE_DATE_EPOCH", "1760000000")
import reportlab.rl_config as rl_config
rl_config.invariant = 1

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = sys.argv[1] if len(sys.argv) > 1 else "ai-teacher-toolkit-2026.pdf"

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
GREEN = HexColor("#4ade80")

F = "Helvetica"
FB = "Helvetica-Bold"
FI = "Helvetica-Oblique"

TITLE = "AI TEACHER TOOLKIT 2026"

prompt_count = 0


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
        self.c.setTitle("AI Teacher Toolkit 2026 — 100+ Ready Prompts & Classroom Playbook for Indian Teachers")
        self.c.setAuthor("Faisal Fayaz Lone")
        self.c.setSubject("AI prompts and workflows for Indian school teachers")
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
        # top hairline + bottom band
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
        c.drawString(M, 14, "Digitalaikart  \u00b7  AI Teacher Toolkit 2026")
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
        # frame
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.4)
        c.rect(38, 38, W - 76, H - 76, stroke=1, fill=0)
        c.setStrokeColor(GOLD_DIM)
        c.setLineWidth(0.6)
        c.rect(46, 46, W - 92, H - 92, stroke=1, fill=0)
        c.setFillColor(GOLD)
        c.setFont(FB, 11)
        c.drawCentredString(W / 2, H - 120, "D I G I T A L A I K A R T   O R I G I N A L")
        c.setFillColor(WHITE)
        c.setFont(FB, 40)
        c.drawCentredString(W / 2, H - 250, "AI TEACHER")
        c.setFillColor(GOLD)
        c.drawCentredString(W / 2, H - 300, "TOOLKIT 2026")
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.line(W / 2 - 70, H - 330, W / 2 + 70, H - 330)
        c.setFillColor(TEXT)
        c.setFont(FB, 15)
        c.drawCentredString(W / 2, H - 372, "100+ Ready Prompts & a Classroom Playbook")
        c.setFont(F, 13)
        c.setFillColor(MUTED)
        c.drawCentredString(W / 2, H - 396, "for Indian Teachers")
        c.setFillColor(TEXT)
        c.setFont(F, 10.5)
        c.drawCentredString(W / 2, H - 470, "Built for CBSE, ICSE and State Boards \u00b7 Classes 1\u201312")
        c.drawCentredString(W / 2, H - 490, "Lesson plans \u00b7 Question papers \u00b7 Worksheets \u00b7 Grading")
        c.drawCentredString(W / 2, H - 510, "Parent messages \u00b7 Regional languages \u00b7 The new CT & AI curriculum")
        c.setFillColor(WHITE)
        c.setFont(FB, 12)
        c.drawCentredString(W / 2, 210, "FAISAL FAYAZ LONE")
        c.setFillColor(MUTED)
        c.setFont(F, 10)
        c.drawCentredString(W / 2, 192, "First Edition \u00b7 October 2026")
        c.setFont(F, 8.6)
        c.drawCentredString(W / 2, 120, "Verified against CBSE Circular Acad-15/2026, NEP 2020, NCF-SE 2023")
        c.drawCentredString(W / 2, 106, "and official 2026 AI tool pricing for India.")
        c.setFillColor(GOLD)
        c.setFont(FB, 9)
        c.drawCentredString(W / 2, 74, "digitalkartai.shop")

    def h1(self, text):
        self.need(70)
        self.chapter = text
        self.toc.append((text, self.page))
        self.c.bookmarkPage("ch%d" % len(self.toc))
        self.c.addOutlineEntry(text, "ch%d" % len(self.toc), level=0)
        self.y -= 8
        self.c.setFillColor(GOLD)
        self.c.setFont(FB, 20)
        for ln in wrap(text, FB, 20, CW):
            self.c.drawString(M, self.y, ln)
            self.y -= 24
        self.y += 6
        self.c.setStrokeColor(GOLD)
        self.c.setLineWidth(1.6)
        self.c.line(M, self.y, M + 62, self.y)
        self.y -= 20

    def h2(self, text):
        self.need(46)
        self.y -= 6
        self.c.setFillColor(GOLD)
        self.c.setFont(FB, 13.5)
        for ln in wrap(text, FB, 13.5, CW):
            self.c.drawString(M, self.y, ln)
            self.y -= 18
        self.y -= 4

    def h3(self, text):
        self.need(34)
        self.c.setFillColor(WHITE)
        self.c.setFont(FB, 11)
        for ln in wrap(text, FB, 11, CW):
            self.c.drawString(M, self.y, ln)
            self.y -= 15
        self.y -= 3

    def p(self, text, color=None, size=10.4, font=F, lead=15.2):
        color = color or TEXT
        for ln in wrap(text, font, size, CW):
            self.need(lead)
            self.c.setFillColor(color)
            self.c.setFont(font, size)
            self.c.drawString(M, self.y, ln)
            self.y -= lead
        self.y -= 5

    def bullet(self, text, size=10.2):
        for i, ln in enumerate(wrap(text, F, size, CW - 16)):
            self.need(14.6)
            self.c.setFillColor(GOLD if i == 0 else TEXT)
            self.c.setFont(F, size)
            if i == 0:
                self.c.drawString(M + 2, self.y, "\u2022")
            self.c.drawString(M + 16, self.y, ln)
            self.y -= 14.6
        self.y -= 2

    def numbered(self, n, text, size=10.2):
        for i, ln in enumerate(wrap(text, F, size, CW - 22)):
            self.need(14.6)
            self.c.setFillColor(GOLD if i == 0 else TEXT)
            self.c.setFont(FB if i == 0 else F, size)
            if i == 0:
                self.c.drawString(M + 2, self.y, "%d." % n)
            self.c.drawString(M + 22, self.y, ln)
            self.y -= 14.6
        self.y -= 2

    def prompt(self, title, body):
        global prompt_count
        prompt_count += 1
        inner = CW - 26
        tlines = wrap("%d. %s" % (prompt_count, title), FB, 10.2, inner)
        blines = wrap(body, F, 9.5, inner)
        h = 16 + len(tlines) * 13.5 + len(blines) * 12.8 + 12
        self.need(h + 6)
        c = self.c
        top = self.y + 6
        c.setFillColor(CARD)
        c.rect(M, top - h, CW, h, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(M, top - h, 3.2, h, stroke=0, fill=1)
        yy = top - 16
        c.setFillColor(GOLD)
        c.setFont(FB, 10.2)
        for ln in tlines:
            c.drawString(M + 13, yy, ln)
            yy -= 13.5
        c.setFillColor(TEXT)
        c.setFont(F, 9.5)
        for ln in blines:
            c.drawString(M + 13, yy, ln)
            yy -= 12.8
        self.y = top - h - 8

    def callout(self, title, text):
        inner = CW - 30
        tlines = wrap(title, FB, 10.4, inner)
        blines = wrap(text, F, 9.8, inner)
        h = 14 + len(tlines) * 14 + len(blines) * 13.2 + 12
        self.need(h + 6)
        c = self.c
        top = self.y + 6
        c.setFillColor(CARD2)
        c.rect(M, top - h, CW, h, stroke=0, fill=1)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1)
        c.rect(M, top - h, CW, h, stroke=1, fill=0)
        yy = top - 17
        c.setFillColor(GOLD)
        c.setFont(FB, 10.4)
        for ln in tlines:
            c.drawString(M + 15, yy, ln)
            yy -= 14
        c.setFillColor(TEXT)
        c.setFont(F, 9.8)
        for ln in blines:
            c.drawString(M + 15, yy, ln)
            yy -= 13.2
        self.y = top - h - 8

    def table(self, headers, rows, widths=None, size=9.2):
        n = len(headers)
        if not widths:
            widths = [CW / n] * n
        total = sum(widths)
        widths = [w / total * CW for w in widths]
        # header
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
            rh = max(len(c) for c in cells) * 12.4 + 10
            self.need(rh)
            c.setFillColor(CARD if ri % 2 == 0 else NAVY_DEEP)
            c.rect(M, self.y - rh, CW, rh, stroke=0, fill=1)
            c.setFillColor(TEXT)
            c.setFont(F, size)
            x = M
            for i, cell in enumerate(cells):
                yy = self.y - 14
                for ln in cell:
                    c.drawString(x + 6, yy, ln)
                    yy -= 12.4
                x += widths[i]
            self.y -= rh
        self.y -= 8

    def spacer(self, h=8):
        self.y -= h

    def pagebreak(self):
        self.new_page()

    def finish(self):
        self.footer()
        self.c.showPage()
        self.c.save()


d = Doc(OUT)

# ======================= COVER =======================
d.cover()

# ======================= HOW TO USE =======================
d.new_page()
d.h1("How to Use This Toolkit")
d.p("This is not a book about artificial intelligence. It is a box of tools you can open on a "
    "Monday morning and use before the first bell. Every one of the prompts in this toolkit is "
    "written for an Indian classroom \u2014 a CBSE, ICSE or State Board teacher, a real chapter from "
    "NCERT or your state textbook, and the class sizes, languages and paperwork you actually deal with.")
d.h2("Three ways to use it")
d.numbered(1, "Straight copy-paste. Open the chapter you need (Lesson Plans, Question Papers, Parent "
              "Messages), pick a prompt, replace the parts in square brackets with your class, subject "
              "and chapter, and paste it into ChatGPT or Gemini.")
d.numbered(2, "Build your own prompt shelf. Once you see the pattern (Chapter 3), you can write your "
              "own prompts in two minutes instead of hunting for a template.")
d.numbered(3, "Follow the 30-day plan (Chapter 13). One small habit a day takes you from \u201cI tried "
              "AI once\u201d to \u201cAI saves me a full evening every week.\u201d")
d.h2("What is inside")
d.bullet("110 numbered, copy-paste prompts across 12 teaching jobs \u2014 planning, assessment, "
         "worksheets, grading, parent messages, administration and the new CT & AI curriculum.")
d.bullet("The 5-part teacher prompt formula (Role \u00b7 Context \u00b7 Task \u00b7 Format \u00b7 Guardrails) "
         "that stops generic answers.")
d.bullet("A verified 2026 tool and pricing sheet for India \u2014 including the free options that are "
         "genuinely good enough.")
d.bullet("Safety, privacy and academic-integrity rules written for schools, not for offices.")
d.callout("A promise about accuracy",
          "Every factual claim in Chapters 1, 2 and 12 \u2014 board circulars, curriculum hours, tool "
          "names and rupee prices \u2014 was checked against the official source in September\u2013October 2026. "
          "Prices and offers in AI change fast: the Appendix B cheat sheet tells you exactly where to "
          "re-check before you rely on a number.")

# ======================= CH 1 =======================
d.h1("1. The 2026 Classroom Reality")
d.p("Two things changed for Indian teachers in 2026, and both are official. First, AI literacy became "
    "part of the school curriculum. Second, powerful AI tools became free or near-free in India. "
    "Together they mean the question is no longer \u201cshould I use AI?\u201d but \u201cwhich 20 minutes of my "
    "week should I give back to it?\u201d")
d.h2("The curriculum has already moved")
d.p("On 1 April 2026, the Union Education Minister launched CBSE's Curriculum Framework for "
    "Computational Thinking (CT) and Artificial Intelligence (AI) for Classes III\u2013VIII, to run from "
    "the 2026\u201327 academic session. (Source: CBSE Circular No. Acad-15/2026 dated 01.04.2026; PIB "
    "release, 1 April 2026.)")
d.bullet("Classes 3\u20135 (Preparatory Stage): Computational Thinking only \u2014 50 hours a year, woven "
         "into Mathematics and \u201cThe World Around Us\u201d, taught by the existing subject teachers using "
         "CBSE worksheets and puzzles. No AI subject yet.")
d.bullet("Classes 6\u20138 (Middle Stage): 100 hours a year \u2014 Advanced CT (about 40 hours), "
         "Introductory AI literacy (about 20 hours) and two interdisciplinary projects (about 40 "
         "hours), delivered jointly by subject teachers and the Computer teacher.")
d.bullet("The framework is deliberately platform-agnostic and mandates CT + AI + Ethics + unplugged "
         "(no-computer) learning, with the stated goal of creating AI-literate learners by 2030.")
d.bullet("For Class IX, all other AI courses run up to 2025\u201326 are discontinued from 2026\u201327; "
         "Class X continues on the 2025\u201326 scheme, and NCERT is providing CT & AI modules for "
         "Classes IX\u2013XII in 2026\u201327 to be transacted as internal-assessment modules.")
d.callout("Why this matters to every teacher, not just computer teachers",
          "CBSE's annual teacher-training theme for 2026\u201327 is \u201cComputational Thinking and "
          "Understanding AI.\u201d The curriculum explicitly asks Mathematics, Science and Social Science "
          "teachers to carry the CT component in their own periods. You do not need to become an AI "
          "expert \u2014 but you do need to be comfortable running the activities. Chapter 11 gives you "
          "ten ready prompts for exactly that.")

d.h2("The tools are free enough in 2026")
d.p("The single most useful fact for an Indian teacher: you almost certainly do not need to pay "
    "anything. Here is the verified October 2026 picture.")
d.table(
    ["Tool / plan", "India price (Oct 2026)", "Good for"],
    [
        ["ChatGPT Free", "\u20b90", "Basic lesson plans, worksheets, quick drafts"],
        ["ChatGPT Go", "\u20b9399 / month", "Heavier daily use, GPT-5 class models"],
        ["ChatGPT Plus", "\u20b91,999 / month", "Deep Research, agent mode, long documents"],
        ["Google Gemini Free", "\u20b90", "Everyday help, 22 Indian languages, image reading"],
        ["Google AI Plus", "\u20b9399 / month (\u20b9199 intro, 6 months)", "More Gemini + NotebookLM, 400 GB storage, family sharing"],
        ["Google AI Pro", "\u20b91,950 / month", "Full Gemini, NotebookLM power features, 2 TB storage"],
        ["Google AI Ultra", "\u20b96,500 / month (5\u00d7 limits)", "Highest limits \u2014 not needed by most teachers"],
        ["NotebookLM", "Free tier", "Grounding AI in your own textbook PDFs"],
        ["Canva for Education", "Free for verified teachers", "Worksheets, slides, posters, certificates"],
        ["Bhashini", "Free", "Translation and voice in 22 Indian languages"],
    ],
    widths=[1.35, 1.5, 1.7])
d.callout("The Jio offer worth knowing",
          "Jio and Google are offering Google AI Pro (normally \u20b91,950/month) free for 18 months to "
          "Jio users aged 18+ on an active unlimited 5G plan of \u20b9349 or above, activated inside the "
          "MyJio app. If you qualify, that is a professional-grade AI subscription at no cost. "
          "Two earlier offers \u2014 Airtel's free Perplexity Pro year and OpenAI's free ChatGPT Go year "
          "\u2014 ended in January 2026, so do not rely on them.")
d.p("A note on the free tools: Gemini handles Hindi, Tamil, Telugu, Kannada, Bengali and other Indian "
    "languages noticeably better than most Western tools, so if you teach in a regional medium, start "
    "there. Bhashini is a Government of India language platform and is free.")

# ======================= CH 2 =======================
d.h1("2. Set Up in 30 Minutes")
d.p("You do not need a course, a certificate or a paid plan to begin. You need one free account, "
    "one clear policy for student data, and a rough idea of which tool to open for which job.")
d.h2("Which tool for which job")
d.table(
    ["Your job", "Open this", "Why"],
    [
        ["Lesson plans, worksheets, question papers", "ChatGPT or Gemini (free)", "Fast drafts, easy to edit, good tables"],
        ["Teaching in a regional language", "Gemini (free)", "Strongest Indian-language output of the free tools"],
        ["Working from your own textbook/chapter PDF", "NotebookLM", "Answers only from the sources you upload"],
        ["Posters, worksheets, slides, certificates", "Canva for Education", "Free for verified teachers; ready templates"],
        ["Translation and voice in Indian languages", "Bhashini", "Free government platform, 22 languages"],
        ["Teaching AI concepts to students (no computers)", "Google Teachable Machine + unplugged games", "Hands-on, no coding, works on one shared screen"],
    ],
    widths=[1.6, 1.25, 1.5])
d.h2("Five data rules to follow from day one")
d.numbered(1, "Never paste a student's full name, roll number, address, phone number or photograph "
              "into a public AI tool. Use \u201cStudent A\u201d, \u201cRoll 12\u201d or initials.")
d.numbered(2, "Never upload internal school documents \u2014 fee records, medical notes, staff "
              "confidential files \u2014 to a free consumer tool.")
d.numbered(3, "Treat everything the AI writes as a draft. You are the subject expert; the AI is a "
              "fast, tireless assistant that sometimes invents facts.")
d.numbered(4, "Check your school's own AI policy first. If your school has none, follow the "
              "safest rule: no identifiable student data leaves your device.")
d.numbered(5, "Tell students clearly when AI was used to prepare a resource, and hold them to the "
              "same honesty in their own work.")
d.callout("One habit that saves the most time",
          "Keep a single document called \u201cMy Prompts\u201d. Every time a prompt works well, save it with "
          "one line saying which class and subject you used it for. In a month you will have a "
          "personal prompt library worth more than any paid course.")

# ======================= CH 3 =======================
d.h1("3. The 5-Part Teacher Prompt")
d.p("\u201cMake a lesson plan on photosynthesis\u201d gives you a generic answer built for a Western "
    "classroom. \u201cYou are an experienced CBSE Class 7 Science teacher in India\u2026\u201d gives you something "
    "you can teach tomorrow. The difference is five parts, in this order.")
d.h2("Role \u00b7 Context \u00b7 Task \u00b7 Format \u00b7 Guardrails")
d.bullet("Role \u2014 tell the AI who it is. \u201cYou are an experienced CBSE Class 8 Mathematics teacher "
         "in India.\u201d")
d.bullet("Context \u2014 give the real details. Board, class, subject, chapter name, medium of "
         "instruction, number of students, time available.")
d.bullet("Task \u2014 one clear job. \u201cCreate a 40-minute lesson plan.\u201d Not five jobs at once.")
d.bullet("Format \u2014 say how you want it. \u201cUse a table with columns Time, Teacher activity, Student "
         "activity, Materials.\u201d")
d.bullet("Guardrails \u2014 the rules that protect you. \u201cUse only NCERT content. Do not invent facts. "
         "Add a note where I should verify. Keep language suitable for Class 8.\u201d")
d.h2("Before and after")
d.callout("Weak prompt",
          "Give me a lesson plan on the water cycle.")
d.callout("Strong prompt (all five parts)",
          "You are an experienced CBSE Class 6 Science teacher in India. Context: NCERT Class 6 "
          "Science, chapter on Water, 45 students, 40-minute period, English medium, no lab available. "
          "Task: Create one 40-minute lesson plan. Format: a table with columns \u2014 Time, Learning "
          "outcome, Teacher activity, Student activity, Materials. Guardrails: use only NCERT-level "
          "content, use everyday Indian examples, include one low-cost hands-on activity with "
          "materials available in any classroom, and add a final row telling me what to verify before "
          "teaching.")
d.h2("Two extra moves that upgrade almost any prompt")
d.bullet("Ask for the answer in a table. Tables are far easier to scan, edit and copy into your "
         "lesson-plan register.")
d.bullet("Add the line: \u201cWhere you are not certain, write [VERIFY] instead of guessing.\u201d This single "
         "line turns a confident-but-wrong answer into an honest draft you can trust.")

# ======================= CH 4 =======================
d.h1("4. Lesson Planning")
d.p("Twenty prompts for the single biggest weekly job. Replace the square brackets with your class, "
    "subject and chapter.")
P4 = [
 ("The 40-minute lesson plan", "You are an experienced [BOARD] Class [X] [SUBJECT] teacher in India. Context: [CHAPTER NAME] from the [NCERT/state] textbook, [N] students, one 40-minute period, [medium] medium. Task: create a complete 40-minute lesson plan. Format: table with columns Time, Learning outcome, Teacher activity, Student activity, Materials. Guardrails: use only textbook-level content, add [VERIFY] wherever uncertain."),
 ("The 5E lesson plan", "Create a 5E lesson plan (Engage, Explore, Explain, Elaborate, Evaluate) for [CHAPTER] for [BOARD] Class [X] [SUBJECT]. For each E, give the teacher's script in 3-4 sentences and the student task. Use Indian, everyday examples."),
 ("Chapter concept note", "Summarise the chapter [CHAPTER] from [BOARD] Class [X] [SUBJECT] into a one-page concept note: key definitions, 5 key terms with simple meanings, 3 formulas or rules, and one common student misconception. Keep it to Class [X] reading level."),
 ("Learning outcomes in NCF-SE style", "Write 5 learning outcomes for [CHAPTER] for Class [X] [SUBJECT] in the competency format used by NCF-SE 2023: \u201cStudents will be able to\u2026\u201d. Make them observable and assessable, not vague."),
 ("Prior-knowledge check", "Create 5 quick questions to find out what my Class [X] students already know about [TOPIC] before I teach [CHAPTER]. Keep it to 5 minutes, no marks."),
 ("Low-cost classroom activity", "Design one hands-on activity to teach [CONCEPT] to Class [X] using only materials available in an average Indian classroom (paper, chalk, water, stones, string). Explain the steps in 6 lines and what students should observe."),
 ("Real-life Indian examples", "Give me 8 real-life Indian examples or analogies that explain [CONCEPT] to a Class [X] student \u2014 from cricket, cooking, farming, trains, festivals or daily life."),
 ("20-minute homework", "Set homework on [CHAPTER] for Class [X] that takes about 20 minutes. Give 6 questions of increasing difficulty and a one-line instruction for parents."),
 ("Blackboard plan", "Write the exact blackboard plan for a 40-minute lesson on [TOPIC] for Class [X]: what to write, in what order, and where to draw a diagram. Present it as a sequence."),
 ("Story hook", "Write a 2-minute opening story or real-life situation to hook Class [X] students before I start [TOPIC]. End with a question that makes them curious."),
 ("Two-period unit plan", "Create a unit plan for [UNIT] for [BOARD] Class [X] [SUBJECT] across [N] periods. For each period give the topic, learning outcome and assessment. Format as a table."),
 ("Remedial plan", "My Class [X] students are weak in [TOPIC]. Create a 3-session remedial plan (20 minutes each) that rebuilds the basics with simple steps, worked examples and short practice."),
 ("Enrichment plan", "Design an enrichment task on [TOPIC] for the fast learners in Class [X] \u2014 one challenging project or investigation that takes a week and stretches their thinking."),
 ("Practical / lab plan", "Create a practical plan for [EXPERIMENT] for Class [X] Science: aim, materials, step-by-step method, expected observation, and the safety precautions to announce before students touch anything."),
 ("Map or diagram teaching plan", "Plan a 40-minute lesson to teach [MAP/DIAGRAM] in Class [X] [SUBJECT]: how to introduce it, what to label first, a memory trick, and 5 questions to check understanding."),
 ("Language lesson plan (poem/prose)", "Create a 40-minute lesson plan to teach the [POEM/CHAPTER] [NAME] in Class [X] [LANGUAGE]: theme, difficult words with meanings, comprehension questions, and one creative response task."),
 ("Maths word problems, Indian context", "Write 8 word problems on [TOPIC] for Class [X] Maths using Indian contexts (rupees, kilometres, cricket scores, market prices). Include a worked solution for each."),
 ("Revision lesson", "Plan a 40-minute revision lesson for [UNIT] before a test for Class [X]: a 10-minute recap, 20 minutes of mixed practice, and a 10-minute doubt round. Give the exact questions to use."),
 ("Group work plan", "Design a group activity on [TOPIC] for a Class [X] of 45 students. Explain how to form groups, what each group does, the time limits, and how to keep noise manageable."),
 ("Exit ticket", "Write a 5-minute exit-ticket for the end of a lesson on [TOPIC] for Class [X]: 3 questions that tell me whether the class understood, plus how to use the answers tomorrow."),
]
for t, b in P4:
    d.prompt(t, b)

# ======================= CH 5 =======================
d.h1("5. Question Papers & Assessment")
d.p("Question-paper making is where AI saves the most hours \u2014 and where you must check the most. "
    "Always review the output against your board's actual blueprint and marking scheme.")
P5 = [
 ("Paper blueprint with marks distribution", "Create a question-paper blueprint for [BOARD] Class [X] [SUBJECT], unit [UNIT], total [N] marks. Give a table: section, question type, number of questions, marks each, total marks. Follow the current [BOARD] pattern for 2026-27."),
 ("5 MCQ + 3 short + 2 HOTS with answer key", "You are an experienced [SUBJECT] teacher and assessment designer. From the chapter content below, create: 5 MCQs (4 options, mark the correct one), 3 short-answer questions, and 2 HOTS (application/case-based) questions. Then give a complete answer key. Content: [PASTE CHAPTER TEXT]."),
 ("Assertion-reason questions", "Create 6 assertion-reason questions on [TOPIC] for Class [X], in the standard format (Assertion A, Reason R, options a-d). Provide the correct answers with one-line reasoning."),
 ("Case-study / competency-based question", "Create one case-study based question on [TOPIC] for Class [X] as per the CBSE competency-based format: a short real-life passage (80-100 words) followed by 4 sub-questions of increasing difficulty, with answers."),
 ("Numerical problems with solutions", "Write 8 numerical problems on [TOPIC] for Class [X] [SUBJECT], from easy to hard, with full step-by-step solutions and the final answer in SI units."),
 ("Diagram-based questions", "Create 5 diagram-based questions on [TOPIC] for Class [X]. Describe each diagram clearly in text so I can draw it on the board, and give the answer for each."),
 ("Fill-ups and match-the-column", "Create a 10-mark exercise on [TOPIC] for Class [X]: 5 fill-in-the-blanks, one match-the-column with 5 pairs, and 3 true/false statements. Give the answer key."),
 ("True/false with justification", "Write 6 true/false statements on [TOPIC] for Class [X] where students must also justify their answer in one line. Give the key with the reasoning."),
 ("Two versions of the same test", "Create two versions (Set A and Set B) of a [N]-mark test on [UNIT] for Class [X]. Both must cover the same concepts at the same difficulty, but with different questions and numbers, so copying is pointless. Provide both answer keys."),
 ("HOTS question bank", "Create 10 higher-order-thinking questions on [UNIT] for Class [X] that require application, analysis or reasoning rather than recall. Tag each with the skill it tests and give a model answer."),
 ("Full periodic test paper", "Generate a complete [N]-mark periodic test paper for [BOARD] Class [X] [SUBJECT] covering [UNITS], following the 2026-27 [BOARD] pattern (sections, marks, internal choice). Then give the marking scheme."),
 ("Answer key with marking scheme", "Create a detailed marking scheme for the question paper below, for Class [X]: for each question give the expected points and how to award partial marks. Paper: [PASTE PAPER]."),
 ("Rubric for a subjective answer", "Create a 4-level rubric (0-1-2-3) to mark a long answer on [TOPIC] for Class [X], describing exactly what earns each level. Keep it to one page."),
 ("Oral / viva question bank", "Create 20 oral/viva questions on [TOPIC] for Class [X], from easy to probing, with the key idea expected in each answer. Suitable for a 5-minute viva per student."),
 ("Project assessment with rubric", "Design a project on [TOPIC] for Class [X]: the brief, the timeline, what students submit, and a rubric with 4 criteria scored out of 5 each. Total 20 marks."),
 ("Portfolio / activity assessment sheet", "Create an observation sheet to assess Class [X] students during activities on [TOPIC]: 5 criteria, a 3-point scale, and space to note one specific comment per student."),
 ("Diagnostic test to find gaps", "Create a 15-question diagnostic test on the prerequisites for [CHAPTER] for Class [X]. Include an answer key and a simple way to read the results \u2014 which wrong answers point to which gap."),
 ("Question paper in a regional language", "Create a [N]-mark question paper on [TOPIC] for Class [X] in [LANGUAGE]. Keep the technical terms in English in brackets after the regional word. Then give the answer key in English."),
 ("Bloom's-tagged question bank", "Create 20 questions on [UNIT] for Class [X] and tag each with the Bloom's level it tests (Remember, Understand, Apply, Analyse, Evaluate, Create). Aim for a spread across all six levels."),
 ("Previous-year-style practice paper", "Create a practice paper for [BOARD] Class [X] [SUBJECT] in the style and difficulty of past board papers on [UNIT], with an answer key. Mark any question whose style you are unsure about with [VERIFY]."),
]
for t, b in P5:
    d.prompt(t, b)

# ======================= CH 6 =======================
d.h1("6. Worksheets & Differentiation")
d.p("One chapter, three levels, one worksheet set. These prompts let you serve the whole class "
    "without working three times as hard.")
P6 = [
 ("Differentiated worksheet, 3 levels", "Create a worksheet on [TOPIC] for Class [X] in three levels: Level 1 (basic, for students who struggle), Level 2 (standard), Level 3 (challenge, for fast learners). Same concept, different difficulty. Include an answer key for each."),
 ("Worksheet with answer key", "Create a 20-mark worksheet on [TOPIC] for Class [X] with a mix of MCQ, short answer and one application question. Give the answer key at the end."),
 ("Visual worksheet (text-described)", "Create a worksheet on [TOPIC] for Class [X] that needs diagrams. Describe each diagram in words so I can draw it, and add a question for each."),
 ("Scaffolded worksheet with hints", "Create a worksheet on [TOPIC] for Class [X] where each question has a small hint in a box. The hints should guide thinking without giving the answer."),
 ("Concept-map worksheet", "Give me a blank concept map for [UNIT] for Class [X] \u2014 the central idea and 8 linked boxes, with the correct links provided separately as an answer key."),
 ("Worksheet for slow learners", "Rewrite the key ideas of [CHAPTER] for Class [X] using very simple sentences and short words, then add 8 easy questions. Keep the reading level two classes lower."),
 ("Extension worksheet for toppers", "Create a challenging extension worksheet on [TOPIC] for the top 5 students of Class [X]: 5 questions that need reasoning, estimation or open-ended thinking, with model answers."),
 ("Vocabulary worksheet", "Create a worksheet with 15 important terms from [CHAPTER] for Class [X]: each term with a simple meaning, then a matching exercise and 5 fill-ups using the terms."),
 ("Worksheet in simple English", "Create a worksheet on [TOPIC] for Class [X] written in very simple English, with short sentences, so students who read slowly can still attempt it. Include an answer key."),
 ("10-minute homework worksheet", "Create a quick 10-minute practice worksheet on [TOPIC] for Class [X] \u2014 8 short questions, one line each, with answers."),
 ("Practical worksheet", "Create a worksheet to go with the [EXPERIMENT] practical for Class [X]: aim, materials, a table to record observations, 3 analysis questions and one conclusion line for students to complete."),
 ("Reading comprehension, Indian context", "Write a 150-word passage on [TOPIC] set in an Indian context, for Class [X], followed by 5 comprehension questions (2 literal, 2 inferential, 1 opinion) and an answer key."),
 ("Maths drill sheet", "Create a 20-question drill sheet on [TOPIC] for Class [X] Maths, arranged from easy to hard, with all answers. Keep numbers manageable so students can compute without a calculator."),
 ("Pre-exam revision worksheet", "Create a revision worksheet covering the whole of [UNIT] for Class [X]: a 10-line summary, 15 mixed questions and an answer key. Suitable for one evening of revision."),
]
for t, b in P6:
    d.prompt(t, b)

# ======================= CH 7 =======================
d.h1("7. Grading, Feedback & Rubrics")
d.p("AI cannot replace your judgement on a student's answer, but it is excellent at drafting the "
    "words of feedback, spotting patterns in mistakes, and building rubrics.")
P7 = [
 ("Feedback on a short answer", "Here is a Class [X] student's answer on [TOPIC]: [PASTE ANSWER]. Give feedback in 3 short parts: what is correct, what is missing, and one concrete next step. Keep it encouraging and suitable for the student to read."),
 ("Turn a rough answer into a model answer", "Here is a weak answer on [TOPIC] for Class [X]: [PASTE]. Rewrite it as a model answer of the length and depth expected in a board exam, then list the 3 differences between the two so I can explain them in class."),
 ("Common-mistake analysis", "Here are 5 wrong answers from my Class [X] test on [TOPIC]: [PASTE]. Identify the common mistake behind each, and suggest one targeted re-teach for each mistake."),
 ("Personalised feedback comment bank", "Create a bank of 15 short feedback comments for Class [X] work on [TOPIC] \u2014 5 praising good work, 5 pointing to a specific weakness, 5 suggesting improvement. Keep each to one sentence."),
 ("Class-level feedback summary", "Here are the scores from a Class [X] test: [PASTE]. Write a short summary I can read to the class: what most students did well, the two weakest areas, and one thing we will fix this week. Do not name any student."),
 ("Rubric generator", "Create a 4-level rubric for the assignment [DESCRIBE ASSIGNMENT] for Class [X], with 4 criteria and clear descriptors for each level. Total marks [N]."),
 ("Consistent grading of a set of answers", "Here are 6 student answers on [TOPIC] for Class [X]: [PASTE]. Score each out of [N] using the same standard, explain each score in one line, and tell me if any answer was borderline."),
 ("Written-work correction checklist", "Give me a 6-point checklist I can stick on my desk to correct Class [X] notebooks on [SUBJECT] quickly and consistently \u2014 what to mark, what to ignore, and how to write one useful comment."),
 ("Student self-assessment sheet", "Create a simple self-assessment sheet for Class [X] after the [TOPIC] unit: 6 \u201cI can\u2026\u201d statements students tick (yes / not yet), plus two lines for what they want help with."),
 ("Peer-assessment sheet", "Create a peer-assessment sheet for Class [X] students to review each other's work on [TASK]: 4 criteria, a 3-point scale, and one \u201cone thing I liked\u201d and \u201cone thing to improve\u201d box."),
]
for t, b in P7:
    d.prompt(t, b)

# ======================= CH 8 =======================
d.h1("8. Parent Communication")
d.p("Clear, warm, short messages save you dozens of phone calls. Always keep the school's approved "
    "tone and never put a child's private details into a public AI tool.")
P8 = [
 ("Positive note home", "Write a short, warm note to the parents of a Class [X] student about good work in [SUBJECT] this week. One paragraph, positive and specific, no marks mentioned. Keep it under 80 words."),
 ("Concern note (attendance/behaviour)", "Write a respectful note to parents about a Class [X] student's [LOW ATTENDANCE / CLASSROOM BEHAVIOUR]. Be factual and kind, ask for a meeting, and avoid blaming language. Under 90 words."),
 ("PTM talking points \u2014 weak student", "Prepare talking points for a parent-teacher meeting about a Class [X] student who is struggling in [SUBJECT]. Give 3 strengths to open with, 2 concerns stated gently, and 3 concrete ways the parent can help at home."),
 ("PTM talking points \u2014 bright student", "Prepare talking points for a parent-teacher meeting about a Class [X] student who is doing very well in [SUBJECT]. Include 3 specific strengths, one area to stretch, and one suggestion to keep them challenged."),
 ("Exam-preparation note to parents", "Write a note to parents of Class [X] about the upcoming [EXAM]: dates, what to revise, how much to study each day, and 4 simple ways parents can support without pressure. Under 150 words."),
 ("Holiday homework note", "Write a short note to parents of Class [X] about the holiday homework for [SUBJECT]: what it is, how long it should take each day, and a reminder to let children work independently."),
 ("Circular for an activity or trip", "Write a school circular for Class [X] about [ACTIVITY / FIELD TRIP]: purpose, date, timing, what to bring, and consent line. Formal but friendly, under 150 words."),
 ("Fees / forms reminder (neutral)", "Write a neutral reminder to parents of Class [X] about [FORM / FEE DEADLINE]. Do not mention amounts; keep it factual and polite, with the school office contact line."),
 ("Message in Hindi (transliterated)", "Write a short message to parents of Class [X] in Hindi, typed in Roman letters (Hinglish), about [TOPIC / EVENT]. Simple words, under 70 words, respectful tone."),
 ("Message in Tamil (transliterated)", "Write a short message to parents of Class [X] in Tamil, typed in Roman letters (Tanglish), about [TOPIC / EVENT]. Simple words, under 70 words."),
 ("Message in Marathi (transliterated)", "Write a short message to parents of Class [X] in Marathi, typed in Roman letters, about [TOPIC / EVENT]. Simple words, under 70 words."),
 ("WhatsApp group announcement", "Write a 3-line WhatsApp announcement for the Class [X] parents' group about [EVENT]. Short, clear, with date, time and what to bring. No more than 40 words."),
]
for t, b in P8:
    d.prompt(t, b)

# ======================= CH 9 =======================
d.h1("9. Regional Language & Inclusion")
d.p("India teaches in more than twenty languages. Gemini and Bhashini are the strongest free options "
    "for regional-medium work; always read the output aloud once before using it.")
P9 = [
 ("Explain a concept in Hindi", "Explain [CONCEPT] to a Class [X] student in simple Hindi (Devanagari). Use everyday examples, keep sentences short, and end with 3 practice questions in Hindi."),
 ("Translate a worksheet to Tamil", "Translate this worksheet into Tamil for Class [X], keeping technical terms in English in brackets after the Tamil word. Worksheet: [PASTE]."),
 ("Bilingual glossary", "Create a bilingual glossary of 20 key terms from [CHAPTER] for Class [X] in English and [LANGUAGE]. Format as a two-column table."),
 ("Simplify text for learning needs", "Rewrite this passage for a Class [X] student who has difficulty reading: shorter sentences, common words, one idea per line. Passage: [PASTE]."),
 ("Instructions in the mother tongue", "Write the classroom instructions for the [ACTIVITY] in [LANGUAGE] so I can read them out to my Class [X] students, with the English meaning in brackets."),
 ("Audio-overview script for a chapter", "Write a 3-minute spoken script that explains [CHAPTER] to Class [X] students as if for a podcast \u2014 friendly, clear, with one question at the end. I will paste it into a tool like NotebookLM to make an audio overview."),
 ("Multi-grade classroom lesson", "Design one 40-minute activity that works for a multi-grade classroom with Class [X] and Class [Y] together on [TOPIC]. Explain how to split attention and what each group does."),
 ("Inclusive mixed-ability activity", "Design a group activity on [TOPIC] for a mixed-ability Class [X], where every member has a role suited to their level (recorder, presenter, materials, timekeeper). Explain how to assign roles fairly."),
]
for t, b in P9:
    d.prompt(t, b)

# ======================= CH 10 =======================
d.h1("10. Administration & Records")
d.p("The paperwork nobody trained you for \u2014 done in minutes.")
P10 = [
 ("Lesson-plan register entry", "Convert this lesson plan into a single paragraph suitable for a school lesson-plan register entry for Class [X] [SUBJECT]. Format: date, topic, learning outcome, activity, assessment. Plan: [PASTE]."),
 ("Monthly teaching report", "Write a one-page monthly teaching report for Class [X] [SUBJECT] for [MONTH]: topics covered, activities done, assessment held, and points for next month. Formal school tone."),
 ("Syllabus-completion tracker", "Create a syllabus-completion tracker for [SUBJECT] Class [X] for the year: a table with unit, planned periods, done periods, and status. Leave the \u2018done\u2019 columns blank for me to fill."),
 ("Invigilation / exam duty note", "Write a short note I can keep for exam duty on [DATE]: reporting time, what to check, seating arrangement steps and how to handle a suspected unfair-means case. Keep it to a one-page checklist."),
 ("Absence follow-up letter", "Write a polite follow-up letter to the parents of a Class [X] student who has been absent for [N] days. Factual, concerned, no accusation, and a request to meet the class teacher."),
 ("Minutes of a staff meeting", "Turn these rough notes from a staff meeting into clean minutes for [DATE]: [PASTE NOTES]. Format: decisions taken, action points, who is responsible, by when."),
 ("Circular to students", "Write a circular to Class [X] students about [TOPIC / EVENT] \u2014 short, clear, with date, time, venue and what to bring. One paragraph."),
 ("Annual report paragraph for a class", "Write a 120-word paragraph for the school annual report describing Class [X]'s year in [SUBJECT]: activities, achievements and one highlight. Positive and specific."),
 ("Progress-report comments (25 students)", "Write a bank of 25 short progress-report comments for Class [X] \u2014 a mix of praise, steady-progress, needs-attention and improvement comments. Each one sentence, no student names."),
 ("Revision schedule around the timetable", "Build a revision schedule for [SUBJECT] Class [X] before [EXAM], fitting study around a normal school day. Give a day-by-day table for [N] days with topics and time per day."),
]
for t, b in P10:
    d.prompt(t, b)

# ======================= CH 11 =======================
d.h1("11. Teaching the New CT & AI Curriculum")
d.p("From 2026-27, CBSE's CT & AI curriculum runs for Classes III\u2013VIII, with Mathematics, Science "
    "and Social Science teachers carrying the Computational Thinking component in their own periods. "
    "These prompts help you run it confidently \u2014 no coding, no new schedule.")
P11 = [
 ("Unplugged CT activity (Classes 3-5)", "Design an unplugged (no computer) activity to teach sequencing and step-by-step thinking to Class [3-5] students using paper, chalk or physical movement. Give clear steps and what to observe."),
 ("Pattern-recognition puzzle set (Classes 3-5)", "Create 8 pattern-based puzzles for Class [3-5] using numbers, shapes and everyday pictures. Arrange them from easy to hard and give the answers."),
 ("Algorithm activity (Classes 6-8)", "Create a step-by-step \u2018algorithm\u2019 activity for Class [6-8] on [everyday task, e.g. making tea]. Then give one version with a deliberate mistake and ask students to debug it."),
 ("Decomposition exercise (Classes 6-8)", "Give a decomposition exercise for Class [6-8]: take one big problem ([SCHOOL FESTIVAL / A SCHOOL CANTEEN MENU]) and break it into smaller sub-problems. Provide a worked example and a blank template for students."),
 ("AI-literacy explainer (Classes 6-8)", "Write a simple, age-appropriate explanation of what Artificial Intelligence is and how it learns from data, for Class [6-8] students. Use 3 everyday Indian examples and end with 4 discussion questions."),
 ("AI ethics debate topics", "Give 6 age-appropriate debate topics on AI ethics for Class [6-8] \u2014 fairness, bias, privacy, jobs and honesty. For each, provide one argument for and one against."),
 ("Two AI project ideas with rubrics", "Suggest 2 interdisciplinary AI/CT project ideas for Class [6-8], each taking about 20 hours. For each, give the aim, steps, what students submit, and a rubric scored out of 10."),
 ("Teacher observation journal template", "Create a Teacher Observation Journal template to track Class [3-5] students' computational-thinking progress: what to observe, a simple 3-point scale, and space for one note per student per month."),
 ("Worksheet mapped to a Maths chapter", "Create a worksheet of CT-flavoured questions mapped to the [MATHS CHAPTER] of Class [X], in the style of CBSE's CT resource books: thinking-based, not recall. Give the answers with reasoning."),
 ("AI-awareness assembly talk", "Write a 3-minute assembly talk for Class [6-8] students introducing AI \u2014 what it is, what it can and cannot do, and how to use it honestly. Simple, engaging, no jargon."),
]
for t, b in P11:
    d.prompt(t, b)

# ======================= CH 12 =======================
d.h1("12. Safety, Ethics & Academic Integrity")
d.p("Using AI well is a professional skill; teaching students to use it honestly is now part of the "
    "job. Here are the rules, then six prompts that keep you on the right side of them.")
d.h2("The ten rules")
RULES = [
 "The AI drafts; you decide. Never teach a fact you have not checked.",
 "No identifiable student data in a public AI tool \u2014 names, roll numbers, photos, addresses.",
 "Never upload confidential school records to a free consumer tool.",
 "Read the AI's output fully before it reaches a student. Every time.",
 "Add \u201cwrite [VERIFY] instead of guessing\u201d to prompts about facts, numbers and law.",
 "Keep a copy of the source you checked, in case a parent or the principal asks.",
 "Tell students when a resource was AI-assisted. Model the honesty you expect.",
 "AI must not do a student's thinking for them \u2014 it can explain, not replace.",
 "Check for bias in examples and questions; correct stereotypes before use.",
 "If something feels wrong, slow down. Speed is never worth an error in a classroom.",
]
for i, r in enumerate(RULES, 1):
    d.numbered(i, r)
P12 = [
 ("Rewrite in the student's own voice (integrity-safe)", "I have a student's rough draft on [TOPIC]. Help me show them how to improve it themselves: give 5 guiding questions they should answer, and one example of how to strengthen a weak sentence \u2014 without writing the answer for them. Draft: [PASTE]."),
 ("Fact-check a passage", "Check this passage for factual errors at Class [X] level and list anything doubtful with the correct version and a source to check. Passage: [PASTE]."),
 ("Age-appropriate explanation policy", "Explain [SENSITIVE TOPIC] to Class [X] students in an age-appropriate, neutral and respectful way, suitable for a classroom in India. Flag anything I should get the principal's approval for."),
 ("Detect AI-written student work", "Here is a piece of student work for Class [X]: [PASTE]. List the signs that suggest it may have been copied from an AI tool, and suggest how to have a fair conversation with the student about it."),
 ("Classroom AI-use rules (student charter)", "Draft a one-page AI-use charter for Class [X] students: 6 clear do's and don'ts, written simply, that we can print and stick on the classroom wall."),
 ("Anonymise student data", "Rewrite these class notes so no student can be identified \u2014 replace names with letters and remove any personal detail. Notes: [PASTE]."),
]
for t, b in P12:
    d.prompt(t, b)

# ======================= CH 13 =======================
d.h1("13. The 30-Day Adoption Plan")
d.p("Do not try to change everything at once. One small step a day, and by the end of the month AI "
    "will have quietly given you back a full evening every week.")
d.table(
    ["Days", "Focus", "What you do"],
    [
        ["1-3", "Get set up", "Create one free account (ChatGPT or Gemini). Write the 5-part prompt formula on a sticky note. Try prompt 1 once."],
        ["4-7", "Lesson planning", "Use three lesson-planning prompts (Chapter 4) for real classes. Save the two that worked best."],
        ["8-11", "Assessment", "Generate one MCQ set and one HOTS question with answer keys (Chapter 5). Check every question before use."],
        ["12-15", "Worksheets", "Create one differentiated worksheet (Chapter 6) at three levels for a topic you teach this week."],
        ["16-19", "Feedback & parents", "Draft one feedback comment bank (Chapter 7) and one parent message (Chapter 8)."],
        ["20-23", "Regional & admin", "Try one regional-language prompt (Chapter 9) and clear one admin job (Chapter 10)."],
        ["24-27", "The new curriculum", "Run one unplugged CT activity (Chapter 11) with your class. Note what worked."],
        ["28-30", "Make it a habit", "Build your personal \u2018My Prompts\u2019 document. Set aside 20 minutes every Friday for AI prep."],
    ],
    widths=[0.7, 1.1, 3.2])
d.callout("The one rule that makes all of this work",
          "Review everything. AI is a fast, tireless assistant that is occasionally confidently wrong. "
          "You are the teacher \u2014 that is the whole point, and it is the one thing AI cannot replace.")

# ======================= APPENDIX A =======================
d.h1("Appendix A \u2014 Master Prompt Index")
d.p("This toolkit contains %d numbered, copy-paste prompts across twelve teaching jobs. Use the "
    "chapter headings to jump to what you need:" % prompt_count)
d.bullet("Chapter 4 \u2014 Lesson Planning (20 prompts): from a 40-minute plan to an exit ticket.")
d.bullet("Chapter 5 \u2014 Question Papers & Assessment (20 prompts): blueprints, MCQ+HOTS sets, rubrics.")
d.bullet("Chapter 6 \u2014 Worksheets & Differentiation (14 prompts): three levels, one topic.")
d.bullet("Chapter 7 \u2014 Grading, Feedback & Rubrics (10 prompts).")
d.bullet("Chapter 8 \u2014 Parent Communication (12 prompts), including three Indian languages.")
d.bullet("Chapter 9 \u2014 Regional Language & Inclusion (8 prompts).")
d.bullet("Chapter 10 \u2014 Administration & Records (10 prompts).")
d.bullet("Chapter 11 \u2014 The New CT & AI Curriculum (10 prompts).")
d.bullet("Chapter 12 \u2014 Safety, Ethics & Integrity (6 prompts + the ten rules).")
d.p("Tip: number the prompts as you save them, and keep a one-line note of the class and subject "
    "you used each one for. Your index will become more valuable than the toolkit itself.")

# ======================= APPENDIX B =======================
d.h1("Appendix B \u2014 Tool Cheat Sheet")
d.p("Where to re-check before you rely on a number. AI prices and offers move fast \u2014 always confirm "
    "on the official page.")
d.table(
    ["What to check", "Official source"],
    [
        ["ChatGPT plans and India prices", "openai.com/chatgpt/pricing (and the ChatGPT app store listing)"],
        ["Gemini / Google AI plans and India prices", "gemini.google.com (Subscriptions, India)"],
        ["The Jio free Google AI Pro offer", "jio.com/google-gemini-offer (and the MyJio app)"],
        ["NotebookLM", "notebooklm.google.com"],
        ["Canva for Education (free for teachers)", "canva.com/education"],
        ["Bhashini (Indian-language tools)", "bhashini.gov.in"],
        ["CBSE CT & AI curriculum and circulars", "cbseacademic.nic.in"],
        ["NCERT textbooks", "ncert.nic.in"],
    ],
    widths=[1.5, 2.2])

# ======================= APPENDIX C =======================
d.h1("Appendix C \u2014 The 10 Verification Rules")
d.p("Print this page. It is the difference between a teacher who uses AI safely and one who gets "
    "burned by it.")
VER = [
 "Read the output before a student does. Every single time.",
 "For any fact, figure, date or rule, open the official source and confirm it.",
 "Add [VERIFY] to prompts about numbers, law and syllabus specifics.",
 "Never trust an AI answer about a board's pattern or marking scheme without checking the board's own paper.",
 "Keep your own copy of the source you checked.",
 "If a question looks wrong, it probably is \u2014 rewrite or drop it.",
 "Use the AI for the first draft, your expertise for the final one.",
 "Do not let AI write feedback that could hurt a child; read every comment as if the parent will see it.",
 "Check for bias and stereotypes in examples before you teach them.",
 "When in doubt, slow down. An error in a classroom costs more than the time you saved.",
]
for i, r in enumerate(VER, 1):
    d.numbered(i, r)
d.spacer(10)
d.callout("Thank you for teaching",
          "India runs one of the largest school systems in the world, and it runs on teachers. This "
          "toolkit exists to give you back time \u2014 for your students, your family and yourself. Use it "
          "well, review everything, and keep teaching like it matters. It does.")
d.p("Questions or feedback: lonefaisal977@gmail.com  \u00b7  WhatsApp +91 96826 00301  \u00b7  "
    "digitalkartai.shop", color=MUTED, size=9.4)

d.finish()
print("PDF written:", OUT)
print("Prompts included:", prompt_count)
print("Pages:", d.page)
