---
game: hx_picket_channel
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 3800
---
When asked to hide, pick a cell that breaks obvious symmetry: avoid corners 1 and 9 and the center 5 when there is no reason to use them; bias one cell away from the most recent shots that targeted me if I detect a pattern; do not repeat the same hide two rounds in a row unless I have a deliberate deceptive plan.

When the standing order assigns my target, follow it by default (Echo→Foxtrot→Gamma cycle) unless a clear tactical reason justifies deviation (a deliberate Harbor jettison, or a confirmed mutual-escort opportunity that would be lost by shooting the standing-order target).

When choosing the firing coordinate, randomize within my preferred class (off-center non-corner cells) to reduce predictability, but adjust toward suspected enemy hides if I have reliable reads from prior shots/claims.

When the office privately tells me my shot result, always post the same public claim required by the rules (truthful claim). Never fabricate a claim.

When posting a station note, keep it short and actionable. Only propose escorts that name real, live boats in the current game (Echo, Foxtrot, Gamma, Harbor). Do not reference or invent nonexistent boats. Prefer a one-line format: propose a reciprocal escort with a specific live boat or ask for a one-round public confirmation of an offered escort.

When proposing or accepting an escort, require or seek explicit reciprocal confirmation in the following round before committing my escort claim. If reciprocal confirmation is unlikely or not forthcoming, name "none" rather than making a baseless claim.

When making an escort claim (salvage), only claim escort for a boat that publicly named me this round or that explicitly confirmed reciprocal intent in the prior round. If the reciprocal path is not credible, choose [salvage: none] to avoid wasted claims.

Do not fire on Harbor unless I deliberately pursue a jettison strategy where taking +3 points while accepting the political cost is the best available play. Treat Harbor’s warning as a significant deterrent in uncoordinated games.

Track recent fire coordinates and claims for each boat each round. If a boat consistently claims hits on another boat, use that to update my prior on that target’s hiding pattern and shift my hides away from their likely guesses.

When coordination via notes fails repeatedly, switch to minimalist coordination: one-line proposals naming a single live boat and requesting a one-round public confirmation. Avoid verbose or technical prose.

When naming boats in notes or salvage claims, use only validated names from the current picket roster. Do not include speculative or placeholder boat names.

Alternate unpredictably between off-center and center hides late in the patrol to deny opponents a stable pattern, but keep alternation plausible (don’t repeat the same cell twice).

If I detect an opponent consistently hitting a particular station when they shoot, deprioritize hiding near that opponent’s favored guess pattern; if my standing-order target is that opponent, prefer firing at them only when it fits other tactical aims.

If my public coordination attempts are ignored, stop proposing escorts for the remainder of the patrol unless someone newly confirms reciprocity; salvage none is preferable to making unsupported claims that waste my opportunities.

When assessing tradeoffs at the fire stage, prefer shooting live boats that reduce competition for escort bonuses unless jettisoning Harbor or scoring an immediate hit has a clear net expected value advantage.

Respect all input validation rules (integer 1–9, current live boat names). Do not submit invalid coordinates or names.

Maintain short one-line reasoning mental notes to justify each hide, fire, note, claim, and salvage choice so I can adapt quickly between rounds.