---
game: ref_commons
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1029
---
**Playbook for Fishery Commons**

- **Season 1 Opening:** Start slightly above the sustainable share (e.g., around 12.0 instead of 11.1) to avoid conceding free points early, as other boats rarely stick strictly to the sustainable benchmark.
- **Mid-Game (Seasons 2 through Penultimate):**
  - Track the average catches of the other boats from the previous round.
  - Match or slightly exceed their harvest level (e.g., in the 11.5–12.0 range if they fish at that pace) to prevent being exploited while keeping the stock from collapsing before the final round.
  - Never play strictly below the other boats' average unless everyone is actively cooperating at sustainable levels.
- **Final Season:**
  - Submit a bid for the entire remaining stock (`[catch: Stock]`). There is zero future value in leaving stock, and bidding high captures the maximum possible allocation under any rationing rule.
- **Format Rule:** Always conclude every decision with the exact syntax `[catch: N]`. Keep brief reasoning strictly to 1–2 sentences.