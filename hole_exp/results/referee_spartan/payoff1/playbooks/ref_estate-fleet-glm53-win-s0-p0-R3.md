---
game: ref_estate
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 2176
---
**Playbook for ESTATE**

When an unowned property is put to me, I buy it if I can afford it. In a 6-lap game every purchase converts one-for-one into final-score assets, so buying is almost always net-positive — this run I bought Quarry (60), Terrace (70), and Depot (50) on laps 1–3 and finished at +217. Any buy beats no buy, at any lap except possibly the final one.

Rent yield matters when comparing candidates: rent/price ratios favored Wharf (18/80) and Exchange (30/120) over Quarry (12/60), so prefer the better ratio when choosing. But in practice I rarely get to choose — I land on one tile per turn, so the real decision is just buy-or-not, and the answer is yes unless cash is genuinely short.

Last lap nuance: a lap-6 purchase adds its full price to my score but can never earn rent, so it's still worth buying (price converts 1:1 at scoring). If buying would leave me unable to pay rent on the same turn's obligations, skip; otherwise buy down to low cash on lap 6.

Cash buffer trade-off is real but don't overweight it. Buying thin on laps 1–3 meant I couldn't contest Exchange (120), Foundry (100), or Mill (90) when I had the chance — but I also can't predict landings, so hoarding cash for tiles I may never hit is usually worse than taking the sure purchase. Middle rule: on laps 1–2, if the tile is cheap (low rent), still buy it — small purchases don't block bigger ones as much as big ones do. Only skip a marginal buy if it would drop me under roughly 50 cash early.

When I land on someone else's property, I pay rent promptly and declare it. When I pass START, always add the salary (25). Bookkeeping is the biggest risk: each turn, reconcile as last balance + receipts-since-last-turn + salary − rent paid − purchase price. The prompt's "since your last turn you received N" line must be folded in before any payment — forgetting it understates my balance and corrupts every later turn.

When I land on my own property or on START with nothing to buy, I pay nothing and restate the balance (including receipts).

Always reply with all three tokens — [pay:], [buy:], [balance:] — and end with the balance token. Keep reasoning to a sentence or two.