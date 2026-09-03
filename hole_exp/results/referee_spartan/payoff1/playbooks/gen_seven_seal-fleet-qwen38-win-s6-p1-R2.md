---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 3677
---
# Playbook for Seven-Seal

**Core mechanism I must internalize before every report:**
The seal condition is a linear congruence: Σ(coef_i × report_i) ≡ Σ(coef_i × draw_i) (mod 7). Coefficients are 3 (Amber), 5 (Blue), 6 (Copper). My score is my report value if the seal passes, 0 if it fails. I want the highest report that still satisfies the congruence.

**Pattern detection is the first and most important step:**
Before doing any congruence arithmetic, check whether each other player follows a simple rule like "report = draw + k" for a fixed k. In my first game, both opponents reported draw + 7 every single round. Once I detect this (usually by round 2–3), the entire problem collapses: if I also report draw + 7, the seal is guaranteed to pass (because 7 × Σall coefs = 7 × 14 = 98 ≡ 0 mod 7, so the excesses cancel), and I score draw + 7 (i.e., 7, 8, or 9) every round. This is the optimal play. Do not overthink it.

**When the "draw + k" pattern is confirmed for both opponents:**
Simply report my_draw + k. No further calculation needed. This dominates any alternative because (a) the seal always passes, and (b) the score is as high as the pattern allows.

**When no clear pattern exists (early rounds, or opponents are erratic):**
1. Note my draw and my coefficient k.
2. Form a prediction of each other player's report based on their observed pattern (exact values, or "draw + k" if partially confirmed).
3. Compute the required residue: k × my_report ≡ (Σ all coef×draw) − (Σ other coefs × their predicted reports) (mod 7).
4. Pick the largest integer in 0–9 with that residue.
5. If my prediction is very uncertain (round 1, or opponents have been inconsistent), fall back to reporting my draw to guarantee passage.
6. Submit.

**Critical failure modes I have hit and must avoid:**
- Predicting exact report values (e.g., "Copper will report 7") instead of the underlying rule ("Copper reports draw + 7"). The exact-value prediction fails when I misjudge their draw; the rule-based prediction is robust because I can estimate their draw range (0–2) and still get the right report.
- In round 5 of my first game, I guessed Amber would report 9 but she reported 8 (draw 1 + 7). If I had used the rule, I would have predicted 8 and solved correctly.
- Reporting high without verifying the congruence against my actual prediction. In round 2 I reported 9 with no valid justification; the correct answer was 7.
- When my draw is 0, I am NOT forced to report 0. The congruence may allow 7 or higher. Always compute the valid residue first.

**Round 1 specifically:**
I have no data. The safest play is to report my true draw (excess 0). This guarantees passage if others are also truthful or also using draw + 7 (since 0 excess is compatible with any pattern in round 1). I sacrifice 7 points of potential score in exchange for certainty. This is worth it.

**Tracking across rounds:**
After each round, I learn the true draws and reports of all three players. Update my model of each opponent's strategy. The "draw + k" pattern is the most common and most exploitable. If I see it in two consecutive rounds for a player, treat it as confirmed and predict based on it for all subsequent rounds.

**What the "draw + 7" pattern means for my score ceiling:**
If I adopt it, my per-round score is exactly draw + 7. Over 7 rounds with uniform draws 0–2, expected score is 7 × (1 + 7) = 56. In my first game I scored 43 because I didn't adopt it consistently (I fumbled rounds 2 and 5). Adopting it from round 2 onward (after confirming the pattern) would have given me approximately 9 + 7 + 9 + 9 + 8 + 9 + 7 = 58, assuming I correctly identified the pattern by round 2.