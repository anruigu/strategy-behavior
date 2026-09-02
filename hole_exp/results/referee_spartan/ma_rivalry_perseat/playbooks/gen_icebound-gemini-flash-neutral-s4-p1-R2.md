---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 2170
---
- Always pledge `[pledge: scout]`. Pledging scout minimizes upfront fuel deduction (cost 1 fuel instead of 2), preserves fuel for the endgame score conversion (1 fuel = 1 point), and retains maximum flexibility to choose actions at the act stage.
- Never pledge `[pledge: raid]` or `[pledge: escort]`. Visible non-scout pledges reveal intent, scare targets into defection or escort, and lock in higher fuel costs upfront.

- Raids target clockwise: North -> East, East -> West, West -> North. Incoming threat comes counter-clockwise (North attacks East, East attacks West, West attacks North).

- At the action stage, assess the state of defection and mutual raid dynamics:
  - In Round 1, execute `[act: raid]` against an unescorted `scout` target to seize an immediate +3 point lead while only having spent 1 fuel on the pledge.
  - Notice the escalation: once I raid in Round 1, my target will typically defect to `raid` in Round 2, and the third player will follow in Round 3, resulting in an all-raid act equilibrium where every player acts `raid`.
  - When all players are acting `raid`, every raid hits another raider, giving everyone -1 point per round (3 rounds of mutual raid drops score from +3 to 0).
  - Therefore, once mutual raiding escalates (Round 3 onwards, or after other players have started defecting to `raid`):
    - If my target is raiding/escorting, raiding them yields -1 POINT.
    - If incoming raider hits me while I scout, scouting scores 0 POINTS. 0 POINTS is strictly better than -1 POINT.
    - If everyone is defecting to `raid`, switch to `[act: scout]` or evaluate if an `[act: escort]` is needed to protect an existing point lead. If all players raid each other, choosing `[act: scout]` avoids the -1 point penalty of a failed raid.
  - If my clockwise target is still reliably acting `scout`, play `[act: raid]` to capture +3 points.
  - In Round 5, only play `[act: raid]` if my target is likely to act `scout`; if the table is locked in mutual raiding, do not blindly raid into another raider for -1 point.

- Never pledge `raid` or `escort` and act `scout`—fuel is deducted based on the pledge. Always keep the pledge at `scout`.