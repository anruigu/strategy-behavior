import importlib.util
from pathlib import Path

from benchmark.clients import write_json


def test_plot_failure_is_recorded_without_stopping_inference(tmp_path):
    path = Path(__file__).with_name('sa_dose_campaign.py')
    spec = importlib.util.spec_from_file_location('sa_dose_campaign', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def broken_plot(out):
        raise ValueError('test: negative error bar')

    assert not module.refresh_figures(tmp_path, broken_plot, write_json, lambda: 'test')
    assert 'negative error bar' in (tmp_path / 'plot-status.json').read_text()
    assert module.refresh_figures(tmp_path, lambda out: None, write_json, lambda: 'test')
    assert '"status": "ok"' in (tmp_path / 'plot-status.json').read_text()
