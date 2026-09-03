---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 2307
---
**Playbook for Harbor Customs**

**Declare stage:**
- The spot check flags any declaration below my heaviest crate. So my declaration must always be ≥ heaviest crate, always, no exceptions. This is a hard floor, not a soft guideline.
- Declaring exactly the heaviest crate value is the safe minimum; declaring true total is the safe maximum. Anywhere in that band passes the check.
- Never declare below my heaviest crate. The -40 penalty plus duty recomputed at 0.30 × true total is devastating.
- Beyond the floor, there's no reward for a high declaration — scoring is my own crates minus my own duty. Don't inflate declarations to "stay competitive" or match other players; that only raises my duty for nothing.
- So: declare exactly my heaviest crate value, every round.

**Route stage:**
- Compare concretely, with the numbers I actually hold: main keeps all 3 crates, duty = floor(0.30 × declared). Night loses my smallest crate, duty = floor(0.15 × declared).
- Night is better when (smallest crate value) < (0.30 − 0.15) × declared = 0.15 × declared. Main is better otherwise.
- Use my KNOWN smallest crate value, not a guess or a probability. I know all three crate values at route time — I erred repeatedly by saying "likely exceeds" or "unlikely" when I could just compute it.
- With a minimal declaration (equal to heaviest crate), night wins only when smallest < 0.15 × heaviest. That is rare — e.g. hold 36/37 smallest 6 → 6 > 5.55, so main was right, and I wrongly took night. Holds like 12/21/35 and 15/21/23 also favor main (12 > 5.25, 15 > 3.45). Default to main; take night only when the smallest crate is genuinely tiny relative to the heaviest.
- Beware sloppy comparisons: "night saves half the duty" is the wrong frame. The saving is only the *difference*, 0.15 × declared, and it must beat the *full value* of the smallest crate, not a fraction of it.

**Overall:**
- Other players' declarations, their routes, and the score standings are irrelevant to my per-round optimization. This is a solvable arithmetic problem each round.
- Optimal per-round play: declare exactly my heaviest crate value; then take main unless smallest crate < 0.15 × that declaration, in which case take night.
- Don't reason about "protecting a lead" or "chasing" — the leaderboard doesn't change the math.