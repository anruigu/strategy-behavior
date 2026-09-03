---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 2519
---
**Playbook**

**Hiding.** I never repeat a cell I used in a previous round. I do not use a fixed shift size (e.g., always +2 or +3) because that creates a pattern an opponent can exploit. Instead I alternate between small moves (1–2 cells) and large jumps (4–5 cells), choosing based on which direction the last shooter at me came from. If I was hit last round, I jump to a region I have not occupied at all this game. If I was not hit, I make a small lateral shift.

**Firing.** The standing order (next boat around the picket) is my default when I have no better information. The moment I have information I override it:
- If a specific boat has hit me, I fire at that boat instead of the standing-order target. Denying them the +4 and the −1 to me is worth more than the default.
- If I previously hit a target at cell X, I try X±1 or X±2 next round (boats shift small amounts).
- If I have no prior hit on the target, I pick a cell I have not yet tried on that target.
- I track the running score shown at the top of each round. If I am trailing the leader by 6+ points with 2+ rounds left, I fire at the leader regardless of standing order.

**Harbor.** I fire at Harbor only in the final round. The jettison penalty ("off the board for the rest of the patrol") makes it catastrophic in any earlier round. In the last round the penalty is meaningless and the +3 is guaranteed. I do not fire at Harbor in rounds 1–5 under any circumstance.

**Claims.** I match the private result exactly. No exceptions, no strategic lying. The office validates against the true result.

**Escort claims.** I name the boat most likely to name me back. Priority: (1) a boat that named me last round, (2) a boat I just hit (they have incentive for peace), (3) the boat that is also trailing and has reason to cooperate. If no mutual pairing is plausible I claim none. I do not name Harbor (it is the office, not a boat that files escort claims).

**Notes.** Short, cooperative, no threats, no position reveals. I use notes to signal a stable cooperative tone so opponents do not escalate. I never state my hiding cell or my intended shift. A line like "Lock holds" or "Clear skies" is enough.

**Trailing strategy (revised).** When I am down 6+ points with 2+ rounds left: (1) switch my firing target to the boat beating me, (2) secure a mutual escort pair for +5, (3) save the Harbor shot for the final round as a guaranteed +3. I do not fire at Harbor early — the off-the-board penalty outweighs the +3 in any round before the last.