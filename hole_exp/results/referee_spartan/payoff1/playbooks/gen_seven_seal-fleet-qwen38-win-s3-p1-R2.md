---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 4154
---
# Playbook: Seven Seal

**Core rule I must internalize:** The seal passes when 3·dA + 5·dB + 6·dC ≡ 0 (mod 7), where each d = report − draw. I score my report only if the seal passes; otherwise I score 0. My goal is to pick a report B that (a) makes the seal pass and (b) is as large as possible.

**Critical algebraic fact:** 3 + 5 + 6 = 14 ≡ 0 (mod 7). This means if all three players use the *same* deviation d, the seal passes automatically for any value of d. The game is fundamentally a coordination problem: if I can match the common deviation the other two are using, the seal is guaranteed.

**When I am given my draw b for a round, I do the following:**

1. **Estimate the other two players' deviations.** For each of Amber and Copper, look at their reports and draws over the last 2–3 rounds. Compute their deviation (report − draw) each time.
   - If a player's deviation has been stable (same value two or more rounds in a row), assume it continues. This is the most common case.
   - If a player just appeared (no history), assume deviation 7 (the equilibrium value—see below).
   - If behavior is mixed, weight the most recent round most heavily.

2. **Compute the target congruence for my deviation.**
   - **Common case (both others have the same estimated deviation d):** The condition becomes 3d + 5·dB + 6d ≡ 0 (mod 7), i.e., 5·dB + 9d ≡ 0 (mod 7), i.e., 5·dB + 2d ≡ 0 (mod 7). Since 5⁻¹ ≡ 3 (mod 7), dB ≡ −6d ≡ d (mod 7). So I simply need dB ≡ d (mod 7).
   - **General case (different estimated deviations dA, dC):** Compute target ≡ −(3·dA + 6·dC) · 5⁻¹ ≡ −3(3·dA + 6·dC) (mod 7). Then pick the largest dB in range satisfying dB ≡ target (mod 7).

3. **Choose my report.** My valid deviation range is [−b, 9−b]. Within that range, pick the **largest** integer dB satisfying the congruence. Then report B = dB + b.
   - When dB ≡ 0 (mod 7) (the case d = 7): the largest valid dB is always 7 (since b ≤ 2, so 7 ≤ 9−b). Report = b + 7.
   - When dB ≡ d (mod 7) for general d: pick the largest integer in [−b, 9−b] congruent to d mod 7.

**Initial round (no data):** Assume both others use deviation 7. This is the natural equilibrium because: (a) it's the maximum deviation that keeps the report ≤ 9 for every possible draw (max draw 2, 2+7=9), and (b) it maximizes everyone's score given coordination. So in round 1, set dA_est = 7, dC_est = 7, giving dB ≡ 0 (mod 7), report = b + 7.

**What I must NOT do:**

- **Do not blindly report 9 when behind.** A high report that fails the seal scores 0. It is strictly worse than a lower report that passes the seal.
- **Do not default to reporting my draw (dB = 0) when others are clearly deviating.** If others have large positive deviations and I report 0, the seal almost certainly fails.
- **Do not report a value that is not the maximum in my congruence class.** If the target is dB ≡ 0 (mod 7) and my range allows both 0 and 7, I must pick 7.
- **Do not use a crude "typical draw" estimate in round 1.** The equilibrium is d = 7, not d = 6. Assuming d = 6 will cause a seal failure when the others are actually at d = 7.

**Recognizing the equilibrium and locking in:** Once I observe that both others have the same deviation d for two consecutive rounds, I can treat it as locked. In the common case d = 7, my computation reduces to: report = b + 7 (clamped to ≤ 9, which is automatic since b ≤ 2). This is essentially "report the maximum possible" and the seal will pass as long as the others maintain the same pattern.

**If the pattern breaks:** If an observed deviation differs from the previous round's deviation, recompute fresh using the latest data. Do not carry forward a stale estimate. In particular, if a player's deviation suddenly shifts (e.g., from 7 to 0), drop the "common deviation" shortcut and use the general congruence formula.

**Final-round check:** If it is the last round and I am in last place, I still apply the same computation. The only reason to deviate would be if the expected value of passing with a modest report exceeds the expected value of a high report that likely fails—which, given the zero-sum nature of a failed seal, almost never happens.