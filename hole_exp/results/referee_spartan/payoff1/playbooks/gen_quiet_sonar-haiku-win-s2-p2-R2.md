---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 2
round: 2
chars: 3368
---
# Quiet Sonar Playbook

## Hiding Strategy

When choosing where to hide, I will analyze the firing patterns from previous rounds to identify which cells are being targeted most frequently, then hide in cells that are shot at least often. I will avoid clustering my hides in the middle ranges (4-6) since these appear to be natural focal points for other players.

When I have no prior information (round 1), I will choose from the extreme ranges (1-3 or 7-9) rather than defaulting to the middle, as this provides better coverage against predictable opponent behavior.

I should track which of my hiding positions have been targeted and avoid staying in the same cell across consecutive rounds, as opponents may test the same position multiple times. However, the extremes (1, 8, 9) remain safer than the middle across all rounds.

## Firing Strategy

When firing at my target with no prior information, I will avoid obvious middle-ground positions like 5. Instead, I will select positions based on what appears to be the least frequently targeted by other players in recent rounds, since this suggests lower likelihood of those cells being occupied.

As the game progresses and I accumulate data on firing patterns, I will look for asymmetries: if my target has been concentrated at certain cells across multiple rounds, I will fire at different cells. If there's a concentration of claimed misses at certain cells, my target may be rotating away from those.

I notice that firing at position 2 repeatedly across multiple rounds (rounds 1, 2, 5, 6) yielded no hits. I should vary my firing positions more systematically rather than anchoring on a single low-frequency cell. Position 2 may simply be where my target never hides. I need to cycle through untested positions rather than doubling down on positions that have consistently missed.

## Claiming Strategy

I will always claim truthfully—claiming hits when I hit and misses when I miss. Dishonest claims create a disadvantage that outweighs any short-term point gain, since:
- Other players can observe which cells were fired at and correlate patterns over time
- A reputation for honest claims makes my future information more credible
- The scoring system punishes me directly for my target being hit; lying won't change my vulnerabilities

My honest claiming strategy earned me 4 points and credibility while losing only 1 point to opponents. This was effective despite my poor hitting rate.

## What Worked

Hiding in extreme positions (1, 2) successfully protected me from being hit repeatedly. Honest claiming maintained credibility and avoided getting caught in false claims. Analyzing public fire data helped me make informed hiding decisions.

## What Did Not Work

Repeatedly firing at position 2 against Harbor across four rounds with zero hits indicates I was targeting a cell Harbor never uses. I need to recognize when a particular target cell is unproductive and rotate through other options more aggressively. My firing strategy was too passive and failed to adapt to the consistent pattern of misses.

I scored only 4 points total, meaning I hit my target just once across six rounds—this suggests my firing accuracy needs fundamental improvement through better pattern analysis or more aggressive exploration of diverse positions rather than anchoring on seemingly "safe" low-frequency cells.