"""One command from VS Code terminal: tests, data download, benchmark, apps, plots.
Optional --spmf-jar enables actual external correctness and time comparison.
Every failure aborts this workflow; no invented results or success flags.
"""
import argparse
import subprocess
import sys


def step(*cmd):
    print('\n>>>', ' '.join(map(str,cmd)),flush=True)
    subprocess.run([sys.executable,'-m',*cmd],check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spmf-jar', default=None, help='Path to official SPMF jar; Java required')
    ap.add_argument('--quick', action='store_true', help='Smoke test only, NOT submission')
    ap.add_argument('--skip-download', action='store_true')
    opts = ap.parse_args()
    step('pytest','-q')
    if not opts.skip_download:step('scripts.download_data')
    step('scripts.dataset_statistics')
    step('scripts.benchmark', *(['--quick'] if opts.quick else []))
    if opts.spmf_jar:step('scripts.run_spmf','--jar',opts.spmf_jar)
    if not opts.quick:step('scripts.rss_memory')
    if not opts.quick:
        step('scripts.scalability')
        step('scripts.length_experiment')
    step('scripts.market_app')
    step('scripts.visual_app')
    step('scripts.plot_results')
    step('scripts.generate_report_tables')
    step('scripts.check_submission')
    print('\nRun finished. Inspect results and fill report/student/public URLs before submission.')

if __name__ == '__main__':main()
