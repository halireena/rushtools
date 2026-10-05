# rushtools (development version)

* `reverse_complement()` now accepts IUPAC ambiguity codes (R, Y, S, W, K,
  M, B, D, H, V), matching the Python package.
* `count_motif()` now errors on an empty motif instead of returning a
  meaningless count.
* `reverse_complement()` keeps `NA` as `NA`; it used to return the text
  `"NA"`.

# rushtools 0.2.0

* New `count_motif()` counts motif occurrences in DNA sequences.

# rushtools 0.1.0

* First version: `gc_content()`, `reverse_complement()`, `log2_fold_change()`,
  `z_score()`, `adjust_p()` and `tidy_de_table()`, with tests.
