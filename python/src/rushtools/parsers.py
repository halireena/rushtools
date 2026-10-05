"""Streaming readers and a writer for FASTA and FASTQ (plain or gzipped)."""
from __future__ import annotations

import gzip
from collections.abc import Iterable, Iterator
from pathlib import Path


def _open_text(path, mode: str = "rt"):
    path = Path(path)
    if path.suffix == ".gz":
        return gzip.open(path, mode, encoding="utf-8")
    return open(path, mode, encoding="utf-8")


def read_fasta(path) -> Iterator[tuple[str, str]]:
    """Yield (id, sequence) for each record; the id is the first word of the header."""
    rid, chunks = None, []
    with _open_text(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if rid is not None:
                    yield rid, "".join(chunks)
                words = line[1:].split()
                if not words:
                    raise ValueError(f"{path}: empty FASTA header")
                rid, chunks = words[0], []
            else:
                if rid is None:
                    raise ValueError(f"{path}: sequence before the first '>' header")
                chunks.append(line)
    if rid is not None:
        yield rid, "".join(chunks)


def read_fastq(path) -> Iterator[tuple[str, str, list[int]]]:
    """Yield (id, sequence, Phred+33 quality scores) for each read."""
    with _open_text(path) as fh:
        while True:
            header = fh.readline()
            if not header:
                return
            if not header.strip():
                continue  # tolerate blank lines between records
            seq = fh.readline().rstrip("\n")
            plus = fh.readline()
            qual = fh.readline().rstrip("\n")
            if not header.startswith("@") or not plus.startswith("+") or len(seq) != len(qual):
                raise ValueError(f"{path}: malformed FASTQ record near {header.strip()!r}")
            words = header[1:].split()
            if not words:
                raise ValueError(f"{path}: empty FASTQ header")
            yield words[0], seq, [ord(c) - 33 for c in qual]


def write_fasta(records: Iterable[tuple[str, str]], path, width: int = 60) -> int:
    """Write (id, sequence) pairs to FASTA, wrapping lines at `width`. Returns the number written."""
    n = 0
    with _open_text(path, "wt") as out:
        for rid, seq in records:
            out.write(f">{rid}\n")
            for i in range(0, len(seq), width):
                out.write(seq[i:i + width] + "\n")
            n += 1
    return n
