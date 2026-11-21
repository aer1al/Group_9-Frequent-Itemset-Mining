**Thành viên:** Thiều Quang - 24127114

**Thành viên:** Tôn Thất Việt Khoa — 24127190  
**Môn học:** Khai thác dữ liệu và ứng dụng (*Data Mining and Applications*)  
**Đề bài:** [HCMUS — Khai thác tập mục phổ biến](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/)


# Đồ án Frequent Itemset Mining — Eclat (Python + Julia, VS Code + Colab)

Đây là dự án cài đặt thuật toán Eclat độc lập bằng Python (set/bitset) và Julia (Set/BitVector), kèm hai ứng dụng thực tế. Trên Windows, Python đạt 41/41 ca kiểm thử, Julia đạt 77/77; mỗi bản có 48 lượt benchmark thành công. Đối chiếu itemset–support với SPMF đạt 24/24 cấu hình benchmark; trên Colab, Python đạt 25/25 khi tính cả toy. Có 10 luật kết hợp market basket, 37 mẫu visual words, kết quả scalability/bộ nhớ và báo cáo IEEE 14 trang tổng cộng, đáp ứng giới hạn 10–15 trang nội dung theo đề bài. Các phép đo của Python, Julia và SPMF có giao thức và chi phí khởi động khác nhau, không được diễn giải như so sánh tốc độ thuần túy.

## Phân công công việc

Bảng dưới đây thể hiện phân công phụ trách từ thời điểm tiếp nhận. Tỷ lệ đóng góp cuối cùng được xác nhận theo công việc thực tế mỗi thành viên hoàn thành.

| Thành viên | Công việc phụ trách |
| --- | --- |
| **Thiều Quang — 24127114** | Xây dựng mã nguồn ban đầu; phát biểu bài toán, cơ sở toán học và chứng minh tính đúng; cài đặt Eclat Python/Julia với set/bitset; xây dựng kiểm thử, đối chiếu brute force/SPMF; thiết kế và chạy benchmark thời gian, bộ nhớ, scalability, độ dài giao dịch; phân tích hiệu năng. Phụ trách **Visual Patterns** — xử lý ảnh, trích patch, k-means, mã hóa visual-word transactions và tích hợp Eclat. Viết phần thuật toán, thực nghiệm và Visual Patterns; tổng hợp báo cáo LaTeX và tích hợp toàn bộ project. |
| **Tôn Thất Việt Khoa — 24127190** | Tiếp nhận phát triển **Market Basket** — xử lý đơn hàng, sinh luật, tính support/confidence/lift, lọc top-10. Phụ trách thu thập, tiền xử lý và thống kê dữ liệu benchmark; đọc/ghi định dạng SPMF và giao diện dòng lệnh; tạo biểu đồ từ kết quả thực nghiệm. Viết phần dữ liệu và Market Basket trong báo cáo; phân tích kết quả luật kết hợp; chuẩn bị demo và hướng dẫn chạy phần dữ liệu, CLI và Market Basket. |

## Phạm vi đồ án theo đề bài

- Đề: <https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/>
- **Chọn duy nhất Eclat** (không phải dEclat), có 2 backend `set` và `bitset`, tự triển khai từ mô tả Zaki (2000), không sao chép SPMF hoặc GitHub.
- **Python từ 3.9** (khuyến nghị 3.11), chỉ dùng NumPy cho xử lý ảnh; `pytest` phục vụ kiểm thử. Không dùng sklearn, mlxtend, efficient-apriori, các thư viện FIM.
- **Julia:** cài đặt Eclat riêng trong `julia/EclatJulia.jl`, gồm backend `Set` và `BitVector`, có CLI, kiểm thử và benchmark. Đã thử Julia 1.13.3 trên Windows; notebook Colab ghi Julia 1.12.6.
- **Chương 1:** Đọc/ghi định dạng SPMF, giao diện dòng lệnh, cài đặt Eclat, kiểm thử trên cơ sở dữ liệu nhỏ và tối ưu bằng bitset.
- **Chương 2:** Bốn bộ benchmark (Foodmart, c20d10k, t25i10d10k, BMS_WebView_1); sáu ngưỡng minsup mỗi bộ được xác định từ support singleton trong dữ liệu. Đo thời gian, bộ nhớ Python và RSS tiến trình, kích thước đầu ra, đối chiếu SPMF, scalability và ảnh hưởng của độ dài giao dịch.
- **Chương 3:** ECommerce (market basket và top-10 luật theo lift); UCI Optdigits (patch descriptors, codebook k-means NumPy, Bag of Visual Words → Eclat).
- **Đường dẫn tài liệu/bộ dữ liệu gốc:** [DATA_SOURCES.md](DATA_SOURCES.md). Script tải dữ liệu ghi SHA256 / URL vào `data/download_manifest.json`.
- **GitHub công khai:** https://github.com/aer1al/Group_9-Frequent-Itemset-Mining
- **Google Colab:** [Notebook Eclat](https://colab.research.google.com/drive/1zk6pnHh-6Xea7r3L5pFuSz2ZveCDUJTf?usp=sharing). Notebook nguồn: `notebooks/Project2.ipynb` (26 cells; 15 ô code đã lưu kết quả). Tác giả xác nhận notebook đã chạy sạch từ đầu đến cuối. Quyền truy cập công khai chưa được xác minh bằng lượt kiểm tra ẩn danh; trước khi nộp, đặt General access thành “Anyone with the link — Viewer” và thử mở bằng cửa sổ đăng xuất.

## 1. Chạy bằng VS Code trên Windows

1. Trên máy thực nghiệm, mở thư mục **`D:\Group_9`** bằng **VS Code > File > Open Folder** (trên máy khác, mở thư mục gốc đã giải nén; không mở riêng từng file `.py`).
2. Cài Python, Julia và Java. **Bản `tools/spmf.jar` đang dùng yêu cầu Java 25**; kiểm tra bằng `java -version`. Có thể dùng VS Code Terminal PowerShell; notebook chạy trên Google Colab. Nếu muốn biên dịch `docs/Report.pdf`, dùng XeLaTeX (MiKTeX/TeX Live).
3. Mở **Terminal > New Terminal** (PowerShell), chạy:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m src.cli data/toy/baskets.txt --minsup 0.5 --backend bitset --output results/toy_result.txt
```

Bạn cũng có thể vào **Terminal > Run Task** chọn `01 | Install dependencies`, `02 | All tests`... trong `.vscode/tasks.json`, hoặc Run and Debug chọn `01 - Eclat toy bitset`.

> Terminal PowerShell: vào thư mục dự án bằng `cd "D:\Group_9"`. Nếu `py` không có, dùng `python -m venv .venv`; nếu `.venv` đã tồn tại, không cần tạo lại.

## 1B. Chạy Eclat Julia từ VS Code Terminal

Chạy trong **PowerShell tại `D:\Group_9`** (không chạy notebook bằng Jupyter của VS Code):

```powershell
julia --version
julia --startup-file=no .\julia\test_eclat.jl
julia .\julia\main.jl --input data/toy/baskets.txt --minsup 0.5 --backend bitset --output results/julia_output.txt
.\.venv\Scripts\python.exe -m scripts.verify_julia_spmf
```

Các chương trình `julia/benchmark_julia.jl` và `julia/export_itemsets.jl` tạo kết quả ở `results/julia_benchmark.csv`, `results/julia_itemsets.csv`. Kết quả hiện có đã được kiểm chứng (48/48 benchmark và 24/24 cấu hình so với SPMF); chỉ chạy lại nếu cần tái tạo dữ liệu.

## 2. Tải bộ dữ liệu benchmark và ứng dụng

```powershell
.\.venv\Scripts\python.exe -m scripts.download_data
.\.venv\Scripts\python.exe -m scripts.dataset_statistics
```

Các file raw nằm trong `data/benchmark/` và `data/applications/`, không commit file lớn hoặc file chưa rõ giấy phép. Các liên kết chính xác nằm ở `DATA_SOURCES.md`. Mỗi raw file có `source_url`, `sha256` và byte size ở `data/download_manifest.json`; `results/dataset_statistics.csv` chứa thống kê do project tính lại.

## 3. Chương 2 — benchmark Eclat thực tế

```powershell
.\.venv\Scripts\python.exe -m scripts.benchmark
.\.venv\Scripts\python.exe -m scripts.rss_memory
.\.venv\Scripts\python.exe -m scripts.scalability
.\.venv\Scripts\python.exe -m scripts.length_experiment
```

**MinSup:** Script xác định sáu ngưỡng bằng 100%, 85%, 70%, 55%, 42% và 32% support singleton lớn nhất của từng bộ dữ liệu. Mỗi ngưỡng được chuyển thành support tuyệt đối `k` và ghi vào CSV để có thể tái lập. Nếu `status=invalid` do giới hạn bộ nhớ hoặc số lượng mẫu, lượt chạy đó không được xem là phép đo hoàn tất; mọi điều chỉnh cần được ghi lại.

`results/rss_memory.csv` ghi peak process RSS (Windows PeakWorkingSetSize / Linux ru_maxrss) trong tiến trình Python mới cho mỗi lần đo.

`results/benchmark.csv` ghi `seconds`, `peak_python_mb` (tracemalloc; không tương đương process RSS), `itemset_count`, `status`, `baseline_match`, phiên bản Python/OS và SHA-256 dữ liệu.

## 4. Đối chiếu kết quả với SPMF

Tải file **release `spmf.jar` chính thức** tại:
<https://www.philippe-fournier-viger.com/spmf/index.php?link=download.php>

Có thể chạy lệnh tự tải release qua Terminal hoặc tải thủ công (nếu mạng chặn):

```powershell
.\.venv\Scripts\python.exe -m scripts.setup_spmf
java -version
.\.venv\Scripts\python.exe -m scripts.run_spmf_fixed
```

SPMF chạy như một tiến trình Java độc lập với CLI `java -jar spmf.jar run Eclat ...`; mã Python không gọi thư viện SPMF. Script đối chiếu từng itemset và support trên bốn bộ benchmark × sáu ngưỡng và một bộ toy. Kết quả được lưu trong `results/spmf_comparison.csv`, còn các đầu ra tham chiếu nằm trong `results/reference_spmf/`. Kết quả hiện tại khớp chính xác 24/24 cấu hình benchmark và 25/25 trường hợp nếu tính toy. Với BMS_WebView_1, module `scripts.run_spmf_fixed` ánh xạ tạm ID item về miền liên tiếp khi gọi SPMF và đổi ngược trước khi đối chiếu; không sửa dữ liệu gốc. Thời gian SPMF được đo bằng `subprocess` và bao gồm thời gian khởi động JVM; cần nêu rõ điều này khi diễn giải so sánh.

## 5. Chương 3 — hai ứng dụng thực tế

```powershell
.\.venv\Scripts\python.exe -m scripts.market_app
.\.venv\Scripts\python.exe -m scripts.visual_app
```

- `results/market_top10.csv`: luật giỏ hàng `X->Y`, support, confidence, lift từ Eclat riêng. File đầu vào ECommerce có `item_1 ... item_n:timestamp`: parser bỏ timestamp, mỗi đơn hàng là một giao dịch. Mapping item ID → tên mặt hàng từ SPMF; luật không chứng minh quan hệ nhân quả.
- `results/visual_patterns.csv`: từ UCI Optdigits (mỗi ảnh 8×8, 16 descriptors patch 2×2) tạo codebook bằng NumPy k-means với seed 2026, mỗi ảnh thành một tập từ trực quan. Eclat khai thác tần suất. Nhãn chữ số không dùng trong lúc tạo codebook hoặc mining. Cần diễn giải giới hạn mất thông tin không gian.

## 6. Biểu đồ, báo cáo IEEE hai cột, Colab

```powershell
.\.venv\Scripts\python.exe -m scripts.plot_results
.\.venv\Scripts\python.exe -m scripts.generate_report_tables
.\.venv\Scripts\python.exe -m scripts.check_submission
```

Biểu đồ SVG được lưu trong `results/charts/` và có thể tạo lại bằng `scripts.plot_results`. Bảng LaTeX lấy dữ liệu CSV hiện có nằm trong `docs/generated/experiment_data.tex`, được `docs/Report.tex` tự động import. Biên dịch bằng XeLaTeX từ Terminal:

```powershell
cd docs
xelatex -interaction=nonstopmode -halt-on-error Report.tex
xelatex -interaction=nonstopmode -halt-on-error Report.tex
cd ..
```

`docs/Report.pdf` là báo cáo IEEE đã cập nhật và biên dịch thành công (13 trang tổng cộng; tài liệu tham khảo bắt đầu ở trang cuối), có phần Python, Julia, SPMF, bảng kết quả và hai ứng dụng. Hướng dẫn biên dịch nằm trong `docs/REPORT_BUILD.md`. Nếu chỉnh LaTeX, cần biên dịch lại hai lượt và kiểm tra PDF cuối.

Notebook `notebooks/Project2.ipynb` là bản đồng bộ từ Colab gồm 26 cells, đã chạy 15 cell code liên tục và không lưu output lỗi. Để chạy trên Colab, upload ZIP mã nguồn khi notebook yêu cầu; xem link Colab ở đầu README. Trên Windows, dùng VS Code Terminal để chạy các mô-đun Python/Julia.

## 7. Tái lập thực nghiệm khi cần

Các kết quả thực nghiệm chính **đã được tạo**. Muốn kiểm tra nhanh mà không chạy lại benchmark, dùng:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests
julia --startup-file=no .\julia\test_eclat.jl
.\.venv\Scripts\python.exe -m scripts.verify_julia_spmf
```

Nếu cần tái tạo đầy đủ, dùng các lệnh benchmark, ứng dụng và `scripts.run_spmf_fixed` ở các mục trên. Công cụ SPMF chạy Java độc lập; thời gian SPMF có gồm khởi động JVM. Không kết luận hiệu năng giữa các ngôn ngữ nếu môi trường và cách đo chưa đồng nhất.

## 8. Nộp Moodle qua GitHub (thực hiện từ VS Code)
 
**Đề HCMUS yêu cầu nộp MỘT link GitHub repo public lên Moodle** .Sau khi đọc hiểu mã nguồn, hoàn thiện thực nghiệm và cập nhật báo cáo:

```powershell
git init
git branch -M main
git add .
git commit -m "Implement Eclat and reproducible experiments"
git remote add origin <URL_REPOSITORY_CUA_BAN>
git push -u origin main
```

**Liêm chính học thuật:** công cụ AI đã hỗ trợ một phần việc chuẩn bị mã và tài liệu. Sinh viên cần tự rà soát, hiểu, kiểm chứng và khai báo theo quy định học phần. Không trình bày công việc chưa thực hiện hoặc kết quả tham chiếu SPMF như sản phẩm do cài đặt của dự án tạo ra.

## 9. Chạy notebook trên Google Colab
1. Mở [Google Colab](https://colab.research.google.com/), đăng nhập và chọn *File → Upload notebook*.
2. Tải lên Eclat_Experiments.ipynb và kết nối runtime Python.
3. Chạy ô khởi tạo đầu tiên. Nếu được yêu cầu chọn tệp, tải lên gói ZIP đầy đủ của dự án.
4. Chạy các ô tiếp theo theo thứ tự. Kiểm tra thông báo lỗi và trạng thái của mỗi bước trước khi tiếp tục.
5. Nếu tải SPMF tự động không thành công, lấy JAR từ [trang tải SPMF chính thức](https://www.philippe-fournier-viger.com/spmf/index.php?link=download.php) và dùng ô tải tệp dự phòng.
6. Chạy ô cuối để tạo gói kết quả. Tải gói về máy và lưu đúng cấu trúc thư mục trước khi cập nhật báo cáo.
