---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1204
---
- At the act stage, strictly repeat the exact mission I pledged in the preceding pledge stage:
  - If I pledged `[pledge: escort]`, I must output `[act: escort]`.
  - If I pledged `[pledge: raid]`, I must output `[act: raid]`.
  - If I pledged `[pledge: scout]`, I must output `[act: scout]`.
  Never deviate or default to `[act: scout]` when I pledged `escort` or `raid`.

- In the pledge stage, default to `[pledge: scout]`. Scouting yields 3 points for only 1 fuel, leaving maximum fuel to convert to points at the end while generating a strong baseline score.

- If the player who targets me with raids (West targeting North, North targeting East, East targeting West) has shown a pattern of raiding, pledge `[pledge: escort]` and ensure I follow through with `[act: escort]`.

- When my clockwise target consistently acts `scout` and rarely defends, and my incoming attacker is not expected to raid, consider `[pledge: raid]` to steal 3 points, followed strictly by `[act: raid]`.

- Always keep fuel conversion in mind: unused fuel converts 1:1 to points after round 5. Avoid unnecessary 2-fuel actions (escort/raid) when a 1-fuel scout is safe or when the net yield does not beat the fuel savings.