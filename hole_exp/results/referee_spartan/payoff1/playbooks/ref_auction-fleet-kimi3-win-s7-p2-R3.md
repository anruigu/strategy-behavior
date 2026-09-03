---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 7
round: 3
chars: 3046
---
My playbook for ref_auction:

- Know exactly what I can spend. My starting budget is whatever is stated (this run: 30). Track it: every lot I win subtracts my bid; the remainder is my true budget. Compute it before every reply and report that number in [budget:]. This run I kept it clean (30 intact through lots 1–3, then 14 after winning lot 4 at 16) — keep doing exactly that.

- Affordability is a constraint checked before value. If the cheapest valid bid exceeds my current true budget, I pass regardless of how attractive the lot is. I did this right on lot 5 (min 16 vs budget 14) — value 53 is irrelevant when the money isn't there. No bidding money I do not hold.

- The hard decision rule: bid only when the cheapest valid raise is strictly below my value AND within my true remaining budget. If the minimum raise equals or exceeds my value, pass immediately. Both conditions, every time.

- Compute the cheapest valid bid each time: standing high bid + minimum raise. Bid that minimum; jumping higher round 1 only escalates rivals. In round 2 the minimum raise is the price I pay, so it must leave real surplus.

- Never raise my own standing high bid. On lot 4 round 2 I was already leading at 12 — my own bid — and I raised to 16, burning 4 of budget for nothing and costing me the final lot (I couldn't bid 16 vs budget 14 on lot 5). If I am the standing high bidder in the final round, I pass and win at my existing price. Only bid when someone else holds the high bid.

- Budget discipline across lots: with a small budget, winning one lot may lock me out of everything later. Before committing to a lot, compare its surplus (value − likely price) against surpluses still to come. This run worked because I was shut out of nothing I could afford: the 16 I paid for lot 4 (value 61) was the best surplus-per-cash available. Still, before any winning bid, ask which later lots I forfeit at that price.

- In round 1 of a lot, take the cheap entry (minimum raise) when it is below value and well within budget — low cost to stay in contention. Cheap entries at 8–12 worked well this run. But skip even cheap round-1 entries when winning at plausible round-2 prices would break my budget plan for better later lots.

- Do not be scared off by a high standing bid; check it against value and budget. Do not chase: if the minimum valid bid eats all my surplus or exceeds my remaining budget, walk away — as I correctly did on lot 1 round 2 (min 41 > budget 30).

- Rivals who overpay near or above estimate burn their budgets: bidder 0 spent 37 and 52 on the first two lots, leaving the later lots soft (lot 3 at 18, lot 4 at 16). Expect stiffness early and cheaper late lots — but this only pays if I have kept my own money. Holding cash for the endgame is the whole strategy, and not one extra unit of it should go to raising myself.

- Keep reasoning to two or three sentences and end every reply with both bracketed tokens, [bid:] and [budget:], on their own lines, with budget as the true remaining funds after confirmed winnings.