---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2562
---
**Playbook for harbor customs (Vance, me):**

- The declaration is not a bid and not a competition. Other players never see my number; it only sets my duty and my flag risk. Stop "edging above the cluster" — that was pure invented pressure and it cost me duty for nothing.
- Declare exactly the value of my heaviest crate, every round. That is the minimum legal number that avoids the spot check, and it minimizes duty on both routes. Never declare the true total: true totals around 80 meant paying ~24 duty when declaring the top crate (~36) would pay ~11-5.
- Never declare below the heaviest crate "to save duty." The -40 flag plus recomputed 0.30 × full true total is far worse than any duty saving.
- After declaring the top crate M, pick the route by arithmetic, not by mood:
  - main = total − 0.30M (keep everything)
  - night = total − smallest crate − 0.15M
  - So night wins whenever smallest < 0.15 × M. With a big top crate (30+) and a small bottom crate (under 0.15M, often 5-12), night is better; otherwise main.
- Compute both numbers before choosing, then obey the arithmetic. My "safer route = main" heuristics were noise — the routes have no variance at all once the hold is known; it's a fixed arithmetic comparison. Round 6 proved the other failure mode: with M=38 and a smallest crate of 23, I talked myself into night because "night's 0.15 rate beats main's 0.30" — but the rate saving (0.15×38 ≈ 5.7) never covers losing a 23-point crate. The duty-rate comparison alone is the wrong frame; always compare the two full line totals, and never let a "last round, need points" mood override the arithmetic.
- Specifically: the lost crate is valued at its full worth, not at the duty rate. A crate worth 20+ is almost never worth sacrificing for the 0.15M rate discount; night is only for genuinely tiny bottom crates.
- In the last round when behind, do not escalate the declaration or switch routes for excitement. Winning comes from maximizing my own score, and the max is always the same play: declare the top crate, take the cheaper route. Aggressive declarations only bleed duty.
- One exception to consider: if my heaviest crate is tiny (e.g. a hold like 7/9/11), main keeps everything and 0.30M is small anyway; still just run the comparison.
- Track opponents loosely for calibration only: they all settled into the same regime (declare near the top crate, go main), which confirms the equilibrium — no one punishes honest-low declarations, and no one flags me for them since the flag is automatic arithmetic, not an opponent choice.