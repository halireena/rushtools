#' Adjust p-values for multiple testing
#'
#' A wrapper around [stats::p.adjust()] that defaults to Benjamini-Hochberg,
#' checks the input range and keeps names.
#'
#' @param p Numeric vector of p-values (`NA` allowed).
#' @param method One of [stats::p.adjust.methods]. Default `"BH"`.
#' @return Numeric vector of adjusted p-values, named like `p`.
#' @examples
#' adjust_p(c(a = 0.01, b = 0.02, c = 0.03, d = 0.5))
#' @export
adjust_p <- function(p, method = "BH") {
  stopifnot(is.numeric(p))
  method <- match.arg(method, stats::p.adjust.methods)
  if (any(p < 0 | p > 1, na.rm = TRUE)) {
    stop("p-values must be between 0 and 1", call. = FALSE)
  }
  out <- stats::p.adjust(p, method = method)
  names(out) <- names(p)
  out
}

#' Standardise a differential expression table
#'
#' Renames the fold-change and p-value columns of any DE result (DESeq2,
#' limma, edgeR, ...) to `log2fc`, `pvalue` and `padj`, computes `padj` if
#' needed, adds a `direction` column and sorts by `padj`.
#'
#' @param de A data frame of DE results.
#' @param lfc_col Name of the log2 fold-change column. Default `"log2FoldChange"`.
#' @param p_col Name of the raw p-value column. Default `"pvalue"`.
#' @param padj_col Name of the adjusted p-value column, or `NULL` (default)
#'   to compute BH-adjusted values from `p_col`.
#' @param padj_cutoff Significance threshold for `padj`. Default 0.05.
#' @param lfc_cutoff Minimum absolute log2 fold change. Default 1.
#' @return A data frame with `log2fc`, `pvalue`, `padj` and `direction`
#'   (`"up"`, `"down"` or `"ns"`), sorted by `padj`.
#' @examples
#' res <- data.frame(gene = c("g1", "g2", "g3"), logFC = c(2.1, -1.5, 0.2),
#'                   P.Value = c(0.0001, 0.003, 0.7))
#' tidy_de_table(res, lfc_col = "logFC", p_col = "P.Value")
#' @export
tidy_de_table <- function(de, lfc_col = "log2FoldChange", p_col = "pvalue",
                          padj_col = NULL, padj_cutoff = 0.05, lfc_cutoff = 1) {
  stopifnot(is.data.frame(de))
  needed <- c(lfc_col, p_col, padj_col)
  missing_cols <- setdiff(needed, names(de))
  if (length(missing_cols) > 0) {
    stop("Column(s) not found: ", paste(missing_cols, collapse = ", "),
         "\nAvailable: ", paste(names(de), collapse = ", "), call. = FALSE)
  }
  out <- de
  out$log2fc <- de[[lfc_col]]
  out$pvalue <- de[[p_col]]
  out$padj <- if (is.null(padj_col)) adjust_p(de[[p_col]]) else de[[padj_col]]
  sig <- !is.na(out$padj) & out$padj < padj_cutoff & abs(out$log2fc) >= lfc_cutoff
  out$direction <- ifelse(sig & out$log2fc > 0, "up",
                          ifelse(sig & out$log2fc < 0, "down", "ns"))
  old <- setdiff(c(lfc_col, p_col, padj_col), c("log2fc", "pvalue", "padj"))
  out <- out[, setdiff(names(out), old), drop = FALSE]
  out <- out[order(out$padj, na.last = TRUE), , drop = FALSE]
  rownames(out) <- NULL
  out
}
