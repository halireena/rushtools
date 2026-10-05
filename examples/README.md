# Example data

Tiny, **made-up** files so every example in the READMEs runs as written.
They are not real plant sequences.

| File | What it is |
|---|---|
| `genes.fasta` | 4 DNA sequences in FASTA format: one with a 108-nt open reading frame (`geneA`), a GC-rich one, an AT-rich one with some `N`s, and one that is only `N`. |
| `reads.fastq` | 3 sequencing reads in FASTQ format, with good, falling and poor quality scores. |

Run the examples from the top folder of the repository, e.g.

```bash
rushtools stats examples/genes.fasta
```
