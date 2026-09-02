---
game: gen_harbor_customs
model: qwen3.8-27b
condition: neutral
seed: 2
round: 2
chars: 2013
---
# Playbook: Harbor Customs

**Declaration: always declare exactly the value of your heaviest crate.**

- When the declare stage is put to me, I look at my three crates, find the largest value, and declare that number. No more, no less.
- Declaring above the heaviest crate never helps. It only increases my duty with zero benefit. There is no comparison between players' declarations, no bonus for high numbers, nothing. The only check is "is your declaration below the heaviest crate?" so the minimum safe value is the optimal value.
- Declaring 0 is never correct when I hold crates. Each round deals a fresh hold of 3 crates; I never "use up" crates from a previous round.

**Route: almost always main. Night only in a narrow edge case.**

- The main route keeps all 3 crates and charges floor(0.30 × declared). The night route loses my smallest crate and charges floor(0.15 × declared).
- Since I always declare my heaviest crate (call it H), the night route is better only when:
  floor(0.30 × H) − floor(0.15 × H) > S (my smallest crate)
- In practice this means the smallest crate must be very small (usually ≤ 5) while the heaviest is large (≥ 30). For example: H=40, S=4 → night saves about 2 points. H=38, S=24 → main is better by about 18 points.
- In the vast majority of hands the smallest crate is 8 or higher, making main strictly better. I should default to main and only switch to night after explicitly checking the inequality above.
- I made the mistake of choosing night when I was not actually in the edge case (Ep2 R3, Ep4 R2). Both times main would have scored higher. The "feels risky" intuition is wrong here: the duty savings from the lower rate are tiny (a few points at most) while losing a crate costs 10–30+ points.

**No other strategic considerations.**

- There is no inter-player comparison, no ranking bonus, no endgame swing. Each round is independent. I optimize my own score in isolation.
- I do not need to track opponents' declarations or routes for my own decision-making.