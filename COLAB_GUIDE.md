**Name:** Thiều Quang  
**ID:** 24127114
**Thành viên:** Tôn Thất Việt Khoa — 24127190  
**Môn học:** Khai thác dữ liệu và ứng dụng (*Data Mining and Applications*)  
**Đề bài:** [HCMUS — Khai thác tập mục phổ biến](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/)

# Hướng dẫn chạy notebook trên Google Colab

Tài liệu này hướng dẫn mở notebook và chạy các bước thực nghiệm trên Colab. Đây là hướng dẫn sử dụng, không thay thế yêu cầu công bố repository và nộp bài theo quy định của học phần.

## Tệp cần chuẩn bị

1. `notebooks/Project2.ipynb` — notebook thực nghiệm chính. Có thể tải bản sao `Eclat_Experiments.ipynb` ở thư mục gốc lên Colab.
2. Gói ZIP chứa toàn bộ dự án, gồm tối thiểu `src/`, `scripts/`, `data/`, `tests/` và `docs/`. Tên gói được yêu cầu ở bước tải lên notebook.

Chỉ tải notebook lên Colab là chưa đủ để chạy thuật toán: mã nguồn Eclat nằm trong thư mục `src/`.

## Quy trình chạy

1. Mở [Google Colab](https://colab.research.google.com/), đăng nhập và chọn **File → Upload notebook**.
2. Tải lên `Eclat_Experiments.ipynb` và kết nối runtime Python.
3. Chạy ô khởi tạo đầu tiên. Nếu được yêu cầu chọn tệp, tải lên gói ZIP đầy đủ của dự án.
4. Chạy các ô tiếp theo theo thứ tự. Kiểm tra thông báo lỗi và trạng thái của mỗi bước trước khi tiếp tục.
5. Nếu tải SPMF tự động không thành công, lấy JAR từ [trang tải SPMF chính thức](https://www.philippe-fournier-viger.com/spmf/index.php?link=download.php) và dùng ô tải tệp dự phòng.
6. Chạy ô cuối để tạo gói kết quả. Tải gói về máy và lưu đúng cấu trúc thư mục trước khi cập nhật báo cáo.

## Kiểm tra kết quả

Kiểm tra các tệp CSV benchmark, đối chiếu SPMF, đầu ra ứng dụng, thống kê, biểu đồ và `docs/generated/experiment_data.tex`. Không báo cáo phép đo bị lỗi, bị giới hạn hoặc chưa chạy như kết quả hoàn chỉnh. Khi chạy trên Colab, ghi rõ môi trường runtime; không gán kết quả đó cho máy Windows cá nhân.

Phiên Colab có thể bị ngắt hoặc xóa. Hãy tải gói kết quả về máy sau khi hoàn tất.

## Hình thức nộp

Theo đề bài, sinh viên nộp đường dẫn repository GitHub công khai trên Moodle và cung cấp liên kết notebook Colab công khai trong README. Việc tải notebook hoặc ZIP lên Colab chỉ phục vụ chạy thực nghiệm, không thay thế các yêu cầu này.
