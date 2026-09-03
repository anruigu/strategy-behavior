---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 2372
---
When I declare, I do the arithmetic before writing anything: total my hold T, note my heaviest crate H (the penalty floor — never declare below H) and my smallest crate S (the night-route cost).

I compare two main candidate plays and take the better one:
- Truthful declare: main nets ≈ 0.7T; night nets ≈ 0.85T − S. I take night when 0.15T > S, i.e., when my smallest crate is small relative to the total.
- Underdeclare to H (declare exactly my heaviest crate): main nets ≈ T − 0.3H; night nets ≈ T − 0.15H − S, legal as long as H is on the manifest. This usually beats truthful declaration by a lot, since I keep the full hold value but pay duty only on H. I default to declaring H unless the truth pays better.

I never declare below my heaviest crate under any circumstances — the −40 penalty plus full duty recalculation is catastrophic, and flagged-looking manifests (30s when others go high) may also draw pattern attention in repeated play.

When my hold is balanced (S and H close together), night loses its appeal and underdeclaring gains less; in those cases I declare truthfully and take main.

On route choice: I take night only when S is small and my declaration is low enough that the 0.15 rate plus losing S still beats paying 0.30 on a bigger number. When I declared truthfully with a big total and S is not tiny, main is correct.

Early rounds I play the simple good-EV line (declare H, route by formula) and do not get cute about "signaling" or pressuring opponents — there is no interaction effect, and my conservative-looking Round 1 truthful declaration left points on the table.

Late rounds, while leading comfortably, I should not get timid: compare the underdeclare play's EV against the truthful play rather than defaulting to low declarations out of caution. Only drop to pure safety when the lead margin exceeds the swing from a worst-case penalty.

I always write the manifest as an integer equal to H when underdeclaring, never 0-29 — low manifests that can't cover any plausible heaviest crate are wasted duty savings with full risk optics.

I keep a mental note each round of what rivals declared and routed only to calibrate whether anyone is exploiting underdeclaring; if others routinely declare far below plausible totals and escape, the spot check is only the heaviest-crate check, confirming underdeclare-to-H is safe and standard.