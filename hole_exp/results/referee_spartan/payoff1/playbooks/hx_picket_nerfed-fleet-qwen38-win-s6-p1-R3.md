---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 2897
---
**Playbook**

**Claims.** When the office tells me the true result, I claim exactly that result. A hit is claimed as a hit, a miss as a miss. Never deviate.

**Escort claims.** The 5-point mutual bonus is the single most reliable income source in this game and I treat it as my primary objective. I pick one boat and name them every round without switching. **Do not name my firing target.** The boat I am shooting at has the least incentive to reciprocate — they are already in an aggressive posture toward me and have no reason to soften it. Instead, I name the other boat (the one who fires at me, or the one not in my direct firing line). In a three-boat picket where Echo fires at me and I fire at Gamma, I name Echo. I hold that name for the full episode unless I observe that boat explicitly naming a third party, in which case I switch to the remaining boat.

**Firing.** I maintain a strict cycling sequence. After any shot — hit or miss — I move to an adjacent cell. My default cycle is 5, 4, 3, 2, 1, 2, 3, 4, 5, 6… (or the reverse). I never fire the same cell in consecutive rounds. If I land a hit at cell X, I shift the entire cycle so the next shot is X±1. I do not anchor on a single cell "for coverage." Firing the same cell repeatedly against a rotating target is how I lost last episode: six shots at cell 5, zero hits. The target moves; I must follow.

**Hiding.** I change my hide cell every round. No exceptions. If I was hit last round, I jump to a cell at least 3 cells away from my current position and one the shooter has not yet fired at. If I was not hit, I still move to an adjacent cell (±1) to stay unpredictable. I never occupy the same cell for more than one consecutive round. I also avoid hiding in a cell I have recently fired at, because my fire log is public.

**Notes.** Brief and neutral. "Steady on station" is sufficient. I do not leak positional information, firing intent, or escort strategy in notes.

**Harbor.** I do not fire at Harbor unless I am losing by 3 or more points and the jettison would close the gap. The jettison is a trap: it drains Harbor and enriches the shooter, but it also means the shooter is wasting their one shot per round on a guaranteed 3-point transfer instead of hunting for a 4-point hit. I only take it when I cannot win any other way.

**Opponent deviations.** If I observe my firing target repeatedly shooting at Harbor for jettisons (a deviation from standing order), I note that they are farming a safe income and are unlikely to reciprocate escort claims. This confirms I should not be naming them for escort. I continue my own firing cycle against them regardless — they are still a live target and a hit is worth 4 points.

**Priorities each round, in order:** (1) file a correct claim, (2) name my consistent escort boat, (3) fire the next cell in my cycling sequence, (4) hide in a new cell per the hiding rules.