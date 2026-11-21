from itertools import combinations
from random import Random
import pytest
from src.algorithm.eclat import mine, min_support_count
from src.rules import make_rules
from src.utils import read_transactions,read_fim_output,write_fim_output


def exhaustive(data,min_count):
    all_items=sorted(set(x for row in data for x in row))
    return {tuple(items): sum(set(items)<=set(row) for row in data)
            for k in range(1,len(all_items)+1)
            for items in combinations(all_items,k)
            if sum(set(items)<=set(row) for row in data)>=min_count}

@pytest.mark.parametrize('database',[
    [[1,2],[2,3],[1,2,3],[2]],
    [[1],[1],[1]],
    [[1,2,3,4],[2,4],[1,3,4],[]],
    [[-4,5],[-4,5],[5],[]],
    [[1,1,2],[1,2],[2,3],[1,3]],
    [[10,20,30],[20,30,40],[10,40],[20,40]],
])
@pytest.mark.parametrize('minsup',[0.25,0.5,0.75,1.0,2])
def test_five_or_more_dbs_against_independent_exhaustive(database,minsup):
    expected=exhaustive(database,min_support_count(minsup,len(database)))
    assert mine(database,minsup,'set').supports==expected
    assert mine(database,minsup,'bitset').supports==expected


def test_randomized():
    random=Random(2026)
    for _ in range(20):
        database=[random.sample(range(1,8),random.randrange(0,5)) for _ in range(10)]
        for variant in ('bitset','set'):
            assert mine(database,0.3,variant).supports==exhaustive(database,3)


def test_known_supports_and_rules():
    data=[[1,2,3],[1,2],[1,3],[2,3],[1,2,3],[2]]
    results=mine(data,0.5).supports
    assert results[(1,2)]==3
    assert results[(2,)]==5
    rules=make_rules(results,len(data),0.5)
    match=[x for x in rules if x.antecedent==(1,) and x.consequent==(2,)]
    assert len(match)==1 and abs(match[0].confidence-0.75)<1e-12


def test_export_reference_format(tmp_path):
    results=mine([[1,2],[1],[2]],0.3).supports
    path=tmp_path/'output.txt'
    write_fim_output(results,path)
    assert read_fim_output(path)==results


def test_reject_invalid(tmp_path):
    bad=tmp_path/'bad.txt';bad.write_text('1 -1 2 -2\n')
    with pytest.raises(ValueError): read_transactions(bad)
    with pytest.raises(ValueError): mine([[1]],0)
