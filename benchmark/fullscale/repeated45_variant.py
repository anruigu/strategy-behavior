"""Explicit fresh Qwen medium variant; preserves the xhigh attempt unchanged."""
import runpy
from pathlib import Path
r=runpy.run_path(str(Path(__file__).with_name('repeated45.py')),run_name='variant_helpers')
name='qwen-3.8-27b-medium'
r['CONFIGS'][name]=r['replace'](r['CONFIGS']['qwen-3.8-27b'],model_id=name,reasoning_effort='medium')
if __name__=='__main__':r['run'](name,6)
