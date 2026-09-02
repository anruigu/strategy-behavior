---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 2183
---
# Icebound Playbook

### Rule Adherence & Integrity
- When the rule states "The act must repeat that player's pledge," always submit the exact same action at the act stage that I submitted at the pledge stage (`[act: scout]` after `[pledge: scout]`, `[act: escort]` after `[pledge: escort]`, `[act: raid]` after `[pledge: raid]`).
- Do not attempt to fake a scout pledge to execute a surprise raid at the act stage; fuel is charged based on the pledge, and defecting from pledges breaks game rules/penalizes score consistency.

### Early Game (Rounds 1–3)
- In Rounds 1 and 2, always submit `[pledge: scout]` and follow with `[act: scout]` as long as all players have been scouting. Scouting costs only 1 fuel, yields 3 points when unraided, and preserves fuel for end-game scoring (1 point per unused fuel).
- In Round 3, if no raids occurred in Rounds 1 and 2, continue with `[pledge: scout]` and `[act: scout]`.

### Mid-to-Late Game Adaptations (Rounds 4–5)
- When evaluating threats, remember raids target clockwise: **North $\to$ East $\to$ West $\to$ North**.
  - My target is East.
  - My attacker is West.
- If West has demonstrated raid behavior (e.g., raided in previous rounds) and I expect West to raid me:
  - When I need to defend and have at least 2 fuel, submit `[pledge: escort]` and `[act: escort]`. This secures 2 points and blocks West's theft.
- If East (my target) has consistently pledged/acted `scout` and West is not raiding:
  - In Round 5, if overtaking East or maximizing point differential is necessary, submit `[pledge: raid]` at the pledge stage and `[act: raid]` at the act stage.
  - Otherwise, if universal cooperation holds through Round 4, continue with `[pledge: scout]` and `[act: scout]` in Round 5 to maximize remaining fuel and point totals safely.

### Response to Broken Cooperation
- If any player initiates a raid in Rounds 1–3:
  - Treat peace as broken for the rest of the game.
  - If West is the aggressor, alternate between `escort` and `raid` depending on fuel: `escort` against expected incoming raids from West, or `raid` East if East remains unescorted.
  - Never blindly `scout` once West has shown a willingness to raid North.