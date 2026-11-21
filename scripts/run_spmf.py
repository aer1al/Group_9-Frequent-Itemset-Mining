"""Execute the official SPMF jar as an EXTERNAL reference, never import its code.
Run all benchmark (dataset, threshold) configurations and compare every itemset+support.
"""
import argparse
import csv
import platform
import subprocess
import time
from pathlib import Path
from src.algorithm.eclat import mine
from src.utils import read_transactions, read_fim_output, write_fim_output
from scripts.benchmark import ROOT


def compare_maps(a, b):
    keys = set(a) | set(b)
    matches = sum(a.get(key) == b.get(key) for key in keys)
    return {'reference_count': len(b), 'ours_count': len(a),
            'matched_patterns': matches, 'total_unique_patterns': len(keys),
            'matching_rate': (matches / len(keys) if keys else 1.0),
            'exact_match': a == b}


def run_spmf_jar(jar, input_path, output_path, min_count, transaction_count, timeout):
    # SPMF documents a PERCENT argument, not integer minsup.
    # Use an interior point of ((k-1)/n,k/n] so floating-point conversion
    # cannot bump the absolute support count from k to k+1.
    percent = 100.0 * (min_count - .25) / transaction_count
    command = ['java', '-jar', str(jar.resolve()), 'run', 'Eclat',
               str(input_path.resolve()), str(output_path.resolve()),
               f'{percent:.12f}%']
    began = time.perf_counter()
    completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    duration = time.perf_counter() - began
    if completed.returncode:
        raise RuntimeError(f'SPMF exit code={completed.returncode}: {completed.stderr[-900:]}')
    if not output_path.is_file():
        raise RuntimeError('SPMF returned 0 but produced no output file')
    return round(duration, 6), command


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--jar', required=True, help='Locally downloaded official spmf.jar file')
    p.add_argument('--benchmark', default='results/benchmark.csv')
    p.add_argument('--timeout', type=int, default=900)
    args = p.parse_args()
    jar = Path(args.jar)
    if not jar.is_file(): raise SystemExit(f'Missing jar: {jar}. See official SPMF download page.')
    source = ROOT / args.benchmark
    if not source.exists():raise SystemExit('Run python -m scripts.benchmark first')
    with source.open(encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    jobs = {}
    for row in rows:
        if row['status'] != 'ok': continue
        jobs[(row['dataset'], int(row['min_count']))] = row
    folder = ROOT/'results'/'reference_spmf'
    folder.mkdir(parents=True, exist_ok=True)
    outpath = ROOT/'results'/'spmf_comparison.csv'
    with outpath.open('w', newline='', encoding='utf-8') as fd:
        fields=['dataset','min_count','minsup_percentage','transactions','status',
                'spmf_seconds_with_jvm_start','reference_count','ours_count',
                'matched_patterns','total_unique_patterns','matching_rate','exact_match',
                'error','spmf_output','command']
        wr = csv.DictWriter(fd,fieldnames=fields);wr.writeheader()
        for (label, threshold), info in jobs.items():
            inp = ROOT/'data'/'benchmark'/f'{label}.txt'
            tx = read_transactions(inp)
            reference = folder/f'{label}__mincount{threshold}.txt'
            result={'dataset':label,'min_count':threshold,'minsup_percentage':round(100*threshold/len(tx),8),
                    'transactions':len(tx),'status':'ok','error':'','spmf_output':str(reference.relative_to(ROOT))}
            try:
                duration, command = run_spmf_jar(jar,inp,reference,threshold,len(tx),args.timeout)
                ours = mine(tx,threshold,backend='bitset').supports
                expected=read_fim_output(reference)
                result.update(spmf_seconds_with_jvm_start=duration,
                              command=' '.join(command), **compare_maps(ours, expected))
            except (RuntimeError, subprocess.TimeoutExpired, ValueError, MemoryError) as exc:
                result.update(status='error',error=repr(exc))
            wr.writerow(result);fd.flush()
            print(label, threshold, result['status'],result.get('matching_rate'), flush=True)
        # Fifth real SPMF comparison on a small, independent toy database.
        toy_path = ROOT/'data/toy/baskets.txt'
        tx = read_transactions(toy_path)
        threshold = 3
        result={'dataset':'toy_baskets','min_count':threshold,
                'minsup_percentage':100*threshold/len(tx), 'transactions':len(tx),
                'status':'ok','error':'','spmf_output':str((folder/'toy_baskets__mincount3.txt').relative_to(ROOT))}
        try:
            duration, command = run_spmf_jar(jar,toy_path,folder/'toy_baskets__mincount3.txt',
                                              threshold,len(tx),args.timeout)
            result.update(spmf_seconds_with_jvm_start=duration,
                          command=' '.join(command),**compare_maps(
                              mine(tx,threshold,'bitset').supports,
                              read_fim_output(folder/'toy_baskets__mincount3.txt')))
        except (RuntimeError, subprocess.TimeoutExpired, ValueError, MemoryError) as exc:
            result.update(status='error',error=repr(exc))
        wr.writerow(result);fd.flush()
        print('toy_baskets',result['status'],result.get('matching_rate'),flush=True)
    print('Saved:',outpath)
    print('Elapsed SPMF seconds includes JVM start-up. Interpret comparisons accordingly.')

if __name__=='__main__': main()
