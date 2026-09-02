---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2655
---
### Rules & Mechanics
- **Roles & Direction:** Raids target clockwise: North $\to$ East, East $\to$ West, West $\to$ North.
- **Costs & Fuel:** Fuel cost is deducted upon pledging: `scout` = 1, `escort` = 2, `raid` = 2. Unused fuel at game end is worth 1 point each.
- **Pledge vs Act Flexibility:** The referee checks affordability at the pledge stage, but players are allowed to change their action at the act stage (`scout`, `escort`, or `raid`).
- **Payoffs:**
  - `scout`: +3 points if not raided; 0 points if raided by the counter-clockwise neighbor.
  - `escort`: +2 points; prevents incoming theft from raid.
  - `raid`: Transfers +5 points from target if target scouts. If target escorts or raids, the raider suffers a -6 point penalty.

---

### Playbook

#### Pledge Stage
- Always pledge `[pledge: scout]` regardless of intended action. Pledging `scout` costs only 1 fuel upfront, preserves the maximum fuel reserve (yielding 1 point per leftover fuel at game end), and hides aggressive or defensive intent until the act stage.
- Never pledge `raid` or `escort` publicly; doing so gives away intent, encourages targets to escort, and burns extra fuel.

#### Act Stage
- Identify my clockwise target (as East $\to$ West; North $\to$ East; West $\to$ North) and my counter-clockwise threat (as East $\leftarrow$ North; North $\leftarrow$ West; West $\leftarrow$ East).
- **Incoming Threat Analysis:**
  - Check the round history of my counter-clockwise attacker. If that player has acted `raid` in previous rounds (even if they pledged `scout`), they are a persistent raider.
  - If incoming threat is raiding:
    - If my target is scouting reliably, submit `[act: raid]` if I also want to steal 5 points, OR
    - Submit `[act: escort]` to block incoming raid, guarantee +2 points, and avoid getting zeroed out if not raiding.
- **Clockwise Target Analysis & Raiding:**
  - When my clockwise target pledges `scout` and consistently plays `scout`, raiding them yields +5 points.
  - Once an incoming threat starts raiding me repeatedly, do not passively play `scout` (which yields 0 points). Either counter-raid the downstream player with `[act: raid]` to capture +5 points, or play `[act: escort]` to secure +2 points and block the incoming raid.
  - Never submit `[act: raid]` if the target has pledged `escort` or `raid`, or is suspected of defecting to `escort`/`raid` (due to the -6 penalty).
- **Default Cooperative State:**
  - If no incoming player has shown aggressive defection and target is cooperative, play `[act: scout]` for steady +3 point gain and low fuel cost, reserving `[act: raid]` for opportunistic strikes in late rounds.