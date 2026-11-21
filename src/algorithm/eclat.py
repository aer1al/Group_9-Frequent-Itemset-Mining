"""Independent, educational implementation of vertical TID-set Eclat.
Designed from descriptions in M. J. Zaki (2000), not copied from SPMF.
Two variants: Python set intersection (baseline), integer bitset (optimized).
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from math import ceil, isfinite
from typing import Iterable

Itemset = tuple[int, ...]

@dataclass
class MiningResult:
    supports: dict[Itemset, int]
    transactions: int
    min_count: int


def min_support_count(minsup: float | int, n: int) -> int:
    """0 < float <= 1: relative; integer >= 1: absolute."""
    if n <= 0:
        raise ValueError('Empty database is not allowed')
    if isinstance(minsup, bool) or not isfinite(float(minsup)) or float(minsup) <= 0:
        raise ValueError('minsup must be positive and finite')
    if isinstance(minsup, int) or float(minsup) > 1:
        if float(minsup) != int(minsup):
            raise ValueError('Absolute minsup must be an integer')
        return int(minsup)
    return max(1, ceil(float(minsup) * n - 1e-12))


def mine(transactions: Iterable[Iterable[int]], minsup: float | int = 0.3,
         backend: str = 'bitset', max_results: int | None = None) -> MiningResult:
    """Mine ALL frequent itemsets, with absolute support counts.
    Prefix DFS, fixed ordering gives unique itemsets. Input transactions
    are sets: repeated items in a transaction never add support.
    """
    if backend not in ('set', 'bitset'):
        raise ValueError('backend must be set or bitset')
    data = [frozenset(int(x) for x in transaction) for transaction in transactions]
    threshold = min_support_count(minsup, len(data))
    vertical = defaultdict(set)
    for tid, transaction in enumerate(data):
        for item in transaction:
            vertical[item].add(tid)
    supports: dict[Itemset, int] = {}
    # Tie-break on item ID for deterministic output. Sorting by support increases
    # reproducibility while preserving the exhaustive DFS search.
    singles = sorted(((i, tids) for i, tids in vertical.items()
                      if len(tids) >= threshold), key=lambda z: (len(z[1]), z[0]))
    if backend == 'bitset':
        prepared = []
        for item, tids in singles:
            mask = 0
            for tid in tids:
                mask |= 1 << tid
            prepared.append((item, mask, len(tids)))

        def recurse(prefix, extensions):
            for index, (item, mask, count) in enumerate(extensions):
                chosen = prefix + (item,)
                key = tuple(sorted(chosen))
                supports[key] = count
                if max_results is not None and len(supports) > max_results:
                    raise RuntimeError('Result cap exceeded; run is censored (do not report as complete)')
                children = []
                for item2, mask2, _ in extensions[index + 1:]:
                    intersection = mask & mask2
                    overlap = intersection.bit_count()
                    if overlap >= threshold:
                        children.append((item2, intersection, overlap))
                recurse(chosen, children)
    else:
        prepared = [(item, tids, len(tids)) for item, tids in singles]

        def recurse(prefix, extensions):
            for index, (item, tids, count) in enumerate(extensions):
                chosen = prefix + (item,)
                supports[tuple(sorted(chosen))] = count
                if max_results is not None and len(supports) > max_results:
                    raise RuntimeError('Result cap exceeded; run is censored (do not report as complete)')
                children = []
                for item2, tids2, _ in extensions[index + 1:]:
                    intersection = tids & tids2
                    if len(intersection) >= threshold:
                        children.append((item2, intersection, len(intersection)))
                recurse(chosen, children)

    recurse((), prepared)
    return MiningResult(supports, len(data), threshold)
