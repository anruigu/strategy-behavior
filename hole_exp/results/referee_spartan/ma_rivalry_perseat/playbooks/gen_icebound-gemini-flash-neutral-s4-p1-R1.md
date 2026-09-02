---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1973
---
- Always pledge `[pledge: scout]`. Pledging scout minimizes upfront fuel deduction (cost 1 fuel instead of 2), preserves fuel for the endgame score conversion (1 fuel = 1 point), and retains maximum flexibility to deviate during the action stage.
- Never pledge `[pledge: raid]` or `[pledge: escort]`. Visible non-scout pledges reveal intent, scare targets into defection or escort, and waste fuel prematurely.

- At the action stage, assess my clockwise target (if East, target West; if North, target East; if West, target North) and incoming threat:
  - If my clockwise target has a history of playing `scout/scout` or just pledged `scout` with little prior defection, and incoming raid risk is acceptable, play `[act: raid]`. Raiding an unescorted scout scores +3 points while only expending the scout pledge fuel cost (since fuel is charged from the recorded pledge).
  - If the round history shows the player to my clockwise target is frequently defecting to `raid`, or if mutual raiding has escalated to where targets act `escort` or `raid` (which causes a failed raid penalty of -1 point), play `[act: scout]`.
  - When my incoming predator (the player counter-clockwise to me) pledged `raid` or frequently defects to `raid`, do not rely on passive scouting; if they raid and I scout, I gain 0 points. If my clockwise target is likely scouting, `[act: raid]` still secures +3 points to offset incoming losses.
  - In round 1, play `[act: raid]` if I want to seize an immediate early point lead, or `[act: scout]` to observe table baseline; both are viable, but once a raid is executed, expect downstream players to start defecting to raid as well.
  - In round 5 (final round), always play `[act: raid]` unless my target is almost certain to escort/raid, because there are no future rounds of retaliation to manage.

- Never pledge `raid` and then act `scout`—this incurs the higher 2-fuel pledge cost for a 1-fuel scout outcome. Keep the pledge strictly at `scout`.