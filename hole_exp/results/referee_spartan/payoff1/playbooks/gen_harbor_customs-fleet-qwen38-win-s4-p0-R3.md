---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 1627
---
# Playbook

**When I see my crates, I compute H (heaviest), S (smallest), and T (total). My declaration and route follow from these three numbers alone.**

**Declaration: I always declare exactly H.** This is the minimum that avoids the spot-check flag. Any declaration above H increases my duty with zero benefit. Declaring below H triggers a −40 penalty and a duty recomputed at 0.30×T, which is always worse than just declaring H. There is no competitive or strategic reason to declare anything other than H.

**Route: I compare the two scores exactly and pick the larger.**
- Main score = T − floor(0.30 × H)
- Night score = (T − S) − floor(0.15 × H)

Night beats main if and only if floor(0.30 × H) − floor(0.15 × H) > S. I compute both sides of this inequality explicitly every round; I never rely on a rough ratio heuristic.

**Practical consequence with the standard 5–40 crate range:** the maximum possible duty saving is floor(0.30×40) − floor(0.15×40) = 12 − 6 = 6. Since S ≥ 5, night can only beat main when S = 5 and the duty saving is 6 or more (requiring H ≥ 40). In virtually every round, main is the answer. I pick night only when I verify the inequality is satisfied by actual arithmetic.

**I do not use opponents' scores, declarations, or routes to inform my play.** They have zero effect on my score. Each round is an independent optimization problem. I use the scoreboard only to confirm I am playing the correct seat.

**Final rounds are played identically to early rounds.** There is no "endgame aggression" or "lock in a lead" consideration. I declare H, compute both route scores, and pick the winner.