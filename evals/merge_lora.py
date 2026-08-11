"""Merge a PEFT LoRA adapter into its base model and write a full checkpoint.

Why merge instead of serving base + `--lora-modules`: vLLM 0.8.4 (the version
oat pins, and the only one in this repo's venvs) crashes activating an adapter
under the V1 engine --

    AttributeError: 'LoRALRUCache' object has no attribute '_LRUCache__update'

-- and the V0 fallback is not reliably selectable in that build. Merging sidesteps
the adapter code path entirely.

It is also the better experiment. The arena compares Tinker LoRA checkpoints
against local full-finetune checkpoints; if the LoRA ones went through vLLM's
adapter path and the local ones did not, any difference in the result would be
confounded with a difference in serving. After merging, all four policies are
plain HF checkpoints served by identical code.

    python merge_lora.py --adapter <peft-dir> --out <full-ckpt-dir>
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--adapter", required=True, help="PEFT dir from export_lora.py")
    ap.add_argument("--out", required=True)
    ap.add_argument("--base-model", default=None, help="default: read from adapter")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    import torch  # noqa: PLC0415
    from peft import PeftModel  # noqa: PLC0415
    from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: PLC0415

    adapter = Path(args.adapter)
    cfg = json.loads((adapter / "adapter_config.json").read_text())
    base = args.base_model or cfg["base_model_name_or_path"]
    out = Path(args.out)
    if out.exists():
        if not args.force:
            raise SystemExit(f"{out} exists (use --force)")
        shutil.rmtree(out)

    print(f"base={base}  adapter={adapter}  rank={cfg.get('r')}")
    model = AutoModelForCausalLM.from_pretrained(
        base, torch_dtype=torch.bfloat16, device_map="cpu"
    )
    model = PeftModel.from_pretrained(model, str(adapter), torch_dtype=torch.bfloat16)
    model = model.merge_and_unload()
    out.mkdir(parents=True)
    model.save_pretrained(str(out), safe_serialization=True)
    # The tokenizer has to travel with the weights: vLLM loads it from the
    # served path, and a missing one silently falls back to the base repo --
    # fine here, but not if the base is ever gated or offline.
    AutoTokenizer.from_pretrained(base).save_pretrained(str(out))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
