from pathlib import Path
import csv
from scripts.benchmark import ROOT
from src.visual import load_optdigits,mine_visual_patterns


def main():
    path=ROOT/'data/applications/optdigits.tra'
    if not path.exists():raise SystemExit('Run python -m scripts.download_data --names optdigits')
    images,_=load_optdigits(path,limit=600)
    result,transactions,centers=mine_visual_patterns(images,k_words=12,minsup=0.45)
    print('images',len(images),'codebook size',len(centers),'patterns',len(result.supports))
    output=ROOT/'results/visual_patterns.csv'
    with output.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['visual_words','support_count','support_fraction'])
        for items,sup in sorted(result.supports.items(),key=lambda v:(-v[1],-len(v[0]),v[0])):
            w.writerow([' '.join(map(str,items)),sup,f'{sup/len(images):.6f}'])
    print('Saved',output)
    print('Visual word IDs are not human-interpretable objects without inspecting codebook patches.')

if __name__=='__main__':main()
