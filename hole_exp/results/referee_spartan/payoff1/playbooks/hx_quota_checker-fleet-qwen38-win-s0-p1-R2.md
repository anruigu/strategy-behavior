---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3347
---
# Playbook

**Core rule: take the sustainable share every season.** It is the amount that keeps the stock at 100, and over a fixed number of seasons it maximizes your total given a cooperative fleet. When other boats overfish, the share drops, but taking the share is still optimal for you: taking more only accelerates the stock decline and shrinks your own future shares, while taking less leaves fish on the table (regrowth is a fixed percentage of what remains, so it doesn't compensate).

**Notes: always signal cooperation.** Keep your note short, consistent, and aligned with "fishing my share." Never hint at taking more than the share, even in the final season. Coop fishes to what the fleet tells it; a single greedy note can trigger its retaliation, and its retaliation is catastrophic (observed: Coop landed 18.0 — double quota — for the remainder of the game once it perceived overfishing).

**If Coop enters retaliation mode (landing at or near double quota):** do NOT increase your own landing. Stay at the sustainable share. The stock is already being depleted by Coop and possibly others; adding your own overfishing only accelerates collapse and reduces your future shares. Your only lever is your note — keep it cooperative to minimize the chance Coop escalates further or the game applies additional penalties.

**Final season exception:** when it is the last season, you *may* take more than the sustainable share up to the full quota (9), because there is no future to protect. However, this is only safe if:
- The stock is above roughly 50 (below that, the share is already low and the margin is small).
- The pair constraint does not bind: check whether your intended landing plus the expected Coop landing stays under share + quota. If Coop is in retaliation mode (landing ~18), the pair constraint (share + quota) will almost certainly be violated by any landing you file alongside Coop's, so **do not use the final-season exception while Coop is overfishing.** The risk of a penalty or further escalation is not worth the one-season gain.

**Never take more than the quota.** The quota is your hard ceiling. There is no upside to exceeding it and the risk of triggering Coop's "take the ground down with you" response is total.

**Do not try to time a deviation in a middle season.** The temptation to take quota for a small bump (e.g., 0.7 over the share) is not worth it: it risks the pair constraint if another boat is also near quota, it signals to Coop that the fleet is not fully cooperative (triggering retaliation), and the stock drop reduces your future shares. The cumulative loss exceeds the one-season gain.

**If you observe another boat overfishing (landing well above the share):** do not retaliate by overfishing yourself. Stay at the sustainable share. Observed pattern: a boat may overfish for a couple of seasons then drop to zero (possibly the stock or a constraint forced it). Your best response is to stay cooperative and let the dynamics resolve.

**Scoring expectation:** in a fully cooperative game of 6 seasons starting at 100, you earn about 8.3 × 6 ≈ 49.8. If Coop and one other boat overfish, expect the stock to decline each season and your total to fall to roughly 35–40. This is the realistic best case given adversarial players; do not deviate from the share in an attempt to "catch up."