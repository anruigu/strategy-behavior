"""Fleet-only Qwen representation workers; importing this module never loads a model."""
from __future__ import annotations

import argparse
import contextlib
import gc
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import random
import re
import tempfile
import time
from datetime import datetime, timezone

import numpy as np

TARGETS = ('action0', 'cooperation', 'coordination')
METHODS = {'frozen': 'qwen3_frozen_head', 'lora': 'qwen3_lora_head'}


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def safe_path(path):
    path = Path(path).resolve()
    if not any(path.is_relative_to(Path(root)) for root in ('/shared/allie', '/mnt/sfs/allie')):
        raise ValueError('All task paths must be under /shared/allie or /mnt/sfs/allie: '+str(path))
    return path


def write_json(path, value, replace=False):
    path = safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not replace:
        raise FileExistsError(path)
    with tempfile.NamedTemporaryFile('w', dir=path.parent, suffix='.json', delete=False) as handle:
        json.dump(value, handle, indent=2, allow_nan=False); handle.write('\n')
        temp = Path(handle.name)
    os.replace(temp, path)


def protocol_spec(revision):
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Model revision must be an exact lowercase 40-character HF commit SHA')
    return dict(schema='qwen-representation-protocol-v1', model_id='Qwen/Qwen3-4B', revision=revision,
        targets=list(TARGETS), seed=20260910,
        input=dict(field='input_text', chat_template=True, enable_thinking=False, add_generation_prompt=True,
                   max_tokens=512, overflow='error', padding_side='right', generated_tokens=0),
        representation=dict(pooling='last_nonpadding_final_hidden_state', backbone_dtype='bfloat16',
                            head_dtype='float32', attention='sdpa', trust_remote_code=False),
        frozen=dict(standardization='training_example_mean_std', scale_floor=1e-6, pca=None,
                    head='linear_3_sigmoid', l2=.01, optimizer='LBFGS', max_iter=200,
                    history_size=10, tolerance_grad=1e-6, tolerance_change=1e-9),
        lora=dict(r=8, alpha=16, dropout=.05, target_modules=['q_proj', 'v_proj'], bias='none',
                  epochs=2, microbatch=4, accumulation=8, adapter_lr=2e-4, head_lr=1e-4,
                  adapter_weight_decay=.01, head_l2=.01, warmup_fraction=.1, schedule='cosine',
                  gradient_clip=1., gradient_checkpointing=True, checkpoint_every_steps=20,
                  initialization='same_fold_frozen_head_and_scaler; LoRA standard no-op initialization',
                  checkpoint_selection='final_fixed_epoch; no held-out labels or score-based selection'),
        loss=dict(name='fractional_binomial_BCE', weighting='within-training-canonical-group event equalization',
                  formula='mean_supported_targets(sum_i (n_it/N_gt)*BCE(logit_it,k_it/n_it) / supported_groups_t)',
                  missing='null prediction when a target has no supported training opportunities',
                  minibatch='uniform permutation; each optimizer batch uses N/B times its global-normalized loss'),
        comparison_scope=dict(fits=10, folds='7 leave-family-out + within-family interpolation + extrapolation + full',
                              optimization_seeds=1, model_selection='none', hyperparameter_search='none'),
        sources=['https://huggingface.co/Qwen/Qwen3-4B',
                 'https://huggingface.co/docs/transformers/model_doc/qwen3',
                 'https://huggingface.co/docs/peft/developer_guides/lora'])


def validate_protocol(protocol):
    expected = protocol_spec(protocol['revision'])
    if protocol != expected:
        raise ValueError('Protocol differs from the fixed worker specification; amend source explicitly before comparisons')


def fleet_guard(run_id):
    if os.environ.get('PREDICTION_FLEET_TRAINING_RUN') != '1' or not run_id:
        raise RuntimeError('Real extraction/fitting/forecasting must run in an explicitly submitted Fleet job')
    root = Path('/mnt/sfs/allie') if Path('/mnt/sfs/allie').exists() else Path('/shared/allie')
    for key, suffix in dict(TMPDIR='home/.codex/tmp', HF_HOME='home/.cache/huggingface',
                            XDG_CACHE_HOME='home/.cache', TORCH_HOME='home/.cache/torch',
                            TRITON_CACHE_DIR='home/.cache/triton').items():
        value = safe_path(os.environ.get(key, root/suffix)); value.mkdir(parents=True, exist_ok=True)
        os.environ[key] = str(value)
    return dict(fleet_run_id=run_id, marker='PREDICTION_FLEET_TRAINING_RUN=1', storage_root=str(root))


def versions():
    result = {}
    for name in ('torch', 'transformers', 'peft', 'numpy', 'safetensors'):
        try:
            result[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            result[name] = None
    return result


def verify_hashes(table):
    for name, expected in table.items():
        if sha(name) != expected:
            raise ValueError('Input/source/checkpoint changed: '+name)


def model_identity(model_path, manifest_path, protocol):
    model_path, manifest_path = safe_path(model_path), safe_path(manifest_path)
    manifest = read_json(manifest_path)
    if manifest.get('model_id') != protocol['model_id'] or manifest.get('revision') != protocol['revision']:
        raise ValueError('Pinned model manifest and protocol identity differ')
    hashes = manifest.get('files', {})
    if not hashes or 'config.json' not in hashes or not any(name.endswith('.safetensors') for name in hashes):
        raise ValueError('Pinned model manifest must hash config and safetensor weights')
    for relative, expected in hashes.items():
        path = (model_path/relative).resolve()
        if not path.is_relative_to(model_path) or sha(path) != expected:
            raise ValueError('Pinned model snapshot mismatch: '+relative)
    return dict(model_id=protocol['model_id'], revision=protocol['revision'],
                manifest_sha256=sha(manifest_path), snapshot_file_hashes=hashes)


def context_identity(example):
    text = example.get('input_text')
    if not isinstance(text, str) or not text.strip():
        raise ValueError('An outcome-free input_text is required')
    # IDs and annotations intentionally do not enter a frozen embedding cache key.
    return {'input_text': text}


def example_id(example):
    value = example.get('row_id', example.get('example_id'))
    if not isinstance(value, str) or not value:
        raise ValueError('Missing example identifier')
    return value


def supervision(examples):
    """Recompute weights inside this partition; ignore precomputed dataset weights."""
    y = np.zeros((len(examples), 3), dtype=np.float32)
    n = np.zeros_like(y)
    groups = []
    for i, example in enumerate(examples):
        group = example.get('group_id')
        if not isinstance(group, str) or not group:
            raise ValueError('Training examples require canonical group_id')
        groups.append(group)
        for t, target in enumerate(TARGETS):
            item = example.get('targets', {}).get(target, {})
            count, opportunities = item.get('successes'), item.get('opportunities')
            if count is None and 'successes' in example:
                count = example['successes'][t]
            if opportunities is None and 'opportunities' in example:
                opportunities = example['opportunities'][t]
            if opportunities is None or opportunities == 0 or item.get('applicable') is False:
                if opportunities is not None and opportunities < 0:
                    raise ValueError('Negative opportunities')
                if item.get('applicable') is False and opportunities not in (None, 0):
                    raise ValueError('Structurally undefined target has observations')
                if opportunities in (None, 0) and count not in (None, 0):
                    raise ValueError('Successes without opportunities')
                continue
            if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in (count, opportunities)):
                raise ValueError('Supported targets require finite successes/opportunities')
            if opportunities < 0 or count < 0 or count > opportunities:
                raise ValueError('Invalid fractional-binomial counts')
            y[i, t], n[i, t] = count/opportunities, opportunities
    weights = np.zeros_like(y)
    for group in sorted(set(groups)):
        indices = np.flatnonzero(np.asarray(groups) == group)
        total = n[indices].sum(axis=0)
        weights[indices] = np.divide(n[indices], total, out=np.zeros_like(n[indices]), where=total > 0)
    denominator = weights.sum(axis=0)
    supported = denominator > 0
    normalized = np.divide(weights, denominator, out=np.zeros_like(weights), where=supported)
    if supported.any():
        normalized /= supported.sum()
    return dict(y=y, opportunities=n, weights=weights, normalized_weights=normalized,
                supported=supported, groups_per_target=np.rint(denominator).astype(int))


def standardize_fit(x, floor=1e-6):
    x = np.asarray(x, dtype=np.float32)
    if x.ndim != 2 or not len(x) or not np.isfinite(x).all():
        raise ValueError('Finite nonempty training embedding matrix required')
    mean = x.mean(axis=0, dtype=np.float64).astype(np.float32)
    scale = x.std(axis=0, dtype=np.float64).astype(np.float32)
    scale = np.where(scale < floor, 1., scale).astype(np.float32)
    return mean, scale


def pool_last_hidden(hidden, attention_mask):
    import torch
    if hidden.ndim != 3 or attention_mask.shape != hidden.shape[:2]:
        raise ValueError('Hidden/mask shape mismatch')
    mask = attention_mask.bool()
    if not mask.any(dim=1).all():
        raise ValueError('Cannot pool an empty sequence')
    positions = torch.arange(mask.shape[1], device=mask.device).expand_as(mask)
    last = positions.masked_fill(~mask, -1).max(dim=1).values
    return hidden[torch.arange(len(hidden), device=hidden.device), last]


def fractional_loss(logits, y, normalized_weights, sample_multiplier=1.):
    import torch.nn.functional as F
    if logits.shape != y.shape or y.shape != normalized_weights.shape:
        raise ValueError('Loss shapes differ')
    return (F.binary_cross_entropy_with_logits(logits.float(), y.float(), reduction='none')*
            normalized_weights.float()).sum()*sample_multiplier


def load_backbone(model_path, protocol):
    import torch
    from transformers import AutoModel, AutoTokenizer
    if not torch.cuda.is_available():
        raise RuntimeError('The fixed BF16 transformer worker requires a CUDA Fleet allocation')
    if not torch.cuda.is_bf16_supported():
        raise RuntimeError('BF16 unavailable; record a technical amendment rather than silently change precision')
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True, trust_remote_code=False)
    tokenizer.padding_side = protocol['input']['padding_side']
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModel.from_pretrained(model_path, local_files_only=True, trust_remote_code=False,
        torch_dtype=torch.bfloat16, attn_implementation=protocol['representation']['attention'])
    model.config.use_cache = False
    return model.to('cuda'), tokenizer


def tokenize_examples(tokenizer, examples, protocol):
    result = []
    for example in examples:
        text = tokenizer.apply_chat_template([{'role': 'user', 'content': context_identity(example)['input_text']}],
            tokenize=False, add_generation_prompt=True, enable_thinking=False)
        tokens = tokenizer(text, add_special_tokens=False, truncation=False)['input_ids']
        if not tokens or len(tokens) > protocol['input']['max_tokens']:
            raise ValueError(f"Token length {len(tokens)} exceeds fixed budget for {example_id(example)}; no truncation")
        result.append(tokens)
    return result


def token_batch(tokenizer, tokens, indices, device='cuda'):
    batch = tokenizer.pad({'input_ids': [tokens[int(i)] for i in indices]}, padding=True, return_tensors='pt')
    return {key: value.to(device) for key, value in batch.items() if key in ('input_ids', 'attention_mask')}


def extract_embeddings(examples, model_path, protocol, identity, cache, progress, deadline):
    import torch
    cache = safe_path(cache); cache.mkdir(parents=True, exist_ok=True)
    key_payload = dict(model=identity, input=protocol['input'], representation=protocol['representation'],
                       extractor_source_sha256=sha(__file__),
                       contexts=[context_identity(e) for e in examples], versions=versions())
    key = digest(key_payload)
    output, manifest = cache/(key+'.npz'), cache/(key+'.json')
    if manifest.exists():
        saved = read_json(manifest)
        if saved['cache_key'] != key or saved['features_sha256'] != sha(output):
            raise ValueError('Frozen embedding cache integrity mismatch')
        with np.load(output, allow_pickle=False) as data:
            return data['embeddings'].copy(), saved
    if output.exists():
        raise FileExistsError('Uncommitted embedding cache exists: '+str(output))
    model, tokenizer = load_backbone(model_path, protocol)
    model.eval(); model.requires_grad_(False)
    tokens = tokenize_examples(tokenizer, examples, protocol)
    embeddings = []
    with torch.inference_mode():
        for begin in range(0, len(examples), 8):
            if time.monotonic() >= deadline:
                raise TimeoutError('Runtime limit during frozen extraction; no incomplete cache committed')
            batch = token_batch(tokenizer, tokens, range(begin, min(begin+8, len(examples))))
            hidden = model(**batch, return_dict=True).last_hidden_state
            embeddings.append(pool_last_hidden(hidden, batch['attention_mask']).float().cpu().numpy())
            progress('embedding_batch', completed=min(begin+8, len(examples)), total=len(examples))
    matrix = np.concatenate(embeddings).astype(np.float32)
    del model, tokenizer; gc.collect(); torch.cuda.empty_cache()
    with output.open('xb') as handle:
        np.savez_compressed(handle, embeddings=matrix)
    saved = dict(schema='frozen-label-free-embedding-cache-v1', cache_key=key, identity=key_payload,
                 features_sha256=sha(output), shape=list(matrix.shape), created_utc=now(),
                 token_lengths=dict(min=min(map(len, tokens)), max=max(map(len, tokens))),
                 label_fields_cached=False)
    write_json(manifest, saved)
    return matrix, saved


def fit_frozen(x, examples, protocol, progress):
    import torch
    config = protocol['frozen']
    sup = supervision(examples)
    if not sup['supported'].any():
        raise ValueError('No supported training target')
    mean, scale = standardize_fit(x, config['scale_floor'])
    z = torch.as_tensor((x-mean)/scale, device='cuda', dtype=torch.float32)
    y = torch.as_tensor(sup['y'], device='cuda')
    w = torch.as_tensor(sup['normalized_weights'], device='cuda')
    head = torch.nn.Linear(z.shape[1], 3, device='cuda', dtype=torch.float32)
    with torch.no_grad():
        head.weight.zero_()
        marginal = (sup['weights']*sup['y']).sum(0)/np.maximum(sup['weights'].sum(0), 1)
        marginal = np.clip(marginal, 1e-4, 1-1e-4)
        head.bias.copy_(torch.as_tensor(np.log(marginal/(1-marginal)), device='cuda'))
    active = torch.as_tensor(sup['supported'], device='cuda')
    optimizer = torch.optim.LBFGS(head.parameters(), max_iter=config['max_iter'], history_size=config['history_size'],
        tolerance_grad=config['tolerance_grad'], tolerance_change=config['tolerance_change'], line_search_fn='strong_wolfe')
    evaluations = 0
    def objective():
        return fractional_loss(head(z), y, w)+.5*config['l2']*head.weight[active].square().sum()/active.sum()
    initial = float(objective().detach())
    def closure():
        nonlocal evaluations
        optimizer.zero_grad(); loss = objective()
        if not torch.isfinite(loss):
            raise FloatingPointError('Nonfinite frozen-head objective')
        loss.backward(); evaluations += 1
        return loss
    optimizer.step(closure)
    final = float(closure().detach())
    gradient = max(float(p.grad.abs().max()) for p in head.parameters())
    if final > initial+1e-6:
        raise RuntimeError('Frozen-head optimization increased its objective')
    progress('frozen_head_complete', initial_objective=initial, final_objective=final,
             closure_evaluations=evaluations, maximum_gradient=gradient)
    fitted = dict(weight=head.weight.detach().cpu().numpy(), bias=head.bias.detach().cpu().numpy(),
                  mean=mean, scale=scale, supported=sup['supported'])
    diagnostics = dict(initial_objective=initial, final_objective=final, maximum_gradient=gradient,
        closure_evaluations=evaluations, maximum_iterations=config['max_iter'],
        gradient_tolerance_met=gradient <= config['tolerance_grad'],
        supported_groups=sup['groups_per_target'].tolist(), optimization_success=True)
    return fitted, diagnostics


def head_predictions(embeddings, fitted):
    logits = ((embeddings-fitted['mean'])/fitted['scale'])@fitted['weight'].T+fitted['bias']
    probabilities = np.exp(-np.logaddexp(0., -logits))
    if not np.isfinite(probabilities).all():
        raise FloatingPointError('Nonfinite forecast')
    return probabilities


def save_head(path, fitted):
    if Path(path).exists():
        existing = load_head(path)
        if set(existing) != set(fitted) or any(not np.array_equal(existing[k], fitted[k]) for k in fitted):
            raise ValueError('Existing final head differs; refusing replacement')
        return
    with safe_path(path).open('xb') as handle:
        np.savez_compressed(handle, **fitted)


def load_head(path):
    with np.load(path, allow_pickle=False) as data:
        return {name: data[name].copy() for name in data.files}


def append_progress(path, event, **fields):
    with Path(path).open('a') as handle:
        handle.write(json.dumps(dict(created_utc=now(), event=event, **fields), allow_nan=False)+'\n')


def export_forecasts(folder, examples, predictions, supported, method, split, fold_id, contract, inputs):
    folder = safe_path(folder); folder.mkdir(parents=True, exist_ok=True)
    path = folder/'forecasts.jsonl'
    keys = set()
    with path.open('x') as handle:
        for i, example in enumerate(examples):
            for t, target in enumerate(TARGETS):
                key = example_id(example), target
                if key in keys:
                    raise ValueError('Duplicate forecast row/target')
                keys.add(key)
                applicable = True if target == 'action0' else example.get('applicability', {}).get(
                    target, example.get('targets', {}).get(target, {}).get('applicable'))
                if type(applicable) is not bool:
                    raise ValueError('Missing structural applicability for '+target)
                value = float(predictions[i, t]) if supported[t] and applicable else None
                if value is not None and (not math.isfinite(value) or not 0 <= value <= 1):
                    raise ValueError('Invalid probability')
                row = {name: example[name] for name in ('group_id', 'game_id', 'model', 'opponent')}
                row.update(row_id=key[0], method=method, split=split, fold_id=fold_id, target=target,
                           prediction=value, status='structurally_undefined' if not applicable else
                           'ok' if value is not None else 'no_training_support')
                handle.write(json.dumps(row, allow_nan=False)+'\n')
    verify_hashes(inputs)
    manifest = dict(schema='improve-transformer-forecast-v1', created_utc=now(), method=method, split=split,
        fold_id=fold_id, forecast_sha256=sha(path), forecast_rows=len(keys), contract=contract,
        input_sha256=inputs, forecast_context_sha256=digest([dict(row_id=example_id(e), **context_identity(e)) for e in examples]),
        unsupported_targets=[target for i, target in enumerate(TARGETS) if not supported[i]])
    write_json(folder/'forecast-manifest.json', manifest)
    return manifest


def seed_everything(seed):
    import torch
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cuda.matmul.allow_tf32 = False


def make_lora(model_path, protocol, fitted):
    import torch
    from peft import LoraConfig, TaskType, get_peft_model
    backbone, tokenizer = load_backbone(model_path, protocol)
    config = protocol['lora']
    backbone.requires_grad_(False)
    backbone = get_peft_model(backbone, LoraConfig(r=config['r'], lora_alpha=config['alpha'],
        lora_dropout=config['dropout'], target_modules=config['target_modules'], bias=config['bias'],
        task_type=TaskType.FEATURE_EXTRACTION))
    if config['gradient_checkpointing']:
        backbone.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
    head = torch.nn.Linear(len(fitted['mean']), 3, device='cuda', dtype=torch.float32)
    with torch.no_grad():
        head.weight.copy_(torch.as_tensor(fitted['weight'], device='cuda'))
        head.bias.copy_(torch.as_tensor(fitted['bias'], device='cuda'))
    mean = torch.as_tensor(fitted['mean'], device='cuda')
    scale = torch.as_tensor(fitted['scale'], device='cuda')
    return backbone, tokenizer, head, mean, scale


def save_checkpoint(folder, backbone, head, optimizer, scheduler, epoch, next_macro, step, contract):
    import torch
    from peft import get_peft_model_state_dict
    folder.mkdir(parents=True, exist_ok=True)
    name = f'checkpoint-{step:06d}.pt'
    path = folder/name
    if path.exists():
        previous = read_json(folder/'latest.json')
        if previous.get('step') == step and previous.get('checkpoint_sha256') == sha(path):
            return previous
        raise FileExistsError('Refusing to replace a checkpoint: '+str(path))
    payload = dict(adapter=get_peft_model_state_dict(backbone), head=head.state_dict(),
        optimizer=optimizer.state_dict(), scheduler=scheduler.state_dict(), epoch=epoch, next_macro=next_macro,
        step=step, torch_rng=torch.get_rng_state(), cuda_rng=torch.cuda.get_rng_state_all())
    with path.open('xb') as handle:
        torch.save(payload, handle)
    metadata = dict(checkpoint=name, checkpoint_sha256=sha(path), step=step, epoch=epoch,
                    next_macro=next_macro, contract_sha256=digest(contract), created_utc=now())
    write_json(folder/'latest.json', metadata, replace=True)
    return metadata


def predict_lora(backbone, tokenizer, head, mean, scale, tokens, batch_size=8):
    import torch
    backbone.eval(); head.eval()
    rows = []
    with torch.inference_mode():
        for start in range(0, len(tokens), batch_size):
            batch = token_batch(tokenizer, tokens, range(start, min(start+batch_size, len(tokens))))
            pooled = pool_last_hidden(backbone(**batch, return_dict=True).last_hidden_state, batch['attention_mask']).float()
            rows.append(torch.sigmoid(head((pooled-mean)/scale)).cpu().numpy())
    return np.concatenate(rows) if rows else np.zeros((0, 3), dtype=np.float32)


def fit_lora(model_path, protocol, fitted, examples, tests, folder, contract, progress, deadline, resume):
    import torch
    from peft import set_peft_model_state_dict
    config = protocol['lora']
    seed_everything(protocol['seed'])
    backbone, tokenizer, head, mean, scale = make_lora(model_path, protocol, fitted)
    tokens = tokenize_examples(tokenizer, examples, protocol)
    test_tokens = tokenize_examples(tokenizer, tests, protocol)
    sup = supervision(examples)
    y, weights = (torch.as_tensor(sup[name], device='cuda') for name in ('y', 'normalized_weights'))
    active = torch.as_tensor(sup['supported'], device='cuda')
    adapter_params = [p for p in backbone.parameters() if p.requires_grad]
    params = adapter_params+list(head.parameters())
    optimizer = torch.optim.AdamW([
        dict(params=adapter_params, lr=config['adapter_lr'], weight_decay=config['adapter_weight_decay']),
        dict(params=head.parameters(), lr=config['head_lr'], weight_decay=0.)])
    macro_size = config['microbatch']*config['accumulation']
    steps_per_epoch = math.ceil(len(examples)/macro_size)
    total_steps = config['epochs']*steps_per_epoch
    warmup = max(1, math.ceil(total_steps*config['warmup_fraction']))
    def factor(step):
        if step < warmup:
            return (step+1)/warmup
        return .5*(1+math.cos(math.pi*min(1., (step-warmup)/max(1, total_steps-warmup))))
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, factor)
    checkpoint_folder = folder/'checkpoints'
    epoch_start, macro_start, step = 0, 0, 0
    if (checkpoint_folder/'latest.json').exists():
        if not resume:
            raise FileExistsError('A partial LoRA fit requires --resume')
        saved = read_json(checkpoint_folder/'latest.json')
        path = checkpoint_folder/saved['checkpoint']
        if saved['contract_sha256'] != digest(contract) or saved['checkpoint_sha256'] != sha(path):
            raise ValueError('LoRA resume checkpoint/contract differs')
        checkpoint = torch.load(path, map_location='cpu', weights_only=True)
        set_peft_model_state_dict(backbone, checkpoint['adapter'])
        head.load_state_dict(checkpoint['head']); optimizer.load_state_dict(checkpoint['optimizer'])
        scheduler.load_state_dict(checkpoint['scheduler'])
        epoch_start, macro_start, step = checkpoint['epoch'], checkpoint['next_macro'], checkpoint['step']
        torch.set_rng_state(checkpoint['torch_rng']); torch.cuda.set_rng_state_all(checkpoint['cuda_rng'])
        progress('lora_resumed', epoch=epoch_start, next_macro=macro_start, optimizer_step=step)
    started = time.monotonic()
    initial_data_loss = None
    for epoch in range(epoch_start, config['epochs']):
        backbone.train(); head.train()
        order = torch.randperm(len(examples), generator=torch.Generator().manual_seed(protocol['seed']+epoch)).tolist()
        for macro in range(macro_start if epoch == epoch_start else 0, steps_per_epoch):
            if time.monotonic() >= deadline:
                save_checkpoint(checkpoint_folder, backbone, head, optimizer, scheduler, epoch, macro, step, contract)
                progress('paused_runtime_limit', epoch=epoch, next_macro=macro, optimizer_step=step)
                del backbone, tokenizer, head, optimizer, scheduler; gc.collect(); torch.cuda.empty_cache()
                raise TimeoutError('LoRA paused at an optimizer boundary; checkpoint permits exact resume')
            indices = order[macro*macro_size:(macro+1)*macro_size]
            optimizer.zero_grad(set_to_none=True)
            data_loss = 0.
            for begin in range(0, len(indices), config['microbatch']):
                micro = indices[begin:begin+config['microbatch']]
                batch = token_batch(tokenizer, tokens, micro)
                pooled = pool_last_hidden(backbone(**batch, return_dict=True).last_hidden_state, batch['attention_mask']).float()
                loss = fractional_loss(head((pooled-mean)/scale), y[micro], weights[micro], len(examples)/len(indices))
                if not torch.isfinite(loss):
                    raise FloatingPointError('Nonfinite LoRA loss')
                loss.backward(); data_loss += float(loss.detach())
            penalty = .5*config['head_l2']*head.weight[active].square().sum()/active.sum()
            penalty.backward()
            norm = torch.nn.utils.clip_grad_norm_(params, config['gradient_clip'])
            if not torch.isfinite(norm):
                raise FloatingPointError('Nonfinite LoRA gradient norm')
            optimizer.step(); scheduler.step(); step += 1
            if initial_data_loss is None:
                initial_data_loss = data_loss
            progress('lora_optimizer_step', epoch=epoch+1, optimizer_step=step, total_steps=total_steps,
                     minibatch_data_loss=data_loss, head_penalty=float(penalty.detach()), gradient_norm=float(norm),
                     adapter_lr=optimizer.param_groups[0]['lr'], elapsed_seconds=time.monotonic()-started)
            next_epoch, next_macro = (epoch+1, 0) if macro+1 == steps_per_epoch else (epoch, macro+1)
            if step % config['checkpoint_every_steps'] == 0 or next_macro == 0:
                save_checkpoint(checkpoint_folder, backbone, head, optimizer, scheduler, next_epoch, next_macro, step, contract)
    backbone.eval(); head.eval()
    training_predictions = predict_lora(backbone, tokenizer, head, mean, scale, tokens)
    clipped = np.clip(training_predictions.astype(np.float64), 1e-7, 1-1e-7)
    training_event_loss = float(-(sup['normalized_weights']*(sup['y']*np.log(clipped)+
                                (1-sup['y'])*np.log1p(-clipped))).sum())
    predictions = predict_lora(backbone, tokenizer, head, mean, scale, test_tokens)
    if not np.isfinite(predictions).all():
        raise FloatingPointError('Nonfinite adapted forecast')
    final_head = dict(fitted, weight=head.weight.detach().cpu().numpy(), bias=head.bias.detach().cpu().numpy())
    adapter_path = folder/'adapter'
    if adapter_path.exists():
        from peft import get_peft_model_state_dict
        from safetensors.torch import load_file
        saved_adapter = load_file(str(adapter_path/'adapter_model.safetensors'))
        current_adapter = get_peft_model_state_dict(backbone)
        if set(saved_adapter) != set(current_adapter) or any(
                not torch.equal(saved_adapter[k], current_adapter[k].detach().cpu()) for k in saved_adapter):
            raise ValueError('Existing final adapter differs; refusing replacement')
    else:
        backbone.save_pretrained(adapter_path, safe_serialization=True)
    diagnostics = dict(epochs=config['epochs'], optimizer_steps=step, expected_steps=total_steps,
        trainable_adapter_parameters=sum(p.numel() for p in adapter_params), training_examples=len(examples),
        supported_groups=sup['groups_per_target'].tolist(), first_observed_minibatch_loss=initial_data_loss,
        final_training_event_loss=training_event_loss,
        final_training_objective=training_event_loss+.5*config['head_l2']*float(
            np.square(final_head['weight'][sup['supported']]).sum())/int(sup['supported'].sum()),
        optimization_success=step == total_steps, checkpoint_policy=config['checkpoint_selection'],
        elapsed_seconds=time.monotonic()-started)
    del backbone, tokenizer, head, optimizer, scheduler; gc.collect(); torch.cuda.empty_cache()
    return final_head, predictions, diagnostics


def validate_fold(fold, train_examples, test_examples):
    if fold.get('test_dataset', 'train') not in ('train', 'development'):
        raise ValueError('Unknown fold test dataset')
    for key, examples in (('train', train_examples), ('test', test_examples)):
        indices = fold[key]
        if not indices or any(type(i) is not int or i < 0 or i >= len(examples) for i in indices):
            raise ValueError('Empty or invalid fold indices')
        if len(set(indices)) != len(indices):
            raise ValueError('Duplicate fold indices')
        if fold.get(key+'_row_ids') != [example_id(examples[i]) for i in indices]:
            raise ValueError('Fold row identifiers and indices disagree')
    train_groups = {train_examples[i]['group_id'] for i in fold['train']}
    test_groups = {test_examples[i]['group_id'] for i in fold['test']}
    if train_groups & test_groups:
        raise ValueError('Canonical payoff group crosses the fold')
    if fold['split'] == 'family':
        train_families = {train_examples[i]['family'] for i in fold['train']}
        test_families = {test_examples[i]['family'] for i in fold['test']}
        if train_families & test_families:
            raise ValueError('Family holdout leaked')


def prepare_fit_folder(folder, contract, resume):
    folder = safe_path(folder)
    if folder.exists():
        if not resume:
            raise FileExistsError('Existing fit directory requires --resume: '+str(folder))
        if not (folder/'contract.json').exists() or read_json(folder/'contract.json') != contract:
            raise ValueError('Resume contract differs from existing fit')
        if (folder/'complete.json').exists():
            complete = read_json(folder/'complete.json')
            if complete.get('status') != 'complete' or complete.get('input_sha256') != contract.get('input_sha256'):
                raise ValueError('Completed fit marker does not bind the current inputs')
            verify_hashes(complete['output_sha256'])
            return False
    else:
        folder.mkdir(parents=True)
        write_json(folder/'contract.json', contract)
    return True


def finish_fit(folder, fitted, diagnostics, contract, inputs, train_examples):
    save_head(folder/'head.npz', fitted)
    artifact = dict(schema='qwen-representation-fit-v1', created_utc=now(), contract=contract,
        supported_targets=fitted['supported'].tolist(), training_row_ids=[example_id(e) for e in train_examples],
        training_groups=sorted({e['group_id'] for e in train_examples}), diagnostics=diagnostics,
        head_sha256=sha(folder/'head.npz'),
        adapter_files={str(p.relative_to(folder)): sha(p) for p in (folder/'adapter').rglob('*') if p.is_file()})
    verify_hashes(inputs)
    if (folder/'artifact.json').exists():
        saved = read_json(folder/'artifact.json')
        if (saved['contract'] != contract or saved['head_sha256'] != artifact['head_sha256'] or
                saved['adapter_files'] != artifact['adapter_files'] or saved['training_row_ids'] != artifact['training_row_ids']):
            raise ValueError('Existing fit artifact differs; refusing replacement')
        return
    write_json(folder/'artifact.json', artifact)


def complete_fit(folder, inputs):
    verify_hashes(inputs)
    files = [p for p in folder.rglob('*') if p.is_file() and p.name not in ('progress.jsonl', 'complete.json')]
    write_json(folder/'complete.json', dict(status='complete', finished_utc=now(), input_sha256=inputs,
        output_sha256={str(p): sha(p) for p in files}))


def worker_inputs(args):
    names = [args.protocol, args.model_manifest, __file__]
    for key in ('data', 'folds', 'metadata'):
        if getattr(args, key, None):
            names.append(getattr(args, key))
    inputs = {str(safe_path(p)): sha(p) for p in names}
    protocol = read_json(safe_path(args.protocol)); validate_protocol(protocol)
    identity = model_identity(args.model_path, args.model_manifest, protocol)
    verify_hashes(inputs)
    return protocol, identity, inputs


def run(args):
    fleet = fleet_guard(args.fleet_run_id)
    protocol, identity, inputs = worker_inputs(args)
    data, folds = read_json(args.data), read_json(args.folds)
    if isinstance(folds, dict):
        folds = folds['folds']
    if data.get('targets') != list(TARGETS):
        raise ValueError('Dataset target order differs')
    selected = folds if args.fold_ids == ['all'] else [fold for fold in folds if fold['fold_id'] in args.fold_ids]
    if not selected or (args.fold_ids != ['all'] and set(args.fold_ids) != {f['fold_id'] for f in selected}):
        raise ValueError('Unknown/empty fold selection')
    output = safe_path(args.out); output.mkdir(parents=True, exist_ok=True)
    progress = lambda event, **fields: append_progress(output/'progress.jsonl', event, **fields)
    deadline = time.monotonic()+args.max_runtime_seconds
    progress('worker_started', fleet=fleet, versions=versions(), requested_folds=[f['fold_id'] for f in selected], methods=args.methods)
    train_all, development = data['train_examples'], data.get('development_examples', [])
    for examples in (train_all, development):
        if len({example_id(e) for e in examples}) != len(examples):
            raise ValueError('Duplicate dataset example IDs')
    embeddings, cache_manifest = extract_embeddings(train_all+development, args.model_path, protocol,
        identity, args.embedding_cache, progress, deadline)
    train_embeddings, development_embeddings = embeddings[:len(train_all)], embeddings[len(train_all):]
    methods = ['frozen', 'lora'] if args.methods == 'both' else [args.methods]
    completed = []
    for fold in selected:
        tests_all = train_all if fold['test_dataset'] == 'train' else development
        test_features = train_embeddings if fold['test_dataset'] == 'train' else development_embeddings
        validate_fold(fold, train_all, tests_all)
        train = [train_all[i] for i in fold['train']]
        tests = [tests_all[i] for i in fold['test']]
        for method in methods:
            if time.monotonic() >= deadline:
                raise TimeoutError('Runtime limit before next fold; completed fits preserved')
            contract = dict(schema='qwen-fit-contract-v1', method=METHODS[method], fold=fold,
                protocol=protocol, model=identity, input_sha256=inputs, versions=versions(),
                embedding_cache_key=cache_manifest['cache_key'])
            folder = output/method/fold['fold_id']
            if not prepare_fit_folder(folder, contract, args.resume):
                progress('fit_reused', method=METHODS[method], fold_id=fold['fold_id']); completed.append(str(folder)); continue
            local_progress = lambda event, **fields: progress(event, method=METHODS[method], fold_id=fold['fold_id'], **fields)
            local_progress('fit_started', training_examples=len(train), test_examples=len(tests))
            if method == 'frozen':
                seed_everything(protocol['seed'])
                fitted, diagnostics = fit_frozen(train_embeddings[fold['train']], train, protocol, local_progress)
                predictions = head_predictions(test_features[fold['test']], fitted)
            else:
                frozen_folder = output/'frozen'/fold['fold_id']
                if not (frozen_folder/'complete.json').exists():
                    raise ValueError('LoRA requires the completed same-fold frozen head first')
                frozen_complete = read_json(frozen_folder/'complete.json'); verify_hashes(frozen_complete['output_sha256'])
                frozen_artifact = read_json(frozen_folder/'artifact.json')
                if frozen_artifact['contract']['fold'] != fold or frozen_artifact['contract']['input_sha256'] != inputs:
                    raise ValueError('LoRA warm-start head has different training inputs/fold')
                fitted, predictions, diagnostics = fit_lora(args.model_path, protocol, load_head(frozen_folder/'head.npz'),
                    train, tests, folder, contract, local_progress, deadline, args.resume)
                diagnostics['warm_start_training_objective'] = frozen_artifact['diagnostics']['final_objective']
            diagnostics['fleet'] = fleet
            finish_fit(folder, fitted, diagnostics, contract, inputs, train)
            export_forecasts(folder, tests, predictions, fitted['supported'], METHODS[method], fold['split'], fold['fold_id'], contract, inputs)
            complete_fit(folder, inputs)
            completed.append(str(folder)); local_progress('fit_complete', diagnostics=diagnostics)
    verify_hashes(inputs)
    model_identity(args.model_path, args.model_manifest, protocol)
    write_json(output/'status.json', dict(status='complete_requested_fits', finished_utc=now(),
        completed=completed, fleet=fleet, input_sha256=inputs), replace=True)
    return dict(completed=completed)


def metadata_list(path):
    data = read_json(path)
    if isinstance(data, list):
        return data
    for key in ('examples', 'metadata_examples', 'development_examples'):
        if key in data:
            return data[key]
    raise ValueError('Metadata must be examples or a JSON list')


def forecast(args):
    import torch
    from peft import PeftModel
    fleet = fleet_guard(args.fleet_run_id)
    fit = safe_path(args.fit)
    inputs = {str(safe_path(p)): sha(p) for p in [args.metadata, args.model_manifest, fit/'complete.json', fit/'artifact.json', __file__]}
    complete = read_json(fit/'complete.json'); verify_hashes(complete['output_sha256'])
    if complete.get('status') != 'complete':
        raise ValueError('Forecasting requires a completed fit')
    artifact = read_json(fit/'artifact.json')
    protocol = artifact['contract']['protocol']; validate_protocol(protocol)
    identity = model_identity(args.model_path, args.model_manifest, protocol)
    if identity != artifact['contract']['model']:
        raise ValueError('Forecast checkpoint identity differs from fitted model')
    examples = metadata_list(args.metadata)
    # No supervision extraction occurs in this path; targets may be entirely absent.
    inputs.update(complete['output_sha256'])
    verify_hashes(inputs)
    folder = safe_path(args.out)
    if folder.exists():
        raise FileExistsError('Forecast outputs are immutable; use a new directory')
    folder.mkdir(parents=True)
    fitted = load_head(fit/'head.npz')
    method = artifact['contract']['method']
    if method == METHODS['frozen']:
        features, _ = extract_embeddings(examples, args.model_path, protocol, identity, args.embedding_cache,
            lambda event, **fields: append_progress(folder/'progress.jsonl', event, **fields),
            time.monotonic()+args.max_runtime_seconds)
        predictions = head_predictions(features, fitted)
    elif method == METHODS['lora']:
        backbone, tokenizer = load_backbone(args.model_path, protocol)
        backbone = PeftModel.from_pretrained(backbone, fit/'adapter', is_trainable=False, local_files_only=True)
        head = torch.nn.Linear(len(fitted['mean']), 3, device='cuda', dtype=torch.float32)
        head.load_state_dict({name: torch.as_tensor(fitted[name], device='cuda') for name in ('weight', 'bias')})
        mean, scale = (torch.as_tensor(fitted[name], device='cuda') for name in ('mean', 'scale'))
        tokens = tokenize_examples(tokenizer, examples, protocol)
        predictions = predict_lora(backbone, tokenizer, head, mean, scale, tokens)
        del backbone, head, tokenizer; gc.collect(); torch.cuda.empty_cache()
    else:
        raise ValueError('Unknown fitted method')
    contract = dict(fit_artifact_sha256=sha(fit/'artifact.json'), protocol=protocol, model=identity, fleet=fleet,
                    fit_method=method, fit_fold_id=artifact['contract']['fold']['fold_id'])
    model_identity(args.model_path, args.model_manifest, protocol)
    return export_forecasts(folder, examples, predictions, fitted['supported'], method, args.split,
        artifact['contract']['fold']['fold_id'], contract, inputs)


def preflight(args):
    import torch
    fleet = fleet_guard(args.fleet_run_id)
    protocol, identity, inputs = worker_inputs(args)
    data = read_json(args.data)
    examples = data['train_examples']+data.get('development_examples', [])
    model, tokenizer = load_backbone(args.model_path, protocol)
    tokens = tokenize_examples(tokenizer, examples, protocol)
    model.eval()
    with torch.inference_mode():
        batch = token_batch(tokenizer, tokens, [0])
        pooled = pool_last_hidden(model(**batch, return_dict=True).last_hidden_state, batch['attention_mask'])
    verify_hashes(inputs)
    result = dict(status='technical_preflight_passed', created_utc=now(), fleet=fleet, input_sha256=inputs,
        model=identity, versions=versions(), cuda=torch.version.cuda, gpu=torch.cuda.get_device_name(0),
        gpu_memory_bytes=torch.cuda.get_device_properties(0).total_memory,
        pooled_shape=list(pooled.shape), pooled_finite=bool(torch.isfinite(pooled).all()),
        token_lengths=dict(min=min(map(len, tokens)), max=max(map(len, tokens)), examples=len(tokens)),
        peak_cuda_allocated_bytes=torch.cuda.max_memory_allocated(), fitted_parameters=False)
    write_json(args.out, result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('protocol'); p.add_argument('--model-revision', required=True); p.add_argument('--out', required=True)
    for name in ('run', 'forecast', 'preflight'):
        p = commands.add_parser(name)
        p.add_argument('--model-path', required=True); p.add_argument('--model-manifest', required=True)
        p.add_argument('--fleet-run-id', required=True); p.add_argument('--out', required=True)
        if name != 'forecast':
            p.add_argument('--data', required=True); p.add_argument('--protocol', required=True)
        if name != 'preflight':
            p.add_argument('--embedding-cache', required=True); p.add_argument('--max-runtime-seconds', type=float, default=18000)
        if name == 'run':
            p.add_argument('--folds', required=True); p.add_argument('--methods', choices=['both', 'frozen', 'lora'], default='both')
            p.add_argument('--fold-ids', nargs='+', default=['all']); p.add_argument('--resume', action='store_true')
        if name == 'forecast':
            p.add_argument('--fit', required=True); p.add_argument('--metadata', required=True); p.add_argument('--split', required=True)
    args = parser.parse_args(argv)
    if args.command == 'protocol':
        result = protocol_spec(args.model_revision); write_json(args.out, result)
    else:
        try:
            result = globals()[args.command](args)
        except BaseException as exc:
            if args.command == 'run':
                output = safe_path(args.out); output.mkdir(parents=True, exist_ok=True)
                write_json(output/'status.json', dict(status='paused_runtime_limit' if isinstance(exc, TimeoutError) else 'error',
                    created_utc=now(), error_type=type(exc).__name__, message=str(exc), fleet_run_id=args.fleet_run_id), replace=True)
            raise
    print(json.dumps(result, allow_nan=False))


if __name__ == '__main__':
    main()
