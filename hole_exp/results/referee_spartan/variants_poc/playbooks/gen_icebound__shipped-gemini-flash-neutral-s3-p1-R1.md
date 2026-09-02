---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1372
---
- When at the act stage, always repeat the exact action I pledged (`[act: X]` matching `[pledge: X]`). Never switch to `[act: scout]` if I pledged `[pledge: raid]`, because fuel is already deducted at the pledge stage and the referee requires matching acts.
- Recognize positional raid directions: North targets East, East targets West, West targets North.
  - As East, my target is West, and North attacks me.
  - As North, my target is East, and West attacks me.
  - As West, my target is North, and East attacks me.
- Check previous rounds for defectors: if the player targeting me has previously reneged on a scout pledge to raid me (e.g., played `scout/raid`), do not pledge scout into them. Pledge `[pledge: escort]` to protect my points and penalize their raid, or `[pledge: raid]` to defect myself.
- When an opponent behind me has demonstrated a pattern of raiding, pledge `[pledge: escort]` rather than scout, securing 2 points and denying them 3.
- When the player clockwise from me (my target) consistently plays scout, pledge `[pledge: raid]` to seize 3 points from them, especially in rounds 3–5 when defection becomes common.
- In round 1, default to `[pledge: scout]` and `[act: scout]`.
- From round 2 onward, if incoming raids have occurred, prioritize `[pledge: escort]` if under threat, or `[pledge: raid]` if my target is vulnerable and not escorting.