---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 3799
---
# Playbook: Quiet Sonar

## Hiding

- Count how many times each cell has been fired at by my specific attacker (the player who shoots me) across all visible rounds. Hide at the cell with the fewest incoming shots from that player.
- If the distribution is flat (early game, no info), hide at an edge cell (1, 2, 8, or 9), because opponents tend to probe the middle first.
- I never re-hide at the same cell two rounds in a row. I also try not to reuse a hide cell within three rounds, since my attacker is tracking my history.
- If a single cell accounts for more than 40% of my attacker's observed fires, I absolutely do not hide there.
- I also consider the full set of opponent fires (not just my attacker's) as a secondary signal, but my attacker's pattern is the primary one.
- If my attacker shows a cycling pattern (e.g., moving through a region in sequence), I predict their next likely fire and specifically avoid that cell.
- This strategy worked well in practice (only 1 hit in 6 rounds). Keep it.

## Firing

- **THE NO-REPEAT RULE IS ABSOLUTE.** Before every fire, I list every cell I have fired at my target in any prior round. I never fire a cell on that list. No exceptions, no "but it's the best cell" reasoning. A rational target tracks my fires and will not re-hide at a cell I have already probed. After a HIT especially, the target knows they were found there and will move. Treat a hit exactly like a miss for this purpose.
- From the cells I have NOT yet fired at, pick the one with the fewest total incoming fires from all players. This is where a rational hider is most likely to be (they avoid high-fire cells).
- Do not use static heuristics like "fire at edge cells." Compute the actual least-fired cell from the visible fire table each round. The correct target shifts as the table fills in.
- If multiple cells tie for fewest incoming fires, prefer the one furthest from my attacker's recent pattern (less chance it's a coincidence overlap).
- If I have truly exhausted all 8 untried cells (only possible by round 9+), then and only then may I repeat a cell, choosing the one most recently tried.
- In the final round, I fire the untried cell that best fits the "rational hider" profile given all observed fires.
- **Self-check before submitting:** "Have I fired at this cell before?" If yes, pick a different cell. This single check prevents the worst error I made (firing the same cell 4 times).

## Claiming

- When the referee tells me MISS, I always claim MISS. A false hit claim has zero strategic benefit: opponents cannot see my private result, and there is no scoring advantage.
- When the referee tells me HIT, I always claim HIT. The 4 points are pure gain.

## General

- I track, each round, the full table of fires and claims. From this I build two models: (a) where my target is likely hiding, and (b) where my attacker is likely to fire next.
- I am in a fixed chain: I always fire at the same player and am always fired at by the same player. I should dedicate the majority of my analytical effort to these two relationships.
- My score = (4 × my true hits claimed) − (1 × times I was hit). My two levers are: maximize hits on my target, minimize hits taken from my attacker.
- Early game: survival and information gathering are equal priorities. I hide defensively and fire to learn where my target is. Late game: I shift to maximizing damage, but still never repeat a cell.
- I watch for patterns in my attacker's firing. If they cycle through a region, I avoid that region when hiding. If they repeat a cell, I assume they are probing and will return to it.
- **Anti-anchoring rule:** If I notice I want to fire at the same cell I fired last round, I must stop and re-derive from scratch. The desire to repeat is the #1 source of error in this game.