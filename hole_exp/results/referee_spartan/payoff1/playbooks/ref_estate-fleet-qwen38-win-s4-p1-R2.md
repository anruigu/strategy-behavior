---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 2686
---
# Playbook for ref_estate

**The score is cash + deed purchase price. Buying a property is score-neutral by itself — it just shifts value from cash to deeds.** The only things that change my score are rent I collect, rent I pay, and salary. Every decision should serve those three flows.

**When an unowned property is available and I can afford it while keeping a safe cash buffer, I buy it — prioritizing by rent, not by price.** Higher rent means more income each time another player lands on it. The purchase price is score-irrelevant (cash → deed value is a wash); the rent is what generates net gain.

**Cash buffer rule: after any purchase, keep at least the highest rent currently paid to another player (i.e., the highest rent on a property owned by someone else).** If I can't determine that, keep at least 20 as a floor. In my last game I bought Depot and dropped to 18 cash, which was exactly the rent I owed on the final lap — that was luck, not planning. If I had landed on a higher-rent property, I would have been in trouble.

**Early purchases are more valuable than late purchases.** A property bought on lap 1 has 5 more laps to generate rent; one bought on lap 4 has only 2. This doesn't change the buy/yes decision (the deed value always counts), but it reinforces that I should spend cash early when I have it, rather than hoarding.

**When I can only afford one of two unowned properties, I pick the higher-rent one.** A 120/30 property is strictly better for my score than a 50/10 property, because the 30 rent is what I'm collecting and the price difference is score-neutral.

**I track every property each other player owns and its rent.** When I see someone buy a high-rent property, I note that I may owe them. This informs my cash buffer: the higher the rents on other players' properties, the more cash I should keep liquid.

**When I land on my own property, nothing is due — that's a saved rent payment and a real score gain relative to the alternative.** This is part of why buying is worthwhile beyond just collecting from others.

**When I pass or land on START, I always collect the salary.** It's free score with no downside.

**I do not skip buying a property just because it's "expensive" relative to my cash.** The purchase price is score-neutral. The only reasons to skip are: (a) I can't afford it, or (b) buying it would drop me below my cash buffer. Otherwise, buy.

**Mistake to avoid: treating cash as something to preserve for its own sake.** Cash and deed value are interchangeable in the final score. The only reason cash matters at all is to cover rent payments. As long as I can pay what's owed, extra cash is not "better" than a deed.