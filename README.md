# Code & Data for the paper "The Common-Neighbors Metric is Noise-Robust & Reveals Substructures of Real-World Networks"

## Description

This repository contains the code and data to replicate the experiments of our paper "The Common-Neighbors Metric is Noise-Robust & Reveals Substructures of Real-World Networks".

## Setup

- Make sure you have Python, Pip and R installed.
- Checkout the repository via

```
git clone https://github.com/PFischbeck/cn-noise-experiments.git
```

- Install the python dependencies with

```
pip3 install -r requirements.txt
```

- Install a submodule dependency for `run` with

```
git submodule init
git submodule update
cd run
pip3 install .
```

- Install the R dependencies (used for plots) with

```
R -e 'install.packages(c("ggplot2", "reshape2", "plyr", "dplyr"), repos="https://cloud.r-project.org/")'
```

## Running the experiments

You can run the experiments via

```
./runner.py gen_base noise measure evaluate
```

The resulting files (as CSVs) can be found in the `input` and `output` folders.

## Generating the plots

The plots can be generated with

```
Rscript R/auc-real-world.R
Rscript R/auc.R
Rscript R/mixed-split-stats.R
Rscript R/score-distribution.R
```

The resulting plots are in the `output/plots` folder.
