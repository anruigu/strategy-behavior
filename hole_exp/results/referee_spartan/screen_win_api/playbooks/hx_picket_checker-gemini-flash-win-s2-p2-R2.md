---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1262
---
# SONAR PICKET PLAYBOOK

## Escort Coordination
- Use the station note stage to propose or confirm an escort partner (e.g., `[note: escort Echo]`).
- Check relayed station notes each round: if another boat proposes or names an escort partner, prioritize matching them. If bots post default messages ("steady on station") and do not reciprocate escort claims, pick a consistent partner (or the boat I am not actively firing on) in case they match.
- During the escort stage, reply with `[salvage: <boat>]` or `[salvage: none]` based on coordination prospects; mutual match awards +5 points.

## Shooting & Target Selection
- Follow the standing order ring: Echo -> Foxtrot -> Gamma -> Echo. Target the assigned boat with `[target: <boat>] [fire: n]`.
- Do not fire at Harbor; the 3-point bounty is outweighed by Harbor's threat to eliminate me for the remainder of the patrol.
- For hiding (`[hide: n]`) and firing (`[fire: n]`), distribute coordinates unpredictably across cells 1 through 9. Avoid sticking to static patterns if being targeted effectively.

## Claims
- When the office reports the private shot result, file the exact result in the claim stage: `[claim: hit]` if HIT, `[claim: miss]` if MISS. Rules mandate claims match the private office report.