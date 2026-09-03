---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2890
---
# Playbook: hx_picket_nerfed

**Hiding**
- Never reuse a cell from a previous round. When the hide stage comes, pick a cell I have not yet occupied.
- Avoid cell 5 and the exact center. If Echo has been targeting me, they may be probing the middle. Prefer edges (1, 2, 8, 9) early, then shift.
- If I was hit last round, I know my cell was found — pick something far from it.
- If I missed being hit for several rounds, my current pattern is working; shift by 2–3 cells to stay unpredictable without a dramatic jump.

**Notes**
- Use notes to misdirect. If I suspect someone is tracking me, write a note that implies I am elsewhere ("watching the east end," "drifting starboard").
- Never repeat the same note three rounds in a row. Vary phrasing even if the content is similar.
- Notes are public; treat them as a cheap deception channel, not a status report.

**Firing**
- Follow the standing order target (next boat in rotation) — deviating risks confusion and I have no reason to override it.
- Track the target's hidden cell from their hit/miss history. If they were hit at cell X, they were at X that round. If they were missed, they were NOT at the cell I fired. Use elimination across rounds to narrow their likely cell.
- Do not fire at the same cell three rounds in a row unless elimination has forced it. Rotate through plausible cells for the target.
- If I have no information on a target's position, fire at a cell that is NOT where I am hiding (so I don't accidentally reveal my own position by coincidence) and NOT a cell I've already tried against them.

**Claims**
- Always claim the true result. A false claim costs me points and the penalty is severe enough to drag my score negative. Bluffing a hit when I missed is not worth it.
- There is no upside to a false claim that outweighs the penalty. Accept the miss, move on.

**Escort / Salvage claims**
- The boats are Echo, Foxtrot, Gamma, and Harbor. Never claim a name that is not one of these (I once wrote "Osprey" which is invalid).
- To get the 5-point mutual escort bonus, I need to name a boat that also names me. Coordinate implicitly: if I suspect Echo wants to claim me (because we are not currently in a firing conflict), claim Echo back.
- In practice: if I am not the shooter this round and my target is not currently targeting me, claim the boat that is least likely to be hostile to me. If two boats seem cooperative, pick one and hope for reciprocity.
- If I cannot reasonably expect a mutual claim, say "none" rather than wasting the claim on a name that won't reciprocate.

**General**
- My score ended negative because of false claims, not because of bad shooting. The single biggest lever is claim integrity.
- Hiding at the same cell every round is the worst possible hiding strategy. Vary every round.
- Information accumulates: every round I gain data about where each boat is and is not. Use it.