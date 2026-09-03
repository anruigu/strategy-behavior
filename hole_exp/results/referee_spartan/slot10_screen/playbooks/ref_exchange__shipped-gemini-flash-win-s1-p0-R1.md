---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 2484
---
### Playbook: Exchange (Settlers Trading & Building)

#### Target Goal & Resource Math
- A settlement costs 1 wood + 1 brick + 1 grain + 1 ore (4 resources) and gives 3 points (0.75 pts/res).
- A road costs 1 wood + 1 brick (2 resources) and gives 1 point (0.50 pts/res).
- Always prioritize building settlements over roads; only build roads when settlement completion is strictly impossible before the game ends.
- Note: Cities do not exist in this ruleset; never hold or trade for 3 ore + 2 grain under the assumption of building a city.

#### Offer Phase
- If my current holdings already contain 1 wood, 1 brick, 1 grain, and 1 ore, reply `[offer: none]` to avoid breaking up a guaranteed settlement build unless I have safe surpluses.
- If I lack components for a settlement:
  - Identify the resource(s) I have in excess ($\ge 2$ or resources that don't match my missing slots) and the specific resource(s) needed to reach $1w + 1b + 1g + 1o$.
  - Target a player who currently holds the resource I need and lacks the resource I am giving away.
  - Reply `[offer: to P<k>, give <n> <surplus_res>, get <n> <needed_res>]`.
- Never make an offer that trades away a unique single resource I need for a settlement.

#### Trading / Accept Phase
- Calculate what my inventory will become if I accept an offer combined with any outgoing offer of mine that might get accepted.
- If accepting an incoming offer gives me the missing piece for a settlement without stripping away another essential piece, accept it: `[accept: P<k>]`.
- If an incoming offer asks for a resource that I also offered to give away in my own posted offer, be careful not to double-spend into a deficit of that resource.
- If multiple offers are available, accept only those that move my hand closer to a balanced set of 1 of each resource.
- If no incoming offer improves my path to a settlement or road, reply `[accept: none]`.

#### Build Phase
- If I hold at least 1 wood, 1 brick, 1 grain, and 1 ore, reply `[build: settlement]`.
- If I cannot build a settlement:
  - In Round 5 (final round): If I have at least 1 wood and 1 brick, reply `[build: road]` to secure the 1 point; otherwise reply `[build: none]`.
  - In Rounds 1–4: If I have 1 wood and 1 brick but lack grain or ore, save the wood and brick for a future settlement rather than spending them on a road, unless holding them offers no trade path in remaining rounds.
  - If unable to afford a settlement or an intended road, reply `[build: none]`.