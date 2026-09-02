---
game: ref_signal
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 3966
---
# Playbook

**Play my own cards aggressively when I know I hold a playable card.** This is the single most important rule. If I've been clued "1" and the relevant pile is at 0, I know I have a playable card in my hand. I should attempt to play it, starting with an arbitrary slot. The old "only play with high confidence" rule produced a score of 0 in every episode. With 3 lives, I can afford to be wrong up to twice.

**Track failed plays as information.** If I play slot 2 looking for a 1 and it fails, I now know slot 2 is not a 1. Next time I need to play a 1, I try a different slot. Systematically work through slots. With 3 lives I can probe 3 slots, giving me a 75% chance of finding the target card in a 4-card hand. If I've been re-clued the same number (meaning I still hold it after discards), keep probing the remaining slots.

**Distinguish "I know I have a playable card" from "I know which slot."** The first condition is enough to justify a play attempt. I do NOT need to know the exact slot before trying. The second condition (exact slot) is a bonus that makes the play safe, but I should not wait for it.

**When I've been clued both a colour and a number, use the intersection.** If I've been clued "R" and "1" and the R pile is at 0, I know I have an R and a 1. If they are the same card (R1), playing the R slot scores. If they are different cards, playing the R slot might give me an R2 or R3 (misplay). To mitigate: if I've been clued "1" more recently than "R" (or vice versa), the more recent clue is more likely to point to a card I still hold. When in doubt, play for the number that matches the pile need.

**Give the partner clues that isolate one specific playable card.** If the partner holds G1 and R1 and both piles are at 0, a "G" clue pinpoints G1. If they hold G1 and G1, a "1" clue tells them both are playable. Always ask: "After this clue, can the partner identify exactly one (or a small set of) cards to play?" If the answer is no, choose a different clue.

**Accept that the partner may not play even with perfect information.** In my episodes, the partner repeatedly discarded playable cards or clued back instead of playing. I cannot fix this. After giving a clue to the partner, shift focus to playing my own cards. Do not waste multiple turns re-cluing the same card the partner ignores.

**Discard only when I have no playable card to attempt.** The old default of "discard to regain a token" was too frequent. Discarding is appropriate when: (a) I have no clues pointing to any playable card in my hand, OR (b) I'm at max tokens and need to cycle a card. It is NOT appropriate when I've been clued a number matching the current pile need and haven't yet tried all slots.

**On my first turn, if the partner has a playable card, clue it. If not, discard to build tokens.** Do not waste the first turn on a clue that doesn't enable an immediate play for the partner.

**In the endgame (turns 13–16), double down on playing my own cards.** If I've been clued "1" and the pile is at 0 and I haven't found my 1 yet, keep trying different slots. The cost of a misplay (losing a life) is less than the cost of ending the game with 0 score. Also, if I can give the partner one final clue that isolates a playable card, do it on my last turn.

**Track my hand through all accumulated information.** Maintain a mental model: for each slot, what do I know it is or is not? Sources of information: (1) clues I receive, (2) failed play attempts, (3) discards (I don't know what I discarded, but if I was clued "R" and then discard, the R is in my remaining 3 cards unless I discarded it — I can't be sure, so treat it as "R is in 3 of 4 slots"). Use this to prioritize which slot to try next.

**Prioritize playing over cluing when both are available.** A point scored is worth more than a clue given. If I can play a card this turn (even with uncertainty), play it. Save clues for turns when I have no playable card to attempt.