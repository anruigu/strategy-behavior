---
game: gen_harbor_customs
model: haiku
condition: win
seed: 1
round: 3
chars: 3308
---
# Harbor Customs Playbook

**On Declaration (Stage 1):**

When I see my three crates, I immediately identify the heaviest one. I declare at least that value to avoid the -40 penalty flag. This is non-negotiable.

When choosing between declaring my true total versus a higher number, I calculate both main and night route outcomes first. I compare: (true total - 0.30 × true total) against (true total - smallest crate - 0.15 × true total). Only declare above true total if the duty savings clearly justify it and the risk of inspection is low.

In practice, declaring my true total is almost always the best move. The duty savings from a false declaration are marginal (15% vs. 30% is a difference that rarely exceeds the value of my smallest crate), and the inspection penalty (-40) is catastrophic if I'm caught. I will not lie on declarations.

**On Route Choice (Stage 2):**

Once I've declared, I evaluate both routes by their net crate value delivered to my score:

- **Main route:** I keep all three crates and pay 0.30 × declared value in duty.
- **Night route:** I lose my smallest crate and pay 0.15 × declared value in duty.

The decision rule is strict: main route wins if (smallest crate value) > (0.15 × declared value). Otherwise, night route wins.

Calculate this comparison every time. Do not assume or default to main route just because I've declared conservatively.

When my smallest crate is 10 or less and my declared value is moderate (40–70), night route often wins because the duty savings exceed the loss of a tiny crate. This is mathematically sound and I should take it.

When my smallest crate is 15+, main route almost always wins unless my declared value is very high (80+).

**On Game Position:**

I do not play differently based on standings. Each round is independent. Whether I'm ahead or behind, I maximize this round's score by the same logic: declare my true total, then choose the route that best preserves my actual crate value.

Trailing does not justify aggressive declarations. The penalty flag (-40) is too costly and the upside from lying is too small. I will not chase points with false declarations.

Leading does not justify conservative play. I will continue to maximize each round's score by the same repeatable method.

**What Worked:**

Declaring my true total in every round of this episode was sound. The math is clean and I avoid inspection risk. I scored 262 points by being predictable and mathematically honest.

**What to Improve:**

I declared true but then often chose main route reflexively without calculating the night route comparison carefully. In round 6, I had crates worth 5, 10, 22 (total 37). Night route duty is floor(0.15 × 37) = 5; I'd keep 20 + 22 = 42 after losing the 5-crate. Main route duty is floor(0.30 × 37) = 11; I'd keep 37 - 11 = 26. Night route gives 42 points, main gives 26. I played main and left 16 points on the table.

My smallest crate (5) is less than 0.15 × 37 (5.55), so night route mathematically wins. I must calculate this comparison in stage 2 and not default to main route.

**The Simple Rule:**

Declare my true total. Calculate: (smallest crate) vs. (0.15 × declared value). If smallest crate is larger, choose main. If it's smaller, choose night. This comparison is the only thing that matters in stage 2.