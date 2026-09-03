---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 2768
---
The core rule: my declaration only costs me — duty scales with it, and declaration above my true total raises duty without adding any points. Never overdeclare.

- When declaring, compute my true total T and my heaviest crate H. My declaration is always between H and T (or below H only if I've deliberately accepted the flag risk — which I almost never should).
- Default: declare exactly T. Underdeclaring below T saves only 0.30 per point (main) or 0.15 per point (night) and gains nothing else. The gap to my heaviest crate is the only "free" underdeclaration space.
- The optimal play I underused: declare H (heaviest crate), not T, when T−H is large and I plan main. Duty saved = 0.30×(T−H); the only constraint is d ≥ H to pass the spot check. E.g., hold 6/19/24: declare 24, not 49 — saves 7 duty, loses nothing. Flagging the smallest crate means the check only sees the heaviest, so declaring anything from H up is safe.
- Never declare above T — a big declaration is pure duty waste. When I fell behind and declared 100 on a 64 hold, I paid ~11 extra duty for zero gain; overdeclaring cannot close a points gap. I will not do this again.
- Standing behind a leader: the way to catch up is minimizing duties and choosing routes correctly, not inflating the manifest.

Route choice — compare exactly:
- Main keeps: T − floor(0.28–0.30×d). Night keeps: (T − smallest) − floor(0.15×d).
- Take night when 0.15×d < value of my smallest crate, roughly. Concretely: night beats main when smallest crate value > 0.15×d. With d around 40 and smallest crate under ~6, main; smallest crate above ~7–8, night is usually better.
- If I've declared d = H (underdeclare strategy) and smallest crate is significant, recompute: night duty at 0.15×H can be tiny while confiscation costs the smallest crate — often declaring T and going night beats underdeclaring with main. Do the full arithmetic each round: max over (declare, route) pairs of expected keep.
- Flag risk on night: the check still only sees the heaviest crate, so d ≥ H stays safe on either route. The confiscation does not change the check.
- Only consider declaring below H (accepting −40 and 0.30×full duty) essentially never — the penalty dwarfs any duty saving. Skip it.

Playbook per round:
1. Compute T, H, smallest S.
2. Candidate A: declare H, route main. Score = T − floor(0.30×H).
3. Candidate B: declare T, route night. Score = T − S − floor(0.15×T).
4. Candidate C: declare T, route main. Score = T − floor(0.30×T).
5. Pick the highest; ties favor main (less variance) and favor keeping all three crates.
6. Ignore opponents' scores when setting my declaration; use the standings only if a tiebreak truly needs variance late — and even then, route choice is the variance lever, not overdeclaration.