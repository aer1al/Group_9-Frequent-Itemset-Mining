from src.algorithm.eclat import mine
from src.utils import read_fim_output, write_fim_output

def test_set_bitset_match(tmp_path):
    tx=[[1,2,3],[1,2],[2,3],[1,3],[2],[1]]
    baseline=mine(tx,0.35,'set').supports
    optimized=mine(tx,0.35,'bitset').supports
    assert baseline==optimized
    p=tmp_path/'ref.txt';write_fim_output(baseline,p)
    assert read_fim_output(p)==optimized
