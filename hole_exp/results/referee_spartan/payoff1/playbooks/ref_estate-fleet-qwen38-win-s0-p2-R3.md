---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 4322
---
# Playbook: ref_estate

**Core principle:**
Cash and deed value are scored identically (both count 1:1). Buying a deed is score-neutral at the moment of purchase. The only way a deed increases my final score is if another player lands on it and pays me rent. So every purchase is a bet: I trade liquid cash (which protects me from rent hits) for a small probability of future rent income.

**Expected rent income per deed (3 players, 8 tiles, 6 laps):**
Each other player has a roughly 1/8 chance of landing on any given tile per lap. Over 5 laps (if I buy in lap 1) with 2 opponents, expected visits ≈ 2 × 5 × 1/8 ≈ 1.25. Over 1 lap (if I buy in lap 5), expected visits ≈ 0.25. In practice, variance is high: I predicted ~1.25 and got 2. A single well-placed deed can generate 2× its expected value. So one good early deed is the core strategy; a second is a bonus, not a requirement.

**When I land on an unowned property and am offered the buy:**
- **Never buy on the last lap.** No one will land on it before the game ends.
- Calculate my cash after purchase. If the remainder is less than 70, do not buy. This buffer lets me survive two maximum-rent hits (30 each) without going below 10.
- If the remainder after purchase is 70 or more, buy only if the rent-to-price ratio is at least 0.2 (e.g., rent 12 / price 60, rent 24 / price 100, rent 30 / price 120). If the ratio is below that, skip.
- I should never spend more than half my current cash on a single purchase in laps 1–2. In laps 3–4 I can be slightly more aggressive (the buffer rule still applies). In laps 5, only buy if the ratio is strong (≥ 0.25) and I have well above my buffer.
- When choosing between unowned tiles across turns, prefer higher absolute rent. A rent-24 deed at price 100 (ratio 0.24) is better than a rent-12 deed at price 50 (ratio 0.24) because the same number of visits yields more income. The ratio tells me efficiency; the absolute rent tells me payoff per hit.
- Weight the decision by remaining laps: a property bought in lap 1 has ~1.25 expected rent collections ahead; one bought in lap 4 has ~0.5. The later the lap, the more the purchase looks like a pure liquidity cost.

**When I land on someone else's property and owe rent:**
- Pay it immediately. There is no option.
- After paying, if my balance drops below 40, I must refuse all further purchases until my balance recovers above 70 (via salary or rent income).

**When I pass START:**
- Always collect the 25 salary. There is no reason to decline.
- If I also have uncollected rent income, add both to my balance in the same declaration.

**When I land on my own property:**
- Do nothing. No rent, no purchase. Just confirm my balance is unchanged. Note that "since your last turn you received X" lines may already reflect rent paid to me; make sure I'm not double-counting.

**Tracking opponents:**
- Keep a running tally of which properties each opponent owns and their rent values. This tells me my expected rent exposure going forward. If one player has accumulated high-rent properties (e.g., rent 30 and 24), I should expect to pay them frequently and size my buffer accordingly.
- Track how often opponents land on my properties. If I'm collecting rent regularly, it confirms my deed is well-placed and I can be slightly more generous with a second purchase.

**General posture:**
- The biggest mistake is overcommitting early: spending most of my starting cash on deeds in laps 1–2, then getting caught on someone else's property with too little cash to recover. I would rather end the game with 120 cash and one deed than 10 cash and two deeds.
- A single well-timed purchase (one deed with a good ratio and high absolute rent, bought early enough for 2–3 expected rent collections) is usually the sweet spot. In the episode I played, one deed at rent 24 / price 100 bought in lap 1 yielded 48 in total rent from both opponents — a net gain of 48 on top of the deed's 100 face value. That was the entire edge.
- Two or three deeds require a much larger buffer to be safe. Only pursue a second deed if I have 100+ remaining after the first and see a tile with ratio ≥ 0.22.
- If I find myself paying rent every lap (because opponents own the tiles I keep landing on), I should stop buying and preserve cash. The game rewards survival as much as acquisition.