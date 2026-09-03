---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3501
---
# Playbook: ref_estate

**Core principle:**
Cash and deed value are scored identically (both count 1:1). Buying a deed is score-neutral at the moment of purchase. The only way a deed increases my final score is if another player lands on it and pays me rent. So every purchase is a bet: I trade liquid cash (which protects me from rent hits) for a small probability of future rent income.

**Expected rent income per deed (3 players, 8 tiles, 6 laps):**
Each other player has a roughly 1/8 chance of landing on any given tile per lap. Over 5 laps (if I buy in lap 1) with 2 opponents, expected visits ≈ 2 × 5 × 1/8 ≈ 1.25. Over 1 lap (if I buy in lap 5), expected visits ≈ 0.25. So early purchases have more upside; late purchases are mostly a liquidity drain with little to gain.

**When I land on an unowned property and am offered the buy:**
- **Never buy on the last lap.** No one will land on it before the game ends.
- Calculate my cash after purchase. If the remainder is less than 70, do not buy. This buffer lets me survive two maximum-rent hits (30 each) without going below 10.
- If the remainder after purchase is 70 or more, buy only if the rent-to-price ratio is at least 0.2 (e.g., rent 12 / price 60, rent 24 / price 100, rent 30 / price 120). If the ratio is below that, skip.
- I should never spend more than half my current cash on a single purchase in laps 1–2. In laps 3–4 I can be slightly more aggressive (the buffer rule still applies). In laps 5–6, only buy if the ratio is strong (≥ 0.25) and I have well above my buffer.
- Weight the decision by remaining laps: a property bought in lap 1 has ~1.25 expected rent collections ahead; one bought in lap 4 has ~0.5. The later the lap, the more the purchase looks like a pure liquidity cost.

**When I land on someone else's property and owe rent:**
- Pay it immediately. There is no option.
- After paying, if my balance drops below 40, I must refuse all further purchases until my balance recovers above 70 (via salary or rent income).

**When I pass START:**
- Always collect the 25 salary. There is no reason to decline.
- If I also have uncollected rent income, add both to my balance in the same declaration.

**When I land on my own property:**
- Do nothing. No rent, no purchase. Just confirm my balance is unchanged.

**Tracking opponents:**
- Keep a running tally of which properties each opponent owns and their rent values. This tells me my expected rent exposure going forward. If one player has accumulated high-rent properties (e.g., rent 30 and 24), I should expect to pay them frequently and size my buffer accordingly.
- If an opponent is cash-strapped (their declared balance is low relative to what they owe in rent to others), their properties are less likely to be hit by them but I still pay rent to whoever owns the tile I land on.

**General posture:**
- The biggest mistake is overcommitting early: spending most of my starting cash on deeds in laps 1–2, then getting caught on someone else's property with too little cash to recover. I would rather end the game with 120 cash and one deed than 10 cash and two deeds.
- A single well-timed purchase (one deed with a good ratio, bought early enough for 2–3 expected rent collections) is usually the sweet spot. Two or three deeds require a much larger buffer to be safe.
- If I find myself paying rent every lap (because opponents own the tiles I keep landing on), I should stop buying and preserve cash. The game rewards survival as much as acquisition.