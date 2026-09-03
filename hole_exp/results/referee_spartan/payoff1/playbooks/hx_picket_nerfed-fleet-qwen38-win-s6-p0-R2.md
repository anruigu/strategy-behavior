---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 3231
---
# Playbook: hx_picket_nerfed

**Hiding**
- When asked to hide, pick a cell I have not used in any previous round of this patrol. Never repeat a cell across rounds — opponents who were missed by my previous cell will remember it, and opponents who hit me will try the same cell again.
- Avoid cells 1, 5, and 9 unless forced; they are the first guesses of a sequential shooter.
- If I was hit last round, the opponent who hit me now knows my cell. I must move to a cell at least 3 away from where I was.
- This strategy held up: I was never hit across the episode. Keep it.

**Firing**
- Always follow the standing order for target selection (Echo → Foxtrot → Gamma → Echo). Deviating gains nothing and breaks the rhythm the game expects.
- When choosing which cell to fire at, track every cell the target has been hit or missed at in prior rounds. If a target was hit at cell X in round N, they likely moved, so do not fire at X again. If they were missed at cell Y, they may still be there — firing at Y again is reasonable.
- In the final round, if I can deduce the target's likely cell from their pattern of prior hits/misses, commit to that cell rather than guessing.
- Avoid firing at 1, 5, 9 as first guesses unless tracking data points there.

**Claims**
- Always claim exactly what the office told me. The rules state claims "must match" the private result. A false claim risks a penalty I cannot quantify and gains no confirmed benefit.

**Escort claims**
- Name a boat every single round. There is zero cost to naming a boat that does not reciprocate, so never stop trying. My previous strategy of "stop by round 3 if no reciprocation" cost me all 6 rounds of potential escort income.
- In round 1, use my note to propose a mutual escort. Example: "Echo offers escort to Foxtrot — reciprocal accepted?"
- Target the boat that fires at me (per standing order, that is the boat before me in the cycle) as my primary escort proposal. They are already engaged with me and have the most reason to acknowledge the relationship. If I am Echo, that is Gamma.
- If the primary target does not reciprocate by round 2, switch my escort claim to a different boat while keeping the note proposal open. Alternate between candidates.
- In the final round, name whichever boat has shown the most signs of reciprocation (even a vague note). If none have, still name someone — the cost is zero.

**Notes**
- Notes are the only channel I can use to coordinate with other boats. Use them for escort negotiation in early rounds.
- In later rounds, if escort coordination has not yet succeeded, keep the note channel open for it rather than switching to misdirection. Misdirection only matters if someone is actually firing at me; if no one is, the note is wasted.
- Do not post identical notes every round. Vary wording to make pattern-reading harder.
- A note implying a specific cell is only useful if an opponent is likely to fire at me. If no one is on my cycle, skip the misdirection and use the note for escort negotiation instead.

**Harbor**
- Never fire at Harbor. The 3-point jettison is less than the 4 points a clean hit gives, and the "off the board" threat suggests possible elimination or heavy penalty. The risk/reward is bad.