# rushtools

Small, tested Python helpers for everyday plant bioinformatics, built while learning Python.

## Install

```bash
pip install git+https://github.com/USER/rushtools.git          # latest version
pip install git+https://github.com/USER/rushtools.git@v0.1.0   # a specific tagged version
```

For development (editable install + tests):

```bash
git clone https://github.com/USER/rushtools.git
cd rushtools
pip install -e ".[dev]"
pytest
```

## Use in Python

```python
from rushtools import gc_content, reverse_complement, translate, read_fasta, n50

gc_content("ATGCGC")            # 0.6667
reverse_complement("ATGC")      # 'GCAT'
translate("ATGTGGTAA")          # 'MW*'
for rid, seq in read_fasta("genes.fasta"):
    print(rid, len(seq))
```

## Use on the command line

```bash
rushtools --help
rushtools gc genes.fasta
rushtools stats genes.fasta
rushtools revcomp ATGCCC
rushtools orfs genes.fasta --min-len 90
```

## Licence

MIT
