from typing import List, Optional, Tuple, Dict, Any

Element = Any  # Maybe make this stricter later idk (e.g. int, str)
Table = List[List[Element]]

def is_commutative(mul_table: Table) -> Tuple[bool, Optional[Tuple[int, int]]]:
    """Check if multiplication is commutative: a * b == b * a"""
    n = len(mul_table)
    for i in range(n):
        for j in range(n):
            if mul_table[i][j] != mul_table[j][i]:
                return False, (i, j)
    return True, None

def find_multiplicative_identity(mul_table: Table) -> Optional[int]:
    """Return the index of the identity element if it exists."""
    n = len(mul_table)
    for e in range(n):
        if all(mul_table[e][i] == i and mul_table[i][e] == i for i in range(n)):
            return e
    return None

def has_zero_divisors(mul_table: Table, zero_index: int = 0) -> Optional[Tuple[int, int]]:
    """Check for zero divisors: a ≠ 0, b ≠ 0, but a * b == 0"""
    n = len(mul_table)
    for i in range(n):
        for j in range(n):
            if i != zero_index and j != zero_index and mul_table[i][j] == zero_index:
                return (i, j)
    return None

def is_integral_domain(mul_table: Table, zero_index: int = 0) -> Tuple[bool, Optional[Tuple[int, int]]]:
    """True if no zero divisors and ring has identity."""
    identity = find_multiplicative_identity(mul_table)
    if identity is None:
        return False, None
    zd = has_zero_divisors(mul_table, zero_index)
    if zd:
        return False, zd
    return True, None

def is_division_ring(mul_table: Table, zero_index: int = 0) -> Tuple[bool, Optional[int]]:
    """Check if every non-zero element has a multiplicative inverse."""
    identity = find_multiplicative_identity(mul_table)
    if identity is None:
        return False, None
    n = len(mul_table)
    for a in range(n):
        if a == zero_index:
            continue
        has_inverse = any(mul_table[a][b] == identity and mul_table[b][a] == identity for b in range(n))
        if not has_inverse:
            return False, a
    return True, None

def analyze_ring(mul_table: Table) -> Dict[str, Dict[str, Any]]:
    """Run all checks and return a structured result."""
    result = {}

    commutative, counter1 = is_commutative(mul_table)
    result["commutative"] = {
        "value": commutative,
        "counterexample": counter1
    }

    identity = find_multiplicative_identity(mul_table)
    result["has identity"] = {
        "value": identity is not None,
        "identity": identity
    }

    integral_domain, counter2 = is_integral_domain(mul_table)
    result["integral domain"] = {
        "value": integral_domain,
        "zero divisors": counter2
    }

    division_ring, missing_inverse = is_division_ring(mul_table)
    result["division ring"] = {
        "value": division_ring,
        "missing inverse": missing_inverse
    }

    return result
