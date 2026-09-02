---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2039
---
### Pledge Phase Playbook

- Always pledge `scout` across all rounds (`[pledge: scout]`). It costs only 1 fuel upfront, preserves the maximum remaining fuel (which converts 1:1 to points after round 5), and conceals tactical intent while retaining complete flexibility for the action phase.
- Never pledge `raid` or `escort`. Paying 2 fuel at pledge time restricts options, permanently wastes end-game fuel points, and signals posture unnecessarily.

---

### Act Phase Playbook

- **Directional Targeting Rules:**
  - Clockwise raid trajectory: North $\to$ East $\to$ West $\to$ North.
  - Incoming attacker: East is attacked by North; West is attacked by East; North is attacked by West.
  - Outgoing target: East attacks West; West attacks North; North attacks East.

- **Act Decision Logic:**
  - **Rounds 1–2:** If all players pledge `scout` and have acted cooperatively, act `scout` (`[act: scout]`). This banks safe early points (+3 points per round) at minimal fuel cost.
  - **Rounds 3, 4, and 5 (Defection Window):**
    - When all players continue pledging `scout` and my clockwise target reliably acts `scout`, defect by acting `raid` (`[act: raid]`). This steals 3 points from the target while paying only 1 fuel (charged from the scout pledge), yielding maximum net points across the mid-to-late game.
    - Continue acting `raid` in rounds 4 and 5 if my target persists in pledging/acting `scout` despite previous defections.
  - **Counter-Defection & Defensive Adjustments:**
    - If my clockwise target is expected to act `escort` or `raid`, do not act `raid` (hitting a non-scout costs 1 point). Act `scout` if unthreatened, or act `escort` (`[act: escort]`) if my incoming attacker is raiding me.
    - If my incoming attacker raids me while my target is defending, act `escort` to prevent theft (+2 points gained, incoming raider penalized -1 point).

- **Formatting:**
  - Provide a single short line of reasoning before the exact bracketed token: `[pledge: scout]`, `[act: scout]`, `[act: escort]`, or `[act: raid]`.