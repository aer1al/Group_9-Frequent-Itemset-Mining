"""Render reproducible SVG charts directly from REAL benchmark CSVs (stdlib only)."""
from pathlib import Path
import csv
import html
from collections import defaultdict
from math import log2
from scripts.benchmark import ROOT, RATIOS

PALETTE={'set':'#3c6796','bitset':'#c2643b','SPMF':'#577e53'}
PATTERN_PALETTE={
    'foodmart':'#3c6796',
    'c20d10k':'#c2643b',
    't25i10d10k':'#577e53',
    'BMS_WebView_1':'#7b5492',
}

def read(path):
    with path.open(encoding='utf-8',newline='') as fd: return list(csv.DictReader(fd))

def chart(series, title, xlabel, ylabel, out):
    clean={key: sorted((float(a),float(b)) for a,b in data if a is not None and b is not None)
           for key,data in series.items() if data}
    clean={k:v for k,v in clean.items() if v}
    if not clean:return
    allpts=[point for data in clean.values() for point in data]
    xmin=min(x for x,y in allpts);xmax=max(x for x,y in allpts)
    ymin=0; ymax=max(y for x,y in allpts)*1.12 or 1
    lx,ty,rx,by=83,53,792,420
    px=lambda x:lx+(x-xmin)/(xmax-xmin or 1)*(rx-lx)
    py=lambda y:by-(y-ymin)/(ymax-ymin)*(by-ty)
    body=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 490">',
          '<rect width="850" height="490" fill="#ffffff"/>',
          f'<text x="20" y="26" font-size="17" font-family="Arial" font-weight="bold">{html.escape(title)}</text>',
          f'<path d="M {lx},{ty} V {by} H {rx}" stroke="#666" fill="none"/>']
    for fraction in (0,.25,.5,.75,1):
        yv=fraction*ymax;y=py(yv)
        body.append(f'<line x1="{lx}" y1="{y:.2f}" x2="{rx}" y2="{y:.2f}" stroke="#e6e6e6"/>')
        body.append(f'<text x="{lx-9}" y="{y+5:.2f}" text-anchor="end" font-size="11">{yv:.3g}</text>')
    for key, points in clean.items():
        color=PALETTE.get(key,'#7b5492')
        coords=' '.join(f'{px(x):.2f},{py(y):.2f}' for x,y in points)
        body.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2.7"/>')
        body.extend(f'<circle cx="{px(x):.2f}" cy="{py(y):.2f}" r="3.7" fill="{color}"/>' for x,y in points)
    for ii,key in enumerate(clean):
        x=lx+ii*200
        body.append(f'<line x1="{x}" y1="460" x2="{x+30}" y2="460" stroke="{PALETTE.get(key,"#7b5492")}" stroke-width="3"/>')
        body.append(f'<text x="{x+36}" y="465" font-family="Arial" font-size="12">{html.escape(key)}</text>')
    body.extend([f'<text x="{lx}" y="450" font-size="11">{xmin:g} - {xmax:g} ({html.escape(xlabel)})</text>',
                 f'<text x="19" y="44" font-size="11">{html.escape(ylabel)}</text>',
                 '</svg>'])
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text('\n'.join(body),encoding='utf-8')
    print('Chart:',out.relative_to(ROOT))


def pattern_summary_chart(rows, out):
    datasets=defaultdict(list)
    for row in rows:
        if row['status']=='ok' and row['backend']=='bitset':
            datasets[row['dataset']].append(
                (
                    100*int(row['min_count'])/int(row['max_singleton_support']),
                    int(row['itemset_count']),
                )
            )

    if set(datasets)!=set(PATTERN_PALETTE):
        raise ValueError(f'Expected four benchmark datasets, found {sorted(datasets)}')
    if any(len(points)!=6 for points in datasets.values()):
        raise ValueError('Expected six successful minsup measurements per dataset')

    left,top,right,bottom=95,58,785,400
    labels=[int(ratio*100) for ratio in RATIOS]
    x_positions=[
        left+index*(right-left)/(len(labels)-1)
        for index in range(len(labels))
    ]
    max_count=max(count for points in datasets.values() for _,count in points)
    log_max=max(1, max_count.bit_length())

    def y_position(count):
        return bottom-log2(count)/log_max*(bottom-top)

    body=[
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 500" '
        'font-family="Arial">',
        '<rect width="850" height="500" fill="#ffffff"/>',
        '<text x="20" y="27" font-size="17" font-family="Arial" font-weight="bold">'
        'Frequent itemset count vs minsup</text>',
        f'<path d="M {left},{top} V {bottom} H {right}" stroke="#666" fill="none"/>',
    ]
    for exponent in range(log_max+1):
        count=2**exponent
        y=y_position(count)
        body.append(
            f'<line x1="{left}" y1="{y:.2f}" x2="{right}" y2="{y:.2f}" '
            'stroke="#e6e6e6"/>'
        )
        body.append(
            f'<text x="{left-10}" y="{y+4:.2f}" text-anchor="end" '
            f'font-size="11">{count}</text>'
        )
    for x,minsup in zip(x_positions,labels):
        body.append(
            f'<line x1="{x:.2f}" y1="{bottom}" x2="{x:.2f}" y2="{bottom+5}" '
            'stroke="#666"/>'
        )
        body.append(
            f'<text x="{x:.2f}" y="{bottom+20}" text-anchor="middle" '
            f'font-size="11">{minsup:g}%</text>'
        )

    for dataset,points in datasets.items():
        points.sort(key=lambda point:point[0],reverse=True)
        color=PATTERN_PALETTE[dataset]
        coords=' '.join(
            f'{x:.2f},{y_position(count):.2f}'
            for x,(_,count) in zip(x_positions,points)
        )
        body.append(
            f'<polyline points="{coords}" fill="none" stroke="{color}" '
            'stroke-width="2.7"/>'
        )
        body.extend(
            f'<circle cx="{x:.2f}" cy="{y_position(count):.2f}" r="3.7" '
            f'fill="{color}"/>'
            for x,(_,count) in zip(x_positions,points)
        )

    for index,dataset in enumerate(datasets):
        x=105+(index%2)*330
        y=458+(index//2)*20
        color=PATTERN_PALETTE[dataset]
        body.append(
            f'<line x1="{x}" y1="{y-4}" x2="{x+25}" y2="{y-4}" '
            f'stroke="{color}" stroke-width="3"/>'
        )
        body.append(
            f'<text x="{x+32}" y="{y}" font-family="Arial" '
            f'font-size="12">{html.escape(dataset)}</text>'
        )
    body.extend([
        '<text x="440" y="438" text-anchor="middle" font-size="12">'
        'MinSup (% của support singleton lớn nhất trên từng dữ liệu)</text>',
        '<text x="20" y="45" font-size="11">'
        'Số frequent itemset (thang log cơ số 2)</text>',
        '</svg>',
    ])
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text('\n'.join(body),encoding='utf-8')
    print('Chart:',out.relative_to(ROOT))


def main():
    src=ROOT/'results'/'benchmark.csv'
    if not src.exists():
        print('Benchmark CSV not found; no real plot to generate');return
    data=[r for r in read(src) if r['status']=='ok']
    pattern_summary_chart(data,ROOT/'results'/'charts'/'all_datasets_patterns.svg')
    comparison=ROOT/'results'/'spmf_comparison.csv'
    ref = {(r['dataset'],int(r['min_count'])):r for r in read(comparison) if r['status']=='ok'} if comparison.exists() else {}
    names=sorted({r['dataset'] for r in data})
    for label in names:
        rows=[r for r in data if r['dataset']==label]
        sec=defaultdict(list); memory=defaultdict(list)
        for r in rows:
            x=float(r['minsup_percentage']);backend=r['backend']
            sec[backend].append((x,r['seconds']))
            memory[backend].append((x,r['peak_python_mb']))
            if backend=='bitset':
                refrow=ref.get((label,int(r['min_count'])))
                if refrow and refrow.get('spmf_seconds_with_jvm_start'):
                    sec['SPMF'].append((x,refrow['spmf_seconds_with_jvm_start']))
        chart(sec,label+': time vs min support','minsup %','Runtime seconds',
              ROOT/'results'/'charts'/f'{label}_runtime.svg')
        chart(memory,label+': Python peak allocations','minsup %','Peak MiB',
              ROOT/'results'/'charts'/f'{label}_memory.svg')
        counts=[(r['minsup_percentage'],r['itemset_count']) for r in rows if r['backend']=='bitset']
        chart({'bitset':counts},label+': frequent itemset count','minsup %','Patterns',
              ROOT/'results'/'charts'/f'{label}_patterns.svg')
    for filename,field in (('scalability.csv','fraction'),('length_experiment.csv','avg_transaction_length')):
        path=ROOT/'results'/filename
        if path.exists():
            rows=[r for r in read(path) if r['status']=='ok']
            chart({'bitset':[(r[field],r['seconds']) for r in rows]},
                  filename,'Dataset scale' if field=='fraction' else 'Mean transaction length',
                  'Runtime seconds', ROOT/'results'/'charts'/f'{path.stem}.svg')

if __name__ == '__main__':main()
