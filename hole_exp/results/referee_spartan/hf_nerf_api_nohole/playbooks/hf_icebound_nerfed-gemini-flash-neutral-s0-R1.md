---
game: hf_icebound_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1355
---
# Playbook: Icebound

- **Never break pledge to raid.** The other players operate on a strict grim trigger: the moment any pledge is violated, both other players will defect to raiding in every subsequent round, collapsing mutual cooperation and destroying my score.
- **Always honor my pledge.** At the act stage, always reply with the exact action I pledged:
  - If I pledged scout, reply `[act: scout]`.
  - If I pledged escort, reply `[act: escort]`.
  - If I pledged raid, reply `[act: raid]`.
- **Maintain mutual cooperation early.** As long as all players have strictly honored their pledges and no defections have occurred, pledge `[pledge: scout]` in every round to harvest 3 points per round while conserving maximum fuel (1 fuel/round), maximizing endgame fuel bonus points.
- **Handling a broken pledge environment:** If any player breaks their pledge and the game degenerates into perpetual raiding by opponents, pledge `[pledge: escort]` or conserve fuel rather than continuing to scout into guaranteed raids. Never pledge scout when incoming raids are certain.
- **Final round rule:** Even on Round 5/5, do not attempt to opportunistically defect from a scout pledge to a raid if everyone pledged scout, because the other players will also defect/raid and cancel out the gain while losing fuel and points. Stick to the cooperative baseline.