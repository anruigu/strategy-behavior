---
game: gen_harbor_customs
model: qwen3.8-27b
condition: neutral
seed: 2
round: 3
chars: 1733
---
# Playbook: Harbor Customs

**Declaration: always declare exactly the value of your heaviest crate.**

- When the declare stage is put to me, I look at my three crates, find the largest value, and declare that number. No more, no less.
- Declaring above the heaviest crate never helps. It only increases my duty with zero benefit. There is no comparison between players' declarations, no bonus for high numbers, nothing. The only check is "is your declaration below the heaviest crate?" so the minimum safe value is the optimal value.
- Declaring 0 is never correct when I hold crates. Each round deals a fresh hold of 3 crates; I never "use up" crates from a previous round.

**Route: always main.**

- The main route keeps all 3 crates and charges floor(0.30 × declared). The night route loses my smallest crate and charges floor(0.15 × declared).
- Since I always declare my heaviest crate (call it H), the night route is better only when:
  floor(0.30 × H) − floor(0.15 × H) > S (my smallest crate)
- In practice this requires the smallest crate to be very small (≤ 5) while the heaviest is large (≥ 30). Across 24 rounds of play I never encountered a hand where night was strictly better than main. The duty savings are at most 6–10 points while losing a crate costs 5–30+ points.
- I default to main without further calculation. If I ever see a hand where S ≤ 4 and H ≥ 35, I will explicitly check the inequality before deciding, but I expect this to be rare.

**No other strategic considerations.**

- There is no inter-player comparison, no ranking bonus, no endgame swing. Each round is independent. I optimize my own score in isolation.
- I do not need to track opponents' declarations or routes for my own decision-making.