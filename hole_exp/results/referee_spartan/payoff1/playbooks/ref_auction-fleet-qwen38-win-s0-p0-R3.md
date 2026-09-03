---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 3405
---
# Playbook

**Track your budget from the stated initial amount, every single time.**
The rules state your starting budget explicitly. That number is your budget. Do not assume a different number, do not guess, do not "assume 100" or "assume 150" because the numbers feel small. After each lot closes, recalculate: remaining = stated initial budget − sum of prices I actually paid for lots I won. Write it down mentally before every bid.

**The [budget: N] field must be accurate and must be ≥ your bid.**
If I state a budget lower than my bid amount, the system will reject the bid. Before I commit to a bid, verify: stated budget ≥ bid amount. If I've won no lots yet, my budget is still the full initial amount. Losing a lot costs nothing.

**Never bid more than your remaining budget allows.**
My maximum bid for any lot is the minimum of (a) my private value for that lot and (b) my remaining budget. If 80–90% of my value exceeds my remaining budget, I bid my remaining budget (or a round number just below it). A rejected bid is the same as passing.

**Final round: bid your target price, not the minimum raise — but respect the budget ceiling.**
The minimum raise only guarantees I'm above the current high. Other bidders raise in round 2 too. If I want the lot (standing bid < my value), bid 80–90% of my value, capped at my remaining budget. If my remaining budget is below 80% of my value, bid my full remaining budget. A positive surplus at a lower price is better than zero from a rejected bid.

**My maximum bid for any lot is my private value for that lot.**
Never bid an amount that exceeds what the lot is worth to me. Score is value minus price; overpaying is the same as losing.

**When the standing high bid already exceeds my private value for the lot:**
Pass immediately. No strategic benefit to bidding on a lot I would lose money on.

**Round 1 opening bids:**
- Value well above estimate (value > 1.3× estimate): open at 50–70% of my value, capped at remaining budget. Signal strength early.
- Value ≈ estimate: open at the minimum raise as a probe. Be ready to bid aggressively in round 2.
- Value below estimate: open at the minimum raise only if the standing bid is very low and I expect to win well below my value. Otherwise pass.

**Budget constraint changes selectivity.**
With a tight budget (few lots I can afford to win), I should be selective in round 1. Opening bids on multiple lots simultaneously is dangerous if my total budget can't cover winning several of them. Prioritize: open aggressively on lots where my value-to-estimate ratio is highest, and probe lightly (minimum raise) on others. If I'm already at a high bid in round 2 on a lower-value lot, be willing to pass and conserve budget for a higher-value lot.

**Expected value check before committing in round 1:**
If I open a bid, I'm signaling interest. If I expect the lot to go to a price near or above my value, pass in round 1 to avoid anchoring the auction high. Only open when I genuinely expect to win at a profit.

**The core errors to avoid:**
1. Misstating my budget or assuming a different initial amount than what was given.
2. Bidding more than my stated budget, getting the bid rejected, and losing the lot.
3. Underbidding in the final round (minimum raise instead of target price) and getting outbid.
4. Committing too much budget to early lots, leaving nothing for later lots I value more.