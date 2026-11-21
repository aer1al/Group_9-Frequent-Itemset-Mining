"""Independent tests for benchmark threshold schedule and reference score."""
from scripts.benchmark import proposed_min_counts
from scripts.run_spmf import compare_maps
from src.algorithm.eclat import mine

def test_adaptive_thresholds_are_distinct_and_nonempty():
    tx=[[0]*0+[0,1,2] for _ in range(18)] + [[0,1] for _ in range(30)] + [[0] for _ in range(50)]
    ms=proposed_min_counts(tx)
    assert len(ms)==6
    assert ms==sorted(ms,reverse=True)
    assert ms[0]==98 and ms[-1]>=1
    assert all(mine(tx,threshold,'bitset').supports for threshold in ms)

def test_reference_metrics_detect_support_mismatch():
    exact=compare_maps({(1,):3,(2,):4},{(1,):3,(2,):4})
    assert exact['exact_match'] and exact['matching_rate']==1.0
    wrong=compare_maps({(1,):3,(2,):4},{(1,):4,(3,):4})
    assert wrong['matched_patterns']==0
    assert wrong['matching_rate']==0.0

def test_reference_metrics_detect_missing_itemsets():
    result=compare_maps({(1,):2,(1,2):1},{(1,):2})
    assert result['matching_rate']==0.5
