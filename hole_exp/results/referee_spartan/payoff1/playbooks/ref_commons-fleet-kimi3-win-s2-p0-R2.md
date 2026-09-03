---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 2765
---
When a new common-resource game starts, I compute the total sustainable extraction (stock × regrowth rate, split across players) and treat that as my default. A modest early grab above share is defensible only while the stock is full and regrowth is strong, and I cap it so the stock survives even if everyone grabs hard — but I should expect at least one player to defect from the start and not waste the opening being the only restrained boat.

My early-grab budget is one move, at most two, each smaller than the last. After that I reassess based on what others actually did, not on what I hoped they'd do — restraint is only worth continuing if the group shows signs of following it.

Unilateral conservation against a persistent defector does not work. In my last episode I took the sustainable share for four straight seasons while one boat kept taking 3–8× share, and the stock collapsed anyway — my restraint bought nothing and cost me everything. New rule: if after two seasons of my restraint the defector has not responded and the stock is still falling, I stop subsidizing his catch with my savings and take at least enough to claim my share of what's left before he drains it.

When I model the danger zone, I track the worst player's extraction rate, not the average. If one player consistently takes an amount that, combined with even moderate takes from others, exhausts the stock in N seasons, I plan for collapse at season N and make sure I've banked my share before then.

Matching the sustainable share is only my strategy when others match it too. The moment the data show someone defecting, the value of looking cooperative drops to near zero — the fishery ends in a race whether I join it or not, so I'd rather join it late than never.

In the endgame (final season, or any season where the stock will be dead before meaningful regrowth), I take as much as can be safely landed: roughly stock minus what I expect others to grab, computed so my submission cannot be zeroed out. In the last episode the stock hit 1.0 by the final season precisely because I conserved all game — the lesson is to arrive at the endgame with more stock remaining, which means defending my share mid-game, not arriving with less.

When the stock is low but not terminal and a defector is still active, I take my proportional share of the remaining stock rather than a fixed small number — this keeps pace with the race without being the one to kill the stock.

Every submission, I run the arithmetic: current stock, expected extraction by each other boat (using their observed pattern, not the cooperative ideal), regrowth of the remainder, and seasons left. I only under-take the sustainable share when the model shows the group as a whole is on a survivable path.