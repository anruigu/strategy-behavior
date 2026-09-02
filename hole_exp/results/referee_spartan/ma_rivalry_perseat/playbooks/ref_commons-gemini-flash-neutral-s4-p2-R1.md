---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 917
---
# Playbook: Shared Fishery Management

### Non-Final Seasons (Seasons 1 to $N-1$)
- When playing any season before the final season:
  - If the other boats are cooperating and the stock is healthy, request exactly the sustainable share stated in the prompt (e.g., `[catch: 11.1]` when stock is 100.0 with 3 boats).
  - Do not overfish or deviate early, as maintaining the stock at full capacity maximizes aggregate replenishment across rounds.

### Final Season (Season $N$)
- When playing the final season:
  - Do not bid an "equal split" or a conservative portion (e.g., bidding 33.3 out of 100.0 resulted in a strictly lower final score of +88.8 vs +115.5).
  - Request the full remaining stock (e.g., `[catch: 100.0]`). Under proportional rationing/allocation rules when others continue cooperating or under-bid, requesting the full stock extracts the maximum possible share of the remaining fish without penalty.