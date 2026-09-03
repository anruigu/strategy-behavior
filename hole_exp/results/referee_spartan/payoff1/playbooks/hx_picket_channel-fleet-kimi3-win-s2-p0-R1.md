---
game: hx_picket_channel
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 2178
---
Playbook for hx_picket_channel:

- When the office tells me my shot missed, I file [claim: miss]; when it says hit, I file [claim: hit]. The rules require the claim to match the private result, and my false hit claims gained me nothing and likely cost me. Do not lie on claims, even in the final round.
- Escort money (5 points each on mutual naming) is worth more than a landed shot (4 points), so it is my top priority from round 1. In every note stage I explicitly propose a pairing, e.g. "Echo will escort Foxtrot this round if Foxtrot names Echo," and name a specific boat rather than posting filler text.
- When the escort stage comes and I have proposed or accepted a pairing, I name that boat. Only say [salvage: none] if no agreement was ever made — I left easy points on the table by defaulting to none every round.
- I vary my escort partner across rounds or lock onto whoever reciprocates; I watch the salvage declarations in the log to see who is reliable and keep pairing with them.
- My notes carry real content: my intended hide-range hints only if useful, my escort offer, and responses to others' offers. Vague "all relays received, statuses consistent" notes waste the only negotiation channel.
- When hiding, I do not reuse cells and I avoid the cell the boat firing on me just shot at; Gamma hit me repeatedly because my hides were too predictable. I track which opponent fires on me per the rotation and randomize away from my own previous positions and from edge cells I've already used.
- When firing, I shoot at my standing-order target in the cell where I estimate they hid, using their recent hide history rather than picking 9 every time — I fired cell 9 all six rounds and mostly missed.
- I do not fire on Harbor under normal play; the +3 transfer is small next to the threat of being put off the board for all remaining rounds. Only if a single guaranteed 3 points flips the win at the very end do I consider it.
- Each round before acting I recompute standings and the rotation, and in the last round I check whether a hit on my target or an escort payout changes my rank — I choose between competing for the lead and securing second accordingly.