---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2675
---
My playbook for ref_auction:

- Know exactly what I can spend. My starting budget was 30 (not 100, not 72). Track it from the stated start: every lot I win subtracts my bid; the remainder is my true budget. I will compute it before every reply and report that number in [budget:]. In this episode I wrote 72 and 2 inconsistently — the truth was 28 available during lot 1, then 2 forever after winning it. That incoherence must never happen again.

- Affordability is a constraint checked before value. If the cheapest valid bid exceeds my current true budget, I pass regardless of how attractive the lot is. I bid 34 on lot 3 and 22 on lot 5 with only 2 left after lot 1 — those bids were invalid or lucky to be ignored. No bidding money I do not hold.

- The hard decision rule: bid only when the cheapest valid raise is strictly below my value AND within my true remaining budget. If the minimum raise equals or exceeds my value, pass immediately. Both conditions, every time.

- Compute the cheapest valid bid each time: standing high bid + minimum raise. Bid that minimum; jumping higher round 1 only escalates rivals. In round 2 the minimum raise is the price I pay, so it must leave real surplus.

- Budget discipline across lots: with a small budget, winning one lot may lock me out of everything later. Before committing to a lot, compare its surplus (value − likely price) against surpluses still to come. Lot 1 gave surplus 27 out of budget 30 — nearly the whole fund. That is only acceptable if nothing later offers more surplus per unit of cash; on later lots worth 32 and 33 with standing bids of 16 and 24, I was frozen out. Next time with a tight budget, I pass on early lots whose price will consume most of it, unless clearly the best surplus available.

- In round 1 of a lot, take the cheap entry (minimum raise) when it is below value and well within budget — low cost to stay in contention. But skip even cheap round-1 entries when winning at plausible round-2 prices would break my budget plan for better later lots.

- Do not be scared off by a high standing bid; check it against value. Do not chase: if the minimum valid bid eats all my surplus or my remaining budget, walk away.

- Rivals who overpay near or above estimate (like the 45 paid on lot 3, value unknown but above my 37) burn their budgets; expect stiffness early and cheaper late lots — but this only pays if I have kept my own money. Holding cash for the endgame is the whole strategy.

- Keep reasoning to two or three sentences and end every reply with both bracketed tokens, [bid:] and [budget:], on their own lines, with budget as the true remaining funds after confirmed winnings.