---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2885
---
**Playbook for ref_auction**

**Read the starting budget from the prompt and use only that number.** The auction description states my budget explicitly (e.g., "You start with a budget of 30"). I use that figure — and only that figure — for all budget calculations. I never substitute a different number from memory or assumption. Before every bid, I compute: stated starting budget − sum of prices I have already committed to winning. That is my remaining budget. I state it exactly.

**I never bid an amount that exceeds my remaining budget.** If the minimum raise would put me over budget, I pass. No exceptions, no "I'll figure it out later."

**When I am put a bid and the standing high bid already meets or exceeds my value for the lot, I pass immediately.** A raise would put me in negative surplus on this lot.

**When I open a round with no standing bid, I bid the minimum raise.** This tests whether others are interested without committing budget. I only escalate in round 2 if the lot is worth it.

**In the final round of a lot, if the standing bid is below my value and I can afford the minimum raise, I bid exactly the minimum raise above the standing bid.** There is no benefit to overbidding in the last round — no one can respond, so I minimize what I pay.

**Before committing in the final round, I verify my remaining budget covers the bid AND leaves me something for future lots.** With a budget of B across N lots, I aim to keep at least B/N per remaining lot available after each commitment. If bidding the minimum raise would consume more than my fair share of remaining budget, I weigh whether this lot's surplus justifies the concentration of spend.

**I do not bid aggressively in round 1 to "deter competition."** With a tight budget spread across many lots, an aggressive opening bid risks locking me into a price I can't afford or wasting budget that should go to a lot where my surplus is higher. I open at the minimum and let round 2 decide.

**When I hold a lot with thin surplus (value only slightly above the likely clearing price), I bid the minimum and do not chase.** If someone outbids me on a lot where my surplus would be only 2–3 points, I accept the loss.

**I prioritize lots where my value-to-estimate gap is largest for my budget.** Those are the lots where I can afford to pay a reasonable price and still earn meaningful surplus. I let go of low-surplus lots early to preserve budget for these.

**If I am the current high bidder in the final round, I do not raise.** I hold my position. There is no reason to pay more than I already have committed, and no one will respond to a raise in the last round anyway.

**I track my wins and losses explicitly as results are reported.** After each lot resolves, I update: which lots I won, at what price, and what my remaining budget is. This running total is the only basis for subsequent bids.