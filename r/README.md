# rushtools

Small, tested helper functions for everyday plant bioinformatics in R.
Needs R 4.0 or newer; no dependencies beyond base R.

## Installation

From GitHub:

```r
install.packages("remotes")   # once
remotes::install_github("halireena/rushtools", subdir = "r")
```

Or from a clone of the repository, with R started in the top `rushtools` folder:

```r
install.packages("r", repos = NULL, type = "source")
```

## Functions

| Function | What it does |
|---|---|
| `gc_content()` | GC fraction of DNA sequences (`NA` if a sequence has no A/C/G/T) |
| `reverse_complement()` | reverse complement of DNA sequences, IUPAC codes allowed |
| `count_motif()` | count motif occurrences in DNA sequences (e.g. a restriction site) |
| `log2_fold_change()` | log2 fold change between two groups (raw or log2 input) |
| `z_score()` | z-score standardisation |
| `adjust_p()` | multiple-testing correction (BH by default) with input checks |
| `tidy_de_table()` | standardise DESeq2 / limma / edgeR result tables |

Each has a help page with examples, e.g. `?count_motif`. Unfamiliar terms
(BH, IUPAC, fold change...) are explained in the
[glossary](../README.md#glossary).

## Example

```r
library(rushtools)

gc_content(c("ATGC", "GGCC"))
#> [1] 0.5 1.0

reverse_complement("ATGCCC")
#> [1] "GGGCAT"

count_motif(c(s1 = "GAATTCGAATTC", s2 = "ATGC"), "GAATTC")   # EcoRI site
#> s1 s2
#>  2  0

log2_fold_change(c(400, 420, 380), c(50, 55, 45))   # about 8x higher
#> [1] 2.975033

z_score(c(2, 4, 6, 8))
#> [1] -1.1618950 -0.3872983  0.3872983  1.1618950

adjust_p(c(a = 0.01, b = 0.02, c = 0.03, d = 0.5))
#>    a    b    c    d
#> 0.04 0.04 0.04 0.50

res <- data.frame(gene = c("g1", "g2", "g3"), logFC = c(2.1, -1.5, 0.2),
                  P.Value = c(0.0001, 0.003, 0.7))
tidy_de_table(res, lfc_col = "logFC", p_col = "P.Value")
#>   gene log2fc pvalue   padj direction
#> 1   g1    2.1  1e-04 0.0003        up
#> 2   g2   -1.5  3e-03 0.0045      down
#> 3   g3    0.2  7e-01 0.7000        ns
```

For a DESeq2 result the default column names already match. DESeq2 keeps
gene IDs in the row names, which `tidy_de_table()` resets, so move them into
a column first:

```r
de <- as.data.frame(DESeq2::results(dds))
tidy_de_table(cbind(gene = rownames(de), de), padj_col = "padj")
```

## Tests

From the top `rushtools` folder (needs `install.packages("testthat")` once):

```bash
cd r
Rscript -e 'testthat::test_local(".")'
```

Changes between versions: [NEWS.md](NEWS.md).
