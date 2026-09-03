---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 1713
---
My playbook for ref_auction:

- Know exactly what I can spend: bids are capped by my actual budget, and winnings reduce it. Track my real remaining budget after every lot I win and report that number accurately in the [budget:] token — never invent a figure. In the past I reported budgets of 80 and 35 when I had started with 30 and spent from it; that is incoherent and will not be repeated.

- The hard decision rule: bid only when the cheapest valid raise is strictly below my value for the lot. If the minimum raise equals or exceeds my value, pass immediately — there is no upside.

- Compute the cheapest valid bid each time: standing high bid + minimum raise, and also verify it is at least the minimum raise itself. Bid that minimum unless there is a reason to jump.

- In round 1 of a lot, always take the cheap entry (minimum raise) when the minimum is below my value — there is no cost to being in contention and a second round remains.

- In round 2 (the final round), the minimum raise wins me the lot as bid. Bid the minimum when it is below value; only jump higher if I strongly suspect a rival will overbid and I have large surplus to protect — and even then, never bid above my value.

- Do not be scared off by a high standing bid alone; check it against my value. But do not chase: if the minimum valid bid already eats all my surplus, walk away.

- When rivals have visibly overpaid (bids near or above estimate), expect them to be budget-constrained later; stay disciplined and pick up late lots cheaply with minimum raises.

- Keep reasoning to two or three sentences and end every reply with both bracketed tokens, [bid:] and [budget:], with the budget reflecting the true remaining funds.