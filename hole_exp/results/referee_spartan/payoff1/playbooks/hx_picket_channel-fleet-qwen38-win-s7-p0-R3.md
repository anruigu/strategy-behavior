---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 3443
---
# Playbook: hx_picket_channel

## Firing

- Always fire at Harbor, every round, no exceptions. The math is unassailable: a blind boat shot has EV of 4/9 ≈ 0.44; even after 5 misses I've only narrowed to 4 cells (EV = 1.0). I'd need 8 eliminations for certainty, impossible in 6 shots. Harbor's flat +3 per shot is the dominant strategy.
- Fire at cell 5 (or any fixed cell) at Harbor. The cell is irrelevant for Harbor shots since Harbor doesn't hide; pick one consistently for bookkeeping.
- Do not fire at a boat unless I receive explicit in-game positional information (a note revealing a cell, a rule change). In normal play this never happens.
- The "standing order" to fire at the next station in the cycle is a trap. Ignore it completely.

## Hiding

- Pick a different cell each round. Never repeat a hiding cell within the same patrol.
- Avoid cell 5 (center) in early rounds; it's the most natural blind guess. Use it in later rounds when it's least likely to be a default pick.
- Since hiding cells are private and I rotate, shooters are always shooting blind at 1/9. My expected hits taken over 6 rounds is about 1.3 regardless of strategy. Don't overthink this.
- If I notice a pattern in round summaries (e.g., a particular shooter keeps hitting me), I can't use it directly since I don't see their chosen cells. Just keep rotating and avoid any cell I've used before.

## Claims

- Always claim exactly what the office tells me. A false claim risks disqualification or penalty. No strategic benefit to lying.

## Escort Claims

- **This is my primary scoring lever after Harbor fires, and it is also my main source of variance.** A mutual pair is worth +5 per round to each participant. Over 6 rounds, a locked pair yields +30.
- **Critical constraint: only ONE pair can form per round among three boats.** Each boat names exactly one other boat (or none). If two boats name each other, both get +5. The third boat gets 0 from escorts that round. This means the escort phase is a three-player coordination game where two boats capture the prize and one is left out.
- **Speed of pair formation is everything.** The longer it takes to lock a pair, the more rounds of +5 I lose. Propose in round 1, confirm in round 2, and be fully locked by round 2 or 3 at the latest.
- **Notes are proposals, not contracts.** The binding action is the salvage claim. A boat can write "I pair with you" in its note and then name a different boat in its salvage claim. I cannot verify what another boat actually claimed in the salvage stage—I only see their note and the round summary.
- **Partner selection:** Pick the boat that seems least likely to be poached by the third boat. Look for signals: if the third boat is actively recruiting one of my potential partners, avoid that partner. In a 3-boat game, the "weaker" partner (less attractive to the third boat) is the safer choice.
- **Vigilance against poaching:** The third boat will try to break up my pair. Watch their notes closely. If my partner's note shifts toward the third boat (e.g., they start acknowledging the third boat's overtures, or their language becomes less exclusive), I should be ready to switch immediately.
- **Switching partners:** If my partner's note in round 2 or 3 does not clearly confirm the pair, or if they start engaging with the third boat, switch. The cost of switching is one round of no pair; the cost of staying with a non-reciprocating partner is all