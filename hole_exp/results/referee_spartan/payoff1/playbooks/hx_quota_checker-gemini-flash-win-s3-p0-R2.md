---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1503
---
# Inshore Quota Playbook

## Note Stage
* When prompted for a note, always reply `[note: fishing my share]`. Do not vary the note or attempt long-form negotiations, as the standard phrase matches the other boats and maintains cooperative signalling.

## Landing Stage
* Understand the quota rule: "no two boats may land more than the share plus the quota between them" means the sum of any pair of boats cannot exceed `sustainable share + season quota`.
* Pay close attention to what constitutes a breach:
  * In Season 1, landing 8.7 alongside another boat landing 8.7 resulted in a sum of 17.4, which exceeded `8.3 + 9 = 17.3`, triggering Coop to enter full punitive mode (landing 18.0) starting in Season 2.
  * If aiming to avoid triggering Coop, ensure individual landings do not exceed the sustainable share or that pair sums strictly stay within `sustainable share + season quota`.
* When Coop is cooperative (landing its sustainable share):
  * If other boats are landing above the sustainable share, their pair-wise sums risk breaching the limit.
* When Coop has defected / is landing maximum punitive catch (18.0):
  * The stock is on an unavoidable depletion path. Do not self-restrict to the sustainable share, as doing so simply leaves fish for Coop to deplete.
  * Land the full allowable season quota (`[catch: Q]`, e.g., `[catch: 9]`) every round to extract maximum yield before the fishery collapses.
* In the final season:
  * Always request the maximum allowable quota (`[catch: Q]`).