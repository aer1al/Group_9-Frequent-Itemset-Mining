**Name:** Thiều Quang  
**ID:** 24127114
**Thành viên:** Tôn Thất Việt Khoa — 24127190
**Môn học:** Khai thác dữ liệu và ứng dụng (*Data Mining and Applications*)
**Đề bài:** [HCMUS — Khai thác tập mục phổ biến](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/)

# Dữ liệu benchmark

Thư mục này chứa các bộ Foodmart, c20d10k, t25i10d10k và BMS_WebView_1. Có thể tải hoặc cập nhật các tệp bằng lệnh:

```powershell
python -m scripts.download_data --names foodmart c20d10k t25i10d10k BMS_WebView_1
```

Nguồn và SHA-256 được ghi trong `DATA_SOURCES.md` và `data/download_manifest.json`. Tệp dữ liệu là đầu vào; kết quả benchmark được lưu riêng trong `results/`.
