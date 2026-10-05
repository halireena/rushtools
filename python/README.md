# rushtools

Small, tested Python helpers for everyday plant bioinformatics, built while learning Python.
No dependencies beyond the Python standard library. Needs Python 3.10 or newer.

## Install

```bash
pip install "git+https://github.com/halireena/rushtools#subdirectory=python"         # latest version
pip install "git+https://github.com/halireena/rushtools@main#subdirectory=python"    # a branch or tag after @
```

(`pip install git+...` needs git installed.)

For development (editable install + tests), in a virtual environment:

```bash
git clone https://github.com/halireena/rushtools.git
cd rushtools/python
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest          # unit tests + the examples in the docstrings
ruff check .    # lint
```

The examples below use the tiny made-up files in
[`../examples/`](../examples/) and are run from the top `rushtools` folder:

```bash
cd ..    # from rushtools/python back to rushtools, where examples/ lives
```

(If you installed without cloning, download
[`examples/genes.fasta`](../examples/genes.fasta) or use your own FASTA file.)
New words (ORF, N50, Phred...) are explained in the
[glossary](../README.md#glossary).

## Use in Python

```python
from rushtools import gc_content, reverse_complement, translate, read_fasta, n50

gc_content("ATGCGC")              # 0.6666666666666666  (4 of 6 bases are G or C)
reverse_complement("ATGC")        # 'GCAT'
translate("ATGTGGTAA")            # 'MW*'   (* = stop codon)
translate("ATGTGGTAA", to_stop=True)  # 'MW'
n50([100, 200, 300, 400, 500])    # 400

for rid, seq in read_fasta("examples/genes.fasta"):
    print(rid, len(seq))
```

```text
geneA 125
geneB 32
geneC 27
scaffold_gap 20
```

| Function | What it does |
|---|---|
| `gc_content(seq, ignore_n=True)` | GC fraction (0-1). N and other non-ACGT letters are left out unless `ignore_n=False`. Raises `ValueError` if there are no A/C/G/T bases. |
| `reverse_complement(seq)` | Reverse complement; keeps upper/lower case and handles IUPAC codes. |
| `translate(seq, to_stop=False, frame=0)` | DNA or RNA to protein with the standard genetic code; `*` marks a stop, `X` a codon with N. |
| `find_orfs(seq, min_len=30)` | ATG-to-stop open reading frames in all six frames, as dicts with `strand`, `frame`, `start`, `end` (1-based, on the forward strand), `length` (nt, stop included) and `protein`. |
| `kmer_count(seq, k)` | Counts of every overlapping k-mer, e.g. `kmer_count("ATATG", 2)` gives `{'AT': 2, 'TA': 1, 'TG': 1}`. |
| `hamming(a, b)` | Number of mismatches between two equal-length sequences. |
| `read_fasta(path)` | Yields `(id, sequence)` per record; the id is the first word of the header. Plain or `.gz`. |
| `read_fastq(path)` | Yields `(id, sequence, qualities)` per read, with qualities as Phred scores (`I` = 40). Plain or `.gz`; 4-line records. |
| `write_fasta(records, path, width=60)` | Writes `(id, sequence)` pairs; returns how many were written. |
| `n50(lengths)` | N50 of a list of contig lengths. |
| `CODON_TABLE` | The standard genetic code as `{"ATG": "M", ...}`. |

ORFs in the example gene:

```python
from rushtools import find_orfs, read_fasta

seqs = dict(read_fasta("examples/genes.fasta"))
for orf in find_orfs(seqs["geneA"], min_len=90):
    print(orf["strand"], orf["start"], orf["end"], orf["length"], orf["protein"])
```

```text
+ 6 113 108 MPGYRSLSATSQNLGMLLSRRSLSTRLATSGLKKN
```

## Use on the command line

Every command prints a tab-separated table (or a single sequence) and
`rushtools COMMAND --help` explains its options.

```bash
rushtools --help
rushtools gc examples/genes.fasta
rushtools stats examples/genes.fasta
rushtools revcomp ATGCCC
rushtools orfs examples/genes.fasta --min-len 90
```

Output of the last four:

```text
id	length	gc
geneA	125	0.496
geneB	32	0.875
geneC	27	0.095
scaffold_gap	20	NA
```

```text
sequences	4
total_bp	204
longest	125
n50	125
```

```text
GGGCAT
```

```text
id	strand	start	end	length_nt	protein_aa
geneA	+	6	113	108	35
```

`gc` prints `NA` for a record with no A/C/G/T bases; `-d 2` changes the
number of decimals. In `orfs`, `length_nt` includes the stop codon and
`protein_aa` does not. To save a table: `rushtools gc examples/genes.fasta > gc.tsv`.

## Licence

MIT. Changes between versions: [CHANGELOG.md](CHANGELOG.md).
