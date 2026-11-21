"""Download authoritative source files and write provenance JSON + SHA256.
Never silently use a mirror. Raw data stays unmodified.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from datetime import datetime,timezone
import argparse
import json
from zipfile import ZipFile
from io import BytesIO
from src.utils import sha256,write_json

ROOT=Path(__file__).resolve().parents[1]
SOURCES={
 'foodmart': ('https://www.philippe-fournier-viger.com/spmf/publicdatasets/foodmartFIM.txt','data/benchmark/foodmart.txt','SPMF public FIM dataset, real retail'),
 'c20d10k': ('https://www.philippe-fournier-viger.com/spmf/publicdatasets/c20d10k.txt','data/benchmark/c20d10k.txt','SPMF synthetic FIM dataset'),
 't25i10d10k': ('https://www.philippe-fournier-viger.com/spmf/publicdatasets/t25i10d10k.txt','data/benchmark/t25i10d10k.txt','SPMF synthetic FIM dataset'),
 'BMS_WebView_1': ('https://www.philippe-fournier-viger.com/spmf/publicdatasets/BMS1_itemset_mining.txt','data/benchmark/BMS_WebView_1.txt','SPMF web clickstream FIM dataset, originally FIMI'),
 'ecommerce': ('https://www.philippe-fournier-viger.com/spmf/publicdatasets/ecommerce_time_without_utility.txt','data/applications/ecommerce_timestamped.txt','SPMF real ecommerce records with timestamp suffix'),
 'ecommerce_names': ('https://www.philippe-fournier-viger.com/spmf/publicdatasets/online_retail_item_names.txt','data/applications/online_retail_item_names.txt','SPMF item id -> original product descriptions'),
 'optdigits': ('https://archive.ics.uci.edu/ml/machine-learning-databases/optdigits/optdigits.tra','data/applications/optdigits.tra','UCI Optical Recognition of Handwritten Digits, training split'),
}

def download(names):
    manifest={}
    outpath=ROOT/'data'/'download_manifest.json'
    existing=json.loads(outpath.read_text(encoding='utf-8')) if outpath.exists() else {}
    for name in names:
        url,rel,desc=SOURCES[name]
        path=ROOT/rel;path.parent.mkdir(parents=True,exist_ok=True)
        downloaded_from = url
        acquisition_method = 'direct_download'
        if not path.is_file() or path.stat().st_size==0:
            print('Downloading',name,url,flush=True)
            request=Request(url,headers={'User-Agent':'Mozilla/5.0 (academic research data provenance)'})
            temporary=path.with_suffix(path.suffix+'.partial')
            try:
                try:
                    with urlopen(request,timeout=90) as response, temporary.open('wb') as out:
                        while True:
                            block=response.read(1024*1024)
                            if not block: break
                            out.write(block)
                except Exception:
                    if name != 'optdigits':raise
                    # UCI's legacy URL may no longer serve the .tra file.
                    # Official UCI modern distribution hosts the original .tra in a ZIP.
                    fallback='https://archive.ics.uci.edu/static/public/80/optical%2Brecognition%2Bof%2Bhandwritten%2Bdigits.zip'
                    print('Legacy UCI URL unavailable; trying UCI official ZIP:',fallback,flush=True)
                    with urlopen(Request(fallback,headers={'User-Agent':'Mozilla/5.0'}),timeout=120) as response:
                        archive=response.read()
                    with ZipFile(BytesIO(archive)) as z:
                        choices=[file for file in z.namelist() if file.lower().endswith('optdigits.tra')]
                        if len(choices)!=1:raise ValueError('Unexpected UCI ZIP: missing/ambiguous optdigits.tra')
                        temporary.write_bytes(z.read(choices[0]))
                    downloaded_from=fallback+'#optdigits.tra'
                with temporary.open('rb') as downloaded:
                    preview=downloaded.read(512).lstrip().lower()
                if not preview or preview.startswith((b'<!doctype',b'<html',b'<head')):
                    raise ValueError('Downloaded empty/HTML error page, not source data: '+url)
                temporary.replace(path)
            finally:
                if temporary.exists():temporary.unlink()
        else:
            print('Existing',path,flush=True)
            old = existing.get(name,{})
            acquisition_method = ('existing_with_matching_manifest'
                    if old.get('sha256') == sha256(path) and old.get('acquisition_method') != 'preexisting_unverified'
                    else 'preexisting_unverified')
        manifest[name]={'source_url':downloaded_from,'acquisition_method':acquisition_method,
                        'description':desc,'local_path':rel,
                        'size_bytes':path.stat().st_size,'sha256':sha256(path),
                        'recorded_utc':datetime.now(timezone.utc).isoformat()}
    existing.update(manifest);write_json(existing,outpath)
    print('Provenance:',outpath)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--names',nargs='+',choices=sorted(SOURCES),default=list(SOURCES))
    a=p.parse_args();download(a.names)
