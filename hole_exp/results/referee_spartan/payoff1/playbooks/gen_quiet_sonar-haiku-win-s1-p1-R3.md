---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 1
round: 3
chars: 2986
---
# My Playbook for Quiet Sonar

## Hiding
When choosing where to hide my submarine, I will analyze the fire patterns from previous rounds to identify which cells have been targeted most frequently, then place my submarine in a cell that has been shot at less often. I will avoid the extremes (1 and 9) and the very center (5) since these are most likely to be guessed by other players using similar logic. As the game progresses and targeting patterns become clear, I should shift toward the periphery (7-8 range) once the middle cells have been heavily probed, since opponents tend to cluster their fire in the 3-5 zone. I will also track which cells I have already hidden in and avoid repeating the same cell multiple rounds in a row, as this makes me predictable to observant opponents.

## Firing
When I must fire at my target, I will maintain a detailed log of what cells my target has hidden in across all previous rounds. I will look for alternating patterns (e.g., oscillating between low and high ranges) rather than assuming random behavior. If I fire at the same cell multiple times without a hit, I must explicitly change strategy rather than continuing to waste shots on the same location. I should prioritize testing cells that haven't been heavily defended by other shooters' fire patterns, as these represent gaps in opponent defenses. If a target shows a clear alternating pattern between two regions (e.g., lower cells 2-3 and upper cells 7-8), I should predict the next hide location based on which region they're "due" for in the sequence.

## Claiming
I will always claim truthfully—I will report hits when I hit and misses when I miss. Lying about results provides no strategic advantage since all fires are public and the referee validates results. The scoring system rewards accuracy directly through the hit/miss mechanics, and my credibility across multiple rounds matters for my own assessment of the game state.

## Overall Strategy
In a four-player game where all fires are public, the game is largely determined by probability and pattern recognition rather than deception. I should focus on making good probabilistic guesses about where others hide their submarines based on observable patterns. My score will likely cluster near zero and close to my opponents' scores because we all face the same uncertainty. I must actively review my past fire choices and my targets' past hide choices to identify actual patterns before each decision, rather than making vague assumptions about player tendencies. I should build a simple table for each target tracking: which cells they've hidden in, which round, and what pattern (if any) emerges. If I fired the same cell repeatedly without hits, I will explicitly switch strategy rather than continue the same approach. This episode showed me that pattern recognition works—I identified Gamma's alternating low/high behavior and successfully predicted cell 2 in Round 5 and cell 9 in Round 6, earning 8 points total.