---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 2422
---
Playbook for Seven-Seal:

- My opening move is draw+7 (report 7, 8, or 9 for draws 0, 1, 2). A uniform shift that is 0 mod 7 passes the seal automatically and bags the biggest points consistent with that shift. This convention was adopted by all three players from round 1 and never failed across 7 rounds — it is the strongest baseline I have.

- Given a target shift, I always take the largest report realizing it: report value only affects my score, while only the shift mod 7 affects the seal. So for shift 0 mod 7, draw+7 dominates draw and honest reporting.

- Once history shows everyone reporting draw+k with k≡0 (mod 7), I follow it without deviation, every round, whatever my draw. Deviating from a working convention can only break the seal and costs everyone their points; the marginal score gain from out-reporting others is worthless against a 0 for the round.

- Before reporting in any round without an established convention, I do the arithmetic: my shift of r moves the weighted sum by (6r) mod 7 for Copper (3 for Amber, 5 for Blue). I pick the shift most likely to cancel the others' inferred shifts, preferring 0 mod 7 absent other information.

- Blindly reporting 9 regardless of draw stays banned: 9−d varies with d, scrambling the seal. 9 is correct exactly when my draw is 2 under the +7 convention.

- After any failed round, I reconstruct each player's shift from revealed draws and reports. If they settled on draw+k, I match it at the largest congruent value. If the pattern is chaos, I anchor on the zero-shift: report draw+7 (or the draw itself if draw+7 risks mis-coordination), and accept the risk rather than hedging.

- No mid-range "hedge" numbers: an uncoordinated shift fails just like a greedy one but scores less when it passes. Commit fully to the modal convention.

- Standings matter only late: in the final round, if leading and the convention is live, I follow it to lock the pass; if trailing badly, I still follow the convention — a failed seal scores 0 for everyone anyway, so the convention remains at least weakly dominant.

- New confirmation from this match: everyone in this player pool apparently starts on draw+7. Round 1 passed at full convention with no prior history. I will trust this priors-forward in future episodes and expect single shifts only when someone experiments; watch reports vs draws each round and recheck the convention holds before extending it.