story.append(P("Choosing between deals, coupons and ads", H2))
story.append(CondPageBreak(2.6*inch))
story.append(table([
    ["Tool", "Use it when", "Cost and risk"],
    ["Platform deal slot", "You have a proven converter and want a velocity spike", "Fees per slot; a price below your floor loses money at scale"],
    ["Capped coupon", "You want visible extra discount with a spending cap you control", "Cheap; only pays out on redemption"],
    ["Sponsored ads", "Your listing converts but is invisible in search", "Flexible budget; wasted if the listing does not convert"],
    ["Bank offers", "Always - they cost you nothing", "None; they run on the platform's side"],
    ["Deep blanket price cut", "Almost never", "Cuts contribution by more than the discount, page after page"],
], [0.22, 0.40, 0.38]))

# ================= 9 =================
story.append(P("9. Ads on a small budget", H1))
story.append(P("You can run a serious festive ad campaign on Rs 300-800 a day if you respect one principle: advertise to convert, not to feel busy. This chapter is that principle made practical.", lead))
story.append(P("Start with automatic campaigns. Amazon's Sponsored Products auto campaigns and Flipkart's equivalent discover the search terms that actually convert for your product, at low bids. Let them run for 7-10 days before the sale, then lift the winning terms into exact-match manual campaigns where your money goes only to proven searches. This harvest-and-move pattern is the whole game; most small sellers skip the second step and keep paying discovery prices for proven terms.", body))
story.append(P("Budget shape matters more than budget size. A flat daily budget for a two-week sale wastes half of it on low-intent days. The shape that works:", body))
story.append(bullets([
    "Ramp from about T-7, at roughly half your intended daily spend, to build ranking history.",
    "Peak spend in the first 48 hours of the sale, when total market traffic is at its highest and ranks are being set.",
    "Second smaller peak at the weekend and again from Dhanteras through Diwali week (2-8 November).",
    "One sensible planning split used by experienced sellers: about 40-50 percent of the festive promo budget to ads weighted toward the ramp and opening 48 hours, 25-35 percent to discount funding, 10-20 percent held in reserve for mid-sale redeployment, and the rest to creative and content.",
]))
story.append(P("Every morning during the sale, look at exactly three numbers: spend, orders, and spend divided by orders. If a campaign's cost per order is under your target, raise its budget 20-30 percent. If it is double, pause it - do not 'give it more time to learn' during a sale; learning is for September, scaling is for October. Watch stock while you scale: the fastest way to torch a rank you paid for is to let an ad keep running after the product goes out of stock.", body))
story.append(P("A note on Meesho Ads and Flipkart's Product Listing Ads: the same harvest-and-move logic applies, and on Meesho remember ads currently require a regular GSTIN. Wherever you advertise, keep sale campaigns separate from everyday ones, or you will never know what the festival actually earned you.", body))

story.append(P("The only ad words you need to know", H2))
story.append(CondPageBreak(2.8*inch))
story.append(table([
    ["Term", "Plain meaning"],
    ["CPC (cost per click)", "What you pay each time someone taps your ad"],
    ["CTR (click-through rate)", "Share of people who see the ad and click. Low CTR usually means a weak image or title"],
    ["Orders / conversion", "Share of clicks that turn into purchases. If clicks are fine but orders are not, fix the listing, not the ad"],
    ["Cost per order", "Ad spend divided by orders. Your daily steering number"],
    ["ACoS / TACoS", "Ad spend as a share of the sales the ads produced (total ad cost over total sales for the wider view). Lower is better once a campaign matures"],
    ["Auto vs manual campaigns", "Auto lets the platform find your search terms; manual targets exact terms you choose. Harvest from the first, scale with the second"],
], [0.26, 0.74]))

story.append(P("Your first Rs 500: a 7-day starter plan", H2))
story.append(P("If ad money is tight, run the smallest honest experiment that teaches you something. Take Rs 500 and one hero product. Day 1-3: Rs 60 a day on an auto campaign, low bids, watching which search terms convert. Day 4: pause the auto campaign, take the two or three search terms that produced orders, and start a manual exact-match campaign at Rs 100 a day on those terms alone. Day 5-7: raise the winner's budget 20 percent a day while its cost per order stays under your Chapter 7 contribution; pause anything that doubles it. That Rs 500 bought you the exact words your buyers use - intelligence you can reuse across every platform, in your titles, in your WhatsApp posts, next season. Scale from knowledge, not hope.", body))

# ================= 10 =================
story.append(P("10. GST 2.0 essentials for festive sellers", H1))
story.append(P("India's GST structure was overhauled in September 2025 into what everyone now calls GST 2.0: two main slabs - 5 percent and 18 percent - plus a 40 percent rate for sin and luxury goods, effective from 22 September 2025. For a festive seller this matters twice over: it changes what your customers pay, and it sets your invoicing arithmetic.", lead))
story.append(P("What moved (from the official announcements):", body))
story.append(bullets([
    "Household essentials - soaps, shampoos, toothpaste, toothbrushes, tableware and kitchenware, bicycles - came down to 5 percent.",
    "Most packaged foods moved to 5 percent: namkeens, bhujia, chocolates, biscuits, pasta, sauces, ice cream, nuts like almonds and dates.",
    "Big-ticket festive categories came down from 28 to 18 percent: TVs above 32 inches, air conditioners, dishwashers, cement; small cars and two-wheelers up to 350cc likewise.",
    "Up at 40 percent: tobacco, pan masala, aerated drinks and luxury goods.",
]))
story.append(P("Why this matters to your festive plan: several categories got a demand tailwind, because post-GST-2.0 price cuts landed on the same goods that sell during the festival. If you sell in electronics, appliances or packaged food, your pricing conversations this season are happening against visibly lower MRPs on some goods. Your own GST rate determines your invoice arithmetic - know your product's exact slab before you set any price.", body))
story.append(P("The four compliance rules a marketplace seller must not fumble:", body))
story.append(numbered([
    "GST registration is mandatory for taxable goods sold through a marketplace, from your very first sale - the normal Rs 40 lakh turnover threshold does not apply to e-commerce sellers (Section 24 of the CGST Act). Composition scheme is not available on marketplaces.",
    "Platforms deduct 1 percent TCS on your taxable sales and deposit it with the government. It shows up in your GST returns as credit - money blocked until you file, not money lost. Reconcile it every month; unmatched TCS is the most common reason sellers overpay tax.",
    "Platform fees carry 18 percent GST, which you can claim as input credit. Download the platform's monthly GST invoices from your seller dashboard and book them - most small sellers leave this money on the table every single month.",
    "If you send stock into a platform warehouse in another state (FBA or Flipkart Fulfilment), that state becomes an Additional Place of Business for GST purposes and typically needs its own registration. Sellers discover this the hard way when stock sits unshippable in a warehouse awaiting an APOB clearance.",
]))
story.append(P("During the sale itself, your invoicing volume can jump 5-10 times for days at a stretch. The preparation is boring and worth it: correct HSN codes on every listing now, an invoice format that matches your GSTIN details, and a nightly reconciliation habit so that the November filing season is a formality instead of an emergency. If you are not already filing through a simple software or a filing service, budget for one before Diwali; it costs a few hundred rupees a month and repays itself in one avoided penalty.", body))

story.append(P("Your monthly GST rhythm as a marketplace seller", H2))
story.append(P("The dates are fixed and unforgiving; the work is easy if it is routine. For monthly filers: GSTR-1 (your outward sales detail, where the month's sales must match what the platforms report) is due by the 11th of the following month, and GSTR-3B (the return where you actually pay) by the 20th. Smaller taxpayers can opt for the quarterly QRMP scheme - check current eligibility on the GST portal. Put both dates in your phone's calendar now, with a reminder three days before each. During festive months, block the hour in advance: October's sales volume is what makes November's filing a job instead of a formality.", body))

# ================= 11 =================
story.append(P("11. Cash flow: the part of the festive season nobody photographs", H1))
story.append(P("Festive season cash flow is a timing mismatch: your suppliers, your GST liability and your ad platform all take money on schedule, while your sales revenue arrives on the platform's settlement calendar. Amazon pays 7 days after delivery on a 7-day cycle; Meesho runs a 7-day payment cycle from the delivery date; Flipkart settlements typically run 7-15 days after delivery, longer for new sellers. Returns add another lag - a returned order can hold up settlement for weeks.", lead))
story.append(P("Run the timing on a worst-case sale week. An order placed on Big Billion Day, delivered on day 5, returned on day 10, settles perhaps a fortnight after that - while the GST on the original sale and the next month's ad spend are already due. Multiply by a hundred orders and you can have a 'record month' on the dashboard and an empty bank account in real life. Sellers describe this as the festive cash crunch for a reason; it is structural, and it is survivable with two habits.", body))
story.append(bullets([
    "Reserve before you spend. Set aside your estimated GST liability (roughly the GST component of your festive sales, minus input credits) in a separate account the week the sales happen. Every rupee of GST you collect belongs to the government; spending it in October makes November a crisis.",
    "Hold a working-capital cushion of one full reorder of your hero SKU, separate from your ad budget. The mid-sale reorder - placed when your bestseller is selling out - is the highest-return decision of the season, and it is exactly the moment sellers discover they cannot pay their supplier.",
]))
story.append(P("Two more timing details worth their own paragraph. Many suppliers offer festive stock on advance payment and raise prices as demand tightens - locking your replenishment price before October is as valuable as any discount you will offer. And platforms run festive-period policy changes (longer returns windows on some categories, changed payouts during events); the announcements sit in your seller dashboard's notifications, which is a tab worth opening once a week this season even when nothing seems wrong.", body))
story.append(callout("The 3-account rule",
    "If you do one thing from this chapter: split your money into three accounts - one for receiving settlements, one for GST you have collected but not yet paid, one for operations. Move money between them deliberately, weekly. When the season ends you will know exactly what you earned, what you owe, and what you can reinvest."))

story.append(P("A cash-flow timeline you can feel", H2))
story.append(CondPageBreak(2.6*inch))
story.append(table([
    ["Date", "Event", "Money in / out"],
    ["9 Oct", "Big Billion Day order, 300 units of your hero SKU", "Nothing in yet"],
    ["10 Oct", "You pay your supplier for the mid-sale reorder", "Out: reorder cost, from your cushion"],
    ["14-18 Oct", "Deliveries complete", "Nothing in yet - settlement clock starts per order"],
    ["21-25 Oct", "Settlements begin landing (7 days after each delivery)", "In: first payouts, minus fees and 1% TCS"],
    ["11 Nov", "GSTR-1 for October due", "Paperwork: sales reported, must match platform data"],
    ["20 Nov", "GSTR-3B due: GST on October sales payable", "Out: the GST you collected in October, minus input credits"],
], [0.12, 0.52, 0.36]))
story.append(Spacer(1, 6))
story.append(P("Look at the gap between 10 October and 25 October: two weeks where you have paid suppliers, run ads and shipped hundreds of orders before the first significant money arrives. That gap is the festive cash crunch in one table - and the reason Chapter 11's two habits (GST reserve, reorder cushion) exist.", body))

# ================= 12 =================
story.append(P("12. Sale week: running the shop while it is on fire", H1))
story.append(P("Sale week is an operations job with a marketing rhythm. Here is the daily loop that works for a one-person or small team.", lead))
story.append(numbered([
    "Morning (first hour): check overnight orders and stock. If any hero SKU is below two days of cover at current velocity, place the reorder or throttle its ads immediately. A stockout mid-sale does not just cost the day's sales - it resets the ranking you spent weeks building, and Flipkart's ranking in particular punishes a promoted product that goes unavailable.",
