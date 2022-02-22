library(tidyverse)
library(extrafont) # font embedding
rm(list=ls())
setwd("~/projects/morph-order/")

# data
dfdata <- read.csv("threefeatdata.csv", sep = '\t')
df <- data.frame(dfdata)

f_df <- df %>% filter(!grepl("Tense.*Aspect|Aspect.*Tense|Mood.*Aspect|Aspect.*Mood|Mood.*Tense|Tense.*Mood", FeatureCombination))
f_df <- f_df %>% filter(!grepl("Person.*Number|Number.*Person|Number.*Gender|Gender.*Number|Person.*Gender|Gender.*Person", FeatureCombination))

f_df$cat <- 'A'

stats <- f_df %>% group_by(cat) %>% summarize(Mean = mean(NormalizedSD), SD = sd(NormalizedSD),
                                            CI_L = Mean - (SD * 1.96)/sqrt(51),
                                            CI_U = Mean + (SD * 1.96)/sqrt(51))

f_df %>%
  ggplot(aes(x=cat, y=NormalizedSD)) +
  geom_violin() +
  # geom_text(aes(label=FeatureCombination)) +
  theme_minimal() +
  labs(x="", y="Normalized Standard Deviation", fill="") +
  theme(legend.position="none", axis.text.x=element_blank(), panel.grid.major.x = element_blank()) +
  # geom_hline(yintercept=0, color="black") +
  geom_point(aes(x=cat, y=median(NormalizedSD)), color = "black", shape=1, size = 3) +
  geom_point(aes(x=cat, y=mean(NormalizedSD)), color = "black", shape=18, size = 3) +
  geom_point(aes(x=cat, y=0.1891909), color="#00BFC4", size = 3) +
  geom_point(aes(x=cat, y=0.2548624), color="#F8766D", size = 3) +
  annotate("text", x='A', y=0.2548624, label = "PNG") +
  annotate("text", x='A', y=0.1891909, label = "TAM") +
  geom_errorbar(mapping = aes(x = cat, ymin = 0.292, ymax = 0.319), width = 0.1) +
  ylim(0.175,0.4125)

ggsave("result_plots/polyexponence.pdf", width=5.25, height=4.5, units = "in", dpi = 300)
embed_fonts("result_plots/polyexponence.pdf")
