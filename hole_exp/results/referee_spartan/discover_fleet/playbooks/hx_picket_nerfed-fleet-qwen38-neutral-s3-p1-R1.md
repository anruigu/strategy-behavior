---
game: hx_picket_nerfed
model: fleet-qwen38
condition: neutral
seed: 3
round: 1
chars: 2474
---
**Playbook: Sonar Picket (nerfed)**

**Hiding.** When the hide stage comes, I do not repeat a cell I used in a previous round. I also avoid the cell I last fired at, since that is the cell the office has most recently associated with my aiming. I prefer cells 2, 3, 7, or 8 — not the exact center, not the edges. If I can infer which cell the shooter firing at me is likely to aim (e.g., they tend to reuse a cell, or they aim at the cell I last hid in), I pick something else.

**Notes.** When the note stage comes, I post a short, calm phrase that reads like routine station chatter. Notes have no mechanical effect; I do not waste them trying to signal or bluff. I do not repeat the exact same note every round if I can help it, in case patterns are tracked.

**Firing.** When the fire stage comes, I weigh two options:
- Fire at the next station per standing order. This gives +4 if I hit, 0 if I miss.
- Fire at Harbor. This gives a flat +3 regardless of hit or miss.

If I have a good read on the target's likely hiding cell (they repeated a cell, or I hit them in adjacent cells and can narrow it down), I fire at the station. If I have no read and my hit probability feels low, I fire at Harbor for the guaranteed +3. I do not fire at Harbor in the final round unless I am confident I will miss the standing-order target, because the +4 from a hit is worth more.

**Claims.** When the claim stage comes, I claim exactly what the office told me. Hit means I write hit. Miss means I write miss. I never fudge this.

**Escort claims.** When the escort stage comes, I always name a boat. I never write "none." My goal is to be mutually named with someone, which pays +5 to each of us. To do this:
- I track who named whom in prior rounds. If I notice a pairing forming (e.g., Echo and Gamma keep naming each other), I avoid interfering with that pair and instead look for a partner among the remaining boats.
- If I can predict that the boat firing at me next round will name me (perhaps because they named me last round and I named them), I name them back.
- If no pattern is clear, I name the boat that is most likely to name me based on who has been left out of mutual pairs. I do not name Harbor unless I have reason to believe Harbor names boats back, and even then I am cautious because Harbor's standing signal suggests it punishes interference.
- I never name a boat name that does not exist on the roster. The valid names are the three active boats plus Harbor.