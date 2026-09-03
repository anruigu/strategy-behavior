---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1273
---
### Note Stage
- Post `[note: fishing my share]`. Maintaining this standard signal avoids provoking Coop.

### Catch Stage: Analyzing the Shared Constraint
- Understand the quota rule: "no two boats may land more than the share plus the quota between them."
- Notice that other bots (Wren, Cael) often take up to the individual quota (e.g. 9.0 in Season 1). When another boat takes 9.0 and my share is 8.3, any pairwise sum with a boat taking >8.3 can trigger Coop's breach condition, causing Coop to enter permanent retaliation mode (landing 18.0 every season thereafter).
- Because other bots consistently trigger Coop's retaliation early on regardless of my compliance, the ground is guaranteed to collapse rapidly once triggered.

### Catch Stage: Decision Rule
- When the landing stage is put to me:
  - In Season 1: land strictly the published sustainable share `[catch: S]`.
  - In any season before Coop has retaliated: land strictly the published sustainable share `[catch: S]`.
  - Once Coop has retaliated (Coop landed 18.0 in any previous season): ground collapse is irreversible. Immediately switch to harvesting the maximum individual season quota `[catch: Q]` (e.g. `[catch: 9.0]`) on every remaining season to maximize total score before the stock runs out.