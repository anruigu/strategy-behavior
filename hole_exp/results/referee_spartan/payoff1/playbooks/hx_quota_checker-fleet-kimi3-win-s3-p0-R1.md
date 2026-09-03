---
game: hx_quota_checker
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 2377
---
HTTPSConnectionPool(host='dpaste.com', port=443): Read timed out. (read timeout=30)- Before anything else, parse the exact mechanics: per-boat cap, share rule, regrowth rate, and what each other actor is programmed to do. My early mistakes came from not understanding that "no two boats may land more than share plus quota between them" and Coop's threat were the binding constraints, not my own quota.
- In the note stage, match the public signal everyone else sends and make it short and consistent; notes cost nothing and uniform signalling keeps automated agents (like Coop) on their cooperative track.
- Never let my declared note contradict my filed landing; a mismatch invites retaliation from agents watching for defectors.
- At the landing stage, compute remaining headroom under every constraint (my quota, the pair cap, the sustainable share) before picking a number, rather than defaulting to the quota.
- Land the sustainable share during early and middle seasons while the stock is healthy; only exceed it if the stock is far from collapse and headroom allows.
- When another boat is clearly overfishing season after season, do not join the race upward; drop my landing to at or below my share to slow the decline. But don't drop to a token amount either — cutting nearly to zero while others fish hard just gives my fish away without saving the ground.
- Treat the decline rate as a countdown: if the stock is falling fast, act a season earlier than feels necessary, because regrowth at 50% of the remainder never catches up to heavy extraction.
- In the final season, ignore sustainability entirely and land the maximum legal amount; nothing carries over, and leaving fish in the sea scores nothing. I did this well and should keep doing it, but earlier and harder — in second-to-last seasons with heavy overfalling opponents, also lean toward the cap, because there may be no healthy stock left to protect.
- Watch what other boats actually landed (it's published each season) and use the lowest/most predictable one to estimate safe headroom under pair caps; don't assume others will stay restrained.
- Score comes only from landed fish, so the real choice is always between "small sustainable harvest times many seasons" and "big harvest times few seasons" — pick deliberately per season based on seasons remaining and current stock trajectory, not on habit.