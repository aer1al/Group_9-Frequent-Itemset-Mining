"""Reproducible, measured Eclat experiments on official FIM benchmarks.
No reference algorithm source code is imported. All rows contain real timings or a failure.
"""
import argparse
import csv
import gc
import platform
import statistics
import sys
import time
import tracemalloc
from collections import Counter
from pathlib import Path
from src.algorithm.eclat import mine, min_support_count
from src.utils import read_transactions, sha256

ROOT = Path(__file__).resolve().parents[1]
DATA = ['foodmart', 'c20d10k', 't25i10d10k', 'BMS_WebView_1']
# Six support thresholds relative to the most frequent singleton support.
# Avoid a fixed 0.9 on sparse datasets: it yields zero patterns at all levels.
RATIOS = (1.00, 0.85, 0.70, 0.55, 0.42, 0.32)

def proposed_min_counts(transactions, quick=False, ratios=RATIOS):
    counts = Counter(x for transaction in transactions for x in set(transaction))
    if not counts:
        raise ValueError('All transactions are empty')
    highest = max(counts.values())
    # Generate distinct thresholds even if maximum support is small.
    thresholds = []
    for factor in ratios:
        count = max(1, round(highest * factor))
        if count not in thresholds:
            thresholds.append(count)
    if len(thresholds) < 6 and not quick:
        raise ValueError('Cannot generate six different thresholds on this dataset')
    return thresholds[:1] if quick else thresholds

def measured(transactions, ms, variant, cap=None):
    gc.collect()
    tracemalloc.start()
    start = time.perf_counter()
    supports = None
    error = ''
    try:
        supports = mine(transactions, ms, variant, max_results=cap).supports
        state = 'ok'
    except (RuntimeError, RecursionError, MemoryError) as exc:
        state = 'invalid'
        error = f'{type(exc).__name__}: {exc}'
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {'backend': variant, 'minsup': ms,
            'seconds': round(elapsed, 6), 'peak_python_mb': round(peak / 1048576, 4),
            'itemset_count': len(supports) if supports is not None else '',
            'status': state, 'error': error}, supports

def run(args):
    dest = ROOT / args.output
    dest.parent.mkdir(parents=True, exist_ok=True)
    columns = ['dataset', 'dataset_sha256', 'transactions', 'unique_items', 'max_singleton_support',
               'minsup', 'min_count', 'minsup_percentage', 'backend', 'seconds',
               'peak_python_mb', 'itemset_count', 'status', 'error', 'baseline_match',
               'python_version', 'platform']
    with dest.open('w', newline='', encoding='utf-8') as fd:
        writer = csv.DictWriter(fd, fieldnames=columns)
        writer.writeheader()
        for label in args.datasets:
            inp = ROOT / 'data' / 'benchmark' / (label + '.txt')
            if not inp.exists():
                raise SystemExit(f'Missing official dataset: {inp}. Run python -m scripts.download_data')
            data = read_transactions(inp)
            frequencies = Counter(x for record in data for x in record)
            values = proposed_min_counts(data, quick=args.quick)
            print(f'\n{label}: {len(data)} transactions, {len(frequencies)} items, thresholds={values}', flush=True)
            for threshold in values:
                baseline = None
                for backend in ('set', 'bitset'):
                    result, supports = measured(data, threshold, backend, args.cap)
                    if backend == 'set':
                        baseline = supports
                        comparison = 'baseline'
                    else:
                        comparison = ('true' if supports is not None and baseline == supports
                                      else 'false_or_invalid')
                    result.update(dataset=label, dataset_sha256=sha256(inp),
                                  transactions=len(data), unique_items=len(frequencies),
                                  max_singleton_support=max(frequencies.values()),
                                  min_count=threshold, minsup_percentage=round(100*threshold/len(data), 8),
                                  baseline_match=comparison, python_version=sys.version.split()[0],
                                  platform=platform.platform())
                    writer.writerow(result)
                    fd.flush()
                    print(label, threshold, backend, result['itemset_count'], result['seconds'],
                          result['status'], flush=True)
    print('Saved:', dest)
    print('Peak memory uses tracemalloc (Python allocations); not operating-system peak RSS.')
    return dest

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datasets', nargs='+', default=DATA, choices=DATA)
    parser.add_argument('--cap', type=int, default=1000000)
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--output', default='results/benchmark.csv')
    run(parser.parse_args())

if __name__ == '__main__':
    main()
