"""Uniform bounded-memory priority sample. Selection never uses labels."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd

def prepare(archive, output, size=100000):
    rng = np.random.default_rng(20261007)
    selected = None
    total = 0
    with zipfile.ZipFile(archive) as z:
        name = next(n for n in z.namelist() if '/data/NF-' in n and n.endswith('.csv'))
        with z.open(name) as stream:
            for frame in pd.read_csv(stream, chunksize=100000):
                frame['_row'] = np.arange(total, total + len(frame))
                total += len(frame)
                frame['_priority'] = rng.random(len(frame))
                selected = frame if selected is None else pd.concat([selected, frame], ignore_index=True)
                selected = selected.nsmallest(size, '_priority')
    selected = selected.sort_values(['FLOW_START_MILLISECONDS', '_row']).drop(columns='_priority')
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    selected.to_pickle(output)
    with output.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    print(json.dumps({'source': str(archive), 'member': name, 'total': total, 'sample':len(selected), 'sample_sha256':digest, 'output':str(output)}), flush=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('archive')
    p.add_argument('output')
    p.add_argument('--size', type=int, default=100000)
    a = p.parse_args()
    prepare(a.archive, a.output, a.size)
