---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 3212
---
# Playbook for ref_estate

**The score is cash + deed purchase price. Buying a property is score-neutral by itself — it just shifts value from cash to deeds.** The only things that change my score are rent I collect, rent I pay, and salary. Every decision should serve those three flows.

**When an unowned property is available and I can afford it while keeping a safe cash buffer, I buy it — prioritizing by rent, not by price.** Higher rent means more income each time another player lands on it. The purchase price is score-irrelevant (cash → deed value is a wash); the rent is what generates net gain.

**Cash buffer rule: after any purchase, keep at least the highest rent currently paid to another player (i.e., the highest rent on a property owned by someone else).** If I can't determine that, keep at least 20 as a floor. I only ever pay one rent per turn (the tile I land on), so a single-rent buffer is sufficient — I don't need to accumulate for multiple simultaneous payments.

**Early purchases are more valuable than late purchases.** In a 6-lap game, a property bought on lap 1 has 5 laps to generate rent; one bought on lap 4 has only 2. Salary income is also limited (I typically pass START only once or twice across 6 laps with rolls of 2–3), so cash hoarded for "later" rarely finds a use. Spend early.

**When I can only afford one of two unowned properties, I pick the higher-rent one.** The purchase price difference is score-neutral; the rent difference is what matters.

**The highest-rent property in the game will often be the most expensive and may be unaffordable for most of the game.** Don't let that deter me from buying the next-best thing I can afford. In practice, the property I *can* buy is the one I should buy.

**I track every property each other player owns and its rent.** When I see someone buy a high-rent property, I note that I may owe them. This informs my cash buffer: the higher the rents on other players' properties, the more cash I should keep liquid.

**When I land on my own property, nothing is due.** This is a neutral event, not a "gain" — the real value of owning a property comes from other players landing on it and paying me rent. Landing on my own tile simply means I skip a rent payment I would have made to the owner (if it weren't mine).

**When I pass or land on START, I always collect the salary.** It's free score with no downside.

**I do not skip buying a property just because it's "expensive" relative to my cash.** The purchase price is score-neutral. The only reasons to skip are: (a) I can't afford it, or (b) buying it would drop me below my cash buffer. Otherwise, buy.

**When I end up one point short of a property I wanted, that's bad luck, not a planning error.** If my earlier purchase was the higher-rent option I could afford, it was the right call. Don't second-guess a correct early decision because a slightly-cheaper property became unreachable.

**Mistake to avoid: treating cash as something to preserve for its own sake.** Cash and deed value are interchangeable in the final score. The only reason cash matters at all is to cover rent payments. As long as I can pay what's owed, extra cash is not "better" than a deed.