test_that("count_motif counts non-overlapping matches", {
  expect_equal(count_motif("GAATTCGAATTC", "GAATTC"), 2L)
  expect_equal(count_motif("ATGC", "GAATTC"), 0L)
  expect_equal(count_motif("gaattc", "GAATTC"), 1L)
  expect_equal(count_motif("AAAA", "AA"), 2L)
  expect_named(count_motif(c(x = "AA"), "A"), "x")
})

test_that("count_motif rejects an empty motif", {
  expect_error(count_motif("ACGT", ""), "non-empty")
  expect_error(count_motif("ACGT", NA_character_), "non-empty")
})
