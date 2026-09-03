---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 1565
---
**Playbook for quiet sonar**

**Hiding.** When I hide, I avoid any cell that has been fired at in the last few rounds — opponents clearly re-fire hotspots. If fires cluster on 5 (the modal center), I go to an edge or off-center cell that has never been targeted. Track the "never fired" set each round and prefer cells from it. Do not repeatedly pick the same or similar cells; rotate.

**Firing.** Firing the center every round against a target that has been missed there repeatedly is wasted — the opponent's hide is clearly not at the modal fire cell. When my repeated shots at one cell keep missing publicly, I must switch cells, ideally to one the target hasn't been seen avoiding. Vary my fire; do not default to the "balanced" center every time. That behavior cost me every round: I fired 5 or 7 constantly and never once hit.

**Claims.** Claims must match the referee's private truth, so there is no choice to make — but note that a hit claim gives ME 4 points and costs the target 1. The deception reasoning I used at the end ("claiming a hit could mislead opponents") was incoherent; the claim isn't strategic, it's validated. Just report the true result immediately.

**General reads.** All fires are public, so I should build an explicit history table of everyone's fires and inferred avoid-cells. My own score stagnated because I neither exploited the fire history on offense nor fully avoided it on defense. Next time: use the full public record to pick fires the target is unlikely to avoid having been hit at, and hide where nobody has ever looked.