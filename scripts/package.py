#!/usr/bin/env python3
"""Build deterministic source and portable skill archives from reviewed source paths."""
import argparse, hashlib, re, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/humancraft'
ROOTS=('.github','bench','benchmark','docs','evals','scripts','skills','tests','.gitignore','README.md','README.zh-CN.md','LICENSE','CONTRIBUTING.md','SECURITY.md','CHANGELOG.md')
ALLOWED={'.md','.py','.json','.html','.txt','.yml','.yaml','.log','.png','.zip','.js','.css'}
EXCLUDED={'.git','__pycache__','.venv','dist','local-eval-results','execution-logs','packets'}
def files(base, roots):
    for name in roots:
        p=base/name
        if not p.exists():raise ValueError(f'missing release path: {p}')
        for f in sorted(p.rglob('*')) if p.is_dir() else [p]:
            rel=f.relative_to(base)
            if any(x in EXCLUDED or x.startswith('.env') for x in rel.parts):continue
            if f.is_symlink():raise ValueError(f'symlink forbidden: {rel}')
            if not f.is_file():continue
            if f.suffix.lower() not in ALLOWED and f.name not in {'LICENSE','.gitignore'}:raise ValueError(f'unreviewed release type: {rel}')
            yield f,rel

def archive(dest, entries, prefix):
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f,rel in entries:
            info=zipfile.ZipInfo(prefix+'/'+rel.as_posix(),date_time=(2026,11,24,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,f.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(dest) as z:
        if z.testzip() is not None:raise ValueError('corrupt archive')
        paths=z.namelist()
        if len(paths)!=len(set(paths)):raise ValueError('duplicate paths')
        entry=prefix+('/SKILL.md' if prefix=='humancraft' else '/skills/humancraft/SKILL.md')
        if entry not in paths:raise ValueError('missing skill entry')
    return len(paths)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    version=re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$',(SKILL/'SKILL.md').read_text(),re.M).group(1)
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    outputs=[]
    for suffix,entries,prefix in [('skill',files(SKILL,('SKILL.md','LICENSE','references','assets','scripts')),'humancraft'),('full',files(ROOT,ROOTS),'HumanCraft-v'+version)]:
        dest=out/f'HumanCraft-v{version}-{suffix}.zip';n=archive(dest,entries,prefix);print(f'{dest.name}: {n} files');outputs.append(dest)
    (out/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}\n' for f in outputs),encoding='utf-8')
if __name__=='__main__':main()
