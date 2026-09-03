---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2241
---
PLAYBOOK — quiet_sonar

Core rules I must remember: claims are validated against the true result, so lying at the claim stage is impossible — never waste thought there. When I get a hit, I just claim hit. My only real decisions are where to hide and where to fire.

HIDING: Someone (Harbor) is always firing at me, and every point I lose comes only from being hit by Harbor. So I predict Harbor's fire, not the general field. In this game the field fired 5 over and over; if I see repeated identical fires, I never hide there. When fires are uniform, I hide on an edge (1 or 9). When fires start scattering, I hide where Harbor specifically has not fired recently. Keep changing my hide cell; if I was hit last round, definitely move, and move far (edge or corner), not just one step.

FIRING: I fire at the same target every round (Foxtrot), so I should build a model of that one player's hiding pattern. Do not just fire the crowd's favorite cell every round — I did that and got one hit out of six. Track which of my fires missed and never repeat a cell my target was confirmed absent from. Rotate among untried cells, favoring center-adjacent values first (4, 6, 5, then 2, 8), since opponents cluster near the middle. If my target keeps surviving in the middle cluster, sweep it systematically rather than re-firing the same miss.

SCORING MATH: a hit gives me +4 and costs my target only -1. My main risk is Harbor hitting me (-1 to me but +4 to Harbor). Avoiding being hit matters less for my own score than landing hits — -1 per hit taken is cheap. So I should be somewhat bold in firing, but hiding away from Harbor's fire pattern is nearly free insurance; keep doing it.

What did not work: firing the same cell round after round after a confirmed miss — pure information waste. Hiding at 2 repeatedly early on was also lazy; if I have no information, edges are fine but I should not sit still once fires are observed.

General rule: claim stage is automatic (tell the truth — it's forced anyway). Fire stage is a search problem: eliminate cells systematically against my fixed target. Hide stage is an evasion problem: stay off my own attacker's recent fire cells, prefer edges, and relocate whenever the pattern of fires changes.