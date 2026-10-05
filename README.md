# rushtools

[![Python tests](https://github.com/halireena/rushtools/actions/workflows/python-tests.yml/badge.svg)](https://github.com/halireena/rushtools/actions/workflows/python-tests.yml)
[![R CMD check](https://github.com/halireena/rushtools/actions/workflows/r-tests.yml/badge.svg)](https://github.com/halireena/rushtools/actions/workflows/r-tests.yml)

My personal function libraries, in two languages:

| Folder      | What it is                                   |
|-------------|----------------------------------------------|
| `r/`        | R package `rushtools` (`R/`, `tests/`, `DESCRIPTION`) |
| `python/`   | Python package `rushtools` (`src/` layout, `pyproject.toml`, `tests/`) |

Tests for both run automatically on every push (see the Actions tab).

## Install the R package

```r
# install.packages("remotes")
remotes::install_github("halireena/rushtools", subdir = "r")
library(rushtools)
```

## Install the Python package

```bash
pip install "git+https://github.com/halireena/rushtools#subdirectory=python"
```

```python
from rushtools import gc_content, read_fasta

for rid, seq in read_fasta("genes.fasta"):
    print(rid, round(gc_content(seq), 3))
```

It also installs a `rushtools` command:

```bash
rushtools stats genes.fasta     # sequence count, total bp, longest, N50
rushtools gc genes.fasta        # GC content per sequence (NA for all-N records)
rushtools orfs genes.fasta --min-len 90
```

R usage:

```r
gc_content(c(a = "ATGC", b = "GGCC"))
reverse_complement("ATGCRY")
tidy_de_table(res, lfc_col = "logFC", p_col = "P.Value")
```

## Run the tests locally

R (from the `r/` folder):

```r
devtools::test()
```

Python (from the `python/` folder):

```bash
pip install -e ".[dev]"
pytest          # unit tests + docstring examples
ruff check .    # lint
```
