source("R/helper/read_data.R")

## read and clean the data
tbl_10 <- read_graph_stats("rgg_n=5000_k=10_seed=0_additionaledges=5")
tbl_10$graph <- "RGG with k=10"
tbl_25 <- read_graph_stats("rgg_n=5000_k=25_seed=0_additionaledges=5")
tbl_25$graph <- "RGG with k=25"
tbl_50 <- read_graph_stats("rgg_n=5000_k=50_seed=0_additionaledges=5")
tbl_50$graph <- "RGG with k=50"

tbl <- rbind(tbl_10, tbl_25, tbl_50)
tbl$is_random <- factor(tbl$is_random, labels = c("Base edges", "Overlay edges"))

library("ggplot2")
ggplot(tbl, aes(x = common_neighbors, fill = is_random)) +
    geom_histogram(position = "dodge", binwidth = 1) +
    facet_grid(cols = vars(graph)) +
    labs(x = "Common neighbors score", y = "Number of edges") +
    theme(legend.title = element_blank(), legend.position = c(0.2, 0.8))
ggsave("output/plots/score-distribution.pdf", width = 10, height = 3)
