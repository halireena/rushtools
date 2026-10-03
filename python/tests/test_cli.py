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
