from src.market import load_ecommerce,read_name_map,top_rules
from src.visual import numpy_kmeans,encode_visual_transactions,mine_visual_patterns
import numpy as np

def test_ecommerce_timestamp_parse(tmp_path):
    p=tmp_path/'sample.txt';p.write_text('5 7 7:129116328\n8 9:129116364\n')
    assert load_ecommerce(p)==[[5,7],[8,9]]
    names=tmp_path/'labels.txt';names.write_text('@ITEM=5=Milk\n@ITEM=7=Bread\n')
    assert read_name_map(names)=={5:'Milk',7:'Bread'}

def test_market_names_and_lift():
    tx=[[1,2],[1,2],[1,2],[1],[2],[3]]
    rows=top_rules(tx,{1:'Milk',2:'Bread'},minsup=0.3,minconf=0.5)
    assert any(r['X']=='Milk' and r['Y']=='Bread' for r in rows)

def test_bovw_determinism():
    images=np.zeros((6,8,8))
    images[0:3,1:5,2:4]=0.8
    images[3:6,3:7,3:6]=1.0
    a,ta,ca=mine_visual_patterns(images,4,minsup=0.3)
    b,tb,cb=mine_visual_patterns(images,4,minsup=0.3)
    assert ta==tb and a.supports==b.supports and np.allclose(ca,cb)
