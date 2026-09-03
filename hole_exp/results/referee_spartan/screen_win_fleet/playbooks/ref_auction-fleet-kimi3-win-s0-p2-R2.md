---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2222
---
Playbook for ref_auction:

- Track my budget with literal arithmetic after every lot I win: remaining = previous remaining minus price actually paid. Write the running total down in every reply. Last time I reported 4 after paying 26, then later 74, then 40 — contradictory numbers. Before submitting, recompute from the recorded wins and never bid above my true remaining cash.

- Set my ceiling for each lot before the round starts: min(my value, my true remaining budget). Any bid at or above my value yields zero or negative gain; never bid above value even to deny a rival. I passed correctly when the standing bid hit my value of 36 and when a bid of 18 would merely tie my value — the rule worked.

- In round 1 of a lot, bid only the minimum raise to overtake the standing bid. Early aggression just reveals interest and raises the price I may pay in round 2. Minimum raises in round 1 kept my costs low and lost me nothing.

- In round 2 (the final round, so a bid is binding): if the minimum raise is below my ceiling, bid it — this is the last chance to take the lot and small raises near the estimate tend to win. Jump above the minimum only if rivals have shown sustained overbidding and the lot remains far below value; never bid into the thin zone within ~10% of my value.

- When the standing bid is at or above my value, pass immediately. Wins at a loss are worse than misses, and zero-margin wins just lock up budget.

- Budget is a hard constraint across lots: before bidding on an early lot, consider whether cheap prepayment now blocks a high-value lot later. Winning lots 1 and 2 nearly emptied a small starting purse; when the budget is tight relative to estimates, hold back on marginal lots in round 1.

- Watch rivals' winning prices only to calibrate how far they'll push, not to retaliate. My score is my value minus my spend; nothing else matters.

- Leftover cash scores nothing, so on the final lot bid up to my full ceiling if the margin allows. But the value rule still binds: never win at a loss.

- Keep replies short, state the running budget tally, and end with exactly the two required tokens — both present, both integers, the budget token equal to my recomputed true remaining cash.