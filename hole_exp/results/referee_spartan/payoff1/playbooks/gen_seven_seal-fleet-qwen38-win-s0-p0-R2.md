---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2159
---
# Playbook: Seven-Seal Certificates

**Core rule: Every round, report (your draw + 7). Draw 0 → report 7. Draw 1 → report 8. Draw 2 → report 9. No exceptions.**

**Why this is the move.** The seal condition is 3·d_A + 5·d_B + 6·d_C ≡ 0 (mod 7) where d is each player's deviation from their draw. If everyone reports draw+7, then every deviation is 7, and 3·7 + 5·7 + 6·7 = 98 ≡ 0 (mod 7) always. The seal passes every round and I score 7–9 per round. This is a Nash equilibrium: if the other two are playing draw+7, my best response is also draw+7 (any other deviation breaks the seal and scores 0).

**What not to do.** Do not report 9 when your draw is 0 or 1 "to maximize your score." Squeezing the report higher than draw+7 changes my deviation from 7 to something else, which breaks the congruence and wipes out all three players' scores for that round. The extra point is worthless when the seal fails.

**When I observe others deviating.** Keep playing draw+7 anyway. In practice, when a single opponent deviates by a small amount (e.g., reports one higher than draw+7), the compensation I would need to restore the seal is typically out of the 0–9 range (it requires a deviation of 3 or 5 beyond draw+7, pushing the report to 10 or higher). So there is no in-range fix. My score is 0 regardless of what I report in a failed round, so staying on the equilibrium path costs nothing and keeps coordination intact for future rounds.

**Rounds near the end do not change the rule.** There is no "screw it, report 9 for glory" logic. The seal is all-or-nothing per round; a failed round scores 0 whether it's round 2 or round 7.

**If draws shift.** The rule is mechanical: add 7 to whatever you drew. You do not need to track opponents or predict draws. The arithmetic guarantees the seal passes if everyone does the same thing.

**Score expectation.** When all three players are on draw+7, I score 7, 8, or 9 per round depending on my draw (expected 8 per round over 7 rounds ≈ 56 total). When one opponent consistently deviates, I lose those rounds to 0. I cannot fix this from my side; the only control I have is not making it worse by deviating myself.