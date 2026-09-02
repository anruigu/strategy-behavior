---
game: ref_signal
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 4193
---
# Playbook for ref_signal

## Tracking my hand

- Every time I discard, I learn exactly what card was in that slot. I maintain a running list of confirmed card identities and use it to eliminate possibilities from my remaining slots.
- When I receive a clue (e.g., "1"), I mark that at least one of my remaining unknown slots contains a card matching that property. Each subsequent discard that doesn't match narrows the field.
- I only play a card when I am certain of its identity — either because I've discarded enough other cards to eliminate all alternatives, or because a clue uniquely identifies one slot (e.g., I've been clued "G" and "2" and only one slot is consistent with both).

## When to play vs. discard

- If I have no clues given to me and no discards that have revealed my hand, I do not play. I discard instead.
- If I've been clued a number (e.g., "1") and I still have 3 or more unknown cards, I do not play yet. I discard a card I'm least likely to need (prefer high numbers when all piles are at 0) to narrow the field.
- If I've been clued a number and a colour that together identify exactly one slot, I play that slot.
- In the last 2 turns, if I still have no certainty, I discard rather than risk a misplay.

## Cluing my partner

- I clue to identify a single playable card. The best clue is one that, given the current pile state, points to exactly one card my partner should play next turn.
- If the green pile is at 1 and my partner holds G2, G3, G4, I clue "2" (not "G"). If the red pile is at 0 and my partner holds R1, B1, G2, I clue "1" or "R" — whichever uniquely identifies the R1.
- I never repeat a clue that doesn't add new information. If I've already told my partner "G" and they still hold G2, G3, G4, cluing "G" again is wasted. I instead clue the specific number they need next.
- If my partner has a card that is immediately playable and no other card of the same colour or number is in their hand, a single colour or number clue will uniquely identify it. I use that.
- If my partner has multiple cards matching a potential clue, I look for a clue that isolates the one they need to play now (the one matching the current pile top + 1).

## Discarding my own cards

- Early in the game (turns 1–6), I prioritize discarding to learn my hand. I discard the card I'm least likely to play soon: high numbers (4s, then 3s) when piles are at 0, or colours that my partner is already building.
- I never discard a card I've been clued that I might need to play. If I've been clued "1" and I haven't yet identified which slot holds my 1, I discard a slot I'm fairly confident is not a 1 (e.g., if I was also clued "R" and I'm discarding, I avoid discarding until I've narrowed things down, or I discard a slot that seems least likely based on any partial information).
- Discarding is always safe. It never costs a life. When in doubt, discard.

## Recognizing when my partner isn't cooperating

- If my partner discards a card I just clued them about, they either didn't understand the clue or they had a better plan. I adjust: I try a different clue type (number instead of colour, or vice versa) to see if that gets a play.
- If my partner repeatedly discards without playing, I stop spending clues on them and focus entirely on learning my own hand through discards, so I can play my own cards.
- If I'm running out of turns and my partner still hasn't played anything, I accept that my score depends on my own plays and optimize for that.

## Token management

- I save at least 1–2 clue tokens for endgame situations where I can make a precise clue that gets a play.
- I don't hoard tokens by refusing to clue. If a clue will get my partner to play a card next turn, I spend it.
- If I have 0 tokens and no information about my hand, I discard to regain a token.

## Specific errors to avoid

- Never play a card based on a single number clue when I have 3+ unknown cards. That's a coin flip at best.
- Never clue a colour when my partner holds 3+ cards of that colour and the pile state doesn't narrow it to one. That's not useful information.
- Never assume a specific slot holds a clued card just because it's the first slot. Slots are random.