"""Same seed, 10/25/50/75/100% transactions, timed from scratch."""
from pathlib import Path
import csv, random
from src.utils import read_transactions
from scripts.benchmark import measured,proposed_min_counts,ROOT

def main():
    path=ROOT/'data/benchmark/BMS_WebView_1.txt'
    if not path.exists(): raise SystemExit('Run python -m scripts.download_data first')
    data=read_transactions(path)
    ids=list(range(len(data)));random.Random(2026).shuffle(ids)
    # Fixed relative minsup across all subsamples; derive from full data to avoid empty output.
    full_min_count = proposed_min_counts(data)[3]
    relative_min_support = full_min_count / len(data)
    out=[]
    for share in (0.10,0.25,0.50,0.75,1.00):
        sample=[data[i] for i in ids[:max(1,round(share*len(data)))]]
        row,_=measured(sample,relative_min_support,'bitset',1000000)
        out.append({'fraction':share,'transactions':len(sample),**row})
        print(out[-1])
    dest=ROOT/'results/scalability.csv'
    with dest.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=out[0].keys());w.writeheader();w.writerows(out)

if __name__=='__main__':main()
