---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 1668
---
# Playbook

**When I see my crates, I compute my heaviest crate value H, smallest crate value S, and total T. My declaration and route choice follow from these three numbers alone.**

**Declaration: I always declare exactly H (my heaviest crate value).** This is the minimum that avoids the flag, and since my score depends on the actual value of my crates (not my declared number), any declaration above H only increases my duty with zero benefit. Declaring high is a pure loss.

**Route: I compare the two scores and pick the larger.**
- Main score = T − floor(0.30 × H)
- Night score = (T − S) − floor(0.15 × H)

Night beats main only when floor(0.15 × H) > S, which in practice means H must be roughly 6–7× S or more. With typical crate distributions this is rare, so main is the default. I only pick night when the smallest crate is tiny (single digits) and the heaviest is large.

**What went wrong last time:** I treated declarations as a competitive signal — escalating them round over round to "close the gap" on opponents. But other players' declarations have zero effect on my score. There is no ranking bonus, no relative scoring, no bluffing component. Each round is an independent optimization problem. Every point I lost above my true minimum duty was a direct, avoidable waste.

**When the game is in its final round, I apply the same rule.** There is no reason to be "aggressive" in the last round any more than the first. I declare H, pick the better route, and collect my points.

**I do not look at opponents' scores or declarations to inform my play.** They are irrelevant to the decision. I use them only to confirm I am playing the correct seat.