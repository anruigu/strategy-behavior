---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2295
---
### Rules & Mechanics
- **Roles & Direction:** Raids target clockwise: North $\to$ East, East $\to$ West, West $\to$ North.
- **Costs & Fuel:** Fuel cost is deducted strictly upon pledging: `scout` = 1, `escort` = 2, `raid` = 2. Unused fuel at game end is worth 1 point each.
- **Pledge vs Act Flexibility:** The referee checks fuel affordability only at the pledge stage. At the act stage, any valid action (`scout`, `escort`, `raid`) can be submitted regardless of pledge, without additional fuel cost or penalty.
- **Payoffs:**
  - `scout`: +3 points if not raided; 0 points if raided by the counter-clockwise neighbor.
  - `escort`: +2 points; prevents incoming theft from raid.
  - `raid`: Transfers +5 points from target if target scouts. If target escorts or raids, the raider suffers a -6 point penalty.

---

### Playbook

#### Pledge Stage
- Always submit `[pledge: scout]`. Pledging scout only costs 1 fuel, maximizes end-game fuel score, and conceals intent until the act stage.
- Never pledge `raid` or `escort` publicly; doing so wastes 1 fuel upfront and signals intent to other players.

#### Act Stage
- Identify my clockwise target (North $\to$ East, East $\to$ West, West $\to$ North) and my counter-clockwise threat (North $\leftarrow$ West, East $\leftarrow$ North, West $\leftarrow$ East).
- **Evaluating Actions:**
  - **Counter-Raid / Exploiting Scout Targets:** If my clockwise target has pledged `scout` and reliably plays `scout`, submit `[act: raid]`. This earns +5 points (stealing from the target), even if I am being raided by my upstream neighbor.
  - **Defending:** If my target is likely to play `escort` or `raid`, but my counter-clockwise neighbor is raiding me, submit `[act: escort]` to block the incoming raid and guarantee +2 points.
  - **Passive Scouting is a Trap when Raided:** If my upstream neighbor has started raiding (e.g. played `raid` in previous rounds), never play `[act: scout]`, as doing so results in 0 points. Always switch to `[act: raid]` (if target is scouting) or `[act: escort]` (if target is escorting/raiding).
  - **Default Cooperation:** If no players have defected to raiding and everyone is scouting reliably, play `[act: scout]` in early rounds, but look for opportunities to defect to `[act: raid]` against reliable scouters.