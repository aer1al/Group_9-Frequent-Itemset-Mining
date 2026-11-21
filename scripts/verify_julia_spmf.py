from pathlib import Path
from collections import defaultdict
import csv
import sys

root = Path.cwd()
results = root / "results"

def load_julia():
    groups = defaultdict(dict)

    with (results / "julia_itemsets.csv").open(
        encoding="utf-8-sig", newline=""
    ) as f:
        for r in csv.DictReader(f):
            key = (r["dataset"], int(r["min_count"]))
            items = tuple(sorted(map(int, r["itemset"].split())))
            groups[key][items] = int(r["support"])

    return groups

def load_spmf(path):
    patterns = {}

    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.lstrip().startswith(("@", "#", "%")):
            continue

        if "#SUP:" not in line:
            raise ValueError(f"Invalid SPMF line: {line[:80]}")

        items_text, support_text = line.split("#SUP:", 1)
        items = tuple(sorted(map(int, items_text.split())))
        support = int(support_text.strip().split()[0])
        patterns[items] = support

    return patterns

def remappings(dataset):
    yield "Original IDs", None

    if dataset != "BMS_WebView_1":
        return

    path = root / "data" / "benchmark" / (dataset + ".txt")
    ids = set()
    order = []
    seen = set()

    for line in path.read_text(encoding="utf-8-sig").splitlines():
        for raw in line.split():
            item = int(raw)
            ids.add(item)

            if item not in seen:
                seen.add(item)
                order.append(item)

    for name, ordered in [
        ("Sorted IDs", sorted(ids)),
        ("First-seen IDs", order),
    ]:
        for offset in (0, 1):
            mapping = {
                item: i + offset
                for i, item in enumerate(ordered)
            }
            yield f"{name}, offset={offset}", mapping

def translate(patterns, mapping):
    if mapping is None:
        return patterns

    return {
        tuple(sorted(mapping[item] for item in items)): support
        for items, support in patterns.items()
    }

julia = load_julia()
checks = []

with (results / "spmf_comparison.csv").open(
    encoding="utf-8-sig", newline=""
) as f:
    reference_rows = list(csv.DictReader(f))

for row in reference_rows:
    key = (row["dataset"], int(row["min_count"]))

    if key not in julia:
        continue

    filename = row["spmf_output"].replace("\\", "/")
    reference_path = root / filename

    if not reference_path.exists():
        print("MISSING FILE:", reference_path)
        checks.append((key, False, "Missing reference"))
        continue

    actual = julia[key]
    expected = load_spmf(reference_path)

    matched = False
    method_used = ""

    for method, mapping in remappings(key[0]):
        if translate(actual, mapping) == expected:
            matched = True
            method_used = method
            break

    checks.append((key, matched, method_used))

    print(
        f"{key[0]} | minsup={key[1]} | "
        f"Julia={len(actual)} | SPMF={len(expected)} | "
        f"{'PASS' if matched else 'CHECK'} | {method_used}"
    )

passed = sum(ok for _, ok, _ in checks)

print()
print(f"EXACT JULIA vs SPMF: {passed}/{len(checks)}")
print("Comparison checks complete.")

if len(checks) != 24 or passed != 24:
    print("Some cases require inspection of the SPMF mapping.")
    sys.exit(1)

