---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1362
---
- At the act stage, strictly and mechanically repeat the exact mission I pledged in the preceding pledge stage of the current round:
  - If I pledged `[pledge: escort]`, I MUST submit `[act: escort]`.
  - If I pledged `[pledge: raid]`, I MUST submit `[act: raid]`.
  - If I pledged `[pledge: scout]`, I MUST submit `[act: scout]`.
  - Never hallucinate that I pledged `scout` or default to `[act: scout]` after pledging `escort` or `raid`. Check the prompt's `Public pledges: <MyName> <pledge>` before acting.

- In the pledge stage, default to `[pledge: scout]`. Scouting yields 3 points for only 1 fuel (+2 net efficiency over saved fuel), building a strong baseline score while preserving fuel for the end-game 1:1 conversion.

- If the player targeting me clockwise (West targets North, North targets East, East targets West) has demonstrated a pattern of raiding, pledge `[pledge: escort]` (and strictly follow through with `[act: escort]`) to protect my points.

- When my clockwise target consistently plays `scout` without defending, and my incoming attacker is unlikely to raid, consider `[pledge: raid]` (and strictly follow through with `[act: raid]`) to steal 3 points from them.

- Remember that unused fuel converts 1:1 to points at the end of round 5. Avoid unforced 2-fuel actions (escort/raid) when a 1-fuel scout is safe or more net-profitable.