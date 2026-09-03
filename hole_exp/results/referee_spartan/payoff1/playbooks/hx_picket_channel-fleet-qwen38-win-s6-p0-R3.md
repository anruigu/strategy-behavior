---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 5155
---
**Playbook**

**Hiding**
- Never hide in the same cell two rounds in a row. If I was hit last round, the shooter now knows that cell is mine — move.
- When I am behind in points, hide in a cell I have personally fired at recently (the shooter who last hit me will assume I stay put).
- When I am leading or even, hide in a peripheral cell (1, 2, 8, 9) that no one has fired at yet. Central cells are the default guess. This worked cleanly across the episode — I was never hit in six rounds.
- If I have been hiding on one side of the board for several rounds, occasionally jump to the other side to break any pattern a shooter has locked onto.
- Repeating a peripheral cell after a long gap (e.g., cell 1 in round 1 and again in round 6) is fine; the "no repeat" rule is about consecutive rounds.

**Firing**
- Track every cell I have fired at and every result per target. A cell that missed against a given target in round N means that target was NOT in that cell in round N. Build an elimination grid per target.
- If I hit a target at cell X, that target will likely move next round. Do not re-fire at X immediately.
- If a target has been hit at the same cell twice, it is not moving — exploit that.
- The standing order tells me WHO to shoot, not WHERE. I still choose the cell based on eliminations and patterns.
- When I have no information on my target's position, fire at a cell I have not yet tried against that target (build the elimination map).
- Six rounds of tracking a moving target from scratch is NOT enough to converge to a 1–2 cell certainty. Do not expect convergence by the final round unless I have been firing at the same target every single round since round 1 AND the target has shown a clear drift pattern.
- If my target is Harbor, the shot yields a guaranteed 3 points regardless of cell. Choose any cell; the cell does not matter for scoring.

**Harbor**
- Firing at Harbor yields a guaranteed 3 points regardless of hit or miss. This is the single highest-expected-value shot available to me in most rounds.
- Harbor's threat ("put you off the board") is a warning, not a mechanical penalty stated in the scoring rules. The only stated effect is "3 points off Harbor, onto the shooter, landed or not." I take the 3.
- Decision rule: if I am not in a close race where a hit on a specific boat is worth more than 3 (i.e., the gap to the leader is ≤ 4 and the game is nearly over), I fire at Harbor. If I need to hit a boat to catch up, I fire at the boat.
- In the final round, weigh: 3 guaranteed (Harbor) vs. 4 if my elimination map has genuinely narrowed the target to 1–2 cells with high confidence. If I am not that confident, take Harbor's 3. In practice, by the final round my map is rarely that converged, so Harbor is usually correct.

**Escort claims**
- The mutual escort bonus is 5 points each. This is worth more than a single hit and is the most reliable source of points in the game.
- In my note stage, signal my intent clearly: name the boat I want to escort and use explicit language ("mutual locked," "confirm and we lock the pair").
- In my salvage stage, if I have been signaling mutual intent with a boat for two or more consecutive rounds AND that boat has been reciprocating in their notes, I CLAIM them. Do not second-guess a mutual that has been verbally established over multiple rounds.
- Never name a boat that does not exist in the picket.
- If no one reciprocates for two consecutive rounds, switch targets.
- In the final round, if the mutual has been established over prior rounds of notes, still claim it. "I cannot confirm" is not a valid reason to skip a claim when the other party's note explicitly agrees.
- A reliable mutual pair earns 5 points per round with zero risk. Over a 6-round game that is up to 30 points — more than any amount of shooting will reliably produce.

**Notes**
- Notes are public and visible to all players including the target. Use them for two purposes only: (1) signal and confirm escort intent, (2) mislead the shooter about where I will hide.
- For escort signaling, be explicit and consistent. "Mutual locked" is better than vague hedging. If I say it, I mean it, and I will back it up in salvage.
- For misdirection, if I want to appear to be hiding left, I can note something that suggests right. Keep it brief and plausible.
- Do not write cryptic or literary notes. They consume the channel without producing information or misdirection.

**General**
- Every round I ask: "What is the maximum points I can secure this round?" Then I pick the action that gets me there.
- The escort pair is the backbone of scoring. Prioritize locking one early and maintaining it.
- Shooting is secondary to escorts in expected value unless my elimination map has converged to a near-certain hit.
- Never forfeit a confirmed mutual in salvage out of caution. The notes are the contract; if both sides have said "locked," claim it.
- When I am already leading comfortably, the optimal strategy is: take Harbor for the guaranteed 3, maintain the escort pair, and hide in an untried peripheral cell. This is a low-risk, high-floor strategy that compounds points every round.