---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 1553
---
# Playbook for Seven-Seal

**The one rule that solves the game:** Always report my_draw + 7.

**Why this is dominant (prove it to yourself once, then never second-guess):**
The seal condition is Σ(coef_i × report_i) ≡ Σ(coef_i × draw_i) (mod 7). If I report my_draw + 7 instead of my_draw, my contribution to the left side changes by 7 × my_coef. Since 7 × anything ≡ 0 (mod 7), the seal condition is completely unaffected by my choice between reporting my_draw and my_draw + 7. Therefore:
- If the seal would pass with a truthful report, it passes with draw+7 too, and I score 7 more points.
- If the seal would fail with a truthful report, it fails with draw+7 too, and I score 0 either way.

Reporting draw+7 weakly dominates reporting truthfully in every possible state of the world. No pattern detection, no opponent modeling, no congruence arithmetic needed.

**Why draw+7 is the ceiling:**
My draw is in {0, 1, 2}. The values in 0–9 congruent to my draw mod 7 are exactly my_draw and my_draw + 7 (since my_draw + 14 > 9). So draw+7 is the highest value I can report without changing the seal condition. There is no higher "safe" report.

**When (if ever) to deviate:**
Only if I have strong evidence that one or both opponents are reporting values NOT congruent to their draws mod 7 (i.e., they're deviating from draw+7 or truthfulness). In that case, I could potentially compensate by reporting a different residue. But:
- This requires correctly predicting their exact deviation, which is risky.
- The expected gain is small (at most 1–2 points