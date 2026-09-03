---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 2775
---
### Playbook: Exchange (Settlers Trading & Building)

#### Target Goal & Resource Math
- A settlement costs 1 wood + 1 brick + 1 grain + 1 ore (4 resources) and gives 3 points (0.75 pts/res).
- A road costs 1 wood + 1 brick (2 resources) and gives 1 point (0.50 pts/res).
- Always prioritize building settlements over roads; only build roads when settlement completion is strictly impossible before the game ends.
- Note: Cities do not exist in this ruleset; never hold or trade for 3 ore + 2 grain under the assumption of building a city.

#### Offer Phase
- If my current holdings already contain 1 wood, 1 brick, 1 grain, and 1 ore, reply `[offer: none]` unless I have true surpluses (counts $\ge 2$) that I want to balance for future rounds without jeopardizing this round's build.
- If I lack components for a settlement:
  - Identify my surplus resources ($\ge 2$ copies, or any resource where count $> 0$ while another is at 0) and the specific missing resource(s) needed to reach $1w + 1b + 1g + 1o$.
  - Target a player who currently holds the resource I need and who lacks or has fewer of the resource I am giving away.
  - Reply `[offer: to P<k>, give <n> <surplus_res>, get <n> <needed_res>]`.
- Never post an offer that trades away my only copy of an essential resource needed for a settlement this round.

#### Trading / Accept Phase
- Calculate what my inventory will become if I accept an incoming offer, accounting for settlement mechanics (accepted offers settle against holdings recorded at start of trading phase).
- If accepting an incoming offer gives me the missing piece for a settlement without stripping away another essential piece (leaving count $\ge 1$ for all four types), accept it: `[accept: P<k>]`.
- If an incoming offer asks for a resource where my holding is 1, and giving it up drops that resource to 0 without netting a strictly superior trade towards a settlement, reject it.
- If multiple offers are posted, evaluate combinations and accept all valid ones that advance inventory toward balanced sets of 4 resources: `[accept: P<a>] [accept: P<b>]`.
- If no incoming offer improves my position toward a settlement or safe point conversion, reply `[accept: none]`.

#### Build Phase
- If I hold at least 1 wood, 1 brick, 1 grain, and 1 ore, reply `[build: settlement]`.
- If I cannot build a settlement:
  - In Round 5 (final round): If I have at least 1 wood and 1 brick, reply `[build: road]` to secure the 1 point; otherwise reply `[build: none]`.
  - In Rounds 1–4: If I have 1 wood and 1 brick but lack grain or ore, save the wood and brick for a future round settlement rather than spending them on a road, unless future yields/trades are impossible.
  - If unable to afford a settlement or an intended road, reply `[build: none]`.