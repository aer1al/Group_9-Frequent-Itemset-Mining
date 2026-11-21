"""Control number of records & domain; vary average transaction length."""
import csv
from random import Random
from scripts.benchmark import measured,ROOT

def main():
    results=[]
    for width in (3,5,7,9,11):
        rng=Random(2026)
        data=[rng.sample(range(60),width) for _ in range(600)]
        row,_=measured(data,0.04,'bitset',200000)
        results.append({'avg_transaction_length':width,**row})
        print(results[-1])
    dest=ROOT/'results/length_experiment.csv'
    with dest.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=results[0].keys());w.writeheader();w.writerows(results)

if __name__=='__main__':main()
