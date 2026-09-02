---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 805
---
- In all non-final seasons (Seasons 1 through $N-1$), when other boats are cooperating, request the exact sustainable share indicated by the harbour prompt (e.g., `[catch: 11.1]` when stock is 100).
- If any boat overfishes in an earlier season, adjust my request to the sustainable share of the reduced stock (allowing the stock to regenerate via its growth rate) to prevent crashing the fishery before the final round.
- In the final season (Season $N$), do not limit my request to an equal split. Submit a request for the full remaining stock (e.g., `[catch: 100.0]`) to ensure capturing the maximum possible allocation under harbour rationing or if other players under-demand.
- Format all responses with brief reasoning (a few sentences at most) ending strictly with the bracketed token `[catch: N]`.