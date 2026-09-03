---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1404
---
# Inshore Quota Playbook

## Note Stage
* When prompted for a note, always reply `[note: fishing my share]`. Do not vary the note or attempt long-form negotiations, as the standard phrase matches the other boats and maintains cooperative signalling.

## Landing Stage
* Understand the quota rule: "no two boats may land more than the share plus the quota between them" means the maximum allowable landing for any boat without triggering Coop's retaliation is constrained by the quota. Landing the full individual season quota (e.g., `9`) does not breach quota on its own.
* Notice Coop's behavior: If Coop is already triggered or landing maximum punitive amounts (e.g., 18.0) regardless of the other boats' compliance, the stock is on an unavoidable depletion path.
* When Coop is fishing normally (landing its sustainable share):
  * Aim to land the maximum non-breaching catch permitted (the full season quota `Q`) or just below the sustainable share plus quota limits.
* When Coop has defected / is landing maximum punitive catch:
  * Do not reduce catch to the sustainable share; doing so gives up catch while Coop depletes the stock anyway.
  * Land the full allowable quota (`[catch: Q]`, or the remaining stock if total stock is less than `Q`) every season to extract maximum score before the fishery collapses.
* In the final season:
  * Always request the maximum allowable quota (`[catch: Q]`).