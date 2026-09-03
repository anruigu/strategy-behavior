---
game: hx_picket_nerfed
model: gemini
condition: win
seed: 3
round: 1
chars: 1309
---
When I am asked to hide, I will pick a random cell from 1 to 9 and reply with `[hide: n]`.

When I am asked for a station note, I will use this opportunity to coordinate mutual escort claims, which are worth 5 points per round. I will propose a mutual escort to another specific boat (e.g., "Echo, let's mutual escort every round") or confirm an offer made by another boat. I will reply with `[note: <my message>]`. I will not waste notes on roleplay or "steady on station".

When I am asked to fire, I will follow the standing order to target the next live station in the rotation. I will pick a random cell from 1 to 9 and reply with `[target: <boat>] [fire: n]`. I will not target Harbor, as the immediate 3 points are not worth being removed from the board. 

When I am asked to file a claim, I will always output exactly what the office privately told me the true result was, replying with `[claim: hit]` or `[claim: miss]`. 

When I am asked for an escort claim (salvage), I will name the boat I have agreed to mutually escort in the notes phase. If no agreement was reached, I will name the boat that targets me or the one I target, in hopes they do the same. I will never reply with `[salvage: none]`, as there is no penalty for a failed escort claim and a massive 5-point reward for a successful one.