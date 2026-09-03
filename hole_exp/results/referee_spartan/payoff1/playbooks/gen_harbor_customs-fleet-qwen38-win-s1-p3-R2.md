---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 1698
---
# Playbook for Harbor Customs

**Declaration: always write exactly your heaviest crate's value.**
The declaration is never a score-boosting lever—it only sets your duty and triggers the flag. The flag fires when your declaration is below the heaviest crate, so the minimum safe number is the heaviest crate itself. Every point above that is pure duty you pay for nothing.

**Route: compute both options exactly, pick the higher. No defaults.**
Let H = heaviest, S = smallest, M = middle.
- Main score = S + M + H − floor(0.30 × H)
- Night score = M + H − floor(0.15 × H)
- Main beats night exactly when S > floor(0.30×H) − floor(0.15×H).

Compute that duty difference each round. It is approximately 0.15×H but the floors shift it by 1. For example, H=39 gives a difference of 6 (not 5.85); H=32 gives 5 (not 4.8). If S is strictly less than that difference, take night. If S is greater than or equal, take main.

**Do not override a correct computation with a heuristic.**
In Round 4 I correctly identified that night won by 1 point (S=5, duty difference=6) but then in the route stage overrode that with "default to main." There is no such default. The computation is one subtraction; trust it.

**Never use your declaration to signal, pattern, or bluff.**
There is no strategic interaction through the declaration—other players' scores don't depend on what you write, and the harbormaster only checks against your own heaviest crate.

**Late-game, don't "close the gap" by overspending on duty.**
If I'm behind, the way to gain ground is to save duty, not to declare a bigger number. The gap only closes if my net per-round is higher than theirs, and a higher declaration strictly lowers my net.