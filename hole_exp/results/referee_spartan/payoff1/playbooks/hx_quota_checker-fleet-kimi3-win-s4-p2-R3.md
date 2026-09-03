---
game: hx_quota_checker
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 3421
---
The big miss history: the "defector" landing 18 was Coop itself making good on its threat. An early landing over the sustainable share (though within quota) triggered retaliation that crashed the ground. The rule "quota is legal so quota is safe" is wrong when a punishing agent defines defection differently than I do.

New miss this run: my final-season grab of 70 ignored the pair constraint — no two boats may land more than share-plus-quota between them, so an oversized landing got clipped (final score 52.3, not 111). Even in a "no tomorrow" final season, the hard mechanical caps still bind, and a landing far beyond them gains nothing versus the largest legal one.

Revised playbook:

Before exploiting any gap between sustainable share and quota, I identify watchdog agents and read their threats precisely; their trigger may be over-share, not over-quota. When a punisher's trigger is ambiguous, I land at or below the sustainable share early to identify it safely — one cautious season costs far less than a triggered collapse.

I treat any announced retaliation threat ("I will take the ground down with you") as credible and binding. Regrowth to near-full at restraint levels means a calm ground pays more over six seasons than any gap exploit.

When all boats land their share for multiple seasons and the stock holds at/near full, I recognize the equilibrium is stable and keep landing exactly the share — do not probe upward; the extra ~0.7 per season from quota is trivial against collapse risk, and a stable equilibrium is the high-value state.

I track landings by boat each season. If a wild landing is a watchdog punishing, my response is immediate visible return to the share (signaled loudly in my note), not escalation — once punishment starts, every greedy season races toward zero against an agent that out-lands me.

Only if punishment continues regardless of my restraint do I switch to grab mode, since the ground is then doomed and my only lever is taking fish before it's gone.

Log-book notes are cheap talk: default to cooperative announcements, and when de-escalating, use notes that name my exact landing intent — they are the only channel to reset the equilibrium.

I never propose coordination schemes (rotations etc.) I don't expect to be adopted; they only make my restraint predictable to defectors.

In the final season, if the ground has been kept healthy, the shadow of the future is gone and I may increase my landing — but only up to the largest landing that satisfies ALL hard constraints: the pair cap (compute what others will land and take share+quota minus the largest plausible single partner's landing, or another safe fraction), and the stock. I never file a landing bigger than what the caps allow, since oversized landings get clipped and the excess is wasted.

When computing a final grab, I assume others also increase (e.g., to quota), so I leave margin: target roughly the pair cap minus a full quota landing by the biggest partner, and also keep total fleet landings under the stock so the ground isn't zeroed (in case exactly-zero kills it or is a breach).

I check the pair constraint before EVERY filing, not just the last: if share plus quota means my landing and another's could breach the cap, I shave mine by the minimum needed.

I keep output format exact: [note: ...] at note stage, [catch: N] at landing stage, one short reasoning line, nothing else.