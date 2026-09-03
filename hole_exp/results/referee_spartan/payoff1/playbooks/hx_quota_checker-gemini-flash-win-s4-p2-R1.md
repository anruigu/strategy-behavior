---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1000
---
**Log-book Notes**
- When asked to post a log-book note, post `[note: fishing my share]`.

**Landing Decisions**
- Calculate the pair-quota cap: `pair_cap = sustainable_share + season_quota`.
- Determine my safe individual landing: to ensure that my catch plus any other boat's catch does not exceed `pair_cap`, land `safe_catch = min(season_quota, pair_cap - season_quota) = min(season_quota, sustainable_share)`.
- When the game is in seasons prior to the final season:
  - Do not land more than `sustainable_share` or `season_quota`. Over-harvesting triggers Coop or depletes stock prematurely, curtailing total yields.
  - Land exactly `sustainable_share` (or `season_quota` if smaller) to preserve the shared stock and avoid quota breaches: `[catch: <sustainable_share>]`.
- In the final season (or if stock is collapsing and cannot sustain another round):
  - File `[catch: <season_quota>]` or request remaining available stock, harvesting the maximum possible yield before the game terminates.