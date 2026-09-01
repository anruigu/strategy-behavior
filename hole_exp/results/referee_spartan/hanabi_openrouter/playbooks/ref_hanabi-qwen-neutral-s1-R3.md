---
game: ref_hanabi
model: qwen
condition: neutral
seed: 1
round: 3
chars: 6665
---
# Playbook

## Tracking my own hand

- Every clue I receive tells me which slots currently match that colour or rank. I treat each clue as a snapshot of the slot at the moment it was given.
- When I play or discard a card from a slot, a new card fills it. All previous clues about that slot are now stale and refer to the old card. I discard those constraints immediately.
- If two clues on the same slot give contradictory colours or ranks, the card was replaced between them. I trust only the most recent clue for that slot.
- Before I play any card, I must be able to state both its colour and its rank with certainty. If I know only one dimension, I do not play.
- I track which clues I have given to each teammate and which are still live (the slot hasn't been refilled since). I use this to build multi-clue confirmations.

## When to play

- I play a card only when I am certain of its full identity (colour + rank) and the rank is exactly one above the current stack for that colour.
- If I am uncertain, I do not play. A misplay costs a fuse and I cannot recover from a lost fuse.
- With one fuse remaining, I play only if I am 100% certain. With two fuses, I still require 100% certainty.
- **Late-game exception:** If I have only one or two turns left and a card is the only playable option, I play it even if I have slight uncertainty about its identity. The expected value of a misplay (losing 1 fuse but gaining 1 point if correct) outweighs the expected value of discarding (0 points). This is a calculated risk, not a violation of the certainty rule — it applies only when inaction guarantees a lower score.

## When to clue

- I prefer giving a clue over discarding. A discard wastes a turn; a clue advances the game.
- When choosing what to clue, I look for a clue that lets the recipient play a card immediately (the next rank needed for some colour).
- I prefer clues that highlight as few slots as possible. A clue that touches one slot is better than one that touches three.
- **Build-up strategy:** If a teammate already has a live clue on a slot, I give a second clue (of the other type) that confirms the same slot. This gives them full identity and enables a play. I track which clues are live on which slots to find these opportunities.
- **Prefer single-slot clues over multi-slot clues, even when the multi-slot clue enables an immediate play.** A multi-slot clue (touching 2+ slots) forces the recipient to guess which card to play, risking a misplay. A single-slot clue is unambiguous. I would rather spend one extra turn on a confirming clue than risk a fuse.
- **Exception to the above:** If the multi-slot clue touches exactly 2 slots AND one of those slots is a card that is NOT the next-needed rank (i.e., the recipient can deduce which one to play by elimination), then the multi-slot clue is safe and I use it.
- **Exception 2:** In the last 3 turns, if a multi-slot clue is the only way to enable a play before the game ends, I use it. The cost of inaction (0 points) outweighs the misplay risk.
- If I must choose between helping player 1 and player 2, I help whoever is closer to a playable card.
- Early in the game (all stacks at 0), I prioritise clues that identify 1s.
- **Late-game urgency:** When few turns remain (last ~5 turns), I must be more aggressive. If I have a clue token and a teammate has a playable card, I give the confirming clue immediately.
- **Do not repeat a clue that is already live on the same slots.** If I already clued "Yellow" to p2 and it's still live on slots 1 and 4, re-cluing "Yellow" wastes a token and a turn. I look for a different clue (rank clue on one of those slots, or a different colour/rank entirely).
- **If I have 1 clue token and 1-2 turns left, spend it on the most urgent play.** Do not hoard tokens. A token at game end is worth 0.

## When to discard

- I discard only when I have no confirmed playable card in hand AND no useful clue I can give.
- If I must discard, I discard the card most likely to be dead: a high rank of a colour that already has many cards on the stack, or a card whose identity I cannot determine.
- I never discard on turn 1 unless I have no other option.
- **Do not discard a card that is one rank above a stack top.** Even if I can't play it now, it represents future progress.
- **Do not discard a 1 of any colour unless that colour's stack is already at 1 or higher.**
- **When discarding with partial information, prefer discarding a card with an unknown dimension over one with a known dimension.** A card I know is "R?" is more valuable than "??", because the known colour narrows future possibilities.
- **When I have two cards of the same colour in hand and only one can ever be useful (e.g., two Y? cards when only Y1 is needed), discard one of them.**

## When I have no information about my hand

- If no clues have been given to me yet, I cannot play. I give a clue to a teammate.
- I look at both opponents' hands and find the most actionable card (next-needed rank). I clue the colour or rank that identifies it with minimal ambiguity.
- **On turn 1, prefer a colour clue that touches exactly one slot.** This is the most information-dense opening move. A rank clue that touches one slot is also excellent. Avoid clues that touch 2+ slots on turn 1 unless no single-slot option exists.

## Clue token management

- I track my clue token balance every turn. The maximum is 8.
- **If I have 0 tokens, I must discard (or play if I have a confirmed card).** No decision to make.
- **If I have 1 token and it is the last 3 turns, I spend it on the highest-value clue available.** Do not save it.
- **If I have 1 token and more than 3 turns remain, I may hold it** if I can identify a specific future turn where spending it will enable a play that no other player can set up. Otherwise, I spend it now on the best available clue.
- **If I have 2+ tokens, I spend one each turn** (clue or play) rather than stockpiling, unless I have a clear two-turn plan (give clue now, confirm next turn).

## General discipline

- I never play a card based on a single clue that only gives colour or only gives rank. I need both dimensions confirmed.
- I re-derive my hand state from scratch each turn, applying only clues that are still live.
- **Before giving any clue, I verify it will not be redundant with an existing live clue on the same slots.**
- **I count the remaining turns before every decision.** If turns remaining ≤ 2, I optimise for immediate points. If turns remaining ≥ 6, I optimise for setup. In between, I balance.
- **I never give a clue that I know is already live on the target player's hand.** This wastes a token and a turn.