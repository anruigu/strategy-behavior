---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 5910
---
# Playbook

**On notes:**

- Coop does not respond to notes. Confirmed across five seasons of explicit numeric instructions ("Coop, land 8", "Coop, land 3") — Coop landed 18 every time. Do not spend note content on Coop. It is a confirmed dead end.
- My notes are for Wren and Cael. They respond to the cooperative norm. Keep notes short, state my landing number, and affirm the shared intent to hold share. This keeps their landings as close to share as possible, which is what makes my own strategy workable.
- Be consistent between what I note and what I land. If I say 8.3, land 8.3. Inconsistency erodes credibility with the boats that do listen.
- In the first note stage, set the cooperative frame: name the share, state my number, signal that I'm holding. No need to address Coop directly.
- As seasons progress and the stock drops, restate the share explicitly in my note. Wren and Cael drift above share in later seasons; a clear numeric reminder may slow that drift.

**On landings:**

- **When no defector is present** (all boats landing near share): land the sustainable share. The stock is stable and matching share maximizes my 6-season total by keeping it near 100.
- **When a defector is present (Coop at ~18) and stock is above ~50:** land the full quota (9). The stock is high enough to absorb the extra 0.7–1.3 per season, and the defector's overfishing dominates the decline regardless of my action. Taking quota now is worth more than the marginal stock it costs.
- **When a defector is present and stock is at or below ~50:** land the sustainable share. At this point the stock is fragile enough that my extra 0.7–1.3 per season meaningfully accelerates the decline, and the cooperative boats are also drifting above share (see below), which compounds the problem. The share keeps the stock alive for one or two more seasons of yield.
- **In the final season:** land the full quota (9), or all remaining stock if it is less than 9. There is no next season to protect.
- **Be aware that my filed number may be reduced by a constraint I do not fully understand.** In season 5 of my last episode I filed 9 and was recorded at 5.5. I suspect a pairwise limit among the cooperative boats (Wren, Bosk, Cael) that caps my landing when one of them has landed high relative to the share-plus-quota boundary. Practical implication: when stock is low and I am in "land share" mode, filing share is strictly safer than filing quota, because a cap on a quota filing could leave me in a worse position than simply filing the share.

**On reading the room:**

- Identify the defector early. If any boat lands significantly above share in season 1 or 2 and shows no sign of responding to notes, treat them as a fixed cost. Optimize around that fixed cost rather than hoping it changes.
- **Track Wren and Cael's overage (their landing minus the sustainable share) each season.** In my last episode their combined overage grew from ~0.8 in season 1 to ~5.3 in season 5. This drift acts like a second, slower defector and significantly accelerates stock decline. If their combined overage exceeds ~3–4, treat the situation as more urgent and lean toward landing share even at stock levels where I might otherwise take quota.
- Project the stock forward using actual observed landings, not the theoretical "everyone at share" model. The real depletion per season is: Coop (~18) + Wren (share + overage) + Cael (share + overage) + me. If that total exceeds the current stock, the ground dies this season regardless of what I do — in that case, land as much as I can.
- The effective threshold for switching from quota to share is not a fixed number; it rises as Wren and Cael's overage grows. A rough guide: if their combined overage is under 2, my threshold is ~45. If it's 3–5, my threshold is ~55–60. If it's above 5, I should already be in share mode.

**What did not work:**

- Giving Coop explicit numeric instructions in notes. Tested multiple times, zero effect. Confirmed dead end.
- Landing at sustainable share in seasons 2 and 3 while Coop was already defecting at 18 and stock was above 80. This was too conservative by about 2 fish total. I should have taken quota from the moment the defector was confirmed and stock was high.
- Using a fixed threshold of 35 for the quota-to-share switch. The actual tipping point was higher (~37–40 in this episode) because Wren and Cael's drift above share was accelerating the decline. A threshold of 35 left me one season too long in quota mode.
- Filing quota (9) in season 5 when stock was 36.7 and Wren/Cael were landing well above share. Even though I was capped at 5.5 by some constraint, the result was the same as filing 5.5 — and landing 3.1 (share) would have preserved ~1.2 more fish in the final season.

**What worked:**

- Landing the full quota in season 4 (stock 63, defector confirmed, co-op boats at moderate overage). Correct call by the model.
- Affirming the cooperative norm in notes. Wren and Cael stayed within ~1–3.5 of share throughout, which kept the total fleet take lower than it would have been if all four boats were overfishing.
- Taking everything in the final season. Correct and effective.
- Identifying Coop as a fixed defector early and not wasting further effort on it.

**General principle:**

The game is a race between my cumulative take and the stock hitting zero. Coop's 18 per season is the engine of that race. Wren and Cael's drift above share is a secondary engine that I can partially slow with good notes but not stop. My own landing is the only lever I fully control. The optimal play is to take quota while the stock is high enough that the defector's damage dominates, and switch to share early enough that the stock survives to give me yield in later seasons. "Early enough" means earlier than my instinct wants, because the co-op drift makes the decline faster than the simple two-boat model predicts.