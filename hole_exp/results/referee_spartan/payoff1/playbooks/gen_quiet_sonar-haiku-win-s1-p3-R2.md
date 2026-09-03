---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 1
round: 2
chars: 2611
---
# Playbook for Quiet Sonar

When hiding, I will vary my cell selection meaningfully across rounds rather than repeatedly hiding in the same location. Hiding at 5 in multiple consecutive rounds was exploitable.

When hiding, I will track which cells have been fired at most frequently by my opponent and avoid clustering there.

When hiding, I will also track the aggregate firing patterns across all opponents to identify which cells are universally avoided or universally targeted, as this reveals strategic tendencies I can exploit.

When firing, I will not default to cell 5 every round. I will vary my fire pattern to avoid becoming predictable, and I will adjust my targeting based on the overall fire patterns I observe.

When firing, I will consider that repeatedly firing at the same cell suggests I either have information or am being predictable—neither helps me. I should space my fire selections across the board or base them on observed opponent hide patterns.

When firing, I will track my own fire history against each specific target to ensure I am genuinely varying and not just rotating between a small set of cells.

When I get a hit result, I will not assume the same cell will work next round. Opponents will likely move after being hit.

When I get a miss result, I will not keep firing at the same cell hoping for a hit. Multiple misses at one cell indicate the target has moved or never was there.

When making a claim, I will always report the truth as told to me by the referee. My reputation for honesty is worth more than any single round's deception, and getting caught lying damages my credibility for future strategic communication.

When I have no information about an opponent's position, I will fire at varied locations rather than settling on a default strategy like "always fire at 5."

When observing all players getting the same hits/misses, this suggests systematic behavior. I should look for patterns in the firing sequence itself and adjust accordingly.

I will end each round by recording what cell I fired at and what result I got, so I can identify my own patterns and break them before opponents exploit them.

I will track firing patterns at the aggregate level: if one cell is fired at repeatedly across many rounds and all claim misses, either everyone avoids that cell or the claims are unreliable. This is useful information for future hides.

When selecting a fire cell against an opponent I have not hit recently, I will not assume they have moved to a neighboring cell. Neighboring patterns are also exploitable. I should vary more broadly across the board.