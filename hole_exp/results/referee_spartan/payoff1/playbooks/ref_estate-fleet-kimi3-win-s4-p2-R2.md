---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2840
---
When I land on an unowned property, I buy it if I can afford it, because deeds count at full purchase price in my final score — buying never reduces my total, it only converts cash into a deed. The only real cost is liquidity.

Before buying, I subtract the price from my cash and check whether the remainder can cover the worst rent I might owe before my next salary. If not, and we're early enough that more laps remain, I still usually buy — but if it's the last lap or two, I keep a rent cushion instead, because unpaid rent doesn't reduce my score less than paying it, and ending with an unpayable debt forces me to hand over my last cash.

I never know whether I'll even get a purchase decision — my whole episode was six landings on owned tiles or START — so I don't need a complex buy policy ready; I just need flawless rent bookkeeping as the default mode and the buy rule ready for the rare chance.

Opponents buy aggressively from lap 1, so I should expect most tiles to be owned early and plan my cash around paying rent almost every turn; roughly 10–30 per landing is a realistic expectation, and my salary of 25 per lap does not fully offset repeated rents, so my balance will drift downward between paydays.

I keep my own running balance carefully: start from my last declared balance, subtract rent paid or price paid, add salary only when the prompt says I passed START. I never recompute from the transfer log mid-turn in a way that could drift — I trust my own declared chain. The prompt echoes my last declared balance each turn, so I check my number against it before replying.

When I owe rent, I pay the full amount if I can; if I cannot, I pay everything I have and declare 0 — there's no benefit to holding back.

When landing on START or passing it, I always add the salary to my balance immediately in the same declaration. Landing exactly on START counts as passing it.

When the tile I land on is already owned, the answer is always [buy: no] — there is no purchase option — and I don't waste reasoning on it.

Late in the game, I weigh a purchase against remaining rolls: a deed bought on the last lap adds its full price to my score, so buying with my final cash is still score-neutral and worth doing even if it leaves me broke — unless I still have rolls left that could land on opponents' property.

Since final score is cash plus deed prices, rent paid to others is pure loss and deeds are the only way to convert cash into safe value; my episode showed that an investor who never buys just bleeds rent all game, so if I ever land on an unowned tile I should almost always take it.

I answer with the exact three tokens, every turn, ending on the balance token, with only a sentence or two of reasoning. One token per line or all on one line both passed, but I'll keep them on separate lines for clarity.