library(tidyverse)
rm(list=ls())
setwd("~/projects/morph-order/result_plots/")

# data
df <- data.frame(
  y = c(2,15,9,13,4,9),
  x = c(rep("Case-Number" , 2) , rep("Tense-Number" , 2) , rep("Aspect-Number" , 2) ),
  cat = factor(rep(c("Suppletive Feature Further", "Suppletive Feature Closer") , 3), levels = c("Suppletive Feature Further", "Suppletive Feature Closer")))

# Grouped
ggplot(df, aes(fill=cat, y=y, x=x)) + 
  geom_bar(position="stack", stat="identity")

df %>%
  ggplot(aes(fill=cat, y=y, x=x)) +
  geom_bar(position="dodge", stat="identity") +
  theme_minimal() +
  xlab('Features') +
  ylab('Frequency') +
  theme(legend.position="top") +
  theme(legend.title = element_blank())

ggsave('suppletion.pdf', width = 6, height = 7.5, units = 'in')
