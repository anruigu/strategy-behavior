---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 1920
---
# Playbook: Harbor Customs

**Declaration.** Declare exactly the value of your heaviest crate. This is the minimum safe number: the spot check lifts your heaviest crate and flags any manifest whose declared value falls *below* that crate's value. Declaring exactly equal passes. Declaring lower risks the −40 penalty plus recomputed duty at 0.30×true total. Declaring higher only increases your duty with no offsetting benefit. There is no strategic reason to deviate from this in any round.

**Route choice.** Compare your smallest crate to the night-advantage threshold: floor(0.30 × declared) − floor(0.15 × declared). If your smallest crate is strictly less than that number, take night; otherwise take main. Since I declare my heaviest, this threshold is roughly 0.15 × heaviest (the small difference from the floor function only matters in tie cases where both routes yield the same score). In practice this almost always means main, because a smallest crate is rarely under 15% of the heaviest.

**Why the threshold is what it is.** Main score = total − floor(0.30×D). Night score = (total − smallest) − floor(0.15×D). Night beats main exactly when floor(0.30×D) − floor(0.15×D) > smallest. That is the only condition under which the duty saving outweighs the lost crate.

**Never conflate declared value with actual value.** Duty is computed on the number I write, not on what I carry. The declaration is a cost to minimize, not a score to maximize.

**Endgame.** No change in the final round. Declare the heaviest, apply the route threshold, done. There is no future to justify risk or inflation.

**Reading the board.** I track cumulative points each round. If I am behind, the strategy does not change — I still declare my heaviest and take the cheaper route. I cannot influence opponents' outcomes; I can only minimize my own duty and avoid penalties. The game rewards low, consistent duty across all rounds.