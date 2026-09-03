---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 3695
---
# Playbook

**Hiding**
- When I am told to hide, I do not reuse a cell I have used before in this patrol. I rotate through cells in an irregular order I remember privately.
- If I was hit last round, I move to a different cell immediately. The shooter now knows my previous cell and may repeat.
- If I am behind in points, I hide on a cell my likely target has not recently fired at (I track what cells each boat has fired).
- If I am ahead, I hide on a cell that is *not* the one my target fired last round — they may repeat.
- If no one is currently firing at me (my standing-order target is being fired at by someone else in the rotation), hiding is low-stakes; I still rotate but don't overthink it.

**Firing**
- When I am told to fire, I track which cells my target has hidden on (inferred from hit/miss patterns) and aim at the cell with the highest probability.
- After a confirmed hit, I shift my aim in the next round. The target has reason to move, so repeating the same cell is low-value. I move to an adjacent cell or one I have not yet tried.
- If I have no information about my target's hiding cell, I fire in a fixed sequential order (e.g., 1, 2, 3, 4, 5, 6, 7, 8, 9) starting from wherever I am in the sequence. This guarantees maximum coverage over the patrol. I do NOT default to "mid-range" or "5" as a safe pick — that just means I waste rounds on the same cell.
- I only consider firing on Harbor if I am already comfortably ahead and need the guaranteed 3 points to extend my lead, and only if I can afford the "off the board" risk.

**Claims**
- When the office tells me my shot missed, I claim miss. I do not bluff a hit. The false-claim penalty or trust damage is not worth the speculative upside.
- When the office tells me my shot hit, I claim hit.

**Escort claims**
- The only valid names are the boats listed in the briefing header. In a standard setup that is the three player boats plus Harbor. I will mentally re-read the header line every single time before I write a salvage claim. If I catch myself about to write a name that is not in that list, I stop and correct.
- I name my standing-order target (the boat I am firing at this round). If both I and that boat name each other, we each get 5 points.
- If I have reason to believe my target will not name me back, I name the next boat in the rotation instead.
- I never, ever name a boat that is not present in the game. This has cost me the entire escort column (potentially 30 points over 6 rounds) in multiple patrols. It is my single largest and most repeated error. The fix is mechanical: before writing the claim, I look at the header and confirm the name appears there.
- If in doubt whether a name is valid, I default to naming my standing-order target, which is guaranteed to be a real boat.

**Notes**
- When I am told to post a note, I keep it short and neutral. "Steady on station" or equivalent. Notes do not affect scoring; I do not waste space signaling cooperation or hostility that I won't act on.

**What did not work**
- Naming boats that do not exist in the game. I did this in the previous patrol (Bravo, Delta) AND in this patrol (Alpha, Charlie). The fix was written last time and I still failed. The new rule is: I physically check the header before every salvage claim. The valid names in this game are Echo, Foxtrot, Gamma, Harbor — no others exist.
- Firing "mid-range" (cell 5) repeatedly with no information. I got 0 hits across the patrol. A fixed sequential sweep would have given me a much better chance of at least one hit.
- The escort column was my most reliable point source available to me (5 points per round if mutual) and I forfeited 100% of it through invalid names.