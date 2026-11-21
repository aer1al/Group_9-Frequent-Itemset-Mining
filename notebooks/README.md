**Name:** Thiều Quang  
**ID:** 24127114
**Thành viên:** Tôn Thất Việt Khoa — 24127190  
**Môn học:** Khai thác dữ liệu và ứng dụng (*Data Mining and Applications*)  
**Đề bài:** [HCMUS — Khai thác tập mục phổ biến](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/)

# Notebook thực nghiệm Eclat — Python + Julia

Notebook chính: [`Project2.ipynb`](Project2.ipynb) (26 cells; lần chạy Colab đã lưu không có output lỗi). Có thể dùng bản tên dễ nhận diện [`Eclat_Experiments.ipynb`](../Eclat_Experiments.ipynb). Link Colab được chia sẻ:
https://colab.research.google.com/drive/1zk6pnHh-6Xea7r3L5pFuSz2ZveCDUJTf?usp=sharing

Trên Colab, mở notebook, chạy phần khởi tạo rồi upload ZIP mã nguồn đầy đủ khi ô yêu cầu. Các bước chính gồm kiểm thử và benchmark Python, đối chiếu SPMF bằng `scripts.run_spmf_fixed`, hai ứng dụng market basket và visual words, Julia (kiểm thử/benchmark/đối chiếu), rồi xuất ZIP kết quả. Bản `tools/spmf.jar` hiện dùng yêu cầu Java 25, notebook có bước cấu hình môi trường Java.

Kết quả đã xác minh: Python benchmark 48/48; Python–SPMF 25/25 khi tính toy; Julia benchmark 48/48; Julia–SPMF 24/24; top-10 luật kết hợp; 37 mẫu visual words. Kết quả được lưu trong `results/` và ZIP xuất từ Colab. Lưu ý phiên bản Julia ở Colab khác bản trên Windows; thời gian chạy giữa Python/Julia/SPMF không được hiểu là so sánh tốc độ thuần thuật toán.

Để chạy trực tiếp trên Windows, mở `D:\Group_9` trong VS Code rồi chạy lệnh Python/Julia trong **Terminal PowerShell**, không cần mở Jupyter trong VS Code. Xem [`README.md` ở thư mục gốc](../README.md) và [hướng dẫn Colab](../COLAB_GUIDE.md).
