---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 2344
---
Playbook for ref_auction:

- My score is value won minus price paid, so every dollar bid is a dollar of potential profit burned. The goal is to win cheaply, not to win at all costs.
- MY BUDGET IS A HARD, BINDING CONSTRAINT — I cannot bid more than the money I have left. I lost my biggest opportunity (value 62, rival at 34) because I bid 38 with only 28 remaining; that one mistake cost ~24 points. Before every bid, compute exactly: starting budget minus everything already paid. Never submit a bid above the cash actually left.
- Prioritize budget allocation across lots: early small-margin wins can starve me for later high-value lots. When two rival bidders are active, don't chase every lot to the edge of my ceiling — shift that budgeting logic toward spending on the lots with the fattest value-over-price gap. If I had passed on thin lots like value-41-at-36, I'd have had the cash to land the value-62 lot.
- Never bid my full value — a win at value scores zero. Set a personal ceiling below value: pass once the price reaches roughly value minus a small margin (say 10–15%). A bid at the very edge of the ceiling is only justified in the final round if I can actually afford it and the alternative is zero.
- Use minimum raises by default. Jumping above the minimum just pays more for the same win.
- In round 1, bid the minimum raise if the standing price is comfortably below my ceiling; otherwise pass and wait.
- In round 2 (final round), bid the minimum raise if it stays under my ceiling AND under my remaining budget; otherwise pass. Don't bid more than the minimum needed to take the lead.
- When I am the standing high bidder in the final round, always pass — never raise against myself.
- The budget token: report the budget I have left before this bid, not the post-bid amount, and compute it from actual payments recorded in the results line (lot X: bidder 2 won at N), not from memory or assumption. I got this wrong repeatedly; wrong budget reporting is noise at best and correlated with my fatal over-budget bid at worst.
- Prefer lots where my value far exceeds the estimate — those are the high-margin wins. Accept losing lots where bidding reaches my ceiling; conceding is free, overpaying is not.
- Estimate isn't a price guide for my decision; only my value minus the standing bid, and my remaining cash, matter.