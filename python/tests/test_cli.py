import pytest

from rushtools.cli import main
from rushtools.parsers import write_fasta


def test_cli_revcomp(capsys):
    assert main(["revcomp", "AAACCG"]) == 0
    assert capsys.readouterr().out.strip() == "CGGTTT"


def test_cli_stats(tmp_path, capsys):
    fasta = tmp_path / "x.fasta"
    write_fasta([("a", "A" * 100), ("b", "C" * 300)], fasta)
    assert main(["stats", str(fasta)]) == 0
    out = capsys.readouterr().out
    assert "sequences\t2" in out and "n50\t300" in out


def test_cli_missing_file(capsys):
    assert main(["gc", "does_not_exist.fasta"]) == 1
    assert "error" in capsys.readouterr().err


def test_cli_gc_reports_na_for_all_n_record(tmp_path, capsys):
    fasta = tmp_path / "n.fasta"
    write_fasta([("allN", "NNNN"), ("b", "ACGT")], fasta)
    assert main(["gc", str(fasta)]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[1:] == ["allN\t4\tNA", "b\t4\t0.500"]


def test_cli_stats_empty_file(tmp_path, capsys):
    fasta = tmp_path / "empty.fasta"
    fasta.write_text("")
    assert main(["stats", str(fasta)]) == 1
    assert "no sequences found" in capsys.readouterr().err


def test_cli_empty_header_is_clean_error(tmp_path, capsys):
    fasta = tmp_path / "bad.fasta"
    fasta.write_text(">\nACGT\n")
    assert main(["gc", str(fasta)]) == 1
    assert "empty FASTA header" in capsys.readouterr().err


def test_cli_orfs(tmp_path, capsys):
    fasta = tmp_path / "orf.fasta"
    write_fasta([("g", "CC" + "ATG" + "GCT" * 10 + "TAA" + "CC")], fasta)
    assert main(["orfs", str(fasta), "--min-len", "30"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[1] == "g\t+\t3\t38\t36\t11"


def test_cli_gc_rejects_negative_digits(tmp_path, capsys):
    # used to print "NA" for every record instead of complaining
    fasta = tmp_path / "x.fasta"
    write_fasta([("a", "ACGT")], fasta)
    with pytest.raises(SystemExit) as exc:
        main(["gc", str(fasta), "--digits", "-1"])
    assert exc.value.code == 2
    assert "must be 0 or more" in capsys.readouterr().err


def test_cli_gc_digits(tmp_path, capsys):
    fasta = tmp_path / "x.fasta"
    write_fasta([("a", "GGC")], fasta)
    assert main(["gc", str(fasta), "-d", "0"]) == 0
    assert capsys.readouterr().out.splitlines()[1] == "a\t3\t1"


def test_cli_revcomp_rejects_non_dna(capsys):
    # used to print "OLLEH" -> "OLLED" without any warning
    assert main(["revcomp", "HELLO"]) == 1
    assert "not a DNA sequence" in capsys.readouterr().err


def test_cli_revcomp_accepts_iupac_and_lowercase(capsys):
    assert main(["revcomp", "acgtRY"]) == 0
    assert capsys.readouterr().out.strip() == "RYacgt"
