"""CLI: python -m src.cli data/toy/baskets.txt --minsup 0.4 --output results/fim.txt"""
import argparse
from .algorithm.eclat import mine
from .utils import read_transactions,write_fim_output

def main():
    p=argparse.ArgumentParser(description='Original implementation of Eclat')
    p.add_argument('input',help='SPMF transaction TXT file')
    p.add_argument('--minsup',default='0.4',help='fraction (0,1], or absolute integer e.g. 3')
    p.add_argument('--backend',choices=['set','bitset'],default='bitset')
    p.add_argument('--output',default='results/itemsets.txt')
    p.add_argument('--max-results',type=int,default=None)
    a=p.parse_args()
    threshold=int(a.minsup) if a.minsup.isdigit() else float(a.minsup)
    result=mine(read_transactions(a.input),threshold,a.backend,a.max_results)
    write_fim_output(result.supports,a.output)
    print(f'{result.transactions=} {result.min_count=} itemsets={len(result.supports)} backend={a.backend}; output={a.output}')

if __name__=='__main__': main()
