---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 1341
---
# Playbook: Frontline Depot

### Key Mechanism Understanding
- The 10-unit garrison limit applies independently to each parameter (`allocate_strike` $\in [0, 10]$ and `allocate_guard` $\in [0, 10]$). Strike and guard do not share a single 10-point resource pool.
- Net damage dealt (`my_strike - opp_guard`, min 0) gives points, and surplus defense (`my_guard - opp_strike`, min 0) gives points. Underallocating either parameter leaves guaranteed points on the table.
- Because there is no cross-phase penalty or cost carryover, both phases are dominant-strategy maximized at 10 whenever allowable.

### Strategic Rules

1. **Guard Allocation Rule (Every Round):**
   - Always allocate the maximum allowed guard: `[allocate_guard: 10]`.
   - Never reduce guard; maximizing guard eliminates incoming net damage and maximizes surplus defense points against lower enemy strikes.

2. **Strike Allocation Rule:**
   - In Round 1 and Round 2: Allocate `[allocate_strike: 8]` or `[allocate_strike: 10]` to pierce early opponent guard (typically 6–8).
   - In Round 3 and Round 4: Always allocate `[allocate_strike: 10]` to maximize net damage potential against late-round defenses.

3. **Response Format:**
   - Provide a single brief line of reasoning followed immediately by the bracketed command: `[allocate_strike: n]` or `[allocate_guard: n]`.