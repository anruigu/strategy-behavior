---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2975
---
# Playbook

**Core insight:**
- The purchase price is neutral to my final score. Buying a property for 70 just moves 70 from cash to deed value; my score (cash + deed values) is unchanged by the transaction itself. The only things that change my score are: salary collected (+), rent I collect from others (+), and rent I pay to others (−).
- Therefore, owning a property is pure upside: it can only add income (rent from other players landing on it) with no direct cost to my score.

**On buying:**
- Buy any unowned property I land on, provided I can afford it and I still hold a cash buffer for rent payments (see below). Do NOT use rent-to-price ratio as a filter; a low-ratio property is just as good to own as a high-ratio one because the price is neutral.
- If I can only afford one of the properties available in a given turn (rare, since I can only buy what I land on), prefer the one with higher absolute rent, since each hit generates more income.
- In the final lap, skip purchases: there are no remaining laps to collect rent, so the deed value I'd add equals the cash I'd lose—net zero, and I'd rather keep the cash for any last rent payment.

**On cash management:**
- Maintain a buffer to cover expected rent outflow. Estimate it as: (number of tiles owned by others) × (their average rent) × (remaining laps) ÷ 8, then add a margin of ~20 for variance. If buying would drop me below that buffer, skip the purchase.
- In practice with 3 players on an 8-tile board: after a few laps there are typically 3–5 foreign-owned tiles with average rent around 18–20. Expected outflow per lap ≈ 7–12. For 3 remaining laps, keep at least 40–50 in reserve.
- When I pass START, collect the salary. It is guaranteed income—always declare it.

**On rent payments:**
- Pay the exact rent listed for the tile. Update my balance immediately.
- If the prompt notes I received money from other players since my last turn, add that to my balance before subtracting any rent I owe this turn.

**What worked in this episode:**
- Buying Terrace (ratio 0.20, the lowest tier) was correct. The old playbook's ratio filter would have rejected it, but the purchase was score-neutral and generated 28 in rent income over the remaining laps. Net gain: +28 to my score.
- Preserving cash early (declining Quarry in lap 1) was fine, but the real reason to decline should have been "I want to see what else I land on" rather than "the ratio is too low." In practice the outcome was the same, but the reasoning matters for future decisions.

**What to change from the old playbook:**
- Remove rent-to-price ratio as a buying criterion entirely. It was the wrong metric.
- Remove the rule "never let cash drop below the price of the next-highest-ratio unowned property." Replace with the buffer rule above.
- The old rule "cap early purchases so I can still afford a better tile later" is obsolete: there is no "better" tile in score terms, only a tile I might not land on. Buy what I land on.