---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2831
---
# Icebound Playbook

## Rules & Mechanics
- Direction of attack (clockwise): North -> East -> West -> North.
- Incoming threats:
  - If I am East, my incoming attacker is North.
  - If I am North, my incoming attacker is West.
  - If I am West, my incoming attacker is East.
- My raid target:
  - If I am East, I target West.
  - If I am North, I target East.
  - If I am West, I target North.
- Costs & Pledges:
  - Fuel is deducted upfront based on the *pledge* (Scout: 1, Escort: 2, Raid: 2).
  - Unused fuel converts 1:1 to points after Round 5.
  - Scout payout: +3 pts (if not raided), 0 pts (if raided).
  - Escort payout: +2 pts (immune to incoming raids).
  - Raid payout: +3 pts vs Scout (target loses 3 pts); -1 pt vs Escort or Raid.
  - **Deception Mechanism**: The act stage allows switching actions regardless of pledge (e.g., pledge scout, act raid or escort), while fuel charged remains strictly based on the pledge. Opponents frequently pledge scout to save fuel and deceive, then act raid.

## Pledge Phase Strategy
- Always pledge `[pledge: scout]` in every round to minimize fuel deduction (1 fuel cost), leaving maximum remaining fuel to convert into endgame points.

## Threat Assessment & Opponent History
- Check the previous round history (shown in the format `Player pledge/act`):
  - **Chronic Raider / Sneak Raider**: Pledges scout and acts raid. If my upstream attacker ever acts raid, assume they will raid every subsequent round regardless of what they pledge.
  - **Pure Cooperator**: Pledges scout and acts scout consistently.

## Act Phase Strategy
- **If upstream attacker has EVER acted raid in any prior round**:
  - Immediately stop acting scout. Acting scout against a raider earns 0 points and wastes the round.
  - If downstream target is a reliable scouter:
    - Submit `[act: raid]` to steal 3 points from downstream. When both North and East raid, North gets -1 pt for raiding into a raider (East) and East gets +3 pts from scouting West.
  - If downstream target is escorting or raiding:
    - Submit `[act: escort]` to secure +2 points and block the incoming raid.
- **If upstream attacker has NEVER acted raid (cooperative)**:
  - If downstream target is scouting:
    - Early rounds (1–3): Submit `[act: scout]` (+3 pts).
    - Endgame (Rounds 4–5): Consider switching to `[act: raid]` to steal 3 points from downstream.
  - If downstream target is raiding/escorting:
    - Submit `[act: scout]` (if upstream is safe) or `[act: escort]` (if defection is feared).

## Endgame (Rounds 4 & 5)
- Always pledge `[pledge: scout]`.
- If upstream attacker has acted raid, act `[act: raid]` if downstream is still scouting, or `[act: escort]` if downstream is defending.
- If upstream attacker is peaceful, submit `[act: raid]` against a scouting downstream target to harvest endgame points.