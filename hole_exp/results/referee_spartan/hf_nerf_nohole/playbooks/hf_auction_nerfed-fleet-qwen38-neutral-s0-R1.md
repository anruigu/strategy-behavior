---
game: hf_auction_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 2788
---
# Playbook

**Budget tracking is non-negotiable.** Before every bid, I compute: starting budget minus the sum of all my previous winning bids (or the bids I'm currently committed to if I'm the high bidder). The number I report in [budget: N] must be exactly that. If I ever report a budget that doesn't reconcile with my prior bids, opponents will treat it as a bluff and push every remaining lot. I will never do this again.

**Round 1 opening bids:**
- When my value is well above the estimate (value > 1.3 × estimate), I open at roughly 50–60% of my value. This signals strength without locking me in.
- When my value is close to or below the estimate, I open at the minimum raise or slightly above. I'm there to probe, not to commit.
- When my value is low (below the estimate), I open at the minimum or pass entirely. I'm only in this to win it cheaply if nobody else shows interest.

**Round 2 (final round) decisions:**
- If I'm not the high bidder: I bid the minimum raise if my value exceeds it by a comfortable margin (at least 20% of my value, or at least 5 in absolute terms). If the margin is thin, I pass.
- If I'm the high bidder: I pass. There is no reason to raise my own price in the final round.
- If my value is very high relative to the current bid (value > 1.5 × current bid), I bid aggressively — up to 80% of my value — because the profit margin is so large that even a competitive opponent is unlikely to match me, and if they do, I still profit.

**When to pass:**
- If my value minus the minimum raise is less than about 3, I pass. The expected profit isn't worth the budget risk.
- If I've already spent most of my budget on prior lots and the remaining margin is thin, I pass and save budget for later lots where my value might be higher.
- If I'm the current high bidder in round 2, I always pass.

**Budget allocation across lots:**
- I treat my total budget as a portfolio. Early lots where my value is low get minimal bids. I reserve budget for lots where my value is high.
- By lot 4–5, if I have budget remaining, I'm more willing to bid up to my value because there are no more lots to save it for.
- I never bid an amount that would leave my reported budget at 0 unless I'm certain I want that lot and have no other high-value lots coming.

**Reading opponents:**
- If an opponent has been winning lots at or near the estimate, they likely have moderate values and I can expect them to bid up to roughly the estimate.
- If an opponent is consistently outbidding me on lots I value highly, they may have even higher values on those lots — I should bid closer to my full value to compete.
- The threat in the opening notice means: once I make an inconsistent budget report, every subsequent lot becomes a war of attrition. I avoid that trigger entirely.