import argparse
from src.utils import read_fim_output

def main():
    p=argparse.ArgumentParser()
    p.add_argument('ours');p.add_argument('spmf');a=p.parse_args()
    ours=read_fim_output(a.ours);spmf=read_fim_output(a.spmf)
    wrong={k:(ours.get(k),spmf.get(k)) for k in ours.keys()|spmf.keys() if ours.get(k)!=spmf.get(k)}
    print('OURS:',len(ours),'SPMF:',len(spmf),'MATCH:',len(wrong)==0)
    print('Differences (first 10):',list(wrong.items())[:10])
    if wrong: raise SystemExit(1)

if __name__=='__main__':main()
