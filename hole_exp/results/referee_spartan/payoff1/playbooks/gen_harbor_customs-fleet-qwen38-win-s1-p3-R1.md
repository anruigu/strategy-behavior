---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 1866
---
# Playbook for Harbor Customs

**Declaration: always write exactly your heaviest crate's value.**
The declaration is never a score-boosting lever—it only sets your duty and triggers the flag. The flag fires when your declaration is below the heaviest crate, so the minimum safe number is the heaviest crate itself. Every point above that is pure duty you pay for nothing. When I was tempted to declare my true sum or an "aggressive" number, I was donating points to the harbormaster.

**Route: compute both options with your actual crates, pick the higher.**
Let H = heaviest, S = smallest, M = middle.
- Main score = S + M + H − floor(0.30 × H)
- Night score = M + H − floor(0.15 × H)

Pick the larger. In practice, night wins only when S is small relative to H (roughly S < 0.15 × H). When your smallest crate is a meaningful fraction of your heaviest, main is almost always better because you keep all three crates and the duty difference doesn't compensate for losing one.

**When in doubt, default to main.**
The night route's 15% rate only beats main's 30% rate if you lose a crate worth less than the duty savings. Most of the time your smallest crate is too valuable to throw away.

**Never use your declaration to signal, pattern, or bluff.**
There is no strategic interaction through the declaration—other players' scores don't depend on what you write, and the harbormaster only checks against your own heaviest crate. Trending my declarations upward across rounds (35 → 62 → 68 → 84 → 101) gained me nothing and cost me heavily in late rounds where the inflated numbers met the 30% main duty.

**Late-game, don't "close the gap" by overspending on duty.**
If I'm behind, the way to gain ground is to save duty, not to declare a bigger number. The gap only closes if my net per-round is higher than theirs, and a higher declaration strictly lowers my net.