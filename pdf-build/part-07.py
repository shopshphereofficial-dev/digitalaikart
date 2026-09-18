story.append(P("17. Questions sellers actually ask", H1))
story.append(P("Can I sell online without GST?", H2))
story.append(P("On Meesho, yes, with an Enrolment ID - but only to buyers within your own state, and without access to ads. On Amazon and Flipkart, a GSTIN is mandatory for taxable goods from your first sale; the usual Rs 40 lakh turnover threshold does not apply to marketplace sellers. GST registration is free on the government portal and takes about 3-7 working days.", body))
story.append(P("Do I need to register a company?", H2))
story.append(P("No. Most small sellers operate as sole proprietors; the platforms only ask for GST/PAN and a bank account. Register a company later, when banks, brand deals or partners require it.", body))
story.append(P("How much money do I need to start?", H2))
story.append(P("A Meesho reseller can start with zero inventory. A small marketplace seller with 10-20 products and a modest ad budget can start meaningfully in the low tens of thousands of rupees - most of it stock, which is money that comes back as sales rather than fees.", body))
story.append(P("My product went out of stock mid-sale. Now what?", H2))
story.append(P("Pause its ads the moment you see two days of cover left, place the fastest replenishment you can afford, and keep the listing live with an availability date. A short gap costs less than a week-long delisting. Then write it in your post-mortem - the stockout is the season teaching you next year's reorder point.", body))
story.append(P("A competitor just went below my price. Should I follow?", H2))
story.append(P("Only down to the floor you computed in Chapter 7, never below it. You cannot control their costs, only your own losses. Below your floor, the rational move is to let them sell and take the traffic your reviews and dispatch speed earn instead.", body))
story.append(P("Are paid deal slots worth it?", H2))
story.append(P("When the listing converts - good images, healthy rating, proven demand - a deal slot is often the cheapest concentrated visibility you can buy. When the listing is weak, a deal is paying to send traffic to a closed shop. Fix the listing first; the 3:1 rule (Chapter 6) applies.", body))
story.append(P("When do I actually get paid?", H2))
story.append(P("Amazon: 7 days after delivery, on a 7-day cycle. Meesho: 7-day payment cycle from the delivery date. Flipkart: typically 7-15 days after delivery, longer for newer sellers. All three deduct fees, and marketplace TCS (1 percent) is withheld and credited back through your GST returns.", body))
story.append(P("Is it too late to register and still catch the season?", H2))
story.append(P("For the opening weekend, yes - and it does not matter. Register now and you arrive with listings, ratings and dispatch rhythm just as the Navratri-to-Diwali wave builds, which is the bigger window anyway. And the season after this one starts in January with the Republic Day sales; every platform habit you build now compounds.", body))
story.append(P("Can I really run this alone?", H2))
story.append(P("For a catalogue of a few dozen products, yes - Chapter 12's daily loop is a one-person job during the peak, and a family member covering dispatch and messages is the difference between surviving sale week and enjoying it. Beyond that, the first hire that pays for itself is someone who packs.", body))
story.append(P("What if the sale went badly - I discounted too deep and lost money?", H2))
story.append(P("Stop discounting immediately, hold your prices through the post-Diwali second wave, and sell your remaining stock at full margin there - it is the highest-margin window of the season precisely because everyone else has gone quiet. Then redo the Chapter 7 worksheet with your real numbers. Every seller has one bad festive season in them; the ones who have two are the ones who skipped the worksheet twice.", body))

story.append(P("18. The plain-English glossary", H1))
story.append(P("The festive-season conversations you will hear in seller groups and dashboards, translated.", lead))
story.append(CondPageBreak(4.2*inch))
story.append(table([
    ["Term", "What it means"],
    ["BBD / GIF", "Flipkart Big Billion Days / Amazon Great Indian Festival - the two flagship sale events"],
    ["SKU", "One distinct product in your catalogue (a red kurta in size M is its own SKU)"],
    ["MRP", "Maximum retail price printed on the product; your selling price is what you actually list at"],
    ["Contribution", "What a sale leaves you after GST, platform fees and product cost - the number Chapter 7 is about"],
    ["FBA / Flipkart Fulfilment", "Sending your stock to the platform's warehouse; they store, pack and ship, and you earn the badge"],
    ["Easy Ship / Ekart", "You store and pack, the platform's courier collects and delivers"],
    ["Prime / F-Assured badge", "The fast-delivery trust badge buyers filter by during sales"],
    ["NDD", "Next Day Dispatch - Meesho's program rewarding fast dispatch with visibility"],
    ["Buy Box", "The main 'Add to Cart' offer on a listing; on Amazon, competing sellers share one page"],
    ["TCS", "Tax collected at source - the 1% the platform deducts from your sales and credits back through your GST returns"],
    ["ITC", "Input tax credit - the GST you paid on purchases and platform fees, claimable against what you owe"],
    ["APOB", "Additional Place of Business - the GST registration you add when your stock sits in another state's warehouse"],
    ["HSN code", "The classification code that determines your product's GST slab and appears on every invoice"],
    ["Settlement", "The payout of a completed order to your bank account, after fees"],
    ["RTO", "Return to origin - a delivery that failed and came back, costing you both-way shipping"],
    ["ACoS / TACoS", "Ad spend as a share of the sales those ads produced - your ad efficiency yardstick"],
    ["GMV", "Gross merchandise value - total sales value on a platform, the headline number in festive news"],
    ["ONDC / SNP", "The Open Network for Digital Commerce, and the Seller Network Participant you join it through"],
    ["Dark store", "The small local warehouse a quick-commerce platform delivers from"],
], [0.26, 0.74]))

story.append(PageBreak())
story.append(P("Appendix: your festive worksheets", H1))
story.append(P("Photocopy these or rebuild them in a spreadsheet. Filled in honestly, they are the whole method of this playbook compressed onto three pages.", lead))
story.append(P("Worksheet 1: the price-floor sheet", H2))
story.append(P("For every product you plan to discount, fill one row before the sale starts. Use your platform's live fee calculator for the fees column at your intended price, not last year's numbers.", body))
story.append(table([
    ["Product", "Selling price (Rs)", "Output GST (Rs)", "Platform fees (Rs)", "Product + packaging cost (Rs)", "Contribution (Rs)", "My floor price (Rs)"],
    ["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""],
], [0.22, 0.13, 0.12, 0.14, 0.15, 0.12, 0.12]))
story.append(Spacer(1, 10))
story.append(P("Worksheet 2: the stock-planning sheet", H2))
story.append(P("One row per SKU. The multiplier is 2-4 times your recent daily average for hero products in a first festive season; use the lower end if you are unsure, because overstock outlives the season while a modest stockout only outlives the week.", body))
story.append(table([
    ["SKU", "30-day avg orders/day", "Multiplier", "Sale days", "Order qty", "To platform fulfilment", "My buffer", "Reorder point"],
    ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""],
], [0.18, 0.14, 0.10, 0.09, 0.10, 0.15, 0.11, 0.13]))
story.append(Spacer(1, 10))
story.append(P("Worksheet 3: the post-mortem half-page", H2))
story.append(P("Fill this in the last week of November and set a calendar reminder for next August with a photo of it attached. Next season starts with this page.", body))
story.append(table([
    ["Question", "Your answer"],
    ["Top 3 products by contribution (not revenue)", ""],
    ["The discount I regret", ""],
    ["The discount I cut too shallow", ""],
    ["What ran out, and when", ""],
    ["What is still on my shelf, and why", ""],
    ["What ads taught me about my buyers", ""],
    ["The one change for next September", ""],
], [0.46, 0.54]))

story.append(P("Sources and verification", H2))
story.append(P("This playbook was researched and verified on 18 September 2026 from: Flipkart's official Big Billion Days 2026 announcement (16 September 2026, confirming 8-9 October dates, member early access and bank offers); Amazon's official seller documentation at sell.amazon.in; Meesho's official supplier site (supplier.meesho.com); the ONDC network's official seller pages (ondc.org); Redseer Strategy Consultants' India Online Retail 2026 festive outlook (September 2026, as reported by The Hindu and on redseer.com); the Press Information Bureau's official releases on the GST 2.0 reforms (September 2025); and published 2026 Hindu festival calendars (regional dates for Navratri, Dussehra, Govardhan Puja, Bhai Dooj and Chhath vary by one day across regional traditions). Amazon's Great Indian Festival 2026 dates were not officially announced at the time of writing; the window stated here reflects reporting of Amazon's own assistant and three years of the event's history - confirm the date in Seller Central. Platform fees, commissions and policies change frequently: always verify current numbers in your own seller dashboard before pricing or committing stock. Nothing in this playbook is legal or tax advice; for your specific situation, consult a qualified professional.", body))

doc.multiBuild(story)
print("Built OK")
