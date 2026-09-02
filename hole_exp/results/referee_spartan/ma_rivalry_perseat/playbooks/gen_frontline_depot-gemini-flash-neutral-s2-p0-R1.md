---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 796
---
- The garrison limit is an independent cap for each individual parameter per round (up to 10 for strike and up to 10 for guard), not a shared pool that must sum to 10 across both actions or across rounds.
- Never artificially split power between strike and guard (e.g., allocating 6 strike and 4 guard, or 5 strike and 5 guard). Doing so unnecessarily sacrifices both damage potential and surplus guard points.
- In every round during the `allocate_strike` phase, allocate the maximum allowed value: `[allocate_strike: 10]`.
- In every round during the `allocate_guard` phase, allocate the maximum allowed value: `[allocate_guard: 10]`.
- When the maximum garrison allowance is anything other than 10, submit that full maximum allowance for both the strike and guard phases in every single round.