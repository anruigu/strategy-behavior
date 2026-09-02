---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 2354
---
# ICEBOUND PLAYBOOK

## Game Understanding & Mechanics
- Pledging scout only costs 1 fuel (saving fuel for the end-game 1 pt/fuel bonus), but the act stage allows submitting any valid action (`scout`, `escort`, `raid`).
- Raids go clockwise: North targets East, East targets West, West targets North.
- A raid on a scouting player gains 5 points (netting +5 points to the raider, while the scout earns 0).
- A raid hitting an escort or another raid loses 1 point (-1).
- An escort yields 2 points and blocks incoming raids from taking points.
- Remaining fuel converts 1:1 to points at the end of round 5.

## Pledge Phase Rules
- Always reply `[pledge: scout]` in all rounds to minimize fuel commitment (1 fuel deducted) while retaining maximum tactical choice for the act phase. Never pledge escort or raid unless forced by constraints.

## Act Phase Rules
- **Round 1 & Round 2 (Baseline Cooperation):**
  - If all players pledged scout, reply `[act: scout]` to secure steady +3 points and conserve fuel.
  - If the player targeting me (West when I am North) pledged `raid`, expect an incoming attack and reply `[act: escort]` if I need protection, or `[act: scout]` if willing to absorb.

- **Round 3 to Round 5 (Exploitation and Defense):**
  - **Check East (my target) and West (my attacker):**
    - If East has demonstrated a habit of defecting to `raid` or if everyone has started defecting, East is likely to `raid` or `escort` rather than `scout`. In that scenario, submitting `[act: raid]` against East will clash and result in -1 point; submit `[act: escort]` instead if West is likely raiding me, or `[act: scout]` if West is likely escorting.
    - If East has consistently submitted `scout` and is expected to actually play `scout`, submit `[act: raid]` to capture the +5 steal.
    - If West (the player targeting me) has shifted to raiding in previous rounds or pledged raid, submit `[act: escort]` to protect my points (+2 points, blocks theft) instead of scouting.

- **Defection Discipline:**
  - Do not blindly submit `[act: raid]` just because East *pledged* scout; check whether East defected to raid in prior rounds. If East previously defected to raid, assume East will act `raid` again, making my raid fail (-1 point). Against an aggressive/defecting East, play `[act: escort]` to defend against West while banking safe points.