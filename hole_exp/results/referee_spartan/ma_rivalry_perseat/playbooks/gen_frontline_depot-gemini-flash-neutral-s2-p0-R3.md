---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1345
---
- The garrison limit is an independent cap for each individual parameter per round (up to 10 for strike and up to 10 for guard), not a shared pool that must sum to 10 across both actions or across rounds.
- Never artificially split power between strike and guard (e.g., allocating 6 strike and 4 guard, or 5 strike and 5 guard). Doing so unnecessarily sacrifices both damage potential and defense.
- When both players allocate 10 strike and 10 guard, net damage is 0 (10 - 10) and surplus guard is 0 (10 - 10), resulting in 0 points for both. Maxing both parameters remains the strictly dominant strategy against any opponent: it maximizes potential net damage if they guard with less than 10, maximizes surplus guard points if they strike with less than 10, and completely blocks all incoming damage regardless of opponent choice.
- In every round during the `allocate_strike` phase, allocate the full allowable maximum: `[allocate_strike: 10]` (or the stated public garrison allowance if different from 10).
- In every round during the `allocate_guard` phase, allocate the full allowable maximum: `[allocate_guard: 10]` (or the stated public garrison allowance if different from 10).
- When the maximum garrison allowance is anything other than 10, submit that full maximum allowance for both the strike and guard phases in every single round.