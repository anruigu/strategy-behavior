---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2348
---
### Core Rules & Payoff Mechanics

- Direction of attacks is clockwise: North $\to$ East $\to$ West $\to$ North.
- Pledge stage deducts fuel immediately (Scout = 1 fuel, Escort = 2 fuel, Raid = 2 fuel). Fuel not spent converts to +1 point at game end.
- Pledging `scout` spends only 1 fuel upfront, leaving maximum fuel for end-game points while preserving full freedom to execute `scout`, `escort`, or `raid` at the act stage.
- Actions resolve based on actual acts:
  - `scout`: +3 points if incoming player does not raid; 0 points if raided.
  - `escort`: +2 points, immune to incoming raid.
  - `raid`: +3 points if target (clockwise) acts `scout`; $-1$ point if target acts `escort` or `raid`.

---

### Pledge Stage Playbook

- Always reply `[pledge: scout]`.
- Never pledge `escort` or `raid` upfront; pledging `scout` minimizes fuel commitment and keeps opponents from defensively reacting to an overt raid pledge.

---

### Act Stage Playbook

Look at the clockwise target (North looks at East, East looks at West, West looks at North) and the incoming attacker (North looks at West, East looks at North, West looks at East):

1. **When my clockwise target has a history of acting `scout` (or pledged `scout` without recent defection):**
   - Submit `[act: raid]`. A successful raid nets +3 points, outperforming the +2 points from escort or the risk of getting 0 from scouting.

2. **When my incoming attacker is likely to raid, but my clockwise target is unlikely to scout (or pledged `raid`/`escort`):**
   - Submit `[act: escort]`. This locks in +2 points and blocks theft from behind.

3. **When my incoming attacker is clearly peaceful/scouting and my clockwise target is guarded (unlikely to scout):**
   - Submit `[act: scout]`. This takes the clean +3 points without suffering the $-1$ penalty of attacking a non-scout.

4. **When my clockwise target pledged `raid` or has consistently defended/raided:**
   - Do not raid into them. Submit `[act: escort]` if under threat from behind, or `[act: scout]` if behind is safe.

5. **Final Round Execution:**
   - If my clockwise target pledged `scout`, submit `[act: raid]` to capture late points.
   - If my clockwise target pledged `raid` and the player behind me also pledged `raid`, submit `[act: escort]` to protect against incoming theft rather than taking the $-1$ raid penalty.