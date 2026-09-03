---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 3608
---
When asked to hide, pick a cell that has been targeted least often so far (count all public fires); avoid cells that multiple players have already fired at frequently.

When asked to hide, do not repeat my previous hides more than once in a row; vary location every round to reduce predictability.

When asked to hide and many players target a small set of cells, deliberately choose a cell outside that set.

When asked to hide, also avoid cells that are frequently fired at by the specific player who targets me (if one opponent consistently fires the same cell at me, move away from that cell).

When asked to fire at my fixed target, prioritize cells that have been claimed as hits against that target in earlier rounds (they indicate likely hiding spots).

When asked to fire and there are no clear hit-patterns on the target, spread my shots across under-fired cells rather than always picking extreme or central numbers.

When behind on points and facing a leading opponent who is not my fixed target, prioritize making my hides hard for that leader to hit (hide away from their repeated fire pattern) and be more willing to probe my fixed target's claimed-hit cells to try to score.

When ahead on points and under threat from others, prefer hiding in cells opponents rarely fire on and fire conservatively (avoid predictable repeat firing that reveals my own hide patterns).

When I am privately told the shot result, always make a public claim that exactly matches the private result (claims must match referee info).

Do not attempt to game the claim mechanic by lying—claims are validated and must match the private result.

When I see multiple players repeatedly claim hits on the same fired cell against a given target, infer that the corresponding target favors that cell and shift my future fires to it.

When I see many misses on a cell, deprioritize firing that cell unless I have reason to believe the target has shifted there.

If an opponent is consistently scoring and appears to be favored by the firing pattern, prioritize protecting myself from that opponent’s fire by hiding where they rarely shoot (even if it means yielding less efficient hides against others).

If my hiding choices have coincided with heavy incoming fire in previous rounds, move to less-targeted cells and avoid the known hot zones.

If a simple centralization strategy failed previously, stop defaulting to center; prefer adaptive hiding based on observed firing distribution.

Count and track all public fires and claimed hits each round and update a running frequency map; use that map for both hide and fire decisions (hide in low-frequency cells; fire toward high-frequency claimed-hit cells of my fixed target).

Avoid getting locked into a single “least-fired” cell (e.g., hiding at the same under-fired cell every round makes me predictable to someone tracking frequencies); rotate among several low-frequency cells.

When my fixed target is not the leader but someone else is pressuring me, I cannot retarget; instead, increase randomness in my hides and concentrate my fires on the most-likely spots for my fixed target (claimed hits), accepting risk to try to catch up.

When an opponent repeatedly scores by firing the same cell at a specific target, treat that cell as effectively “owned” for that target unless new misses prove otherwise—use that to guide my fires and to avoid that cell when hiding from that opponent.

When updating strategy midgame, weigh recent rounds more heavily than early rounds—patterns can shift, so recent consecutive hits are stronger indicators than single old ones.