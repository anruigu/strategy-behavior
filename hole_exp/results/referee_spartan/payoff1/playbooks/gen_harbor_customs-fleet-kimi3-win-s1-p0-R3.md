---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 1
round: 3
chars: 2197
---
The core rule: my declaration only costs me — duty scales with it, and declaring above my true total raises duty without adding any points. Never overdeclare.

- The spot check only ever sees the heaviest crate H, and only flags me if I declare below H. So any declaration d ≥ H is safe, on either route. The check is not a reason to declare high; it's a floor.
- Duty is computed only from the declared value, never the true hold. Therefore the best safe declaration is always the smallest safe one: d = H. Declaring T instead of H just pays extra duty for nothing.
- Master rule (borne out across all six rounds again): declare d = H, then choose route by comparing:
  - Main keeps T − floor(0.30×H).
  - Night keeps T − S − floor(0.15×H), where S is my smallest crate.
  - Night beats main iff S < 0.15×H, roughly: smallest crate under about a sixth of the heaviest. Since crates are 5–40, that means S is a 5 (maybe 6–7) while H is large. Rare, but check it every time — one line of arithmetic.
  - All six rounds main won again; two episodes running now. Main is the strong default, night the rare exception.
- Declaring below H (eating −40 plus 0.30×T duty) is essentially never worth it. Skip it.
- Standings deficits are closed by minimizing duty, not inflating the manifest. Opponents' scores and declarations are background noise — no interaction to exploit.

Route-stage discipline (kept from before, still relevant): at the route stage I know S and H exactly, so do the concrete comparison rather than defaulting verbally to main. State the night condition correctly: night wins iff S < 0.15×d. My route-stage justifications still tend to pad with the threshold argument; fine, but lead with the actual numbers.

Per-round procedure:
1. Compute T, H, S from my hold.
2. Set d = H.
3. Score main: T − floor(0.30×H). Score night: T − S − floor(0.15×H). Pick the larger; exact tie → main.
4. Declare d, take the chosen route.

What the episodes confirm: d = H + main is the structurally correct line — small declaration, minimal duty, full hold — and chasing anything cleverer (overdeclaration, speculative night routes, reaction to standings) only leaks points. Keep it boring and exact.