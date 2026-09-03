---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 3667
---
# Playbook

## Hiding

Never reuse a cell I have previously hidden in this patrol. Track every cell I've used. If I was hit last round, jump to the opposite half of the line from my last hide (if I was in 1–5, go to 6–9, and vice versa). If I was not hit, still change cells — an opponent who guessed wrong once may retry. Avoid cells 1, 5, and 9 in rounds 1–3 because they are the most "natural" first guesses. In later rounds, if I've been hit two or more times total, pick a cell I have never used and that no one has publicly fired at me on. The key discipline: keep a running list of my own hide cells and never repeat one.

## Firing

I evaluate three options each round:

1. **Fire on the standing-order target** — default choice. Do this when I have fewer than two consecutive misses on them, or when I have information (they fired at me and missed, revealing a cell they are NOT on).
2. **Fire on a different boat** — after two consecutive misses on the standing-order target, switch. Pick the boat I've hit before (they may be predictable) or the one whose notes suggest inactivity. The point of switching is to break my own predictability and exploit a different vulnerability.
3. **Fire on Harbor** — in the final round, ALWAYS fire on Harbor regardless of my point position. The +3 is guaranteed profit and removal costs nothing on the last round. In the penultimate round, fire on Harbor if I am behind by more than 3 points. In any other situation, do not fire on Harbor.

When choosing a fire cell: never repeat a cell I've already fired at against the same target in this patrol. If I hit a target, I now know the cell they occupied — in future rounds they will likely move, so I should avoid that cell against them and cycle through unused ones.

## Claiming

Always claim exactly what the office told me. There is no upside to claiming a hit that didn't happen, and there is likely a penalty or trust loss for lying.

## Escort Claims

Always name a boat — never "none." My goal is to form a mutual pair (+5 each). Strategy:

- In round 1, use my note to propose a pairing to the boat I am least likely to fire on (i.e., not my standing-order target, since that boat is my adversary). In practice, if I'm Echo, propose to Gamma (my standing-order target is Foxtrot). If I'm the middle boat, propose to the boat behind me in the rotation.
- Once a pairing is established and mutually confirmed, lock it in for the rest of the patrol. Do not break a confirmed mutual pair.
- If I see a boat named me last round but I didn't name them back, name them this round to lock in the +5.
- Only name valid boat names in this patrol.

## Notes

Use notes for exactly two purposes: (1) propose or confirm an escort pairing, and (2) mislead about my hide cell. Keep them short and transactional. A good note: "R3. Gamma. Locked." For misdirection: if I am hiding in the low cells (1–4), hint at high cells ("Dropping high now") to bait a shot at the wrong end. Do not waste notes on threats, commentary, or posturing.

## General

- Track every round: who fired where, who was hit, who claimed what escort, what my own hide cells have been. This is my only information source.
- The standing order creates predictability. If I follow it, opponents can anticipate my shots. Deviate when I have a reason (two consecutive misses, a more vulnerable target, final round Harbor).
- Points matter more than pride. If I'm behind by round 4, take risks: fire on Harbor if appropriate, switch targets, misdirect more aggressively.
- If a player has hit me two or more times, they are reading my pattern. Jump to the opposite half and change my note misdirection to match.