**Name:** Thiều Quang  
**ID:** 24127114
**Thành viên:** Tôn Thất Việt Khoa — 24127190
**Môn học:** Khai thác dữ liệu và ứng dụng (*Data Mining and Applications*)
**Đề bài:** [HCMUS — Khai thác tập mục phổ biến](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/)

# Kết quả thực nghiệm

Các kết quả trong thư mục này được tạo bởi những script của dự án. Hiện có CSV benchmark, đối chiếu SPMF, RSS, thống kê dữ liệu, hai ứng dụng, scalability và transaction length; biểu đồ SVG nằm trong `charts/`. CSV hiện ghi nhận 25/25 phép đối chiếu itemset-support với SPMF khớp chính xác, gồm cả sáu mức trên BMS_WebView_1. Trên BMS, ID item được ánh xạ tạm về miền liên tiếp khi gọi SPMF rồi đổi ngược trước khi so sánh; dữ liệu gốc không bị thay đổi. `all_datasets_patterns.svg` so sánh số frequent itemset theo minsup trên bốn bộ benchmark. Chỉ diễn giải các phép đo có trạng thái thành công trong CSV.
