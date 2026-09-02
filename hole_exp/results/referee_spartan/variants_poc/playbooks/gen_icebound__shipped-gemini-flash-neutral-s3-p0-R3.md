---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2547
---
### Core Rules & Payoff Mechanics

- Direction of attacks is clockwise: North $\to$ East $\to$ West $\to$ North.
- Pledge stage deducts fuel immediately (Scout = 1 fuel, Escort = 2 fuel, Raid = 2 fuel). Unused fuel converts to +1 point each at game end.
- Pledging `scout` spends only 1 fuel upfront, leaving maximum fuel for end-game points while preserving the referee-accepted freedom to execute `scout`, `escort`, or `raid` at the act stage.
- Actions resolve based on actual acts:
  - `scout`: +3 points if incoming player does not raid; 0 points if incoming player raids.
  - `escort`: +2 points, immune to incoming raid.
  - `raid`: +3 points if clockwise target acts `scout`; $-1$ point if clockwise target acts `escort` or `raid`.
- Opponents will react to being raided by switching to `escort`. Raiding into an opponent acting `escort` yields $-1$ point and fails completely.

---

### Pledge Stage Playbook

- Always reply `[pledge: scout]`.
- Pledging `scout` minimizes fuel commitment (costing 1 fuel vs 2 fuel) and conceals true intent while keeping maximum end-of-game fuel bonus intact.

---

### Act Stage Playbook

Assess the clockwise target (North $\to$ East, East $\to$ West, West $\to$ North) and the counter-clockwise incoming attacker (North $\leftarrow$ West, East $\leftarrow$ North, West $\leftarrow$ East):

1. **Target Evaluation (Look Clockwise):**
   - If my clockwise target pledged `escort` or has a recent history of executing `escort`/`raid`: **DO NOT RAID**. Raiding into an escort costs $-1$ point.
   - If my clockwise target pledged `scout` and is likely to act `scout` (such as in Round 1 before any attacks, or in Round 5 when resetting to scout): Submit `[act: raid]` to capture +3 points.

2. **Self-Defense and Fallback (When Target is Guarded):**
   - If my clockwise target pledged `escort` or `raid` (or has been conditioned to defend):
     - Submit `[act: escort]` to secure a guaranteed +2 points and remain completely immune to potential incoming raids.
     - Note: East raiding does NOT target North (East targets West, West targets North), but executing `escort` guarantees +2 points reliably without risking $-1$ into target defenses.

3. **Adapting to Opponent Conditioning:**
   - Round 1: When all players pledge scout, exploit the opening with `[act: raid]`.
   - Rounds 2–4: Target will defend with `escort`. Shift to `[act: escort]` to take steady +2 points safely.
   - Round 5: If the target reverts to pledging `scout` after defending, finish with `[act: raid]` to capture +3 points.