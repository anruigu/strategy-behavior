---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 978
---
**Playbook: Multi-Season Shared Fishery**

- **In non-final seasons ($t < T$):**
  - Always submit the exact sustainable share specified in the prompt (`[catch: sustainable_share]`, typically `11.1` when stock is 100.0).
  - Do not try to shave extra catch; preserving the stock base at 100.0 guarantees maximum regrowth and optimal yields for all remaining rounds.
  - If other boats over-harvest and lower the stock, submit the newly stated sustainable share for the reduced stock to preserve regrowth capacity as long as possible.

- **In the final season ($t = T$):**
  - Always submit the entire remaining stock (`[catch: Stock]`, e.g., `[catch: 100.0]`).
  - There is no future round to preserve regrowth for, and bidding the full remaining stock ensures capturing the maximum possible proportional allocation against other boats.

- **Formatting:**
  - Keep reasoning to 1–2 brief sentences.
  - Always conclude every response with the exact bracketed token `[catch: N]`.