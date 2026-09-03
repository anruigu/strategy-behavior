---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 1681
---
# Playbook: Harbor Customs

**Declaration rule (most important):** Always declare exactly your heaviest crate value. This is the minimum that avoids the flag, and since duty scales with your declared value, any amount above the minimum is pure loss. There is no upside to declaring higher — the game never rewards a high declaration, it only extracts more duty.

**Route rule:** Compare your heaviest crate to roughly 6.7× your smallest crate.
- If heaviest > 6.7 × smallest → take night (the low duty rate saves more than you lose by confiscating the smallest crate).
- Otherwise → take main (you keep all three crates and the duty difference isn't worth the lost crate).

**What I did wrong:** In the middle and late rounds I started inflating my declarations upward (54, 62, 72, 80, 84) because I felt pressure to "close the gap" on the leader. This cost me roughly 40–50 points across the game. The instinct to escalate your declaration when you're behind is the single most expensive mistake in this game. Your score is determined entirely by your true crate values minus duty; the declaration is a cost lever you control, not a scoring lever.

**When the score display shows you trailing:** Do nothing different. Declare your heaviest, pick the route by the 6.7× rule, and accept the round. The gap closes or doesn't based on crate luck, not on your declaration.

**When you are leading:** Same thing. There is no "safe" higher declaration to protect your lead. Declaring your heaviest is always optimal regardless of your position.

**Tie-breaking within a round:** If the 6.7× ratio is close to the boundary, compute both scores exactly with floors and pick the higher one.