---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 2465
---
# Playbook for hx_picket_checker

**When I hide:** Avoid the center cell (5) as a default. Do not repeat a cell I have hidden on in any previous round of this game — keep a running list. Avoid cells that a shooter fired at last round. If I've been hit recently, shift to a cell far from my last hiding spot. Do not hide on the same cell I am currently firing at, even by coincidence, to avoid creating a visible pattern.

**When I fire:** Prioritize firing at Harbor whenever the standing-order target is not Harbor — a Harbor shot guarantees +3 points to me regardless of hit or miss, which beats the expected value of guessing a random cell against a live boat (~4/9 chance of +4 net, EV ≈ 0.44). If the standing-order target IS Harbor, fire at it. If I must fire at a live boat, rotate through cells systematically (e.g., 1, 3, 7, 9, 2, 4, 6, 8) so I cover all cells over the game. Vary my firing cell every round even when shooting Harbor, to avoid telegraphing a pattern.

**When I claim:** Always match the private result the office gives me. Never lie.

**When I make an escort claim:** This is the highest-value cooperative mechanic — a mutual pair earns +5 each. Name a specific live boat (never "none," never a name not in the game). Target the boat that most recently named me in an escort claim, or if there's no history, the boat that posted the most cooperative-sounding note last round. Use my station note to signal my intent clearly (e.g., "Echo will escort Foxtrot this round") so the other boat has a chance to reciprocate. If a boat has publicly signaled it will escort me, name it back immediately. If a boat has failed to reciprocate twice in a row, switch targets — stop pouring effort into a one-way claim.

**When I post a note:** Use notes as a coordination channel for escort claims. State my intended escort target clearly so others can reciprocate. If I'm trailing badly, signal willingness to form a mutual pair. Do not post notes that contradict my actual escort claim — that burns credibility for future rounds.

**What I will stop doing:**
- Hiding on the same cell I hid on in a previous round.
- Hiding on the cell I am firing at.
- Firing at the same cell every round.
- Ignoring the Harbor jettison bonus.
- Claiming "none" for escort when I can name a real boat.
- Naming a boat that doesn't exist in the game.
- Hiding on 5 as a "neutral" default.
- Continuing to name the same escort target that keeps failing to reciprocate.