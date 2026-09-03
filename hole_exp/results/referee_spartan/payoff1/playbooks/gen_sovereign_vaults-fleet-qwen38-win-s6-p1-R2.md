---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 1271
---
# Playbook: Sovereign Vaults

**Core principle: Never deposit. Declare your true yield.**

Each unit of gold I retain scores 2 points; each unit I deposit scores 1 point. My total gold per round is fixed (my yield), so depositing any unit strictly loses 1 point versus keeping it. There is no treasury bonus, no comparative mechanic, no round-end adjustment that rewards deposits. The only rational deposit is always 0.

**Declare stage:** Declare my actual yield. Since I will deposit 0 regardless, the declared number is effectively free — the audit only checks that my deposit doesn't exceed my declaration, and 0 never exceeds anything. Declaring my true yield is simple and safe.

**Deposit stage:** Always deposit 0. No exception. No round is special. No end-game bonus exists.

**Scoring expectation:** My total score will be 2 × (sum of all my yields across all rounds). This is the maximum achievable score and is independent of what the opponent does. The game is essentially solo optimization once you accept the never-deposit principle.

**What I confirmed in play:** The opponent also deposited 0 every round. No penalty was applied for declaring high and depositing 0. The audit passed cleanly every round. Final score matched exactly: 2 × (9+3+3+3+3) = 42.