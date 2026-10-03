"""rushtools: small, tested helpers for plant bioinformatics.

The most useful functions are imported here, so users can write
``from rushtools import gc_content`` instead of ``from rushtools.seq import gc_content``.
"""
from rushtools.assembly import n50
from rushtools.parsers import read_fasta, read_fastq, write_fasta
from rushtools.seq import (
    CODON_TABLE,
    find_orfs,
    gc_content,
    hamming,
    kmer_count,
    reverse_complement,
    translate,
)

__version__ = "0.1.0"

__all__ = [
    "CODON_TABLE",
    "find_orfs",
    "gc_content",
    "hamming",
    "kmer_count",
    "n50",
    "read_fasta",
    "read_fastq",
    "reverse_complement",
    "translate",
    "write_fasta",
]
