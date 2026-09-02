---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 2726
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
  - Scout and raided: 0 points - 1 fuel = -1 net.
  - Escort: +2 points - 1 fuel = +1 net (prevents incoming raid).
  - Raid target who scouted: +3 points - 1 fuel = +2 net (and target gains 0).
  - Raid target who escorted or raided: -1 point - 1 fuel = -2 net.

---

### Pledge Strategy
- **Always submit `[pledge: scout]` in every round (Rounds 1 through 5).**
  - Pledging scout guarantees the minimal 1 fuel deduction while keeping all act choices (`scout`, `escort`, `raid`) completely available at the act stage.
  - It maintains full flexibility and conceals actual intentions.

---

### Act Strategy
- **Round 1:**
  - Submit `[act: scout]` to secure safe points and establish cooperation baseline.

- **Rounds 2 through 5:**
  - Evaluate the public pledges and known behavior of both my target (clockwise) and threat (counterclockwise):
    1. **If my target pledged `escort` or `raid`:**
       - Do NOT act `raid` (hitting escort/raid loses 1 point).
       - If my threat has turned aggressive (frequently acts `raid`), submit `[act: escort]` (+2 points, blocks theft).
       - If my threat is not an active raid threat, submit `[act: scout]` (+3 points).
    2. **If my target pledged `scout`:**
       - Check target's history: if they consistently act `scout` when pledging `scout`, submit `[act: raid]` to steal +3 points.
       - If target is known to disguise acts by pledging scout but acting escort/raid, submit `[act: scout]` (or `[act: escort]` if threatened).

---

### Fuel & End-Game Management
- By consistently pledging `scout` across all 5 rounds, total fuel consumed will be at most 5, preserving at least 3 fuel for +3 bonus points at game end.
- Never pledge `escort` or `raid` at the pledge stage; execute tactical escorts or raids strictly through the act stage to preserve the fuel advantage.