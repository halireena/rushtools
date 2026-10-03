"""Sequence helpers: GC content, reverse complement, translation, ORFs, k-mers, Hamming distance."""
from __future__ import annotations

_COMP = str.maketrans("ACGTRYSWKMBDHVNacgtryswkmbdhvn", "TGCAYRSWMKVHDBNtgcayrswmkvhdbn")

_BASES = "TCAG"
_AMINO = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
#: The standard genetic code (NCBI table 1) as {codon: one-letter amino acid}; '*' = stop.
CODON_TABLE: dict[str, str] = {
    a + b + c: _AMINO[16 * i + 4 * j + k]
    for i, a in enumerate(_BASES)
    for j, b in enumerate(_BASES)
    for k, c in enumerate(_BASES)
}
_STOPS = {"TAA", "TAG", "TGA"}


def gc_content(seq: str, ignore_n: bool = True) -> float:
    """Return the GC fraction (0-1) of a DNA sequence.

    Args:
        seq: DNA sequence, any case.
        ignore_n: leave N bases out of the denominator.

    Raises:
        ValueError: if the sequence has no usable bases.

    >>> gc_content("ATGC")
    0.5
    """
    s = seq.upper()
    gc = s.count("G") + s.count("C")
    denom = len(s) - s.count("N") if ignore_n else len(s)
    if denom == 0:
        raise ValueError("sequence has no A/C/G/T bases")
    return gc / denom


def reverse_complement(seq: str) -> str:
    """Return the reverse complement (keeps case; handles IUPAC codes).

    >>> reverse_complement("AAACCG")
    'CGGTTT'
    """
    return seq.translate(_COMP)[::-1]


def translate(seq: str, *, to_stop: bool = False, frame: int = 0, unknown: str = "X") -> str:
    """Translate DNA (or RNA) to protein with the standard genetic code.

    Args:
        seq: nucleotide sequence; U is read as T.
        to_stop: stop at, and exclude, the first stop codon.
        frame: 0, 1 or 2.
        unknown: letter for codons containing N or other symbols.

    >>> translate("ATGTGGTAA")
    'MW*'
    """
    if frame not in (0, 1, 2):
        raise ValueError("frame must be 0, 1 or 2")
    s = seq.upper().replace("U", "T")
    out = []
    for i in range(frame, len(s) - 2, 3):
        aa = CODON_TABLE.get(s[i:i + 3], unknown)
        if to_stop and aa == "*":
            break
        out.append(aa)
    return "".join(out)


def find_orfs(seq: str, min_len: int = 30) -> list[dict]:
    """Find ATG-to-stop ORFs (stop codon included) in all six frames.

    Returns dicts with strand, frame, start, end (1-based inclusive forward-strand
    coordinates), length (nt) and protein, sorted by start.
    """
    s_fwd = seq.upper()
    n = len(s_fwd)
    orfs = []
    for strand, s in (("+", s_fwd), ("-", reverse_complement(s_fwd))):
        for frame in range(3):
            i = frame
            while i + 3 <= n:
                if s[i:i + 3] != "ATG":
                    i += 3
                    continue
                j = i
                while j + 3 <= n and s[j:j + 3] not in _STOPS:
                    j += 3
                if j + 3 > n:
                    break
                length = j + 3 - i
                if length >= min_len:
                    start, end = (i + 1, j + 3) if strand == "+" else (n - (j + 3) + 1, n - i)
                    orfs.append({"strand": strand, "frame": frame, "start": start, "end": end,
                                 "length": length, "protein": translate(s[i:j + 3], to_stop=True)})
                i = j + 3
    return sorted(orfs, key=lambda o: (o["start"], o["strand"]))


def kmer_count(seq: str, k: int) -> dict[str, int]:
    """Count overlapping k-mers. Returns {kmer: count}."""
    if k < 1:
        raise ValueError("k must be >= 1")
    counts: dict[str, int] = {}
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i + k]
        counts[kmer] = counts.get(kmer, 0) + 1
    return counts


def hamming(a: str, b: str) -> int:
    """Number of positions at which two equal-length sequences differ."""
    if len(a) != len(b):
        raise ValueError(f"sequences differ in length: {len(a)} vs {len(b)}")
    return sum(x != y for x, y in zip(a, b))
