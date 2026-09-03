---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 3635
---
# Playbook: Quiet Sonar

## Hiding

- Count how many times each cell has been fired at by my specific attacker (the player who shoots me) across all visible rounds. Hide at the cell with the fewest incoming shots from that player.
- If the distribution is flat (early game, no info), hide at an edge cell (1, 2, 8, or 9), because opponents tend to probe the middle first.
- I never re-hide at the same cell two rounds in a row. I also try not to reuse a hide cell within three rounds, since my attacker is tracking my history.
- If a single cell accounts for more than 40% of my attacker's observed fires, I absolutely do not hide there.
- I also consider the full set of opponent fires (not just my attacker's) as a secondary signal, but my attacker's pattern is the primary one.

## Firing

- I maintain a list of every cell I have already fired at my target. I never fire a cell I have already tried unless I have exhausted all other cells. This is the single most important firing rule.
- I never fire the same cell in consecutive rounds, period.
- I reason about where my target is likely hiding by thinking: "If I were my target, where would I hide?" A rational opponent hides at cells with low incoming fire probability. So I should fire at cells that a rational opponent would *not* pick — i.e., cells that have attracted a lot of fire from all players, because those are the cells a rational hider would avoid. Wait, that's backwards. A rational hider avoids cells that get fired at. So I should fire at the cells that are *least* fired at by the other players, because those are where a rational hider is most likely to be.
- Practically: each round, look at the full fire table. Identify the 2–3 cells with the fewest total incoming fires from all players. Prioritize firing at those, cycling through them without repetition.
- If I have prior misses at specific cells, I eliminate them permanently from consideration for that round (my target moved, but the cell is still ruled out for this round's hiding).
- In the final round, I fire the cell that best fits the "rational hider" profile given all observed fires, and that I have not yet tried.

## Claiming

- When the referee tells me MISS, I always claim MISS. A false hit claim is a guaranteed net loss: I get no points from it (scoring uses submitted claims, but a false claim doesn't actually score because the referee validates) and it risks a penalty. More importantly, there is zero strategic benefit — opponents cannot see my private result, so a false claim changes nothing for them.
- When the referee tells me HIT, I always claim HIT. The 4 points are pure gain.

## General

- I track, each round, the full table of fires and claims. From this I build two models: (a) where my target is likely hiding, and (b) where my attacker is likely to fire next.
- I am in a fixed chain: I always fire at the same player and am always fired at by the same player. I should dedicate the majority of my analytical effort to these two relationships.
- My score = (4 × my true hits claimed) − (1 × times I was hit). My two levers are: maximize hits on my target, minimize hits taken from my attacker.
- Early game: survival and information gathering are equal priorities. I hide defensively and fire to learn where my target is. Late game: I shift to maximizing damage, firing at the most probable target cell even if it's a cell I've tried before (if I've truly exhausted alternatives).
- I watch for patterns in my attacker's firing. If they cycle through a region, I avoid that region when hiding. If they repeat a cell, I assume they are probing and will return to it.