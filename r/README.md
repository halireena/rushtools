# rushtools

Small, tested helper functions for everyday plant bioinformatics in R.

## Installation

```r
# install.packages("remotes")
remotes::install_github("yourGitHubName/rushtools")
```

## Functions

| Function | What it does |
|---|---|
| `gc_content()` | GC fraction of DNA sequences |
| `reverse_complement()` | reverse complement of DNA sequences |
| `log2_fold_change()` | log2 fold change between two groups (raw or log2 input) |
| `z_score()` | z-score standardisation |
| `adjust_p()` | multiple-testing correction (BH by default) with input checks |
| `tidy_de_table()` | standardise DESeq2 / limma / edgeR result tables |
| `count_motif()` | count motif occurrences in DNA sequences |

## Example

```r
library(rushtools)
gc_content(c("ATGC", "GGCC"))
reverse_complement("ATGCCC")
```
