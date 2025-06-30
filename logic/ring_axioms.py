# checks ring axioms that haven't been implemented yet
from typing import List, Optional, Tuple

Table = List[List[int]]

def is_associative(table: Table) -> Optional[Tuple[int, int, int]]:
    """Check if table is associative: (a * b) * c == a * (b * c) for all a, b, c."""
    n = len(table)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                left = table[table[a][b]][c]
                right = table[a][table[b][c]]
                if left != right:
                    return (a, b, c)
    return None

def has_additive_inverses(add_table: Table, zero: int) -> Optional[int]:
    """Check that every element has an inverse: a + (-a) = 0."""
    n = len(add_table)
    for a in range(n):
        if not any(add_table[a][b] == zero for b in range(n)):
            return a
    return None

def is_distributive(add: Table, mul: Table) -> Optional[Tuple[int, int, int, str]]:
    """Check distributivity of multiplication over addition."""
    n = len(add)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                # Left distributive: a*(b+c) == a*b + a*c
                bc = add[b][c]
                left = mul[a][bc]
                right = add[mul[a][b]][mul[a][c]]
                if left != right:
                    return (a, b, c, "left")

                # Right distributive: (a+b)*c == a*c + b*c
                ab = add[a][b]
                left = mul[ab][c]
                right = add[mul[a][c]][mul[b][c]]
                if left != right:
                    return (a, b, c, "right")
    return None
