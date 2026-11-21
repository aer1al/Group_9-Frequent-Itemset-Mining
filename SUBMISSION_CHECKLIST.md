**Name:** Thiều Quang  
**ID:** 24127114
**Thành viên:** Tôn Thất Việt Khoa — 24127190  
**Môn học:** Khai thác dữ liệu và ứng dụng (*Data Mining and Applications*)  
**Đề bài:** [HCMUS — Khai thác tập mục phổ biến](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/)

# Danh mục kiểm tra trước khi nộp đồ án

Đề bài chính thức: [Khai thác tập mục phổ biến — HCMUS](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/).

## Cài đặt và kiểm chứng

- [ ] Đọc và có thể giải thích cách Eclat mở rộng tiền tố bằng phép giao TID-set, điều kiện support và cách tỉa nhánh.
- [ ] Chạy toàn bộ kiểm thử tự động; cập nhật README bằng kết quả của lần chạy cuối.
- [ ] Xác minh đầu vào/đầu ra theo định dạng SPMF và các trường hợp giao dịch rỗng, mục trùng, ngưỡng support.
- [ ] Đối chiếu từng itemset và support với SPMF trên mọi cặp dữ liệu–minsup cần báo cáo; giải thích tất cả sai khác hoặc lần chạy lỗi.

## Thực nghiệm

- [ ] Lưu URL nguồn, SHA-256 và thống kê được tính từ từng tệp dữ liệu đã tải.
- [ ] Hoàn tất các mức minsup được chọn cho ít nhất bốn bộ benchmark; không tính lần chạy lỗi hoặc bị giới hạn output là kết quả hoàn tất.
- [ ] Báo cáo số lượng itemset, thời gian chạy và peak memory; phân biệt `tracemalloc` với RSS tiến trình.
- [ ] Hoàn thành thí nghiệm scalability, ảnh hưởng của độ dài giao dịch và biểu đồ so sánh với SPMF trong cùng điều kiện.
- [ ] Chạy ứng dụng Market Basket và Bag of Visual Words trên dữ liệu nguồn; bổ sung top-10 luật, nhận xét và giới hạn.
- [ ] Ghi môi trường phần cứng/phần mềm, seed, tham số và các lần chạy không thành công để bảo đảm khả năng tái lập.

## Báo cáo và công bố

- [ ] Hoàn thiện báo cáo tiếng Việt theo mẫu IEEE conference, đạt 10–15 trang nội dung chính (không tính tài liệu tham khảo và phụ lục).
- [ ] Đảm bảo mọi bảng, hình và kết luận được dẫn chiếu trong văn bản, có nguồn và dựa trên kết quả đã xác minh.
- [ ] Kiểm tra thông tin sinh viên, các khai báo cần thiết về công cụ AI và quy định học phần.
- [x] Chạy notebook trên Google Colab từ đầu đến cuối trong một phiên sạch (tác giả xác nhận).
- [ ] Xác minh quyền truy cập công khai của link Colab bằng cửa sổ đăng xuất.
- [ ] Đưa mã nguồn lên repository GitHub công khai với lịch sử commit trung thực; nộp duy nhất đường dẫn repository theo hướng dẫn của học phần.

Trạng thái hiện tại của các tệp kết quả trong workspace: cả 48 lượt benchmark đều thành công; các CSV thống kê, RSS, scalability (5 mức), transaction length (5 mức), top-10 luật và visual patterns đã có. CSV đối chiếu SPMF ghi nhận 25/25 cấu hình khớp chính xác, gồm cả 6/6 mức BMS_WebView_1. Biểu đồ số frequent itemset theo minsup và nhận xét mật độ dữ liệu đã có trong `docs/Report.pdf`; PDF đã biên dịch lại thành công, 14 trang tổng cộng, tài liệu tham khảo bắt đầu ở trang cuối. Tác giả xác nhận notebook đã chạy sạch từ đầu đến cuối; quyền truy cập công khai của link Colab vẫn chưa xác minh được vì lượt kiểm tra ẩn danh chuyển đến trang đăng nhập Google.

Chương trình `python -m scripts.check_submission` hỗ trợ kiểm tra một số điều kiện tự động; kết quả của chương trình không thay thế việc rà soát báo cáo và kiểm tra thực nghiệm.
