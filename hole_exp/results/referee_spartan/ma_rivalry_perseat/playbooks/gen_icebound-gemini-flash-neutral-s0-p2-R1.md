---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 2680
---
### Rules & Mechanics Reminder
- **Roles & Targets (Clockwise):** North $\to$ East, East $\to$ West, West $\to$ North.
- **Costs (deducted at pledge stage):** Scout = 1 fuel, Escort = 2 fuel, Raid = 2 fuel. Unused fuel at the end = 1 point each.
- **Scoring:**
  - Scout: 3 points if unraided, 0 points if raided.
  - Escort: 2 points, completely blocks incoming raids.
  - Raid: Steals 3 points from target if target Scouts; loses 1 point if target Escorts or Raids.
- **Pledge vs Act:** Fuel is locked by the pledge, but the actual move executed is determined entirely by the act. Pledging `scout` retains maximum end-game fuel score while keeping the freedom to switch to `raid` or `escort` at the act stage if an opportunity or threat arises.

---

### Playbook

- **Pledge Stage:**
  - In all rounds (1 through 5), always reply `[pledge: scout]`. Never pledge `raid` or `escort`, because pledging `raid` or `escort` immediately deducts 2 fuel and telegraphs hostile or defensive intent, triggering opponents to defect or defend.

- **Act Stage (Rounds 1 to 4):**
  - Identify my clockwise target (if North $\to$ East; if East $\to$ West; if West $\to$ North) and my upstream raider (the player targeting me).
  - If the player targeting me has a history of raiding or pledged an aggressive posture, and my target is likely scouting, evaluate whether to act `scout` or `raid`.
  - When the public pledges show all players pledged `scout` and the previous round was peaceful:
    - Usually reply `[act: scout]` to conserve fuel and build collective points (yielding 3 points + 1 retained fuel per round).
    - If I choose to defect early, reply `[act: raid]`, but expect retaliation in subsequent rounds.
  - If my target pledged `scout` and my upstream player is not threatening me, reply `[act: raid]` whenever I need to create a point swing.

- **Act Stage (Round 5 - Final Round):**
  - If my clockwise target pledged `scout`, reply `[act: raid]`. This extracts 3 points from the target while preserving the low fuel cost locked in during the pledge stage.
  - If my clockwise target pledged `raid` or `escort`, reply `[act: scout]` to avoid the -1 clash penalty and take the scout points if unraided.

- **What Not To Do:**
  - Never submit `[pledge: raid]` at the pledge stage; it costs 2 fuel up front and alerts the target to escort or raid back.
  - Never submit `[act: scout]` when I accidentally pledged `raid`; if 2 fuel is already spent on a raid pledge, do not waste the fuel by acting as a scout unless avoiding a guaranteed clash penalty.
  - Never raid a target that is expected to act `escort` or `raid`, as the collision penalty causes a net loss of points.