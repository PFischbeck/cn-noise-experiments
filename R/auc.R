source("R/helper/read_data.R")

## read and clean the data
tbl <- join_by_noisy_graph(
  read_noisy_information(),
  read_auc()
)

tbl <- tbl[tbl$feature == "common_neighbors", ]

tbl$graph <- gsub("_seed=[0-9]+$", "", tbl$graph)
tbl$graph <- gsub("^rgg", "a_rgg", tbl$graph)
tbl$graph <- gsub("^hrg", "b_hrg", tbl$graph)

tbl_rgg <- tbl[grep("^a_rgg", tbl$graph), ]
tbl_rgg$graph <- factor(tbl_rgg$graph, labels = c("RGG with k=10", "RGG with k=25", "RGG with k=50"))
tbl_hrg <- tbl[grep("^b_hrg", tbl$graph), ]
tbl_hrg$graph <- factor(tbl_hrg$graph, labels = c("HRG with beta=2.2", "HRG with beta=2.6", "HRG with beta=2.9"))


# tbl <- rbind(tbl_rgg, tbl_hrg)

library("ggplot2")
ggplot(tbl_rgg, aes(x = additional_edges, y = auc_score, group = additional_edges)) +
  geom_boxplot() +
  facet_grid(cols = vars(graph)) +
  labs(x = element_blank(), y = "AUC value")
ggsave("output/plots/auc-rgg.pdf", width = 10, height = 2)
ggplot(tbl_hrg, aes(x = additional_edges, y = auc_score, group = additional_edges)) +
  geom_boxplot() +
  facet_grid(cols = vars(graph)) +
  labs(x = "Overlay edge factor", y = "AUC value")
ggsave("output/plots/auc-hrg.pdf", width = 10, height = 2)
