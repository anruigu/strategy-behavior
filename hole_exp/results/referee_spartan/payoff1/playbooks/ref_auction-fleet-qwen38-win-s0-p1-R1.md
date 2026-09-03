---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2997
---
# Playbook

**Budget tracking.** I start with a stated budget. I only subtract from it when I actually win a lot (i.e., I'm the high bidder at the end of the lot). I never subtract when I merely place a bid that someone outbids. Every time I report my budget, I compute: starting budget minus the sum of all lot prices I have won so far. I do not add, I do not guess, I do not carry forward a number I didn't derive. If I'm uncertain, I recount from the results shown to me.

**Opening a lot when no one has bid.** I open at the minimum raise, not at a "competitive" level. The minimum raise is the cheapest way to signal interest. If no one else is bidding, I win at the minimum. If someone does bid, I have a full second round to respond. Opening high just locks in a higher price for no benefit.

**Round 1 of a contested lot.** If the current high bid is below my value, I bid the minimum raise to stay in the auction. I do not bid above the minimum raise in round 1 unless the lot is worth so much more than the current price that even a large raise still leaves a strong surplus. Bidding high in round 1 just raises the floor for round 2.

**Round 2 (final round) when I want to win.** I bid exactly the minimum raise. This is the last chance, so I commit, but I commit at the lowest legal price. If the minimum raise exceeds my value, I pass without hesitation.

**Round 1 when I want to win but the margin is thin.** If my value is only slightly above the current bid (e.g., within one or two minimum raises), I bid the minimum raise and accept that I may lose. I do not overbid in round 1 to "apply pressure" — that just raises the final price if the opponent calls.

**When to pass.** I pass when the minimum raise would put my price at or above my value. I also pass when the lot's value to me is low relative to my remaining budget and I suspect better-value lots are still ahead.

**Budget allocation across lots.** I track my remaining budget after each won lot. Before bidding on a new lot, I check: if I win this at the likely final price, do I still have enough left for future lots I expect to want? If the answer is no, I bid more conservatively or pass.

**What did not work in my last play:**
- I reported budgets that were nonsensical (higher than my starting budget, increasing when they should only decrease). This tells me I was not actually tracking. I must recompute from scratch each time using only: starting budget minus amounts paid for lots I won.
- I bid above the minimum raise in round 1 of contested lots (e.g., bidding 27 when min raise was 23). This inflated the final price and cost me the lot when the opponent raised past my value. Always bid the minimum raise in round 1.
- I lost a high-value lot (worth 48 to me) because I bid too low too early and then the opponent outbid me in round 2. In round 2, if I still want the lot and the min raise is below my value, I must bid it — no more "conserving budget" hesitation on the final round of a lot I value.