# Contributing

This is a small personal project, but bug reports, questions and
suggestions are very welcome: please open an issue on GitHub with the
command or code you ran, what you expected and what happened (a few lines
of an example file help a lot).

If you'd like to send a fix:

1. Fork and clone the repository, then make a branch.
2. Python: `cd python && pip install -e ".[dev]"`, then make sure
   `pytest` and `ruff check .` both pass.
3. R: from `r/`, run `Rscript -e 'testthat::test_local(".")'`. If you
   change a roxygen comment (`#'`), regenerate the help pages with
   `Rscript -e 'roxygen2::roxygenise()'`.
4. Add a test for any bug you fix, and a line to `python/CHANGELOG.md` or
   `r/NEWS.md`.
5. Keep the two packages in step where a function exists in both
   (e.g. `gc_content()` and `reverse_complement()`).

The example files in `examples/` are used by the READMEs; if you change
them, update the outputs shown there.
