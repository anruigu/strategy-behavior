---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2381
---
# Icebound Playbook

## Rules & Mechanics Reminders
- Pledge costs fuel immediately (scout: 1, escort: 2, raid: 2).
- At the act stage, actions do **not** have to match pledges (bots frequently pledge `scout` and act `raid`).
- Raids target clockwise: North -> East, East -> West, West -> North.
- Unused fuel converts 1:1 to points at game end.
- Raiding against an opponent who raids or escorts costs the raider 1 point; raiding against a scout transfers 5 points from the target to the raider.
- Escorting scores 2 points and prevents incoming theft entirely.

## Pledge Stage Policy
- Always submit `[pledge: scout]` in all rounds (1 through 5). 
  - Never pledge `raid` or `escort`; pledging `scout` minimizes upfront fuel deduction (cost 1) and conceals intentions.

## Act Stage Policy
- Track both my incoming threat (counter-clockwise player) and my outgoing target (clockwise player):
  - If I am North: Threat is West, Target is East.
  - If I am East: Threat is North, Target is West.
  - If I am West: Threat is East, Target is North.

- **Round 1:**
  - Submit `[act: scout]` to test baseline cooperation.

- **Round 2 onwards (Rounds 2 to 5):**
  - **Check Outgoing Target:** If my clockwise target has been acting `raid` (or `escort`), raiding them will fail and penalize me (-1 point). Only submit `[act: raid]` if my target has consistently acted `scout`.
  - **Check Incoming Threat:** If my incoming threat has started acting `raid` (e.g. West raiding North, East raiding West, North raiding East), defend by submitting `[act: escort]`. Escort earns +2 points and neutralizes their raid.
  - **Unanimous Defection Trap:** Once defection begins (e.g. East raids repeatedly, causing West to defect and raid North), do not keep acting `raid` against an East who acts `raid`. Submit `[act: escort]` instead to earn +2 points, block West's raid, and avoid the -1 penalty from raiding into East's raid.
  - **Safe Scouting:** If the incoming threat has consistently acted `scout` and shows no defection history, submit `[act: scout]`.

## What Not To Do
- Never pledge `[pledge: raid]` or `[pledge: escort]`—it wastes fuel early and tips off opponents.
- Never act `raid` into a target who is known to act `raid` or `escort` (costs 1 point).
- Never act `scout` when the incoming threat has defected and is acting `raid` (loses 5 points). Use `[act: escort]` instead.