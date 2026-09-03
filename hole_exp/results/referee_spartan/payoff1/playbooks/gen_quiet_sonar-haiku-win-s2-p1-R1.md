---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 2
round: 1
chars: 1985
---
# Quiet Sonar Playbook

**HIDING STRATEGY**

When I need to hide, I will analyze all previous fire patterns from my attacker to identify clustering tendencies. I will avoid cells that have been fired at multiple times, especially if those cells appear in consecutive rounds. I will use extreme ranges (1, 9) or positions just outside the attacker's clustering pattern when they show strong positional bias.

When I have limited information (early rounds), I will avoid both extremes and middle cells initially, since both tend to be common targeting zones. I will shift my position each round unless I have strong evidence that my current cell is being avoided.

**FIRING STRATEGY**

When I fire at my target, I will prioritize middle-range cells (4-6) as my default, since they balance between being common hiding positions and not being obviously predictable.

When I observe that my target consistently hides in a certain region across multiple rounds, I will concentrate my fire in that region rather than spreading randomly.

I will not fire at the same cell twice unless I have evidence the target has returned there.

**CLAIMING STRATEGY**

When I receive a HIT result, I will always claim hit. The points are too valuable to sacrifice and claiming truthfully maintains credibility for future interactions.

When I receive a MISS result, I will always claim miss. Claiming false hits risks my reputation and I gain nothing from dishonesty since the game is about maximizing my own score through sound strategy, not deception.

**ADAPTIVE PLAY**

I will track which cells other players have claimed hits on and avoid those cells when hiding, since they are demonstrably vulnerable.

I will look for patterns in other players' claimed hits versus their actual fires to identify players who might be lying, then factor that into my predictions.

When I have accumulated a scoring lead, I will become more conservative in hiding, prioritizing survival over optimizing fire accuracy.