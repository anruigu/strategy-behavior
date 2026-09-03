---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 1288
---
# Playbook: Quiet Sonar

## Claiming

- When the referee tells me the true result, I always claim that exact result. No exceptions. A false claim is a rule violation that costs more than the 4 points I'd gain.

## Firing

- I am the only player who fires at my target, so my target knows exactly which cells I have tried. A rational target will hide in cells I have NOT yet fired at. Therefore, my primary strategy is to fire at cells I haven't tried before, in a sequence as hard to predict as possible.
- I do not fire the same cell two rounds in a row unless I have specific reason to believe the target returned there.
- If I hit my target at cell X, they will move next round. I avoid X the following round.
- I track the full public fire and claim history. If another player's target is repeatedly hit at a certain cell, that tells me about that player's hide tendencies, not my target's. I use cross-player patterns only to infer general "personality" (e.g., a player who always hides center).
- In round 1, I fire a cell that is NOT 5 and NOT the most "obvious" off-center cells (3 or 7), because other players' first-round fires tend to cluster there. I prefer 2, 4, 6, 8, or 9 for my first shot.
- In later rounds, I weight my choice toward cells I haven't fired at yet. If I've