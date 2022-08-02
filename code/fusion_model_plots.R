library(tidyverse)
library(extrafont) # font embedding
rm(list=ls())
setwd("~/projects/morph/")

dfdata <- read.csv("cat_cluster.csv", sep = ',')
df <- data.frame(dfdata)

df %>%
  ggplot() +
  geom_line(aes(x=L1Mem, y=L1Surp), color = '#F8766D', size = 1.5) +
  geom_line(aes(x=L2Mem, y=L2Surp), color = '#00BFC4', size = 1.5) +
  # geom_text(aes(label=FeatureCombination)) +
  theme_minimal() +
  labs(x="Memory", y="Surprisal", fill="") +
  theme(legend.position="top", panel.grid.major.x = element_blank())

ggsave("../morph-order/result_plots/cat_cluster.pdf", width=4, height=4, units = "in", dpi = 300)