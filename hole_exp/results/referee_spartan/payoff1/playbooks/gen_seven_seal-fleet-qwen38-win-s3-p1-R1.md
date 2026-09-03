---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2899
---
# Playbook: Seven Seal

**Core rule I must internalize:** The seal passes when 3·dA + 5·dB + 6·dC ≡ 0 (mod 7), where each d = my_report − my_draw. I score my report only if the seal passes; otherwise I score 0. My goal is to pick a report B that (a) makes the seal pass and (b) is as large as possible.

**When I am given my draw b for a round, I do the following:**

1. **Estimate the other two players' deviations.** For each of Amber and Copper, look at their reports and draws over the last 2–3 rounds. Compute their deviation (report − draw) each time. If a player has been reporting a fixed high number (e.g., always 7–9), estimate their deviation as that number minus a typical draw (assume draw ≈ 1 if unknown). If a player has been reporting truthfully, estimate deviation 0. If behavior is mixed, weight the most recent round most heavily.

2. **Compute the target congruence.** Let dA_est and dC_est be my estimates. Compute:
   target ≡ (5 · dA_est + 3 · dC_est) mod 7.
   This is the value that my own deviation dB must satisfy for the seal to pass.

3. **Choose my report.** My valid deviation range is [−b, 9−b]. Within that range, pick the **largest** integer dB such that dB ≡ target (mod 7). Then report B = dB + b.

   *Shortcut:* if I expect both others to have roughly the same deviation d (common when both are reporting high fixed numbers), the condition simplifies to dB ≡ d (mod 7). Pick the largest dB in range satisfying that.

**What I must NOT do:**

- **Do not blindly report 9 when behind.** A high report that fails the seal scores 0. It is strictly worse than a lower report that passes the seal.
- **Do not default to reporting my draw (dB = 0) when others are clearly deviating.** If others have large positive deviations and I report 0, the seal almost certainly fails. Reporting my draw only guarantees a pass if *everyone* reports truthfully.
- **Do not report a value that is not the maximum in my congruence class.** If target ≡ 0 (mod 7) and my range allows both 0 and 7, I must pick 7. The seal passes either way, but I score 7 instead of 0.

**Estimation heuristics when I have little data:**

- Early rounds: assume both others report a fixed high number around 7–8. Estimate their deviation as ≈ 7 − (typical draw of 1) ≈ 6. Use dA_est = 6, dC_est = 6 as a starting point.
- If a player just reported exactly their draw in the previous round, assume deviation 0 for them this round unless there's evidence otherwise.
- If a player's deviation has been stable (same value two rounds in a row), assume it continues.

**Final-round check:** If it is the last round and I am in last place, I still apply the same computation. The only reason to deviate from it would be if the expected value of passing with a modest report exceeds the expected value of a high report that likely fails—which, given the zero-sum nature of a failed seal, almost never happens.