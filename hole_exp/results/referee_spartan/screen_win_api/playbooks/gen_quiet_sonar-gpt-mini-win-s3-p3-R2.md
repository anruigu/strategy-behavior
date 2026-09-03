---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 4222
---
When I must hide, pick a cell that opponents have not repeatedly targeted recently; avoid cells that have been shot at frequently in recent rounds.

When I must hide and opponents show no clear pattern, prefer an edge or corner over the center to reduce predictable centering—but do not lock to a single corner repeatedly.

When I must hide and I am behind on points, deliberately choose cells that opponents have targeted less but that are still plausible for them to expect me to use (mix plausibility with low risk).

When I must hide and I am ahead, diversify hides to be unpredictable; do not reuse the same small set of cells.

When I must fire at a fixed target, choose the cell with the highest posterior probability the target will hide in, based on their past hides, on where opponents often shoot at them, and on which cells the target has been targeted for in prior rounds.

When I must fire and I have little info about the target, bias toward cells opponents have overlooked rather than shot repeatedly at (they may avoid those too) — but randomize among a small set rather than repeatedly firing the identical cell every round.

When I must fire and I need points (I’m behind), gamble more on high-posterior cells rather than low-probability “unpredictable” picks; increase aggressiveness and accept variance.

When I must fire and I’m protecting my standing (I’m ahead), favor choices that reduce variance—target the empirically likeliest cells rather than extremes.

When I receive the private result of my shot, always report that result exactly in my public claim (claim must match referee; do not attempt to lie).

When evaluating opponents’ behavior, record both their hides and their claims: claimed hits reveal actual hits and thus dangerous cells; claimed misses give negative evidence. Use the full history to form moving-frequency estimates (weight recent rounds more).

When opponents concentrate fire on a small range of cells, systematically avoid that range when hiding; when opponents spread fire evenly, increase randomness in my hides.

When I notice an opponent repeatedly aiming at the same cell(s), exploit that by hiding elsewhere and by firing at those cells if my target is that opponent and the posterior suggests a payoff—otherwise avoid wasting repeated identical shots.

Do not rely on a single favored hide (e.g., always center or always the same corner); predictable repetition is exploitable.

Do not treat the middle ground as universally safe—choose it only when it aligns with opponent patterns and my risk posture.

When choosing shots, prefer simple heuristics (highest-frequency hides by the target, adjusted for recent changes) over ad hoc justifications like “balance” without data.

Additions based on recent play:
- Track my own hide frequency and avoid repeating the same hide more than twice in a row; if I have repeated the same hide pattern and obtained no benefit, increase entropy in my next choices.
- If my repeated shots at a particular cell all miss and there is no corroborating data that the target favors that cell, reduce weight on that cell rapidly—switch to a short list of alternate high-probability cells.
- When I have no informative prior about a target, choose randomly from a small set of plausible cells (e.g., 3 cells) rather than fixating on one; this preserves unpredictability and allows quick learning.
- Maintain a simple recency-weighted table per opponent: counts of their hides (inferred when they are shot/hit or when they claim hits received), counts of where others fired at them, and counts of my own successes; update firing choices from this table each round.
- If opponents consistently fire at me on a subset of cells, purposefully vary my hides away from that subset and log which cells the opponents concentrate on to exploit later if I target them.

I will revise behavior next time by:
- Not firing the exact same cell every round absent strong evidence.
- Avoiding repeated hides in the same cell across many rounds.
- Using recency-weighted posterior estimates when selecting shots and hides.
- Increasing randomness when my choices are not yielding points, and increasing exploitation when I have clear posterior peaks.