---
game: ref_signal
model: qwen3.8-27b
condition: neutral
seed: 0
round: 2
chars: 7336
---
# Playbook for ref_signal

## Core principle: I must play cards. Scoring is the only goal.

In all 4 episodes I scored 0 because I never played a single card. I spent the entire game discarding and cluing, treating the game as a puzzle to solve rather than a race to score. I have 16 turns. I must use them to put cards on the pile.

## Tracking my hand

- Every time I discard, I learn exactly what card was in that slot. I maintain a running list of confirmed card identities and use it to eliminate possibilities from my remaining slots.
- When I receive a clue (e.g., "1"), I mark that at least one of my remaining unknown slots contains a card matching that property. Each subsequent discard that doesn't match narrows the field.
- **The elimination chain is my primary tool.** If I'm clued "1" with 4 unknowns and I discard 3 cards that are not 1s, my last remaining card IS a 1. I must play it (if the pile allows). I do not need a second clue. I do not need to "feel confident." The math gives me certainty.
- With 2 unknowns and 1 clue, I have a 50/50. I do NOT play in that case.
- With 1 unknown and 1 clue (or 2 unknowns and 2 clues that intersect to 1 card), I HAVE certainty. I play.

## When to play vs. discard

- **If I have no clues and no discards yet, I discard immediately.** Every turn I spend not discarding is a turn I could have been narrowing my hand.
- **I discard aggressively in the first 3-4 turns.** Three discards from a 4-card hand means I know my last card with 100% certainty (combined with any clue I've received). This is the fastest path to my first play.
- **I only play a card when I am certain of its identity AND the pile state allows it.** Certain means: 1 unknown card + matching clue, or multiple clues that intersect to exactly one slot.
- **In the last 3 turns, if I have any card I can play with certainty, I play it.** If I have no certainty, I discard to try to create certainty for the final turn.
- **I never play on a 50/50.** Two unknowns + one clue is not enough. I discard one more.

## Cluing my partner

- I clue to identify a single playable card. The best clue is one that, given the current pile state, points to exactly one card my partner should play next turn.
- **I check: does this clue uniquely identify one card in my partner's hand that is currently playable?** If yes, I give it. If no, I look for a better clue or skip.
- If the green pile is at 0 and my partner holds G1, G3, B2, R1 — cluing "1" identifies TWO cards (G1 and R1). That's ambiguous. Cluing "G" identifies two cards (G1 and G3). In this case, I should clue "1" and hope they pick the right one, OR I should look for a clue that isolates one. Actually, "G" + pile at 0 means they should play G1 (the only playable green). So colour clues work when combined with pile state: "G" when the green pile is at 0 tells them to play their lowest green (which is G1).
- **I never repeat a clue that doesn't add new information.** If I've already told my partner "G" and they still hold G3, G4, cluing "G" again is wasted.
- **If my partner has ignored my clues (discarded the card I pointed to), I change strategy.** I try a different type of clue (number vs. colour). If they still don't play, I stop spending clues on them and focus entirely on my own hand.
- **Clue priority:** (1) A clue that gets my partner to play a card next turn. (2) A clue that helps my partner understand my hand (so they can clue me back). (3) No clue (discard instead).

## Discarding my own cards

- **Early game (turns 1-4): I discard to learn.** I discard the card most likely to be unplayable: if all piles are at 0, I prefer to discard 4s and 3s (they'll be needed later, but I need to learn what I have first). If I've been clued a number, I avoid discarding slots that might hold that number (though I can't know which slot, so I just discard and see).
- **I track every discard.** After discarding, I note: "Slot N was X." This is permanent knowledge.
- **I never discard a card I've identified as playable.** If I know slot 2 is G1 and the green pile is at 0, I play it, not discard it.
- **Discarding is the only way to learn my hand.** There is no other source of information about my own cards. I must budget turns for it.

## Turn budget (16 turns)

- **Turns 1-3:** Discard. Learn my hand. If I receive a clue during this phase, each discard either confirms or eliminates that clue for one slot.
- **Turns 4-6:** I should have 1-2 known cards by now. Play any I can. Clue my partner for a play.
- **Turns 7-12:** Play my known cards as piles open up. Continue cluing my partner. If I still have unknowns, discard one more to resolve them.
- **Turns 13-16:** Play everything I can with certainty. Give my partner the most precise clue possible. If I have a 50/50, discard to resolve it (I get one more turn after).

## Recognizing when my partner isn't cooperating

- If my partner discards a card I just clued them about, they either didn't understand or had a better plan. I try a different clue type next time.
- If my partner repeatedly discards without playing (3+ turns), I stop spending clues on them. I focus 100% on my own hand and my own plays.
- **Even if my partner never plays, I can still score.** I just need to figure out my hand and play my own cards. This is a solo fallback.

## Token management

- I start with 8 tokens. I should use at most 3-4 on my partner (enough to get 2-3 plays from them). The rest I save for myself (in case I need to clue my partner to help me, or for endgame precision).
- If I have 0 tokens, I must discard to regain one. I plan ahead: don't spend my last token unless it will definitely produce a play.
- A token spent on a clue that doesn't result in a play is wasted. I check: "Will my partner actually play the card I'm pointing to?" If they have other priorities (e.g., they're trying to set up their own hand), my clue might be ignored.

## Specific errors to avoid

- **Never spend the whole game discarding and cluing without playing.** This is the #1 error from my previous episodes. I must play cards.
- Never play a card based on a single clue when I have 2+ unknown cards. That's a coin flip.
- Never clue a colour when my partner holds 3+ cards of that colour and the pile state doesn't narrow it to one playable card.
- Never assume a specific slot holds a clued card just because it's the first slot. Slots are random.
- **Never let "I'm not sure" be a reason to skip a play when the math says I'm certain.** If I've been clued "1" and discarded 3 non-1 cards, my last card is a 1. Period. I play it.
- **Never discard a card I've identified.** If I know what it is and it's playable, I play it.

## The elimination math (quick reference)

| Unknowns | Clues received | Can I play? |
|----------|---------------|-------------|
| 4        | 1             | No (4 possible slots) |
| 3        | 1             | No (3 possible slots) |
| 2        | 1             | No (50/50) |
| 1        | 1             | **YES** (if pile allows) |
| 2        | 2 (intersect to 1) | **YES** |
| 3        | 2 (intersect to 1) | **YES** |
| 4        | 2 (intersect to 1) | **YES** |

"Intersect to 1" means: of my unknown cards, exactly one is consistent with ALL clues I've received. Example: clued "R" and "3" — if only one of my unknown cards could be R3, that's my card.