#' GC content of DNA sequences
#'
#' Computes the fraction of G and C bases in each sequence.
#'
#' @param seqs Character vector of DNA sequences (case-insensitive).
#' @param ignore_n Logical. If `TRUE` (default), N and any other non-ACGT
#'   characters are left out of the denominator.
#' @return Numeric vector of GC fractions between 0 and 1, named like `seqs`.
#'   Sequences with no valid bases return `NA`.
#' @examples
#' gc_content(c("ATGC", "GGCC", "ATAT"))
#' gc_content("GCNNNN", ignore_n = FALSE)
#' @export
gc_content <- function(seqs, ignore_n = TRUE) {
  stopifnot("`seqs` must be character" = is.character(seqs))
  seqs <- toupper(seqs)
  n_gc <- nchar(gsub("[^GC]", "", seqs))
  n_total <- if (ignore_n) nchar(gsub("[^ACGT]", "", seqs)) else nchar(seqs)
  out <- n_gc / n_total
  out[n_total == 0] <- NA
  names(out) <- names(seqs)
  out
}

#' Reverse complement of DNA sequences
#'
#' @param seqs Character vector of DNA sequences containing only A, C, G, T
#'   or N (any case).
#' @return Character vector of upper-case reverse complements, named like `seqs`.
#' @examples
#' reverse_complement("ATGCCC")
#' reverse_complement(c(fwd = "GGATCCNA"))
#' @export
reverse_complement <- function(seqs) {
  stopifnot("`seqs` must be character" = is.character(seqs))
  seqs <- toupper(seqs)
  bad <- grepl("[^ACGTN]", seqs)
  if (any(bad)) {
    stop("Non-DNA characters found in sequence(s) ",
         paste(which(bad), collapse = ", "), call. = FALSE)
  }
  comp <- chartr("ACGTN", "TGCAN", seqs)
  out <- vapply(strsplit(comp, ""), function(b) paste(rev(b), collapse = ""),
                FUN.VALUE = character(1))
  names(out) <- names(seqs)
  out
}

#' Count occurrences of a motif in DNA sequences
#'
#' Counts non-overlapping, case-insensitive exact matches.
#'
#' @param seqs Character vector of DNA sequences.
#' @param motif A single motif, e.g. "GAATTC" (treated as fixed text, not a regex).
#' @return Integer vector of counts, named like `seqs`.
#' @examples
#' count_motif(c("GAATTCGAATTC", "ATGC"), "GAATTC")
#' @export
count_motif <- function(seqs, motif) {
  stopifnot(is.character(seqs), is.character(motif), length(motif) == 1)
  hits <- gregexpr(toupper(motif), toupper(seqs), fixed = TRUE)
  out <- vapply(hits, function(h) sum(h > 0), FUN.VALUE = integer(1))
  names(out) <- names(seqs)
  out
}
