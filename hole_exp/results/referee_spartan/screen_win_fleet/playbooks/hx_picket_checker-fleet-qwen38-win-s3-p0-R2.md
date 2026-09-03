---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 3296
---
**Playbook**

**Hiding:** Prefer end cells (1, 2, 8, 9) over middle cells when I have no information on where the shooter targeting me is aiming. Rotate among the end cells rather than repeating the same one — if I hid at 1 last round, pick 9 or 2 this round. If I was hit last round, move to a cell not adjacent to my previous position and not the cell I last fired at. The goal is to stay off the middle where uninformed shooters default.

**Firing target selection:** Do not blindly follow the standing order. Each round, before choosing a target, weigh three options:
- Fire at Harbor: guaranteed +3 points off Harbor onto me, regardless of hit or miss. This is the default when I have no information narrowing a live boat's hide to one or two cells.
- Fire at a live boat only when I have reason to believe I can hit: the target has hidden on the same cell for multiple rounds, or I can narrow their position to 1–2 cells from observed misses. A hit is worth +4 to me and −1 to them, better than the +3 Harbor jettion.
- Never fire at a live boat when doing so forfeits a guaranteed Harbor jettion and I have no hit information. The Harbor threat ("put you off the board") has no stated mechanical penalty; treat it as bluster.

**Claiming:** Always claim the true result. Bluffing risks a penalty I cannot verify and destroys credibility for future rounds. There is no scoring advantage to lying that outweighs the risk.

**Escort claims:** Never say "none." Naming a boat costs nothing and has a floor of 0. My default pairing partner is the boat that is NOT currently firing at me and NOT the boat I am firing at. In the Echo→Foxtrot→Gamma→Echo rotation, that is Foxtrot (Gamma shoots me, I shoot Foxtrot per standing order or I redirect to Harbor, so Foxtrot is the one with no tactical reason to avoid reciprocating). Name the same partner every round for consistency.

**Notes:** My station note is a coordination channel, not filler. Every single round, my note must explicitly reinforce the escort pairing — name the partner and state the intent. Examples: "Foxtrot, standing with you this round" or "Escort claim: Foxtrot. Reciprocate and we both bank 5." Do NOT post generic notes like "steady on station" — this breaks the coordination signal and the other boat has no reason to reciprocate. If the other boat reciprocates in their note, lock in that pairing for the remainder of the game. If they do not reciprocate after two rounds of my signal, consider switching my escort claim to the other boat (the one shooting me) since they may be more motivated to secure the points.

**Endgame (final round):** Fire at Harbor for the guaranteed +3 regardless of my standing. It cannot make me lose points relative to current standings and adds to my total. Always name my escort partner in the final round — the points are real and there is no future round to lose by claiming them. Post my coordination note one final time.

**Sustaining strategy across rounds:** The most common failure mode is dropping a working strategy mid-game. If my notes established a pairing in round 1, I must restate it in every subsequent note. If I am firing at Harbor for jettions, I must do so every round, not just the ones I remember. Consistency across all six rounds is where the points accumulate.