"""Download the official RELEASE jar for external comparison, no SPMF code imported."""
from pathlib import Path
from urllib.request import Request,urlopen
from scripts.benchmark import ROOT
from src.utils import sha256

URL='https://www.philippe-fournier-viger.com/spmf/spmf.jar'

def main():
    target=ROOT/'tools/spmf.jar'
    target.parent.mkdir(exist_ok=True)
    if target.is_file() and target.stat().st_size>100000:
        print('Existing official release jar:',target,'SHA256:',sha256(target));return
    tmp=target.with_suffix('.download')
    try:
        with urlopen(Request(URL,headers={'User-Agent':'Mozilla/5.0'}),timeout=90) as response, tmp.open('wb') as fd:
            while True:
                chunk=response.read(1024*1024)
                if not chunk:break
                fd.write(chunk)
        with tmp.open('rb') as fd:
            if fd.read(2)!=b'PK':raise ValueError('Not a valid ZIP/JAR binary; check network/proxy')
        tmp.replace(target)
    finally:
        if tmp.exists():tmp.unlink()
    print('SPMF jar download:',URL,'bytes:',target.stat().st_size,'SHA256:',sha256(target))

if __name__=='__main__': main()
