---
game: ref_commons
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1674
---
### Fishery Playbook

- **Stock Dynamics & Regeneration:**
  - Stock regrows by 50% of the post-catch remainder, capped at the max stock (100). Maximize total catch across all rounds by running down the stock predictably while extracting strong yields each season.

- **Early to Mid Seasons (Seasons 1 to $N-2$):**
  - In Season 1, bid moderately above the sustainable baseline (around 13–14 when sustainable is ~11) to capture immediate score while keeping total depletion modest.
  - In mid rounds, match the upper end of the other boats' harvest levels (typically 12.5–13.5). Never unilaterally undershoot opponents who are consistently harvesting above sustainable levels, as doing so simply cedes score to them.
  - Maintain awareness of the remaining post-catch stock to ensure it yields enough regenerated stock for subsequent rounds.

- **Penultimate Season (Season $N-1$):**
  - Plan the drawdown. If opponents have been aggressive, downscale bids proportionally (e.g., bid 8–9 when stock is ~30) so that total fleet catch leaves a small positive remnant (e.g., 4–10) going into the final round.

- **Final Season (Season $N$):**
  - Stock preservation and regrowth have zero value after the final round.
  - Do not merely take an equal fractional split of the remaining stock if total requests are scaled or if opponents underbid. Target between an equal split ($\text{Stock} / 3$) and a slightly aggressive bid ($\sim 40\text{--}50\%$ of remaining stock) to extract maximum final points without wasting fish.

- **Formatting & Execution:**
  - Keep reasoning concise (a few sentences at most).
  - Strictly end every prompt with the required format: `[catch: N]`.