# rushtools

[![Python tests](https://github.com/halireena/rushtools/actions/workflows/python-tests.yml/badge.svg)](https://github.com/halireena/rushtools/actions/workflows/python-tests.yml)
[![R CMD check](https://github.com/halireena/rushtools/actions/workflows/r-tests.yml/badge.svg)](https://github.com/halireena/rushtools/actions/workflows/r-tests.yml)

My personal function libraries for everyday plant bioinformatics, in two languages:

| Folder      | What it is                                   |
|-------------|----------------------------------------------|
| `python/`   | Python package `rushtools` (`src/` layout, `pyproject.toml`, `tests/`): DNA sequence helpers, FASTA/FASTQ readers, assembly stats and a `rushtools` command |
| `r/`        | R package `rushtools` (`R/`, `tests/`, `DESCRIPTION`): GC content, reverse complements, fold changes, z-scores, p-value adjustment, tidying differential expression tables |
| `examples/` | Tiny made-up FASTA and FASTQ files so every example below runs as written |

Tests for both run automatically on every push (see the Actions tab).
New to some of the words? See the [glossary](#glossary) at the bottom.

## What you need first

- **git**, to download the code (`git --version` to check)
- **Python 3.10 or newer** for the Python package (`python --version`; on macOS/Linux it may be called `python3`)
- **R 4.0 or newer** for the R package (`R --version`)

You only need the language you plan to use.

## Getting started in 5 minutes (Python)

Run these in a terminal. They download the code, make a private Python
environment (a "virtual environment", so nothing clashes with other projects),
install the package and try it on the example files.

```bash
git clone https://github.com/halireena/rushtools.git
cd rushtools
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e "./python[dev]"
rushtools --version
```

```text
rushtools 0.2.0
```

Now ask it about the example FASTA file. Each command prints a
tab-separated table you can paste into a spreadsheet:

```bash
rushtools stats examples/genes.fasta     # sequence count, total bp, longest, N50
```

```text
sequences	4
total_bp	204
longest	125
n50	125
```

```bash
rushtools gc examples/genes.fasta        # GC content per sequence (NA for all-N records)
```

```text
id	length	gc
geneA	125	0.496
geneB	32	0.875
geneC	27	0.095
scaffold_gap	20	NA
```

`scaffold_gap` is only `N`s (unknown bases), so it has no GC content to report.

```bash
rushtools orfs examples/genes.fasta --min-len 90
```

```text
id	strand	start	end	length_nt	protein_aa
geneA	+	6	113	108	35
```

One open reading frame in `geneA`, on the forward (`+`) strand, from base 6 to
base 113: 108 nucleotides including the stop codon, which code for 35 amino acids.

```bash
rushtools revcomp ATGCCC
```

```text
GGGCAT
```

And the same from Python (save as a `.py` file and run it from the `rushtools` folder,
or paste it into `python`):

```python
from rushtools import gc_content, read_fasta

for rid, seq in read_fasta("examples/genes.fasta"):
    try:
        print(rid, round(gc_content(seq), 3))
    except ValueError as err:   # the all-N record has no real bases to count
        print(rid, "skipped:", err)
```

```text
geneA 0.496
geneB 0.875
geneC 0.095
scaffold_gap skipped: sequence has no A/C/G/T bases
```

Reading sequencing reads with their quality scores:

```python
from rushtools import read_fastq

for rid, seq, quals in read_fastq("examples/reads.fastq"):
    print(rid, seq, "mean quality:", round(sum(quals) / len(quals), 1))
```

```text
read1 ATGCCGGGGTACCGTAGTTT mean quality: 40.0
read2 GTCTGCGACCTCACAAAATT mean quality: 30.5
read3 TGGGCATGCNTTTATCCCGA mean quality: 12.5
```

More Python functions and options: [`python/README.md`](python/README.md).
To use your own data, swap `examples/genes.fasta` for the path to your file
(plain or gzipped, e.g. `my_genes.fa.gz`).

When you are done, `deactivate` leaves the virtual environment; next time,
`cd rushtools` and `source .venv/bin/activate` again.

### Install without cloning

If you just want the package and not the example files or tests:

```bash
pip install "git+https://github.com/halireena/rushtools#subdirectory=python"
```

## Getting started (R)

Start R **from the top `rushtools` folder** you cloned above and install the
package straight from the `r/` folder. This needs no extra packages:

```r
install.packages("r", repos = NULL, type = "source")
library(rushtools)
```

Or install from GitHub without cloning:

```r
install.packages("remotes")   # once
remotes::install_github("halireena/rushtools", subdir = "r")
library(rushtools)
```

Then:

```r
gc_content(c(a = "ATGC", b = "GGCC"))
#>   a   b
#> 0.5 1.0

reverse_complement("ATGCRY")    # R and Y are IUPAC codes for "A or G" and "C or T"
#> [1] "RYGCAT"

# a differential expression result, e.g. from limma
res <- data.frame(gene = c("g1", "g2", "g3"),
                  logFC = c(2.1, -1.5, 0.2),
                  P.Value = c(0.0001, 0.003, 0.7))
tidy_de_table(res, lfc_col = "logFC", p_col = "P.Value")
#>   gene log2fc pvalue   padj direction
#> 1   g1    2.1  1e-04 0.0003        up
#> 2   g2   -1.5  3e-03 0.0045      down
#> 3   g3    0.2  7e-01 0.7000        ns
```

`tidy_de_table()` renames the columns to `log2fc`, `pvalue` and `padj`
(BH-adjusted p-value), and calls a gene `up` or `down` when `padj < 0.05` and
the fold change is at least 2x (`|log2fc| >= 1`). Every function has a help
page, e.g. `?tidy_de_table`. Full list: [`r/README.md`](r/README.md).

## Run the tests locally

Python (from the top `rushtools` folder, with the virtual environment active):

```bash
cd python
pytest          # unit tests + the examples in the docstrings
ruff check .    # lint (style and common-mistake checks)
cd ..
```

R (needs `install.packages("testthat")` once):

```bash
cd r
Rscript -e 'testthat::test_local(".")'
cd ..
```

or, if you use devtools, `devtools::test()` inside R.

## Glossary

| Term | Meaning |
|---|---|
| **FASTA** | Plain-text file of sequences. Each record is a `>` header line (the first word is the ID) followed by one or more lines of sequence. See [`examples/genes.fasta`](examples/genes.fasta). |
| **FASTQ** | Plain-text file of sequencing reads, 4 lines per read: `@ID`, sequence, `+`, and one quality character per base. See [`examples/reads.fastq`](examples/reads.fastq). |
| **Phred quality** | How sure the sequencer is about a base: Q = -10 log10(error probability). Q20 = 1 error in 100, Q30 = 1 in 1000, Q40 = 1 in 10,000. In FASTQ files each score is stored as the character with code Q + 33 (`I` = 40, `5` = 20, `!` = 0). |
| **GC content** | Fraction of bases that are G or C (0 to 1). Differs between genomes and genes; very high or low values can affect PCR and sequencing. |
| **N / IUPAC codes** | Letters for uncertain bases: `N` = any base, `R` = A or G, `Y` = C or T, `S` = G or C, `W` = A or T, `K` = G or T, `M` = A or C, `B`/`D`/`H`/`V` = "not A/C/G/T" respectively. |
| **Reverse complement** | The sequence of the other DNA strand, read in its own 5'->3' direction: swap A<->T and C<->G, then reverse. |
| **Strand / frame** | DNA is read in triplets (codons), so each strand has 3 possible reading frames: 6 in total. `+` is the sequence as written, `-` its reverse complement. |
| **ORF** | Open reading frame: a stretch that starts with the start codon `ATG` and runs to a stop codon (`TAA`, `TAG`, `TGA`). A candidate protein-coding region. |
| **k-mer** | Every substring of length k. `ATATG` has the 2-mers `AT`, `TA`, `AT`, `TG`. |
| **Hamming distance** | Number of positions at which two equal-length sequences differ. |
| **Contig / N50** | Contigs are the pieces a genome assembly is made of. N50 is the contig length L such that contigs of length L or longer hold at least half of all bases; bigger usually means a more complete assembly. |
| **log2 fold change** | How much a gene's expression changes: log2(treated / control). 1 = doubled, -1 = halved, 0 = no change. |
| **Pseudocount** | A small number (default 1) added before taking logs so that zero counts don't give `-Inf`. |
| **z-score** | (value - mean) / standard deviation: how many SDs a value is from the average. |
| **Multiple testing / BH / padj** | Testing thousands of genes at p < 0.05 gives many false positives by chance. The Benjamini-Hochberg (BH) adjustment turns p-values into `padj` values that control the false discovery rate (the expected share of false hits among the genes you call significant). |
| **Differential expression (DE)** | Finding genes whose expression differs between conditions, usually with DESeq2, limma or edgeR in R. |

## Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Use `python3` instead (macOS/Linux), or install Python 3.10+ from python.org. |
| `ERROR: Package 'rushtools' requires a different Python` | Your Python is older than 3.10. Check with `python --version`. |
| `rushtools: command not found` | The virtual environment is not active: run `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`) from the `rushtools` folder, then try again. |
| `No such file or directory: 'examples/genes.fasta'` | Run the command from the top `rushtools` folder (the one with `examples/` in it), or give the full path to the file. |
| `ValueError: sequence has no A/C/G/T bases` | `gc_content()` was given a sequence of only `N`s (or an empty one). Skip it with `try`/`except`, as in the example above; the `rushtools gc` command prints `NA` instead. |
| `error: sequence before the first '>' header` | The file is not FASTA. If its first line starts with `@`, it is FASTQ: use `read_fastq()`. |
| `ModuleNotFoundError: No module named 'rushtools'` when running `pytest` | Make sure the virtual environment is active and you ran `pip install -e "./python[dev]"`. |
| R: `there is no package called 'remotes'` | Run `install.packages("remotes")` first, or install from the clone with `install.packages("r", repos = NULL, type = "source")`. |
| R: `invalid package 'r'` / `no packages specified` | Start R from the top `rushtools` folder (or `setwd("path/to/rushtools")`), not from inside `r/`. |
| R: `Non-DNA characters found in sequence(s) 1` | The sequence contains something other than A/C/G/T/N/IUPAC codes, e.g. `U` (RNA) or a space. |

## Citing, licence and contributing

- If rushtools helps your work, please cite it: GitHub shows a "Cite this repository" button generated from [`CITATION.cff`](CITATION.cff).
- MIT licence ([`python/LICENSE`](python/LICENSE), [`r/LICENSE.md`](r/LICENSE.md)).
- What changed between versions: [`python/CHANGELOG.md`](python/CHANGELOG.md) and [`r/NEWS.md`](r/NEWS.md).
- Bug reports and suggestions are welcome; see [`CONTRIBUTING.md`](CONTRIBUTING.md).
