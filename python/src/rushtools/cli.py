"""Command-line interface: `rushtools <command> ...`."""
from __future__ import annotations

import argparse
import sys

from rushtools import __version__
from rushtools.assembly import n50
from rushtools.parsers import read_fasta
from rushtools.seq import find_orfs, gc_content, reverse_complement


def _cmd_gc(args: argparse.Namespace) -> None:
    print("id\tlength\tgc")
    for rid, seq in read_fasta(args.fasta):
        print(f"{rid}\t{len(seq)}\t{gc_content(seq):.{args.digits}f}")


def _cmd_stats(args: argparse.Namespace) -> None:
    lengths = [len(seq) for _, seq in read_fasta(args.fasta)]
    print(f"sequences\t{len(lengths)}")
    print(f"total_bp\t{sum(lengths)}")
    print(f"longest\t{max(lengths)}")
    print(f"n50\t{n50(lengths)}")


def _cmd_revcomp(args: argparse.Namespace) -> None:
    print(reverse_complement(args.sequence))


def _cmd_orfs(args: argparse.Namespace) -> None:
    print("id\tstrand\tstart\tend\tlength_nt\tprotein_aa")
    for rid, seq in read_fasta(args.fasta):
        for o in find_orfs(seq, min_len=args.min_len):
            print(f"{rid}\t{o['strand']}\t{o['start']}\t{o['end']}\t{o['length']}\t{len(o['protein'])}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rushtools", description="Small plant-bioinformatics helpers.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    p = sub.add_parser("gc", help="GC content of every sequence in a FASTA file")
    p.add_argument("fasta", help="input FASTA (plain or .gz)")
    p.add_argument("-d", "--digits", type=int, default=3, help="decimal places (default: 3)")
    p.set_defaults(func=_cmd_gc)

    p = sub.add_parser("stats", help="number of sequences, total length, N50")
    p.add_argument("fasta", help="input FASTA (plain or .gz)")
    p.set_defaults(func=_cmd_stats)

    p = sub.add_parser("revcomp", help="reverse complement of a sequence typed on the command line")
    p.add_argument("sequence", help="DNA sequence")
    p.set_defaults(func=_cmd_revcomp)

    p = sub.add_parser("orfs", help="ATG-to-stop ORFs in all six frames")
    p.add_argument("fasta", help="input FASTA (plain or .gz)")
    p.add_argument("--min-len", type=int, default=90, help="minimum ORF length in nt (default: 90)")
    p.set_defaults(func=_cmd_orfs)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point used by the `rushtools` command (see [project.scripts] in pyproject.toml)."""
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except (FileNotFoundError, ValueError) as err:
        print(f"rushtools: error: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
