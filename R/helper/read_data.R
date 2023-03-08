library(reshape2)
library(plyr)
library(dplyr)

read_noisy_information <- function() {
  read.csv("output/noise_attributes.csv")
}

read_classification <- function() {
  read.csv("output/classification/results.csv")
}

read_auc <- function() {
  read.csv("output/auc/results.csv")
}

read_split_stats <- function(graph) {
  read.csv(sprintf("output/real_world_split_stats/%s.csv", graph))
}

join_by_noisy_graph <- function(...) {
  plyr::join_all(list(...), by = "noisy_graph")
}

read_graph_stats <- function(graph) {
  read.csv(sprintf("output/graph_stats/%s.csv", graph))
}