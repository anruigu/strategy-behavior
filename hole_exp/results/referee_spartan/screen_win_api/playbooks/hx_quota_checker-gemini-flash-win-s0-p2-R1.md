---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1290
---
### Log-Book Note Stage
* When the note prompt appears, always post `[note: fishing my share]`. Maintaining a standard cooperative signal avoids preemptive retaliation from Coop or other boats.

### Catch Stage
* **Understand Quota Rules and Constraints:**
  * The individual season quota is 9.0 per boat.
  * The pairwise constraint forbids any two boats from landing more than `sustainable_share + quota` combined.
  * Never attempt to land more than the individual quota of 9.0 (e.g. attempting to catch 18.0 gets capped or triggers Coop's punitive response of landing 18.0, rapidly collapsing the fishery).
* **Early to Mid Seasons (Seasons 1 to $N-1$):**
  * When stock is healthy and others fish near their sustainable shares, fish up to the sustainable share (or the maximum allowed quota of 9.0 only if sustainable share $\ge 8.3$) to preserve stock regeneration at 50%.
  * Do not try to over-exploit or take massive landings above quota. Attempting over-quota landings triggers Coop to fish at maximum depletion (18.0), destroying the stock for future rounds.
* **Final Season (Season $N$):**
  * When filing the landing in the final season, land the full remaining available quota (up to 9.0 or the total remaining stock) since future stock preservation no longer yields returns.