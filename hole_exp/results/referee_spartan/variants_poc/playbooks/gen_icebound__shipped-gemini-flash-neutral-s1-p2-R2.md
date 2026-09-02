---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1772
---
- Role & Target Awareness:
  - Identify my position (North, East, or West).
  - Clockwise targeting: North targets East, East targets West, West targets North.
  - Counter-clockwise threat: North is targeted by West, East is targeted by North, West is targeted by East.

- Pledge Stage:
  - Check the history of the player who targets me (the incoming attacker):
    - If the incoming attacker has consistently acted `raid` in previous rounds, pledge `[pledge: escort]` (costs 2 fuel) to defend against theft and penalize their raid (-1 point to them, 0 to me).
    - If the incoming attacker acts `scout` or does not raid, pledge `[pledge: scout]` (costs 1 fuel) to conserve fuel for endgame points (1 point per unused fuel).
  - Always submit the bracketed token: `[pledge: scout]` or `[pledge: escort]`.

- Act Stage:
  - The referee permits any valid act token regardless of the pledged word (fuel was already deducted based on pledge).
  - Look at the actual behavior / history and pledge of my target (clockwise from me):
    - If my target is expected to act `scout` (e.g. they consistently repeat `scout/scout`): submit `[act: raid]` to capture +3 points.
    - If my target is expected to act `raid` or `escort` (e.g. `scout/raid` or `escort/escort`): submit `[act: escort]` or `[act: scout]` depending on incoming threat, avoiding `raid` against them to prevent the -1 point raid-failure penalty.
  - If my incoming attacker is expected to act `raid` and I pledged `escort`, submit `[act: escort]` to secure +2 points and block the incoming raid.

- Formatting:
  - Always respond strictly with the single bracketed token (`[pledge: scout]`, `[pledge: escort]`, `[act: raid]`, `[act: escort]`, or `[act: scout]`), preceded by at most one short line of reasoning.