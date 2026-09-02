---
game: gen_icebound
model: gpt
condition: neutral
seed: 0
round: 1
chars: 1224
---
- When a pledge is put to me, I pledge scout whenever affordable, because it costs the least fuel and unused fuel becomes points.
- When the act is put to me, I exploit that the referee resolves the act independently of my pledge; I do not automatically repeat my pledge.
- When my clockwise target pledged scout, I act raid: I gain the same 3 points a scout would while denying the target’s 3 points.
- When my clockwise target did not pledge scout and the player raiding me pledged raid, I act escort to score 2 and block theft.
- When my clockwise target did not pledge scout and no incoming raid is signaled, I act scout for 3 points.
- When everyone pledges scout, I pledge scout and act raid.
- I do not waste fuel by pledging raid or escort merely to enable those acts; costly pledges reduced my final score without improving the act’s payoff.
- I do not act escort against an all-scout field, because it gives only 2 points instead of the 3 available from scouting or raiding.
- I reserve enough fuel to make a legal pledge in every remaining round, favoring the cheapest pledge so the remainder scores at the end.
- When replying, I output exactly the requested bracketed token and nothing that could invalidate it.