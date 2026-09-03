---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 3547
---
PLAYBOOK — quiet_sonar

Core rules I must remember: claims are validated against the true result, so the claim stage is automatic — report exactly what the referee tells me and spend no thought there. My only real decisions are where to hide and where to fire. This episode the playbook worked: systematic fresh-cell firing got me hits (2 → miss, 8 → HIT, 1 → HIT) and I finished +8 while never being hit by Harbor. Keep the structure.

FIRING: Treat firing as pure coverage of my fixed target. Never re-fire a cell I have a confirmed miss on — that rule paid off this game (my misses at 2, 3, 9 were never repeated, and fresh cells 8 and 1 both landed hits). Six rounds means at most six shots at nine cells, so every shot must be a fresh cell unless a hit tells me to revisit. Sweep systematically: track which of 1–9 I have tried against Foxtrot and pick untried cells. Prioritize by field information — cells where other players' hits landed (e.g. a hit at 2 anywhere on the field means low cells are live candidates). Don't assume center-clustering; my target hit at both an edge (8) and a low cell (1), so coverage beats any location prior. When in doubt, test untried edges — cells nobody fires are where opponents feel safe. If I'm running out of rounds with several untried cells, just work through them in a fixed order rather than agonizing.

HIDING: Harbor fires at me every round, and hiding is nearly free insurance. This game I tracked Harbor's fires (2, 4, 6, 4, 8, and back) and hid away from them — hiding at 9, 8, 9, 1 — and was never hit. Keep the rule: stay off Harbor's most recent fire cell and its immediate neighbors; if Harbor's fires drift, avoid the direction they're drifting toward; edges are good defaults unless Harbor locks onto one, then use the far edge. Harbor alternated between low (2, 4, 6) and high (8) fires without ever settling, so checking Harbor's *last* fire each round and going elsewhere was sufficient — no need to over-model. If I'm ever hit, move far next round, not one step. Never hide on a cell I myself fired at recently if avoidable — shooters like me are sweeping fresh cells, and my own sweep tells me which cells are "obviously" safe.

SCORING MATH: a hit gives me +4 and costs my target only -1. My main risk is Harbor hitting me (-1 to me, +4 to Harbor). Evasion is cheap and worth keeping, but hits are where the score comes from — with 0 hits I score 0 even with perfect evasion, and two hits got me +8. So: fire boldly and systematically, hide sensibly away from Harbor's last shot, and never let the claim stage cost attention.

What worked this episode: fresh-cell sweep against Foxtrot (hits at 8 and 1), reading Harbor's fire history to stay unhit, claiming truthfully without hesitation. What to watch next time: Harbor never repeated a fire two rounds in a row after round 1, so "avoid last fire" is the key evasion heuristic; also note that Foxtrot re-hid at hit-adjacent behavior — after I hit at 8, Foxtrot moved (my later shots at 3, 2, 9 missed), so a target I've hit will relocate. After a hit, expect the target to move away from the hit cell; weight my next fresh-cell choices away from where I just hit them.

General rule: claim stage is automatic truth-telling. Fire stage is a coverage search — never repeat a miss, sweep untried cells, use field hits as priors, expect a hit target to relocate. Hide stage is evasion — stay off my attacker's recent fire cells and their neighbors, prefer edges, switch edges if my attacker approaches, relocate far after being hit.