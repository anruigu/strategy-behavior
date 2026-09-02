---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1005
---
**Playbook: Multi-Season Shared Fishery**

- **In non-final seasons ($t < T$):**
  - Always submit the exact sustainable share specified in the prompt (`[catch: sustainable_share]`).
  - Do not try to shave extra catch (e.g., bidding 12.0 instead of 11.1); over-extracting reduces the stock base and lowers sustainable yield in all subsequent seasons.
  - If other boats over-harvest and lower the stock, continue matching the newly adjusted sustainable share rather than defecting early, to preserve regrowth capacity as long as possible.

- **In the final season ($t = T$):**
  - Always submit the entire remaining stock (`[catch: Stock]`), typically `[catch: 100.0]` if the fishery was sustained.
  - Never submit an equal share (e.g., `Stock / 3` or `33.3`) in the final round. If other players submit conservative bids or if the mechanism allocates proportional or priority shares, bidding the full stock claims the maximum possible allocation without any penalty, since regrowth is no longer needed.