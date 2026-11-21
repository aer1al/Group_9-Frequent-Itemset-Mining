**Name:** Thiều Quang  
**ID:** 24127114
**Thành viên:** Tôn Thất Việt Khoa — 24127190  
**Môn học:** Khai thác dữ liệu và ứng dụng (*Data Mining and Applications*)  
**Đề bài:** [HCMUS — Khai thác tập mục phổ biến](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/)

# Nguồn dữ liệu và khả năng truy xuất

Tài liệu này ghi nhận nguồn, mục đích và các bước chuyển đổi dữ liệu của đồ án. Dữ liệu nguồn không được trình bày như dữ liệu do sinh viên tự thu thập hoặc tạo ra. Script `python -m scripts.download_data` lưu URL, thời điểm tải, kích thước và SHA-256 vào `data/download_manifest.json`.

Tại thời điểm cập nhật, các tệp dữ liệu được liệt kê dưới đây hiện diện trong workspace. Trước khi phát hành repository, cần kiểm tra chính sách phân phối của từng nguồn và xác minh manifest với các tệp thực tế.

| Tên local | Nguồn trực tiếp | Nguồn gốc | Mục đích |
|---|---|---|---|
| `data/benchmark/foodmart.txt` | https://www.philippe-fournier-viger.com/spmf/publicdatasets/foodmartFIM.txt | SPMF public datasets, customer transactions, 4,141 transactions | Benchmark số 1 |
| `data/benchmark/c20d10k.txt` | https://www.philippe-fournier-viger.com/spmf/publicdatasets/c20d10k.txt | SPMF synthetic dataset, 10,000 transactions | Benchmark số 2 |
| `data/benchmark/t25i10d10k.txt` | https://www.philippe-fournier-viger.com/spmf/publicdatasets/t25i10d10k.txt | SPMF synthetic dataset, 9,976 transactions | Benchmark số 3 |
| `data/benchmark/BMS_WebView_1.txt` | https://www.philippe-fournier-viger.com/spmf/publicdatasets/BMS1_itemset_mining.txt | BMS clickstream from FIMI, reformatted by SPMF, 59,602 transactions | Benchmark số 4 |
| `data/applications/ecommerce_timestamped.txt` | https://www.philippe-fournier-viger.com/spmf/publicdatasets/ecommerce_time_without_utility.txt | SPMF converted real e-commerce transaction dataset, timestamp suffix | App 1 Market Basket |
| `data/applications/online_retail_item_names.txt` | https://www.philippe-fournier-viger.com/spmf/publicdatasets/online_retail_item_names.txt | SPMF item ID -> product descriptions | App 1 labels |
| `data/applications/optdigits.tra` | https://archive.ics.uci.edu/ml/machine-learning-databases/optdigits/optdigits.tra | UCI Optical Recognition of Handwritten Digits, training subset | App 2 image/BoVW |

Landing pages:
- SPMF: https://www.philippe-fournier-viger.com/spmf/index.php?link=datasets.php
- FIMI: http://fimi.uantwerpen.be/data/ (historical mirror, availability may vary)
- UCI: https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits
- Course assignment: https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/

## Chuyển đổi dữ liệu
- Benchmark FIM: lưu từng dòng thành transaction, số nguyên là item ID, bỏ trùng trong mỗi giao dịch.
- App 1: file ecommerce có `item item ... last_item:timestamp`, lấy **phần trước dấu `:`** làm items và loại riêng timestamp; giữ mỗi giao dịch là một tập item. Map `@ITEM=id=name` để hiện tên sản phẩm. Cần mô tả thêm việc bộ dữ liệu gốc đã được SPMF chuyển đổi trước đó.
- App 2: UCI Optdigits lưu 64 cường độ ảnh 8x8 + label; không dùng nhãn để học codebook. Mỗi patch 2x2 là vector 4 chiều, k-means NumPy biến thành visual word, mỗi ảnh chuyển thành tập visual-word ID. Số lần visual word xuất hiện trong ảnh được gộp về 1 vì FIM dùng tập hợp.
- Dữ liệu tại `data/toy/*` là ví dụ **synthetic do dự án viết**, không trích từ SPMF.

## Quyền sử dụng và liêm chính

- Không sao chép hoặc đọc mã nguồn thuật toán trên SPMF/GitHub để triển khai.
- Chỉ dùng SPMF dưới dạng phần mềm đối chiếu output do SPMF chạy độc lập, không import/copy code.
- Báo cáo cả kết quả không khớp, lỗi hoặc timeout; không xem các trường hợp này là phép đo hoàn tất.
- Tôn trọng giấy phép riêng của mỗi bộ dữ liệu khi phát hành trên GitHub/Hugging Face.
