---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 2558
---
# Playbook

**On buying:**

When an unowned property is put to me and I can afford it (my cash ≥ price), I buy it. The purchase is score-neutral at the moment (cash and deed value swap at the same amount) and score-positive if I collect rent from it later. The only time I decline is when the purchase price exceeds my current cash.

I do not decline to "preserve a cash buffer." A cash buffer has no greater final-score value than the deed it would buy.

**On prioritising which properties to buy:**

When I land on an unowned property I can afford, I buy it regardless of rent level, because the decision is between buying now (score-neutral floor, rent upside) and not buying (score-neutral, no upside). There is no opportunity cost of buying one property over another in this game — I only get the option when I land on it. So "prefer high rent" is a matter of ex-post satisfaction, not a decision criterion. The criterion is simply: can I afford it? If yes, buy.

**On laps remaining and buying:**

Buying earlier in the game is strictly better than buying later because it opens a longer window for collecting rent. But since I only get the option when I land on a property, I don't get to choose timing — I just buy whenever I can. When the final lap remains and I land on an unowned property, buying is score-neutral with zero chance to collect rent. I still buy; there is no downside.

**On rent payments:**

When I land on someone else's property, I pay the stated rent. It is a fixed cost. I track my cash carefully after each payment.

**On incoming rent:**

When other players land on properties I own, I receive their rent. This is added to my cash balance on the turn it is received. I track it the same way I track salary — it increases my declared balance.

**On salary:**

When I pass or land on START, I collect the 25 salary and add it to my declared balance before paying any rent for that turn.

**On tracking:**

I keep a running total: my cash, my deeds, and my cumulative score (cash + sum of deed purchase prices). The final number that matters is that total. I do not agonise over intermediate cash levels. Each turn I account for: salary received, rent paid, rent received from others, and any purchase made.

**On format:**

- Pay token: use `P<k>` (e.g. `[pay: 24 to P1]`), not "investor 1" or "P<k>" spelled out.
- Buy token: exactly `yes` or `no`, not `none` or any other word.
- Balance token: the integer cash I hold after all transactions this turn (salary added, rent subtracted, purchase subtracted, incoming rent added).