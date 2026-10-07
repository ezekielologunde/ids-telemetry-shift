"""Stream official BagIt CSV archive; verify payload checksums and time coverage."""
import argparse
import collections
import hashlib
import json
import pathlib
import zipfile
import pandas as pd


def audit(path):
    path = pathlib.Path(path)
    with path.open('rb') as archive:
        digest = hashlib.file_digest(archive, 'sha256').hexdigest()
    result = {"archive": path.name, "archive_sha256": digest}
    with zipfile.ZipFile(path) as z:
        manifest = next(n for n in z.namelist() if n.endswith('/manifest-sha1.txt'))
        root = manifest.rsplit('/', 1)[0] + '/'
        verified = []
        for line in z.read(manifest).decode().splitlines():
            expected, name = line.split(maxsplit=1)
            with z.open(root + name) as stream:
                actual = hashlib.file_digest(stream, 'sha1').hexdigest()
            if actual != expected:
                raise ValueError(f'Checksum mismatch: {name}')
            verified.append({"path": name, "sha1": actual})
        result['verified_payloads'] = verified
        csvname = next(n for n in z.namelist() if '/data/NF-' in n and n.endswith('.csv'))
        labels, attacks, days = collections.Counter(), collections.Counter(), collections.Counter()
        rows = 0
        minimum, maximum = None, None
        invalid_intervals = 0
        missing = collections.Counter()
        with z.open(csvname) as raw:
            for df in pd.read_csv(raw, chunksize=100000):
                result.setdefault('columns', df.columns.tolist())
                rows += len(df)
                labels.update(df['Label'].astype(str))
                attacks.update(df['Attack'].astype(str))
                start = pd.to_numeric(df['FLOW_START_MILLISECONDS'], errors='coerce')
                end = pd.to_numeric(df['FLOW_END_MILLISECONDS'], errors='coerce')
                lo, hi = int(start.min()), int(end.max())
                minimum = lo if minimum is None else min(minimum, lo)
                maximum = hi if maximum is None else max(maximum, hi)
                invalid_intervals += int(((end < start) | start.isna() | end.isna()).sum())
                day = pd.to_datetime(start, unit='ms', utc=True).dt.strftime('%Y-%m-%d')
                days.update(day + '|' + df['Label'].astype(str))
                missing.update({k: int(v) for k, v in df.isna().sum().items()})
        result.update(rows=rows, labels=dict(labels), attacks=dict(attacks), day_label_counts=dict(sorted(days.items())), start_min_ms=minimum, end_max_ms=maximum, invalid_intervals=invalid_intervals, missing_counts=dict(missing))
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('archive')
    p.add_argument('--output', required=True)
    a = p.parse_args()
    result = audit(a.archive)
    out = pathlib.Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['rows', 'labels', 'day_label_counts', 'invalid_intervals']}))
