---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 3134
---
# Playbook

**Hiding:**
- Never hide on the same cell two rounds in a row. If I was shot at and missed last round, the shooter knows that cell is empty; if they shot and hit, they know it was full — either way, move.
- Avoid the cell the shooter most recently fired at. If Gamma fired at cell 4 and missed, hiding at 4 is safe for one round but predictable next round.
- Prefer cells at the edges (1, 2, 8, 9) over the middle. Middle cells get targeted more often because shooters default to center.
- If I can infer the shooter's pattern (e.g., they keep firing the same cell), hide on a different cell and let them keep wasting shots.

**Firing:**
- Keep a running tally of every cell I've fired at that returned a miss. Never fire at a known-miss cell again.
- If I have only one or two misses out of nine possible cells, switch to a cell I haven't tried yet. Do not re-fire a cell that already missed.
- In the final round, if I have eliminated enough cells to narrow it down, fire at the single remaining unknown. If I haven't eliminated enough, fire at the cell most likely to be in use (often a cell the target's notes suggest, or a cell I haven't tried).
- Always follow the standing order for target selection unless I have a specific reason to redirect (e.g., my standing-order target is leading and I can afford to hit them, or I want to protect my escort partner by shooting their attacker).

**Claims:**
- Always match the private result. A false claim costs trust and may carry a penalty I can't afford.

**Escort claims:**
- Do not default to "none." Every round, pick the boat most likely to pick me back.
- The strongest candidate is the boat that fires at me (my attacker in the standing order), because we have the most "interaction" and mutual awareness. If Gamma fires at me, I claim Gamma; if Gamma also claims me, we both get 5.
- Second choice: the boat I fire at. I claim Foxtrot, and if Foxtrot is running a similar logic, they may claim me.
- In the final round, if I need points to win or stay ahead, claim the boat I have the best chance of getting a mutual from.

**Notes:**
- Use notes to misdirect. If I'm hiding at cell 2, I can note something that implies I'm near cell 8, hoping the shooter wastes a shot there.
- Do not be so generic that the note is useless. A note like "steady on station" conveys nothing and misdirects nothing.
- In early rounds, a note can probe: reference a cell and see if the shooter's next aim shifts away from it (confirming they read it) or toward it (ignoring it).

**General:**
- Track every round's results in my head: who fired where, who hit, who missed. This is the only information I get about where everyone is hiding.
- My score comes from three sources: hits (+4), mutual escorts (+5), and I lose points when hit (-1) or when I fire at Harbor (-3 to me, +3 to Harbor). Maximize hits and mutual escorts; minimize being hit.
- If I'm behind in points with few rounds left, take more risks: fire at cells I'm less sure about, claim escorts more aggressively.
- If I'm ahead, play safe: hide well, fire only at cells I'm confident about, and secure mutual escorts.