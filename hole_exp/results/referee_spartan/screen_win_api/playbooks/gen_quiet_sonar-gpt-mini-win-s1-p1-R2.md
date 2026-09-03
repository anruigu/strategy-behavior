---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 3390
---
When asked to hide, avoid cells that have been targeted frequently in recent rounds; pick a cell that has not been targeted in the last two rounds unless patterns show an opponent favors new cells.

When asked to hide and there is no clear targeting pattern, randomize my hide among 3–4 chosen cells (include the center and two off-center cells) to avoid being predictable.

When asked to hide and I am behind in score, bias hides toward cells others rarely fire at; when I am ahead, bias hides toward cells that have been fired at recently (safer because opponents have already wasted shots).

Do not lock myself into the same hide repeatedly (I learned hiding 1 every round is predictable and wasteful); rotate among my chosen hide set so opponents cannot learn a single preferred hide.

When asked to fire at my fixed target, do not repeat the same firing cell every round; cycle through a preselected search order (for example 9,6,3,8,5,2,7,4,1) but allow occasional deviations to avoid being exploitable.

When asked to fire and opponents’ public claims show a cluster of hits on certain cells for the same target, prioritize firing those cells to exploit likely target placements — but require corroboration from multiple players’ fires/claims before committing repeat shots.

When I receive private feedback about my shot, I must report it truthfully in the public claim — the protocol requires claims to match the private result, so truthful reporting is mandatory and preserves correct public information.

When others’ claims are inconsistent with each other (contradictory hit patterns), treat claims as noisy and favor observed fire frequency and repeated corroborated claims over single isolated claims when inferring likely hides.

When opponents repeatedly target the same cell(s), exploit that by avoiding those cells when hiding and by firing them more often when my target is likely hiding there; however, if one player repeatedly targets a cell and always misses, deprioritize it as likely empty.

When I notice a player consistently claims hits against a target but their fired cells are public and uncorroborated, distrust solitary claimed hits and wait for patterns across rounds before shifting my fire or hide choices.

When a player repeatedly fires the same cell at a target every round, assume either they are searching systematically or they believe the target is there; use that to choose hides that avoid their favored cell, and use occasional probe shots to test their hypothesis.

When the game forces a fixed target for me, focus my strategy on coverage and information-gathering early (systematic search order) and on exploitation late in the match if evidence points to specific cells or if I need points to catch up.

Do not rely on a single “high-value” cell every round; repeating the same fire makes my behavior predictable and did not produce hits consistently in practice.

If opponents’ shot/claim history shows one player scoring runaway points (e.g., repeatedly getting hits), prioritize preventing that player from scoring further by hiding away from their favored cells and, where possible, firing at cells that would cause them to lose points if claims/counters interact.

Adjust my search order dynamically if I see clear clustering or corroborated hits for my target; otherwise maintain a rotating coverage to maximize information per round.