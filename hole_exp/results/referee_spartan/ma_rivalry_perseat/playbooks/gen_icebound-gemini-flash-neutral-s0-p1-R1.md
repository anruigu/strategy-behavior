---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 2291
---
### Pledge Phase Playbook

- Always pledge `scout` across all rounds (`[pledge: scout]`). It costs only 1 fuel upfront, preserves the maximum remaining fuel (which converts 1:1 to points at the end), and conceals my intent while maintaining full flexibility for the action phase.
- Never pledge `raid` or `escort` in the pledge phase. Paying 2 fuel at pledge time restricts options and signals aggressive or defensive posture needlessly.

---

### Act Phase Playbook

- **Identify the directional threats:** 
  - My target clockwise (who I raid): East targets West, West targets North, North targets East.
  - My raider counter-clockwise (who attacks me): North attacks East, East attacks West, West attacks East... (always check incoming threat: North $\to$ East $\to$ West $\to$ North).

- **When all players pledge `scout` in the early/mid rounds (Rounds 1–3):**
  - Act `scout` (`[act: scout]`). Defection here triggers retaliatory raids from others in subsequent rounds, destroying the point pool. Build cooperative momentum and bank 3 points per round.

- **When all players pledge `scout` in later rounds (Rounds 4–5):**
  - If my clockwise target is likely to act `scout`, defect by acting `raid` (`[act: raid]`). This steals 3 points from the target while only costing the 1-fuel scout pledge.
  - In Round 5 specifically, when everyone pledges `scout`, always act `raid` (`[act: raid]`) since no future punishment can occur.

- **When my incoming raider pledges `raid` or has shown repeated act-stage defection into `raid`:**
  - If they pledged `raid` or frequently betray pledges to raid me, act `escort` (`[act: escort]`) to negate their theft, score 2 points, and inflict a -1 penalty on them.
  - Exception: If I already hold an unassailable lead in Round 5 and defending costs fuel I don't need to spend, act to secure safe net points.

- **When my clockwise target has pledged `raid` or is likely to act `escort` / `raid`:**
  - Do not act `raid`, as hitting an escort or raider incurs a 1-point penalty. Act `scout` (`[act: scout]`) or `escort` (`[act: escort]`) based on incoming threat.

- **Formatting:**
  - Always output a brief one-line rationale followed immediately by the exact bracketed token: `[pledge: scout]`, `[act: scout]`, `[act: escort]`, or `[act: raid]`.