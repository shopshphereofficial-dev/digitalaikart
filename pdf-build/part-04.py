    "Ramp ads from about T-7 rather than T-1. Ranking signals take days to register; a budget switched on the night before buys traffic without buying position.",
    "Charge your phone, brief your family, stock your kitchen. Sale week is a shift job. The sellers who win are simply the ones who show up every hour of it.",
]))
story.append(callout("The 3:1 rule for your first festive sale",
    "For every hour you plan to spend 'promoting', spend three hours making the listing worth buying: photos, title, reviews, dispatch speed, packaging. Sellers invert this ratio, buy ads to a bad listing, and call the season a failure. The product page is the conversion machine; ads are just the hose."))

story.append(P("The 10-point listing audit", H2))
story.append(P("Run this on every product you plan to push during the sale. It takes about ten minutes per listing and pays for itself with the first order.", body))
story.append(numbered([
    "Title: readable first, keyword-honest second. A buyer should understand what you sell from the title alone, on a phone screen, in two seconds.",
    "Images: at least 4-6 per product. Main image clean and uncluttered (marketplaces commonly require a plain white background for the main image and check this automatically); the rest showing scale, details, packaging and use.",
    "Image size: high resolution - 1000 pixels or more per side, so buyers can zoom. Blurry zoom is a silent conversion killer.",
    "Attributes: every field filled - size, material, colour, dimensions, what is in the box. Blank fields suppress you in filtered searches.",
    "Measurements in the photos and the text. Returns start with surprise; measurements prevent surprise.",
    "Description written for the buyer's objections: how it is used, what it is made of, what arrives and what does not.",
    "HSN code and GST slab correct, so your invoicing and the platform's reports match in November.",
    "Stock counts accurate in the system, not in your head. Mid-sale, the listing says what the system says.",
    "Price history consistent: a listing that jumps between wildly different prices invites price-history flags on some platforms; plan your festive price and hold it cleanly.",
    "Questions in the Q&A answered. Unanswered questions on a festive listing read like an abandoned shop.",
]))
story.append(P("Photography on a phone", H2))
story.append(P("Product photos are the closest a marketplace buyer gets to holding your product, and a phone is enough to take good ones. The recipe: shoot near a window in daylight (never under a yellow bulb), tape a plain white sheet as the backdrop for the main image, keep the phone steady and tap to focus, shoot from eight angles - front, back, top, inside, scale reference next to a common object, in use, packaging, and what is in the box - and reject anything slightly blurry. Edit only for brightness and crop, never for colour that misrepresents the product, because returns punish flattery. Two hours of shooting produces a season of listings.", body))
story.append(P("How much stock to buy: a five-step method", H2))
story.append(numbered([
    "Write your average daily orders per product over the last 30 days. New listing? Use your best comparable product's number, or a conservative one per day.",
    "Pick a festive multiplier for the sale weeks. For a first festive season, plan 2-4 times your daily average on hero products - platforms and agencies report festive-day spikes several times higher than normal, but overstocking is the more expensive error for a small seller.",
    "Multiply, add the days you expect to sell, and subtract what you already hold. That is your order quantity.",
    "Split it: roughly 60-70 percent into platform fulfilment for the badge, the rest in your own space as the mid-sale buffer you can redirect.",
    "Write your reorder point now: when stock on hand falls below (supplier lead time in days x expected daily sales), order. During the sale you will not have the peace of mind to do this arithmetic, so do it today.",
]))
story.append(P("The sprint on one page", H2))
story.append(CondPageBreak(3.2*inch))
story.append(table([
    ["Days out", "Action", "Why it matters"],
    ["T-14 to T-10", "Listing audit: titles, attributes, 4-6 images, HSN codes", "Listing quality feeds ranking and deal eligibility"],
    ["T-12", "Account health check; clear pending claims and flags", "A healthy account is a condition for running deals"],
    ["T-10", "Compute and write down price floors per product (Ch. 7)", "The decision made calmly now saves panic at 11 pm on sale day"],
    ["T-8", "Submit deal nominations and set capped coupons", "Deal slots close before the sale begins, not during it"],
    ["T-7", "Stock into platform warehouses for hero SKUs; buffer at home", "Stock-in cut-offs and slow warehouse check-in make late arrival risky"],
    ["T-7", "Switch ad ramp on at half your intended daily budget", "Ranking signals need days to register before the sale"],
    ["T-3", "Build sale campaigns separate from evergreen ones; keep paused", "Clean read on what the festival itself earned"],
    ["T-1", "Freeze all changes; verify every promotion is configured correctly", "Misconfigured promotions are the classic day-one horror"],
    ["T-0", "First hour: verify every deal, coupon and price is live and correct", "The platform will not fix it for you"],
], [0.13, 0.42, 0.45]))

# ================= 7 =================
story.append(P("7. Pricing that survives the sale: the contribution floor", H1))
story.append(P("The festive season is where margins go to die, because discounts stack multiplicatively while your costs barely move. The single most valuable 30 minutes you will spend this fortnight is computing the floor price of each product you plan to discount. Here is the method.", lead))
story.append(P("Your floor is the price at which contribution - what is left of the sale price after GST, platform fees and product cost - still clears a minimum you set. Not MRP minus 30 percent; the number the fees leave for you.", body))
story.append(P("A worked example (illustrative numbers - your category, weight slab and fees will differ; recompute with your platform's live fee calculator):", body))
story.append(CondPageBreak(3.6*inch))
story.append(table([
    ["Line item", "Sale price A (Rs 799)", "10% off (Rs 719)", "20% off (Rs 639)"],
    ["Selling price (incl. 5% GST)", "799", "719", "639"],
    ["Output GST to government (5%)", "-38", "-34", "-30"],
    ["Commission (12%)", "-96", "-86", "-77"],
    ["Fixed/closing fee", "-15", "-15", "-15"],
    ["Shipping (weight slab)", "-70", "-70", "-70"],
    ["Collection fee (2%)", "-16", "-14", "-13"],
    ["GST on platform fees (18%)", "-35", "-33", "-31"],
    ["Product cost + packaging", "-345", "-345", "-345"],
    ["Money left per order (contribution)", "184 (23%)", "122 (17%)", "58 (9%)"],
], [0.40, 0.20, 0.20, 0.20]))
story.append(Spacer(1, 6))
story.append(P("Read the last row twice. A 20 percent discount did not cut your profit by 20 percent - it cut it by about 70 percent, because commission, shipping and fees shrink only slightly while product cost stays fixed. At Rs 639 you are working for Rs 58 an order; one return, which costs you two-way shipping, erases the profit of four sales.", body))
story.append(P("Now the practical rules that fall out of this arithmetic.", body))
story.append(bullets([
    "Set each product's floor before the sale, write it on a sheet next to your desk, and treat it as law. When a competitor drops below your floor during the sale, let them - you cannot win a race to the bottom, only finish it.",
    "Prefer coupons over blanket price cuts. A coupon is visible to buyers as a discount but lets you keep the list price intact for later, control the budget (coupons can be capped), and switch it off when the cap is hit.",
    "One hero deal beats ten shallow ones. The platform's ranking systems reward products with a spike of sales velocity; a deep, well-advertised deal on one product lifts its rank, and its halo lifts your other listings.",
    "Remember the recovery items. The 18 percent GST on platform fees and the 1 percent TCS come back to you as input credit when you file - but with a lag, which is exactly why Chapter 11 exists.",
    "Watch price parity. Amazon and Flipkart both care whether your price on their platform is higher than elsewhere; a price that undercuts them on your own channels can cost you visibility on theirs.",
]))
story.append(callout("The worksheet",
    "For each product write five numbers: selling price, output GST rate, total platform fees (from the live calculator, at your intended price), product plus packaging cost, and the contribution that remains. Then write the floor: the price at which contribution hits the minimum you will accept - many small sellers use 10-15 percent during festive weeks. Products that cannot clear the floor at a competitive price are not sale products; sell them at full price to the post-Diwali wave instead."))

story.append(P("A second example, on Meesho's zero commission", H2))
story.append(P("The same method on a Rs 499 gift hamper with Meesho's 0 percent commission shows why channel choice is a pricing decision. Output GST at 5 percent is about Rs 24; Meesho's shipping (weight-based, shown to you before you price) runs about Rs 60 plus GST; the hamper costs you Rs 260 to assemble. That leaves roughly Rs 144 per order - about 29 percent contribution - before any ad spend. The margin you keep by choosing the right channel for the right product is often larger than the margin you can ever win by discounting harder on the wrong one.", body))
story.append(P("How discounts stack with bank offers", H2))
story.append(P("Bank offers cut the price the customer pays without cutting your payout - the bank funds the difference. Stack deliberately:", body))
story.append(CondPageBreak(2.4*inch))
story.append(table([
    ["", "Example numbers (Rs)"],
    ["Your list price", "999"],
    ["Your festive discount (10%)", "899"],
    ["Bank offer during the sale (10%)", "Customer pays about 809"],
    ["Your settlement (based on your price of 899)", "Computed on 899, not 809"],
], [0.60, 0.40]))
story.append(Spacer(1, 6))
story.append(P("So when Big Billion Days runs a 10 percent Axis or ICICI instant discount, you do not need to match it from your own margin - your 10 percent plus the bank's 10 percent lands the customer at roughly 20 percent off while your payout is computed on your price. This is the cheapest deep discount you will ever offer; use it on hero products where the psychological price point matters.", body))

# ================= 8 =================
story.append(P("8. Deals, coupons and badges", H1))
story.append(P("Buying visibility during the big sales is cheaper than earning it, if you use the platform's own machinery. The machinery is deals, coupons and badges - here is how they fit together.", lead))
story.append(P("Deals are the platform's discounted showcase slots. Amazon runs Lightning Deals and event-long deals with a fee per deal slot; Flipkart runs its own deal nominations through Seller Hub. Two facts decide your deal strategy. First, deal nominations open weeks before the event and close when slots fill - if you are reading this in late September, check your deal dashboard today, not tomorrow. Second, a deal is a bet on velocity: the platform gives you placement, you give up margin, and the payoff only works if your listing converts the traffic - which brings you back to photos and reviews.", body))
story.append(P("Coupons are the disciplined cousin. A capped coupon - '10% off, first 500 redemptions' - shows the same discount to the buyer while capping your total spend and keeping your list price intact. During the sale, coupons stack on platform bank offers (this year's Big Billion Days includes 10 percent instant discounts on Axis and ICICI cards plus member discounts), so your 10 percent coupon rides a 20 percent bank offer into a much bigger effective discount at no extra cost to you. This is the cheapest visibility you will buy all year.", body))
story.append(P("Badges are silent conversion boosters, and you qualify for them through operations, not money:", body))
story.append(bullets([
    "Prime (Amazon) and F-Assured (Flipkart) come from platform fulfilment - send your hero SKUs into FBA and Flipkart warehouses before the sale's stock-in cut-off. Both platforms stop accepting inbound stock ahead of the event; the cut-off for the Great Indian Festival falls in the days just before opening, and warehouse check-in slows badly in the final week, so land your stock early.",
    "Next Day Dispatch on Meesho - a seller's best free visibility lever - is earned by dispatch discipline in the weeks before the sale. Start treating your dispatch SLA as a marketing channel now.",
    "A 4.0-plus star rating is a de facto deal-eligibility requirement. Chase honest reviews in September, when each one is cheap to earn, rather than in October when it is too late to matter.",
]))
story.append(callout("The one deal to refuse",
    "Never fund a deal with a price below your Chapter 7 floor 'because it is good visibility'. Visibility that loses money per unit scales your losses at sale speed. If the deal the platform suggests is below floor, counter with a smaller discount plus a coupon, or decline the slot and let ads do the work."))

