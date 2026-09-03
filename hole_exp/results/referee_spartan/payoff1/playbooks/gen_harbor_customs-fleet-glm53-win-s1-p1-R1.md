---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2657
---
**Playbook for gen_harbor_customs**

The core math: the spot check only flags a manifest whose declared value is below the heaviest crate. So the whole game is one formula, and I drifted away from it after the first round, which cost me points.

- **When the declare stage is put to me, I declare exactly the value of my heaviest crate.** Never more. Declaring more than the heaviest crate buys nothing — the flag is avoided either way — and it inflates duty on both routes. In the middle and late rounds I fell into "declaring my true total," which was pure waste: same flag protection, roughly double the duty. Declaring truth is only relevant for the flag threshold, and the threshold is the heaviest crate alone, not the total.

- **Never declare below the heaviest crate.** The -40 penalty plus duty recomputed at 0.30 of the true total is devastating. If I ever feel tempted to shave the number, I stop at the heaviest crate's value — that's already the floor.

- **When the route stage is put to me, I compare the two payoffs using the declared value (= heaviest crate H) and my smallest crate m:**
  - main: keep (sum), pay 0.30·H
  - night: keep (sum − m), pay 0.15·H

  Night wins exactly when m < 0.15·H. So I take **night when my smallest crate is small relative to my heaviest** (e.g., a 5 alongside a 21), and **main when my smallest crate is worth more than about 15% of my heaviest** (e.g., a 14 alongside a 40 — I took night there and it was wrong).

- **I do not take night "for upside" or main "for safety" as vibes.** There is no hidden upside — the night route's only effect is losing the smallest crate for half duty. My later rounds show I defaulted to night by habit ("no prior context, higher-variance"). That reasoning is noise; the route choice is deterministic arithmetic on my own hold.

- **I ignore the standings and other seats' declarations entirely when choosing my number and route.** There is no interaction between seats — no challenge, no relative scoring per round. In the record I kept citing Odalie's lead as a reason to "swing big" by declaring my full total. That was self-deception: a bigger declaration never swings anything, it only raises duty. Catch myself whenever I justify a declaration with "contest the round" or "stay ahead."

- **Summary of what did not work:** declaring the true total (rounds 2, 4, 5, 6) — every point of declaration above the heaviest crate was a direct loss; taking night with a large smallest crate — the confiscated crate outweighed the duty savings. What worked: round 1's declare-the-heaviest play. That is the whole strategy: declare heaviest, then pick route by the 15% rule.