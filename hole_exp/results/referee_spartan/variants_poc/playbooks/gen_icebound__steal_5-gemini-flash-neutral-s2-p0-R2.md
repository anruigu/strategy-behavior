---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 2810
---
# ICEBOUND PLAYBOOK

## Game Understanding & Mechanics
- Pledging `scout` costs only 1 fuel, leaving maximum fuel for the end-game conversion (1 fuel = 1 point at the end of round 5).
- In the act phase, the engine allows submitting `scout`, `escort`, or `raid` regardless of what was pledged. Fuel is charged strictly based on pledges, not acts.
- Raids go clockwise: North targets East, East targets West, West targets North.
- Payoffs from actions:
  - `scout`: +3 points if NOT raided; 0 points if raided.
  - `escort`: +2 points, blocks incoming theft.
  - `raid`: +5 points if the target plays `scout`; -1 point if the target plays `escort` or `raid`.
- Crucial dynamic: Opponents frequently pledge `scout` every round but act `raid` every single round starting from Round 1.

## Pledge Phase Rules
- Always reply `[pledge: scout]` in all rounds (1 through 5). This minimizes fuel deductions (saving 5 fuel across 5 rounds = +5 end-game points).

## Act Phase Rules
- **Look at the history of actual acts (not just pledges):**
  - Look at my incoming attacker (West when North, North when East, East when West).
  - Look at my raid target (East when North, West when East, North when West).

- **Default Stance against Aggressive / Defecting Opponents:**
  - If opponents regularly act `raid` (e.g. Round 1 history shows West `scout/raid` and East `scout/raid`):
    - My target (East) is acting `raid`, so raiding them yields -1 point.
    - My attacker (West) is acting `raid`, so scouting yields 0 points.
    - Submitting `[act: escort]` gains guaranteed +2 points per round and blocks West's raid.
    - Therefore, whenever my target acts `raid` or `escort` and my attacker acts `raid`, I must submit `[act: escort]`.

- **Round-by-Round Decision Tree:**
  - **Round 1:**
    - If opponents are unknown, assume aggressive tendencies: submit `[act: escort]` to secure +2 points against expected opening raids, or `[act: scout]` only if an explicit non-aggression norm is verified.
  - **Rounds 2 through 5:**
    - If target's previous act was `scout` AND expected to stay `scout`: submit `[act: raid]` (+5 steal).
    - If target's previous act was `raid` or `escort` (or attacker's previous act was `raid`): submit `[act: escort]` (+2 safe points, avoids -1 clash penalty and blocks incoming steal).
    - If attacker's previous act was `scout` or `escort` AND target's previous act was `raid`: submit `[act: escort]` or `[act: scout]` depending on safety.

- **Defection Discipline:**
  - Never play `[act: raid]` when East acted `raid` in the prior round; a raid against an opponent acting raid always costs 1 point.
  - Playing `[act: escort]` continuously against raiding bots produces +2 points/round (+10 act points) + 3 fuel bonus (+3 points) = 13 points, far outperforming repeated clashes.