---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1498
---
Playbook for ref_auction:

- My score is value won minus price paid, so every dollar bid is a dollar of potential profit burned. The goal is to win cheaply, not to win at all costs.
- Never bid my full value — a win at value scores zero. I did this and earned nothing from it. Set a personal ceiling below value: pass once the price reaches roughly value minus a small margin (say 10–15%).
- Use minimum raises by default. Jumping above the minimum just pays more for the same win; my big opening anchor at the estimate on the last lot could easily have overshot what rivals would pay.
- In round 1, bid the minimum raise if the standing price is comfortably below my ceiling; otherwise pass and wait.
- In round 2 (final round), bid the minimum raise if it stays under my ceiling; pass if it doesn't. Don't bid more than the minimum needed to take the lead.
- When I am the standing high bidder in the final round, always pass — never raise against myself.
- Track remaining budget but don't fixate on it: the binding constraint is the value ceiling, not the bankroll. Report the budget token honestly as the budget I have left, not the post-bid amount — I got this wrong multiple times and it was meaningless noise at best.
- Prefer lots where my value far exceeds the estimate — those are the high-margin wins. Accept losing lots where bidding reaches my ceiling; conceding is free, overpaying is not.
- Estimate isn't a price guide for my decision; only my value minus the standing bid matters.