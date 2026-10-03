test_that("adjust_p matches p.adjust and keeps names", {
  p <- c(a = 0.01, b = 0.04, c = 0.03, d = NA)
  expect_equal(unname(adjust_p(p)), p.adjust(unname(p), method = "BH"))
  expect_named(adjust_p(p), names(p))
  expect_error(adjust_p(c(0.1, 1.5)), "between 0 and 1")
  expect_error(adjust_p(0.1, method = "nonsense"))
})

test_that("tidy_de_table standardises limma-style output", {
  res <- data.frame(gene = c("g1", "g2", "g3"), logFC = c(2.1, -1.5, 0.2),
                    P.Value = c(0.0001, 0.003, 0.7))
  out <- tidy_de_table(res, lfc_col = "logFC", p_col = "P.Value")
  expect_s3_class(out, "data.frame")
  expect_true(all(c("log2fc", "pvalue", "padj", "direction") %in% names(out)))
  expect_false(any(c("logFC", "P.Value") %in% names(out)))
  expect_equal(out$direction, c("up", "down", "ns"))
  expect_equal(out$padj, sort(out$padj))
})

test_that("tidy_de_table gives a helpful error for wrong column names", {
  expect_error(tidy_de_table(data.frame(a = 1)), "not found")
})
