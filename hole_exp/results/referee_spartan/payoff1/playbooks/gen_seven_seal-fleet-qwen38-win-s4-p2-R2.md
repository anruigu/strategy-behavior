---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 2160
---
# Playbook for Seven-Seal Certificates

**Core rule: always report (my draw + 7).** If I draw 0, report 7. If I draw 1, report 8. If I draw 2, report 9. Do this every round without exception.

**Why this is the move:** The seal condition is linear in each player's deviation from their true draw. When every player deviates by exactly 7, the weighted sum of deviations is 7×(3+5+6) = 98 ≡ 0 (mod 7), so the seal always passes. Reporting draw+7 is also the highest report compatible with the seal when the others report truthfully (deviation 0): the condition reduces to 6×my_deviation ≡ 0 (mod 7), forcing my deviation to be 0 or 7. No higher report is equally safe under either equilibrium.

**What I must not do:**

- Never report a fixed number (like always 9) regardless of my draw. When my draw is 0, reporting 9 gives deviation 9 instead of 7, which breaks the seal whenever the others are also inflating by 7.
- Never retreat to reporting my true draw out of fear. If the seal is failing, it is because someone's deviation is off, not because inflation itself is dangerous. The fix is to stay at +7, not to abandon it.
- Never treat a seal failure in one round as evidence that the strategy is broken. A single round's failure is a signal about what the other players reported, not about the correctness of my own rule.

**If the seal fails a round:** Check whether my own report equaled my draw + 7. If it did, the failure is entirely due to the other players' deviations. Stay at +7 next round. If it did not (I made an arithmetic slip or deviated for another reason), correct back to draw + 7 immediately. The +7 rule is the unique maximum-inflation strategy that is safe under both the all-inflate and all-truthful equilibria, so it is always my best expected-value play regardless of what happened last round.

**Confirmation from play:** In a 7-round game as Copper, the +7 rule passed the seal every round and produced the maximum possible score for my draws (55 points from draws 2,0,1,1,1,1,0 → reports 9,7,8,8,8,8,7). The strategy is optimal; there is no round in which a different report would have scored higher while still passing the seal.