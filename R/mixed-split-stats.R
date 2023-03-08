source("R/helper/read_data.R")

## read and clean the data
tbl <- read_split_stats("soc-brightkite")
tbl$graph <- factor(tbl$graph, labels = c("Base graph", "Overlay graph"))

library("ggplot2")
ggplot(tbl, aes(x = ratio, y = components, color = graph)) +
    geom_line() +
    geom_point() +
    labs(x = "", y = "Connected components") +
    theme(legend.title = element_blank(), legend.position = c(0.8, 0.4))
ggsave("output/plots/mixed-split-components.pdf", width = 7, height = 3)
ggplot(tbl, aes(x = ratio, y = gcc, color = graph)) +
    geom_line() +
    geom_point() +
    labs(x = "Ratio of overlay edges", y = "GCC") +
    theme(legend.position = "none")
ggsave("output/plots/mixed-split-gcc.pdf", width = 7, height = 3)

ggplot(tbl, aes(x = ratio, y = avg_val, color = graph)) +
    geom_line() +
    geom_point() +
    labs(x = "Ratio of overlay edges", y = "Average CN value") +
    theme(legend.position = "none")
ggsave("output/plots/mixed-split-cn-val.pdf", width = 7, height = 3)
