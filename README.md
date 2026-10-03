# rushtools

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
import rushtools
```

## Run the tests locally

R (from the `r/` folder):

```r
devtools::test()
```

Python (from the `python/` folder):

```bash
pip install -e . pytest
pytest
```
