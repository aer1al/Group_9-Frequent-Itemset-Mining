from pathlib import Path
import csv
import html
import base64

root = Path(__file__).resolve().parents[1]
charts = root / "results" / "charts"

tables = {
    "Thong ke du lieu": "dataset_statistics.csv",
    "Benchmark Eclat": "benchmark.csv",
    "Doi chieu SPMF": "spmf_comparison.csv",
    "Bo nho RSS": "rss_memory.csv",
    "Scalability": "scalability.csv",
    "Transaction length": "length_experiment.csv",
    "Top 10 association rules": "market_top10.csv",
    "Visual patterns": "visual_patterns.csv",
}

parts = ["""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>Eclat HCMUS Dashboard</title>
<style>
body {font-family:Arial,sans-serif;max-width:1200px;
margin:auto;padding:35px;background:#f5f7fb;color:#222}
header,section {background:white;padding:25px;
border-radius:12px;margin-bottom:22px}
h1,h2 {color:#174778}
table {border-collapse:collapse;width:100%;font-size:13px}
td,th {border:1px solid #ddd;padding:8px;text-align:left}
th {background:#e8eff8}
.tablewrap {overflow-x:auto}
img {max-width:100%;display:block;margin:auto}
figure {border:1px solid #ddd;border-radius:10px;
padding:15px;margin:18px 0}
a {color:#1263ad}
</style>
</head>
<body>
<header>
<h1>DO AN ECLAT - HCMUS</h1>
<p>Frequent Itemset Mining - Python</p>
<p>Học phần: Khai thác dữ liệu và ứng dụng (Data Mining and Applications)</p>
<p>Thành viên: Thiều Quang (24127114); Tôn Thất Việt Khoa (24127190)</p>
<p><a href="https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/">Đề bài HCMUS</a></p>
<p>41 unit tests | 24/24 SPMF | 4 benchmark datasets</p>
<p><a href="docs/Report.pdf">Xem bao cao IEEE</a></p>
</header>
<section><h2>Chuong 2 - Ket qua thuc nghiem</h2>
"""]

for title, filename in tables.items():
    path = root / "results" / filename
    if not path.exists():
        continue

    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames or []

    parts.append("<h3>" + html.escape(title) + "</h3>")
    parts.append('<div class="tablewrap"><table><tr>')
    for col in columns:
        parts.append("<th>" + html.escape(col) + "</th>")
    parts.append("</tr>")

    for row in rows[:15]:
        parts.append("<tr>")
        for col in columns:
            parts.append("<td>" + html.escape(
                str(row.get(col, ""))
            ) + "</td>")
        parts.append("</tr>")

    parts.append("</table></div>")
    parts.append(
        f"<p>Hien thi {min(15,len(rows))}/{len(rows)} dong. "
        f"<a href='results/{filename}'>Xem CSV day du</a></p>"
    )

parts.append("</section>")
parts.append("<section><h2>Bieu do Eclat</h2>")

selected = [
    "foodmart_runtime.svg",
    "c20d10k_runtime.svg",
    "t25i10d10k_runtime.svg",
    "BMS_WebView_1_runtime.svg",
    "c20d10k_memory.svg",
    "foodmart_patterns.svg",
    "scalability.svg",
    "length_experiment.svg",
]

for filename in selected:
    svg = charts / filename
    encoded = base64.b64encode(svg.read_bytes()).decode()
    parts.append(
        "<figure><h3>" + html.escape(svg.stem) + "</h3>"
        '<img src="data:image/svg+xml;base64,'
        + encoded + '"></figure>'
    )

parts.append("</section></body></html>")

target = root / "Eclat_Results_Dashboard.html"
target.write_text("".join(parts), encoding="utf-8")
print("Created:", target)
