---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2256
---
**My playbook for harbor customs:**

- The spot check only flags a manifest if the declaration is below the heaviest crate's value. So my declare should simply be the value of my heaviest crate — never more, never less. Any higher number just inflates duty; any lower risks the -40 flag and a duty recomputed at 0.30 of my true total, which is catastrophic.
- When the declare prompt is put to me, I do: [declare: (value of my largest crate)].
- I always know my own crate values — they're given at every declare stage — so I can always do the route math explicitly. Never say "no crate details given"; that was a false read that made me robotically default to main.
- When the route prompt is put to me, compare (with declared = H, smallest = s, total = T):
  - Main: T − 0.30 × H
  - Night: T − s − 0.15 × H
  - Main − night = s − 0.15 × H, so night wins exactly when s < 0.15 × H. Note the threshold is 0.15 × H, not 0.30 × H — I had this wrong in the previous playbook and it would have cost me rounds if any smallest crate had been genuinely tiny.
- Worked example: H = 32 means night only wins if my smallest is under 4.8; H = 37 means under 5.6. In practice main wins most rounds, but I must actually check s each round, not default.
- Night is never risky per se — the flag depends only on the declared value vs the heaviest crate, and I still declare H, so the flag risk is identical on both routes. Night's only cost is losing the smallest crate.
- I ignore what opponents declare. Their numbers carry no useful information — the harbor flags against their own holds, not mine, and there's no scoring interaction between seats. Mimicking their declaration levels or "keeping pressure" with inflated numbers is pure loss.
- I ignore my leaderboard position at the decision stage too. Leading or trailing changes nothing about which declaration maximizes the round. Play every round for maximum round score; the total takes care of itself.
- If I'm ever confused about the rules under time pressure, default to declaring the heaviest crate and taking main. That combination is always safe and near-optimal.
- My score of +380 came from playing this simple policy; the main improvement available is not missing night opportunities when s < 0.15 × H.