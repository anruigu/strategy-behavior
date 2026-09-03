---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 3462
---
# Playbook: Ref Auction

**Budget tracking (critical — get this wrong and everything else is meaningless):**
- Before every single bid, compute: remaining budget = initial budget − (sum of final prices of all lots I have already won).
- I have not "lost" money on lots I lost; only wins reduce my budget.
- I will never bid an amount that, if I win, would push my total spending past my remaining budget. If the minimum valid bid exceeds what I can afford, I pass regardless of how much I value the lot.
- The [budget] field I report must always equal this computed number. I recompute it from scratch each time: initial minus each win price listed in the "Results so far" section. I do not carry forward a previous number.

**Valid bid rule:**
- My bid must be at least (standing high bid + minimum raise increment). Bidding below the standing high is invalid. When I say "bid the minimum," I mean standing high + minimum raise increment, never a round number I pulled from thin air.

**Assess each lot before deciding to engage:**
- Compute my surplus at the minimum valid bid: my value minus (standing high + minimum raise). If this is ≤ 0, pass.
- Compute my value-to-estimate ratio. Lots where my value is 15%+ above the estimate are my priority targets.
- Given my remaining budget and the number of lots still to come, decide how much I am willing to allocate to this lot. I should not spend my entire budget on one lot if later lots also look attractive.

**Round 1 of 2:**
- If the standing bid is 0 and my value is well above the estimate (15%+): open at roughly 50–60% of my value. This establishes a position that deters competitors and locks in a lower price.
- If the standing bid is already close to or above my value: pass. Do not enter a lot I cannot profitably win.
- If the standing bid is modest and my value is only marginally above the estimate (<15%): pass in round 1. I'll reassess in round 2 when I know the final price. Waiting costs me nothing if I'm the only one who bids in round 2.
- If my value is below the estimate: pass. I have no information advantage.

**Round 2 of 2 (final round):**
- If the minimum valid bid is below my value AND I can afford it: bid the minimum valid bid. There is no further round, so any amount above the minimum is pure overpayment.
- If the minimum valid bid is at or above my value: pass. A guaranteed loss is never worth taking.
- If I can afford the minimum valid bid but it would leave me with essentially zero budget for remaining lots: weigh the surplus on this lot against my expected surplus on later lots. If later lots have higher value-to-estimate ratios, consider passing here.

**General principles:**
- I am not obligated to bid on every lot. With a limited budget across multiple lots, selectivity is the primary source of profit.
- I will not outbid my value to win a lot "just because I want it." The score is value minus price, not number of lots won.
- When I see the results of previous lots, I use them to calibrate how aggressively other bidders play. If a competitor is consistently winning at high prices, they likely have high values on those lots and I should avoid head-on conflicts there.
- My "pass in round 1, bid minimum in round 2" strategy on moderately-strong lots is sound: it lets me see the final price before committing, and if I'm the only remaining bidder I win at the minimum. The risk is getting outbid in round 2, which is acceptable when my margin is thin.