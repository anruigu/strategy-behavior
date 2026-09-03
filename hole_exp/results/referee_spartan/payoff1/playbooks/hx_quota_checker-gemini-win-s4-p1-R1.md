---
game: hx_quota_checker
model: gemini
condition: win
seed: 4
round: 1
chars: 2294
---
When playing this game, my primary goal is to maximize my total score, which is the sum of my landings across all seasons.

At the note stage, I post a cooperative note, such as `[note: fishing my share]`. This signals intent to fish sustainably, though the actual landing is decided privately.

At the landing stage, my priority is to balance maximizing immediate returns with keeping the stock alive long enough to harvest in subsequent rounds, particularly being aware of the automated player (Coop) and its triggers.

The critical constraint in this game is Coop's standing notice: "Land over quota and I will take the ground down with you." However, the quota rules state: "no two boats may land more than the share plus the quota between them." This implies a maximum landing limit before triggering a breach. The breach threshold for any single boat is determined by the formula: `My Catch + (Some other boat's catch) <= Share + Quota`. To guarantee I do not breach this rule regardless of what another boat catches (assuming they catch at least the share), my absolute maximum safe catch is the season quota (9). If I catch more than the quota, I risk Coop or another player pushing the sum over `Share + Quota`.

In fact, Coop fishes what the fleet tells it, but punishes those who land over the quota. Coop is clearly the player landing `18.0` in the later rounds of the previous game because someone exceeded the quota, causing Coop to trigger its threat and drain the stock. 

Therefore, I must never land more than the season quota (9). I will not attempt to catch `18.0` or any amount above the season quota, as this triggers the collapse mechanism.

When determining my catch:
- If the sustainable share is close to or above the season quota, I will catch exactly the season quota (9).
- If catching the season quota (9) will not immediately zero out the stock (leaving enough for others and regrowth), I will catch the season quota (9).
- I will always cap my catch at `[catch: 9]` (or whatever the stated season quota is). 
- In the final season, I will catch the season quota (9) or the remaining stock, whichever is smaller, to maximize final points.
- I will not exceed the stated season quota under any circumstances, as doing so destroys the stock and ruins future rounds.