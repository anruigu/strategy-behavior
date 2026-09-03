---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 1757
---
# Playbook: Seven-Seal Certificates

**Core rule: Every round, report (your draw + 7). Draw 0 → report 7. Draw 1 → report 8. Draw 2 → report 9. No exceptions.**

**Why this is the move.** The seal condition is 3·d_A + 5·d_B + 6·d_C ≡ 0 (mod 7) where d is each player's deviation from their draw. If everyone reports draw+7, then every deviation is 7, and 3·7 + 5·7 + 6·7 = 98 ≡ 0 (mod 7) always. The seal passes every round and I score 7–9 per round. This is a Nash equilibrium: if the other two are playing draw+7, my best response is also draw+7 (any other deviation breaks the seal and scores 0).

**What not to do.** Do not report 9 when your draw is 0 or 1 "to maximize your score." I did this in most rounds and the seal failed every single time. The extra point of report is worthless when the seal fails; the round scores 0. Squeezing from 8 to 9 (when draw is 1) changed my deviation from 7 to 8, which broke the congruence and wiped out all three players' scores.

**When I observe others deviating.** Keep playing draw+7 anyway. If the seal fails because of their deviation, my score is 0 regardless of what I report—so there's no cost to staying on the equilibrium path. Staying consistent also keeps the door open for coordination: if I ever flip to a different pattern, I make it harder for all three of us to ever land back on a passing configuration.

**Rounds near the end do not change the rule.** There is no "screw it, report 9 for glory" logic. The seal is all-or-nothing per round; a failed round is 0 whether it's round 2 or round 7.

**If draws shift.** The rule is mechanical: add 7 to whatever you drew. You do not need to track opponents or predict draws. The arithmetic guarantees the seal passes if everyone does the same thing.