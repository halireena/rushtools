test_that("gc_content handles simple, mixed-case and empty sequences", {
  expect_equal(gc_content("GGCC"), 1)
  expect_equal(gc_content("atat"), 0)
  expect_equal(gc_content("ATGC"), 0.5)
  expect_true(is.na(gc_content("")))
})

test_that("gc_content treats N according to ignore_n", {
  expect_equal(gc_content("GCNN"), 1)
  expect_equal(gc_content("GCNN", ignore_n = FALSE), 0.5)
})

test_that("gc_content keeps names and rejects non-character input", {
  expect_named(gc_content(c(a = "GC", b = "AT")), c("a", "b"))
  expect_error(gc_content(123), "must be character")
})

test_that("reverse_complement is correct and reversible", {
  expect_equal(reverse_complement("AACG"), "CGTT")
  expect_equal(reverse_complement("atgn"), "NCAT")
  s <- "ATGCGTTAGC"
  expect_equal(reverse_complement(reverse_complement(s)), s)
})

test_that("reverse_complement rejects RNA and other letters", {
  expect_error(reverse_complement("AUGC"), "Non-DNA")
})
