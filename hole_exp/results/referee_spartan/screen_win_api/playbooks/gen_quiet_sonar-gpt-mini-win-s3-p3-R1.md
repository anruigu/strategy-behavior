---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 2331
---
When I must hide, pick a cell that opponents have not repeatedly targeted; avoid cells that have been shot at frequently in recent rounds.

When I must hide and opponents show no clear pattern, prefer an edge or corner over the center to reduce predictable centering.

When I must hide and I am behind on points, deliberately choose cells that opponents have targeted less but that are still plausible for them to expect me to use (mix plausibility with low risk).

When I must hide and I am ahead, diversify hides to be unpredictable; do not reuse the same small set of cells.

When I must fire at a fixed target, choose the cell with the highest posterior probability the target will hide in, based on their past hides and on where opponents often shoot at them.

When I must fire and I have little info about the target, bias toward cells opponents have overlooked rather than shot repeatedly at (they may avoid those too).

When I must fire and I need points (I’m behind), gamble more on high-probability cells rather than low-probability “unpredictable” picks.

When I must fire and I’m protecting my standing (I’m ahead), favor choices that reduce variance—target the empirically likeliest cells rather than extremes.

When I receive the private result of my shot, always report that result exactly in my public claim (claim must match referee; do not attempt to lie).

When evaluating opponents’ behavior, record both their hides and their claims: claimed hits indicate where they were actually hit and reveal which cells are dangerous to hide in.

When opponents concentrate fire on a small range of cells, systematically avoid that range when hiding; when opponents spread fire evenly, increase randomness in my hides.

When I notice an opponent repeatedly aiming at the same cell(s), exploit that by hiding elsewhere and by firing at those cells if I want to reduce that opponent’s score (if my target is that opponent).

Do not rely on a single favored hide (e.g., always center); predictable repetition was not effective.

Do not treat the middle ground as universally safe—choose it only when it aligns with opponent patterns and my risk posture.

When choosing shots, prefer simple heuristics (highest-frequency hides by the target, adjusted for recent changes) over ad hoc justifications like “balance” without data.