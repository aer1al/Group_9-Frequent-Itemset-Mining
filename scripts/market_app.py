from pathlib import Path
from scripts.benchmark import ROOT
from src.market import load_ecommerce,read_name_map,top_rules,save_rules

def main():
    filename=ROOT/'data/applications/ecommerce_timestamped.txt'
    namespath=ROOT/'data/applications/online_retail_item_names.txt'
    if not filename.exists() or not namespath.exists():
        raise SystemExit('Download application data: python -m scripts.download_data --names ecommerce ecommerce_names')
    transactions=load_ecommerce(filename)
    rules=top_rules(transactions,read_name_map(namespath),minsup=0.01,minconf=0.25,k=10)
    if not rules:print('No rules; consider different minsup/minconf and state reason.')
    save_rules(rules,ROOT/'results/market_top10.csv')
    for r in rules:print(r)
    print('Saved results/market_top10.csv')

if __name__=='__main__':main()
