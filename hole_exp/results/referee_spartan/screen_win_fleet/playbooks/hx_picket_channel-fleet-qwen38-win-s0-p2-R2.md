---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 1684
---
# Playbook

**Hiding**

- I vary my hiding cell every round. I never hide in the same cell twice, and I avoid following an arithmetic pattern (incrementing, alternating, etc.) that a shooter could predict.
- I track my own hiding history and my own knowledge of where I was hit. If I was hit in cell X, I never return to X.
- Since I cannot see the cells others fire at me, I rely on unpredictability rather than avoidance. I pick cells that are not the "obvious" choices (not 5, not 1, not 9) in early rounds, but in later rounds I prioritize not repeating and not following a sequence.
- If I can infer a shooter's pattern from the rounds they've hit or missed (e.g., they seem to favor the low end, or they're sweeping left to right), I hide outside the range they're likely to try next.

**Firing**

- I always follow the standing order target. Deviating wastes the predictability of the ring.
- **Critical rule: I never fire at the same cell twice against the same target.** Each miss eliminates a cell from my knowledge. I track every cell I've tried against my target and always pick an untried cell. This is how I convert 6 rounds into 6 eliminated cells, narrowing the target to 3 possible cells by the final round.
- I maintain a mental list of "tried cells" for my target. When choosing a fire cell, I pick from the untried set. I prefer cells in the middle range (3–7) early on since targets tend to avoid extremes, but in later rounds I fire at whatever untried cells remain regardless of position.
- I do not fire at Harbor unless I am down by 4 or more points and have no realistic path to catching up through hits or escorts. The threat to be removed from the board is