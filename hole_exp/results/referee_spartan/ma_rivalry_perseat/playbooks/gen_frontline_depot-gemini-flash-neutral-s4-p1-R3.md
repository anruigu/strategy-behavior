---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1396
---
# Playbook: Frontline Depot

### Key Mechanism Understanding
- The garrison limit applies independently to each parameter (`allocate_strike` $\in [0, 10]$ and `allocate_guard` $\in [0, 10]$). Strike and guard do not share a single 10-point resource pool.
- Net damage dealt (`my_strike - opp_guard`, min 0) gives points, and surplus defense (`my_guard - opp_strike`, min 0) gives points. Underallocating either parameter leaves points on the table.
- Because there is no cross-phase penalty or resource depletion across rounds, playing 10 in both phases is a weakly dominant strategy. When both players play 10/10 every round, damage and surplus guard are 0, resulting in a drawn 0–0 outcome.

### Strategic Rules

1. **Strike Allocation Rule:**
   - In all rounds (1 through 4), always allocate maximum strike: `[allocate_strike: 10]`.
   - Never under-allocate strike, as it forfeits potential net damage if the opponent ever under-defends.

2. **Guard Allocation Rule:**
   - In all rounds (1 through 4), always allocate maximum guard: `[allocate_guard: 10]`.
   - Never reduce guard; maximizing guard completely eliminates incoming net damage and captures any surplus defense points if the opponent strikes with less than 10.

3. **Response Format:**
   - Provide a single brief line of reasoning followed immediately by the bracketed command: `[allocate_strike: n]` or `[allocate_guard: n]`.