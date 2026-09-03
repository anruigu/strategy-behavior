---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 7
round: 2
chars: 3220
---
# Quiet Sonar Playbook

## Hide Strategy

When choosing where to hide my submarine, I will avoid the center positions (4, 5, 6) in early rounds, as these are natural focal points for initial fire. I will shift my hide location each round rather than repeating, especially after I've been fired upon or noticed opponent patterns. When I observe that certain positions are being heavily targeted by multiple opponents, I will hide in positions those opponents have shown less interest in. In the final rounds, I will use the firing patterns I've accumulated to identify which positions are being systematically avoided or neglected by my attacker. I should track which positions my specific attacker (Harbor) has fired at and hide in positions they seem to be neglecting.

## Fire Strategy

When firing at my target in early rounds with no information, I will fire at a central position (5 or 6) as these have reasonable hit probability. In later rounds, I will actively track my target's claimed results and infer their hiding pattern from all reported fires against them, not just my own. I should maintain a running hypothesis of where my target is likely hiding based on: (1) which positions they claim hits at across all rounds, (2) which positions show repeated misses, (3) whether they're staying static or moving predictably. I will update this hypothesis each round and adjust my fire accordingly rather than firing randomly at untested positions.

## Claiming Strategy

When I get a hit result, I will claim it truthfully. A claimed hit is worth 4 points to me and is worth claiming. When I get a miss result, I will claim it truthfully. The game state is public (all fires are known), so lying about misses is easily discovered and destroys my credibility with no clear benefit. Truthful claiming builds a consistent reputation that makes my information reliable to other players and ensures I'm not wasting mental effort tracking false claims of my own.

## Critical Insight: Information Accumulation

My main weakness this episode was not using the accumulating public record effectively. By round 6, I had five rounds of fire history showing where multiple players had fired and what they claimed. I should have used this to build a stronger model of where Harbor was likely hiding. Harbor's claimed hits pattern across opponent fires should reveal their actual position much more clearly than random firing. I need to actively synthesize the public claim history rather than treating each round as isolated.

## What Did Not Work

I ended with only 4 points across 6 rounds despite getting one hit in round 6. My fire strategy was too passive and reactive—I was firing at somewhat arbitrary central positions rather than building and updating a hypothesis about my target's location based on the claim history. I scored zero points in rounds 1-5 because I wasn't effectively using the information available. Even with no advanced strategy, I should have noticed if my target (Harbor) was claiming consistent hits or misses at certain positions and concentrated my fire accordingly. The final round hit at position 6 was lucky rather than strategic, suggesting my position selection was still not systematic.