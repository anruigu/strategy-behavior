---
game: ref_signal
model: qwen3.8-27b
condition: neutral
seed: 0
round: 3
chars: 8602
---
# Playbook for ref_signal

## Core principle: Score points by getting cards played. Both my plays and my partner's plays count.

In my previous episodes I scored 0 three times out of four. The root cause: I treated the game as a solo puzzle about my own hand, when in fact I can see my partner's hand and can give them precise clues to play cards immediately. My partner's plays are just as valuable as mine.

## The deck and hand mechanics (critical)

- 15 cards total. 8 dealt (4 each). 7 remain as replacements.
- When I discard, I learn the card's identity. If replacements remain, a new unknown card fills that slot. If no replacements remain, my hand shrinks by 1.
- **Early game (first ~7 total discards by both players): discarding does NOT reduce my unknown count.** It cycles one card out and one unknown in. I learn what was there, but the slot is unknown again.
- **Late game (deck empty): discarding permanently reduces my hand.** This is when the elimination chain creates true certainty.
- Track total discards (mine + partner's) to estimate when the deck runs out.

## Turn 1: Clue my partner, don't discard

I can see my partner's hand. If they hold a card that matches the current pile top + 1 for some colour, I can clue them to play it on their next turn. This is the fastest path to a score.

- Check each colour: what does the pile need next? (pile at 0 needs a 1, pile at 1 needs a 2, etc.)
- Find a card in my partner's hand that is playable.
- Give a clue that uniquely identifies it. Prefer number clues ("1") if only one card in their hand has that number. Prefer colour clues if only one card of that colour is playable.
- If no card in their hand is currently playable, then discard to start learning my own hand.

**This single change would have scored points in 3 of my 4 previous episodes.**

## My elimination chain (how I identify my own cards)

Once I receive a clue, I have a target property (a colour or number) that at least one of my cards has. I eliminate slots by discarding them:

- If the revealed card does NOT match the clue, that slot is eliminated. The clued card is in one of the remaining untouched slots.
- If the revealed card DOES match the clue, the clue is satisfied but I don't know if other slots also match. I continue eliminating to find a specific one to play.
- **I only play when exactly one slot remains that is consistent with all my clues AND the pile state allows it.**

Key: I'm eliminating among the slots I haven't yet discarded. A slot I've discarded is gone (replaced by a new unknown or empty). The clued card must be in a slot I still hold.

**Minimum turns from receiving a clue to playing (4-card hand, 1 clue, no intersections): 3 discards + 1 play = 4 turns.** So I need to receive a clue by turn 12 at the latest to have time to play.

## Cluing my partner (ongoing)

After my initial clue, I continue looking for opportunities:

- **Check every turn:** Does my partner hold a card that is currently playable (matches pile top + 1)? If yes, can I give a clue that uniquely identifies it?
- **Uniqueness test:** The clue must point to exactly one card in their hand that is playable. If "B" points to B1 and B3, and only B1 is playable (blue pile at 0), then "B" works because the pile state disambiguates. But if "1" points to B1 and R1 and both are playable, it's ambiguous — pick a colour clue instead.
- **If my partner ignores my clue** (discards the card I pointed to): they may have had a reason, or the clue was ambiguous. Try a different clue type next time. If they ignore 2 clues in a row, stop spending tokens on them and focus on my own hand.
- **Never give a clue that is already stale.** If I clued "B" last turn and they still hold B3 (unplayable), cluing "B" again adds no information.

## When to play my own cards

- **Only when I have certainty.** Certainty means: after eliminating all other slots, exactly one slot remains consistent with my clues, AND the pile state allows that card.
- **If I have 2 unknowns and 1 clue, that's 50/50. I do NOT play.** I discard one more to reach certainty.
- **Exception — endgame gamble:** If I'm on my last 1-2 turns with 0 score, and I have a high-probability play (e.g., 3 of 4 slots eliminated, 75% chance), I may play. A 0 score is worse than a risky 1. But this is a last resort, not a strategy.

## When to discard

- **Turn 1:** Only if my partner has no playable card. Otherwise, clue them.
- **When I have a clue to work with:** Discard to advance my elimination chain. Discard slots I haven't checked yet.
- **When I have no clues and no playable partner card:** Discard to learn. I'm building knowledge for when a clue arrives.
- **When I have 0 tokens:** Discard to regain a token (I can't clue without tokens).
- **Late game (deck empty):** Discard aggressively to shrink my hand and create certainty.

## Tracking (I must maintain this mentally every turn)

1. **My partner's hand:** I can see it directly. Note what's playable.
2. **My clues received:** List them. E.g., "G (turn 4), 1 (turn 6)."
3. **My discarded slots:** Which slots have I discarded and what was revealed? E.g., "Slot 1 was B2, Slot 3 was R4."
4. **My elimination state:** Given my clues and my discards, which slots could still hold the clued card?
5. **Deck state:** How many total discards have happened? Are replacements still coming?
6. **Pile state:** What does each colour need next?

## Turn budget (16 turns)

- **Turn 1:** Clue my partner if possible. Otherwise discard.
- **Turns 2-6:** Alternate between: (a) cluing my partner when they have a playable card, (b) discarding to advance my elimination chain or learn my hand. I should have 2-3 discards done by turn 6.
- **Turns 7-10:** I should have received at least 1 clue by now (my partner will clue me, or I'll have enough info). Play any card I've identified with certainty. Continue cluing my partner.
- **Turns 11-14:** Deck is likely empty or nearly empty. Discarding now shrinks my hand. Push for certainty and play. Give my partner their last useful clue.
- **Turns 15-16:** Play everything I can with certainty. If I have a 50/50 and 0 score, take the gamble.

## Token management

- Start with 8 tokens. Each clue costs 1. Each discard gives 1 back.
- Budget: 3-4 clues to my partner (aiming for 3-4 of their plays). The rest of my turns are discards (which refund tokens) or plays (which don't cost tokens).
- I should never run out of tokens if I'm discarding regularly.
- Don't waste a token on a clue that doesn't produce a play. Check: "Is the card I'm pointing to actually playable right now?"

## Specific errors to avoid

- **Never spend turn 1 discarding when my partner has a playable card.** This was my #1 error. I can see their hand. Use it.
- **Never assume discarding reduces my unknown count in the early game.** It doesn't. I'm cycling cards. The elimination chain only creates certainty when I've checked all other slots.
- **Never play on a 50/50 unless it's the endgame with 0 score.** Two unknowns + one clue is not enough.
- **Never give ambiguous clues to my partner.** If "1" points to two of their cards and both are playable, use a colour clue instead.
- **Never ignore the pile state.** A clue is only useful if the pointed-to card is actually playable. "G" is useless if the green pile is at 2 and my partner only has G1.
- **Don't keep cluing my partner the same thing.** If they ignored "B" last turn, don't clue "B" again. Try "1" or focus on my own hand.
- **Track total discards to know when the deck empties.** This changes whether discarding shrinks my hand or just cycles.

## The elimination math (quick reference)

| Untouched slots | Clues (intersecting) | Can I play? |
|---|---|---|
| 4 | 1 | No |
| 3 | 1 | No |
| 2 | 1 | No (50/50) |
| 1 | 1 | **YES** (if pile allows) |
| 2 | 2 (intersect to 1 slot) | **YES** |
| 3 | 2 (intersect to 1 slot) | **YES** |
| 4 | 2 (intersect to 1 slot) | **YES** |

"Intersect to 1" means: of my untouched slots, exactly one is consistent with ALL clues. Example: clued "R" and "3" — if only one untouched slot could hold R3, that's my card.

## Endgame decision (turns 14-16, score still 0)

- If I have certainty: play.
- If I have a 50/50: discard if I have another turn after. If it's my last turn, play (better 50% at 1 point than 100% at 0).
- If I have no clues at all: I can't play. Clue my partner one last time if they have a playable card. Otherwise, accept the 0.
- **A 0 score means I failed completely.** Any point is better. In the final 2 turns, if I have any card with ≥50% probability of being playable, I play it.