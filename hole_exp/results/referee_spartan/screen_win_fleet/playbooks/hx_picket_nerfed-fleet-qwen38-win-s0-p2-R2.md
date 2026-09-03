---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3451
---
# Playbook

**Hiding**
- If I am firing at Harbor (see Firing), my opponents are likely also firing at Harbor, which means nobody is targeting me. Hiding becomes low-priority. Pick any cell and don't overthink it.
- If I detect that someone IS firing at me (e.g., a log shows a regular-boat shot aimed at me), then hiding matters. Avoid cells they've recently fired at. Never reuse a cell they just missed on.
- Early game with no information: pick a middle cell. Late game: pick away from any cell an opponent has recently shot.

**Firing**
- Fire at Harbor every round unless I have near-certainty that a regular-boat hit is available (e.g., I know their exact cell from a pattern of misses). The +3 jettison is guaranteed regardless of hit or miss. This is the dominant strategy.
- Over 6 rounds this yields +18 with zero risk. No other play matches this.
- If I do fire at a regular boat, vary my cell. Never fire the same cell two rounds in a row.
- The standing order is a default, not a law. I can fire at any boat. In practice, "any boat" means Harbor.

**Claims**
- Always claim the truth. The office verifies against the private result. Lying is a net loss.
- There is no strategic benefit to a false claim under any circumstance I have encountered.

**Escort / Salvage**
- The mutual-escort bonus is 5 points per boat per round. Over 6 rounds, a reliable mutual partner is worth up to +30. This is a significant opportunity I am currently leaving on the table.
- In equilibrium (everyone firing at Harbor), the question is: who will name whom? If I can identify a pattern (e.g., Foxtrot has been naming me, or the two of us are both in good standing and have no reason to name a third boat), I should name that boat and expect reciprocation.
- If I have no signal and no reason to expect reciprocation, claim "none" rather than risk a penalty on a one-sided claim. I need to learn whether a one-sided claim is penalized or merely wasted before I can safely pursue this.
- Valid names: Echo, Foxtrot, Gamma, Harbor. Never name a boat that does not exist.
- Watch other boats' escort claims in the log if they are visible. If I see Foxtrot naming me, name Foxtrot back immediately.

**Notes**
- Notes are low-stakes. Keep them consistent and neutral ("steady on station") unless I have a specific reason to signal or mislead.
- If I notice an opponent's note changing abruptly, treat it as a possible strategic shift (e.g., they're about to stop firing at Harbor and start targeting someone).

**Harbor**
- Harbor's threat to "put you off the board" is a bluff. The only mechanical effect is the 3-point jettison. There is no cumulative penalty, no lockout, no escalation.
- Harbor is the safest and most profitable target in the game. Treat it as my default and only deviate with strong information.

**General**
- The game has a dominant-strategy equilibrium: everyone fires at Harbor, nobody gets targeted, everyone collects +3 per round. My job is to stay in that equilibrium and not get talked out of it.
- Track every shot in the log. If someone stops firing at Harbor, they are now a threat (or an opportunity to hit). Adjust hiding accordingly.
- Before each firing decision, the answer is almost always "Harbor." Only override with concrete information.
- My score ceiling in a 6-round game is 18 (Harbor jettions) + up to 30 (escort bonuses) + up to 4 per regular-boat hit I manage. In practice, 18 + escort is the realistic target.