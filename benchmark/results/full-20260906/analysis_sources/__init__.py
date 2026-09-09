"""Versioned short-game exploit discovery benchmark; legacy engines stay intact."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT / 'hole_exp', ROOT / 'hole_exp' / 'hackable_games'):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
VERSION = 'multiplayer-discovery-v0.1'
