---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 1991
---
# Playbook: Harbor Customs

**Declaration rule (most important):** Always declare exactly your heaviest crate value. This is the minimum that avoids the flag, and since duty scales with your declared value, any amount above the minimum is pure loss. There is no upside to declaring higher — the game never rewards a high declaration, it only extracts more duty.

**Route rule:** Compare your heaviest crate (your declared value D) to roughly 6.67× your smallest crate.
- If D > 6.67 × smallest → take night (the low duty rate saves more than you lose by confiscating the smallest crate).
- Otherwise → take main (you keep all three crates and the duty difference isn't worth the lost crate).

In practice, across full games the heaviest/smallest ratio rarely exceeds 5, so main is the overwhelming default. Night only becomes relevant when the smallest crate is genuinely tiny relative to the heaviest (e.g., smallest ≤ 5 and heaviest ≥ 36). If you ever see a ratio above 6, stop and compute exactly.

**Near the boundary:** Because of floor functions, the 6.67× rule is an approximation. When the ratio is between 6 and 8, compute both scores exactly: main = (sum of all three) − floor(0.30 × D), night = (sum minus smallest) − floor(0.15 × D), where D is your declared value (your heaviest crate). Pick the higher.

**The temptation to inflate:** When the score display shows you trailing, the instinct is to declare higher to "close the gap." Do not do this. Your score is determined entirely by your true crate values minus duty; the declaration is a cost lever you control, not a scoring lever. Inflating your declaration when you are behind costs you points every round. Declare your heaviest, pick the route by the rule, and accept the round. The gap closes or doesn't based on crate luck, not on your declaration.

**When you are leading:** Same thing. There is no "safe" higher declaration to protect your lead. Declaring your heaviest is always optimal regardless of your position.