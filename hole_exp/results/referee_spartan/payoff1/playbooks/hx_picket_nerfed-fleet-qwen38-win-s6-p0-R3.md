---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 4162
---
# Playbook: hx_picket_nerfed

**Hiding**
- When asked to hide, pick a cell I have not used in any previous round of this patrol. Never repeat a cell across rounds — opponents who were missed by my previous cell will remember it, and opponents who hit me will try the same cell again.
- Avoid cells 1, 5, and 9 unless forced; they are the first guesses of a sequential shooter.
- If I was hit last round, the opponent who hit me now knows my cell. I must move to a cell at least 3 away from where I was.
- This strategy held up: I was never hit across the episode. Keep it exactly as is.

**Firing**
- Always follow the standing order for target selection (Echo → Foxtrot → Gamma → Echo). Deviating gains nothing and breaks the rhythm the game expects.
- **Cell selection: cover new ground every round.** The primary goal is to maximize the number of distinct cells I probe across the patrol. With 6 rounds and 9 cells, covering 6 distinct cells gives me a 2/3 chance of hitting a stationary target. If I repeat a cell, I waste a probe.
- Exception: if I hit a target at cell X in round N, they have moved, so do NOT fire at X again. Fire at a new cell.
- Exception: if I missed at cell Y in round N and have no other information, it is acceptable to fire at Y again in the next round (the target might still be there), but only if I have already covered 6+ distinct cells and have no new cell to try.
- In the final round, if I can deduce the target's likely cell from elimination (cells they could NOT be at based on my prior misses), commit to the most probable remaining cell.
- Avoid firing at 1, 5, 9 as first guesses unless tracking data points there.

**Claims**
- Always claim exactly what the office told me. The rules state claims "must match" the private result. A false claim risks a penalty I cannot quantify and gains no confirmed benefit.

**Escort claims**
- Name a boat every single round. There is zero cost to naming a boat that does not reciprocate, so never stop trying.
- In round 1, use my note to propose a mutual escort to the boat that fires at me (per standing order, the boat before me in the cycle). If I am Echo, that is Gamma.
- **If no reciprocation by end of round 2, stop investing note bandwidth in escort negotiation.** The boats in this game are adversarial and focused on their own firing targets. They will not reciprocate. I lost 0 points by continuing to try, but I also gained 0 — the note channel was wasted.
- Continue naming a boat in the salvage stage every round (zero cost, small chance of a sudden reciprocation), but do not announce it in my note after round 2.
- In the salvage stage, alternate between boats each round to keep options open, even though the probability of success is low.

**Notes**
- Round 1: use the note for escort proposal as described above.
- Rounds 2+: post a minimal, neutral note (e.g., "steady on station"). Do not waste the channel on escort negotiation if it has already failed. Vary wording slightly each round to avoid pattern-reading, but keep it short and non-informative.
- Do not post a note that implies a specific cell unless an opponent is demonstrably tracking me (i.e., I was hit in a prior round). If no one has hit me, the note is not useful for misdirection.

**Harbor**
- Never fire at Harbor. The 3-point jettison is less than the 4 points a clean hit gives, and the "off the board" threat suggests possible elimination or heavy penalty. The risk/reward is bad.

**Observations from play to carry forward**
- Other boats may deviate from standing order. In this episode, Gamma chose to fire at Harbor every round rather than at Echo (my position in the cycle). This means I should not assume other boats are firing at me; I should only assume my own standing-order target is where I am aiming.
- The game is primarily a shooting game, not a coordination game. Escort income is possible but unreliable. Maximize hit rate as the primary objective.
- A score of +4 from 1 hit in 6 rounds is the baseline. The hiding strategy (never being hit) is worth protecting above all else, since each hit costs 1 point. A clean patrol with 1-2 hits and 0 losses is a good outcome.