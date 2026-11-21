"""Chapter 3 application #1. Timestamped SPMF ecommerce -> baskets."""
from pathlib import Path
import csv
from .algorithm.eclat import mine
from .rules import make_rules


def load_ecommerce(path, limit=None):
    """SPMF ecommerce format: id id ... lastid:unix_timestamp.
    Timestamp denotes transaction metadata, NOT another item.
    """
    transactions=[]
    for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
        line=line.strip()
        if not line or line[0] in '@#%':continue
        items,sep,timestamp=line.rpartition(':')
        if not sep: raise ValueError('Missing :timestamp suffix in ecommerce file')
        int(timestamp) # validation; timestamp is not an item
        transactions.append(sorted({int(i) for i in items.split()}))
        if limit and len(transactions)>=limit:break
    return transactions


def read_name_map(path):
    names={}
    for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
        if not line.startswith('@ITEM='):continue
        _,_,payload=line.partition('@ITEM=')
        item,sep,label=payload.partition('=')
        if sep:
            try: names[int(item)]=label.strip()
            except ValueError: pass
    return names


def top_rules(data, names=None, minsup=0.012,minconf=0.3,k=10):
    result=mine(data,minsup,'bitset',max_results=1000000)
    rules=make_rules(result.supports,len(data),minconf)
    def human(items):return ' + '.join((names or {}).get(x,f'item_{x}') for x in items)
    return [{'X':human(r.antecedent),'Y':human(r.consequent),'support':round(r.support,5),
             'confidence':round(r.confidence,5),'lift':round(r.lift,5)} for r in rules[:k]]


def save_rules(rows,path):
    dest=Path(path);dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('w',encoding='utf-8-sig',newline='') as f:
        fieldnames=['X','Y','support','confidence','lift']
        w=csv.DictWriter(f,fieldnames=fieldnames);w.writeheader();w.writerows(rows)
