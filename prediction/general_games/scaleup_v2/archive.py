"""Archive the released study source and fingerprint reproducibility artifacts."""
import hashlib
import importlib
import importlib.metadata
from pathlib import Path
import platform
import tarfile
from prediction import modeling
from prediction.io_utils import read_json,write_json,now,digest
from . import ROOT,DATA,STUDY
from .collection import source_hashes
from prediction.general_games.native import library_hashes,environment_record


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def versions():
    result={}
    for name in ('textarena','numpy','scipy','scikit-learn','matplotlib','openai','joblib','threadpoolctl'):
        module=importlib.import_module('sklearn' if name=='scikit-learn' else name)
        try:value=importlib.metadata.version(name);source='distribution metadata'
        except importlib.metadata.PackageNotFoundError:value=getattr(module,'__version__',None);source='module __version__ (vendored package without distribution metadata)'
        result[name]=dict(version=value,source=source,path=module.__file__)
    return result


def build():
    repo=ROOT.parents[2];m=read_json(DATA/'manifest.json')
    assert m['source_hashes']==source_hashes() and m['environment']==environment_record()
    assert read_json(DATA/'native-source-hashes.json')==library_hashes()
    with tarfile.open(DATA/'collection-source.tar.gz') as tar:
        for name,value in m['source_hashes'].items():assert digest(tar.extractfile(name).read().decode())==value
    with tarfile.open(DATA/'native-source.tar.gz') as tar:
        for name,value in library_hashes().items():assert hashlib.sha256(tar.extractfile(name).read()).hexdigest()==value
    assert sha(DATA/'native-source.tar.gz')==m['native_archive_sha256']
    sources={repo/name for name in source_hashes()};sources.update(ROOT.glob('*.py'))
    sources.add(repo/'prediction/modeling.py')
    viewer=repo/'prediction/scaleup/viewer'
    for pattern in ('*.py','*.html','*.js','*.css'):sources.update(viewer.glob(pattern))
    source_hash={str(p.relative_to(repo)):sha(p) for p in sorted(sources)}
    path=STUDY/'reproduction-source.tar.gz'
    with tarfile.open(path,'w:gz') as tar:
        for p in sorted(sources):tar.add(p,arcname=str(p.relative_to(repo)))
    artifacts=[DATA/name for name in ('catalog.json','manifest.json','mechanics.v2.json','mechanics-revision.json','native-source.tar.gz','collection-source.tar.gz','TEXTARENA_LICENSE','DATASET_CARD.md')]
    artifacts += [STUDY/name for name in ('protocol.json','training/plan.json','test/plan.json','prediction/frozen.json','summary.json','predictions.json','all-episodes.jsonl','all-actions.jsonl','REPORT.md')]
    artifacts += [STUDY/'prediction'/name for name in read_json(STUDY/'prediction/frozen.json')['artifact_hashes']]
    artifacts += [STUDY/'prediction/supplemental-pooled-n440'/name for name in ('manifest.json','groups.evaluator.json','test-predictions.json','audit.json')]
    artifacts += sorted((STUDY/'figures').glob('*'))
    raw={str(p.relative_to(ROOT)):sha(p) for folder in STUDY.rglob('raw_calls') for p in sorted(folder.glob('*.json'))}
    write_json(STUDY/'raw-call-sha256.json',raw);artifacts.append(STUDY/'raw-call-sha256.json')
    result=dict(created=now(),python=platform.python_version(),versions=versions(),
        source_archive_sha256=sha(path),source_files=source_hash,artifact_sha256={str(p.relative_to(ROOT)):sha(p) for p in artifacts},native_and_collection_archives_verified=True,
        note='Prediction manifests/frozen.json record the prospective freeze. This later release manifest fingerprints the audited readout and source; it is not a replacement for that earlier chronology.')
    write_json(STUDY/'reproduction.json',result);return dict(source_files=len(sources),artifacts=len(artifacts),versions=result['versions'])


if __name__=='__main__':print(build())
