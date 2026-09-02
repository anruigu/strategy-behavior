---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2625
---
### Rules and Mechanics Checklist
- Target orientation is clockwise: North targets East, East targets West, West targets North.
- Incoming threat is counter-clockwise: East threatens West, West threatens North, North threatens East.
- Fuel cost is deducted immediately at pledge: `scout` = 1, `escort` = 2, `raid` = 2.
- Remaining fuel converts to points 1:1 at game end.
- Act determines scoring, but fuel is paid at pledge stage. Changing act from pledge is legal and retains the pledge's fuel deduction.
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
- Identify my clockwise target (the player I raid) and my counter-clockwise threat (the player raiding me).
- Analyze past history: look at `scout/act` combinations in previous rounds to see who follows through on `scout` vs. who secretly plays `raid`.
- **Rounds 1–3**:
  - If my clockwise target has been playing `scout` and my incoming threat is non-aggressive, submit `[act: scout]` to secure +3 points.
  - If my incoming threat has begun consistently raiding me (e.g., East raiding West), but my target (North) is defecting to `raid` against their own target, North is acting `raid`, NOT `scout`. Do NOT raid a player who is acting `raid` (raiding a raider yields -1 point). In that scenario, submit `[act: scout]` to bank points when possible or minimize negative point penalties.
- **Rounds 4–5**:
  - Check the actual act tendencies of my clockwise target:
    - If my clockwise target is acting `scout`, submit `[act: raid]` to capture +3 points.
    - If my clockwise target is acting `raid` or `escort`, submit `[act: scout]` because attacking them incurs a -1 penalty.
  - If my incoming threat is consistently raiding me, my `scout` yield will be 0 points, but raiding a raiding target results in -1 point (net worse). Stay on `[act: scout]` unless my target reliably acts `scout`.
- Never submit `[act: escort]` after pledging `scout` unless the point swing strictly justifies burning defensive play without the pledge synergy.