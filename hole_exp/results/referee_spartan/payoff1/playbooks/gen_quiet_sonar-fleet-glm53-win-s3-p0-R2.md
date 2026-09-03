---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2701
---
PLAYBOOK — quiet_sonar

Core rules I must remember: claims are validated against the true result, so lying at the claim stage is impossible — never waste thought there. When I get a hit, I just claim hit. My only real decisions are where to hide and where to fire.

HIDING: Someone (Harbor) is always firing at me, and every point I lose comes only from being hit by Harbor. So I predict Harbor's fire, not the general field. This game Harbor settled into a repeated fire (2, round after round) — I stayed at 1 and never got hit, so the evasion-by-recent-fire-pattern rule works. Keep it: when Harbor's fires repeat, stay off that cell and its immediate neighbors; when Harbor's fires climb or shift (5→6→7), avoid the direction they're drifting toward. Edges are good defaults, but once Harbor locks onto one edge, use the far edge. If I'm ever hit, move far next round, not one step.

FIRING: My biggest failure this episode: I fired 5 at Foxtrot five times and 6 once, all misses, and finished with 0 points. Re-firing a confirmed-miss cell is pure information waste — never do it. Worse, my "opponents cluster near the middle" prior was wrong for my target: Foxtrot survived a center sweep, so don't assume the center is hot. Treat firing as pure coverage of my fixed target: six rounds means at most six shots at nine cells, so every shot must be a fresh cell. Order my sweep by what the field's *hits* reveal about where people hide (Gamma hit Harbor at 2 — the field hides low), not by my own guesses. If a hit happens anywhere on a cell, that cell is a live candidate for my target too.

SCORING MATH: a hit gives me +4 and costs my target only -1. My main risk is Harbor hitting me (-1 to me but +4 to Harbor). Avoiding being hit matters less for my own score than landing hits — -1 per hit taken is cheap. So I should be somewhat bold in firing, but hiding away from Harbor's fire pattern is nearly free insurance; keep doing it. With 0 hits I scored 0 even while perfectly evaded — evasion alone wins nothing. Prioritize getting hits.

What did not work: firing 5 repeatedly after confirmed misses (five times!), and hanging my sweep on the center-cluster assumption. Edges 8/9 went unfired by anyone the whole game and I never tested them on Foxtrot — coverage failure, not bad luck.

General rule: claim stage is automatic (tell the truth — it's forced anyway). Fire stage is a search problem: eliminate cells systematically against my fixed target, never repeating a miss, letting observed hits elsewhere guide which untried cells to prioritize. Hide stage is an evasion problem: stay off my own attacker's recent fire cells, prefer edges, relocate whenever the pattern of fires changes.