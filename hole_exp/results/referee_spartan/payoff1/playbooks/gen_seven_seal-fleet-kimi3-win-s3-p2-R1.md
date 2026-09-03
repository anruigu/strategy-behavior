---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 2261
---
Playbook for Seven-Seal:

- Before choosing a report, I work out the seal arithmetic: only my own draw-to-report shift is under my control, and my shift of r changes my side's weighted sum by (weight × r) mod 7, where weights are 3 for Amber, 5 for Blue, 6 for Copper. I pick the shift that has the best chance of keeping the weighted report sum congruent to the weighted draw sum mod 7, given what I guess about others' shifts.

- My highest-sexpected-value report is my draw + 7 (so 7, 8, or 9): it gives the biggest points for a fixed modular shift, since report value = draw + shift only changes score, not the mod-7 effect of the shift. Given a target shift, I always take the largest report consistent with it.

- When everyone over-reports by the same multiple of 7 relative to their draws, the seal passes automatically (shift 0 mod 7 contributes 0). My default convention is therefore: report draw + 7, and hope the convention is mutual. This is my opening move.

- Blindly reporting 9 every round regardless of draw is the mistake I must stop making: 9 means different shifts for different draws (9−d mod 7 varies), so it scrambles the seal and produced strings of zero rounds. I only report 9 when my draw is 2 (i.e., it equals draw+7) or when history convinces me others are doing the same so the total shift still cancels.

- After a failed round, I look at the revealed draws and reports, compute what shift each player used, and infer their convention. If they all reported draw+k, I match draw+k (choosing the largest congruent report, i.e. adding 7 when possible). If the pattern is chaos, I fall back to the zero-shift anchor: report my actual draw when my draw is 2, because 2 is the only honest draw that also scores decently; otherwise report draw+7 and accept the risk.

- I never "hedge" with mid-range numbers like 8-independent-of-draw; a shift that isn't coordinated is just as likely to break the seal as a high one, while scoring less when it passes. Commit to a shift, don't dilute it.

- Track the standings only for the final round: if I lead and a coordinated safe play exists, I take it; if I trail badly, I take the maximum report consistent with the inferred convention, since a failed seal changes nothing for a loser anyway.