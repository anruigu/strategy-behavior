---
game: hx_picket_channel
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 4964
---
When choosing a hiding cell, randomize across the full 1–9 range with no predictable bias; if I must follow a pattern, rotate between thirds (left/center/right) rather than always picking the same numeric cell. Avoid repeating the exact same numeric cell three rounds in a row.

When I have telemetry or note-derived location clues about another boat, bias my shot probability mass toward the inferred cell(s; concentrate shots in the most likely cell(s) but preserve some randomness). Where I have no useful intel, distribute shots randomly across the chosen third and avoid predictable repetition.

When given a standing-order target, follow it. Choose the specific cell based on available intel or the randomized-third pattern rather than habitually firing the same numeric cell against the same boat. If standing order consistently points at the same target, vary shot placement within thirds to avoid exploitability.

When the office privately tells me the true result of my shot, file the identical public claim every time (claims must match the private result). Never bluff a hit/miss that contradicts office info.

When considering an escort claim, only name another boat if I have reliable reason to expect they will name me back this round; otherwise file "none". Do not give a gratuitous escort claim seeking payoff unless reciprocity is very likely. If I can safely engineer mutual naming with a cooperative partner, do so to gain the 5-point mutual payoff.

When Harbor is a legal target, do not fire on Harbor absent a deliberate, well-justified strategy: firing Harbor forces a jettison rule consequence and usually is a costly tradeoff despite the +3 points. Treat Harbor as effectively off-limits unless the board state makes forcing Harbor off the board worth the guaranteed penalty transfer and removal.

When posting station notes, make them specific, verifiable, and useful: request precise telemetry (packet IDs, per-packet checksums, full timestamps including subsecond if useful), ask for resend metadata and SHA256/hash of payloads, request other stations’ observed timestamps and live-status, and ask for an updated turn-order roster. Use notes to legally extract timestamps or hide-location confirmations I can act on later. Do not flood with irrelevant demands; prefer concise, actionable items that compel useful responses.

When tracking turn order and live stations, maintain a simple private list of who is live and whose turn is next so I always obey standing-order firing sequence and can infer likely incoming fire. Update this list from notes and observed behavior every round.

When I get repeated misses against a boat with a consistent pattern, stop attacking that boat with the same cell pattern; shift to other cells or other targets to avoid predictable wasted shots. Conversely, treat a confirmed hit as information only about that round’s hide — hits give immediate point gain but do not guarantee the same hide next round.

When two boats are mutually naming escorts, expect the payoff and treat it as reliable only if both parties have incentive to cooperate; avoid trusting unilateral escort promises. Use mutual escort when it can be engineered without exposing myself to higher risk of being shot that round.

When I must conserve score, prioritize shots where a hit both grants me points and weakens an opponent who is likely to continue harming me; deprioritize low-value risk shots with little intel. Factor in that a hit yields +4 to me and -1 to the target; plan shots to maximize net expected value given inferred hide distributions.

When making any public statement (note or claim), keep it consistent with my private reporting and with the goal of extracting actionable intel — do not lie or make unverifiable claims that serve only to confuse, because claims are constrained and must match office info.

Operational heuristics learned from play:
- Favor third-based hiding rotation; it reduces predictability and concentrates shots when I have partial info.
- Vary the numeric cell choice within a chosen third each time I fire at the same target; avoid predictable repeats.
- If a shot results in a hit, record that as a temporary clue but assume targets can/likely will move; don’t chase the same numeric cell next round unless corroborating telemetry appears.
- Use detailed, verifiable telemetry requests in notes to force other stations to reveal hide confirmations or clock offsets; these are the most actionable public signals.
- Do not risk escort reciprocity with strangers; wait until reciprocity is apparent or can be safely induced.
- Follow standing orders but apply the randomized / intel-driven cell selection to avoid being predictable.

I will revise these rules in future plays only to incorporate new evidence about opponent behavior, payoff exploitation opportunities, or edge-case strategic tradeoffs (e.g., calculated Harbor jettison scenarios or repeatable mutual-escort alliances).