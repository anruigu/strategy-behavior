---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 3477
---
# Playbook for ref_estate

**Core principle: buying is score-neutral on the deed axis.** When I buy a property for X, my cash drops by X and my deed value rises by X, so my total score is unchanged. The only upside from buying is rent income from other players landing on it. The only downside is that I might need that cash to pay rent to someone else. So I buy if I can afford it AND keep a buffer for rent payments.

**Prioritize by absolute rent, not rent-to-price ratio.** A tile with rent 30 generates more expected income than one with rent 24, regardless of price. Price is neutral on the deed axis, so the only thing that matters for expected gain is how much rent I'll collect over the remaining laps.

**Default action: buy what I land on if I can afford it while keeping a cash buffer.** I don't control my rolls, so I can't reliably save up for a specific tile. If I land on a tile and skipping it means I might never see it again, the expected rent loss is real. Buying is the correct default.

**Cash buffer: keep at least the maximum rent on the board (the highest-rent tile's rent value) in cash at all times during laps 1 through 4.** This ensures I can always pay the worst-case rent without going negative. In the example board that's 30. If buying would drop me below the buffer, I skip unless the tile I'm buying itself has rent equal to or greater than the buffer (meaning I'm replacing the risk with equivalent or better income potential).

**On laps 5 and 6 (final two laps), I can relax the buffer.** With fewer laps remaining, the probability of being hit by a large rent payment is lower, and the upside of collecting rent from a high-rent tile I own is more valuable. I can drop to near-zero cash on the final lap if buying a high-rent tile.

**In the final lap specifically, buying is score-neutral.** No further rent will be collected after the game ends, so a purchase adds deed value and subtracts equal cash with zero expected income. I skip it unless I have some other reason (which I don't, since cash and deeds count equally).

**When I land on someone else's property, I pay the rent immediately and update my balance.** No negotiation, no delay.

**When I pass or land on START, I collect my salary and add it to my balance.** I track this carefully because it's the only recurring income I get for free.

**When I receive rent from other players landing on my properties, I add it to my cash balance at the point it's reported to me.** I don't net it against future payments; I just keep a running total.

**When a purchase is unaffordable, I say [buy: no] and carry my current balance forward.** I do not round up or assume I can borrow.

**What went well in my last episode:** The buffer rule protected me from being cash-strapped. Buying Foundry early (lap 1) paid out 24 in rent by lap 3. Buying Exchange on lap 5 was a good aggressive call with 2 laps left. Skipping Depot on the final lap was correct (couldn't afford it, and it would have been neutral anyway).

**What to watch for:** If I have multiple affordable tiles in a row, I should compare their absolute rents and prefer the higher one, but since I land where I land, the practical rule is just "buy if buffer allows." The one scenario where I should consider skipping is if buying a low-rent tile (rent < 10) would drop me below the buffer while a higher-rent tile is nearby and I'm confident I'll reach it — but this is rare and hard to justify, so I default to buying.