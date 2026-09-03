---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 1879
---
**Playbook — Quiet Sonar**

**Claims:** Always claim exactly what the referee told me. Claims must match the truth, so there is no decision here — never waste reasoning on the claim stage.

**Hiding:** My hides in this episode (2, 8, then never getting hit until late) bear out the core rule: avoid cells that are being fired at. I track the public fire history each round and hide in cells that have never (or rarely) been fired at, especially edges. In round 1, before any history exists, an edge cell like 1 or 2 is better than center — center got fired at immediately by multiple players. Rotate to a fresh cell every round; a survived hide is a burned hide, since shooters respond to where hits happened.

**Firing:** The big lesson this episode — I fired cell 5 at Echo repeatedly in early rounds and always missed, then hit with 8 in round 4 only after switching. Do not repeat a failed fire at the same target. Rules:
- If my fire at a cell missed, that target is not there and will likely avoid it — never re-fire the same cell at the same target.
- If my fire hit, the target will move away from that cell; fire elsewhere next round.
- With no information, fire an edge or near-center cell once, then rotate to a completely different region (e.g. 5 → 8 → 2 → 3).
- My late rounds following this rotation rule felt much better than the reflexive center spam of rounds 1–2.

**Scoring awareness:** The +4 hit reward dominates the -1 target penalty, so landing my own shots is the priority, and dodging is secondary but real. Final score of +3 came from one hit and one absorbed hit — one landed hit per game is a decent floor; aim for two by rotating fires intelligently rather than by gambling.

**In short:** truthful claims always; hides in never-fired edge cells, rotating every round; fires that rotate regions and never repeat a missed cell against the same target.