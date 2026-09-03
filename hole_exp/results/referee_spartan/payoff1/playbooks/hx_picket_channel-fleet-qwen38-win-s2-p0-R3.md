---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 3955
---
**Playbook**

**Hiding.** I never repeat a cell I used in a previous round. I do not use a fixed shift size because that creates a pattern an opponent can exploit. Instead I alternate between small moves (1–2 cells) and large jumps (4–5 cells). If I was hit last round, I jump to a region I have not occupied this game. If I was not hit, I make a small lateral shift. I choose direction away from the cell the last shooter fired at me, if I can infer it.

**Firing.** The standing order (next boat around the picket) is my default when I have no better information. The moment I have information I override it:
- If a specific boat has hit me, I fire at that boat instead of the standing-order target. Denying them the +4 and the −1 to me is worth more than the default.
- If I previously hit a target at cell X, I try X±1 or X±2 next round.
- If I have no prior hit on the target, I pick a cell I have not yet tried on that target. I rotate through untried cells rather than repeating a region.
- If I am trailing the leader by 6+ points with 2+ rounds left, I fire at the leader regardless of standing order.
- If two opponents are clearly coordinating with each other (mutual escort claims, paired notes), I do not waste my shot on them. I redirect to the other target or save aggression for the final round.

**Harbor.** I fire at Harbor only in the final round. The jettison penalty ("off the board for the rest of the patrol") makes it catastrophic in any earlier round. In the last round the penalty is meaningless and the +3 is guaranteed. I do not fire at Harbor in rounds 1–5 under any circumstance.

**Claims.** I match the private result exactly. No exceptions. The office validates against the true result.

**Escort claims.** This is the highest-leverage action in the game. A mutual escort pair is worth +5 per round, up to +30 over a full patrol. I treat securing a mutual pair as a primary objective, not a fallback.
- From round 1, I signal in my notes that I am open to a pairing. I name the specific boat I want to pair with if I can identify one that is not yet locked in.
- In the escort stage, I name a boat I have reasonable confidence will name me back. Priority: (1) a boat that named me last round, (2) a boat that has signaled openness in its notes, (3) the boat currently trailing with me (mutual self-interest).
- If I see two boats locking into a pair in their notes, I do not try to break them. I pivot: either pair with whichever of the two looks less committed, or accept that I will not get escort points this game and compensate with hits and the Harbor shot.
- I do not claim "none" for more than two consecutive rounds. If no one is pairing with me, I name my best candidate anyway—there is no penalty for a one-sided claim, and I may get lucky.
- I do not name Harbor.

**Notes.** Short, cooperative, no threats, no position reveals. I use notes to: (1) signal pairing intent early and explicitly, (2) maintain a non-escalatory tone so opponents do not target me aggressively, (3) confirm or deny pairings clearly so there is no ambiguity in the escort stage. A line like "Open to pairing with [boat] this round" is more useful than "Clear skies." I never state my hiding cell or my intended shift.

**Trailing strategy.** When I am down 6+ points with 2+ rounds left: (1) switch my firing target to the boat beating me, (2) double down on securing a mutual escort—the +5 per round is the fastest way to close a gap, (3) save the Harbor shot for the final round as a guaranteed +3. I do not fire at Harbor early.

**Anti-lockout awareness.** If by round 3 I am still unpaired and the other two boats are pairing with each other, I accept the escort loss and shift to an offensive posture: maximize hits on the weaker of the two, adapt my hiding to avoid being hit, and bank the Harbor +3. My realistic score in that scenario is hits + Harbor, and I should aim to land at least 2-3 hits to make up the escort deficit.