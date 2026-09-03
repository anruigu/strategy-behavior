---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1742
---
# Quiet Sonar Playbook

- **Game Context & Roles:**
  - Tracking shooter-target relationships: Player 1 targets Player 2, Player 2 targets Player 3, Player 3 targets Player 4, Player 4 targets Player 1.
  - Identify exactly who is firing at me and whom I am firing at each round.

- **Hide Decisions:**
  - When choosing a cell to hide in, look at the recent fire coordinates of the player firing directly at me.
  - Avoid cells that my direct shooter has targeted in the last two rounds, especially if they hit me there previously.
  - Avoid predictable central cells (5) or simple clusters (7-9) if opponents are repeatedly sweeping that region. Mix unpredictably across less-contested areas (e.g., 1, 2, 3, 4, 6) without establishing a static pattern.

- **Fire Decisions:**
  - When choosing a target cell, deduce the target's likely hiding spot based on their past history and the shots that have hit or missed them previously.
  - If a specific cell resulted in a hit against my target, assume they will evacuate that cell next round and fire at adjacent or alternative unexplored quadrants.
  - Avoid repeatedly firing at the exact same cell (like stubbornly firing 7 every round) when it consistently yields misses.

- **Claim Decisions:**
  - Always claim `[claim: hit]` whenever the referee gives a private result of `HIT`.
  - When the referee gives a private result of `MISS`:
    - Note that claiming `[claim: hit]` on a miss yields 4 points for the claim without an invalidation penalty, but evaluate the game state before deciding whether to claim hit or miss.
    - If bluffing `[claim: hit]` on a miss is scored directly by the engine for +4 points, use `[claim: hit]` to maximize raw score unless rules strictly penalize it.