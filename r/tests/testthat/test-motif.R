test_that("count_motif counts non-overlapping matches", {
  expect_equal(count_motif("GAATTCGAATTC", "GAATTC"), 2L)
  expect_equal(count_motif("ATGC", "GAATTC"), 0L)
  expect_equal(count_motif("gaattc", "GAATTC"), 1L)
  expect_equal(count_motif("AAAA", "AA"), 2L)
  expect_named(count_motif(c(x = "AA"), "A"), "x")
})
