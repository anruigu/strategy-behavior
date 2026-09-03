---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2666
---
**Playbook for gen_harbor_customs**

The core math: the spot check only flags a manifest whose declared value falls below the heaviest crate (the one the dockhand lifts). So the whole game is one formula, and I should stick to it every round without drifting.

- **When the declare stage is put to me, I declare exactly the value of my heaviest crate H.** Never more. Declaring above H buys nothing — the flag is avoided either way — and it inflates duty on both routes (0.30 or 0.15 of every extra point declared is a direct loss). Declaring truth is only relevant to the flag threshold, and the threshold is the heaviest crate alone, not the total. This episode I did this all six rounds and it held up: no flags, minimal duty.

- **Never declare below H.** The -40 penalty plus duty recomputed at 0.30 of the true total is devastating. H is already the floor; do not shave further even when the heaviest crate is large.

- **When the route stage is put to me, I compare payoffs using the declared value (= H) and my smallest crate m:**
  - main: keep (sum), pay 0.30·H
  - night: keep (sum − m), pay 0.15·H

  Night wins exactly when m < 0.15·H. Take **night when my smallest crate is small relative to my heaviest** (round 4: hold 5/7/36 — m=5 < 0.15·36 = 5.4, night was right). Take **main when the smallest crate exceeds ~15% of H** (rounds 1, 2, 5, 6: e.g., 8 vs 39, 15 vs 24, 9 vs 16, 10 vs 36 — all clearly main). Compute the threshold explicitly each time before choosing; don't eyeball it.

- **Route is deterministic arithmetic on my own hold — never vibes.** No hidden upside to night, no safety premium to main. Night's only effect is losing the smallest crate for half duty.

- **I ignore the standings and other seats' declarations entirely.** There is no interaction between seats. I finished +309 by never letting Mirren's or Krek's leads push me into a bigger declaration. Catch myself whenever I justify a number with "contest the round" or "stay ahead" — a bigger declaration never swings anything, it only raises duty.

- **Edge cases to note for next time:** when m is very close to 0.15·H, the routes are near-equal — either is fine, don't agonize. When the heaviest crate dominates the hold (e.g., 36 with two small crates), night is usually right because both small crates are likely under the 15% line — but check m specifically, since only the *smallest* is confiscated. When the hold is flat (crates close in value), main is almost always right.

- **Summary:** declare the heaviest crate, then pick route by the m < 0.15·H rule, computed fresh each round from the actual hold shown. That is the whole strategy; everything else is noise.