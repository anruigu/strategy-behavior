---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2654
---
# Icebound Playbook

## Rules & Mechanics Reminders
- Pledge costs fuel immediately (scout: 1, escort: 2, raid: 2).
- At the act stage, actions do **not** have to match pledges (players/bots routinely pledge `scout` and act `raid` or `escort`).
- Raids target clockwise: North -> East, East -> West, West -> North.
- Unused fuel converts 1:1 to points at game end.
- Raiding against an opponent who raids or escorts costs the raider 1 point; raiding against a scout transfers 5 points from the target to the raider.
- Escorting scores 2 points and prevents incoming theft entirely.

## Pledge Stage Policy
- Always submit `[pledge: scout]` in all rounds (1 through 5). 
  - Never pledge `raid` or `escort`; pledging `scout` minimizes upfront fuel deduction (cost 1 vs 2) and saves fuel for end-game conversion.

## Act Stage Policy
- Track both my incoming threat (counter-clockwise player) and my outgoing target (clockwise player):
  - If I am North: Threat is West, Target is East.
  - If I am East: Threat is North, Target is West.
  - If I am West: Threat is East, Target is North.

- **Round 1:**
  - Submit `[act: scout]` to test baseline cooperation and score 3 points.

- **Round 2 onwards (Rounds 2 to 5):**
  - **Check Incoming Threat:** 
    - Look at the actual action history (not pledges) of my counter-clockwise threat.
    - If the threat has acted `scout` in all previous rounds and has never raided me, submit `[act: scout]` to earn 3 points. Note: West pledging `escort` but acting `scout` means West is scouting, not raiding. Do not escort unnecessarily if West reliably acts `scout`.
    - If the threat has acted `raid` in any previous round, or if there is credible risk of incoming raid, submit `[act: escort]` to secure +2 points and block theft.
  - **Check Outgoing Target:**
    - If my clockwise target has been acting `raid` or `escort`, raiding them will fail and penalize me (-1 point). Only act `raid` if my target reliably acts `scout` AND my threat is harmless.
  - **Round 5:**
    - If my incoming threat has never raided, stick to `[act: scout]`; if they have ever raided or shown aggression, default to `[act: escort]`.

## What Not To Do
- Never pledge `[pledge: raid]` or `[pledge: escort]`—it wastes 1 extra fuel upfront that would otherwise become end-game points.
- Never act `raid` into a target who is known to act `raid` or `escort` (costs 1 point).
- Never act `scout` when the incoming threat has actively defected and acted `raid` (loses 5 points).
- Do not mistake a player's pledged `escort` for an incoming attack if their actual act is consistently `scout`. Base threat assessments on resolved acts.