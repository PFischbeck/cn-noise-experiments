source("R/helper/read_data.R")

## read and clean the data
tbl <- join_by_noisy_graph(
  read_noisy_information(),
  read_auc()
)

tbl <- tbl[tbl$feature == "common_neighbors", ]

tbl$graph <- gsub("_seed=[0-9]+$", "", tbl$graph)

tbl_real <- tbl[grep("^(rgg|hrg)", tbl$graph, invert=TRUE), ]

library("ggplot2")
ggplot(tbl_real, aes(x=additional_edges, y=auc_score, group=additional_edges)) + geom_boxplot() + facet_wrap(~graph) + labs(x="Overlay edge factor", y="AUC value")
ggsave("output/plots/auc-real.pdf", width=10, height=4)