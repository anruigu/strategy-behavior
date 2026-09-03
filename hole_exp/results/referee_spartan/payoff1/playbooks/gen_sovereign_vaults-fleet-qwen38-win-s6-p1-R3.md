---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 2020
---
# Playbook: Sovereign Vaults

**Core principle: Never deposit. Declare your true yield.**

Each unit of gold I retain scores 2 points; each unit I deposit scores 1 point. My total gold per round is fixed (my yield), so depositing any unit strictly loses 1 point versus keeping it. There is no treasury bonus, no comparative mechanic, no round-end adjustment that rewards deposits. The only rational deposit is always 0.

**Declare stage:** Declare my actual yield. Since I will deposit 0 regardless, the declared number is effectively free — the audit only checks that my deposit does not exceed my declaration, and 0 never exceeds anything. Declaring my true yield is simple, safe, and carries no risk. There is no benefit to inflating or deflating the declaration because the deposit is always 0.

**Deposit stage:** Always deposit 0. No exception. No round is special. No end-game bonus exists.

**Scoring expectation:** My total score will be exactly 2 × (sum of all my yields across all rounds). This is the maximum achievable score and is independent of what the opponent does. The game is solo optimization once you accept the never-deposit principle.

**History format note:** The round-history lines (e.g. "yields 1/9, declared 1/9, deposited 0/0") are in **p2/p1** order, not p1/p2. I confirmed this by cross-referencing: in round 1 the history read "yields 1/9" while I was told my private yield was 9, so the second number is mine. This matters only for reading the opponent's numbers; I never need to rely on the history for my own decisions since I am told my yield directly each round.

**What I confirmed in this episode:**
- Declared true yield every round (9, 7, 8, 7, 4). Deposited 0 every round.
- No audit failure. No penalty for declaring and depositing 0.
- Final score was exactly 2 × (9+7+8+7+4) = 2 × 35 = 70. ✓
- Opponent also deposited 0 every round (all deposits shown as 0/0).
- Opponent's score progression did not follow a simple 2×yield pattern, suggesting either a different strategy or