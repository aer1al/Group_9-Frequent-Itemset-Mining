"""Association rules from own Eclat support dictionary. No FIM dependencies."""
from dataclasses import dataclass
from itertools import combinations

@dataclass(frozen=True)
class Rule:
    antecedent: tuple[int,...]
    consequent: tuple[int,...]
    support: float
    confidence: float
    lift: float


def make_rules(supports:dict, n_transactions:int, minconf:float=0.5):
    if not (0<minconf<=1): raise ValueError('minconf must be in (0,1]')
    out=[]
    for items,sxy in supports.items():
        if len(items)<2: continue
        for r in range(1,len(items)):
            for left in combinations(items,r):
                right=tuple(x for x in items if x not in left)
                sx=supports.get(left)
                sy=supports.get(right)
                if not sx or not sy: continue
                conf=sxy/sx
                if conf+1e-12<minconf: continue
                out.append(Rule(left,right,sxy/n_transactions,conf,conf/(sy/n_transactions)))
    return sorted(out,key=lambda rule:(-rule.lift,-rule.confidence,-rule.support,rule.antecedent,rule.consequent))
