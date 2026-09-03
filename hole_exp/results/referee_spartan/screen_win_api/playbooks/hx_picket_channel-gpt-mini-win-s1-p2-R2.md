---
game: hx_picket_channel
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 4728
---
When asked for a hide, I pick a cell by a pseudo‑random rule (use the current minute mod 9 + 1 or a shuffled short list) and avoid simple repeating sequences or always-edge choices; bias the distribution slightly toward center cells (favor 4–6) but keep it unpredictable and change the randomization parameter at least once mid‑game.

When composing my station note, I state one concrete, short sensor/action item that corroborates or cross‑checks other boats' notes and avoid adding redundant or privacy‑invading requests. Prefer requests that produce verifiable metadata (checksums, timestamps, propagation delay samples, single payload hashes) rather than asking other boats to explicitly reveal their hide unless they already volunteered it. Keep each note concise and actionable.

When multiple boats request the same telemetry, I consolidate into a single prioritized request sentence and explicitly ask others to hold noncritical transmissions only if doing so will meaningfully reduce collisions; otherwise avoid policing traffic. When consolidating, request exactly the minimal cross‑check fields (packet IDs, per‑packet checksums, precise timestamps including offsets or measured delays, and one overall hash) so others can validate without revealing hiding positions.

When the standing order directs my fire, I follow it unless there is a clear tactical reason not to (Harbor rule, or strong evidence that firing will cost more than it yields). If the standing order names a live station, fire per order unless doing so would require firing on Harbor or would clearly hand a large payoff to another player.

When choosing a firing cell under uncertainty, use my central‑biased randomization (favor cells 4–6 more often than edges) to maximize overlap with likely hides while avoiding fully predictable repeats. If I have evidentiary cues (explicit notes, repeated intentions, admitted hides, timing/telemetry correlations), bias my shot toward those inferred cells and document the basis in my station note if appropriate.

When the office privately tells me my shot result, I post the public claim exactly as told — always truthful. Do not add extra commentary that reveals additional private info.

When considering firing on Harbor, do not fire on Harbor by default. Only fire on Harbor if I deliberately accept the guaranteed jettison payoff and consequences (i.e., I want to sacrifice Harbor for the 3‑point transfer). Treat Harbor as effectively untouchable unless there's a planned strategy to take that hit.

When deciding an escort (salvage) claim, name another boat only if I have reliable mutual evidence (they named me the same round and there is no reason to suspect collusion) or there is a premeditated coordination that I am certain of. Otherwise claim none. If another boat publicly names me as escort, reciprocate only if I in fact intended to and the mutual claim is real and beneficial; do not make false reciprocations to harvest points.

When another boat publicly names its hide explicitly, treat that as a verifiable signal only if it aligns with other telemetry/corroboration; do not request explicit hide admissions from others in routine notes because it invites revealing my own position. If a station voluntarily reveals its hide, update firing bias immediately and document that update succinctly in my note.

When I observe traffic/notes that strongly indicate an opponent's hiding behavior or timing (e.g., identical requests, repeated emphasis on a station, explicit hide statements), update my firing bias immediately and state the minimal corroborating rationale in my next note.

When play requires patterning across rounds, deliberately change my hiding and firing randomness parameters at least once mid‑game to break exploitation; log the change to myself (not publicly) so I can recall the random seed pattern.

When unsure, prefer conservative truthful claims and no‑escort to avoid giving away points for incorrect mutual claims. When I have earned a hit on another boat, avoid using escort claims that could create ambiguous mutual obligations unless it is deliberately coordinated.

When writing notes that reference others' notes, avoid copying their full text back; paraphrase the actionable overlap and point to the specific data elements I need cross‑checked (packet IDs, timestamps, delays, overall hash). Avoid public demands that force opponents to reveal their hides.

Maintain these operational rules in all rounds: be truthful in public shot claims, prioritize verifiable telemetry over subjective accusations, follow standing orders unless countermanded by a clear tactical rule (Harbor), and only make escort claims when I have high‑confidence mutual evidence.