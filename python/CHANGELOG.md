# Changelog (Python package)

## Unreleased

- `rushtools gc --digits` with a negative number now gives a clear error;
  it used to print `NA` for every record.
- `rushtools revcomp` now refuses input that is not DNA (e.g. `HELLO`)
  instead of printing nonsense. The `reverse_complement()` function itself
  is unchanged.
- `pytest` works from `python/` even before `pip install -e .`.

## 0.2.0

- `read_fasta()` / `read_fastq()`: a bare `>` or `@` header is a clear
  `ValueError` instead of an `IndexError`; FASTQ blank lines between
  records are tolerated.
- `rushtools gc` prints `NA` for records with no A/C/G/T bases and carries
  on with the rest of the file.
- `rushtools stats` on an empty file says "no sequences found".
- `gc_content(ignore_n=True)` leaves every non-ACGT symbol out of the
  denominator, matching the R package (it used to drop only `N`).
- `kmer_count()` is case-insensitive and skips k-mers with ambiguous bases
  (`skip_ambiguous=False` for the old behaviour).
- `__version__` comes from the package metadata; ships `py.typed`.

## 0.1.0

- First version: `gc_content()`, `reverse_complement()`, `translate()`,
  `find_orfs()`, `kmer_count()`, `hamming()`, `n50()`, FASTA/FASTQ readers,
  `write_fasta()` and the `rushtools` command (`gc`, `stats`, `revcomp`,
  `orfs`).
