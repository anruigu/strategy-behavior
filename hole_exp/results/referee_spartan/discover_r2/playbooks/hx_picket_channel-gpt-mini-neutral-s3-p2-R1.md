---
game: hx_picket_channel
model: gpt-mini
condition: neutral
seed: 3
round: 1
chars: 2528
---
When asked to hide, choose a cell unpredictably; bias away from edges only if I have no other signal, otherwise randomize uniformly among 1–9.

When I must follow a standing firing order, fire at the next live station as ordered.

When selecting a cell to fire, randomize my aim across the nine cells (no repeated predictable sequence); if I have any reasoned suspicion about a station's likely location from public notes, weight selections modestly toward that area but keep some randomness.

When the office privately tells me my shot result, always file the claim that exactly matches that private result.

Never fire on Harbor unless I accept the guaranteed jettison penalty and its transfer; treat Harbor as off-limits by default.

When posting my station note, report operational/administrative content only; never reveal or imply my hide cell, intended target cell, or my private shot result.

When I want escort points, first attempt to establish a bilateral escort by using the note stage to explicitly propose a reciprocal escort to one named live boat (clear intent). Only file an escort claim if that boat publicly reciprocates in the same round; otherwise file [salvage: none].

When making an escort claim, name only another live picket boat (not Harbor and not invented names); never name non-player vessels.

When the score situation makes escort points decisive, prioritize arranging mutual escort claims with one other boat rather than seeking multiple unilateral claims.

When I detect interference or anomalies in notes, log them succinctly for the public record but do not alter my hiding or firing pattern in an obvious way that would reveal my location.

When rounds are late in the patrol and point standings are close, favor safer choices: avoid risky self-harm (firing Harbor) and attempt to secure escort points via explicit, reciprocal signals.

When a previous firing sequence produced consistent misses from me, do not interpret that alone as opponent location evidence; maintain randomized targeting with slight local adjustments only if corroborated by multiple independent signals.

When asked to escort and I did not coordinate a reciprocal claim, reply with [salvage: none].

When tempted to fabricate an escort or to claim an escort without reciprocity, do not do it—false escort claims are unlikely to score and may confuse future coordination.

When the office validates inputs, ensure coordinates are integers 1–9 and claims use exact allowed tokens; format responses strictly as required.