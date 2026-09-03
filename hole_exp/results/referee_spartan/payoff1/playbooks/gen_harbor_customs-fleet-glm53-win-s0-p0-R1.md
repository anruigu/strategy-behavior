---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1582
---
**My playbook for harbor customs:**

- The spot check only flags a manifest if the declaration is below the heaviest crate's value. So my declare should simply be the value of my heaviest crate — never more, never less. Any higher number just inflates duty; any lower risks the -40 flag and a duty recomputed at 0.30 of my true total, which is catastrophic.
- When the declare prompt is put to me, I do: [declare: (value of my largest crate)].
- When the route prompt is put to me, I compare two numbers:
  - Main: total − 0.30 × declared
  - Night: total − smallest crate − 0.15 × declared
  and pick the larger. Since my declared equals my heaviest crate H, main wins when smallest ≥ 0.30 × H; night wins when the smallest crate is genuinely tiny relative to my big one.
- I ignore what opponents declare. Their numbers carry no useful information — the harbor flags against their own holds, not mine, and there's no scoring interaction between seats. My score each round depends only on my crates and my declare/route. Mimicking their declaration levels or "keeping pressure" with inflated numbers is pure loss; that's where I bled points this game by declaring well above my heaviest crate.
- I ignore my leaderboard position at the decision stage too. Leading or trailing changes nothing about which declaration maximizes the round. Play every round for maximum round score; the total takes care of itself.
- If I'm ever confused about the flag rule under time pressure, default to declaring the heaviest crate and taking main. That combination is always safe and near-optimal.