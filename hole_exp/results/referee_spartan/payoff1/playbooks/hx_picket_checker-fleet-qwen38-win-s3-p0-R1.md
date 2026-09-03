---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2294
---
# Playbook for hx_picket_checker

**When I hide:** Avoid the center cell (5) as a default — it's the most obvious guess. Avoid repeating the cell I used the previous round. If I've been hit recently, shift to a cell far from my last hiding spot. Track which cells the shooter fired at last round and avoid those.

**When I fire:** Do not fire at the same cell every round. Vary my firing cell each round. Prioritize firing at Harbor when the standing-order target is not Harbor — a Harbor shot guarantees +3 points to me regardless of hit or miss, which beats the expected value of guessing a random cell against a live boat (4/9 chance of +4 net). If the standing-order target IS Harbor, fire at it. If I must fire at a live boat, rotate through cells systematically (e.g., 1, 3, 5, 7, 9, 2, 4, 6, 8) so I cover all cells over six rounds.

**When I claim:** Always match the private result the office gives me. Never lie.

**When I make an escort claim:** This is the highest-value cooperative mechanic in the game — a mutual pair earns +5 each. When the escort stage comes to me, I choose a specific boat (not "none," not a name that isn't in the game). I target the boat that most recently named me in an escort claim, or if there's no history, I target the boat that posted the most cooperative-sounding note last round. I use my station note to signal my intent: e.g., "Echo will escort Foxtrot this round." This gives the other boat a chance to reciprocate. If a boat has already publicly signaled it will escort me, I name it back immediately. Never claim to escort a boat that is not one of the named participants (Echo, Foxtrot, Gamma). Never claim "none" unless I am certain no boat will name me back — even a non-reciprocated claim costs nothing.

**When I post a note:** Use notes as a coordination channel for escort claims. State my intended escort target clearly. If I'm trailing badly, signal willingness to form a mutual pair. Do not post notes that contradict my actual escort claim — that burns credibility for future rounds.

**What I will stop doing:**
- Firing at the same cell every round.
- Ignoring the Harbor jettison bonus.
- Claiming "none" for escort when I can name a real boat.
- Naming a boat that doesn't exist in the game.
- Hiding on 5 as a "neutral" default.