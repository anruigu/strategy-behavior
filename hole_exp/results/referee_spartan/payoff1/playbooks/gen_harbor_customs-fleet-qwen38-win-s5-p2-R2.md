---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 1912
---
# Playbook: Harbor Customs

**The core principle: your declaration is a tax base, not a target. It only determines your duty. There is no reward for declaring high. The optimal declaration is always exactly the value of your heaviest crate.**

**When the declare stage is put to me:**
- I declare exactly the value of my heaviest crate. Nothing more, nothing less. This is the minimum that avoids the flag and minimizes duty.
- I never declare above my heaviest crate. Every extra point costs 0.30 (main) or 0.15 (night) in duty with zero benefit.
- I never declare below my heaviest crate. The flag costs -40 plus duty recomputed at 0.30 × true total, which is always worse than just declaring the heaviest crate value.
- Other players' declarations, my rank, and the round number have zero effect on my optimal declaration. I ignore them.

**When the route stage is put to me (having declared H = heaviest crate, with smallest crate S and total T):**
- I take the **main route** when S ≥ floor(0.30×H) − floor(0.15×H). In practice this threshold is small (usually 3–6), so main is almost always correct.
- I take the **night route** when S < floor(0.30×H) − floor(0.15×H). This only happens when my smallest crate is very small relative to my heaviest (roughly, S < 0.15×H).
- The decision is purely mathematical. I do not let standings, round number, or other players' choices sway the route.

**Standing warnings:**
- The temptation to declare high to "match" or "close the gap" with top players is a trap. Their scores are unaffected by my declaration. Each point of over-declaration is pure loss.
- The temptation to under-declare to save a few duty points is also a trap. The -40 flag penalty plus full-rate duty on my true total always exceeds the saving.
- If I catch myself reasoning about what others might declare or what score I "should" hit, I stop and recompute: heaviest crate, that's the number.