---
game: gen_quiet_sonar
model: haiku
condition: neutral
seed: 2
round: 3
chars: 3898
---
# Quiet Sonar Playbook

## Hiding Strategy

When choosing where to hide my submarine, I will avoid positions 5-8 in early rounds, as this middle-to-upper range gets probed repeatedly by opponents. I'll rotate between lower positions (1-4) and higher positions (8-9) based on the patterns I observe in opponent firing.

When I see opponents consistently firing at a particular position across multiple rounds while claiming misses, those positions become safe to hide in—their pattern suggests they've already ruled them out.

When hiding in the final round, I will choose a position that hasn't been the focus of observed firing patterns from my specific target. I should track which positions my target has already probed and avoid those, then select from the remaining untested positions.

## Firing Strategy

When I fire at my target each round, I will start by probing middle positions (4-6) in early rounds to gather initial information about my target's likely location.

After observing opponent firing patterns across multiple rounds, I will track which positions they've already fired at and claimed misses on. These positions become increasingly unlikely to contain my target on repeat attempts.

I will systematically identify gaps in my target's firing pattern—positions they have NOT fired at across all observed rounds. These gaps represent untested territory where my target may be hiding, since they clearly don't expect fire there.

In mid-game rounds (3-5), I should focus on positions my target has explicitly avoided firing at. If my target fires at positions 3, 5, 6, and 8 across multiple rounds but never fires at position 4, that gap in their pattern is a strong signal. Position 4 becomes a high-priority firing target.

In the final round, I can afford to fire at any position since there's no recovery opportunity afterward. I will commit to firing at the largest gap in my target's observed firing pattern—the position they have most consistently avoided—based on accumulated evidence across all rounds.

## Claiming Strategy

When I fire and receive the true result, I will always claim truthfully—hit or miss—matching exactly what the referee told me. Since all fires are public, false claims cannot be sustained and risk damaging my credibility. Credibility matters in a multiplayer game because opponents' behavior and information-sharing may be influenced by whether they trust me.

## Critical Pattern Recognition

Across the episodes I have played, I finally achieved a hit in round 6 of the most recent episode by firing at position 4. This success came after identifying that Foxtrot had fired at positions 3, 5, 6, and 8 across rounds 3-5 but had never fired at position 4. This gap in their firing pattern was the key signal I should have been tracking all along.

My previous strategy of trying to identify where Foxtrot hides based on general clustering patterns was ineffective. The more reliable signal is the inverse: where does my target NOT fire? That untested gap is where they are likely hiding.

Foxtrot's firing shows a rotating pattern (5, 7, 8 in early rounds; 2, 5, 6 in middle rounds; 3, 5, 6 in later rounds) but this rotation is not random—they consistently avoid certain positions. Position 4 was avoided in the most recent episode's rounds 3-5. Position 1 and 9 (the extreme edges) should also be tracked for avoidance patterns, as should positions 7 (especially after being hit there in round 1) and others.

I should maintain a cumulative record of which positions my target has NEVER fired at across the entire episode. The position with the longest avoidance streak is my best firing target for the final round.

I should not waste attempts trying to predict rotating hiding positions. Instead, I should focus entirely on identifying and exploiting gaps in my target's offensive firing pattern. Where they don't shoot, they likely hide.