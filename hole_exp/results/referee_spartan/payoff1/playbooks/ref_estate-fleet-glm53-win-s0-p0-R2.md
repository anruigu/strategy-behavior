---
game: ref_estate
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 1993
---
**Playbook for ESTATE**

When an unowned property is put to me, I buy it if I can afford it, prioritizing high-rent tiles (Exchange, Foundry) over cheap ones. With only 6 laps, purchase price converts one-for-one into final-score assets while rent income stacks on top, so buying is almost always net-positive. This run confirmed it: buying Quarry on lap 1 and Foundry on the final lap both paid off, and the final-lap Foundry buy was still correct even though it left me at 41 cash — cash below the purchase price of a deed is just dead weight at scoring time.

Exception: on the very last lap, do not keep a cash buffer. A purchase on lap 6 can never earn rent but still adds its full price to my score, so if I land on something unowned I buy it down to (nearly) zero cash. Earlier laps are different: spending thin early meant I could only watch while P1 and P2 snapped up Exchange, Terrace, Mill and Depot. If a purchase would drain me enough to miss a better property soon after, prefer the higher-rent tile and skip the marginal one. As a rule of thumb: early laps, keep enough buffer to buy anything on the board (~120); late laps, buy everything I land on.

Rent yield matters more than price when choosing between candidates: rent/price ratios here favored Wharf (18/80) and Exchange (30/120) over Quarry (12/60), so at equal opportunity, prefer the better ratio — but any buy beats no buy.

When I land on someone else's property, I pay rent promptly. When I pass START, I always add the salary (25). Critical bookkeeping detail that worked: the prompt tells me "since your last turn you received N" — I must add those receipts to my last declared balance before settling. Reconcile every turn: last balance + receipts + salary − payments − purchase price.

When I land on my own property or START with nothing to buy, I pay nothing and restate my balance (including receipts).

Always reply with all three tokens and end with the balance token; keep reasoning to a sentence or two.