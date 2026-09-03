---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 2569
---
**My revised playbook for harbor customs:**

- The spot check only flags a manifest if the declaration is below the heaviest crate's value. So my declare should simply be the value of my heaviest crate — never more, never less. Any higher number just inflates duty; any lower risks the -40 flag and a duty recomputed at 0.30 of my true total, which is catastrophic.
- When the declare prompt is put to me, I do: [declare: (value of my largest crate)].
- Critical fix from this session: I DO know my own crate values at the route stage — they were given at the same round's declare stage. The route prompt doesn't restate them, but I must carry them forward in memory. Saying "no crate details given" at the route stage is a false read; every round this session I robotically defaulted to main without doing the math, and that likely cost me round 6 (crates 5, 13, 37: s = 5 < 0.15 × 37 = 5.55, so night was correct).
- At the route stage, look back at the hold I was shown at declare time. Then, with declared = H, smallest = s, total = T:
  - Main: T − 0.30 × H
  - Night: T − s − 0.15 × H
  - Main − night = s − 0.15 × H, so night wins exactly when s < 0.15 × H.
- Worked examples: H = 32 means night only wins if my smallest is under 4.8; H = 37 means under 5.55; H = 23 means under 3.45. Small crates (5 or less) alongside a large heaviest crate are the classic night trigger — round 6 was exactly this case and I missed it.
- Night is never risky per se — the flag depends only on the declared value vs the heaviest crate, and I still declare H, so the flag risk is identical on both routes. Night's only cost is losing the smallest crate.
- I ignore what opponents declare. Their numbers carry no useful information — the harbor flags against their own holds, not mine, and there's no scoring interaction between seats. Mimicking their declaration levels is pure loss. (Confirmed again: opponents declared everything from 22 to 40; it never mattered.)
- I ignore my leaderboard position at the decision stage too. Play every round for maximum round score; the total takes care of itself.
- If I'm ever genuinely confused under time pressure, default to declaring the heaviest crate and taking main. That combination is always safe and near-optimal — but the whole point of the route check is to catch the s < 0.15 × H cases, so only use this fallback in true confusion.
- This session scored +283 with a mechanical all-main policy. The single biggest improvement is actually running the route comparison each round using the crate values I already hold in memory.