---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2933
---
# Playbook

**Setting your ceiling before you bid:** For each lot, compute your max acceptable bid as min(value − 5, value × 0.85). Never bid above this number. If the minimum raise in the current round would push you above your ceiling, pass.

**Budget tracking:** Start with the stated budget. Subtract from it only when you actually win a lot (i.e., when the results confirm you are the winner). Report your true remaining budget each turn. Do not subtract for bids that do not result in a win. If my remaining budget is less than my ceiling for a lot, lower my ceiling to (remaining budget − 2).

**Round 1 openings (no standing bid):** Open at roughly 50–60% of the lot's estimate. The goal is to enter the auction at low cost and let round 2 do the real work. Do not open at a fraction of your value.

**Round 1 with existing competition:** If the standing bid is well below your ceiling, bid the minimum raise. This keeps you in at lowest cost while you wait to see whether others will continue or drop.

**Round 2 (final round) — the critical round:** This is where you either win or lose the lot. Bidding the minimum raise here almost guarantees you lose to any competitor who is genuinely interested, because they will simply outbid you by the same minimum. Instead, bid at or very near your ceiling. Rationale: if you bid your ceiling and win, you lock in a small guaranteed profit (value − ceiling ≥ 5 or ≥ 15% of value). If you bid your ceiling and lose, you gain nothing — exactly the same outcome as bidding the minimum and losing. There is no downside to bidding higher in the final round unless it exceeds your ceiling, and the upside (actually winning the lot) is substantial. Concretely: in round 2, bid = min(ceiling, standing_bid + minimum_raise rounded up), but if that is just the minimum raise and you are not already the high bidder, jump to your ceiling instead.

**Exception — you are the standing high bidder in round 2:** If no one has raised over you, you do not need to re-bid. Pass and let the auction close at your existing bid. You only need to act if someone raises.

**When to pass (any round):** If the standing high bid already exceeds your ceiling, pass immediately. Do not raise your ceiling because you want the lot. The next lot may offer a better risk/reward.

**Aggression calibration across lots:** With a small budget and many lots, I can realistically win only one or two. I should identify which lots give me the best value-to-estimate ratio (i.e., where my value is highest relative to the estimate) and be most aggressive in round 2 on those. On lots where my value is close to or below the estimate, I can afford to be more passive and let others take them.

**Do not confuse "staying in" with "winning."** Round 1 is for staying in. Round 2 is for winning. A strategy that treats both rounds the same (minimum raise) will consistently lose to bidders who commit in the final round.