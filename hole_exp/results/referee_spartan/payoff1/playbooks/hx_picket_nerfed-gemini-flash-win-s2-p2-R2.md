---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1718
---
# PLAYBOOK: SONAR PICKET

## Station Notes & Coordination
- In the note phase, clearly propose a mutual escort pair: `[note: Escort <boat>, please confirm]`.
- Pay close attention to incoming notes from other boats. If a bot consistently sends "steady on station" and ignores proposals, recognize that bot is non-communicative and test alternatives (e.g., switch escort offers to the other active boat if one is non-responsive).
- Keep communication explicit and direct to maximize the chances of establishing a 5-point mutual escort.

## Escort (Salvage) Phase
- If another boat explicitly signaled an escort match with me, name them: `[salvage: <boat>]`.
- If an ongoing partner fails to reciprocate across consecutive rounds, pivot to naming the other peer boat rather than staying locked into an unreciprocated pair.
- Never default to `[salvage: none]` while positive pairing opportunities exist.

## Firing & Targets
- Adhere to the rotation order (`Echo -> Foxtrot -> Gamma -> Echo`) unless a coordinated shift is arranged: `[target: <assigned_boat>] [fire: n]`.
- Vary shot coordinates unpredictably across rounds (avoid repetitive predictable firing patterns) to improve hit rates against evading opponents.
- Do not fire on Harbor unless forced by an extreme point deficit where Harbor's immediate 3-point payout outweighs the elimination risk.

## Claims
- Strictly report the private office result: if reported MISS, submit `[claim: miss]`; if reported HIT, submit `[claim: hit]`. Public claims must match private truths.

## Hiding
- Randomize/vary hide coordinates across rounds (1 to 9) to prevent incoming shooters from predicting movement patterns. Avoid repeating the same cell in consecutive rounds.