---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2723
---
### Core Rules & Mechanics
- Direction of attack: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North (clockwise).
- Unused fuel converts 1:1 to points at the end of Round 5.
- Pledging charges fuel upfront (`scout` = 1, `escort` = 2, `raid` = 2).
- The referee permits playing any action (`scout`, `escort`, `raid`) at the act stage regardless of the initial pledge, but pledged fuel is never refunded.
- Submitting a raid against an opponent who also raids or escorts loses 1 point; raiding a scout transfers 3 points from the target.
- Escort scores 2 points and blocks incoming raids. Raiding when other players also raid yields mutual penalties.

---

### Playbook

#### Pledge Stage
- **Rounds 1–4:** Always submit `[pledge: scout]`. It minimizes upfront fuel commitment (1 fuel), establishes table cooperation, and preserves maximum end-game fuel for points.
- **Round 5:** Always submit `[pledge: scout]`. Pledging scout only consumes 1 fuel, leaving maximum fuel to convert 1:1 to points at round end while retaining full freedom to act `scout`, `escort`, or `raid`.
- **General Rule:** Never submit `[pledge: raid]` or `[pledge: escort]`. Pledging either wastes extra fuel upfront without providing any action-phase benefit over a scout pledge.

#### Act Stage
- **Rounds 1–3:**
  - If no player has defected to raid, play `[act: scout]`. Conserves fuel and reliably earns 3 points.
  - If upstream player (the one who attacks me) defected to raid in the previous round, switch to `[act: escort]`.
- **Round 4:**
  - If all players have been fully peaceful, play `[act: scout]`.
  - If upstream player defected to raid in earlier rounds, play `[act: escort]`.
- **Round 5:**
  - If upstream player (West when I am North) pledged `escort` or defected to `raid` in Round 4: play `[act: escort]`. This defends against late-game defections and reliably locks in 2 points (+3 fuel conversion).
  - If all players pledged `scout` and table has been completely peaceful through Round 4:
    - If downstream player (East when I am North) is predicted to stay `scout` and upstream is predicted to stay peaceful/raid-blocked, play `[act: raid]` to capture +3 from downstream.
    - If there is any sign of downstream escorting or general end-game defections across the board, play `[act: escort]`.

#### Defection & Recovery Rules
- If upstream player defects to `raid` while pledging `scout`:
  - Keep pledging `[pledge: scout]` to conserve fuel, but submit `[act: escort]` in subsequent rounds to block incoming theft.
- Never chase lost points by submitting `[pledge: raid]` or blindly raiding against players likely to escort; protect remaining fuel to capture the guaranteed 1:1 end-game conversion points.