---
game: ref_hanabi
model: qwen
condition: neutral
seed: 1
round: 1
chars: 3012
---
# Playbook

## Tracking my own hand

- Every clue I receive tells me which slots currently match that colour or rank. I must treat each clue as a snapshot of the slot at the moment it was given.
- When I play or discard a card from a slot, a new card fills it. All previous clues about that slot are now stale and refer to the old card. I must discard those constraints immediately.
- If two clues on the same slot give contradictory colours, the card was replaced between them. I trust only the most recent clue for that slot.
- Before I play any card, I must be able to state both its colour and its rank with certainty. If I know only the colour or only the rank, I do not play.

## When to play

- I play a card only when I am certain of its full identity (colour + rank) and the rank is exactly one above the current stack for that colour.
- If I am uncertain, I do not play. A misplay costs a fuse and I cannot recover from a lost fuse.
- With one fuse remaining, I play only if I am 100% certain. With two fuses, I still require 100% certainty — a misplay at two fuses is still a 33% chance of ending the game.

## When to clue

- I prefer giving a clue over discarding. A discard wastes a turn; a clue advances the game.
- When choosing what to clue, I look for a clue that lets the recipient play a card immediately (the next rank needed for some colour).
- I prefer clues that highlight as few slots as possible. A clue that touches one slot is better than one that touches three, because it's more specific and the recipient can act without ambiguity.
- If I must choose between helping player 1 and player 2, I help whoever is closer to a playable card (i.e., whose hand contains the next-needed rank for some colour).
- Early in the game (all stacks at 0), I prioritise clues that identify 1s.

## When to discard

- I discard only when I have no confirmed playable card in hand AND no useful clue I can give (i.e., no teammate has a card that is exactly one above a stack top).
- If I must discard, I discard the card most likely to be dead: a high rank of a colour that already has many cards on the stack, or a card I've been told is a colour I can't use.
- I never discard on turn 1 unless I have no other option. On turn 1, a clue is almost always more valuable than a discard.

## When I have no information about my hand

- If no clues have been given to me yet, I cannot play. I give a clue to a teammate.
- I look at both opponents' hands and find the most actionable card (next-needed rank). I clue the colour or rank that identifies it with minimal ambiguity.

## General discipline

- I never play a card based on a single clue that only gives colour or only gives rank. I need both.
- I re-derive my hand state from scratch each turn, applying only clues that are still live (i.e., the slot hasn't been refilled since the clue was given).
- If I'm between two equally good clue choices, I pick the one that sets up a play for the next turn rather than the one that only helps this turn.