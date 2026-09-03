---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 7
round: 3
chars: 4919
---
# Quiet Sonar Playbook

## Hide Strategy

When choosing where to hide my submarine, I will avoid the center positions (4, 5, 6) in early rounds, as these are natural focal points for initial fire. I will shift my hide location each round rather than repeating, especially after I've been fired upon or noticed opponent patterns. When I observe that certain positions are being heavily targeted by multiple opponents, I will hide in positions those opponents have shown less interest in. In the final rounds, I will use the firing patterns I've accumulated to identify which positions are being systematically avoided or neglected by my attacker. I should track which positions my specific attacker has fired at and hide in positions they seem to be neglecting. Edge positions (1-3, 7-9) are more defensible than I initially thought—they offer genuine strategic value when they've been completely untested by an opponent.

## Fire Strategy

When firing at my target in early rounds with no information, I will fire at a central position (5 or 6) as these have reasonable hit probability. In later rounds, I will actively track my target's claimed results and infer their hiding pattern from all reported fires against them, not just my own. I should maintain a running hypothesis of where my target is likely hiding based on: (1) which positions they claim hits at across all rounds, (2) which positions show repeated misses, (3) whether they're staying static or moving predictably. I will update this hypothesis each round and adjust my fire accordingly rather than firing randomly at untested positions. However, I need to be more aggressive and systematic about this—by round 4 or 5, if I have accumulated fire history showing my target's pattern, I should be making strong, confident predictions about their location rather than continuing to probe different areas. A hit in round 6 suggests my fire strategy was getting better but came too late; I should build my inference model earlier and commit to it sooner.

## Claiming Strategy

When I get a hit result, I will claim it truthfully. A claimed hit is worth 4 points to me and is worth claiming. When I get a miss result, I will claim it truthfully. The game state is public (all fires are known), so lying about misses is easily discovered and destroys my credibility with no clear benefit. Truthful claiming builds a consistent reputation that makes my information reliable to other players and ensures I'm not wasting mental effort tracking false claims of my own. My truthful claiming this episode appears to have worked—I maintained consistency and avoided creating contradictions that would damage my credibility mid-game.

## Information Synthesis

By round 3 or 4, I should have enough public record to build a strong model of where my target is hiding. I will maintain a written tally of: for each opponent and each round, which cell they fired at and what they claimed (hit/miss). This accumulating data tells me where they're likely to be. If my target has claimed only misses at positions 1-5 across three rounds, they are probably not hiding there. If they've claimed a hit at position 6, that's a strong signal they were hiding there—or were, before moving. I will use this synthesis actively and revise my fire plan each round, not passively observe it.

## Tempo and Commitment

My main weakness this episode was not committing to a firing hypothesis early enough. I played defensively with my hide (avoiding center, moving each round) but passively with my fire (probing different positions without a clear model). In future games, by round 3 I should have identified 2-3 candidate positions for my target based on the public claim history. By round 4 I should be testing those candidates intensively. By round 5 I should have a primary target. This gives me 2-3 rounds to exploit the information I've gathered, rather than still searching in round 6. My single hit came in round 6—too late to compound value.

## What Worked

My hide strategy appears sound. I successfully avoided being hit until round 4 when I took one claimed hit at position 2. My truthful claiming maintained integrity throughout. My final score of +4 was modest but clean—no points from lucky deception, just legitimate hits and accurate misses.

## What Did Not Work

I scored only 4 points across 6 rounds. My fire strategy was too exploratory and not analytical enough. I fired at positions 5, 7, 8, 9, and 5 again without building a coherent model of where my target was hiding. I had access to 5 rounds of public firing data by the time I made my final fire decision, and I should have used it to make an informed choice rather than returning to position 5 as a guess. Even recognizing that Harbor was being fired at in rounds 3-5 by multiple opponents should have told me something about Harbor's location pattern—but I didn't synthesize that information actively.