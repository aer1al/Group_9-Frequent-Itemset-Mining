"""Measure true peak process RSS for set/bitset in isolated Python child processes.
Windows PeakWorkingSetSize; Linux ru_maxrss. One dataset and median minsup each.
"""
from pathlib import Path
import argparse
import csv
import ctypes
import json
import os
import subprocess
import sys
import time
from scripts.benchmark import ROOT,DATA
from src.utils import read_transactions
from src.algorithm.eclat import mine


def process_peak_rss_mib():
    if sys.platform == 'win32':
        from ctypes import wintypes
        class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
            _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD),
                ('PeakWorkingSetSize',ctypes.c_size_t),('WorkingSetSize',ctypes.c_size_t),
                ('QuotaPeakPagedPoolUsage',ctypes.c_size_t),('QuotaPagedPoolUsage',ctypes.c_size_t),
                ('QuotaPeakNonPagedPoolUsage',ctypes.c_size_t),('QuotaNonPagedPoolUsage',ctypes.c_size_t),
                ('PagefileUsage',ctypes.c_size_t),('PeakPagefileUsage',ctypes.c_size_t)]
        counters=PROCESS_MEMORY_COUNTERS()
        counters.cb=ctypes.sizeof(counters)
        fn=ctypes.windll.psapi.GetProcessMemoryInfo
        fn.argtypes=[wintypes.HANDLE,ctypes.POINTER(PROCESS_MEMORY_COUNTERS),wintypes.DWORD]
        fn.restype=wintypes.BOOL
        handle=ctypes.windll.kernel32.GetCurrentProcess()
        if not fn(handle,ctypes.byref(counters),counters.cb):
            raise OSError('GetProcessMemoryInfo failed')
        return counters.PeakWorkingSetSize/(1024*1024)
    import resource
    ru=resource.getrusage(resource.RUSAGE_SELF)
    return ru.ru_maxrss/ (1024*1024 if sys.platform=='darwin' else 1024)


def worker(dataset,threshold,backend):
    inp=ROOT/'data/benchmark'/f'{dataset}.txt'
    tx=read_transactions(inp)
    start=time.perf_counter()
    output=mine(tx,threshold,backend,max_results=1000000)
    elapsed=time.perf_counter()-start
    print(json.dumps({'dataset':dataset,'min_count':threshold,'backend':backend,
       'seconds':round(elapsed,6), 'peak_rss_mib':round(process_peak_rss_mib(),4),
       'patterns':len(output.supports),'status':'ok'}))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--worker',action='store_true')
    parser.add_argument('--dataset',choices=DATA)
    parser.add_argument('--threshold',type=int)
    parser.add_argument('--backend',choices=['set','bitset'])
    args=parser.parse_args()
    if args.worker:
        worker(args.dataset,args.threshold,args.backend)
        return
    benchmark=ROOT/'results/benchmark.csv'
    if not benchmark.exists():raise SystemExit('Run benchmark first')
    with benchmark.open(encoding='utf-8') as fd:raw=list(csv.DictReader(fd))
    rows=[]
    for label in DATA:
        thresholds=sorted({int(r['min_count']) for r in raw if r['dataset']==label and r['status']=='ok'}, reverse=True)
        if len(thresholds)<6:
            print(label,'must have 6 valid support thresholds, skipping');continue
        k=thresholds[len(thresholds)//2]
        for backend in ('set','bitset'):
            proc=subprocess.run([sys.executable,'-m','scripts.rss_memory','--worker',
                   '--dataset',label,'--threshold',str(k),'--backend',backend],
                   text=True,capture_output=True)
            if proc.returncode:
                data={'dataset':label,'min_count':k,'backend':backend,'seconds':'',
                      'peak_rss_mib':'','patterns':'','status':'invalid:'+proc.stderr[-500:]}
            else:
                data=json.loads(proc.stdout.strip())
            rows.append(data)
            print('Process RAM:',label,k,backend,data.get('peak_rss_mib'),flush=True)
    output=ROOT/'results/rss_memory.csv'
    with output.open('w',encoding='utf-8',newline='') as fd:
        cols=['dataset','min_count','backend','seconds','peak_rss_mib','patterns','status']
        w=csv.DictWriter(fd,fieldnames=cols);w.writeheader();w.writerows(rows)
    print('Saved:',output)

if __name__=='__main__':main()
