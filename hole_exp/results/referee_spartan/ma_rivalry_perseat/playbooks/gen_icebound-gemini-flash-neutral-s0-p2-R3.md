---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2378
---
### Rules & Mechanics Reminder
- **Roles & Targets (Clockwise):** North $\to$ East, East $\to$ West, West $\to$ North.
- **Costs (deducted at pledge stage):** Scout = 1 fuel, Escort = 2 fuel, Raid = 2 fuel. Unused fuel at the end = 1 point each.
- **Scoring:**
  - Scout: 3 points if unraided, 0 points if raided.
  - Escort: 2 points, blocks incoming raids.
  - Raid: Steals 3 points from target if target acts Scout; loses 1 point if target acts Escort or Raid.
- **Pledge vs Act:** Fuel cost is determined and deducted at pledge submission based on the pledge. The actual outcome is resolved purely by submitted acts. Pledging `scout` spends only 1 fuel (saving +1 point in endgame fuel) while maintaining full strategic freedom to act `scout`, `escort`, or `raid`.

---

### Playbook

- **Pledge Stage (Rounds 1–5):**
  - Always submit `[pledge: scout]`. Never pledge `escort` or `raid`, as it unnecessarily wastes 1 fuel point up front and telegraphs intentions.

- **Act Stage (Rounds 1–4):**
  - Identify my clockwise target (North $\to$ East, East $\to$ West, West $\to$ North) and the upstream player targeting me.
  - Check history: if my upstream player defects and acts `raid` against me (e.g. East pledges scout but acts raid against West), do NOT continue acting scout passively while taking 0 points. Counteract upstream raids by acting `escort` (guaranteeing 2 points and blocking theft) or retaliating downstream with `raid` if my target acts scout.
  - If my upstream player is cooperative (acts `scout`), submit `[act: scout]`. This reliably harvests 3 points per round with minimal fuel expenditure.

- **Act Stage (Round 5 - Final Round):**
  - If my clockwise target is expected to act `scout` (e.g. North consistently acts scout), submit `[act: raid]` to steal 3 points.
  - If my upstream player is expected to raid me and my downstream target is also raiding/escorting, submit `[act: escort]` to protect against the raid and secure 2 points.
  - If my clockwise target is anticipated to act `escort` or `raid`, avoid raiding them to prevent the -1 point penalty.

- **What Not To Do:**
  - Never submit `[pledge: raid]` or `[pledge: escort]`.
  - Never continue blindly submitting `[act: scout]` in rounds 4–5 when history clearly shows the upstream player is submitting `[act: raid]`.
  - Never raid a target that is expected to act `escort` or `raid`.