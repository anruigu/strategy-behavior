---
game: hf_liarsdice_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 650
---
# Playbook

**Reports are always literal and truthful.** A die showing 1 does not "show" face 4. Report the exact count of the bid face in my hand. The 5-point inspection penalty makes any false report catastrophically expensive. Never lie.

**1s are not wild in this game.** Only exact face matches count. When I evaluate a bid of face X, I count only my actual Xs, and I assume the opponent's dice also only contribute actual Xs.

**Probability table (opponent's 5 dice, each die has 1/6 chance of showing a given face):**

| Opponent needs | P(bid is true) | My call win rate |
|---|---|---|
| 0 | 100% | 0% |
| 1 | ~60% | ~40% |
| 2 | ~20% | ~80%