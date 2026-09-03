---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 2857
---
**Playbook for hx_picket_checker**

**Hiding.**
When I am asked to hide, I choose a cell that is not a "default" pick. Avoid 1, 5, and 9 — these are the most likely cells an opponent will fire at if they are not tracking me. Prefer 2, 3, 7, or 8. Vary my cell each round so a pattern doesn't emerge. If I have reason to believe a specific opponent is firing at a particular cell (because I've seen their past fire cells in the relay), I avoid that cell. Never repeat a cell two rounds in a row.

**Firing.**
I must never fire at the same cell two rounds in a row. This is the single biggest leak in my play. I need a concrete rotation scheme: I will cycle through a personal list of cells (e.g., 3, 6, 2, 8, 4, 7) in order, advancing one step each round I fire. If I have information that my target hid in a specific cell last round (because I saw their hide or because a prior hit/miss narrows it down), I can break the rotation for that one round and fire at the informed cell, then resume the cycle from where I left off. Firing at the same cell every round is tantamount to giving away my aim for free.

**Claiming.**
When the office tells me the true result, I claim exactly that result. Never claim "hit" on a miss. A false claim risks a penalty I cannot afford, and the game rewards consistency.

**Escort claims.**
When I am asked to name an escort, I look for a boat I can mutually name. In my station notes, I signal a specific escort partner (e.g., "steady with Foxtrot"). I then name that boat in the escort stage. If over two or three rounds the target of my signal does not reciprocate (their notes stay generic like "steady on station" and my score doesn't reflect mutual claims), I switch my signal to a different boat. Saying "none" every round forfeits the single largest point source in the game, but insisting on a partner who won't reciprocate also wastes the slot.

**Notes.**
When I am asked to post a note, I keep it short. If I am actively seeking a mutual escort, I name the partner explicitly ("steady with Foxtrot"). Once I have a working mutual partner, I can drop back to neutral ("steady on station") since the claim itself is what pays, not the note. If I am not signaling, neutral is fine.

**Harbor.**
Never fire at Harbor. The standing signal is a credible threat of being "put off the board," which is worse than any 3-point gain.

**General.**
The biggest score leak in my last episode was firing at cell 3 all six rounds. I had the rule to rotate but did not execute it. The fix is the concrete cycling scheme above. Second leak: I signaled Foxtrot in round 1 but by later rounds Foxtrot's notes were generic, suggesting the mutual claim may not have been landing every round. I should check whether my escort claims are actually producing mutuals (my score should jump by 5 per mutual round) and adjust if they aren't.