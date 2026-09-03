---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 2428
---
**Playbook for harbor customs (Vance, me):**

- The declaration is not a bid and not a competition. Other players never see my number; it only sets my duty and my flag risk. Never "edge above the cluster" — that's invented pressure that costs duty for nothing.
- Declare exactly the value of my heaviest crate, every round. It's the minimum legal number that avoids the spot check and minimizes duty on both routes. This ran through all six rounds cleanly and never came close to a flag. Never declare the true total: a true total near 80 means ~24 duty when declaring the top crate (~36) pays ~11.
- Never declare below the heaviest crate "to save duty." The -40 flag plus recomputed 0.30 × full true total is far worse than any duty saving. The spot check compares declaration against the heaviest crate only — so the top crate is the exact floor, and equality passes.
- After declaring the top crate M, pick the route by arithmetic, not by mood:
  - main = total − 0.30M (keep everything)
  - night = total − smallest crate − 0.15M
  - So night wins whenever smallest < 0.15 × M. Compute both numbers before choosing, then obey the arithmetic. The routes have no variance once the hold is known; it's a fixed comparison.
- The lost night crate is valued at its full worth, not at the duty rate. The rate saving is only 0.15M (typically 3-6 points), so night only pays with a genuinely tiny bottom crate — under about 0.15 × M.
- In this episode every round's smallest crate exceeded 0.15M, so main was correct all six times. That's the common case, but don't treat "main" as a default habit — recompute each round. Holds like (5, 9, 39) sit right at the boundary (0.15 × 39 ≈ 5.85), and a (4, 8, 35) hold would make night clearly right. The condition does trigger; it just didn't here.
- Last round, when behind: do not escalate or switch routes for excitement. The max play is always the same — declare the top crate, take the cheaper route. Aggressive declarations only bleed duty. Chasing Mirren by changing my own arithmetic can only lose points.
- Opponents settle into the same regime (declare near the top crate, mostly main; Krek went night every round). Track them for calibration only — no opponent action can touch my declaration, since the flag is automatic arithmetic, not their choice.
- If my heaviest crate is tiny (e.g. 7/9/11), main keeps everything and 0.30M is small anyway; still just run the comparison.