#!/usr/bin/env python3
import glob
import multiprocessing
import os
from pathlib import Path

import run

if __name__ == "__main__":
    run.use_cores(multiprocessing.cpu_count() - 2)
    run.group("gen_base")

    real_world_input_files = [os.path.basename(
        f) for f in glob.glob("input/real-world-graphs/*")]

    run.add(
        "gen_real",
        "cp input/real-world-graphs/[[input_file]] [[output_file]]",
        {
            "seed": list(range(50)),
            "input_file": real_world_input_files,
            "output_file": "input/graphs/[[input_file]]_seed=[[seed]]"
        },
        creates_file="[[output_file]]"
    )

    run.add(
        "gen_hrg",
        "python3 gen_hrg.py --n [[n]] --k [[k]] --beta [[beta]] --seed [[seed]] [[file]]",
        {
            "n": [5000],
            "k": [25],
            "beta": [2.2, 2.6, 2.9],
            "seed": list(range(50)),
            "file": "input/graphs/hrg_n=[[n]]_k=[[k]]_beta=[[beta]]_seed=[[seed]]"
        },
        creates_file="[[file]]",
    )

    run.add(
        "gen_rgg",
        "python3 gen_rgg.py --n [[n]] --k [[k]] --seed [[seed]] [[file]]",
        {
            "n": [5000],
            "k": [10, 25, 50],
            "seed": list(range(50)),
            "file": "input/graphs/rgg_n=[[n]]_k=[[k]]_seed=[[seed]]"
        },
        creates_file="[[file]]",
    )

    run.run()

    run.group("noise")
    graph_files = [os.path.basename(f) for f in glob.glob("input/graphs/*")]
    run.add(
        "gen_noise",
        "python3 gen_noise.py --file input/graphs/[[graph]] --m [[additional_edges]] [[file]]",
        {
            "graph": graph_files,
            "additional_edges": [0.5, 1, 2, 3, 4, 5],
            "name": "[[graph]]_additionaledges=[[additional_edges]]",
            "file": "output/noisy_graphs/[[name]].csv"
        },
        stdout_file="output/noise_attributes.csv",
        header_string="graph,noisy_graph,additional_edges",
        stdout_res="[[graph]],[[name]],[[additional_edges]]",
    )

    run.run()

    run.group("measure")

    noisy_graph_files = [
        Path(f).stem for f in glob.glob("output/noisy_graphs/*")]

    run.add(
        "measure_stats",
        "python3 measure_stats.py --file output/noisy_graphs/[[file]].csv",
        {
            "file": noisy_graph_files,
        },
        stdout_file="output/graph_stats/[[file]].csv",
    )

    run.add(
        "measure_real_stats",
        "python3 measure_real_stats.py --no-header --file input/real-world-graphs/[[file]]",
        {
            "file": real_world_input_files,
        },
        stdout_file="output/real_world_graph_stats/results.csv",
        header_command="python3 measure_real_stats.py --only-header"
    )

    run.add(
        "measure_mixed_stats",
        "python3 measure_mixed_stats.py --file input/real-world-graphs/[[file]]",
        {
            "file": real_world_input_files,
        },
        stdout_file="output/mixed_graph_stats/[[file]].csv",
    )

    run.run()
    run.group("evaluate")

    stats_files = [Path(f).stem for f in glob.glob("output/graph_stats/*.csv")]

    run.add(
        "measure_auc",
        "python3 measure_auc.py --no-header --feature [[feature]] --file output/graph_stats/[[file]].csv",
        {
            "feature": ["common_neighbors"],
            "file": stats_files,
        },
        stdout_file="output/auc/results.csv",
        header_command="python3 measure_auc.py --only-header"
    )

    run.add(
        "measure_mixed_split",
        "python3 measure_mixed_split_stats.py --no-header --file output/mixed_graph_stats/[[file]].csv --ratio [[ratio]]",
        {
            "feature": ["common_neighbors"],
            "file": real_world_input_files,
            "ratio": list([x / 100 for x in range(0, 100 + 1, 5)]),
        },
        stdout_file="output/real_world_split_stats/[[file]].csv",
        header_command="python3 measure_mixed_split_stats.py --only-header"
    )

    run.run()
