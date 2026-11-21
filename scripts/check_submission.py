"""Check non-inventable external submission requirements and observed results."""
from pathlib import Path
import csv
from collections import defaultdict
from scripts.benchmark import ROOT,DATA


def get_rows(path):
    if not path.exists(): return []
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))


def verify():
    checks=[]
    def check(ok,label):checks.append((bool(ok),label))
    files=get_rows(ROOT/'results'/'benchmark.csv')
    refs=get_rows(ROOT/'results'/'spmf_comparison.csv')
    by_name=defaultdict(set)
    for row in files:
        if row['status']=='ok' and row['backend']=='bitset':by_name[row['dataset']].add(row['min_count'])
    check(all(len(by_name[name])>=6 for name in DATA),'4 official benchmarks x at least 6 valid minsup points')
    check(all((ROOT/'data/benchmark'/f'{name}.txt').is_file() for name in DATA), '4 official raw dataset files present')
    check(len(refs)>=25 and all(row['status']=='ok' and row['exact_match']=='True' for row in refs),
          'SPMF matches EVERY support + itemset on 4x6 comparisons + 1 toy')
    check(len([r for r in get_rows(ROOT/'results/rss_memory.csv') if r['status']=='ok'])>=8,
          'True isolated peak process RSS for 4 datasets x 2 backends')
    check((ROOT/'results/scalability.csv').is_file() and
          len(get_rows(ROOT/'results/scalability.csv'))>=5,'5 real scalability measures')
    check(len(get_rows(ROOT/'results/length_experiment.csv'))>=5,'5 transaction-length measures')
    check(len(get_rows(ROOT/'results/market_top10.csv'))>=10,'Top-10 ECommerce association rules')
    check(bool(get_rows(ROOT/'results/visual_patterns.csv')),'Real UCI visual patterns output')
    check((ROOT/'data/download_manifest.json').is_file(),'Provenance SHA256 manifest exists')
    content=(ROOT/'README.md').read_text(encoding='utf-8')
    check('https://github.com/YOUR_ACCOUNT/YOUR_REPO' not in content and
          'YOUR_ACCOUNT' not in content, 'Real GitHub public repository URL filled')
    check('CHUA_CO_LINK' not in content and 'COLAB_LINK_HERE' not in content,
          'Real public Colab URL filled')
    latex=(ROOT/'docs/Report.tex').read_text(encoding='utf-8')
    check('[Điền họ tên và MSSV]' not in latex and '[Điền email]' not in latex,
          'Student identity completed in Report.tex')
    check((ROOT/'docs/Report.pdf').is_file(), 'Report.pdf exists; PDF page count must be inspected')
    return checks


def main():
    checks=verify()
    for passed,label in checks:print(('[OK] ' if passed else '[CẦN LÀM] ')+label)
    ok=sum(x for x,_ in checks)
    print(f'{ok}/{len(checks)} checks satisfied. Not a grading guarantee.')
    Path(ROOT/'results'/'submission_check.txt').write_text('\n'.join(
         ('PASS' if p else 'MISSING')+' | '+label for p,label in checks)+'\n',encoding='utf-8')

if __name__=='__main__':main()
