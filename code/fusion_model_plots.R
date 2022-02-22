library(tidyverse)
library(extrafont) # font embedding
rm(list=ls())
setwd("~/morph/")

dfdata <- read.csv("fusion_model.csv", sep = '\t')
df <- data.frame(dfdata)

df %>%
  ggplot() +
  geom_line(aes(x=L1Mem, y=L1Surp), color = '#F8766D') +
  geom_line(aes(x=L2Mem, y=L2Surp), color = '#00BFC4') +
  # geom_text(aes(label=FeatureCombination)) +
  theme_minimal() +
  theme(text = element_text(family = "Times New Roman")) +
  labs(x="Memory", y="Surprisal", fill="") +
  theme(legend.position="top", panel.grid.major.x = element_blank())

ggsave("../projects/morph-order/result_plots/fusion.pdf", width=4, height=4, units = "in", dpi = 300)
embed_fonts("result_plots/fusion.pdf")