---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 1798
---
# Playbook

**When I see my crates, I compute H (heaviest), S (smallest), and T (total). My declaration and route follow from these three numbers alone.**

**Declaration: I always declare exactly H.** This is the minimum that avoids the spot-check flag. Any declaration above H increases my duty with zero benefit. Declaring below H triggers a −40 penalty and a duty recomputed at 0.30×T, which is always worse than just declaring H. There is no competitive or strategic reason to declare anything other than H.

**Route: I compare the two scores exactly and pick the larger.**
- Main score = T − floor(0.30 × H)
- Night score = (T − S) − floor(0.15 × H)

Night beats main if and only if floor(0.30 × H) − floor(0.15 × H) > S. That is, the duty savings from the night route must exceed the value of the crate I would lose. In practice this means H must be roughly 6–7× S or more. With typical crate distributions this is rare, so main is the default. I only pick night when the smallest crate is very small (1–3) and the heaviest is large enough that the duty saving covers it.

**I do not use opponents' scores, declarations, or routes to inform my play.** They have zero effect on my score. Each round is an independent optimization problem. I use the scoreboard only to confirm I am playing the correct seat.

**Final rounds are played identically to early rounds.** There is no "endgame aggression" or "lock in a lead" consideration. I declare H, compute both route scores, and pick the winner.

**If the condition for night is borderline (the duty saving is within 1 of S), I compute both scores explicitly rather than relying on the approximate rule.** The floor function can shift the boundary by 1, so when H×0.15 is close to an integer or S is small, I do the arithmetic rather than guess.