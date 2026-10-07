"""Use the existing verified portable Tectonic cache in an isolated container."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--compiler-dir',type=Path,required=True);a=p.parse_args()
build=root/'paper/build';build.mkdir(parents=True,exist_ok=True)
compiler=a.compiler_dir.resolve()
image='python@sha256:0dd364ba7e10242f07755449e3a3d0e35f9efd987952737b90def6709ab0c5ce'
assert hashlib.sha256((compiler/'tectonic').read_bytes()).hexdigest()=='a98aa59ad5c1df39a6c9e56cbfc5088f2b11d6c179c0130b97998e4bd46a46da'
cmd=['docker','run','--rm','--name','ids-telemetry-paper-build','--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--cpus','2','--memory','2g','--pids-limit','64','--tmpfs','/tmp:rw,exec,size=536870912','--env','HOME=/tmp','--env','XDG_CACHE_HOME=/compiler/cache','--mount',f'type=bind,source={compiler},target=/compiler,readonly','--mount',f'type=bind,source={root / "paper"},target=/input,readonly','--mount',f'type=bind,source={build},target=/output',image,'sh','-c','cp /compiler/tectonic /tmp/tectonic && chmod +x /tmp/tectonic && /tmp/tectonic --keep-logs --outdir /output /input/main.tex']
r=subprocess.run(cmd,capture_output=True,encoding='utf-8',errors='replace',timeout=180)
(build/'stdout.txt').write_text(r.stdout);(build/'stderr.txt').write_text(r.stderr)
receipt={'command':cmd,'exit_code':r.returncode,'source_sha256':hashlib.sha256((root/'paper/main.tex').read_bytes()).hexdigest()}
if r.returncode==0:
    pdf=(build/'main.pdf').read_bytes();(root/'paper/main.pdf').write_bytes(pdf);receipt['pdf_sha256']=hashlib.sha256(pdf).hexdigest()
(build/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(r.stdout,r.stderr);raise SystemExit(r.returncode)
