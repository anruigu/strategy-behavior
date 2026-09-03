---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 1496
---
# Playbook

**Declare: always declare exactly your heaviest crate's value.** The declaration only feeds into the duty calculation; it never adds points. The only hard constraint is that it must be ≥ the heaviest crate or you get flagged (−40 plus duty at 0.30× true total). So the optimal declaration is the minimum that avoids the flag: your heaviest crate, no more.

**Route: almost always take main.** With the declaration set to the heaviest crate H and smallest crate s, main scores S − floor(0.30H) while night scores S − s − floor(0.15H). Night beats main only when floor(0.30H) − floor(0.15H) > s. That gap maxes out at 6 (when H = 40) and s is always ≥ 5, so the sole exception is s = 5 and H = 40, where night gains exactly 1 point. In every other case main is strictly better.

**When I feel behind on points, I do not inflate my declaration.** A higher declaration only raises my duty with no offsetting gain. Being in last place is not a reason to declare 120; it is a reason to declare the minimum safe number and collect the full crate value minus the smallest possible duty.

**Concrete procedure each round:**
1. Note my three crate values. Identify the heaviest (H) and the smallest (s).
2. Declare H.
3. Take main, unless s = 5 and H = 40, in which case take night.

**Nature of the game:** This is a solo optimization problem against the harbormaster, not a contest of deception. All players converge on the same dominant strategy (declare H, take main). No reason to deviate.