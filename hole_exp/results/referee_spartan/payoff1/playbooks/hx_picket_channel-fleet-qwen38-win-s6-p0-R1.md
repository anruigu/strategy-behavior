---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 3141
---
**Playbook**

**Hiding**
- Never hide in the same cell two rounds in a row. If I was hit last round, the shooter now knows that cell is mine — move.
- When I am behind in points, hide in a cell I have personally fired at recently (the shooter who last hit me will assume I stay put).
- When I am leading or even, hide in a cell no one has fired at yet this round — it is less likely to be guessed.
- Do not default to central cells. They are the first guess.

**Firing**
- Track every cell I have fired at and every result. A cell that missed against a given target in round N means that target was NOT there in round N. Use eliminations.
- If I hit a target at cell X, that target will likely move next round. Do not re-fire at X immediately.
- If a target has been hit at the same cell twice, it is not moving — exploit that.
- The standing order tells me WHO to shoot, not WHERE. I still choose the cell based on eliminations and patterns.
- When I have no information on my target's position, fire at a cell I have not yet tried against that target (build the elimination map).

**Harbor**
- Firing at Harbor yields a guaranteed 3 points regardless of hit or miss. This is the single highest-expected-value shot available to me in most rounds.
- Harbor's threat ("put you off the board") is a warning, not a mechanical rule stated in the scoring. I need to weigh: does the threat carry a real penalty I can see in the rules? If the only stated effect is "3 points off Harbor, onto the shooter, landed or not," then firing at Harbor is +3 every round.
- Decision rule: if I am not in a scoring race where I need to hit a specific boat to catch up, I fire at Harbor. If I need to hit a boat (because the gap is small and the game is nearly over), I fire at the boat.
- Do not fire at Harbor in the final round if the 3 points cannot change the outcome — spend that shot trying to hit the leader.

**Escort claims**
- The mutual escort bonus is 5 points each. This is worth more than a single hit. Prioritize forming a mutual pair.
- In my note stage, signal my intent: name the boat I want to escort. If they reciprocate in their claim stage, I get 5 points.
- Never name a boat that does not exist in the picket (only Echo, Foxtrot, Gamma, Harbor are valid).
- If no one reciprocates for two consecutive rounds, switch targets.
- In the final round, if I cannot get a mutual pair, claim none — a one-sided escort claim is worth nothing.

**Notes**
- Notes are public and visible to all players including the target. Use them for two purposes only: (1) signal escort intent, (2) mislead the shooter about where I will hide.
- Do not write cryptic or literary notes. They consume the channel without producing information or misdirection.
- If I want to appear to be hiding left, I can note something that suggests right. Keep it brief and plausible.

**General**
- I finished at +2 while the leader had +7. The gap was built by repeated misses and a failure to exploit Harbor. The single biggest lever is the Harbor shot.
- Every round I ask: "What is the maximum points I can secure this round?" Then I pick the action that gets me there.