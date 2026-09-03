---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 3017
---
# Playbook for ref_estate

**Core principle: buying is score-neutral on the deed axis.** When I buy a property for X, my cash drops by X and my deed value rises by X, so my total score is unchanged. The only upside from buying is rent income from other players landing on it. The only downside is that I might need that cash to pay rent to someone else or to buy a better tile later. So the real question is never "can I afford it?" but "is this the best use of my cash?"

**Rank tiles by rent, not by whether I land on them.** A tile with rent 30 is worth more to me than one with rent 14, all else equal. When I'm cash-constrained, I should be selective and prefer higher-rent tiles. When I'm flush, I buy whatever I land on.

**Cash-constraint test.** Before buying, check: after this purchase, could I still buy the highest-rent unowned tile if I landed on it next turn? If yes, buy freely. If no, apply the threshold below.

**Threshold for cash-constrained purchases.** If buying the current tile would leave me unable to buy the highest-rent unowned tile, I only buy the current tile if its rent is at or above the median rent on the board. Below that, I skip and save for the better tile. (In a typical 8-tile board with rents spread from 10 to 30, the median is around 18–20.)

**When I'm not cash-constrained, buy everything I land on.** If I can afford the current tile AND still afford the best remaining tile afterward, there's no reason to skip. Extra properties mean extra rent income with no opportunity cost.

**Early laps (1–3): build a portfolio of high-rent tiles.** The goal is to own 2–3 tiles with the highest rents by mid-game. This means it's often correct to skip a low-rent tile early in order to save for a high-rent one. One high-rent property (rent 30) outperforms two low-rent properties (rent 14 + 12) over the remaining laps.

**Mid laps (4–5): buy what's affordable, favoring higher rent.** By now I've seen where other players' properties are and have a sense of which rents I'll be paying. I can be more aggressive with purchases since the rent-collection window is shorter.

**Final lap: skip all purchases.** No further rent will be collected, so a purchase is pure cash-to-deed conversion with zero expected income. Always skip.

**Cash buffer: at least the median rent on the board.** I should always keep enough cash to pay a typical rent hit. I don't need the maximum rent as a buffer because the probability of landing on the single highest-rent tile is low (1/8 per player per lap). A buffer of ~18–20 covers most cases.

**Paying rent: pay immediately, update balance.** No negotiation, no delay.

**Collecting salary: add to balance when passing or landing on START.** Track carefully.

**Tracking rent received: add to balance when reported.** Keep a running total.

**When a purchase is unaffordable, say [buy: no] and carry balance forward.**

**What went wrong last episode:** I bought Wharf (rent 18) and Terrace (rent 14) in the first two laps, spending 150 of my 2