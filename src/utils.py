"""Parse plain SPMF FIM input and output. Only standard-library code."""
from pathlib import Path
import hashlib
import json


def read_transactions(path):
    """One transaction per line, whitespace separated integer item IDs.
    SPMF comment lines (#, %, @) are skipped; empty transactions retained.
    The sequential format (-1,-2) is intentionally rejected.
    """
    rows=[]
    for line_number, raw in enumerate(Path(path).read_text(encoding='utf-8-sig').splitlines(), 1):
        line=raw.strip()
        if line.startswith(('#','%','@')):
            continue
        if not line:
            rows.append([])
            continue
        try:
            row=[int(x) for x in line.split()]
        except ValueError as e:
            raise ValueError(f'Invalid integer in {path}:{line_number}') from e
        if -1 in row or -2 in row:
            raise ValueError(f'Likely sequential, not itemset data: {path}:{line_number}')
        rows.append(sorted(set(row)))
    if not rows:
        raise ValueError(f'No transactions in {path}')
    return rows


def write_fim_output(supports, path):
    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8') as f:
        for items in sorted(supports,key=lambda x:(len(x),x)):
            f.write(' '.join(map(str,items))+f' #SUP: {supports[items]}\n')


def read_fim_output(path):
    results={}
    for index,line in enumerate(Path(path).read_text(encoding='utf-8-sig').splitlines(),1):
        line=line.strip()
        if not line or line.startswith(('#','%','@')): continue
        if '#SUP:' not in line:
            raise ValueError(f'Missing #SUP: in {path}:{index}')
        left,right=line.split('#SUP:',1)
        key=tuple(sorted(int(x) for x in left.split()))
        if key in results: raise ValueError(f'Duplicate itemset in {path}:{index}')
        results[key]=int(right.strip())
    return results


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()


def write_json(obj,path):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str)+'\n',encoding='utf-8')
