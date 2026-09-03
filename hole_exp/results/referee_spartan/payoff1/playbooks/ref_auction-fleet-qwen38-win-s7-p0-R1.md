---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 2898
---
# Playbook: Ref Auction

**Budget discipline (non-negotiable):**
- Before every single bid, compute: remaining budget = initial budget − (sum of final prices of all lots I have already won). I have not "lost" money on lots I lost; only wins reduce my budget.
- I will never bid an amount that, if I win, would push my total spending past my remaining budget. If the minimum raise exceeds what I can afford, I pass regardless of how much I value the lot.
- The [budget] field I report must always equal this computed number. I will not guess or carry forward a stale figure.

**Assess each lot before deciding to engage:**
- Compute my "surplus at minimum win": my value minus the minimum raise needed to win right now. If this is ≤ 0, pass immediately.
- Compute my value-to-estimate ratio. Lots where my value is 25%+ above the estimate are my priority targets—these are where I have the most private information advantage.
- Given my remaining budget and the number of lots still to come, decide how much I am willing to allocate to this lot. I should not spend my entire budget on the first high-value lot I see if later lots also look attractive.

**Round 1 of 2:**
- If the standing bid is 0 and my value is well above the estimate: open at roughly 50–60% of my value. This establishes a position high enough that a competitor would need to move significantly to overtake me, but low enough that I still have surplus.
- If the standing bid is already close to or above my value: pass. Do not enter a lot I cannot profitably win.
- If the standing bid is modest and my value is only marginally above the estimate: bid the minimum or pass. I'm not strong enough on this lot to fight.

**Round 2 of 2 (final round):**
- If the minimum raise is below my value AND I can afford it: bid the minimum raise. There is no further round, so any amount above the minimum is pure overpayment.
- If the minimum raise is at or above my value: pass. A guaranteed loss is never worth taking.
- If I can afford the minimum raise but it would leave me with essentially zero budget for remaining lots: weigh the surplus on this lot against my expected surplus on later lots. If later lots have higher value-to-estimate ratios, consider passing here.

**General principles:**
- I am not obligated to bid on every lot. With a limited budget across multiple lots, selectivity is the primary source of profit.
- I will not bid "to signal interest" if I'm not confident I can win profitably at the end. Signaling has no value if I fold in round 2.
- I will not outbid my value to win a lot "just because I want it." The score is value minus price, not number of lots won.
- When I see the results of previous lots, I use them to calibrate how aggressively other bidders play. If a competitor is consistently winning at high prices, they likely have high values on those lots and I should avoid head-on conflicts there.