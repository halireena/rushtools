"""Assembly statistics."""
from __future__ import annotations

from collections.abc import Iterable


def n50(lengths: Iterable[int]) -> int:
    """Return the N50: the length L such that contigs >= L hold at least half of all bases.

    >>> n50([100, 200, 300, 400, 500])
    400
    """
    lengths = sorted(lengths, reverse=True)
    if not lengths:
        raise ValueError("no lengths given")
    total = sum(lengths)
    running = 0
    for length in lengths:
        running += length
        if running * 2 >= total:
            return length
    raise AssertionError("unreachable")  # pragma: no cover
