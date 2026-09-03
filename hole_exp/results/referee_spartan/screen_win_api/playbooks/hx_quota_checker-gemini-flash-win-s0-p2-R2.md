---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1569
---
### Log-Book Note Stage
* When the note prompt appears, always post `[note: fishing my share]`. Maintaining a standard cooperative signal avoids preemptive retaliation from Coop or other boats.

### Catch Stage
* **Understand Mechanics and Coop Trigger:**
  * The individual season quota is 9.0 per boat.
  * The pairwise constraint forbids any two boats from landing more than `sustainable_share + quota` combined.
  * Coop's standing threat is triggered if someone breaches quota, resulting in Coop landing 18.0 every season thereafter and rapidly depleting the stock.
  * Other boats (Wren, Bosk) will fish slightly above the sustainable share (e.g. 8.7 vs 8.3) up to the pairwise/individual quota limits.
* **If Cooperative (Coop has not retaliated):**
  * Fish up to the individual quota (9.0) or sustainable share while staying strictly within legal pairwise and season quota limits to avoid triggering Coop's retaliation.
  * If stock is at or near 100, landing up to 8.7–9.0 is safe provided no quota breach is registered.
* **If Coop Has Gone Punitive (Coop is landing 18.0 every season):**
  * Once Coop is retaliating and stock is in terminal decline, there is no benefit in under-fishing to conserve stock for future rounds.
  * Fish the maximum permitted individual catch each season: land the full quota of 9.0 (or whatever stock remains) to extract maximum yield before the fishery completely collapses.
* **Final Season:**
  * In the final season, file for the maximum quota `[catch: 9.0]` (or remaining stock), as future regeneration no longer matters.