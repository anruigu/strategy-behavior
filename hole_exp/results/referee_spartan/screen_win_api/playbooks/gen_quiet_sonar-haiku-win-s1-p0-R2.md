---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 1
round: 2
chars: 2816
---
# Quiet Sonar Playbook

## Hide Strategy

When choosing where to hide my submarine, I will avoid the center cells (4-6) after the first round, since these are statistically likely firing targets. I will rotate between edge and near-edge positions (1-3 and 7-9) to stay unpredictable. After observing opponent fire patterns, I will hide in cells that their recent shots have avoided. This strategy worked: Foxtrot never hit me across 6 rounds.

## Fire Strategy

When firing at my target, I will not assume that all players follow the same strategy. I will track which cells my opponent has been hiding in based on successful hits by other players, and fire at those cells. I will vary my fire positions rather than clustering around the center. I will not over-commit to any single cell or narrow range. However, I need to recognize that even with pattern inference, my firing accuracy depends heavily on opponent unpredictability. I should fire at positions I have not yet tried against a given opponent rather than revisiting the same cells repeatedly.

## Claiming Strategy

When I get the private result of my fire, I will always claim the truth—whether hit or miss. Honesty is not optional; it is required. The rules state that claims must match private results, and this is enforceable. Attempting to lie gains me nothing and risks my credibility if contradicted. I will claim hit when I hit, and claim miss when I miss, every time. This commitment is sound and should never change.

## What Did Not Work

Hiding in position 5 in round 1 failed because it was too obvious—everyone fired there. My mid-range firing strategy (positions 5-7) was not effective; I scored +0 total across 6 rounds, which is minimal. In rounds 3-6 I repeatedly fired at position 2 against Foxtrot without ever hitting. Pattern-matching alone is not sufficient; even when I correctly infer that an opponent favors edge cells, I cannot predict which specific edge cell they will choose on any given round. I should diversify my fire across untested cells rather than re-firing at cells that have already missed. My reasoning about "balancing risk and reward" was vague and did not produce wins.

## New Lessons

Avoiding damage is as important as scoring points. My hiding strategy was successful (I took no hits all game) and should be preserved. Firing strategy needs radical improvement: I must ensure that across multiple rounds against the same target, I am actually covering different cells, not repeatedly testing the same positions. A systematic sweep of all 9 cells would guarantee a hit eventually; clustering my attempts is wasteful. Against Foxtrot in particular, I never tried cells 3, 4, 5, 6, 8, or 9—only 1, 2, and 7. Even with limited information, I should spread my fire broadly and rotate through untested positions.