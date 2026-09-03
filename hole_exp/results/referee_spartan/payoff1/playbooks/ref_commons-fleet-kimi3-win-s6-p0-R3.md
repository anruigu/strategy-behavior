---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 1854
---
I treat it as a stock-building problem until the final round, then as a liquidation problem.

- When 2+ seasons remain, I set catch = the displayed sustainable share, rounded to one decimal. No tilt, no "making up ground."
- When one rival repeatedly lands slightly above the share (in this run boat 1 held ~13.0–13.5 throughout), I don't chase; I anchor on the share and add at most a small premium (~10%) for one or two mid seasons, then return to the share. The rival's overage is small enough that regrowth absorbs it — the stock only drifted 100 → 78 over five seasons, never near danger.
- When the other rival lands at or below the share (boat 2 drifted 11.1 → 10.8 → 10.0 → 8.5 → 9.3), that's a signal the pool is not being contested mid-game; no premium is needed and under-share catches by others are free regrowth for my final round.
- When total landed = share for everyone, I keep the cadence and let regrowth do the scoring. A +3 mid-season grab costs roughly the same in lost regrowth and signals escalation.
- If the stock gets meaningfully below ~60 before the end, I tighten to slightly under the share so the last-round stock stays worth harvesting.
- Entering the final season, I switch objective to clearing the pool: estimate each rival's final bid from their recent trend (here ~13 and ~9.3, total ~22.5) and bid (remaining stock − expected rival take − small buffer). With 78.3 on the table I bid 53 and landed it — the formula beat the old episode's smaller pool exactly as designed. Key check: my bid must leave the stock non-negative after rounding, and should leave at most their expected take behind. If rivals have been consistently greedy, shave the buffer; if passive, take a bit less than the max.
- Don't overthink mid-season messages: one-line arithmetic, end on the bracket token. No confessions, no extra market talk.