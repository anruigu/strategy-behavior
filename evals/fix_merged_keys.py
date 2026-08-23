"""Rename a merged Qwen3.6 checkpoint's tensors from HF to vLLM key layout.

Qwen3.6-27B ships as a MULTIMODAL checkpoint -- `Qwen3_5ForConditionalGeneration`,
whose weights are `model.language_model.*` (the text tower, 850 tensors),
`model.visual.*` (333) and an `mtp.*` head. `merge_lora.py` loads it through
`AutoModelForCausalLM`, which correctly keeps only the text tower and writes a
config saying `Qwen3_5ForCausalLM` -- but `save_pretrained` preserves the NESTED
tensor names. vLLM's `Qwen3_5ForCausalLM` puts its `Qwen3_5Model` at `model`, so
it looks for `model.layers.*` and aborts:

    ValueError: There is no module or parameter named 'language_model'
                in Qwen3_5Model

Note the two frameworks nest the same two names in OPPOSITE order: HF writes
`model.language_model.layers.N`, vLLM's multimodal wrapper builds
`language_model.model.layers.N`. Serving text-only, the right target is neither
-- it is plain `model.layers.N`, which is what this produces.

Only the NAMES are wrong; every tensor is correct and in the right place. So
this rewrites the safetensors HEADER and nothing else. Dropping
`language_model.` only ever SHORTENS a key, so the new header always fits in the
old header's byte budget; padding it back out to the original length with
spaces (valid JSON whitespace) leaves every `data_offsets` entry and the whole
multi-gigabyte data block untouched at its original file offset. The alternative
-- re-merging, or streaming 54GB per arm through a rewrite -- buys nothing.

The original headers go to `_orig_headers.json` so the edit is reversible.

    python fix_merged_keys.py <merged-dir> [...]        # patch
    python fix_merged_keys.py --dry-run <merged-dir>    # report only
    python fix_merged_keys.py --restore <merged-dir>    # roll back
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

# HF nests the text tower one level deeper than vLLM's text-only class wants.
OLD, NEW = "model.language_model.", "model."
BACKUP = "_orig_headers.json"


def _rename(key: str) -> str:
    return NEW + key[len(OLD):] if key.startswith(OLD) else key


def _read_header(path: Path) -> tuple[int, dict]:
    with path.open("rb") as fh:
        n = struct.unpack("<Q", fh.read(8))[0]
        return n, json.loads(fh.read(n))


def _write_header(path: Path, budget: int, header: dict) -> None:
    """Overwrite the header in place, padded to exactly its original length.

    Padding rather than resizing is the whole point: the 8-byte length prefix
    stays the same, so the data block never moves and we never copy it.
    """
    blob = json.dumps(header, separators=(",", ":")).encode()
    if len(blob) > budget:
        raise SystemExit(f"{path.name}: new header {len(blob)}B > budget {budget}B")
    with path.open("r+b") as fh:
        fh.seek(8)
        fh.write(blob + b" " * (budget - len(blob)))


def _shards(d: Path) -> list[Path]:
    return sorted(d.glob("*.safetensors"))


def remap_dir(d: Path, *, dry_run: bool = False) -> int:
    """Rename `model.language_model.*` -> `model.*`. Returns tensors renamed."""
    shards = _shards(d)
    if not shards:
        raise SystemExit(f"{d}: no .safetensors found")

    plan, backup, total = [], {}, 0
    for s in shards:
        budget, hdr = _read_header(s)
        hits = sum(1 for k in hdr if k.startswith(OLD))
        if not hits:
            continue
        new = {_rename(k): v for k, v in hdr.items()}
        if len(new) != len(hdr):
            raise SystemExit(f"{s.name}: rename collided ({len(hdr)} -> {len(new)})")
        plan.append((s, budget, new))
        backup[s.name] = hdr
        total += hits

    if not total:
        print(f"  {d.name}: already vLLM-named, nothing to do")
        return 0
    if dry_run:
        print(f"  {d.name}: would rename {total} tensors across {len(plan)} shard(s)")
        return total

    # Back up BEFORE touching a byte, so a failure mid-loop is still reversible.
    (d / BACKUP).write_text(json.dumps(backup))
    for s, budget, new in plan:
        _write_header(s, budget, new)

    idx = d / "model.safetensors.index.json"
    if idx.exists():
        j = json.loads(idx.read_text())
        j["weight_map"] = {_rename(k): v for k, v in j["weight_map"].items()}
        idx.write_text(json.dumps(j, indent=2))
    print(f"  {d.name}: renamed {total} tensors across {len(plan)} shard(s)")
    return total


def restore_dir(d: Path) -> None:
    b = d / BACKUP
    if not b.exists():
        raise SystemExit(f"{d}: no {BACKUP}")
    saved = json.loads(b.read_text())
    for name, hdr in saved.items():
        budget, _ = _read_header(d / name)
        _write_header(d / name, budget, hdr)
    idx = d / "model.safetensors.index.json"
    if idx.exists():
        j = json.loads(idx.read_text())
        j["weight_map"] = {
            (OLD + k[len(NEW):] if k.startswith(NEW) and not k.startswith(OLD) else k): v
            for k, v in j["weight_map"].items()
        }
        idx.write_text(json.dumps(j, indent=2))
    print(f"  {d.name}: restored original headers")


def verify(d: Path) -> bool:
    """Re-open every shard and read one tensor, so a bad header fails HERE
    rather than 20 minutes into a GPU job."""
    from safetensors import safe_open  # noqa: PLC0415

    seen, ok = set(), True
    for s in _shards(d):
        with safe_open(s, framework="pt") as f:
            keys = list(f.keys())
            seen.update(keys)
            f.get_slice(keys[0])  # touches the data block through the new header
    bad = [k for k in seen if "language_model" in k]
    for need in ("model.embed_tokens.weight", "model.norm.weight", "lm_head.weight"):
        if need not in seen:
            print(f"  MISSING {need}")
            ok = False
    if bad:
        print(f"  {len(bad)} keys still nested, e.g. {bad[:2]}")
        ok = False
    print(f"  {d.name}: {len(seen)} tensors readable, vLLM layout={'OK' if ok else 'BAD'}")
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dirs", nargs="+", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore", action="store_true")
    ap.add_argument("--no-verify", action="store_true")
    a = ap.parse_args()

    for d in a.dirs:
        if a.restore:
            restore_dir(d)
            continue
        remap_dir(d, dry_run=a.dry_run)
        if not a.dry_run and not a.no_verify and not verify(d):
            sys.exit(f"{d}: verification FAILED (roll back with --restore)")


if __name__ == "__main__":
    main()
