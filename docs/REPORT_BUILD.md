**Name:** Thiều Quang  
**ID:** 24127114
**Thành viên:** Tôn Thất Việt Khoa — 24127190  
**Môn học:** Khai thác dữ liệu và ứng dụng (*Data Mining and Applications*)  
**Đề bài:** [HCMUS — Khai thác tập mục phổ biến](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/itemset/)

# Biên dịch và hoàn thiện báo cáo

Báo cáo được viết bằng tiếng Việt theo định dạng IEEE conference. Đề bài yêu cầu nội dung chính dài 10–15 trang. Nguồn LaTeX là `docs/Report.tex`; bảng thực nghiệm được tạo từ các CSV bởi lệnh:

```powershell
python -m scripts.generate_report_tables
```

Sau đó mở Terminal VS Code, chạy từ thư mục repo:

```powershell
cd docs
xelatex -interaction=nonstopmode -halt-on-error Report.tex
xelatex -interaction=nonstopmode -halt-on-error Report.tex
cd ..
```

Cần cài MiKTeX/TeX Live + font Noto Serif/Noto Sans; LaTeX source là `docs/Report.tex`, kết quả `docs/Report.pdf`.

Các CSV benchmark, đối chiếu SPMF, hai ứng dụng, scalability và transaction length nằm trong `results/`. Tệp `results/spmf_comparison.csv` hiện ghi nhận 25/25 cấu hình khớp chính xác, gồm sáu mức BMS_WebView_1; mã item của BMS được ánh xạ tạm khi chạy SPMF và đổi ngược trước khi so sánh. Để tạo SVG, PDF hình và bảng LaTeX từ kết quả hiện có, chạy từ thư mục gốc:

```powershell
python -m scripts.plot_results
python -m scripts.add_report_figures
python -m scripts.generate_report_tables
```

Sau đó biên dịch `Report.tex` hai lượt bằng XeLaTeX như hướng dẫn ở trên. Trước khi nộp, xác minh lại mọi bảng/hình, tài liệu tham khảo, liên kết công khai và số trang; không thay dữ liệu chưa có bằng giá trị suy đoán.

Tệp `docs/generated/experiment_data.tex` được sinh tự động; không sửa tay các số liệu trong tệp này. Báo cáo đã được biên dịch lại sau khi bổ sung biểu đồ số frequent itemset theo minsup và cập nhật thông tin hai thành viên; PDF hiện có 14 trang tổng cộng, với tài liệu tham khảo bắt đầu ở trang cuối. Nếu tiếp tục chỉnh sửa, hãy biên dịch lại hai lượt bằng XeLaTeX và kiểm tra PDF đầu ra.
