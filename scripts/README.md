**Name:** Thiều Quang  
**ID:** 24127114
**Thành viên:** Tôn Thất Việt Khoa — 24127190
**Môn học:** Khai thác dữ liệu và ứng dụng (*Data Mining and Applications*)
**Đề bài:** [HCMUS — Khai thác tập mục phổ biến](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/)

# Lệnh thực thi các quy trình

Tại thư mục `Eclat_Submission_VSCode`:

```powershell
.\.venv\Scripts\python.exe -m scripts.download_data
.\.venv\Scripts\python.exe -m scripts.dataset_statistics
.\.venv\Scripts\python.exe -m scripts.benchmark
.\.venv\Scripts\python.exe -m scripts.rss_memory
.\.venv\Scripts\python.exe -m scripts.scalability
.\.venv\Scripts\python.exe -m scripts.length_experiment
.\.venv\Scripts\python.exe -m scripts.setup_spmf
.\.venv\Scripts\python.exe -m scripts.run_spmf --jar tools/spmf.jar
.\.venv\Scripts\python.exe -m scripts.market_app
.\.venv\Scripts\python.exe -m scripts.visual_app
.\.venv\Scripts\python.exe -m scripts.plot_results
.\.venv\Scripts\python.exe -m scripts.generate_report_tables
.\.venv\Scripts\python.exe -m scripts.check_submission
```

Các lệnh tải dữ liệu cần kết nối Internet; lệnh đối chiếu SPMF cần Java và tệp JAR chính thức. Dữ liệu toy chỉ phục vụ kiểm thử, không được xem là benchmark thực tế.
