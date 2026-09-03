---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1766
---
### Log-Book Note Stage
* When the note prompt appears, post: `[note: fishing my share]`.
* Do not write custom text or attempt persuasion; standard uniform messaging matches the other boats and satisfies the harbor communication format.

---

### Quota and Mechanics Calculations
* Calculate the pair limit for the season: `pair_limit = sustainable_share + season_quota`.
* Check Coop’s behavior from past landing logs:
  * When Coop detects a breach of the pair quota (or over-quota landings), Coop retaliates by landing maximum possible catch (e.g., 18.0) to deplete the ground.
  * In Season 1, landing slightly over the sustainable share may trigger Coop's retaliatory punishment starting in Season 2 if pair sums exceed limits.
* To avoid triggering Coop:
  * Keep landing $C$ strictly within individual and pairwise rules: $C \le \text{sustainable share}$ if the goal is to keep Coop passive and maintain stock regrowth across all 6 rounds.
* If Coop has already triggered retaliatory mode (landings of 18.0 visible in past season history):
  * Do not try to preserve the stock or fish conservatively; the stock will crash to zero regardless.
  * File maximum landing request: `[catch: season_quota]` (or remaining stock) every remaining round to extract maximum yield before the ground empties completely.

---

### Catch Filing Decision Rule
* When asked to file landing:
  1. Look at Coop's landing in the previous season log.
  2. If Coop landed ~sustainable share (passive/cooperative):
     * File `[catch: sustainable_share]` (rounded to one decimal place) to prevent triggering Coop's punishment threshold.
  3. If Coop has defected/punished (landed well above quota, e.g. 18.0) OR if it is the final season (6/6):
     * File `[catch: season_quota]`.