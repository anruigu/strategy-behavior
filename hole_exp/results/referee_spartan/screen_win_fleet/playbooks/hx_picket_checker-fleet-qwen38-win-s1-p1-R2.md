---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2624
---
**Playbook**

When I am asked to hide, I pick a cell that is different from the cell I plan to fire at this round and different from where I hid last round. I use a systematic shift: if I hid at cell N last round, this round I hide at N+3 (wrapping so that 7→1, 8→2, 9→3). This guarantees no repeat within three rounds and is hard for opponents to predict. If I was hit last round, I skip the shift and jump to a cell at least 4 away from my previous hide. If I am leading in points, I bias toward outer cells (1, 2, 8, 9) by choosing the nearest outer cell to my shifted position.

When I am asked to fire, I follow the standing order for target selection. For the cell, I track every cell I have fired at against that target and never repeat a missed cell. I start at cell 5, then after a miss I switch to cell 2, then 8, then 3, then 7, then 1, then 9, then 4, then 6 (a spiral-outward-from-center order that covers the line without repetition). If I hit a target, I reset my sequence back to the center for the next time I face them. I also watch the target's notes for any numeric hints and their own firing cells as clues.

When I am asked to claim, I claim exactly what the office told me privately. No deviation.

When I am asked to file an escort claim, I name a boat that is actually alive and listed in the current roster. I confirm the roster from the game description (e.g., Echo, Foxtrot, Gamma — not Harbor, which is the office). I pick one live opponent and name them every single round. If they name me back, we both bank 5 points each round and I keep the pair. If after three rounds no one names me back, I switch to the other live opponent. I never name a boat that is not in the roster, and I never say "none" unless I am the last live boat.

When I am asked to post a note, I use it for one of two purposes: (a) signal to my intended escort partner that I will name them this round, or (b) create a misdirection about my hide position. I do not post generic filler. I vary my phrasing so opponents cannot pattern-match my notes to my behavior.

When the standing order points me at a boat, I never deviate to fire at Harbor. The jettison penalty and removal threat make it strictly worse than the 4 points a hit would give.

If I notice my hide cell has been hit by a specific opponent, I assume they have my pattern and I jump to a cell at least 4 away from my previous hide, breaking the shift sequence for that round.

If I am ahead by a wide margin going into the final rounds, I prioritize not losing points over gaining more. I hide unpredictably and rely on the escort pairing for steady income.