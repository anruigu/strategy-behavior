---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 2943
---
### Mechanics & Directional Awareness
- Raid direction is fixed clockwise: North $\to$ East, East $\to$ West, West $\to$ North.
- My target to raid is the player clockwise from me (as West, my target is North).
- My direct threat who can raid me is the player counterclockwise from me (if I am West, East threatens me; if North, West threatens me; if East, North threatens me).
- Fuel cost is charged strictly upon *pledge* (scout: 1, escort: 2, raid: 2).
- The act stage accepts any valid action (`scout`, `escort`, `raid`), allowing me to deviate from my pledge based on the revealed public pledges of all players.
- Unused fuel scores 1 point each at game end. Net yield:
  - Successful scout (not raided): +3 points - 1 fuel = +2 net.
  - Escort: +2 points - 2 fuel = 0 net (neutral point gain, protects fuel/points from raid).
  - Successful raid (target scouted): +3 points stolen - 2 fuel = +1 net (plus denying target +3).
  - Failed raid (target escorted or raided): -1 point - 2 fuel = -3 net.

---

### Pledge Strategy
- In Round 1, always submit `[pledge: scout]` to conserve fuel and project cooperative intent.
- In Rounds 2 through 5:
  - If opponents regularly scout at act stage, submit `[pledge: scout]` to minimize fuel deduction.
  - If I plan to raid at act stage, submit `[pledge: raid]` only if I need fuel deduction committed, but prefer `[pledge: scout]` when fuel is tight to retain the flexibility of spending only 1 fuel if I decide to stay scout.

---

### Act Strategy
- **If the player clockwise from me (my target) pledged `scout` and historically stays `scout`:**
  - If my threat (counterclockwise player) is not raiding me, submit `[act: raid]` to steal 3 points from my target.
- **If my threat (counterclockwise player) is likely to act `raid`:**
  - Do not act `scout` (a scouted player loses 3 points).
  - Submit `[act: escort]` if I need to neutralize their incoming raid and score safe escort points, or submit `[act: raid]` if my own target is also scouting.
- **If my target is defecting/raiding or escorting consistently:**
  - Never act `raid` against them (a failed raid costs -1 point and loses fuel value).
  - Submit `[act: scout]` if unthreatened, or `[act: escort]` if threatened.
- **When all players pledge `scout`:**
  - If opponents consistently defect to `raid` at the act stage, submit `[act: escort]` or `[act: raid]` against my target rather than naively scouting.
  - If opponents genuinely stay `scout`, submit `[act: raid]` against my target to capture the swing.

---

### Fuel and End-Game Management
- Track fuel closely so I never enter a round with 0 fuel unless it is Round 5.
- Remember that holding unused fuel converts to points 1:1; do not waste 2 fuel on an escort or failed raid if saving fuel yields higher net value.
- In Round 5, if my target is scouting, submit `[act: raid]`; if I am threatened and target is raiding, evaluate whether saving fuel beats escorting.