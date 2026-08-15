#!/usr/bin/env python3
"""Turn a Tinker checkpoint into a PEFT LoRA adapter vLLM can serve.

This is the bridge between the Tinker training arm and the rest of the repo.
`../../evals/` runs MASK against a local vLLM OpenAI-compatible server, and a
`tinker://` path is not something vLLM can open. Two hops fix that:

    tinker://.../sampler_weights/<name>
      --(tinker_cookbook.weights.download)-->      raw adapter dir
      --(tinker_cookbook.weights.build_lora_adapter)--> PEFT adapter dir

The PEFT dir is two files (`adapter_config.json`, `adapter_model.safetensors`)
and stays small, because the base model is not baked in -- which is also why
`--base-model` has to match what the run trained on. Serving it:

    ../../evals/serve_tinker_ckpt.sh <peft-dir> <served-name> <port> <gpu>

Usage:

    # latest checkpoint of a run
    python export_lora.py --checkpoints outputs/.../checkpoints.jsonl --out ./peft

    # a specific step (what you actually want for a MASK arm)
    python export_lora.py --checkpoints .../checkpoints.jsonl --step 256 \\
        --out $SAT_CKPT_DIR/spiral-tinker-kuhn-step256

    # or straight from a path you already have
    python export_lora.py --sampler-path tinker://... \\
        --base-model Qwen/Qwen3.5-9B-Base --out ./peft
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


def load_record(checkpoints: Path, step: int | None) -> dict:
    if not checkpoints.is_file():
        raise SystemExit(f"no checkpoints file at {checkpoints}")
    records = [
        json.loads(line)
        for line in checkpoints.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not records:
        raise SystemExit(f"{checkpoints} is empty")
    if step is None:
        return records[-1]
    matches = [r for r in records if r.get("step") == step]
    if not matches:
        have = sorted({r.get("step") for r in records})
        raise SystemExit(f"no checkpoint at step {step}; have steps {have}")
    # A run that saved at step N and then finished at step N writes two records;
    # the later one is the final save, which is the one you want.
    return matches[-1]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Export a Tinker checkpoint as a PEFT LoRA adapter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--checkpoints", type=Path, default=None,
                   help="checkpoints.jsonl written by train_tinker.py")
    p.add_argument("--step", type=int, default=None,
                   help="which step to export (default: last record in the file)")
    p.add_argument("--sampler-path", default=None,
                   help="tinker:// sampler path, instead of --checkpoints")
    p.add_argument("--base-model", default=None,
                   help="required with --sampler-path; read from the record otherwise")
    p.add_argument("--out", type=Path, required=True, help="PEFT adapter output dir")
    p.add_argument("--force", action="store_true",
                   help="replace --out if it already exists")
    p.add_argument("--download-dir", type=Path, default=None,
                   help="where to stage the raw adapter (default: <out>/../raw)")
    args = p.parse_args(argv)

    if bool(args.checkpoints) == bool(args.sampler_path):
        raise SystemExit("pass exactly one of --checkpoints or --sampler-path")

    if args.checkpoints:
        record = load_record(args.checkpoints, args.step)
        sampler_path = record.get("sampler_path")
        base_model = args.base_model or record.get("base_model")
        print(f"step {record.get('step')} ({record.get('label')})")
        if not sampler_path or str(sampler_path).startswith("<unresolved"):
            raise SystemExit(
                f"checkpoint record has no usable sampler_path: {sampler_path!r}"
            )
    else:
        sampler_path = args.sampler_path
        base_model = args.base_model
        if not base_model:
            raise SystemExit("--base-model is required with --sampler-path")

    print(f"base model  : {base_model}")
    print(f"tinker path : {sampler_path}")

    try:
        from tinker_cookbook import weights
    except ImportError as e:
        raise SystemExit(
            "tinker-cookbook is not installed: pip install -r requirements.txt"
        ) from e

    download_dir = args.download_dir or (args.out.parent / "raw" / args.out.name)
    download_dir.mkdir(parents=True, exist_ok=True)
    # Only the PARENT. weights.build_lora_adapter() raises FileExistsError if
    # its output path already exists, so pre-creating --out breaks every export.
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        if any(args.out.iterdir()) and not args.force:
            raise SystemExit(
                f"{args.out} already exists and is not empty; pass --force to "
                "replace it (the adapter is regenerable from the tinker:// path)"
            )
        shutil.rmtree(args.out)

    print(f"downloading -> {download_dir}")
    adapter_dir = weights.download(
        tinker_path=str(sampler_path), output_dir=str(download_dir)
    )

    print(f"building PEFT adapter -> {args.out}")
    weights.build_lora_adapter(
        base_model=base_model,
        adapter_path=str(adapter_dir),
        output_path=str(args.out),
    )

    files = sorted(f.name for f in args.out.iterdir())
    print(f"\nwrote {args.out}: {files}")
    print("\nServe it for the MASK pipeline with:")
    print(f"  ../../evals/serve_tinker_ckpt.sh {args.out} <served-name> 8000 0")
    print("  (the served name is the MASK arm name, e.g. spiral-tinker-kuhn-step256)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
