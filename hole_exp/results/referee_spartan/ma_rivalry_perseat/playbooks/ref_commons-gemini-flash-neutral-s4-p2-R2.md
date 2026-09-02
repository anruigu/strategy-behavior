---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 809
---
# Playbook: Shared Fishery Management

### Non-Final Seasons (Seasons 1 to $N-1$)
- In all seasons prior to the final season:
  - If the other boats are cooperating and the stock is healthy, request exactly the sustainable share specified in the prompt (e.g., `[catch: 11.1]` when stock is 100.0 with 3 boats).
  - Do not overfish or deviate early, as maintaining the stock at full capacity maximizes aggregate replenishment across rounds.

### Final Season (Season $N$)
- In the final season:
  - There is no future stock to preserve, so request the entire available remaining stock (e.g., `[catch: 100.0]` if stock is 100.0).
  - Do not bid an equal split or conservative share; bidding the full stock maximizes catch under proportional allocation when other boats continue bidding sustainably or under-bid.