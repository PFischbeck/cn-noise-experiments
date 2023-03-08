import argparse
import csv
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import roc_auc_score


def experiment(feature, filename, no_header, only_header):
    writer = csv.writer(sys.stdout)
    if not no_header:
        writer.writerow(['noisy_graph', 'feature', 'auc_score'])
    if only_header:
        return

    df = pd.read_csv(filename)

    X = df[[feature]]
    Y = 1 - df["is_random"]

    score = roc_auc_score(Y, X)

    writer.writerow([Path(filename).stem, feature, score])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Measure the AUC scores for a given feature and mixed graph.')
    parser.add_argument('--feature', type=str, help='Feature to use.')
    parser.add_argument('--file', type=str, help='Path to data file.')
    parser.add_argument('--no-header', action='store_true', help='Print no header.')
    parser.add_argument('--only-header', action='store_true', help='Print only the header.')

    args = parser.parse_args()
    if not args.only_header and not args.file:
        parser.error('--file is required if --only-header is not set.')
    experiment(args.feature, args.file, args.no_header, args.only_header)
