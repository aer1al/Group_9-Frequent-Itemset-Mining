"""Document vertical representations used by Eclat (TID-set and bitset)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class VerticalItem:
    item_id: int
    transaction_ids: frozenset[int]

    @property
    def support(self):
        return len(self.transaction_ids)

    def to_bitset(self):
        mask=0
        for tid in self.transaction_ids:
            mask |= (1<<tid)
        return mask
