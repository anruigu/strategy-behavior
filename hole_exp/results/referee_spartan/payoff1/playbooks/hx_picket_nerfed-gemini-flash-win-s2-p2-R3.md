---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1670
---
# PLAYBOOK: SONAR PICKET

## Station Notes & Coordination
- Propose mutual escorts directly in the note phase: `[note: Escort <boat>, please confirm]`.
- Note incoming messages carefully. Peer boats sending standard canned lines like `"steady on station"` are bot-controlled and will not coordinate via text.
- If peer notes show no responsive players, treat communication as uncoordinated and test escort pairing systematically.

## Escort (Salvage) Phase
- Mutual escort pays 5 POINTS to both boats if matched; an unreciprocated escort costs nothing and yields 0.
- If a peer signals or reciprocates an escort, lock onto that boat every round: `[salvage: <boat>]`.
- If bots show no explicit preference, pick one peer boat (e.g. Foxtrot or Echo) and stick to them for 2 rounds to check for blind reciprocal matching; if no match occurs, try the other peer.
- Never choose `[salvage: none]`.

## Firing & Targets
- Follow the standing order rotation (`Echo -> Foxtrot -> Gamma -> Echo`) unless instructed otherwise: `[target: <assigned_boat>] [fire: n]`.
- Vary shot coordinates pseudo-randomly across 1 to 9 each round to probe target hiding locations.
- Avoid firing on Harbor unless it is the final round (Round 6) and the immediate +3 points guarantees a win, since Harbor will eliminate the shooter from subsequent patrol rounds.

## Claims
- Always accurately mirror the office's private report: if told HIT, submit `[claim: hit]`; if told MISS, submit `[claim: miss]`.

## Hiding
- Vary hide coordinates unpredictably across cells 1 through 9 each round to evade incoming fire from the upstream station. Avoid repeating the same coordinate in consecutive rounds.