---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 3685
---
# Playbook

**Setting your ceiling before you bid:** For each lot, compute your max acceptable bid as min(value − 5, value × 0.85). Never bid above this number. If the minimum raise in the current round would push you above your ceiling, pass.

**Budget tracking (critical):** Start with the stated budget. The moment a result confirms I won a lot, subtract the price I paid from my remaining budget. Report the true remaining budget every turn. Do not subtract for bids that do not result in a win. If my remaining budget is less than my ceiling for a lot, my effective ceiling drops to my remaining budget (minus a small reserve of 2 for future lots if any remain). **Never bid more than my remaining budget.** If I cannot afford to bid at my ceiling, I bid what I can afford, or pass if even the minimum raise exceeds my remaining budget.

**Round 1 openings (no standing bid):** Open at roughly 50–60% of the lot's estimate. The goal is to enter the auction at low cost and let round 2 do the real work. Do not open at a fraction of your value.

**Round 1 with existing competition:** If the standing bid is well below my ceiling and my budget is sufficient, bid the minimum raise. This keeps me in at lowest cost while I wait to see whether others will continue or drop.

**Round 2 (final round) — the critical round:** This is where I either win or lose the lot. Bidding the minimum raise here almost guarantees I lose to any competitor who is genuinely interested, because they will simply outbid me by the same minimum. Instead, bid at or very near my ceiling. Rationale: if I bid my ceiling and win, I lock in a small guaranteed profit. If I bid my ceiling and lose, I gain nothing — exactly the same outcome as bidding the minimum and losing. There is no downside to bidding higher in the final round unless it exceeds my ceiling or my remaining budget, and the upside (actually winning the lot) is substantial. Concretely: in round 2, bid = min(ceiling, remaining_budget − 2), but if that is just the minimum raise and I am not already the high bidder, jump to that cap instead.

**Exception — I am the standing high bidder in round 2:** If no one has raised over me, I do not need to re-bid. Pass and let the auction close at my existing bid. I only need to act if someone raises.

**When to pass (any round):** If the standing high bid already exceeds my ceiling, pass immediately. If the minimum raise exceeds my remaining budget, pass. Do not raise my ceiling because I want the lot. The next lot may offer a better risk/reward.

**Aggression calibration across lots:** With a small budget and many lots, I can realistically win only one or two (sometimes fewer). I should identify which lots give me the best value-to-estimate ratio (i.e., where my value is highest relative to the estimate) and be most aggressive in round 2 on those. On lots where my value is close to or below the estimate, I can afford to be more passive and let others take them. **Prioritize budget preservation early so that I can commit my ceiling on the best lot.** If I burn my budget on mediocre lots early, I will be forced to pass on the good ones later.

**Do not confuse "staying in" with "winning."** Round 1 is for staying in. Round 2 is for winning. A strategy that treats both rounds the same (minimum raise) will consistently lose to bidders who commit in the final round.

**Score is value minus cost, not value minus estimate.** A lot where my value is 42 and I pay 35 gives me +7. A lot where my value is 51 and I pay 43 gives me +8. The edge (value − price) is what matters, not the estimate. The estimate is only useful for gauging how much competitors might be willing to pay.