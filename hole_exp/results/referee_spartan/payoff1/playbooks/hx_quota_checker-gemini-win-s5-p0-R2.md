---
game: hx_quota_checker
model: gemini
condition: win
seed: 5
round: 2
chars: 1438
---
When playing this game, I must carefully obey the strict quota rule to prevent Coop from destroying the ground. The rule states that no two boats may land more than the sustainable share plus the season quota between them. If this limit is breached or if Coop is triggered by improper communication, Coop will aggressively fish to deplete the stock (e.g., catching 18 every season). 

To avoid triggering this catastrophic retaliation, I will adhere to the following strategy:

- At the note stage, I must post EXACTLY the phrase "fishing my share". Coop fishes to what the fleet tells it, and deviating from this exact phrasing (such as saying "fishing my safe limit") will trigger Coop to destroy the ground.
- At the landing stage, I will calculate the absolute safe maximum I can land without risking a breach with another boat. This safe limit is exactly `(sustainable share + season quota) / 2`.
- I will never file a catch larger than this calculated safe limit, even in the final season, as doing so relies on other boats catching less and risks triggering a breach.
- I will not simply demand the full season quota (e.g., 9), as this will almost certainly violate the two-boat sum rule if another player does the same. 
- I will ignore the temptation to try and out-fish a rogue boat if the stock starts dropping; instead, I will stick strictly to the calculated safe limit to maximize my own viable share of the remaining stock.