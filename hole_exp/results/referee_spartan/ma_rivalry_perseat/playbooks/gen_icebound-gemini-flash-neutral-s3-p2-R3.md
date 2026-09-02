---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2632
---
### Rules and Mechanics Checklist
- Target orientation is clockwise: North targets East, East targets West, West targets North.
- Incoming threat is counter-clockwise: East threatens West, West threatens North, North threatens East.
- Fuel cost is deducted immediately at pledge: `scout` = 1, `escort` = 2, `raid` = 2.
- Remaining fuel converts to points 1:1 at game end.
- Act determines scoring, but fuel is paid at pledge stage. Changing act from pledge is legal and retains the pledge's fuel deduction (e.g., pledging scout and acting raid costs only 1 fuel).
- Target acts and payouts:
  - Scouting target: +3 to raider, 0 to scout.
  - Escorting target: -1 to raider, +2 to escort.
  - Raiding target: -1 to raider, raider resolves own attack independently.
  - Safe scout: +3 to scout (net +2 vs unused fuel).

---

### Playbook

#### Pledge Stage
- Always submit `[pledge: scout]` across all rounds (1 through 5).
  - It costs only 1 fuel upfront, preserving maximum fuel for the 1:1 end-game conversion.
  - It maintains a cooperative signal and lures opponents into committing to `scout`.
  - Never pledge `raid` or `escort`, as both waste 2 fuel upfront and scare opponents into defensive or retaliatory actions.

#### Act Stage
- Identify my clockwise target (the player I attack) and my counter-clockwise threat (the player who attacks me).
- Analyze round history (`pledge/act` records) carefully: distinguish what each opponent *pledged* from what they actually *acted*.

- **Rounds 1–3**:
  - Always submit `[act: scout]` in Round 1 to establish baseline play.
  - In Rounds 2 and 3, check the true acting history of my clockwise target:
    - If my clockwise target is acting `scout`, submit `[act: scout]` to secure +3 points (or take the 0 if raided by my threat, avoiding active penalties).
    - If my clockwise target has defected to `raid` (e.g., North acting `raid` against East), raiding North will result in a -1 penalty. Stick with `[act: scout]` because 0 is better than -1.

- **Rounds 4–5**:
  - Evaluate my clockwise target's actual act in the immediately preceding round(s):
    - If my clockwise target acted `scout` in the prior round (e.g., North acted `scout` in Round 4), submit `[act: raid]` to capture the +3 point theft.
    - If my clockwise target acted `raid` or `escort` in the prior round, submit `[act: scout]`, because attacking a raider or escort incurs a -1 point penalty.
  - Do not blindly raid in Round 5 if my target has a proven history of acting `raid` in late rounds; only raid if the target is genuinely acting `scout`.

- Never submit `[act: escort]` after pledging `scout`.