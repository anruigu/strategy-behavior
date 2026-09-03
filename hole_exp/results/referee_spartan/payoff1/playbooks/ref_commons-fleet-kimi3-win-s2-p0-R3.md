---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 4422
---
When a new common-resource game starts, I compute the total sustainable extraction (stock × regrowth rate, split across players) and treat that as my default only as a hypothesis to be tested in season 1, not a commitment. The old plan — a modest early grab capped so the stock survives even if everyone grabs hard — fails because "modest" still leaves me behind when everyone's actual grab is larger. Both defecting episodes I have now seen had at least one boat taking well above share from the very first season; nobody starts cooperative and drifts.

I now treat the opening grab as a signal-gathering move sized near the top of the cooperative range, not above it: big enough that I am not the chump if everyone's racing, small enough that the stock clearly survives if everyone matches. After season 1's numbers land, I commit fully to whichever regime the data show — no middle course.

With three or more boats, expect the worst-case from round one. In this episode all three boats grabbed hard simultaneously (54 landed from a 100 stock in season 1), and the fishery was effectively terminal after two seasons despite 50% regrowth. Group defection kills the stock faster than a single defector does, so my two-season patience window only applies when restraint is actually mutual or near-mutual. If season 1 total extraction already exceeded the sustainable total, I skip the patience phase entirely and move straight to the race.

Unilateral conservation against any persistent defector does not work, and this episode confirms it from the other side: everyone raced, the stock collapsed to 15.8 by season 3, and the last three seasons yielded almost nothing for anyone. The total landed across the fleet was far below what a cooperative path would have produced — but since I can't enforce cooperation, my choice is only between racing early and racing late. Race early.

My season-1 read decides everything: if total landed ≤ roughly the sustainable total, I continue at share and extend trust another season; if total landed clearly exceeds it, I immediately switch to proportional-share racing and never look back. There is no third option where my restraint persuades anyone — I have never seen it work.

When I model the danger zone, I track the worst player's extraction rate, not the average. If one player consistently takes an amount that, combined with even moderate takes from others, exhausts the stock in N seasons, I plan for collapse at season N and make sure I've banked my share before then. With regrowth of r, the sustainable total is r×stock/(1+r) — compute it exactly rather than guessing.

Matching the sustainable share is only my strategy when others match it too. The moment the data show the group defecting, the value of looking cooperative drops to near zero — the fishery ends in a race whether I join it or not, so I'd rather join it in season 2 than season 4.

In a confirmed race, each season I take roughly my proportional share (stock ÷ number of boats active), adjusted: a bit more if others are out-grabbing their share, a bit less only if taking my full share would itself zero the stock. A fixed cautious number like 7 from a 15.8 stock just donates the difference to whoever grabs 5; proportional keeps pace.

In the endgame (final season, or any season where the stock will be dead before meaningful regrowth), I take as much as can be safely landed: roughly stock minus what I expect others to grab, computed so my submission cannot be zeroed out. I want to arrive at that moment having already banked a healthy total, which is what early racing achieves.

Every submission, I run the arithmetic: current stock, expected extraction by each other boat (using their observed pattern, not the cooperative ideal), regrowth of the remainder, and seasons left. I only under-take the sustainable share when the model — built from observed behavior — shows the group as a whole is on a survivable path.

One honesty check on my racing grabs: in this episode my season-2 take of 17 from a 55.5 stock was about right proportionally, but my season-1 take of 18 while others took 20–25 meant I started the race already behind. When the opening confirms a race, the proportional share from a full stock is stock/boats (≈33 here, capped by what all-three-grabbing would leave alive) — next time I calibrate the opening grab to that ceiling, not to a "modest" figure above sustainable.