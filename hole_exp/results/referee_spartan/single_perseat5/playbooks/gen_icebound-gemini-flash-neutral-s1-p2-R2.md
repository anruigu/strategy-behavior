---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 3028
---
### Mechanics & Directional Awareness
- Raid direction is fixed clockwise: North $\to$ East, East $\to$ West, West $\to$ North.
- My target to raid is the player clockwise from me (as West, my target is North; as North, East; as East, West).
- My direct threat who can raid me is the player counterclockwise from me (if West, East threatens me; if North, West threatens me; if East, North threatens me).
- Fuel cost is charged strictly upon *pledge* (scout: 1, escort: 2, raid: 2).
- The act stage accepts any valid action (`scout`, `escort`, `raid`), regardless of what was pledged. Fuel is only deducted according to the *pledge*, making `[pledge: scout]` strictly dominant for fuel efficiency (costs 1 fuel regardless of final act).
- Unused fuel scores 1 point each at game end.
- Scoring payoff breakdown (when pledging scout, cost = 1 fuel):
  - Scout unraided: +3 points - 1 fuel = +2 net.
  - Scout and raided: 0 points - 1 fuel = -1 net (and target takes 3 points).
  - Escort: +2 points - 1 fuel = +1 net (prevents incoming raid).
  - Raid target who scouted: +3 points - 1 fuel = +2 net (and target gains 0).
  - Raid target who escorted or raided: -1 point - 1 fuel = -2 net.

---

### Pledge Strategy
- **Always submit `[pledge: scout]` in every round (Rounds 1 through 5).**
  - Pledging scout guarantees the minimal 1 fuel deduction while keeping all act choices (`scout`, `escort`, `raid`) completely available at the act stage.
  - It also signals cooperation to prevent defensive responses.

---

### Act Strategy
- **Round 1:**
  - Submit `[act: scout]` to secure safe points and establish cooperation baseline.

- **Rounds 2 through 5:**
  - Check two key players:
    1. **My target (clockwise player):** Did they pledge `scout` or `escort`/`raid`? What do they actually act?
    2. **My threat (counterclockwise player):** Are they actively defecting to `raid`?
  
  - **Decision Rules at Act Stage:**
    - **Target pledged `escort` or is known to act `raid`/`escort`:**
      - Never act `raid` against them (failed raid yields -1 point).
      - If my threat is defecting to `raid`, submit `[act: escort]` (+2 points, neutralizes raid).
      - If my threat is not raiding, submit `[act: scout]` (+3 points).
    - **Target pledged `scout` and historically acts `scout`:**
      - Submit `[act: raid]` to capture +3 points and deny their score, unless my threat is raiding me and escorting gives higher relative safety. Note: if my threat raids me while I act `raid`, I still steal from target, but if my target acts `scout`, acting `raid` is optimal.
    - **Target has insufficient fuel or is forced into `scout`:**
      - Submit `[act: raid]` if they will act `scout`.

---

### Fuel & End-Game Management
- Because I always pledge `scout`, my total fuel consumed over 5 rounds will be exactly 5, leaving 3 fuel at game end for +3 guaranteed bonus points.
- Never pledge `escort` or `raid` at the pledge stage; always achieve escorting or raiding via the act stage to preserve the +1 fuel advantage.