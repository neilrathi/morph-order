# morph-order
Code for "Explaining patterns of fusion in morphological paradigms using the memory--surprisal tradeoff" (at CogSci 2022)

Contact [neilrathi@gmail.com](mailto:neilrathi@gmail.com) for questions.

## Directory
* `model_run_2.py` is Python code for generating the fusion data for each pair of features
* `code` contains Python code for running experiments and plot generation
* `langs` contains data from each language
* `avg_rank_diff.csv` compares the difference in rank and fusion of all two-feature combinations per language
* `result_plots` contains tradeoff plots

## Requirements
* R. We used version 4.0.3. Analyses and plot generation require `tidyr`, `dplyr`, `ggplot2`, and `rPref`.
* Python 3.8
* GPU TensorFlow. We used version 2.2.0.
