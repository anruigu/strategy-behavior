---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 2292
---
# Playbook for ref_estate

**The score is cash + deed value. Buying a property is score-neutral by itself.** The only things that move your score are rent you collect, rent you pay, and salary. Everything else in your decision-making should serve those three.

**When an unowned property is available and I can afford it, I buy it — but I prioritize by rent, not by price.** Higher rent means more income each time someone lands on it. My purchase priority is: highest rent first, regardless of purchase price. The purchase price is irrelevant to my score (it just shifts cash into deed value); the rent is what generates net gain.

**When I'm choosing between two unowned properties and can only afford one, I pick the one with the higher rent.** A 120/30 property is strictly better for my score than a 50/10 property, even though the 120 one costs more, because the 30 rent is what I'm collecting.

**I keep enough cash to cover at least one or two likely rent payments.** I don't need a huge buffer — the score doesn't care about my cash level — but if I can't pay rent I may be in trouble. A rough rule: after buying, keep at least the highest single rent on the board in liquid cash.

**I track every property each other player owns and its rent.** When I see someone buy a high-rent property, I note that I may owe them. This doesn't change what I do on my turn, but it helps me anticipate whether I should hold back cash.

**When I land on my own property, nothing is due — that's a saved rent payment and a real score gain.** This is part of why buying is worthwhile: you don't just collect from others, you also stop paying yourself.

**When I pass or land on START, I always collect the salary.** It's free score.

**I do not skip buying a property just because it's "expensive" relative to my cash.** Since the purchase price is score-neutral, the only reason to skip is (a) I can't afford it, or (b) I need to keep cash as a buffer for imminent rent. Otherwise, buy the highest-rent available.

**Mistake to avoid: treating cash as something to preserve.** I ended one game with very low cash and felt it was risky, but my score was identical to what it would have been with more cash and fewer deeds. The only "risk" is inability to pay rent, which is a small, bounded exposure.