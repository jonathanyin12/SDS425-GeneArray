# GeneArray Example
#
# This is a small subset of a much larger problem.
#
# Files in SlideFiles/ have been pre-processed by JE to maintain
# confidentiality, but the substance of the problem is intact.
#
# 33 files, with 11 sets, each one in triplicate
# 320 genes on each array in the interior (16 * 20)
# 320 * 11 = 3520 total genes available for study
# 7 images taken within each well
#
files <- dir("SlideFiles/")

# Read one file and glance at it (file.path() is platform-independent):
x <- read.csv(file.path("SlideFiles", files[1]), as.is = TRUE)
dim(x)
head(x[,-c(1:130)], 22)

table(x$type)
table(x$slide)
table(x$row)
table(x$col)
table(x$well)

# Reading everything into R:
system.time({
  x <- NULL
  for (i in 1:length(files)) {
    cat("Reading", files[i], "\n")
    x[[i]] <- read.csv(file.path("SlideFiles", files[i]), as.is=TRUE)
  }
})

# For convenience, the first 130 columns are image characteristics:
ncols <- 130
imagecols <- 1:130

# "rf" - negative controls
# "gene" - core wells the slides, almost all of which should be similar to
#          negative controls

# 16 * 24 * 7 = 2688 rows per CSV file
# 320 * 11 = 3520 genes being explore in interior of the slides

y <- x[[1]]
y[1:7,]
pairs(y[y$type == "rf", 1:6])

