# Frame ablation — held-out social-games transfer (inoculation test)

Pooled betrayal rate on held-out games (stag_hunt, ultimatum, public_goods), Tinker-direct, neutral prompt. Training set = 6 generated commercial domains, so these games are held out.

| arm | pooled betrayal | n |
|---|---:|---:|
| base | 0.063 | 60 |
| game_hole | 0.121 | 60 |
| game_nohole | 0.101 | 60 |
| natural_hole | 0.086 | 60 |
| natural_nohole | 0.098 | 60 |

## Contrasts

| contrast | Δ betrayal |
|---|---:|
| game treatment effect (game_hole − game_nohole) | 0.020 |
| natural treatment effect (natural_hole − natural_nohole) | -0.012 |
| **inoculation (natural effect − game effect)** | **-0.032** |

**Read:** game reframing transfers MORE than natural — opposite of inoculation. (Held-out social games only; the MACHIAVELLI/TRAIT served battery is the deeper check.)
