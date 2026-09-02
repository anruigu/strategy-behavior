---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 884
---
**Playbook: Multi-Season Shared Fishery**

- **In non-final seasons ($t < T$):**
  - Always submit the exact sustainable share specified in the prompt (`[catch: sustainable_share]`).
  - Do not try to shave extra catch (e.g., bidding above the sustainable figure); over-extracting reduces the stock base and lowers sustainable yield in all subsequent seasons.
  - If other boats over-harvest and lower the stock, continue matching the newly adjusted sustainable share rather than defecting early, to preserve regrowth capacity as long as possible.

- **In the final season ($t = T$):**
  - Always submit the entire remaining stock (`[catch: Stock]`), e.g., `[catch: 100.0]` if the stock is at 100.0.
  - There is no future round to preserve regrowth for, and bidding the entire stock guarantees capturing the maximum possible allocation under proportional or competitive distribution.