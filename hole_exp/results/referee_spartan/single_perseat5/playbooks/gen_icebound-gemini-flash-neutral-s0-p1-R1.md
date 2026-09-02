---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 3029
---
# Icebound Playbook

## Rules & Mechanics
- Direction of attack: North -> East -> West -> North.
- Incoming threats:
  - If I am East, my incoming threat is North.
  - If I am North, my incoming threat is West.
  - If I am West, my incoming threat is East.
- My raid target:
  - If I am East, I target West.
  - If I am North, I target East.
  - If I am West, I target North.
- Costs & Pledges:
  - Fuel is deducted based on the *pledge* (Scout: 1, Escort: 2, Raid: 2).
  - Unused fuel converts 1:1 to points at the end of round 5.
  - Scout net gain if safe: +3 pts - 1 fuel = +2 net over sitting on fuel.
  - Escort net gain: +2 pts - 2 fuel = 0 net over sitting on fuel (only useful for defense).
  - Raid net gain vs Scout: +3 pts - 2 fuel = +1 net (plus steals 3 from target).
  - Raid vs Escort/Raid: -1 pt - 2 fuel = -3 net penalty.
  - **Critical Rule**: The act phase *allows* deviating from the pledge (e.g. pledge scout, act raid), but fuel is charged on the pledge cost, while scoring resolves on the submitted act. However, if my upstream neighbor raids me, scouting yields 0 points.

## Pledge Phase Strategy
- Check incoming threat's fuel and recent behavior:
  - If the player who attacks me has shown a propensity to raid (or in later rounds where raids become frequent):
    - When I expect an incoming raid and cannot afford to lose 3 points, pledge `[pledge: escort]`.
  - When the environment is cooperative or my attacker lacks fuel to raid:
    - Pledge `[pledge: scout]` to minimize fuel deduction (1 fuel) and signal cooperation.
- Do not pledge `[pledge: raid]` early unless specifically aiming to deter, as it burns 2 fuel upfront.

## Act Phase Strategy
- If I pledged `[pledge: scout]`:
  - Look at the public pledges:
    - If my incoming attacker pledged `raid`: 
      - If I can switch action to `[act: escort]`, do it to protect points, or switch to `[act: raid]` against my downstream target if they pledged `scout` (mutual trade).
    - If my incoming attacker pledged `scout` (or cannot raid me), and my downstream target pledged `scout`:
      - Evaluate defecting: switching to `[act: raid]` pays off heavily if downstream is scouting and won't switch, but note it triggers retaliation in future rounds. In Round 5, if downstream pledged scout, submit `[act: raid]`.
      - In early/mid rounds with mutual cooperation, submit `[act: scout]` to maintain peace and earn +3 points.
- If I pledged `[pledge: raid]`:
  - If my downstream target pledged `escort` or `raid`, and I want to avoid the -1 point penalty, submit `[act: escort]` or `[act: scout]`.
  - If my downstream target pledged `scout`, submit `[act: raid]`.
- If I pledged `[pledge: escort]`:
  - Submit `[act: escort]` to ensure incoming raid defense.

## Endgame (Rounds 4 & 5)
- Expect end-game defection / raid cascades from all players.
- In Round 5:
  - If my upstream threat pledged `raid`, do not submit `[act: scout]` (it will be stripped to 0 points).
  - If my downstream target pledged `scout`, submit `[act: raid]`.