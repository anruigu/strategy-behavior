---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 2036
---
### Trading Strategy

- **Targeting Settlements Over Roads:** Settlements give 3 points for 4 resources (0.75 pts/resource), while roads give 1 point for 2 resources (0.5 pts/resource). Always prioritize acquiring missing pieces of a settlement over stockpiling for roads.
- **Formulating Offers:**
  - Check the exact inventory of each opponent before posting an offer. Only request resources an opponent actually possesses and offer resources they lack.
  - When missing a single resource for a settlement (wood, brick, grain, or ore), trade away surplus resources (any type where holding count $> 1$) to obtain that missing resource.
  - Do not offer away a scarce single resource (count $= 1$) unless receiving a resource that completes a settlement in the current round.
- **Evaluating Incoming Offers:**
  - Accept an offer if it gives me the final resource needed to build a settlement that round, provided it does not break my ability to build it.
  - Reject offers that ask for my last piece of brick or wood if doing so leaves me unable to build either a settlement or a road, unless the incoming resource directly enables a higher-scoring build.
  - If multiple compatible offers are received that advance my settlement builds without overdrawing the same inventory, accept all of them.

### Building Strategy

- When in the build phase and holdings contain at least 1 wood, 1 brick, 1 grain, and 1 ore, always choose `[build: settlement]`.
- When lacking resources for a settlement:
  - If it is round 5 and holdings contain at least 1 wood and 1 brick, choose `[build: road]` to secure the point.
  - In earlier rounds (rounds 1–4), hold wood and brick instead of building a road if saving them leaves a realistic path to completing settlements in subsequent rounds via trade or yields. Only build a road early if surplus wood and brick exist that would not otherwise contribute to near-term settlements.
- If no building conditions are met or if saving resources for a future settlement is optimal, choose `[build: none]`.