import gzip

import pytest

from rushtools import n50, read_fasta, read_fastq, write_fasta


def test_fasta_roundtrip(tmp_path):
    records = [("seq1", "ATG" * 30), ("seq2", "GGCC")]
    path = tmp_path / "x.fasta"
    assert write_fasta(records, path, width=10) == 2
    assert list(read_fasta(path)) == records
    assert path.read_text().splitlines()[1] == "ATGATGATGA"      # wrapped at 10


def test_fasta_gzip(tmp_path):
    path = tmp_path / "x.fa.gz"
    write_fasta([("a", "ACGT")], path)
    with gzip.open(path, "rt") as fh:
        assert fh.read() == ">a\nACGT\n"
    assert list(read_fasta(path)) == [("a", "ACGT")]


def test_fasta_without_header_raises(tmp_path):
    path = tmp_path / "bad.fasta"
    path.write_text("ACGT\n>a\nACGT\n")
    with pytest.raises(ValueError):
        list(read_fasta(path))


def test_read_fastq(tmp_path):
    path = tmp_path / "r.fastq"
    path.write_text("@r1 extra\nACGT\n+\nII5!\n")
    assert list(read_fastq(path)) == [("r1", "ACGT", [40, 40, 20, 0])]


def test_n50():
    assert n50([100, 200, 300, 400, 500]) == 400
    assert n50([2, 2, 2, 3, 3, 4, 8, 8]) == 8
    with pytest.raises(ValueError):
        n50([])


def test_fasta_empty_header_raises(tmp_path):
    path = tmp_path / "bad.fasta"
    path.write_text(">\nACGT\n")
    with pytest.raises(ValueError, match="empty FASTA header"):
        list(read_fasta(path))


def test_fastq_empty_header_raises(tmp_path):
    path = tmp_path / "bad.fastq"
    path.write_text("@\nACGT\n+\nIIII\n")
    with pytest.raises(ValueError, match="empty FASTQ header"):
        list(read_fastq(path))


def test_fastq_tolerates_blank_lines_and_gzip(tmp_path):
    path = tmp_path / "r.fastq.gz"
    with gzip.open(path, "wt") as fh:
        fh.write("@r1\nAC\n+\nII\n\n@r2\nGT\n+\n!!\n\n")
    assert [r[0] for r in read_fastq(path)] == ["r1", "r2"]


def test_fastq_malformed_raises(tmp_path):
    path = tmp_path / "bad.fastq"
    path.write_text("@r1\nACGT\n+\nII\n")
    with pytest.raises(ValueError, match="malformed"):
        list(read_fastq(path))


def test_read_fastq_windows_line_endings(tmp_path):
    # text mode turns \r\n into \n, so files saved on Windows read cleanly
    path = tmp_path / "crlf.fastq"
    path.write_bytes(b"@r1\r\nACGT\r\n+\r\nII5!\r\n")
    assert list(read_fastq(path)) == [("r1", "ACGT", [40, 40, 20, 0])]
