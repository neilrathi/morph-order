library(tidyverse)
library(rPref)
rm(list=ls())
setwd("~/Desktop/src/combo/langs/")
lang = "ara"

# FINE GRAINED ANALYSIS
fine_optim <- read.csv(paste(lang, "/avg_rank_diff.csv", sep = ""), sep = '\t')
fusion <- read.csv(paste(lang, "/surprisals.txt", sep = ""), sep = '\t')

# rectangular sum
pareto_area = function(x, y) {
  area = 0
  for (i in 1:length(x)) {
    if (i == 1) {
      area <- x[i]*y[i]
    }
    else {
      area <- area + min(y[i], y[i-1])*(x[i]-x[i-1])
    }
  }
  return(area)
}

# permutation test w/ area under pareto curve
permutation_test = function(df, x, y, num_iter = 10000) {
  # skyline preferences
  p <- high(x) * high(y)
  res <- psel(df, p, top = nrow(df))
  # skyline
  res1 <- res %>% filter(.level == "1")
  res1 <- res1[order(res1$meansurp),]
  # empirical AUC
  standard = with(res1, pareto_area(meansurp, rank))
  results = c()
  for(i in 1:num_iter) {
    # shuffle data
    y_shuffled = sample(y)
    df_shuffled <- data.frame(x, y_shuffled)
    # create skyline as above
    p <- high(x) * high(y_shuffled)
    res <- psel(df_shuffled, p, top = nrow(df_shuffled))
    res1 <- res %>% filter(.level == "1")
    res1 <- res1[order(res1$x),]
    # shuffled AUC
    result = with(res1, pareto_area(x, y_shuffled))
    results = c(results, result)
  }
  # estimated p-value
  mean(results <= standard)
}

# create df
# colnames(optim) <- c('feats', 'rank')
# colnames(fusion) <- c('feats', 'meansurp', 'medsurp', 'sdsurp')
# fine_optim <- merge(optim, fusion)

# permutation test on empirical data
# with(fine_optim, permutation_test(fine_optim, meansurp, rank))

# for tradeoff plot
p <- high(fine_optim$meansurp) * high(fine_optim$rank)
res <- psel(fine_optim, p, top = nrow(fine_optim))
res1 <- res %>% filter(.level == "1")
res1 <- res1 %>% add_row(meansurp = 0, rank = max(fine_optim$rank))
res1 <- res1 %>% add_row(meansurp = max(fine_optim$meansurp), rank = 0)
res1 <- res1[order(res1$meansurp),]

res %>%
  ggplot(aes(x = meansurp, y = rank)) + 
  geom_point(data = res) + 
  #geom_step(data = res1 , aes(x = meansurp, y = rank), direction="vh") +
  xlab('Average Fusion') + ylab('Difference in Rank') +
  theme_minimal()

ggsave(paste("../result_plots/", lang, "_avg_tradeoff.pdf", sep = ""), width = 6, height = 4)
