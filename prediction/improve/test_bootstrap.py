"""Pure bootstrap integrity checks; no Torch/model imports or real wheel installs."""
import os
import json
from pathlib import Path
import runpy
import stat
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

from prediction.improve import bootstrap as b


class BootstrapTests(unittest.TestCase):
    @staticmethod
    def fake_torch():
        flags = {'cudnn': True, 'flash': True, 'memory_efficient': False, 'math': True}
        cuda = SimpleNamespace(cudnn_sdp_enabled=lambda: flags['cudnn'],
            flash_sdp_enabled=lambda: flags['flash'], mem_efficient_sdp_enabled=lambda: flags['memory_efficient'],
            math_sdp_enabled=lambda: flags['math'], enable_cudnn_sdp=lambda value: flags.update(cudnn=value))
        return SimpleNamespace(backends=SimpleNamespace(cuda=cuda), __version__='synthetic', __file__='synthetic-origin')

    def test_policy_changes_only_cudnn_and_smoke_matches_real_attention_shape(self):
        result = b.apply_sdpa_policy(self.fake_torch())
        self.assertTrue(result['before']['cudnn']); self.assertFalse(result['after']['cudnn'])
        for key in ('flash', 'memory_efficient', 'math'):
            self.assertEqual(result['before'][key], result['after'][key])
        config = b.tiny_config()
        self.assertEqual(config['head_dim'], 128)
        self.assertEqual(config['num_attention_heads'] // config['num_key_value_heads'], 4)

    def test_generated_wrapper_sets_policy_before_worker_and_preserves_argv_and_bytes(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR', '/shared/allie/home/.codex/tmp')) as name:
            root = Path(name); worker = root / 'worker.py'; entry = root / 'worker_entry.py'
            worker.write_text("import sys, torch\nassert not torch.backends.cuda.cudnn_sdp_enabled()\n"
                              "assert sys.argv[1:] == ['--run-root', 'synthetic', '--resume']\n")
            old = worker.read_bytes(); fake = self.fake_torch()
            entry_hash = b.write_worker_entry(entry, worker, (fake.__version__, fake.__file__))
            with patch.dict(sys.modules, {'torch': fake}), patch.object(sys, 'argv', [str(entry), '--run-root', 'synthetic', '--resume']), patch.dict(os.environ, {'FLEET_RUN_NAME': 'synthetic', 'PREDICTION_FLEET_TRAINING_RUN': '1'}):
                runpy.run_path(str(entry), run_name='__main__')
            self.assertEqual(worker.read_bytes(), old)
            record = json.loads((root / 'worker-backend.json').read_text())
            self.assertEqual(record['entry_sha256'], entry_hash)
            self.assertEqual(record['worker_sha256'], b.sha(worker))
            self.assertFalse(record['after']['cudnn'])
            worker.write_text('raise RuntimeError("must never execute changed worker")\n')
            with patch.dict(sys.modules, {'torch': fake}), patch.dict(os.environ, {'FLEET_RUN_NAME': 'synthetic', 'PREDICTION_FLEET_TRAINING_RUN': '1'}):
                with self.assertRaisesRegex(RuntimeError, 'Frozen worker bytes'):
                    runpy.run_path(str(entry), run_name='__main__')

    def test_fleet_guard_precedes_output_creation(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, 'Fleet'):
                b.fleet_paths('/shared/allie/example', None)

    def test_wheel_checksum_and_native_members(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR', '/shared/allie/home/.codex/tmp')) as name:
            root = Path(name); wheel = root / 'synthetic.whl'; out = root / 'overlay'
            with zipfile.ZipFile(wheel, 'w') as archive:
                archive.writestr('scipy/__init__.py', '# synthetic\n')
                archive.writestr('scipy.libs/libsynthetic.so', b'not a real shared library')
            with self.assertRaisesRegex(ValueError, 'SHA256'):
                b.extract_wheel(wheel, out, '0' * 64)
            self.assertFalse(out.exists())
            files = b.extract_wheel(wheel, out, b.sha(wheel))
            self.assertEqual(set(files), {'scipy/__init__.py', 'scipy.libs/libsynthetic.so'})
            with self.assertRaises(FileExistsError):
                b.extract_wheel(wheel, out, b.sha(wheel))

    def test_rejects_traversal_torch_shadow_and_symlinks_before_writing(self):
        cases = ['../escape', '/absolute', 'torch/__init__.py', 'scipy/a.pth', 'scipy/link']
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR', '/shared/allie/home/.codex/tmp')) as name:
            root = Path(name)
            for i, member in enumerate(cases):
                wheel = root / f'{i}.whl'; out = root / f'out{i}'
                with zipfile.ZipFile(wheel, 'w') as archive:
                    archive.writestr('scipy/__init__.py', '')
                    info = zipfile.ZipInfo(member)
                    if member.endswith('/link'):
                        info.external_attr = (stat.S_IFLNK | 0o777) << 16
                    archive.writestr(info, 'bad')
                with self.assertRaisesRegex(ValueError, 'Unsafe'):
                    b.extract_wheel(wheel, out, b.sha(wheel))
                self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main()
