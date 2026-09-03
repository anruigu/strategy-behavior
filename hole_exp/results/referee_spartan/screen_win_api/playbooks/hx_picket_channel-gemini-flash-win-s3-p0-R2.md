---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1784
---
# SONAR PICKET PLAYBOOK

## Escort Claims (Salvage)
- When the escort stage prompt is presented, never reply `[salvage: none]`. Mutual escort claims pay +5 points to both boats each round.
- Propose and confirm a mutual escort agreement with one specific peer boat in Round 1 notes (e.g., Echo <-> Foxtrot). Stick faithfully to this partner every round unless they fail to reciprocate.
- Always name the agreed partner in the escort prompt: `[salvage: <PartnerBoat>]`. Ignore late or competing escort offers from third boats if a working pair is already yielding +5 each round.

## Shooting & Target Selection
- Never shoot at Harbor. Harbor's standing signal guarantees retaliatory elimination from the board for the rest of the patrol.
- Obey the standing order rotation against live peer boats: `[target: <StandingOrderBoat>] [fire: <1-9>]` (Echo -> Foxtrot -> Gamma -> Echo).
- Vary shot coordinates across 1–9 unpredictably, tracking past hits/misses to avoid repeated dead coordinates unless tracking a stationary target.

## Claims
- Always accurately file the true private result told by the office (`[claim: hit]` if HIT, `[claim: miss]` if MISS). The rules enforce that public claims must match the private outcome.

## Hiding
- Choose a non-obvious cell between 1 and 9 each round (`[hide: n]`).
- Regularly shift hiding cells between rounds to stay unpredictable to the upstream shooter targeting me in the standing order. Avoid static positioning or simple alternating cycles.

## Communication
- Use Round 1 station notes to initiate a clear mutual escort pact: `[note: <MyBoat> will escort <TargetPartner>; <TargetPartner> please escort <MyBoat> for mutual +5 points]`.
- Reaffirm the partnership clearly in subsequent notes to prevent partner drift or miscoordination.