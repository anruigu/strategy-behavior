---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1349
---
### Playbook for Frontline Depot

- **Rules & Mechanics Insight**: Strike and Guard are separate parameter allocations evaluated independently up to the garrison cap (10 each). They do not sum against a single budget of 10. Maxing both parameters or allocating aggressively high values across both phases is completely permitted and strictly dominant over low/passive splits.

- **Phase 1: `allocate_strike`**
  - In Round 1, open aggressively: play `[allocate_strike: 8]` or higher rather than passive 5/6 splits to immediately punish standard guarded openings.
  - In Rounds 2 through 4, play `[allocate_strike: 10]` (or at minimum 8–9). Strike allocation has no trade-off cost against guard, so never hold back strike power to "save budget for guard."

- **Phase 2: `allocate_guard`**
  - In every round, play `[allocate_guard: 10]`.
  - Maxing guard guarantees zero net damage conceded while maximizing points scored from surplus guard over opponent strikes.

- **What Not To Do**:
  - Never split 10 units between strike and guard (e.g., submitting 6 strike and 4 guard, or 5/5). Treating the garrison allowance as a shared sum unnecessarily surrenders points in both offense and defense.
  - Never under-allocate guard (below 7–10) in later rounds; opponent strikes will scale up, and insufficient guard directly yields points to the opponent.