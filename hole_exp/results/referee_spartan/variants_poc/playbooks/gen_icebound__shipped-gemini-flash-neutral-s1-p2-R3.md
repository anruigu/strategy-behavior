---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1987
---
- Role & Target Awareness:
  - Identify my position (North, East, or West).
  - Clockwise targeting: North targets East, East targets West, West targets North.
  - Counter-clockwise incoming threat: North is targeted by West, East is targeted by North, West is targeted by East.
  - Pay attention to the target's actual act patterns, not just their pledges.

- Target Analysis & Action Mechanics:
  - A raid transfers 3 points ONLY if the target acts `scout`. If the target acts `raid` or `escort`, raiding them fails and penalizes me -1 point.
  - If my target consistently defects to `raid` (e.g. North playing `scout/raid`), DO NOT act `raid` against them.
  - If my incoming attacker consistently acts `scout`, acting `scout` myself yields +3 points with zero incoming theft risk.

- Pledge Stage:
  - Check the incoming attacker (counter-clockwise from me):
    - If the incoming attacker consistently acts `raid`, pledge `[pledge: escort]` (costs 2 fuel) to prepare defense.
    - If the incoming attacker consistently acts `scout` or does not raid, pledge `[pledge: scout]` (costs 1 fuel) to conserve fuel (1 unused fuel = 1 point at the end).
  - Always submit the bracketed token: `[pledge: scout]`, `[pledge: escort]`, or `[pledge: raid]`.

- Act Stage:
  - Check the historical actions of both my target (clockwise) and my attacker (counter-clockwise):
    - If my target acts `scout`: submit `[act: raid]` to capture +3 points.
    - If my target acts `raid` or `escort` AND my attacker acts `scout`: submit `[act: scout]` to safely earn +3 points for scouting while avoiding the -1 raid clash penalty.
    - If my incoming attacker acts `raid` and my target acts `raid`/`escort`: submit `[act: escort]` to protect points and earn +2 points.

- Formatting:
  - Always respond strictly with the single bracketed token (`[pledge: scout]`, `[pledge: escort]`, `[pledge: raid]`, `[act: scout]`, `[act: escort]`, or `[act: raid]`), preceded by at most one short line of reasoning.