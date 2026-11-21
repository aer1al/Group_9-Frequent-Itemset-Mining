"""Recompute source-side descriptive statistics, never substitute SPMF table values."""
import csv
from collections import Counter
from scripts.benchmark import ROOT,DATA
from src.utils import read_transactions,sha256

def main():
    rows=[]
    for dataset in DATA:
        path=ROOT/'data'/'benchmark'/f'{dataset}.txt'
        if not path.exists():raise SystemExit(f'Not downloaded: {path}')
        tx=read_transactions(path)
        items=set(x for t in tx for x in t)
        lengths=[len(x) for x in tx]
        rows.append({'dataset':dataset,'transactions':len(tx),'unique_items':len(items),
                     'avg_length':round(sum(lengths)/len(tx),4),'max_length':max(lengths),
                     'empty_transactions':sum(length==0 for length in lengths),
                     'sha256':sha256(path)})
    out=ROOT/'results/dataset_statistics.csv'
    with out.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    for row in rows:print(row)
    print('Saved:',out)

if __name__=='__main__':main()
