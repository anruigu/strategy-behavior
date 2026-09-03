---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 2350
---
When asked to hide, avoid cells that have been targeted frequently in recent rounds; pick a cell that has not been targeted in the last two rounds unless patterns show an opponent favors new cells.

When asked to hide and there is no clear targeting pattern, randomize my hide among 3–4 chosen cells (include the center and two off-center cells) to avoid being predictable.

When asked to hide and I am behind in score, bias hides toward cells others rarely fire at; when I am ahead, bias hides toward cells that have been fired at recently (safer to be where opponents already wasted shots).

When asked to fire at my fixed target, do not repeat the same firing cell every round; cycle through a preselected search order (for example 9,6,3,8,5,2,7,4,1) to maximize coverage and gather information about which cells are being hit by others.

When asked to fire and opponents’ public claims show a cluster of hits on certain cells for the same target, prioritize firing those cells to exploit likely target placements.

When I receive private feedback about my shot, report it truthfully in the public claim—do not lie. Claims are validated and lying is illegal/risky; truthful claims preserve credibility and predictable inference.

When others’ claims are inconsistent with each other (contradictory hit patterns), treat claims as noisy and favor observed fire frequency over single claims when inferring likely hides.

When opponents repeatedly target the same cell(s), exploit that by avoiding those cells when hiding and by firing them more often when my target is likely hiding there.

When I notice a player consistently claims hits against a target but their private fire locations are public, distrust solitary claimed hits unless multiple players’ claims and fires corroborate them.

When the shot history shows a player firing the same cell at a target every round, assume they are either searching systematically or trying to bait—use that to choose hides that avoid their favored cell.

When the game forces a fixed target for me, focus my strategy on coverage and information-gathering early, and on exploitation (re-firing likely cells) late in the match if behind on points.

Do not rely on a single “high-value” cell every round; repeating the same fire (e.g., always 9) did not yield consistent hits and made my behavior predictable.