"""Generate TeX tables from observed experiment CSV files ONLY.
Never fabricate missing metrics. The report remains a draft until validated.
"""
from pathlib import Path
import csv
from collections import defaultdict
from scripts.benchmark import ROOT

OUT=ROOT/'docs'/'generated'/'experiment_data.tex'

def read(path):
    if not path.is_file():return []
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def esc(s):
    return str(s).replace('\\',r'\textbackslash{}').replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#').replace('$',r'\$').replace('{',r'\{').replace('}',r'\}')

def fmt(value,precision=4):
    try:return f'{float(value):.{precision}f}'
    except (ValueError,TypeError):return '--'

def main():
    benchmark = read(ROOT/'results'/'benchmark.csv')
    ref = {(r['dataset'],r['min_count']):r for r in read(ROOT/'results'/'spmf_comparison.csv')}
    markets = read(ROOT/'results'/'market_top10.csv')
    visions = read(ROOT/'results'/'visual_patterns.csv')
    lines=[r'% Auto-generated from actual CSV results. Do not edit hand-written numbers here.',
           r'\section{Kết quả đo đã ghi nhận và đối chiếu}',
           r'Mọi giá trị trong các bảng tiếp theo chỉ được lấy từ tệp CSV do chương trình chạy trên máy tạo ra; dấu gạch ngang biểu thị thiếu dữ liệu. Phép đo SPMF bao gồm thời gian khởi động JVM. Peak Python MiB chỉ phản ánh phân bổ Python đo bằng tracemalloc.']
    if not benchmark:
        lines.append(r'\textit{Chưa có kết quả benchmark thực. Không thể công bố đường cong hiệu năng hoặc tỉ lệ khớp SPMF.}')
    else:
        for label in dict.fromkeys(r['dataset'] for r in benchmark):
            label_rows=[r for r in benchmark if r['dataset']==label]
            grouped=defaultdict(dict)
            for r in label_rows:grouped[r['min_count']][r['backend']]=r
            # Let compact tables share pages instead of queueing behind wide figures.
            lines.extend([r'\begin{table}[!htbp]',r'\centering\scriptsize',
                          r'\caption{Kết quả đo thực của '+esc(label)+r' theo support tuyệt đối.}',
                          r'\begin{tabular}{@{}rrrrrr@{}}\toprule',
                          r'$k$ & \#FI & Set(s) & Bit(s) & SPMF(s) & Khớp \\ \midrule'])
            for threshold in sorted(grouped, key=lambda x:int(x),reverse=True):
                b=grouped[threshold].get('bitset',{});s=grouped[threshold].get('set',{})
                rr=ref.get((label,threshold),{})
                mark='CÓ' if rr.get('exact_match')=='True' else ('KHÔNG' if rr.get('exact_match')=='False' else '?')
                lines.append(' & '.join([str(threshold),str(b.get('itemset_count') or '--'),
                     fmt(s.get('seconds')),fmt(b.get('seconds')),
                     fmt(rr.get('spmf_seconds_with_jvm_start')),mark])+r' \\')
            lines.extend([r'\bottomrule\end{tabular}',r'\end{table}'])
    if markets:
        lines.extend([r'\begin{table*}[!tp]',r'\centering\scriptsize',
                      r'\caption{Top-10 luật kết hợp từ dữ liệu ECommerce thực, xếp theo lift.}',
                      r'\begin{tabular}{@{}p{.32\textwidth}p{.32\textwidth}rrr@{}}\toprule',
                      r'Vế trái $X$ & Vế phải $Y$ & Support & Confidence & Lift \\ \midrule'])
        for r in markets[:10]:
            lines.append(' & '.join([esc(r['X'])[:240],esc(r['Y'])[:240],fmt(r['support']),
                                     fmt(r['confidence']),fmt(r['lift'])])+r' \\')
        lines.extend([r'\bottomrule\end{tabular}',r'\end{table*}'])
    else:lines.append(r'\textit{Chưa có output luật giỏ hàng thực tế.}')
    if visions:
        lines.extend([r'\begin{table}[!htbp]',r'\centering\scriptsize',
                      r'\caption{Năm mẫu visual words phổ biến nhất trên ảnh UCI Optdigits.}',
                      r'\begin{tabular}{@{}lrr@{}}\toprule',
                      r'Visual-word itemset & Support & Tỉ lệ \\ \midrule'])
        for r in visions[:5]:
            lines.append(' & '.join([esc(r['visual_words']),r['support_count'],fmt(r['support_fraction'])])+r' \\')
        lines.extend([r'\bottomrule\end{tabular}',r'\end{table}'])
    else:lines.append(r'\textit{Chưa có output visual patterns thực tế.}')
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Generated:',OUT.relative_to(ROOT))

if __name__=='__main__': main()
