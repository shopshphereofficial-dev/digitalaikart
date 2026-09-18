    "Morning (second hour): read last day's numbers - spend, orders, cost per order, returns started. Move ad budgets up or down by the rules in Chapter 9. Pause, never delete: you want the history.",
    "Midday: dispatch. Aim to clear every order placed before your platform's same-day cut-off. Dispatch speed feeds the badges (Chapter 8) and the reviews (Chapter 13).",
    "Afternoon: customer questions. Sale-week buyers message before they buy, and the first seller to answer usually wins the order. Check the Q&A section on your listings too.",
    "Night: tomorrow's pricing and coupon check. Verify every promotion is live and correctly priced - misconfigured promotions are the classic day-one horror story, in both directions: a discount that did not switch on, or one that switched on deeper than your floor.",
]))
story.append(P("On returns, prevention beats processing. Most festive returns come from expectation mismatch, which means they come from lazy listings: wrong dimensions, flattering-but-dishonest photos, missing 'what's in the box' details. Fix the listing, and the return rate follows. When returns do arrive, process them daily - a pending return blocks settlement and, on some categories, re-saleable stock during the highest-demand fortnight of the year.", body))
story.append(P("Protect your sanity with one rule: no structural changes during the sale. No new categories, no redesigns, no platform experiments. You are running a shop during a stampede; your only jobs are stock, speed, answers and arithmetic.", body))

story.append(P("When things go wrong during the sale", H2))
story.append(CondPageBreak(2.8*inch))
story.append(table([
    ["What happened", "Your first response"],
    ["A deal did not go live at launch", "Check the deal dashboard for rejection or eligibility reasons; convert to a capped coupon immediately so the day is not lost"],
    ["A listing got suppressed", "Open Seller Central / Seller Hub support chat at once; suppressed listings are usually a compliance flag (image, claim, category) fixed in minutes if caught early"],
    ["Hero SKU went out of stock", "Pause its ads immediately, request the fastest replenishment, and keep the listing active with an expected-availability date rather than delisting"],
    ["A price glitch (too deep or too shallow)", "Fix the price, then verify from the buyer side (app, not dashboard). Report platform-side display errors through support the same hour"],
    ["Courier pickup missed", "Rebook for the earliest slot and inform affected buyers through the platform's messaging - silence creates the complaints, not the delay"],
    ["Account health dropped", "Read the specific metric, fix the underlying orders or claims, and reply to the notification - health issues fester when ignored, and recover fast when addressed"],
], [0.34, 0.66]))

# ================= 13 =================
story.append(P("13. The Diwali second wave and the post-sale fortnight", H1))
story.append(P("Here is the pattern most sellers miss: the sale events end, everyone goes quiet, and then India keeps buying. Redseer documented a dual-peak in recent festive seasons - a second wave of purchases after Diwali, led by high-ticket items, as buyers who deferred during the sale rush return with their wallets, and as delivery delays push some purchases past the festival itself. The post-Diwali fortnight is the highest-margin selling window of the season precisely because most of your competition has gone home.", lead))
story.append(P("So plan Wave 4 explicitly:", body))
story.append(bullets([
    "Hold your prices (or most of them) through mid-November. The deep-discount pressure ends with the platform events; buyers in the second wave are choosing on availability and trust, not on the last rupee.",
    "Keep a modest ad budget running - cost per click typically falls after the sales end, while buying intent for Dhanteras, Diwali, Bhai Dooj and Chhath (14-15 November) continues.",
    "Bank the reviews. The fortnight after a sale is when your buyers write them, if you ask. A short, polite, honest review request inside the platform's own messaging - not SMS spam - converts best right after delivery. Every review earned now is free ranking for next season.",
    "Clear returns and reconciliations fast, while records are fresh. This is also when you download your sale reports and capture the data this playbook keeps asking you for: which products earned their margin, which ads paid, which dates delivered.",
]))
story.append(P("Then do the quiet post-mortem that turns one good season into a business. Half a page is enough: top 3 products by contribution (not revenue), the one discount you regret, the one you under-cut, stock you ran out of, stock you still hold, and the single change you will make next September. Put a calendar reminder for next August with that page attached. The sellers who dominate a festive season are the ones who took notes in the previous one.", body))
story.append(P("And a word for the end of the tunnel: 20-25 November. The season is over, the second wave has passed, and what remains is your actual business - ideally with a customer list, better rankings, cleaner listings and more reviews than you started with, plus cash reserves that survived GST week. That is what winning the festive season means. Not the biggest sales chart. The strongest January.", body))

story.append(P("Two review messages that work (edit to your voice)", H2))
story.append(callout("After a smooth delivery",
    "Namaste! Your order was delivered today - thank you for buying from our small business. If everything arrived as expected, a two-line review on the listing genuinely helps a seller like us. If anything is not right, please message us here first and we will fix it. - Happy Diwali!"))
story.append(Spacer(1, 4))
story.append(callout("After the festive rush",
    "Thank you for shopping with us this festive season. If a moment of your time is possible, your honest review helps other buyers find us. We are a small team, and every review matters. Wishing you and your family a wonderful season ahead."))

# ================= 14 =================
story.append(P("14. Quick commerce and ONDC: should you bother this season?", H1))
story.append(P("Quick commerce is the growth story of 2026 - festive sales on the channel are projected to grow 110-120 percent, taking roughly 18 percent of all festive online sales. Should a small seller chase it in the next three weeks? Usually, no - and here is the honest reasoning.", lead))
story.append(P("Quick-commerce platforms (Blinkit, Zepto, Swiggy Instamart and others) are not open marketplaces. They typically buy your inventory through purchase orders, stock it in their dark stores and sell it themselves; you are a supplier fulfilling a category manager's forecast. Onboarding a new brand generally runs several weeks - entity documentation, brand and trademark checks, state-wise GST registrations for the states you supply, and commercial terms that usually include commissions and deposit models for newer brands. Starting that process in mid-September means arriving after Diwali. If quick commerce is your plan, start the conversation now for a post-season or next-festive launch - and remember you need working capital to fulfil purchase orders ahead of payment, not after a sale like a marketplace.", body))
story.append(P("What you can do this season with zero onboarding: sell the categories quick commerce has made habitual. The 10-minute apps have trained a large slice of India to expect festive and gifting items delivered fast - impulse sweets, small gifts, puja items, decor. If your marketplace listings cover these and you dispatch same-day, you are already catching the demand the apps created.", body))
story.append(P("ONDC, the government-backed open network, is the calmer long-term play for a small seller. You join through a seller network participant (many offer simple app-based onboarding, some with Hindi-first flows), list once, and become visible across multiple buyer apps, with your own store QR code to share on WhatsApp and print at your shop. Costs and commissions are set by the seller app you choose and are typically lower than the big marketplaces. The Ministry of MSME also runs support programs for small enterprises joining digital commerce through ONDC under its RAMP programme - check current eligibility and details on the official MSME and ONDC portals rather than through agents. The realistic note: ONDC volumes per seller are still smaller than the marketplaces', so treat it as a second channel with better economics, not a replacement - and set it up in the quiet weeks, not now.", body))

# ================= 15 =================
story.append(P("15. Selling on WhatsApp and Instagram this festive season", H1))
story.append(P("Marketplaces bring strangers; WhatsApp and Instagram bring people who already know you. For gifting, hampers, customised orders and local delivery, these channels earn the best margin in Indian small business - no commission, no ads (unless you choose them), and payment by UPI reaching you the same minute. The festive season is when this channel earns its keep, because gifting demand is personal, last-minute and word-of-mouth.", lead))
story.append(P("Set the shop up properly once, and it runs all season:", body))
story.append(bullets([
    "WhatsApp Business (the free app, not a personal account): a complete profile with your catalogue of festive products, quick replies for the ten questions everyone asks, labels to track orders (New, Paid, Shipped, Done), and an away message for the hours you are packing orders.",
    "Status as your storefront: post daily - what shipped today, what is new, how many of last year's gift boxes are left. Status disappears in 24 hours, which makes urgency honest instead of manufactured.",
    "Broadcast lists, not groups: a broadcast message reaches each customer individually (and only if they have saved your number), without exposing your customer list to each other. Build your lists now - every marketplace buyer who has messaged you is a candidate.",
    "Payments: share your UPI ID or QR with every order. Money arriving instantly is your working capital during the settlement-lag weeks of Chapter 11.",
    "Instagram, simply: switch to a professional account, keep 6-9 festive posts alive in a highlight called 'Festive 2026', and reply to every comment and DM as if it were a shop counter - because it is.",
]))
story.append(P("Two cautions. Every rule that applies to a marketplace applies here too: GST on your sales is due regardless of channel, and food sellers still need their FSSAI licence. And keep records - a simple spreadsheet of orders, or a small invoicing app - because October memory does not survive to November filing.", body))
story.append(callout("The channel-stacking plan",
    "The strongest small-seller combination this season: marketplaces for discovery volume, WhatsApp-Instagram for repeat customers and hampers. Every marketplace order ships with a small card carrying your WhatsApp number. The marketplace finds the customer once; the WhatsApp channel keeps them forever - at zero commission."))


story.append(P("16. Master checklists", H1))
story.append(P("Print this chapter or keep it open on a second screen through the season. Each list is deliberately short enough to actually finish.", lead))
story.append(P("Before the sales open (this week)", H2))
story.append(numbered([
    "Festive calendar saved, with my platform's confirmed dates and stock-in cut-offs marked.",
    "Deal nominations submitted in Seller Central / Seller Hub; coupon budgets and caps set.",
    "Price floor computed per product (Chapter 7) and written where I can see it.",
    "Hero SKUs into platform fulfilment; 30-40 percent of forecast held in my own buffer.",
    "Ads: auto campaigns harvesting since T-7; manual exact-match campaigns built and paused.",
    "Account health clean; listings audited (title, attributes, 4-6 images, HSN codes correct).",
    "GST account reconciled through last month; TCS and platform-fee credits claimed.",
    "Three accounts set up: settlements, GST reserve, operations.",
    "Supplier reorder prices locked for a mid-sale replenishment.",
]))
story.append(P("During the sale (daily loop)", H2))
story.append(numbered([
    "Stock check on hero SKUs; reorder or throttle ads if under two days of cover.",
    "Yesterday's numbers read: spend, orders, cost per order; budgets adjusted.",
    "Every order before cut-off dispatched; tracking updated.",
    "Buyer messages and Q&A answered.",
    "Every promotion verified live and correctly priced.",
    "Returns processed; no return sitting unactioned overnight.",
    "End of day: two-line journal - what sold, what surprised me.",
]))
story.append(P("After Diwali (the second wave and the wind-down)", H2))
story.append(numbered([
    "Prices held through mid-November; ads still on, at a lower budget.",
    "Review requests sent inside the platform after each delivery.",
    "Sale reports downloaded; contribution (not revenue) computed per product.",
    "TCS and input credits reconciled; GST return filed on time.",
    "Post-mortem half-page written; calendar reminder set for next August.",
    "Next season's first decision made: which channel to deepen, which to drop.",
]))
story.append(Spacer(1, 10))
story.append(goldline())
story.append(Spacer(1, 6))
