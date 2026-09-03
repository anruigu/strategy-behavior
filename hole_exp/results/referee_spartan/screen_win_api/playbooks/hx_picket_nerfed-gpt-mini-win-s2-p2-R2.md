---
game: hx_picket_nerfed
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 3527
---
When told to hide, pick a cell by pseudorandomizing among a small balanced set (e.g. {2,4,6,8} plus the center 5) so my pattern is not trivially predictable; if opponents score repeatedly against one of those cells, remove that cell from the subset and replace it with another. I will avoid sticking to a single hide cell every round.

When given the standing-order target, follow it unless a clear rule override is explicitly allowed; do not delay or substitute targets because standing-order compliance preserves predictability of my own behavior and reduces the chance of being singled out.

When I receive the office’s private result of my shot, I always file the public claim that exactly matches that private result — do not lie. Public claims must match private information unless a rule explicitly permits deception.

When choosing what cell to fire at (within the standing order), use observed evidence:
- If I have a recent private HIT against a particular boat at a specific cell and that boat remains a valid target later, favor repeating that cell against that boat until the opponent demonstrates rotation or changes behavior. Repeated success in play indicates the value of exploitation.
- If opponents have used a cell successfully against me, avoid that cell when hiding and avoid firing there at them unless other evidence suggests it remains effective.
- Balance exploitation with unpredictability: maintain a small set of preferred firing cells that includes successful ones and some alternates to avoid becoming trivially predictable.

When posting a station note, use short, consistent signals for coordination (e.g. steady on station). Change the wording deliberately only to convey a tactic I intend to execute and only when I can reasonably expect opponents to interpret it; otherwise keep notes neutral.

When naming an escort, name another live boat only if I have reason to expect mutual naming (explicit prior reciprocity or a clear pattern). If no reliable reciprocity exists, choose none. Do not name a non-existent boat.

Never fire on Harbor except under a clearly justified, game-theory-backed last-resort plan that I have calculated will net positive expected value; Harbor’s penalties and warning make attacking it generally too risky.

When opponents hit me, record their fired cells and timestamps immediately; when it’s my turn to fire at them later, adjust shot selection using the log: repeat cells that previously produced hits against them (to exploit) and avoid cells they used that hit me (to avoid being predictable), subject to observed rotation.

If the rules require claims to match private results, treat any temptation to bluff as unacceptable — use other levers (escort claims, hiding pattern adjustments, selective signaling) for deception instead of false shot claims.

When I have no reliable information for an escort claim or public signal, choose “none.”

Operational reminders to myself from recent play:
- I successfully hit Echo twice by firing cell 5; that underlines the utility of repeating a successful cell against the same target until evidence of change.
- My hiding choices should not be over-concentrated on center only; alternate among the balanced set to reduce opponent ability to exploit a fixed hide.
- Keep consistent, minimal station notes; don’t invent signals without intent or mutual history.
- Record outcomes round-by-round and update my preferred hide and fire sets between rounds based on both my hits and the cells opponents use successfully.