    "Bhai Dooj gifting (10-11 November). Sibling gifts: small electronics accessories, personalised items, sweets combos. A quieter day with less competition, perfectly timed to sell your remaining gift stock.",
    "Post-Diwali home organisation (November). The second wave is not just electronics: after the festival comes the cleaning-and-storage surge. Storage boxes, organisers and kitchen racks sell into late November with almost no festive discounting.",
    "Winter layers (late November). Seasonal timing overlaps the festive tail: shawls, blankets and thermals for the north. This is how you turn Wave 4 into Wave 5 instead of ending your season on Bhai Dooj.",
]))
story.append(P("Notice what these ten have in common: they are all calendar-driven, so your money turns quickly; they are all giftable or bundleable, so order values rise without extra fees; and most are light, so shipping stays in the cheap weight slabs. That combination - fast turns, giftable, light - is the small seller's sweet spot this season.", body))

# ================= 4 =================
story.append(P("4. Choosing your channel: where a small seller actually wins", H1))
story.append(P("You do not need to be everywhere. You need to be excellent on one platform first, then expand. Spreading a small catalogue and a small budget across three platforms is how first-time sellers end up with three mediocre shops instead of one good one.", lead))
story.append(CondPageBreak(3.4*inch))
story.append(table([
    ["Channel", "Commission", "GST needed?", "Best for", "Money reaches you"],
    ["Amazon", "Referral fee varies by category (roughly 2-25%), plus closing and fulfilment fees",
     "GST or PAN to register", "Branded and premium products; tools (FBA, Sponsored ads) are the strongest in the market",
     "Paid 7 days after delivery, on a 7-day cycle"],
    ["Flipkart", "Category commission plus fixed, shipping and collection fees; registration is free",
     "GSTIN mandatory for taxable goods", "Value fashion, festive volume, Tier-2 reach; Big Billion Days is the volume event",
     "Typically 7-15 days after delivery"],
    ["Meesho", "0 percent commission", "No - sellers without a GSTIN can sell with an Enrolment ID (intra-state only)",
     "Unbranded, low-price, high-volume lines; the fastest legal way to start selling",
     "7-day payment cycle from delivery"],
    ["ONDC network", "Set by the seller app you join, commonly low single digits", "GSTIN generally expected",
     "Local shops and small brands wanting reach without a marketplace's take rate",
     "Varies by seller app"],
    ["WhatsApp / Instagram", "None (you run it)", "GST still legally applies to your sales", "Building a repeat customer base and festive gift hampers",
     "Instant, via UPI"],
], [0.13, 0.27, 0.17, 0.24, 0.19]))
story.append(Spacer(1, 6))
story.append(P("A few plain truths about each channel, from the platforms' own seller documentation.", body))
story.append(P("Amazon is the most complete machine and the most unforgiving. You can register with just a GST number (or PAN) and a bank account. Fulfilment by Amazon gets you the Prime badge, which matters most during the Great Indian Festival, when buyers filter for fast delivery. Amazon pays you 7 days after delivery on a 7-day cycle, and its fee structure varies by category - always run the fee preview in Seller Central before you price, never from memory.", body))
story.append(P("Flipkart reaches deep into smaller towns, and Big Billion Days delivers the single biggest order spike most Indian sellers see all year. Registration is free. The catch is GST: for taxable goods, a GSTIN is mandatory from your very first sale - the usual Rs 40 lakh turnover threshold does not apply to marketplace sellers, because selling through an e-commerce operator requires registration regardless of turnover. Flipkart deducts category commission plus fixed, shipping and collection fees, charges 18 percent GST on those fees (recoverable as input credit), and deducts 1 percent TCS (also recoverable when you file). Since late 2025 Flipkart has run zero commission on many products under Rs 1,000 - but commission slabs change, so check the live calculator in Seller Hub before pricing anything.", body))
story.append(P("Meesho is the honest starting point for a zero-budget seller. Zero commission, zero penalty for late dispatch or order cancellation (as of its current supplier terms), delivery to more than 28,000 pincodes, and a 7-day payment cycle from the delivery date. Sellers without a GSTIN can register with an Enrolment ID and sell within their own state - a legal testing ground before you formalise. Note that Meesho Ads and some visibility programs currently require a regular GSTIN, which is one more reason to get GST registered when you are ready to scale.", body))
story.append(P("ONDC - the government-backed Open Network for Digital Commerce - is not an app but a network: you join through a seller network participant, list once, and become discoverable across multiple buyer apps with your own store QR code to promote. Commissions are typically lower than marketplaces. It is worth a calm look after the season, not a panicked experiment during it.", body))
story.append(P("Fulfilment: the hidden channel decision", H2))
story.append(P("Each marketplace gives you three ways to deliver, and the choice changes your badges, your costs and your sleep.", body))
story.append(bullets([
    "Platform fulfilment (FBA on Amazon, Flipkart Fulfilment): you send stock to the platform's warehouse before the sale; they store, pack, ship and handle returns. You earn the Prime or F-Assured badge and the highest conversion. The risks are the stock-in cut-offs (warehouses stop accepting inbound inventory days before the event) and stock you cannot redeploy mid-sale if demand shows up somewhere else.",
    "Platform logistics, your warehouse (Amazon Easy Ship, Flipkart's standard flow with Ekart pickup): you store and pack, the platform's courier collects. The flexible middle path - your stock stays reachable, the badge is weaker.",
    "Self-ship: you handle storage, packing and couriering yourself. Maximum control, maximum work, and the weakest placement during a sale, when buyers filter for fast delivery.",
]))
story.append(P("A common festive pattern used by experienced sellers: commit about 60-70 percent of your forecast for hero SKUs to platform fulfilment and hold the rest in your own space as the buffer you can point at either marketplace mid-sale. Split that decision per product, not across your whole catalogue - long-tail items rarely justify warehouse stock.", body))
story.append(callout("The one-platform rule",
    "Lead with the platform that fits your product: Flipkart for value fashion and festive volume, Amazon for branded or premium items, Meesho for unbranded low-price lines. Get your first 25 reviews and your fulfilment rhythm on one platform, then add the second in the post-Diwali lull - not in the middle of the sale."))

# ================= 5 =================
story.append(P("5. Starting from zero this week: an honest plan", H1))
story.append(P("Read this chapter sitting down. If you are not already a registered seller, you will not be fully ready for the first day of the Great Indian Festival, and that is fine - the season runs eight more weeks after it. The profitable target for a brand-new seller is the Navratri-to-Diwali wave and the second wave after it, not the opening weekend.", lead))
story.append(P("Here is the realistic sequence. GST registration comes first for most routes: it is free on the GST portal, takes about 3-7 working days, and for marketplace sellers it is compulsory for taxable goods regardless of turnover. With your GSTIN in hand, Flipkart's onboarding typically clears in a day or two once documents match exactly - the most common rejection is a name that differs between GST records, PAN and bank details, so make them identical, spacing and punctuation included. Amazon needs your GST (or PAN) plus an active bank account. Meesho is the fastest door of all and will even take you without a GSTIN for intra-state selling while you wait for registration.", body))
story.append(bullets([
    "Days 1-7: GST application (if needed) and document hygiene - PAN, bank account in the business's name, pickup address, and product data cleaned up.",
    "Days 3-10: register on your chosen platform; list 10-20 products with genuinely good photos (white background, 1000x1000 pixels or better, multiple angles) rather than 200 rushed ones.",
    "Days 10-20: first orders, first dispatches, first reviews. Dispatch speed and photo quality are the two things a new seller fully controls.",
    "From mid-October: you arrive trained, with ratings, just as the Navratri-Diwali wave builds. That is your launch window, and it is the biggest one anyway.",
]))
story.append(P("Two traps to refuse. First, agencies offering 'guaranteed sale participation' for a fat fee this week - the platforms' own seller support and documentation are free, and most of what agencies sell at this stage is form-filling you can do yourself. Second, buying reviews or ratings. Platforms detect it, suspend accounts for it, and a suspension letter in October costs you the entire season.", body))
story.append(P("Set expectations with arithmetic, not dreams. A new seller with 15 decent listings, fast dispatch and a small ad budget should realistically target double-digit daily orders by Diwali week in a decent category - not ten thousand orders. The festive season compounds what you have built; it does not conjure a business from nothing.", body))

story.append(P("The paperwork table", H2))
story.append(CondPageBreak(2.6*inch))
story.append(table([
    ["Platform", "Register with", "Typical first listing", "Watch out for"],
    ["Amazon", "GST (or PAN) + active bank account", "A day or two after verification", "Fee preview before pricing; category approvals for gated lines"],
    ["Flipkart", "GSTIN, PAN, bank account, pickup address, digital signature", "Usually 1-2 days once documents match", "Name mismatches between GST, PAN and bank - the No.1 rejection cause"],
    ["Meesho", "GSTIN, or Enrolment ID for non-GST sellers (intra-state only)", "Often the same week", "Ads and some programs need a regular GSTIN; QC engine checks image quality"],
    ["ONDC (via a seller app)", "Business identity, bank details, catalogue, licences like FSSAI if category needs them", "Days to about a week via the seller app", "Costs and tools differ by seller app - compare before joining"],
], [0.14, 0.34, 0.22, 0.30]))

# ================= 6 =================
story.append(P("6. The final-fortnight sprint: T-14 to sale day", H1))
story.append(P("Everything that can be fixed before a sale opens is worth roughly twice what it is worth during the sale, because during the sale you have no time to fix it. Work this chapter backwards from your platform's opening day - for Big Billion Days that is 9 October, and if Amazon's festival opens in the reported late-September window, run this list against that date too.", lead))
story.append(P("T-14 to T-8: fix the shop window", H2))
story.append(numbered([
    "Audit every listing you plan to push. Title readable and keyword-honest, full attributes filled, at least 4-6 images, size and dimension data correct. One weak hero image costs more sales than a weak discount.",
    "Rewrite titles for festive search. Add the words people actually type in these weeks - 'gift', 'Diwali', 'Navratri', 'festive', 'puja' - only where they are true for your product. Keyword-stuffed titles depress clicks on mobile, which is where most sale traffic lives.",
    "Clean your account health. Check Seller Central or Seller Hub for pending issues, unresolved claims and listing-quality flags. A healthy account is a condition for running deals and promotions.",
    "Set your price floors now, with the worksheet in Chapter 7. Decide today the lowest price each product can go to during the sale - because on day two of the sale, at 11 pm, you will not do this math calmly.",
]))
story.append(P("T-7 to T-3: load the machine", H2))
story.append(numbered([
    "Submit deals and coupons through the platform's deal dashboard the moment the festive nomination window is open for your account - deal slots fill up and close before the sale, not during it. Every platform revises mechanics each year, so confirm current deadlines inside Seller Central and Seller Hub rather than from last year's blog posts.",
    "Allocate stock. Send bestsellers into platform fulfilment (FBA on Amazon, Flipkart Fulfilment) to earn the Prime and F-Assured badges, but hold 30-40 percent of your forecast in your own space as the buffer you can redirect mid-sale. Never commit stock to a warehouse you cannot replenish.",
    "Build your ad campaigns now, but leave them off. Separate festive campaigns from your everyday ones so you can control budgets and read results cleanly.",
    "Prepare your packaging and labels. Returns during festive weeks are high; strong packaging is a returns policy.",
]))
story.append(P("T-2 to T-0: final checks", H2))
story.append(numbered([
    "Freeze changes. No listing rewrites, no category moves, no pricing-structure experiments in the last 48 hours. Change one variable at a time, and change none during launch.",
