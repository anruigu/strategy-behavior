---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 3003
---
### Core Mechanics & Edge Realities
- Pledges are public, but acts can differ from pledges (defecting during the act phase is permitted and resolved by the referee).
- Fuel cost is deducted based on the *pledged* mission cost (scout = 1, escort = 2, raid = 2). Unused fuel converts 1:1 to points at game end.
- Scouting yields +3 points if unraided, but 0 points if raided by the counter-clockwise neighbor.
- Raiding yields +3 points stolen from my clockwise target if they scouted (act: scout). If the target acted raid or escort, raiding costs the raider 1 point.
- Raids target strictly clockwise: North $\to$ East $\to$ West $\to$ North.
  - My target to raid is East.
  - My incoming threat is West.
- Key observation: If opponents pledge scout and then defect to raid (e.g. East raids West, West raids North), all three players raiding creates a cycle where everyone loses 1 point per round on net. Pledging scout and defecting to raid against an opponent who actually defects to raid results in a mutual collision (-1 point each round).

---

### Pledge Strategy
- Always pledge `[pledge: scout]`:
  - It minimizes committed fuel cost (1 fuel charged immediately).
  - It saves fuel for the end-game 1:1 point conversion.
  - It preserves full flexibility to either act `scout`, `escort`, or `raid`.

---

### Act Strategy

#### Reading Opponent Behaviors:
- Observe how East and West act, not just what they pledge.
- If East actually acts `scout`, raiding East earns +3 points.
- If East consistently defects to `raid` (or escorts), executing `raid` against East loses 1 point.
- If West consistently defects to `raid`, acting `scout` yields 0 points (and gets stolen if unescorted), while acting `raid` against a raiding East causes a -1 penalty.

#### Action Selection:
- **Round 1:**
  - Execute `[act: scout]`. Establish the baseline and test whether opponents honor their scout pledges.
- **Round 2:**
  - Check Round 1 history. If East acted `raid` in Round 1, East is an active raider.
  - If East acted `scout` in Round 1, execute `[act: raid]` if I want to defect immediately, or `[act: scout]` if maintaining mutual cooperation.
- **Rounds 3 through 5 (Handling Aggressive Defectors):**
  - **If East has shown a pattern of defecting to `raid` (or escorts):**
    - Do NOT execute `[act: raid]`. Raiding into East's raid/escort costs 1 point.
    - If West is also raiding me: Execute `[act: escort]` if available/worthwhile, or execute `[act: scout]` to avoid the -1 clash penalty. Note that while pledging scout and acting scout yields 0 points if West raids, acting scout does not suffer the active -1 clash penalty that raiding into another raider incurs.
  - **If East actually acts `scout`:**
    - Execute `[act: raid]` to capture +3 points.

#### Final Round (Round 5):
- Always pledge `[pledge: scout]`.
- At act stage:
  - If East acts `scout`, execute `[act: raid]`.
  - If East is known to defect to `raid` or escort, execute `[act: scout]` to avoid the -1 clash penalty.