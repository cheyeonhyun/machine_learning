#!/bin/Rscript
args <- commandArgs(TRUE)
data <- args[1]
directed <- as.logical(args[2])
d <- args[3]
in_d <- args[4]
out_d <- args[5]
between <- args[6]
closeness <- args[7]
eig <- args[8]
fc <- args[9]
wc<- args[10]
clique <- args[11]

source("igraph_inr2.r")

writetable(data, directed, d, in_d, out_d, between, closeness, eig, fc, wc, clique)
