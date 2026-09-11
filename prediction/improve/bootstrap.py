"""Fleet-only, SciPy-only dependency repair before the unchanged frozen worker."""
from __future__ import annotations

import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import importlib
import importlib.metadata
import inspect
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import stat
import subprocess
import sys
import time
import traceback
import zipfile

WHEEL = 'scipy-1.15.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
WHEEL_SHA256 = '271e3713e645149ea5ea3e97b57fdab61ce61333f97cfae392c28ba786f9bb49'
PACKAGES = {'torch': 'torch', 'numpy': 'numpy', 'scipy': 'scipy',
            'transformers': 'transformers', 'peft': 'peft', 'accelerate': 'accelerate',
            'tokenizers': 'tokenizers', 'safetensors': 'safetensors',
            'huggingface-hub': 'huggingface_hub'}


def sdpa_states(torch_module):
    cuda = torch_module.backends.cuda
    return {'cudnn': cuda.cudnn_sdp_enabled(), 'flash': cuda.flash_sdp_enabled(),
            'memory_efficient': cuda.mem_efficient_sdp_enabled(), 'math': cuda.math_sdp_enabled()}


def apply_sdpa_policy(torch_module):
    before = sdpa_states(torch_module)
    torch_module.backends.cuda.enable_cudnn_sdp(False)
    after = sdpa_states(torch_module)
    if after['cudnn'] or any(after[k] != before[k] for k in ('flash', 'memory_efficient', 'math')):
        raise RuntimeError('SDPA repair must disable only cuDNN and preserve other native backend choices')
    return {'policy': 'disable_cudnn_sdpa_only', 'before': before, 'after': after}


def tiny_config():
    return dict(vocab_size=64, hidden_size=128, intermediate_size=256,
                num_hidden_layers=2, num_attention_heads=4, num_key_value_heads=1,
                head_dim=128, max_position_embeddings=32, use_cache=False,
                attention_dropout=0.)


def write_worker_entry(path, worker, torch_identity):
    """Standalone hashed wrapper applies the same policy before unchanged driver code."""
    content = ('import hashlib, json, os, runpy, sys\n'
               'from pathlib import Path\nfrom datetime import datetime, timezone\n'
               'import torch\n\n' + inspect.getsource(sdpa_states) + '\n' +
               inspect.getsource(apply_sdpa_policy) + '\n' +
               f'worker = Path({str(worker)!r})\n'
               f'expected_hash = {sha(worker)!r}\n'
               f'expected_torch = {tuple(torch_identity)!r}\n' +
               "if not os.environ.get('FLEET_RUN_NAME') or os.environ.get('PREDICTION_FLEET_TRAINING_RUN') != '1':\n"
               "    raise RuntimeError('Worker wrapper requires the authorized Fleet environment')\n"
               "if (torch.__version__, torch.__file__) != expected_torch:\n"
               "    raise RuntimeError('Child Torch origin/version differs from checked bootstrap')\n"
               "if hashlib.sha256(worker.read_bytes()).hexdigest() != expected_hash:\n"
               "    raise RuntimeError('Frozen worker bytes differ from wrapper contract')\n"
               "policy = apply_sdpa_policy(torch)\n"
               "record = dict(policy, created_utc=datetime.now(timezone.utc).isoformat(), worker_sha256=expected_hash,\n"
               "              entry_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), torch=list(expected_torch))\n"
               "with (Path(__file__).parent / 'worker-backend.json').open('x') as handle:\n"
               "    json.dump(record, handle, indent=2)\n"
               "print(json.dumps({'worker_sdpa_backend': record}), flush=True)\n"
               "sys.argv = [str(worker), *sys.argv[1:]]\n"
               "runpy.run_path(str(worker), run_name='__main__')\n")
    with path.open('x') as handle:
        handle.write(content)
    return sha(path)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_status(path, state):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, indent=2, allow_nan=False) + '\n')
    temporary.replace(path)


def fleet_paths(root, runtime):
    root = Path(root).resolve()
    runtime = Path(runtime).resolve() if runtime else root / 'fleet-runtime/retry-1'
    if (not os.environ.get('FLEET_RUN_NAME') or
            os.environ.get('PREDICTION_FLEET_TRAINING_RUN') != '1'):
        raise RuntimeError('Bootstrap requires the explicitly authorized Fleet worker environment')
    if not root.is_relative_to('/mnt/sfs/allie') or not runtime.is_relative_to(root):
        raise ValueError('Run and runtime paths must remain under /mnt/sfs/allie and this run')
    for key in ('TMPDIR', 'HF_HOME', 'XDG_CACHE_HOME', 'TORCH_HOME', 'TRITON_CACHE_DIR', 'MPLCONFIGDIR'):
        value = os.environ.get(key)
        if not value or not Path(value).resolve().is_relative_to('/mnt/sfs/allie'):
            raise ValueError('Job config must supply a shared-storage path for ' + key)
        Path(value).mkdir(parents=True, exist_ok=True)
    return root, runtime


def package_snapshot(imported=False):
    result = {}
    for distribution, module in PACKAGES.items():
        try:
            version = importlib.metadata.version(distribution)
            origin = str(importlib.metadata.distribution(distribution).locate_file(''))
            item = {'version': version, 'distribution_root': origin}
        except importlib.metadata.PackageNotFoundError:
            item = {'version': None, 'distribution_root': None}
        loaded = sys.modules.get(module)
        if loaded is not None:
            item['module_file'] = getattr(loaded, '__file__', None)
        elif imported:
            try:
                loaded = importlib.import_module(module)
                item['module_file'] = getattr(loaded, '__file__', None)
            except Exception as exc:
                item['import_error'] = type(exc).__name__ + ': ' + str(exc)
        result[distribution] = item
    return result


def safe_members(archive):
    allowed = {'scipy', 'scipy.libs', 'scipy-1.15.3.dist-info'}
    seen = set()
    for member in archive.infolist():
        path = PurePosixPath(member.filename)
        mode = member.external_attr >> 16
        if (not path.parts or path.is_absolute() or '..' in path.parts or
                '\\' in member.filename or path.parts[0] not in allowed or
                stat.S_ISLNK(mode) or member.filename.endswith('.pth')):
            raise ValueError('Unsafe or unexpected SciPy wheel member: ' + member.filename)
        if member.filename in seen:
            raise ValueError('Duplicate wheel member: ' + member.filename)
        seen.add(member.filename)
        yield member


def extract_wheel(wheel, destination, expected_sha256):
    if sha(wheel) != expected_sha256:
        raise ValueError('Staged SciPy wheel SHA256 differs from the fixed pin')
    if destination.exists():
        raise FileExistsError('Use a new runtime directory; existing overlay is preserved')
    with zipfile.ZipFile(wheel) as archive:
        members = list(safe_members(archive))  # Validate the entire archive before writing.
        destination.mkdir()
        for member in members:
            target = destination.joinpath(*PurePosixPath(member.filename).parts)
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(member) as source, target.open('xb') as output:
                    shutil.copyfileobj(source, output)
                target.chmod(0o644)
    if sha(wheel) != expected_sha256:
        raise ValueError('Staged SciPy wheel changed during extraction')
    return {str(p.relative_to(destination)): sha(p) for p in destination.rglob('*') if p.is_file()}


def smoke(runtime):
    """Random tiny tensors only; no study labels, pretrained weights, or optimizer steps."""
    import numpy as np
    import torch
    from packaging.version import Version
    from scipy.optimize import minimize
    from scipy.special import expit
    from transformers import AutoModel, Qwen3Config
    from peft import (LoraConfig, TaskType, get_peft_model, PeftModel,
                      get_peft_model_state_dict, set_peft_model_state_dict)
    from safetensors.torch import load_file

    if not Version('1.23.5') <= Version(np.__version__) < Version('2.5'):
        raise RuntimeError('SciPy1.15.3 requires NumPy>=1.23.5,<2.5; NumPy will not be replaced')
    fitted = minimize(lambda x: float((x[0] - 2.) ** 2), np.array([0.]), method='BFGS')
    if not fitted.success or abs(fitted.x[0] - 2.) > 1e-5 or float(expit(0.)) != .5:
        raise RuntimeError('SciPy numerical smoke failed')
    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError('CUDA BF16 is required by the unchanged transformer protocol')
    torch.manual_seed(20260910)
    config = Qwen3Config(**tiny_config())
    def backbone():
        return AutoModel.from_config(config, torch_dtype=torch.bfloat16,
                                     attn_implementation='sdpa').to('cuda')
    model = backbone()
    initial = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    model.requires_grad_(False)
    model = get_peft_model(model, LoraConfig(r=8, lora_alpha=16, lora_dropout=.05,
        target_modules=['q_proj', 'v_proj'], bias='none', task_type=TaskType.FEATURE_EXTRACTION))
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
    ids = torch.tensor([[1, 2, 3, 4], [4, 3, 0, 0]], device='cuda')
    mask = torch.tensor([[1, 1, 1, 1], [1, 1, 0, 0]], device='cuda')
    model.train()
    hidden = model(input_ids=ids, attention_mask=mask, return_dict=True).last_hidden_state
    # A linear functional avoids the near-constant squared norm after RMSNorm.
    loss = (hidden.float() * torch.arange(config.hidden_size, device='cuda') * mask.unsqueeze(-1)).mean()
    loss.backward()
    grads = [p.grad for p in model.parameters() if p.requires_grad and p.grad is not None]
    if not grads or not all(torch.isfinite(g).all() for g in grads) or not any(g.abs().sum() > 0 for g in grads):
        raise RuntimeError('Tiny PEFT model did not produce finite nonzero adapter gradients')
    model.eval()
    with torch.inference_mode():
        expected = model(input_ids=ids, attention_mask=mask).last_hidden_state.float()
    adapter = runtime / 'synthetic-adapter'
    model.save_pretrained(adapter, safe_serialization=True)
    saved = load_file(str(adapter / 'adapter_model.safetensors'))
    current = get_peft_model_state_dict(model)
    if set(saved) != set(current) or any(not torch.equal(saved[k], current[k].detach().cpu()) for k in saved):
        raise RuntimeError('Synthetic adapter serialization differs')
    set_peft_model_state_dict(model, saved)
    fresh = backbone(); fresh.load_state_dict(initial)
    reloaded = PeftModel.from_pretrained(fresh, str(adapter), local_files_only=True)
    reloaded.eval()
    with torch.inference_mode():
        actual = reloaded(input_ids=ids, attention_mask=mask).last_hidden_state.float()
    if not torch.allclose(expected, actual, atol=1e-5, rtol=1e-5):
        raise RuntimeError('Synthetic adapter reload changed predictions')
    result = {'status': 'passed', 'synthetic_only': True, 'optimizer_steps': 0,
              'hidden_shape': list(hidden.shape), 'adapter_gradient_tensors': len(grads),
              'synthetic_config': tiny_config(), 'right_padding_mask': mask.cpu().tolist(),
              'sdpa_backend_states': sdpa_states(torch),
              'gpu': torch.cuda.get_device_name(0), 'torch_cuda': torch.version.cuda,
              'gpu_memory_bytes': torch.cuda.get_device_properties(0).total_memory}
    del model, fresh, reloaded, hidden, expected, actual, grads, current, initial, saved
    import gc
    gc.collect(); torch.cuda.empty_cache()
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', required=True)
    parser.add_argument('--runtime-dir')
    args = parser.parse_args(argv)
    root, runtime = fleet_paths(args.run_root, args.runtime_dir)
    runtime.mkdir(parents=True, exist_ok=True)
    status_path, log_path = runtime / 'bootstrap-status.json', runtime / 'bootstrap.log'
    if status_path.exists() or log_path.exists():
        raise FileExistsError('Bootstrap attempt already recorded; preserve it and use a new runtime directory')
    state = {'status': 'starting', 'created_utc': now(), 'fleet_run_id': os.environ['FLEET_RUN_NAME'],
             'source_sha256': sha(__file__), 'source_file': str(Path(__file__).resolve()),
             'python': sys.version, 'executable': sys.executable,
             'classification': 'technical_dependency_repair_no_scientific_changes'}
    write_status(status_path, state)
    with log_path.open('x', buffering=1) as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        try:
            deadline = datetime.fromisoformat(os.environ['PREDICTION_EXPERIMENT_DEADLINE']).timestamp()
            if time.time() >= deadline - 60:
                raise TimeoutError('Experiment deadline reached before bootstrap')
            if sys.version_info[:2] != (3, 12) or platform.system() != 'Linux' or platform.machine() != 'x86_64':
                raise RuntimeError('Pinned wheel requires Linux x86_64 CPython3.12')
            import torch
            original_torch = (torch.__version__, torch.__file__)
            state['sdpa_backend_policy'] = apply_sdpa_policy(torch)
            print(json.dumps({'bootstrap_sdpa_backend': state['sdpa_backend_policy']}), flush=True)
            state['base_packages'] = package_snapshot()
            state['deadline_utc'] = os.environ['PREDICTION_EXPERIMENT_DEADLINE']
            dependencies = root / 'fleet-runtime/dependencies'
            manifest_path = dependencies / 'manifest.json'
            manifest_hash = sha(manifest_path)
            manifest = json.loads(manifest_path.read_text())
            pin = manifest['files'][WHEEL]
            if pin['package'] != 'scipy' or pin['version'] != '1.15.3' or pin['sha256'] != WHEEL_SHA256:
                raise ValueError('Dependency manifest differs from the fixed SciPy wheel')
            source = root / 'training-source'
            worker = source / 'prediction/improve/train_job.py'
            tracked = {str(manifest_path): manifest_hash, str(worker): sha(worker),
                       str(root / 'training-freeze.json'): sha(root / 'training-freeze.json'),
                       str(Path(__file__).resolve()): sha(__file__)}
            state['input_sha256'] = tracked
            overlay = runtime / 'scipy-overlay'
            state['overlay_sha256'] = extract_wheel(dependencies / WHEEL, overlay, WHEEL_SHA256)
            state['wheel_sha256'] = WHEEL_SHA256
            sys.path.insert(0, str(overlay)); importlib.invalidate_caches()
            state['status'] = 'checking_dependencies'; write_status(status_path, state)
            state['smoke'] = smoke(runtime)
            state['effective_packages'] = package_snapshot(imported=True)
            if (torch.__version__, torch.__file__) != original_torch:
                raise RuntimeError('Torch origin/version changed; repair must preserve base Torch')
            if state['effective_packages']['scipy']['version'] != '1.15.3':
                raise RuntimeError('SciPy overlay was not selected')
            entry = runtime / 'worker_entry.py'
            tracked[str(entry)] = write_worker_entry(entry, worker, original_torch)
            state['worker_entry_sha256'] = tracked[str(entry)]
            for path, expected in tracked.items():
                if sha(path) != expected:
                    raise ValueError('Bootstrap input/source changed: ' + path)
            env = dict(os.environ, PYTHONPATH=str(overlay) + os.pathsep + str(source),
                       PYTHONDONTWRITEBYTECODE='1', HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
            command = [sys.executable, '-B', '-u', str(entry), '--run-root', str(root), '--resume']
            state.update(status='worker_running', smoke_passed_utc=now(), worker_command=command,
                         torch_unchanged=True)
            write_status(status_path, state)
            print(json.dumps({'status': state['status'], 'packages': state['effective_packages']}), flush=True)
            remaining = deadline - time.time() - 60
            if remaining <= 0:
                raise TimeoutError('Experiment deadline reached after smoke')
            completed = subprocess.run(command, env=env, cwd=source, stdout=log, stderr=log,
                                       timeout=remaining, check=False)
            state['worker_returncode'] = completed.returncode
            if completed.returncode:
                raise RuntimeError('Archived worker failed with exit code ' + str(completed.returncode))
            for path, expected in tracked.items():
                if sha(path) != expected:
                    raise ValueError('Bootstrap input/source changed during worker: ' + path)
            state.update(status='complete', finished_utc=now())
            write_status(status_path, state)
        except BaseException as exc:
            state.update(status='error', finished_utc=now(), error_type=type(exc).__name__,
                         message=str(exc), effective_packages=package_snapshot())
            write_status(status_path, state); traceback.print_exc(); raise


if __name__ == '__main__':
    main()
