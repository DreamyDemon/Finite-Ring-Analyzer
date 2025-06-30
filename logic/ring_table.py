# logic/ring_table.py
from typing import List, Union, Tuple, Any
import re

def build_znz_table(n: int) -> List[List[int]]:
    """Return multiplication table for Z/nZ."""
    return [[(i * j) % n for j in range(n)] for i in range(n)]

def validate_custom_table(table: List[List[int]]) -> bool:
    """Core checks: square, all entries in 0..n-1."""
    n = len(table)
    if any(len(row) != n for row in table):
        return False
    valid = set(range(n))
    return all(x in valid for row in table for x in row)

def validate_addition_table(add_table: List[List[int]], zero_index: int = 0) -> None:
    """Raise if not a valid commutative group table with identity at zero_index."""
    if not validate_custom_table(add_table):
        raise ValueError("Addition table must be square with entries 0..n-1.")
    n = len(add_table)
    # Commutativity
    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]:
                raise ValueError(f"Addition not commutative at ({i},{j}).")
    # Identity at zero_index
    for i in range(n):
        if add_table[zero_index][i] != i or add_table[i][zero_index] != i:
            raise ValueError(f"Addition identity must be element {zero_index} (row/col).")

def validate_multiplication_table(mul_table: List[List[int]]) -> None:
    """Raise if not a valid multiplication table (shape + range)."""
    if not validate_custom_table(mul_table):
        raise ValueError("Multiplication table must be square with entries 0..n-1.")

def parse_fast_blocks(
    text: str,
    custom: bool = False
) -> List[Union[List[List[int]], Tuple[List[List[int]], List[List[int]]]]]:
    """
    Parses fast-input batches separated by blank lines (optional).

    - custom=False (Z/nZ): each block must be 2 lines (n + elems); returns mul-table only.
    - custom=True  (Custom):
        * 2-line blocks: ZnZ‑style subset → returns (add, mul).
        * 1+2*n-line blocks: full custom tables → returns (add, mul).
        * Otherwise: ValueError.
    """
    raw_blocks = re.split(r"\n\s*\n", text.strip())
    out: List[Any] = []

    for idx, blk in enumerate(raw_blocks, start=1):
        lines = [l.strip() for l in blk.splitlines() if l.strip()]
        if not lines:
            continue

        # 1) Read n
        try:
            n = int(lines[0])
        except ValueError:
            raise ValueError(f"Batch {idx}: expected integer n, got '{lines[0]}'")

        # 2) Z/nZ tab
        if not custom:
            if len(lines) != 2:
                raise ValueError(f"Batch {idx}: Z/nZ fast mode needs 2 lines (n + elems), got {len(lines)}")
            elems = [int(x) for x in re.split(r"[,\s]+", lines[1]) if x]
            if any(e < 0 or e >= n for e in elems):
                raise ValueError(f"Batch {idx}: elems must be in 0..{n-1}, got {elems}")
            mul = [[(a*b) % n for b in elems] for a in elems]
            out.append(mul)
            continue

        # 3) Custom tab: ZnZ‑style fallback (2 lines)
        if len(lines) == 2:
            elems = [int(x) for x in re.split(r"[,\s]+", lines[1]) if x]
            if any(e < 0 or e >= n for e in elems):
                raise ValueError(f"Batch {idx}: elems must be in 0..{n-1}, got {elems}")
            add = [[(a+b) % n for b in elems] for a in elems]
            mul = [[(a*b) % n for b in elems] for a in elems]
            out.append((add, mul))
            continue

        # 4) Custom tab: full custom tables (1 + 2*n lines)
        if len(lines) == 1 + 2*n:
            add_rows = lines[1:1+n]
            mul_rows = lines[1+n:1+2*n]
            def parse_tbl(rows: List[str], kind: str) -> List[List[int]]:
                tbl = []
                for r, row in enumerate(rows, start=1):
                    nums = [int(x) for x in re.split(r"[,\s]+", row) if x]
                    if len(nums) != n:
                        raise ValueError(f"Batch {idx} {kind} row {r}: need {n}, got {len(nums)}")
                    tbl.append(nums)
                return tbl
            out.append((parse_tbl(add_rows, "Addition"), parse_tbl(mul_rows, "Multiplication")))
            continue

        # Otherwise invalid
        raise ValueError(f"Batch {idx}: invalid number of lines ({len(lines)}) for n={n}")

    return out
