import pytest

from rushtools import CODON_TABLE, find_orfs, gc_content, hamming, kmer_count, reverse_complement, translate


def test_gc_content_basic():
    assert gc_content("GGCC") == 1.0
    assert gc_content("ATAT") == 0.0
    assert gc_content("atgc") == pytest.approx(0.5)


def test_gc_content_ignores_n_by_default():
    assert gc_content("GCNN") == 1.0
    assert gc_content("GCNN", ignore_n=False) == 0.5


def test_gc_content_empty_raises():
    with pytest.raises(ValueError, match="no A/C/G/T"):
        gc_content("NNNN")


@pytest.mark.parametrize("seq, expected", [
    ("ATGC", "GCAT"),
    ("AAAACCCGGT", "ACCGGGTTTT"),
    ("atgN", "Ncat"),
    ("", ""),
])
def test_reverse_complement(seq, expected):
    assert reverse_complement(seq) == expected


def test_reverse_complement_twice_is_identity():
    s = "ATGCRYKMNacgt"
    assert reverse_complement(reverse_complement(s)) == s


def test_codon_table_is_complete():
    assert len(CODON_TABLE) == 64
    assert CODON_TABLE["ATG"] == "M"
    assert sorted(c for c, aa in CODON_TABLE.items() if aa == "*") == ["TAA", "TAG", "TGA"]


def test_translate():
    assert translate("ATGTGGTAA") == "MW*"
    assert translate("ATGTGGTAAGGG", to_stop=True) == "MW"
    assert translate("AUGNNNUGG") == "MXW"
    assert translate("CATGTGG", frame=1) == "MW"


def test_translate_bad_frame():
    with pytest.raises(ValueError):
        translate("ATG", frame=3)


def test_find_orfs_both_strands():
    seq = "CCATGAAATTTGGGTAACC" + reverse_complement("ATGCCCGGGAAATTTTGA") + "GG"
    orfs = find_orfs(seq, min_len=12)
    assert [(o["strand"], o["start"], o["end"]) for o in orfs] == [("+", 3, 17), ("-", 20, 37)]
    assert orfs[0]["protein"] == "MKFG"


def test_kmer_count():
    assert kmer_count("ATATA", 2) == {"AT": 2, "TA": 2}
    with pytest.raises(ValueError):
        kmer_count("ATG", 0)


def test_hamming():
    assert hamming("GATTACA", "GACTATA") == 2
    with pytest.raises(ValueError):
        hamming("ATG", "AT")


def test_gc_content_ignores_all_ambiguity_codes():
    # matches the R package: anything other than A/C/G/T leaves the denominator
    assert gc_content("GCRYSS") == 1.0
    assert gc_content("GCRYSS", ignore_n=False) == pytest.approx(2 / 6)


def test_kmer_count_case_insensitive_and_skips_ambiguous():
    assert kmer_count("acgNN", 2) == {"AC": 1, "CG": 1}
    assert kmer_count("acgNN", 2, skip_ambiguous=False) == {"AC": 1, "CG": 1, "GN": 1, "NN": 1}
