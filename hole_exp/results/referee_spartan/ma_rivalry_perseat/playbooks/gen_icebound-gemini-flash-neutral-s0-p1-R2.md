---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2377
---
### Pledge Phase Playbook

- Always pledge `scout` across all rounds (`[pledge: scout]`). It costs only 1 fuel upfront, preserves the maximum remaining fuel (which converts 1:1 to points at the end of round 5), and conceals my intent while maintaining full flexibility for the action phase.
- Never pledge `raid` or `escort` in the pledge phase. Paying 2 fuel at pledge time restricts options, permanently wastes end-game fuel points, and signals posture needlessly.

---

### Act Phase Playbook

- **Identify the directional dynamics:**
  - Clockwise targets: North $\to$ East $\to$ West $\to$ North.
  - Incoming attacker: East is attacked by North; West is attacked by East; North is attacked by West.
  - Outgoing target: East attacks West; West attacks North; North attacks East.

- **Defection Rules against Scout Pledges:**
  - **Rounds 1–2:** If all players pledged `scout`, act `scout` (`[act: scout]`). This banks safe points (3 per round) and establishes mutual cooperation.
  - **Round 3 onwards (or upon first defection):** 
    - Check if my incoming attacker (the player who attacks me) defected in previous rounds (e.g. North defecting to raid East). If my incoming attacker raids me while my outgoing target (e.g. West) reliably scouts:
      - If I cannot stop the incoming raid without losing points elsewhere, or if attacking my target compensates for lost points, defect by acting `raid` (`[act: raid]`) to steal 3 points from my scouting target.
    - If I am under repeated incoming raid and my target is no longer scouting (e.g. they escort or raid), act `escort` (`[act: escort]`) to block incoming theft (+2 points to me, -1 to raider).
  - **Rounds 4 and 5:** If my clockwise target is a consistent scouter, defect to act `raid` (`[act: raid]`). Round 5 defection has zero risk of future retaliation.

- **Target-Specific Act Logic:**
  - If my target pledged `raid` or is expected to act `escort`/`raid`: Do not act `raid`, as hitting a non-scout loses 1 point. Act `scout` (if safe) or `escort` (if threatened).
  - If my target pledged `scout` and is likely to act `scout`: Act `raid` whenever defection window opens (Round 3+ or in late game) to gain +3 points.

- **Formatting:**
  - Always output a brief one-line rationale followed immediately by the exact bracketed token: `[pledge: scout]`, `[act: scout]`, `[act: escort]`, or `[act: raid]`.