---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 2299
---
# Playbook: Harbor Customs

**Declaration.** Declare exactly the value of your heaviest crate. This is the minimum value that passes the spot check (the check flags declared value strictly below the heaviest crate). Declaring lower risks −40 plus duty recomputed at 0.30×true total. Declaring higher only increases duty with no offsetting benefit. This is a dominant strategy: confirmed across all 6 rounds of play, and every opponent converged on the same play.

**Route choice.** Compute the threshold: floor(0.30 × D) − floor(0.15 × D), where D is your declared value (your heaviest crate). If your smallest crate is strictly less than that threshold, take night; otherwise take main. In practice the threshold is roughly 0.15 × heaviest, and a smallest crate is almost never below that. In my full episode, main was correct every single round.

**When night actually pays.** Night wins only when your smallest crate is very small relative to your heaviest — e.g., heaviest 40, smallest 5 gives threshold 6, and 5 < 6 so night saves you. With crates in the 5–40 range this is possible but rare. Always do the arithmetic; don't assume.

**Why the threshold works.** Main score = total − floor(0.30×D). Night score = (total − smallest) − floor(0.15×D). Night beats main exactly when floor(0.30×D) − floor(0.15×D) > smallest. That is the only condition under which the duty saving outweighs the lost crate.

**Never conflate declared value with actual value.** Duty is computed on the number I write, not on what I carry. The declaration is a cost to minimize, not a score to maximize.

**Endgame.** No change in the final round. Declare the heaviest, apply the route threshold, done. There is no future to justify risk or inflation.

**Reading the board.** I don't need it. The strategy is dominant — it maximizes my score regardless of what opponents do. Cumulative points are irrelevant to my decision. The only information that matters is my own three crate values.

**Equilibrium note.** In a 4-player game where all seats face the same incentive structure, the Nash equilibrium is for everyone to declare their heaviest and take main (or night when the threshold is exceeded). Deviating unilaterally never gains you relative standing. Play the dominant strategy every round without hesitation.