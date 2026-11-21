"""Fill author's submission metadata ONLY; does not assert experiments were run."""
import argparse
from pathlib import Path
from scripts.benchmark import ROOT


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--name',required=True)
    parser.add_argument('--student-id',required=True)
    parser.add_argument('--email',required=True)
    parser.add_argument('--github',required=True,help='Public repository HTTPS URL')
    parser.add_argument('--colab',required=True,help='Public Colab notebook HTTPS URL')
    args=parser.parse_args()
    if not args.github.startswith('https://github.com/'):
        raise SystemExit('Please enter a public github.com URL')
    if not (args.colab.startswith('https://colab.research.google.com/') or
            args.colab.startswith('https://drive.google.com/')):
        raise SystemExit('Please enter a public Google Colab URL')
    original=ROOT/'README.md'
    report=ROOT/'docs/Report.tex'
    r=original.read_text(encoding='utf-8')
    t=report.read_text(encoding='utf-8')
    r=r.replace('`CHUA_DIEN`',f'`{args.name} — {args.student_id}`')
    r=r.replace('https://github.com/YOUR_ACCOUNT/YOUR_REPO',args.github.rstrip('/'))
    r=r.replace('`COLAB_LINK_HERE`',args.colab)
    t=t.replace('[Điền họ tên và MSSV]',args.name + ' -- ' + args.student_id)
    t=t.replace('[Điền email]',args.email)
    original.write_text(r,encoding='utf-8')
    report.write_text(t,encoding='utf-8')
    print('Metadata updated. VERIFY URLs public and refresh docs/Report.pdf with XeLaTeX.')
    print('Other experimental TODOs are NOT marked complete by this script.')

if __name__=='__main__':main()
