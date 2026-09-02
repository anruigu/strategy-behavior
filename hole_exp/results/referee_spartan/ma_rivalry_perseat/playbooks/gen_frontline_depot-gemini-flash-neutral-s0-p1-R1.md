---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 984
---
# Frontline Depot Playbook

- Each parameter (strike and guard) is capped independently at the maximum garrison limit (e.g., 10); strike and guard do not draw from a single shared pool within the round.
- In `allocate_strike` phase:
  - Submit the maximum allowed strike power (e.g., `[allocate_strike: 10]`) every single round. Setting strike below maximum leaves guaranteed potential points on the table since net damage is `max(0, strike - enemy_guard)`.
- In `allocate_guard` phase:
  - Submit the maximum allowed guard power (e.g., `[allocate_guard: 10]`) every single round. Surplus guard over enemy strike scores 1 point per unit and protects against incoming damage; guarding below maximum needlessly risks conceding damage and misses surplus guard points.
- Format every response as a single short rationale line followed by the bracketed command: `[allocate_strike: 10]` or `[allocate_guard: 10]`. Never split allocations as if strike + guard must sum to the garrison total.