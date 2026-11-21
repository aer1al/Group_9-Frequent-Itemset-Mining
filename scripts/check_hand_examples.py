r"""Independent hand-example checker (no FIM library or Eclat implementation used).

Run from project root:
    .\.venv\Scripts\python.exe -m scripts.check_hand_examples
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOY = ROOT / "data" / "toy"
CASES = (
    ("eclat_hand_basic", 11),
    ("eclat_hand_special", 13),
)


def expected_rows(transactions: list[set[int]], minsup: int) -> list[str]:
    items = sorted(set().union(*transactions))
    results = []
    for size in range(1, len(items) + 1):
        for itemset in combinations(items, size):
            support = sum(set(itemset).issubset(t) for t in transactions)
            if support >= minsup:
                results.append(" ".join(map(str, itemset)) + f" #SUP: {support}")
    return results


def main() -> None:
    for name, count in CASES:
        inp = TOY / f"{name}.txt"
        expected = TOY / f"{name}_expected.txt"
        transactions = [set(map(int, line.split())) for line in inp.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert len(transactions) == 6, f"{name}: expected 6 transactions"
        assert len(set().union(*transactions)) == 5, f"{name}: expected 5 distinct items"
        computed = expected_rows(transactions, minsup=3)
        documented = expected.read_text(encoding="utf-8").strip().splitlines()
        assert len(computed) == count, f"{name}: found {len(computed)} not {count}"
        assert computed == documented, f"{name}: mismatch in itemsets or supports"
        print(f"PASS {name}: {len(transactions)} transactions, 5 items, minsup=3, {len(computed)} frequent itemsets")
    print("HAND EXAMPLES: 2/2 EXACT")


if __name__ == "__main__":
    main()
