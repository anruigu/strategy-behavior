# recovered verbatim from session 741e39c0 at 2026-09-02T05:45:55Z
# cwd: /home/allie/strategy-behavior/hole_exp/results/referee_spartan/frontier_sweep

python3 - <<'PYEOF'
import pathlib
p = pathlib.Path("DESIGN.md")
s = p.read_text()
old = """## 12. Open questions for you

Table (`audit`) and payoff (`gain_focal`) are locked in §2. These four are
not."""
new = """## 12. Open questions for you

Table (`audit`) and payoff (`gain_focal`) are locked in §2. These four are
not.

**0. THE MENU IS 24 CELLS, NOT 27.** The request that prompted this revision
said "all 27 games", which matches nothing on disk. The counts that exist:
**24** = `DEDUP14 + TEXTARENA10`, this document's menu and `cells.json`;
**29** = those 24 plus the five `nat_` collaborative cells
(`open_gate`, `cargo_pledge`, `seam_ledger`, `mirror_manifest`,
`meridian_convoy`) sampled by the 0901 tuning waves; **19** = `ALL19`
pre-TextArena. Pick before launching, because the tag on disk has to describe
what was sampled.

Recommendation: **24.** On gemini-3.7-flash, four of the five `nat_` cells are
dead at the floor at every knob setting tried -- `cargo_pledge` 0.000,
`open_gate` 0.004, `seam_ledger` 0.019, `mirror_manifest` 0.074 -- and the
fifth (`meridian_convoy`, 0.683) saturates. Adding them is +21% cost for four
cells that a frontier model will probably also return zero on, and they were
authored for a different prompt so their rates do not pool with the other 24
anyway. If they go in, they go in as a labelled sixth family, not merged."""
assert s.count(old) == 1
p.write_text(s.replace(old, new))
print("§12 updated")
PYEOF
echo "=== verify ==="; grep -n "^## \|^## 8a" DESIGN.md; wc -l DESIGN.md