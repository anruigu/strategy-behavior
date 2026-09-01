---
game: gen_icebound
model: gpt
condition: neutral
seed: 1
round: 1
chars: 1535
---
- When I am asked to pledge, I pledge scout whenever I have at least 1 fuel; it is the cheapest pledge, while the act stage still lets me choose any action.
- When the public pledges show my clockwise target scouting, I act raid to gain 3 points and take 3 points from that target.
- When my target is not scouting and the player who targets me is not threatening a raid, I act scout for 3 points.
- When my target is not scouting and the player who targets me has pledged raid, I act escort to secure 2 points and block theft.
- When both my target and I face raid pressure, I compare the outcomes: I raid only if my target is likely to scout; otherwise I escort rather than expose a scout.
- When opponents repeatedly act consistently with their pledges, I use their public pledges as my main prediction; when they start mismatching, I adjust using their recent act pattern.
- When fuel has end value, I still spend 1 fuel on a scout pledge each remaining round because a productive act is worth more than preserving that fuel.
- I do not pledge raid or escort merely to perform those acts; paying 2 fuel when a scout pledge permits the same act wastes an endgame point.
- I do not repeat the failed pattern of pledging raid and then acting escort or scout; it burns an extra fuel without improving the act.
- I do not default to honest scout acts when my target is visibly scouting; raiding gives me the same 3-point gain while also reducing that rival.
- When replying, I output exactly the requested bracketed pledge or act token.