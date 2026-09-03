---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 3148
---
When I get my private draw d, I default to the highest report with the same residue mod 7: report 7 on 0, 8 on 1, 9 on 2. This never worsens my own seal contribution and strictly improves my payoff if accepted.

I do not report my actual low draw as "safe"; 0/1/2 gives the same residue as 7/8/9 but scores less when accepted, so it forgoes upside without helping the seal.

I do not blind-report 9 unless my draw is 2 or I have computed that the residue is required; a 9 from draw 0 or 1 changes my weighted term and can be the marginal cause of a failed seal.

Each round I convert every shown report to its residue mod 7 and compare it with the revealed draws to infer whether each opponent is residue-preserving, always inflating, or random; I update my forecast of their next report from that pattern, not from their score alone.

When opponents are consistently residue-preserving high (as they were across all seven rounds this episode), I stop re-deriving offsets and simply play my residue-preserving high report immediately; the seal then passes automatically since all reports match all draws mod 7. This mutual residue-preserving convention is self-sustaining: everyone gets maximum value and no one has an incentive to deviate, so I protect it rather than probe it.

This episode confirmed the default end-to-end: seven straight seal passes, no deviations by anyone, and I finished within one point of the leader despite trailing much of the game. Deviating to chase a one-point lead on round 7 would have risked a zero; in a stable residue-preserving equilibrium the ordering is set by draws, not by report choices, so I accept that.

Since everyone earns their report when the seal passes, scores are driven by the seat's coefficients only in that they affect nothing — each player's weighted term matters for the seal, not for their own points. I therefore never try to "counterweight" opponents' coefficients; I only ensure my own residue is correct relative to theirs.

On the final round there is no future to protect, but the same logic holds: the highest residue-consistent report weakly dominates any mismatching gamble, since a sealed 7/8/9 beats an unsealed anything.

Before deviating from the default, I estimate the other two weighted report residues, compute the residue my report must have to satisfy the seal equation, then choose the largest integer 0–9 with that residue; if I cannot forecast them confidently, I use my own residue-preserving high report.

When history shows repeated failures from everyone reporting 9, I treat "join the 9s" as a losing convention and keep my residue correct; I only deviate from residue-preserving high if the arithmetic says my offset is needed to make the seal pass.

If I am behind late, I still prefer the highest residue-consistent report rather than a hopeful mismatch, because a failed seal scores zero and preserves the gap.

If every likely opponent report combination makes acceptance impossible regardless of my residue, I recognize my report cannot affect the outcome and still choose the residue-preserving high number so I keep maximum value if my forecast is wrong.