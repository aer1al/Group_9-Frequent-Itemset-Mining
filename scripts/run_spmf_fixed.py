"""Reference verification using official SPMF jar, with reversible item-ID compacting.

This does NOT implement SPMF or modify the Eclat algorithm. For datasets whose
original item IDs are sparse/large, it maps them to 1..M for SPMF's matrix,
then translates reference output back before exact comparison.

Run from project root:
  .\\.venv\\Scripts\\python.exe -m scripts.run_spmf_fixed --jar tools/spmf.jar
"""
import argparse
import csv
import json
import subprocess
from pathlib import Path

from scripts.benchmark import ROOT
from scripts.run_spmf import run_spmf_jar, compare_maps
from src.algorithm.eclat import mine
from src.utils import read_transactions, read_fim_output, write_fim_output, sha256


def prepare_spmf_input(label, tx, original_input, folder):
    """Return (SPMF input path, inverse ID map, mapping path or None)."""
    ids = sorted({item for record in tx for item in record})
    if not ids:
        return original_input, None, None
    # The reference Eclat's triangular matrix can be too large when IDs are
    # sparse and high, even with a small number of distinct items.
    if max(ids) <= max(2000, 4 * len(ids)) and min(ids) >= 0:
        return original_input, None, None
    forward = {old: new for new, old in enumerate(ids, 1)}
    inverse = {new: old for old, new in forward.items()}
    compact_path = folder / f'{label}__compact_input.txt'
    with compact_path.open('w', encoding='utf-8', newline='\n') as handle:
        for record in tx:
            handle.write(' '.join(map(str, sorted(forward[x] for x in record))) + '\n')
    mapping_path = folder / f'{label}__item_mapping.json'
    mapping_path.write_text(json.dumps({
        'purpose': 'Reversible encoding for external SPMF reference ONLY',
        'original_file': str(original_input.relative_to(ROOT)),
        'original_sha256': sha256(original_input),
        'transaction_count': len(tx),
        'distinct_items': len(ids),
        'original_min_id': min(ids),
        'original_max_id': max(ids),
        'compact_sha256': sha256(compact_path),
        'compact_to_original': {str(k): v for k, v in inverse.items()}
    }, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'{label}: remap {len(ids)} item IDs, largest original ID {max(ids)} -> 1..{len(ids)}', flush=True)
    return compact_path, inverse, mapping_path


def remap_output(native, inverse):
    if inverse is None:
        return native
    translated = {}
    for items, support in native.items():
        key = tuple(sorted(inverse[i] for i in items))
        if key in translated:
            raise ValueError(f'Duplicate decoded itemset: {key}')
        translated[key] = support
    return translated


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--jar', required=True)
    p.add_argument('--benchmark', default='results/benchmark.csv')
    p.add_argument('--timeout', type=int, default=900)
    args = p.parse_args()
    jar = ROOT / args.jar
    if not jar.is_file():
        raise SystemExit(f'Missing SPMF jar: {jar}')
    bench = ROOT / args.benchmark
    if not bench.is_file():
        raise SystemExit(f'Missing {bench}. Run benchmark first.')
    with bench.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    jobs = {}
    for r in rows:
        if r['status'] == 'ok':
            jobs[(r['dataset'], int(r['min_count']))] = r

    output_dir = ROOT / 'results' / 'reference_spmf'
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = ROOT / 'results' / 'spmf_comparison.csv'
    fields = ['dataset', 'min_count', 'minsup_percentage', 'transactions', 'status',
              'spmf_seconds_with_jvm_start', 'reference_count', 'ours_count',
              'matched_patterns', 'total_unique_patterns', 'matching_rate', 'exact_match',
              'error', 'spmf_output', 'command', 'remapped', 'mapping_file']
    with out_file.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        cached = {}
        for (label, threshold), _ in jobs.items():
            result = {'dataset': label, 'min_count': threshold, 'status': 'ok', 'error': ''}
            try:
                if label not in cached:
                    original = ROOT / 'data' / 'benchmark' / f'{label}.txt'
                    tx = read_transactions(original)
                    inp, inverse, mapping_path = prepare_spmf_input(label, tx, original, output_dir)
                    cached[label] = (tx, inp, inverse, mapping_path)
                tx, inp, inverse, mapping_path = cached[label]
                readable_ref = output_dir / f'{label}__mincount{threshold}.txt'
                native_ref = (output_dir / f'{label}__mincount{threshold}__compact_native.txt'
                              if inverse is not None else readable_ref)
                result.update(minsup_percentage=round(100 * threshold / len(tx), 8),
                              transactions=len(tx), remapped=(inverse is not None),
                              mapping_file=str(mapping_path.relative_to(ROOT)) if mapping_path else '',
                              spmf_output=str(readable_ref.relative_to(ROOT)))
                duration, command = run_spmf_jar(jar, inp, native_ref, threshold, len(tx), args.timeout)
                native_supports = read_fim_output(native_ref)
                ref_supports = remap_output(native_supports, inverse)
                if inverse is not None:
                    write_fim_output(ref_supports, readable_ref)
                our_supports = mine(tx, threshold, backend='bitset').supports
                result.update(spmf_seconds_with_jvm_start=duration,
                              command=' '.join(command), **compare_maps(our_supports, ref_supports))
            except (RuntimeError, ValueError, MemoryError, KeyError, subprocess.TimeoutExpired) as exc:
                result.update(status='error', error=repr(exc))
            writer.writerow(result)
            f.flush()
            print(label, threshold, result['status'], result.get('matching_rate'), flush=True)

        toy_path = ROOT / 'data' / 'toy' / 'baskets.txt'
        toy = read_transactions(toy_path)
        threshold = 3
        toy_ref = output_dir / 'toy_baskets__mincount3.txt'
        result = {'dataset': 'toy_baskets', 'min_count': threshold, 'status': 'ok', 'error': '',
                  'minsup_percentage': 100 * threshold / len(toy), 'transactions': len(toy),
                  'spmf_output': str(toy_ref.relative_to(ROOT)), 'remapped': False, 'mapping_file': ''}
        try:
            duration, command = run_spmf_jar(jar, toy_path, toy_ref, threshold, len(toy), args.timeout)
            result.update(spmf_seconds_with_jvm_start=duration, command=' '.join(command),
                          **compare_maps(mine(toy, threshold, backend='bitset').supports,
                                         read_fim_output(toy_ref)))
        except (RuntimeError, ValueError, MemoryError, KeyError, subprocess.TimeoutExpired) as exc:
            result.update(status='error', error=repr(exc))
        writer.writerow(result)
        print('toy_baskets', result['status'], result.get('matching_rate'), flush=True)
    print('Saved:', out_file)
    print('Original benchmark files were NOT changed. Remap is for external SPMF only.')
    print('SPMF time includes JVM startup; it is not directly comparable to in-process Python time.')


if __name__ == '__main__':
    main()
