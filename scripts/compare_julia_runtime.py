from pathlib import Path
import csv
import math
import shutil
from reportlab.graphics.shapes import Drawing, Rect, Line, Circle, String
from reportlab.graphics import renderPDF, renderSVG
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

DATASETS = [
    "foodmart", "c20d10k",
    "t25i10d10k", "BMS_WebView_1"
]

SERIES = [
    "Julia Set", "Julia Bitset",
    "Python Set", "Python Bitset", "SPMF"
]

COLORS = [
    "#2171B5", "#22A884", "#D95F02",
    "#8856A7", "#444444"
]

measurements = {}

def rows(filename):
    with (RESULTS / filename).open(
        encoding="utf-8-sig", newline=""
    ) as stream:
        return list(csv.DictReader(stream))

def record(row, name, field):
    key = (
        row["dataset"],
        int(row["min_count"]),
        name
    )
    value = float(row[field])

    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"Invalid timing: {key}")

    if key in measurements:
        raise ValueError(f"Duplicate timing: {key}")

    measurements[key] = value

for r in rows("julia_benchmark.csv"):
    if (
        r["count_match"].lower() != "true"
        or r["backend_exact_match"].lower() != "true"
    ):
        raise ValueError(f"Julia check failed: {r}")

    record(
        r,
        "Julia " + r["backend"].title(),
        "seconds"
    )

for r in rows("benchmark.csv"):
    if r["status"] == "ok":
        record(
            r,
            "Python " + r["backend"].title(),
            "seconds"
        )

for r in rows("spmf_comparison.csv"):
    if (
        r["status"] == "ok"
        and r["exact_match"].lower() == "true"
    ):
        record(
            r,
            "SPMF",
            "spmf_seconds_with_jvm_start"
        )

thresholds = {}

for ds in DATASETS:
    mins = sorted({
        m for (d, m, method) in measurements
        if d == ds
    })

    if len(mins) != 6:
        raise ValueError(
            f"{ds}: expected 6 minsup levels, got {mins}"
        )

    for m in mins:
        for method in SERIES:
            if (ds, m, method) not in measurements:
                raise ValueError(
                    f"Missing: {ds}, {m}, {method}"
                )

    thresholds[ds] = mins

def s(d, x, y, value, size=20,
      align="start", color="#262626"):

    d.add(String(
        x, y, str(value),
        fontName="Helvetica",
        fontSize=size,
        textAnchor=align,
        fillColor=HexColor(color)
    ))

def legend(d, y):
    for i, name in enumerate(SERIES):
        x = 70 + i * 285

        d.add(Line(
            x, y + 7, x + 52, y + 7,
            strokeColor=HexColor(COLORS[i]),
            strokeWidth=5
        ))

        s(d, x + 63, y, name, 22)

def panel(d, ds, x, y, w, h):
    d.add(Rect(
        x, y, w, h,
        strokeColor=HexColor("#D6DBE0"),
        fillColor=HexColor("#FFFFFF")
    ))

    s(d, x + 24, y + h - 45, ds, 28)

    left = x + 93
    bottom = y + 97
    plotw = w - 146
    ploth = h - 185

    s(
        d, left, bottom + ploth + 19,
        "Time (seconds, log scale)", 19
    )

    all_times = [
        measurements[(ds, m, method)]
        for m in thresholds[ds]
        for method in SERIES
    ]

    low = math.log10(min(all_times)) - 0.2
    high = math.log10(max(all_times)) + 0.2

    def tx(m):
        seq = thresholds[ds]
        return (
            left
            + (m - seq[0])
            / (seq[-1] - seq[0])
            * plotw
        )

    def ty(value):
        return (
            bottom
            + (math.log10(value) - low)
            / (high - low)
            * ploth
        )

    for i in range(5):
        v = low + i * (high - low) / 4
        py = bottom + ploth * i / 4

        d.add(Line(
            left, py, left + plotw, py,
            strokeColor=HexColor("#E5E9ED")
        ))

        s(
            d, left - 9, py - 6,
            f"{10 ** v:.2g}",
            18, "end"
        )

    d.add(Line(
        left, bottom,
        left + plotw, bottom,
        strokeColor=HexColor("#333333")
    ))

    d.add(Line(
        left, bottom,
        left, bottom + ploth,
        strokeColor=HexColor("#333333")
    ))

    for m in thresholds[ds]:
        px = tx(m)

        d.add(Line(
            px, bottom - 5, px, bottom,
            strokeColor=HexColor("#333333")
        ))

        s(d, px, bottom - 30, m, 17, "middle")

    s(
        d,
        left + plotw / 2,
        bottom - 65,
        "Absolute minimum support (count)",
        19, "middle"
    )

    for i, method in enumerate(SERIES):
        points = [
            (
                tx(m),
                ty(measurements[(ds, m, method)])
            )
            for m in thresholds[ds]
        ]

        for p, q in zip(points, points[1:]):
            d.add(Line(
                p[0], p[1], q[0], q[1],
                strokeColor=HexColor(COLORS[i]),
                strokeWidth=3
            ))

        for px, py in points:
            d.add(Circle(
                px, py, 4.5,
                strokeColor=HexColor(COLORS[i]),
                fillColor=HexColor(COLORS[i])
            ))

# Four panels in one overview
fig = Drawing(1530, 1160)

s(
    fig, 765, 1128,
    "Eclat: Julia / Python / SPMF runtime comparison",
    33, "middle"
)

legend(fig, 1084)

for ds, x, y in zip(
    DATASETS,
    [20, 787, 20, 787],
    [568, 568, 44, 44]
):
    panel(fig, ds, x, y, 724, 498)

chart_dir = RESULTS / "charts" / "julia_comparison"
chart_dir.mkdir(parents=True, exist_ok=True)

overview = chart_dir / "julia_python_spmf_runtime.svg"
renderSVG.drawToFile(fig, str(overview))

# Four individual SVG charts
for ds in DATASETS:
    single = Drawing(1530, 760)

    s(
        single, 765, 723,
        ds + " - runtime comparison",
        34, "middle"
    )

    legend(single, 679)
    panel(single, ds, 20, 45, 1490, 590)

    renderSVG.drawToFile(
        single,
        str(chart_dir / (ds + "_runtime_all.svg"))
    )

# PDF for IEEE
figures_dir = ROOT / "docs" / "figures"
figures_dir.mkdir(parents=True, exist_ok=True)

pdf = figures_dir / "julia_python_spmf_runtime.pdf"

renderPDF.drawToFile(
    fig,
    str(pdf),
    "Julia, Python, SPMF runtime comparison"
)

print("Created SVG:", overview)
print("Created PDF:", pdf)

# Add the result to IEEE
texpath = (
    ROOT / "docs" / "generated"
    / "julia_runtime_comparison.tex"
)
texpath.parent.mkdir(parents=True, exist_ok=True)

tex = r"""
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/julia_python_spmf_runtime.pdf}
\caption{Thời gian chạy Eclat trên bốn bộ dữ liệu với sáu mức minimum support: Julia (Set và BitVector), Python (set và bitset), và SPMF. Trục tung dùng thang logarit. Số liệu SPMF bao gồm khởi động JVM, trong khi thời gian Julia/Python được lấy từ benchmark riêng. Các phép đo không phải một so sánh hiệu năng thuần thuật toán trong điều kiện kiểm soát đồng nhất.}
\label{fig:julia-python-spmf-runtime}
\end{figure*}
Hình~\ref{fig:julia-python-spmf-runtime} tổng hợp kết quả thời gian của hai bản cài đặt do nhóm phát triển và SPMF. Mỗi mức support có một phép đo được ghi trong các tệp CSV; sự khác biệt về cách đo và chi phí khởi động khiến các đường thời gian chỉ có giá trị mô tả, không đủ để khẳng định Julia, Python hay SPMF nhanh hơn trong mọi trường hợp.
"""

texpath.write_text(
    tex.strip() + "\n",
    encoding="utf-8"
)

report = ROOT / "docs" / "Report.tex"
original = report.read_text(encoding="utf-8")

injection = r"\input{generated/julia_runtime_comparison.tex}"
anchor = r"\input{generated/analysis_charts.tex}"

if injection not in original:
    if original.count(anchor) != 1:
        raise RuntimeError(
            "Cannot locate unique analysis_charts anchor"
        )

    backup = ROOT / "docs" / "Report_before_julia.tex"

    if not backup.exists():
        shutil.copy2(report, backup)

    report.write_text(
        original.replace(
            anchor,
            anchor + "\n" + injection,
            1
        ),
        encoding="utf-8"
    )

    print("Updated Report.tex")
else:
    print("Julia chart already included; skipped duplicate")

print("Generated:", texpath)
