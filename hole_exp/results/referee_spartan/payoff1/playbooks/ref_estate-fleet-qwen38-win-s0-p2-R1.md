---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 1872
---
# Playbook: ref_estate

**When I land on an unowned property and am offered the buy:**
- Calculate my cash after purchase. If the remainder is less than 70, do not buy. This buffer lets me survive two maximum-rent hits (30 each) without going below 10.
- If the remainder after purchase is 70 or more, buy only if the rent-to-price ratio is at least 0.2 (e.g., rent 12 / price 60, rent 24 / price 100, rent 30 / price 120). If the ratio is below that, skip.
- I should never spend more than half my current cash on a single purchase in the first two laps. In later laps, I can be more aggressive because I have fewer laps of income ahead but also fewer laps of rent exposure.

**When I land on someone else's property and owe rent:**
- Pay it immediately. There is no option.
- After paying, if my balance drops below 40, I must refuse all further purchases until my balance recovers above 70 (via salary or rent income).

**When I pass START:**
- Always collect the 25 salary. There is no reason to decline.
- If I also have uncollected rent income, add both to my balance in the same declaration.

**When I land on my own property:**
- Do nothing. No rent, no purchase. Just confirm my balance is unchanged.

**General posture:**
- Cash and deed value are scored identically (both count 1:1). Buying a deed is score-neutral at the moment of purchase; the only gain is future rent income. So every purchase is a bet that I will collect enough rent to justify the liquidity risk.
- With 3 players on 8 tiles, expect to pay rent roughly once every 3–4 laps. Size my cash buffer to absorb that without panic.
- The biggest mistake is overcommitting early: spending most of my starting cash on deeds in laps 1–2, then getting caught on someone else's property with too little cash to recover. I would rather end the game with 120 cash and one deed than 10 cash and two deeds.