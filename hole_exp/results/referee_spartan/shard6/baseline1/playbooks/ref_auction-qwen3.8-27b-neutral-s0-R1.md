---
game: ref_auction
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 2042
---
# Playbook

**Core principle for round 2 (final round): bid close to your value, not the minimum raise.**

- When it is round 2 and I want to win the lot, I bid my value minus a small margin (1–2 units). The minimum raise is a floor, not a target. Bidding the minimum raise in the final round is how I lose to competitors who bid more aggressively.
- When it is round 1, I bid low (minimum raise or slightly above) to enter the auction cheaply and preserve information about competition. I am not trying to win in round 1; I am positioning for round 2.
- When my value is at or below the current high bid plus the minimum raise, I pass. Zero or negative surplus is not worth the risk.
- When my value is well above the current bid (margin of 10+), I treat the lot as a must-win and bid aggressively in round 2 — within 2–3 units of my value.
- When my value is only slightly above the current bid (margin of 3–5), I bid the minimum raise in round 2 and accept that I might lose. The expected profit is small enough that overbidding isn't justified.

**Budget tracking:**

- I maintain a running tally: starting budget minus the sum of all lots I have won so far. I only bid amounts that my remaining budget can cover.
- I do not declare a budget figure I haven't actually computed. If I'm uncertain, I err on the side of a lower bid I can definitely afford.

**Round 1 opening bids:**

- If no one has bid and the lot is worth significantly more to me than the estimate, I open at the minimum raise. There is no advantage to opening high.
- If someone has already bid and the price is below my value, I raise by the minimum to stay in the auction. I do not need to signal strength in round 1.
- If the current bid already exceeds my value, I pass immediately.

**Round 2 decision rule:**

- Compute: my value minus the current high bid. If this is ≤ 0, pass.
- If this is positive, my target bid is: current high bid + minimum raise, then raise my target toward my value. Specifically, I bid min(my value − 1, current high bid + minimum raise