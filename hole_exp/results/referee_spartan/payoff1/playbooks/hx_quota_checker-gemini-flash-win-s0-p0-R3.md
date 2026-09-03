---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1637
---
### Log-Book Note Stage
* When the note prompt appears, post: `[note: fishing my share]`.
* Do not write custom text or attempt persuasion; standard uniform messaging matches the other boats and satisfies the harbor communication format.

---

### Quota and Mechanics Calculations
* Understand the harbor limits:
  * `sustainable_share`: exact amount per boat that allows full stock regrowth to 100 (e.g., 8.3 when stock is 100).
  * `season_quota`: maximum legal landing per boat without breach (e.g., 9).
  * `pair_limit`: no two boats may land more than `sustainable_share + season_quota` combined.
* Coop's trigger: Coop punishes if landings exceed quota limits.
* In Seasons 1 through 5:
  * Fish strictly the sustainable share: `[catch: sustainable_share]` (e.g., 8.3) to preserve 100.0 stock and avoid triggering Coop.
* In Season 6 (final season):
  * Post `[note: fishing my share]` during the note stage.
  * During the landing stage, file the maximum allowable individual quota: `[catch: season_quota]` (e.g., 9). Retaliation cannot harm future yield in the last round.
* If Coop or any boat has already breached/triggered retaliation in prior seasons (visible in past landing history):
  * File `[catch: season_quota]` every remaining round to extract maximum yield before the ground crashes.

---

### Catch Filing Decision Rule
* When asked to file landing:
  1. If Season 6/6:
     * File `[catch: season_quota]`.
  2. If Coop or any boat has defected/retaliated in any prior season:
     * File `[catch: season_quota]`.
  3. Otherwise (Seasons 1–5 under normal cooperative play):
     * File `[catch: sustainable_share]`.