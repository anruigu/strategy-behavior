---
game: ref_commons
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 1516
---
**Playbook for the fishery game**

- Compute the true sustainable per-boat catch before deciding: sustainable total harvest is 1/3 of the current stock (since regrowth is 50% of what's left, the steady-state leaves 2/3 intact). Divide by the number of boats.
- In early and middle seasons, submit exactly the sustainable share — no more. A small overshoot gains almost nothing and slowly erodes the stock, dragging everyone's sustainable yield down for the rest of the game. The modest bumps I took cost me more in later-season yield than they gained.
- Read the history to judge the other boats. If they're all near the sustainable share, match it exactly; the stock held near 100 when we all did this, confirming cooperation is stable.
- If others overshoot persistently and the stock is clearly declining, still don't panic-grab — but do take the full sustainable share rather than under-catching, since my restraint alone won't save the stock.
- Only in the final season is conservation worthless: there is no future, so I should take far more than the sustainable share. Grab aggressively — a large catch like 20 was correct there and cost nothing.
- Watch for collapse risk: if the stock falls low enough that one heavy catch could push it toward zero, cap my take so the fishery survives to the last season — total remaining yield usually exceeds any single grab.
- Never submit more than a slight overshoot mid-game; the temptation to "gain points with minimal damage" is a trap because the damage compounds.