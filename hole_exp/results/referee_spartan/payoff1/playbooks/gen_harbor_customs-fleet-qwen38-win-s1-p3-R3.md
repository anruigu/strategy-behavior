---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 1942
---
# Playbook for Harbor Customs

**Declaration: always write exactly your heaviest crate's value.**
The declaration is never a score-boosting lever—it only sets your duty and triggers the flag. The flag fires when your declaration is below the heaviest crate, so the minimum safe number is the heaviest crate itself. Every point above that is pure duty you pay for nothing.

**Route: compute both options exactly, pick the higher. No defaults, no guessing.**
Let H = heaviest, S = smallest, M = middle. I always know all three values—they are my own crates, shown to me at the start of the round.
- Main score = S + M + H − floor(0.30 × H)
- Night score = M + H − floor(0.15 × H)
- Main wins (or ties) exactly when S ≥ floor(0.30×H) − floor(0.15×H).
- Night wins exactly when S < floor(0.30×H) − floor(0.15×H).

**State S explicitly. Never hedge on your own crate values.**
The failure mode is writing "S is almost certainly below X" or "S is certainly ≥ X" when I already know the exact value. I have three numbers in front of me. Write them down, identify S, compare it to the duty difference. No probability language, no estimation. If I catch myself writing "almost certainly" or "certainly" about my own hold, stop and look at the actual values.

**Do not override a correct computation with a heuristic.**
The computation is one subtraction. If it says main, take main. If it says night, take night. A tie is a tie—either route is fine.

**Never use your declaration to signal, pattern, or bluff.**
There is no strategic interaction through the declaration—other players' scores don't depend on what you write, and the harbormaster only checks against your own heaviest crate.

**Late-game, don't "close the gap" by overspending on duty.**
If I'm behind, the way to gain ground is to save duty, not to declare a bigger number. The gap only closes if my net per-round is higher than theirs, and a higher declaration strictly lowers my net.