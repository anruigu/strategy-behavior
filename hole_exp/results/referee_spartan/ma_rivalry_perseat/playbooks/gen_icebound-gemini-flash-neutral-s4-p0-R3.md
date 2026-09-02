---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 2410
---
### Core Mechanics & Edge Realities
- Pledges are public, but acts can differ from pledges (defecting during the act phase is permitted and resolved by the referee).
- Fuel cost is deducted based solely on the *pledged* mission cost (scout = 1, escort = 2, raid = 2). Unused fuel converts 1:1 to points at game end.
- Pledging scout only consumes 1 fuel per round, leaving maximum fuel (3 remaining at game end = +3 bonus points).
- Scouting yields +3 points if unraided, but 0 points if raided by the counter-clockwise neighbor.
- Raiding yields +3 points stolen from my clockwise target if they acted scout. If the target acted raid or escort, raiding loses 1 point (-1 penalty).
- Raids target strictly clockwise: North $\to$ East $\to$ West $\to$ North.
  - My raid target is East.
  - My incoming threat is West.
- Key observation: East frequently plays naive Tit-for-Tat or cooperative scout, reverting to `act: scout` whenever I or others raid, whereas West frequently defaults to `act: raid`. In this ecosystem, consistently executing `[act: raid]` against East repeatedly reaps +3 points per round.

---

### Pledge Strategy
- Always submit `[pledge: scout]` in every round:
  - Charges only 1 fuel per round.
  - Guarantees saving 3 fuel across 5 rounds (+3 end-game points).
  - Preserves full strategic flexibility to execute `scout`, `escort`, or `raid` at the act stage.

---

### Act Strategy

#### Round 1:
- Submit `[act: scout]`. Establish the baseline, observe initial defections, and let opponents reveal their tendencies.

#### Rounds 2 through 5:
- **Default Action:** Submit `[act: raid]`.
  - Opponents routinely pledge scout and often act scout (or reset to scout after Round 2). Executing `[act: raid]` exploits East's scout actions for +3 points.
  - Even if East occasionally raids in Round 2, East tends to revert to `act: scout` in Rounds 3–5, generating consistent +3 payoffs that vastly outweigh occasional -1 clash penalties.
- **Exception (Defensive Adjustment):**
  - If East has acted `raid` or `escort` for two consecutive rounds without ever reverting to `scout`, switch to `[act: scout]` to avoid the recurring -1 raid penalty (scoring 0 is strictly better than -1).
  - As soon as East acts `scout` again, immediately resume `[act: raid]`.

---

### Format Reminder
- Output short one-line reasoning followed by the exact bracketed token `[pledge: ...]` or `[act: ...]`.