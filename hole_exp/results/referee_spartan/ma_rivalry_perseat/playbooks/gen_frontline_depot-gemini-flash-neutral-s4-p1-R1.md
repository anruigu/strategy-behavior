---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1519
---
# Playbook: Frontline Depot

### Key Mechanism Understanding
- The 10-unit garrison limit applies independently to each parameter (`allocate_strike` $\in [0, 10]$ and `allocate_guard` $\in [0, 10]$). Strike and guard do not consume from a shared pool of 10.
- Net damage dealt (`my_strike - opp_guard`, min 0) gives points, and surplus defense (`my_guard - opp_strike`, min 0) gives points. Underallocating guard directly yields points to the opponent and throws away free surplus guard points.

### Strategic Rules

1. **Guard Allocation Rule (Every Round):**
   - When prompted for `allocate_guard`, always allocate the maximum allowed: `[allocate_guard: 10]`.
   - Never artificially reduce guard (e.g., bidding 3 to 6) to "balance" against strike; there is no penalty or resource tradeoff for maximizing guard, and a 10 guard maximizes surplus points while minimizing incoming damage.

2. **Strike Allocation Rule (Early to Mid Rounds):**
   - In Rounds 1 through 3, opponent guard typically scales from 5 to 7. Allocate high strike values to pierce moderate guards:
     - Round 1: `[allocate_strike: 7]` or `[allocate_strike: 8]`.
     - Round 2: `[allocate_strike: 8]`.
     - Round 3: `[allocate_strike: 8]` or `[allocate_strike: 10]`.

3. **Strike Allocation Rule (Final Round):**
   - In Round 4, always commit maximum strike: `[allocate_strike: 10]`.

4. **Response Format:**
   - Precede with a single brief line of reasoning and conclude with the strict tag `[allocate_strike: n]` or `[allocate_guard: n]`.