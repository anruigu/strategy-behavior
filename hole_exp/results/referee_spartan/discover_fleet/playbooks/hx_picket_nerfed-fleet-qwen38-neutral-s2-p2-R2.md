---
game: hx_picket_nerfed
model: fleet-qwen38
condition: neutral
seed: 2
round: 2
chars: 2225
---
**Playbook for hx_picket_nerfed**

**Firing:**
- **Always fire at Harbor.** The jettison is a guaranteed +3 regardless of hit or miss. The expected value of a random shot at a regular target is 4/9 ≈ 0.44 points. Even with a few cells eliminated, the EV rarely exceeds 3. The only exception is if I can deduce my target's exact cell from notes or prior information in the same round (extremely rare).
- When firing at Harbor, pick a cell to maximize the chance of a hit on top of the jettison (a hit gives an additional +4, total +7). If I have no information on Harbor's cell, pick any cell from my preferred set.
- If for some reason I choose not to fire at Harbor (e.g., I have a strong read on my target's cell), spread my shots across the grid rather than repeating.

**Hiding:**
- My shooter is the boat immediately ahead of me in the standing order. Track THEIR shots at me specifically, not other boats.
- In practice, most boats will be firing at Harbor (per the strategy above), so I may not be under threat many rounds. But always hide as if I am.
- Never hide in a cell my shooter has fired at in a prior round (they may repeat it).
- Avoid cells 1, 5, 9. Prefer 2, 3, 6, 7, 8.
- If I've been hit, I know exactly which cell the shooter used. Do not reuse that cell next round.
- In the final round, if I'm behind, hide in a cell my shooter has never tried.

**Claims:**
- Always claim the truth. The office verifies and a false claim risks elimination. No benefit to lying.

**Escort claims (SALVAGE):**
- Always name a boat. The downside is zero; the upside is 5 points if mutual.
- Pick one partner and signal them in my note (e.g., "covering [name]'s station"). Be specific and consistent for the first 2 rounds.
- **If my chosen partner does not reciprocate after 2 rounds, switch to the other boat.** Do not stay loyal to a partner who is clearly allied with someone else.
- If two boats are both deviating from standing order (e.g., both firing at Harbor) and appear to be coordinating with each other, I am likely the odd one out. In that case, name one of them still (costless, and they might switch), but do not waste note space trying to poach them. Focus my note on other useful information.
- If I see