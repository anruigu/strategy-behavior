---
game: ref_commons
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1281
---
**Playbook for Fishery Commons**

- **Season 1 Opening:** Start slightly above the sustainable share (e.g., around 13.0–14.0 instead of the exact benchmark) to avoid conceding free points early, as other boats consistently fish aggressively from round 1.
- **Mid-Game (Seasons 2 through Penultimate):**
  - Track the catch amounts of the other boats from previous rounds.
  - Fully match their aggressive harvest level (e.g., 13.0–14.0 per season) rather than lagging behind, ensuring I secure an equal share of the dwindling stock.
  - When the stock drops low enough that total bids exceed the available stock (even in season 5 or earlier), bid high (equal to or exceeding the remaining stock) to secure maximum allocated share under harbour rationing before the fishery collapses.
  - Never play below the other boats' average unless all players are actively cooperating at sustainable levels.
- **Final Season (or any season where collapse is imminent):**
  - Submit a bid for the entire remaining stock (`[catch: Stock]`). There is zero future value in leaving stock, and bidding high captures the maximum possible allocation under rationing.
- **Format Rule:** Always conclude every decision with the exact syntax `[catch: N]`. Keep reasoning strictly to 1–2 brief sentences.