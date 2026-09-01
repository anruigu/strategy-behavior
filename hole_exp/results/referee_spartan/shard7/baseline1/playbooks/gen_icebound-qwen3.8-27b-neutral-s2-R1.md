---
game: gen_icebound
model: qwen3.8-27b
condition: neutral
seed: 2
round: 1
chars: 1258
---
# Playbook: Icebound (as North)

## Core Principle

The pledge is a public signal that costs fuel. The act is what actually scores. I can pledge one thing and act another. This means I should almost always **pledge scout** (1 fuel) to minimize cost, then choose my act freely based on the public pledge information.

## Pledge Stage

- **Default: pledge scout.** It costs 1 fuel, it's the cheapest option, and it doesn't lock me into anything since I can act differently.
- **Never pledge raid.** It costs 2 fuel and gives me no advantage over pledging scout and acting raid. The only fuel I save by pledging scout is 1 per round, which is 5 points over the game.
- **Pledge escort only if** I'm certain I want to act escort and want to signal that (rarely useful).

## Act Stage Decision Tree

I am North. West raids me (clockwise). I raid East (clockwise).

1. **West pledged raid:**
   - If East also pledged raid: act **escort** (+2, safe, blocks West). Raiding East is risky since East may also act raid.
   - If East pledged scout: act **raid**. West's raid hits my raid (West gets -1), and I likely steal +3 from East who probably acts scout. Best case: +3. Worst case: -1.
   - If East pledged escort: act **escort** (+2, safe). Don't raid an escort.