---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 2891
---
# Playbook: Seven-Seal

**The constraint I must satisfy every round:**

Let d_A, d_B, d_C be the deviations (report minus draw) for Amber, Blue, and me. The seal passes if and only if:

3·d_A + 5·d_B + 6·d_C ≡ 0 (mod 7)

Since 6 ≡ −1 (mod 7), this simplifies to:

d_C ≡ 3·d_A + 5·d_B (mod 7)

**When I am asked to report, I do the following in order:**

1. **Predict the other two players' deviations.** Use each player's deviation from the most recent round where it was revealed. If a player has used the same deviation for 2+ consecutive rounds, treat that as their default and expect it to continue. If a player just changed their deviation, use the new value.

2. **Compute k = (3·d_A_pred + 5·d_B_pred) mod 7.** This is the residue my deviation must satisfy.

3. **Compute r = (my_draw + k) mod 7.** This is the residue my report must satisfy mod 7.

4. **Choose my report C as the largest integer in [0, 9] with C ≡ r (mod 7).** Concretely: if r ≤ 2, report r + 7; otherwise report r. This maximizes my score subject to the seal passing.

**Tracking discipline:**

- After each round's results are revealed, immediately record each player's deviation (report − draw) in my mental log.
- If a player's deviation shifts, note it and update my prediction for the next round.

**What I must not do:**

- Do not report a number "to differ from" an opponent. The seal is a weighted sum constraint, not an inequality. Changing my report to be different from theirs is meaningless unless it satisfies the mod-7 equation.
- Do not report my draw (truthful reporting) as a fallback. It scores nothing extra and wastes the chance to add 7.
- Do not report 9 unconditionally. It only passes the seal when my deviation happens to equal 9 − my_draw and that satisfies the constraint. Verify before committing.
- Do not skip the computation to "play safe." A failed seal gives everyone 0; a correctly computed report always scores at least 0 and usually scores high. The expected value of computing is strictly better than guessing.

**If my prediction of an opponent's deviation is wrong:**

The seal will fail and I score 0 for that round. This is the cost of imperfect prediction. Mitigation: if an opponent has been inconsistent (deviation changes frequently), lower my report slightly (choose the smaller valid C, i.e., r instead of r+7) to reduce the gap if I end up behind, but never below 0. In practice, with only 3 possible draws and a small deviation space, opponents tend to settle into a pattern quickly, so the most-recent-deviation predictor should work well after round 2.

**First round (no history):**

If I have no prior data on opponents, assume d_A = d_B = 7 (reporting 9 is the obvious greedy move and the most common default). Then k = (21+35) mod 7 = 0, so r = my_draw, and I report my_draw + 7. This scores 7–9 points and passes the seal if both opponents also deviate by 7.