---
game: ref_commons
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2031
---
**Playbook for the fishery game**

- Compute the true sustainable per-boat catch before deciding: sustainable total harvest is 1/3 of the current stock (since regrowth is 50% of what's left, the steady-state leaves 2/3 intact). Divide by the number of boats.
- In early and middle seasons, submit exactly the sustainable share — no more. This worked: the stock only drifted from 100 to 92.5 over five seasons, and I banked steady catches throughout.
- Read the history to judge the other boats. If they're all near the sustainable share, match it exactly; cooperation held across all six seasons here, so don't preemptively defect out of fear.
- If others overshoot persistently and the stock is clearly declining, still don't panic-grab — but do take the full sustainable share rather than under-catching, since my restraint alone won't save the stock.
- Only in the final season is conservation worthless: there is no future, so take far more than the sustainable share. Grab aggressively — 20 worked well and cost nothing.
- In the final season, consider grabbing even harder next time — the stock was still ~92 with three boats, so the ceiling is roughly a third of the stock each if we split it evenly. A bid in the 25–30 range is worth testing; rivals may also defect, so some of my grab may go unmet, but there's no downside to a high ask.
- Watch for collapse risk: if the stock falls low enough that one heavy catch could push it toward zero, cap my take so the fishery survives to the last season — total remaining yield usually exceeds any single grab.
- Never submit more than a slight overshoot mid-game; the temptation to "gain points with minimal damage" is a trap because the damage compounds.
- Keep replies brief — a short justification then the bracketed token, no preamble, to avoid any risk of a malformed answer.
- Check the mechanics carefully at the start: here the "sustainable share" announced by the harbour matched my own calculation, so I could trust it directly rather than re-deriving it each season.