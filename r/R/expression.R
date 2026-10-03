#' log2 fold change between two groups
#'
#' @param treated,control Numeric vectors of measurements for each group.
#' @param pseudocount Number added to each mean before taking logs (only used
#'   when `is_log2 = FALSE`). Default 1.
#' @param is_log2 Logical. Are the values already log2-transformed? Default `FALSE`.
#' @param na.rm Logical. Remove `NA` before averaging? Default `TRUE`.
#' @return A single number: log2(treated / control).
#' @examples
#' log2_fold_change(c(400, 420, 380), c(50, 55, 45))
#' log2_fold_change(c(8.6, 8.7), c(5.6, 5.8), is_log2 = TRUE)
#' @export
log2_fold_change <- function(treated, control, pseudocount = 1,
                             is_log2 = FALSE, na.rm = TRUE) {
  stopifnot(is.numeric(treated), is.numeric(control),
            length(pseudocount) == 1, pseudocount >= 0)
  m_t <- mean(treated, na.rm = na.rm)
  m_c <- mean(control, na.rm = na.rm)
  if (is_log2) {
    return(m_t - m_c)
  }
  if (any(c(treated, control) < 0, na.rm = TRUE)) {
    stop("Raw values must be non-negative; did you mean is_log2 = TRUE?", call. = FALSE)
  }
  log2(m_t + pseudocount) - log2(m_c + pseudocount)
}

#' Z-score standardisation
#'
#' Centres a vector on its mean and divides by its standard deviation.
#'
#' @param x Numeric vector.
#' @param na.rm Logical. Ignore `NA` when computing mean and SD? Default `TRUE`.
#' @return Numeric vector of z-scores, the same length as `x`. If `x` has zero
#'   variance, zeros are returned with a warning.
#' @seealso [base::scale()] for matrices.
#' @examples
#' z_score(c(2, 4, 6, 8))
#' @export
z_score <- function(x, na.rm = TRUE) {
  stopifnot(is.numeric(x))
  s <- stats::sd(x, na.rm = na.rm)
  if (is.na(s) || s == 0) {
    warning("x has zero (or undefined) variance; returning 0s", call. = FALSE)
    return(ifelse(is.na(x), NA_real_, 0))
  }
  (x - mean(x, na.rm = na.rm)) / s
}
