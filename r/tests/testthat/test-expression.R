test_that("log2_fold_change works on raw and log2 values", {
  expect_equal(log2_fold_change(8, 2, pseudocount = 0), 2)
  expect_equal(log2_fold_change(c(8.6, 8.4), c(5.5, 5.5), is_log2 = TRUE), 3)
  expect_equal(log2_fold_change(0, 0), 0)
})

test_that("log2_fold_change refuses negative raw values", {
  expect_error(log2_fold_change(c(-1, 2), c(1, 2)), "is_log2")
})

test_that("z_score has mean 0 and sd 1", {
  z <- z_score(c(2, 4, 6, 8, 10))
  expect_equal(mean(z), 0)
  expect_equal(sd(z), 1)
  expect_length(z, 5)
})

test_that("z_score warns on constant input", {
  expect_warning(z <- z_score(c(3, 3, 3)), "zero")
  expect_equal(z, c(0, 0, 0))
})
