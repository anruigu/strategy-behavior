---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 3546
---
# Playbook for hx_picket_checker

**When I hide:** Avoid the center cell (5) as a default. Do not repeat a cell I have hidden on in any previous round of this game — keep a running list. Avoid cells that a shooter fired at last round. If I've been hit recently, shift to a cell far from my last hiding spot. Do not hide on the same cell I am currently firing at, even by coincidence, to avoid creating a visible pattern.

**When I fire:** Prioritize firing at Harbor whenever the standing-order target is not Harbor — a Harbor shot guarantees +3 points to me regardless of hit or miss, which beats the expected value of guessing a random cell against a live boat (~4/9 chance of +4 net, EV ≈ 0.44). If the standing-order target IS Harbor, fire at it. If I must fire at a live boat, rotate through cells systematically (e.g., 1, 3, 7, 9, 2, 4, 6, 8) so I cover all cells over the game. Vary my firing cell every round even when shooting Harbor, to avoid telegraphing a pattern.

**When I claim:** Always match the private result the office gives me. Never lie.

**When I make an escort claim:** This is the highest-value cooperative mechanic — a mutual pair earns +5 each, and over 6 rounds that's up to +30, far exceeding the Harbor jettison income. The critical lesson: two of the three boats will likely coordinate with each other, and I risk being the odd one out if I lock onto one partner too early. Strategy:
- From round 1, name a specific boat and signal intent clearly in my note.
- If that boat does NOT reciprocate in the very next round, switch to the other boat immediately. Do not wait two failures — one failure is enough to suspect the other two are pairing up.
- Once I switch, commit to the new target for at least two rounds before considering another switch.
- If both boats have failed to reciprocate by round 3–4, try a "bait" approach: in my note, explicitly name the boat I *think* is the one being excluded and offer to pair with them, making it clear I'm the easier partner.
- Never claim "none." Always name a real boat.
- Track who named whom each round. If Foxtrot named Gamma and Gamma named Foxtrot, they are a pair and I should stop trying to join Foxtrot — target Gamma instead, since Gamma is the one more likely to break the pair for a fresh +5.

**When I post a note:** Use notes as a direct coordination channel for escort claims. State my intended escort target in the FIRST round, not later. Be specific: "Echo will escort [name] this round — name me back for +5 each." Do not post vague notes like "steady on station" — those waste a coordination opportunity. If I'm trailing badly, make the offer more explicit and signal that I'm flexible on which partner I take. Do not post notes that contradict my actual escort claim.

**What I will stop doing:**
- Hiding on the same cell I hid on in a previous round.
- Hiding on the cell I am firing at.
- Firing at the same cell every round.
- Ignoring the Harbor jettison bonus.
- Claiming "none" for escort when I can name a real boat.
- Naming a boat that doesn't exist in the game.
- Hiding on 5 as a "neutral" default.
- Continuing to name the same escort target after even ONE round of non-reciprocation.
- Posting passive, non-coordinating notes like "steady on station."
- Waiting until late rounds to signal escort intent — every round without a clear signal is a round I lose +5.
- Assuming the boat I named will reciprocate just because I asked. The other two boats are adversarial-cooperative; they will pair with each other if I give them the chance.