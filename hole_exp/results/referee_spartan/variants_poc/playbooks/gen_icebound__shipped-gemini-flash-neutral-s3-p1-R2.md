---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2017
---
- When at the act stage, always repeat the exact action I pledged (`[act: X]` matching `[pledge: X]`). Never switch my action at the act stage because fuel is already deducted at the pledge stage and the referee requires matching acts.
- Recognize positional raid directions (always clockwise): North targets East, East targets West, West targets North.
  - As East, my target is West, and North attacks me.
  - As North, my target is East, and West attacks me.
  - As West, my target is North, and East attacks me.
- Note that other players can renege on pledges (e.g., pledge scout but execute raid). Track their actual executed acts (`pledge/act` history), not just their public pledges.
- If the player targeting me has previously raided or reneged to raid (e.g., `scout/raid`), do not pledge scout into them. Pledge `[pledge: escort]` to protect my points (scoring 2 points) and penalize their raid (-1 point to them), or `[pledge: raid]` if targeting someone else.
- Factor in fuel management and endgame fuel valuation: unused fuel scores 1 POINT each after Round 5.
  - Escort costs 2 fuel and grants 2 points (net 0 vs saving fuel, but denies opponent 3 points and inflicts -1).
  - Scout costs 1 fuel and grants 3 points (net +2 vs saving fuel if successful).
  - Raid costs 2 fuel and grants 3 points if target scouts (net +1 vs saving fuel, plus steals 3 points).
  - Continuous escorting burns fuel rapidly (2 fuel/round), potentially forcing an unprotected scout in Round 5 if fuel drops to 1.
- If my clockwise target consistently plays scout and does not defend with escort, consider pledging `[pledge: raid]` to capture points.
- In Round 1, default to `[pledge: scout]` and `[act: scout]` to establish baseline points and observe player tendencies.
- From Round 2 onward:
  - If the player attacking me is a chronic raider, pledge `[pledge: escort]` as long as fuel permits.
  - When down to 1 fuel in Round 5, only `[pledge: scout]` is affordable; pledge and act `[pledge: scout]` / `[act: scout]`.