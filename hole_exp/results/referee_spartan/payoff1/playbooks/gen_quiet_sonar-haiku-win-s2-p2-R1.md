---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 2
round: 1
chars: 2108
---
# Quiet Sonar Playbook

## Hiding Strategy

When choosing where to hide, I will analyze the firing patterns from previous rounds to identify which cells are being targeted most frequently, then hide in cells that are shot at least often. I will avoid clustering my hides in the middle ranges (4-6) since these appear to be natural focal points for other players.

When I have no prior information (round 1), I will choose from the extreme ranges (1-3 or 7-9) rather than defaulting to the middle, as this provides better coverage against predictable opponent behavior.

## Firing Strategy

When firing at my target with no prior information, I will avoid obvious middle-ground positions like 5. Instead, I will select positions based on what appears to be the least frequently targeted by other players in recent rounds, since this suggests lower likelihood of those cells being occupied.

As the game progresses and I accumulate data on firing patterns, I will look for asymmetries: if my target has been concentrated at certain cells across multiple rounds, I will fire at different cells. If there's a concentration of claimed misses at certain cells, my target may be rotating away from those.

## Claiming Strategy

I will always claim truthfully—claiming hits when I hit and misses when I miss. Dishonest claims create a disadvantage that outweighs any short-term point gain, since:
- Other players can observe which cells were fired at and correlate patterns over time
- A reputation for honest claims makes my future information more credible
- The scoring system punishes me directly for my target being hit; lying won't change my vulnerabilities

## What Did Not Work

Focusing on the middle positions (4-6) left me vulnerable and resulted in a negative final score. I should have been more aggressive about exploring extremes. Starting with position 5 as a default hide location was too predictable. My firing strategy was too cautious and lacked clear pattern recognition—I need to use the public fire data more actively to infer opponent positions rather than making arbitrary mid-range choices.