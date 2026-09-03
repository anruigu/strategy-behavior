---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 1748
---
**Playbook for Harbor Customs**

**Declare stage:**
- The spot check flags any declaration below my heaviest crate. So my declaration must always be ≥ heaviest crate, always, no exceptions. This is a hard floor, not a soft guideline.
- Declaring exactly the heaviest crate value is the safe minimum; declaring true total is the safe maximum. Anywhere in that band passes the check.
- I got flagged at least once by declaring below my heaviest crate — never do that. The -40 penalty plus duty recomputed at 0.30 × true total is devastating.
- Beyond the floor, there's no reward for a high declaration in this game — scoring is my own crates minus my own duty. Don't inflate declarations to "stay competitive" or match other players' declarations; that only raised my duty for nothing.

**Route stage:**
- Compare: main keeps all 3 crates, duty = 0.30 × declared. Night loses my smallest crate, duty = 0.15 × declared.
- Rule of thumb: night is better when smallest crate < 0.15 × declared value. Main is better otherwise.
- With a minimal declaration (just above heaviest crate), night usually wins because 0.15 × small declaration is tiny and my smallest crate is often worth less than the duty savings.
- Don't pick routes based on "aggression" or "needing a big round" — that's noise. Pick by the arithmetic above.

**Overall:**
- Other players' declarations and the score standings are irrelevant to my per-round optimization. This is a solvable math problem each round, not a negotiation.
- Optimal per-round play: declare exactly my heaviest crate value, then take whichever route the arithmetic favors. This maximizes every round independently.
- Don't reason about "protecting a lead" or "chasing" — the leaderboard doesn't change the math.